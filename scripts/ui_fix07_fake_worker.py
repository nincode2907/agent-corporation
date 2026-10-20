"""Long-running fake transport for UI Fix 07's isolated browser regression only."""
import asyncio
from uuid import UUID

from agent_corporation_api.modules.execution import worker
from agent_corporation_api.modules.execution.gateway import CallOutcome
from agent_corporation_api.modules.observability.scope import CompanyScope


async def fake_transport(_base_url, _api_key, _payload, _timeout):
    await asyncio.sleep(30)
    return CallOutcome("completed", "synthetic_final_response", "Báo cáo tổng hợp từ fake transport.",
                       "00000000-0000-4000-8000-000000000501",
                       {"prompt_tokens": 7, "completion_tokens": 5, "total_tokens": 12})


async def main():
    stop = asyncio.Event()
    await worker.supervise(CompanyScope(UUID("b93f752e-7b69-5e8b-8f74-1498a15a5609"),
                                        UUID("b4375333-b12b-5fca-b984-87864032d3a8")),
                          stop_event=stop, transport=fake_transport,
                          gate_check=lambda _settings, _scope: {
                              "allowed": True, "mode": "demo-test", "verified": False,
                              "reason": "isolated_synthetic_transport_harness"})


asyncio.run(main())
