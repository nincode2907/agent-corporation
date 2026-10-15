"""Real PostgreSQL transactions and worker tests; all transports are fake, no inference."""
import asyncio
from concurrent.futures import ThreadPoolExecutor
from datetime import UTC, datetime, timedelta
import os
from pathlib import Path
import subprocess
import sys
from types import SimpleNamespace
from uuid import uuid4

import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.engine import make_url
from sqlalchemy.orm import sessionmaker

from agent_corporation_api.settings import get_settings
from agent_corporation_api.modules.demo.factory import DEMO_SCOPE
from agent_corporation_api.modules.governance.auth import OwnerPrincipal
from agent_corporation_api.modules.observability.scope import CompanyScope, set_company_scope
from agent_corporation_api.modules.execution.gateway import CallOutcome
from agent_corporation_api.modules.playground import service, worker

pytestmark = pytest.mark.skipif(os.getenv('PLAYGROUND_TEST_ISOLATED') != '1', reason='Disposable PostgreSQL runner required')
SETTINGS = SimpleNamespace(codex_server_base_url='http://127.0.0.1:15600', codex_server_api_key=None)


@pytest.fixture
def pg():
    settings = get_settings()
    assert make_url(settings.database_url).database.startswith('ac_pgtest_')
    admin = create_engine(settings.migration_database_url)
    engine = create_engine(settings.database_url)
    factory = sessionmaker(engine, expire_on_commit=False)
    auth, employee, version = uuid4(), uuid4(), uuid4()
    scope = DEMO_SCOPE
    with admin.begin() as db:
        db.execute(text("INSERT INTO environments(id,name,kind) VALUES(:env,'playground fixture','demo') ON CONFLICT DO NOTHING"), {'env': scope.environment_id})
        db.execute(text("INSERT INTO companies(id,environment_id,name) VALUES(:company,:env,'fixture') ON CONFLICT DO NOTHING"), {'company': scope.company_id, 'env': scope.environment_id})
        db.execute(text("INSERT INTO owner_model_profiles(environment_id,company_id,version,model,reasoning_effort) VALUES(:env,:company,1,'fixture-model','medium') ON CONFLICT(environment_id,company_id) DO UPDATE SET version=1,model='fixture-model',reasoning_effort='medium'"), {'company': scope.company_id, 'env': scope.environment_id})
        db.execute(text("INSERT INTO owner_sessions(id,owner_id,environment_id,company_id,token_hash,csrf_hash,expires_at) VALUES(:id,'owner-local',:env,:company,:token,'fixture',CURRENT_TIMESTAMP+interval '1 hour')"), {'id': auth, 'env': scope.environment_id, 'company': scope.company_id, 'token': uuid4().hex})
        db.execute(text("INSERT INTO employees(id,environment_id,company_id,lifecycle) VALUES(:id,:env,:company,'active')"), {'id': employee, 'env': scope.environment_id, 'company': scope.company_id})
        db.execute(text("INSERT INTO employee_versions(id,environment_id,company_id,employee_id,version,profile) VALUES(:id,:env,:company,:employee,1,'{\"display_name\":\"Fixture employee\",\"role\":\"Analyst\"}')"), {'id': version, 'env': scope.environment_id, 'company': scope.company_id, 'employee': employee})
    principal = OwnerPrincipal(scope, auth, 'owner-local')
    yield factory, principal, employee, admin
    with admin.begin() as db:
        db.execute(text('DELETE FROM playground_turns'))
        db.execute(text('DELETE FROM playground_sessions'))
        db.execute(text('UPDATE runtime_dispatch_guard SET request_span_id=NULL,environment_id=NULL,company_id=NULL WHERE environment_id=:env'), {'env': scope.environment_id})
    engine.dispose(); admin.dispose()


def create(pg, max_requests=5, **extra):
    factory, principal, employee, _ = pg
    return service.create_session(factory, DEMO_SCOPE, principal, {'employee_id': employee, 'profile_version': 1, 'max_requests': max_requests, 'expires_in_minutes': 30, 'timeout_seconds': 1, 'accept_demo_policy': True, 'idempotency_key': uuid4(), **extra})


def send(pg, session, key=None, content='fixture input'):
    return service.send(pg[0], DEMO_SCOPE, session['id'], {'input_text': content, 'idempotency_key': key or uuid4()})


def sql(pg, command, **params):
    with pg[3].begin() as db:
        result = db.execute(text(command), params)
        return result.mappings().all() if result.returns_rows else None


def test_multi_turn_history_snapshots_usage_unknown_and_work_order_isolation(pg):
    original_orders = sql(pg, 'SELECT count(*) AS n FROM work_orders')[0]['n']
    original_calls = sql(pg, 'SELECT count(*) AS n FROM model_calls')[0]['n']
    session = create(pg)
    first = send(pg, session, content='first')
    async def transport(base, key, payload, timeout):
        assert payload['model'] == 'fixture-model' and payload['tools'] == []
        return CallOutcome('completed', 'fixture', 'answer one', 'fixture-call', None)
    asyncio.run(worker.tick(pg[0], SETTINGS, transport))
    detail = service.detail(pg[0], DEMO_SCOPE, session['id'])
    assert detail['turns'][0]['status'] == 'completed' and detail['turns'][0]['usage'] is None
    assert detail['turns'][0]['usage_provenance'] == 'unknown'
    sql(pg, "UPDATE owner_model_profiles SET version=2,model='changed' WHERE company_id=:id", id=DEMO_SCOPE.company_id)
    second = send(pg, session, content='second')
    async def second_transport(base, key, payload, timeout):
        assert payload['model'] == 'fixture-model'
        assert [m['content'] for m in payload['messages'][1:]] == ['first', 'answer one', 'second']
        return CallOutcome('completed', 'fixture', 'answer two', 'fixture-call-2', {'prompt_tokens': 3, 'completion_tokens': 4, 'total_tokens': 7})
    asyncio.run(worker.tick(pg[0], SETTINGS, second_transport))
    detail = service.detail(pg[0], DEMO_SCOPE, session['id'])
    assert detail['session']['used_requests'] == 2
    assert detail['turns'][1]['usage']['total_tokens'] == 7
    assert all(t['profile_snapshot']['version'] == 1 for t in detail['turns'])
    assert len([e for e in detail['events'] if e['event_type'] == 'PLAYGROUND_CALL_FINISHED']) == 2
    assert sql(pg, 'SELECT count(*) AS n FROM work_orders')[0]['n'] == original_orders
    assert sql(pg, 'SELECT count(*) AS n FROM model_calls')[0]['n'] == original_calls


def test_session_and_send_idempotency_concurrent_duplicate_and_concurrency(pg):
    factory, principal, employee, _ = pg
    spec = {'employee_id': employee, 'profile_version': 1, 'max_requests': 5, 'expires_in_minutes': 30, 'timeout_seconds': 1, 'accept_demo_policy': True, 'idempotency_key': uuid4()}
    session = service.create_session(factory, DEMO_SCOPE, principal, spec)
    assert service.create_session(factory, DEMO_SCOPE, principal, spec)['id'] == session['id']
    with pytest.raises(service.RuntimeDenied, match='idempotency_payload_mismatch'):
        service.create_session(factory, DEMO_SCOPE, principal, {**spec, 'max_requests': 6})
    key = uuid4()
    with ThreadPoolExecutor(max_workers=4) as pool:
        turns = list(pool.map(lambda _: send(pg, session, key), range(4)))
    assert len({t['id'] for t in turns}) == 1
    with pytest.raises(service.RuntimeDenied, match='idempotency_payload_mismatch'):
        send(pg, session, key, 'different')
    with pytest.raises(service.RuntimeDenied, match='concurrency'):
        send(pg, session)
    with ThreadPoolExecutor(max_workers=4) as pool:
        calls = list(pool.map(lambda _: service.reserve(factory, DEMO_SCOPE), range(4)))
    assert sum(call is not None for call in calls) == 1
    assert service.detail(factory, DEMO_SCOPE, session['id'])['session']['used_requests'] == 1


def test_expired_grant_before_send_and_before_dispatch_never_calls(pg):
    session = create(pg)
    sql(pg, "UPDATE playground_sessions SET expires_at=CURRENT_TIMESTAMP-interval '1 second' WHERE id=:id", id=session['id'])
    with pytest.raises(service.RuntimeDenied, match='expired'):
        send(pg, session)
    second = create(pg)
    send(pg, second)
    sql(pg, "UPDATE playground_sessions SET expires_at=CURRENT_TIMESTAMP-interval '1 second' WHERE id=:id", id=second['id'])
    called = []
    async def transport(*args):
        called.append(1)
    asyncio.run(worker.tick(pg[0], SETTINGS, transport))
    detail = service.detail(pg[0], DEMO_SCOPE, second['id'])
    assert not called and detail['session']['used_requests'] == 0 and detail['turns'][0]['status'] == 'cancelled'


def test_limit_exceeded_and_replay_same_key_does_not_spend_again(pg):
    session = create(pg, max_requests=1)
    key = uuid4()
    turn = send(pg, session, key)
    reserved = service.reserve(pg[0], DEMO_SCOPE)
    service.finish(pg[0], DEMO_SCOPE, reserved, CallOutcome('completed', 'fixture', 'answer'))
    assert send(pg, session, key)['id'] == turn['id']
    with pytest.raises(service.RuntimeDenied, match='limit_exceeded'):
        send(pg, session)
    assert service.reserve(pg[0], DEMO_SCOPE) is None


def test_stop_queued_and_revoke_are_durable_without_dispatch(pg):
    session = create(pg)
    send(pg, session)
    service.stop(pg[0], DEMO_SCOPE, session['id'])
    service.stop(pg[0], DEMO_SCOPE, session['id'])
    assert service.detail(pg[0], DEMO_SCOPE, session['id'])['turns'][0]['status'] == 'cancelled'
    assert service.reserve(pg[0], DEMO_SCOPE) is None
    assert service.detail(pg[0], DEMO_SCOPE, session['id'])['session']['used_requests'] == 0
    service.stop(pg[0], DEMO_SCOPE, session['id'], revoke=True)
    with pytest.raises(service.RuntimeDenied, match='revoked'):
        send(pg, session)


@pytest.mark.parametrize('reason', ['stop', 'expiry', 'logout'])
def test_in_flight_stop_expiry_logout_close_transport_unknown_and_no_retry(pg, reason):
    session = create(pg)
    send(pg, session)
    reserved = service.reserve(pg[0], DEMO_SCOPE)
    calls, cancellations = [], []
    async def run():
        started = asyncio.Event()
        async def transport(*args):
            calls.append(1); started.set()
            try:
                await asyncio.Event().wait()
            finally:
                cancellations.append(1)
        task = asyncio.create_task(worker.execute(pg[0], DEMO_SCOPE, reserved, SETTINGS, transport))
        await started.wait()
        if reason == 'stop':
            await asyncio.to_thread(service.stop, pg[0], DEMO_SCOPE, session['id'])
        elif reason == 'expiry':
            sql(pg, "UPDATE playground_sessions SET expires_at=CURRENT_TIMESTAMP-interval '1 second' WHERE id=:id", id=session['id'])
        else:
            sql(pg, 'UPDATE owner_sessions SET revoked_at=CURRENT_TIMESTAMP WHERE id=:id', id=pg[1].session_id)
        await asyncio.wait_for(task, 3)
    asyncio.run(run())
    result = service.detail(pg[0], DEMO_SCOPE, session['id'])
    assert calls == [1] and cancellations == [1] and result['turns'][0]['status'] == 'unknown'
    assert result['session']['used_requests'] == 1 and result['turns'][0]['usage'] is None
    assert service.reserve(pg[0], DEMO_SCOPE) is None


def test_worker_crash_restart_fences_late_completion_keeps_unknown_guard_and_consumed_request(pg):
    session = create(pg)
    turn = send(pg, session)
    reserved = service.reserve(pg[0], DEMO_SCOPE)
    sql(pg, "UPDATE playground_turns SET lease_until=CURRENT_TIMESTAMP-interval '1 second' WHERE id=:id", id=turn['id'])
    assert service.recover(pg[0], DEMO_SCOPE) == 1
    assert service.recover(pg[0], DEMO_SCOPE) == 0
    service.finish(pg[0], DEMO_SCOPE, reserved, CallOutcome('completed', 'stale', 'must not overwrite'))
    result = service.detail(pg[0], DEMO_SCOPE, session['id'])
    assert result['turns'][0]['status'] == 'unknown' and result['turns'][0]['output'] is None
    called = []
    async def transport(*args):
        called.append(1)
    asyncio.run(worker.tick(pg[0], SETTINGS, transport))
    assert called == []
    with pytest.raises(service.RuntimeDenied, match='concurrency_or_unknown'):
        send(pg, session)
    service.resolve_unknown(pg[0], DEMO_SCOPE, session['id'], turn['id'])
    assert service.detail(pg[0], DEMO_SCOPE, session['id'])['session']['used_requests'] == 1
    assert service.detail(pg[0], DEMO_SCOPE, session['id'])['turns'][0]['status'] == 'unknown'
    send(pg, session, content='new intentional turn')
    assert service.reserve(pg[0], DEMO_SCOPE) is not None


def test_rls_fail_closed_scope_and_profile_policy_acceptance(pg):
    session = create(pg)
    with pg[0]() as db, db.begin():
        assert db.execute(text('SELECT count(*) FROM playground_sessions')).scalar_one() == 0
        set_company_scope(db, CompanyScope(uuid4(), uuid4()))
        assert db.execute(text('SELECT count(*) FROM playground_sessions')).scalar_one() == 0
    with pytest.raises(service.RuntimeDenied, match='policy_acceptance'):
        create(pg, accept_demo_policy=False)
    with pytest.raises(service.RuntimeDenied, match='save_profile'):
        create(pg, profile_version=2)
    with pytest.raises(service.RuntimeDenied, match='demo_only'):
        service.create_session(pg[0], CompanyScope(uuid4(), uuid4()), pg[1], {})


def test_real_worker_process_crash_and_new_process_recovery_never_replays(pg):
    session = create(pg)
    turn = send(pg, session)
    source = str(Path(__file__).resolve().parents[1] / 'src')
    bootstrap = f"import sys;sys.path.insert(0,{source!r});from agent_corporation_api.database import get_session_factory;from agent_corporation_api.modules.demo.factory import DEMO_SCOPE;from agent_corporation_api.modules.playground import service,worker;"
    crashed = subprocess.run([sys.executable, '-c', bootstrap + "import os;assert service.reserve(get_session_factory(),DEMO_SCOPE);os._exit(19)"], capture_output=True)
    assert crashed.returncode == 19
    sql(pg, "UPDATE playground_turns SET lease_until=CURRENT_TIMESTAMP-interval '1 second' WHERE id=:id", id=turn['id'])
    restart = bootstrap + '''
import asyncio
from types import SimpleNamespace
calls=[]
async def fake(*args):
    calls.append(1)
asyncio.run(worker.tick(get_session_factory(),SimpleNamespace(codex_server_base_url='http://127.0.0.1:15600',codex_server_api_key=None),fake))
assert not calls
'''
    recovered = subprocess.run([sys.executable, '-c', restart], capture_output=True)
    assert recovered.returncode == 0
    detail = service.detail(pg[0], DEMO_SCOPE, session['id'])
    assert detail['turns'][0]['status'] == 'unknown' and detail['session']['used_requests'] == 1


def test_grant_effective_expiry_is_bounded_by_owner_session(pg):
    expiry = datetime.now(UTC) + timedelta(minutes=2)
    sql(pg, 'UPDATE owner_sessions SET expires_at=:expiry WHERE id=:id', id=pg[1].session_id, expiry=expiry)
    session = create(pg, expires_in_minutes=240)
    assert session['expires_at'] == expiry


def test_work_order_runtime_and_playground_share_capacity_without_dispatching_each_others_jobs(pg):
    from agent_corporation_api.modules.execution import service as runtime
    spec = {'phase': '06', 'batch_id': 'fixture-cross-lane', 'purpose': 'fixture only', 'model': 'fixture-model', 'effort': 'medium', 'max_requests': 1, 'max_concurrency': 1, 'timeout_seconds': 1, 'max_requeues': 0, 'expires_at': datetime.now(UTC)+timedelta(minutes=5)}
    grant = runtime.grant_create(pg[0], DEMO_SCOPE, 'owner-local', spec)
    run_id = runtime.run_create(pg[0], DEMO_SCOPE, 'owner-local', {**{k: spec[k] for k in ('phase', 'batch_id', 'purpose', 'model', 'effort')}, 'grant_id': grant['id'], 'input_text': 'fixture work order', 'idempotency_key': uuid4()})
    session = create(pg)
    send(pg, session)
    turn = service.reserve(pg[0], DEMO_SCOPE)
    assert runtime.reserve_next(pg[0], DEMO_SCOPE) is None
    service.finish(pg[0], DEMO_SCOPE, turn, CallOutcome('completed', 'fixture', 'playground output'))
    # Playground tick never picks the queued Work Order even when capacity is free.
    called = []
    async def transport(*args):
        called.append(1)
    asyncio.run(worker.tick(pg[0], SETTINGS, transport))
    assert called == [] and runtime.run_get(pg[0], DEMO_SCOPE, run_id)['status'] == 'queued'
    work = runtime.reserve_next(pg[0], DEMO_SCOPE)
    assert work['id'] == run_id and service.reserve(pg[0], DEMO_SCOPE) is None
    runtime.finish(pg[0], DEMO_SCOPE, work, CallOutcome('completed', 'fixture', 'work order output'))
    assert runtime.run_get(pg[0], DEMO_SCOPE, run_id)['status'] == 'completed'
