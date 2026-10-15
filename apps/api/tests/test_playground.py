import asyncio
from types import SimpleNamespace
from uuid import uuid4

from fastapi.testclient import TestClient
import pytest

from agent_corporation_api.main import app
from agent_corporation_api.modules.demo.factory import DEMO_SCOPE
from agent_corporation_api.modules.execution.gateway import CallOutcome, parse_response
from agent_corporation_api.modules.governance import auth
from agent_corporation_api.modules.playground import router, service, worker


def test_policy_is_separate_and_demo_loopback_only():
    policy = service.gate(SimpleNamespace(codex_server_base_url='http://127.0.0.1:15600'), DEMO_SCOPE)
    assert policy['mode'] == 'development-playground' and policy['verified'] is False
    for url in ('http://example.com:15600', 'http://host.docker.internal:15600'):
        with pytest.raises(service.RuntimeDenied):
            service.gate(SimpleNamespace(codex_server_base_url=url), DEMO_SCOPE)
    with pytest.raises(service.RuntimeDenied):
        service.gate(SimpleNamespace(codex_server_base_url='http://127.0.0.1:15600'), None)


def test_history_keeps_only_bounded_explicit_completed_context():
    previous = [{'input_text': f'question {i}' + 'x' * 8000, 'output': 'y' * 8000} for i in range(20)]
    history = service.build_history({'display_name': 'Demo', 'role': 'fixture'}, previous, 'new')
    assert history[0]['role'] == 'system' and history[-1]['content'] == 'new'
    assert len(history) < 22 and 'question 0' not in str(history)


def test_anonymous_and_extra_tool_configuration_denied(monkeypatch):
    client = TestClient(app, base_url='http://127.0.0.1:15501')
    assert client.get('/api/v1/playground/sessions').status_code == 401
    principal = auth.OwnerPrincipal(DEMO_SCOPE, uuid4(), 'owner-local')
    app.dependency_overrides[auth.require_owner_write] = lambda: principal
    try:
        base = {'employee_id': str(uuid4()), 'profile_version': 1, 'max_requests': 5, 'expires_in_minutes': 30, 'accept_demo_policy': True, 'idempotency_key': str(uuid4())}
        for extra in ({'tools': ['terminal']}, {'fallback_models': ['other']}, {'network_tools': True}, {'max_concurrency': 2}):
            assert client.post('/api/v1/playground/sessions', json={**base, **extra}).status_code == 422
        for body in ({**base, 'accept_demo_policy': False}, {**base, 'max_requests': 101}, {**base, 'expires_in_minutes': 241}):
            assert client.post('/api/v1/playground/sessions', json=body).status_code == 422
        for extra in ('tools', 'model', 'effort', 'terminal', 'deploy', 'config'):
            body = {'input_text': 'fixture', 'idempotency_key': str(uuid4()), extra: True}
            assert client.post(f'/api/v1/playground/sessions/{uuid4()}/messages', json=body).status_code == 422
    finally:
        app.dependency_overrides.clear()


def test_csrf_required_for_playground_grant(monkeypatch):
    def owner(request):
        request.state.owner_csrf_hash = 'fixture'
        return auth.OwnerPrincipal(DEMO_SCOPE, uuid4(), 'owner-local')
    monkeypatch.setattr(auth, 'require_owner', owner)
    client = TestClient(app, base_url='http://127.0.0.1:15501')
    assert client.post('/api/v1/playground/sessions', json={}, headers={'Origin': 'http://127.0.0.1:15500'}).status_code == 403


def test_unauthorized_provider_tool_output_is_unknown():
    result = parse_response(200, {}, b'{"choices":[{"message":{"content":"ok","tool_calls":[{"name":"terminal"}]}}]}')
    assert result.status == 'unknown' and result.output is None


def test_managed_worker_starts_and_stops_with_api(monkeypatch):
    observed = []
    async def fake():
        observed.append('start')
        try:
            await asyncio.Event().wait()
        finally:
            observed.append('stop')
    monkeypatch.setenv('PLAYGROUND_WORKER_ENABLED', 'true')
    monkeypatch.setattr(worker, 'supervise', fake)
    with TestClient(app) as client:
        assert client.get('/api/v1/health/live').status_code == 200
    assert observed == ['start', 'stop']


def test_worker_payload_never_adopts_tools_and_missing_usage_stays_unknown(monkeypatch):
    captured, finished = [], []
    monkeypatch.setattr(service, 'should_stop', lambda *args: False)
    monkeypatch.setattr(service, 'finish', lambda *args: finished.append(args[-1]))
    async def transport(base, key, payload, timeout):
        captured.append(payload)
        return CallOutcome('completed', 'final_response', 'fixture')
    turn = {'profile_snapshot': {'model': 'fixture', 'reasoning_effort': 'low'}, 'history': [{'role': 'user', 'content': 'fixture'}], 'timeout_seconds': 1, 'tools': ['terminal'], 'fallback_models': ['other']}
    asyncio.run(worker.execute(None, DEMO_SCOPE, turn, SimpleNamespace(codex_server_base_url='http://127.0.0.1:15600', codex_server_api_key=None), transport))
    assert len(captured) == 1 and captured[0]['tools'] == [] and captured[0]['tool_choice'] == 'none'
    assert 'fallback_models' not in captured[0] and finished[0].usage is None


def test_supervisor_restarts_loop_after_fault_without_creating_grants(monkeypatch):
    attempts = []
    async def tick(*args):
        attempts.append(1)
        if len(attempts) == 1:
            raise RuntimeError('fixture crash')
        raise asyncio.CancelledError()
    monkeypatch.setattr(worker, 'tick', tick)
    monkeypatch.setattr(worker, 'get_session_factory', lambda: None)
    monkeypatch.setattr(worker, 'get_settings', lambda: None)
    with pytest.raises(asyncio.CancelledError):
        asyncio.run(worker.supervise())
    assert len(attempts) == 2 and worker.STATE['running'] is False
