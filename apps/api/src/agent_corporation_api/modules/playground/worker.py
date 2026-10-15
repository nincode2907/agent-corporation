"""App-owned worker. Only Playground jobs; never dispatches Work Orders."""
from __future__ import annotations

import asyncio
from datetime import UTC, datetime

from ...database import get_session_factory
from ...settings import get_settings
from ..demo.factory import DEMO_SCOPE
from ..execution.gateway import CallOutcome, post_text
from . import service

STATE = {'running': False, 'last_tick': None, 'error': None}


async def execute(factory, scope, turn, settings, transport=None):
    service.gate(settings, scope)
    profile = turn['profile_snapshot']
    payload = {'model': profile['model'], 'reasoning_effort': profile['reasoning_effort'],
               'messages': turn['history'], 'tools': [], 'tool_choice': 'none',
               'parallel_tool_calls': False, 'n': 1, 'stream': False}
    if await asyncio.to_thread(service.should_stop, factory, scope, turn):
        await asyncio.to_thread(service.finish, factory, scope, turn, CallOutcome('unknown', 'stop_before_http'))
        return
    task = asyncio.create_task((transport or post_text)(settings.codex_server_base_url, settings.codex_server_api_key, payload, turn['timeout_seconds']))
    beat = asyncio.get_running_loop().time()
    try:
        while not task.done():
            await asyncio.wait({task}, timeout=0.2)
            if await asyncio.to_thread(service.should_stop, factory, scope, turn):
                task.cancel()
                await asyncio.gather(task, return_exceptions=True)
                await asyncio.to_thread(service.finish, factory, scope, turn, CallOutcome('unknown', 'stop_or_expiry_http_closed'))
                return
            if asyncio.get_running_loop().time() - beat >= 5:
                await asyncio.to_thread(service.heartbeat, factory, scope, turn)
                beat = asyncio.get_running_loop().time()
        await asyncio.to_thread(service.finish, factory, scope, turn, await task)
    except asyncio.CancelledError:
        task.cancel()
        await asyncio.gather(task, return_exceptions=True)
        await asyncio.to_thread(service.finish, factory, scope, turn, CallOutcome('unknown', 'app_worker_shutdown_no_replay'))
        raise
    except Exception:
        task.cancel()
        await asyncio.gather(task, return_exceptions=True)
        await asyncio.to_thread(service.finish, factory, scope, turn, CallOutcome('unknown', 'worker_exception_no_replay'))


async def tick(factory, settings, transport=None):
    service.gate(settings, DEMO_SCOPE)
    await asyncio.to_thread(service.recover, factory, DEMO_SCOPE)
    turn = await asyncio.to_thread(service.reserve, factory, DEMO_SCOPE)
    if turn:
        await execute(factory, DEMO_SCOPE, turn, settings, transport)


async def supervise():
    STATE['running'] = True
    try:
        while True:
            try:
                await tick(get_session_factory(), get_settings())
                STATE.update(last_tick=datetime.now(UTC).isoformat(), error=None)
            except asyncio.CancelledError:
                raise
            except Exception:
                # No SQL, prompts, outputs, credentials or raw exception in logs/status.
                STATE['error'] = 'Worker đang chờ database/schema hoặc gateway cấu hình hợp lệ.'
            await asyncio.sleep(0.5)
    finally:
        STATE['running'] = False
