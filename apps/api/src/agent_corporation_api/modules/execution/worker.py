"""Explicit scoped worker; no startup, health, page-load or automatic inference."""
from __future__ import annotations
import argparse
import asyncio
import hashlib
import signal
from functools import partial
from uuid import UUID
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text
from ...database import get_session_factory
from ...settings import get_settings
from ..observability.scope import CompanyScope
from . import service
from .gateway import post_text, CallOutcome
from .gates import runtime_gate


async def execute_reserved(factory,scope,run,base_url,api_key,transport=post_text,stop_event=None):
    payload={"model":run["model"],"reasoning_effort":run["effort"],"messages":run["history"],"tools":[],"tool_choice":"none","parallel_tool_calls":False,"n":1,"stream":False}
    shutdown_requested=stop_event is not None and stop_event.is_set()
    if shutdown_requested or await asyncio.to_thread(service.should_stop,factory,scope,run):
        reason="worker_shutdown_before_http" if shutdown_requested else "stop_before_http_after_reservation"
        # The transport has not been invoked, so this is a known local failure,
        # not an uncertain gateway outcome. finish() releases the global guard.
        await asyncio.to_thread(service.finish,factory,scope,run,CallOutcome("failed",reason))
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
            if (stop_event is not None and stop_event.is_set()) or await asyncio.to_thread(service.should_stop,factory,scope,run):
                task.cancel()
                try:
                    await task
                except asyncio.CancelledError:
                    pass
                reason="worker_shutdown_http_closed" if stop_event is not None and stop_event.is_set() else "stop_or_grant_expiry_http_closed"
                await asyncio.to_thread(service.finish,factory,scope,run,CallOutcome("unknown",reason))
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


async def _idle(stop_event,poll_interval):
    if stop_event is None:
        await asyncio.sleep(poll_interval)
        return
    try:
        await asyncio.wait_for(stop_event.wait(),timeout=poll_interval)
    except TimeoutError:
        pass


async def work(scope,once=False,*,transport=post_text,gate_check=runtime_gate,stop_event=None,factory=None,poll_interval=0.5):
    settings=get_settings()
    factory=factory or get_session_factory()
    last_recovery=0.0
    while stop_event is None or not stop_event.is_set():
        now=asyncio.get_running_loop().time()
        if last_recovery==0.0 or now-last_recovery>=5:
            recovered=await asyncio.to_thread(service.recover_expired,factory,scope)
            last_recovery=now
            if recovered:
                print(f"Đã đối chiếu {recovered} call mất lease: unknown; không phát lại POST.",flush=True)
        proof=gate_check(settings, scope)
        if not proof["allowed"]:
            if once:
                print("CG01 blocked; không dispatch.",flush=True)
                return
            await _idle(stop_event,poll_interval)
            continue
        run=await asyncio.to_thread(service.reserve_next,factory,scope)
        if run:
            # Recheck trusted proof immediately before network; metadata may have changed since reservation.
            if not gate_check(settings, scope)["allowed"]:
                await asyncio.to_thread(service.finish,factory,scope,run,CallOutcome("failed","cg01_changed_after_reservation"))
                if once:
                    return
                continue
            await execute_reserved(factory,scope,run,settings.codex_server_base_url,settings.codex_server_api_key,
                                   transport=transport or partial(post_text, transport_mode=getattr(settings, "codex_server_transport", "loopback")),
                                   stop_event=stop_event)
        if once:
            return
        await _idle(stop_event,poll_interval)


async def supervise(scope,*,stop_event=None,transport=None,gate_check=runtime_gate,factory=None,poll_interval=0.5):
    """Run one demo-scope worker under a PostgreSQL session-level singleton lock."""
    factory=factory or get_session_factory()
    lock_key=int.from_bytes(hashlib.sha256(f"agent-corporation:runtime-worker:{scope.environment_id}:{scope.company_id}".encode()).digest()[:8],"big",signed=True)
    lock_session=factory()
    bind=lock_session.get_bind()
    lock_session.close()
    lock_connection=bind.connect()
    acquired=False
    try:
        acquired=bool(lock_connection.execute(text("SELECT pg_try_advisory_lock(:key)"),{"key":lock_key}).scalar_one())
        lock_connection.commit()
        if not acquired:
            print("Runtime worker đã có tiến trình active trong scope; tiến trình trùng không dispatch.",flush=True)
            return False
        await work(scope,transport=transport or post_text,gate_check=gate_check,stop_event=stop_event,factory=factory,poll_interval=poll_interval)
        return True
    finally:
        if acquired:
            try:
                lock_connection.execute(text("SELECT pg_advisory_unlock(:key)"),{"key":lock_key})
                lock_connection.commit()
            finally:
                lock_connection.close()
        else:
            lock_connection.close()


def main():
    parser=argparse.ArgumentParser(description="Worker text-only có grant riêng; mặc định không inference")
    parser.add_argument("--environment",type=UUID,required=True)
    parser.add_argument("--company",type=UUID,required=True)
    parser.add_argument("--once",action="store_true")
    args=parser.parse_args()
    try:
        async def run_supervised():
            stop_event=asyncio.Event()
            loop=asyncio.get_running_loop()
            for sig in (signal.SIGTERM,signal.SIGINT):
                try:
                    loop.add_signal_handler(sig,stop_event.set)
                except (NotImplementedError,RuntimeError):
                    pass
            if args.once:
                await work(CompanyScope(args.environment,args.company),once=True)
            else:
                await supervise(CompanyScope(args.environment,args.company),stop_event=stop_event)
        asyncio.run(run_supervised())
    except SQLAlchemyError:
        # A DB failure can contain input/history/output in SQL parameters. Halt without
        # logging them or replaying an uncertain POST; lease recovery remains explicit.
        parser.exit(1, "Cơ sở dữ liệu không khả dụng; worker đã dừng, không phát lại call.\n")

if __name__=="__main__":
    main()
