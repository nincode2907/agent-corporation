"""Explicit scoped worker; no startup, health, page-load or automatic inference."""
from __future__ import annotations
import argparse
import asyncio
from uuid import UUID
from sqlalchemy.exc import SQLAlchemyError
from ...database import get_session_factory
from ...settings import get_settings
from ..observability.scope import CompanyScope
from . import service
from .gateway import post_text, CallOutcome
from .gates import check_gate


async def execute_reserved(factory,scope,run,base_url,api_key,transport=post_text):
    payload={"model":run["model"],"reasoning_effort":run["effort"],"messages":run["history"],"tools":[],"tool_choice":"none","parallel_tool_calls":False,"n":1,"stream":False}
    if await asyncio.to_thread(service.should_stop,factory,scope,run):
        await asyncio.to_thread(service.finish,factory,scope,run,CallOutcome("unknown","stop_before_http_after_reservation"))
        return
    task=asyncio.create_task(transport(base_url,api_key,payload,run["timeout_seconds"]))
    last_heartbeat=asyncio.get_running_loop().time()
    try:
        while not task.done():
            await asyncio.wait({task},timeout=0.2)
            now=asyncio.get_running_loop().time()
            if now-last_heartbeat>=10:
                await asyncio.to_thread(service.heartbeat,factory,scope,run)
                last_heartbeat=now
            if await asyncio.to_thread(service.should_stop,factory,scope,run):
                task.cancel()
                try:
                    await task
                except asyncio.CancelledError:
                    pass
                await asyncio.to_thread(service.finish,factory,scope,run,CallOutcome("unknown","stop_or_grant_expiry_http_closed"))
                return
        outcome=await task
        await asyncio.to_thread(service.finish,factory,scope,run,outcome)
    except asyncio.CancelledError:
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            pass
        await asyncio.to_thread(service.finish,factory,scope,run,CallOutcome("unknown","worker_cancelled_http_closed"))
        raise
    except Exception:
        # Never replay after a local exception because the POST may already have reached Codex.
        await asyncio.to_thread(service.finish,factory,scope,run,CallOutcome("unknown","worker_exception"))


async def work(scope,once=False):
    settings=get_settings()
    factory=get_session_factory()
    while True:
        recovered=await asyncio.to_thread(service.recover_expired,factory,scope)
        if recovered:
            print(f"Đã đối chiếu {recovered} call mất lease: unknown; không phát lại POST.",flush=True)
        proof=check_gate(settings.runtime_gate_path,settings.runtime_gateway_source_path,base_url=settings.codex_server_base_url)
        if not proof["allowed"]:
            print("CG01 blocked; không dispatch.",flush=True)
            return
        run=await asyncio.to_thread(service.reserve_next,factory,scope)
        if run:
            # Recheck trusted proof immediately before network; metadata may have changed since reservation.
            if not check_gate(settings.runtime_gate_path,settings.runtime_gateway_source_path,base_url=settings.codex_server_base_url)["allowed"]:
                await asyncio.to_thread(service.finish,factory,scope,run,CallOutcome("unknown","cg01_changed_after_reservation"))
                return
            await execute_reserved(factory,scope,run,settings.codex_server_base_url,settings.codex_server_api_key)
        if once:
            return
        await asyncio.sleep(0.5)


def main():
    parser=argparse.ArgumentParser(description="Worker text-only có grant riêng; mặc định không inference")
    parser.add_argument("--environment",type=UUID,required=True)
    parser.add_argument("--company",type=UUID,required=True)
    parser.add_argument("--once",action="store_true")
    args=parser.parse_args()
    try:
        asyncio.run(work(CompanyScope(args.environment,args.company),args.once))
    except SQLAlchemyError:
        # A DB failure can contain input/history/output in SQL parameters. Halt without
        # logging them or replaying an uncertain POST; lease recovery remains explicit.
        parser.exit(1, "Cơ sở dữ liệu không khả dụng; worker đã dừng, không phát lại call.\n")

if __name__=="__main__":
    main()
