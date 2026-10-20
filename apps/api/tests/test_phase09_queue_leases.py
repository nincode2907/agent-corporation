"""Opt-in queue lease tests; requires an isolated PostgreSQL at migration head."""
import os
from concurrent.futures import ThreadPoolExecutor
from uuid import uuid4

import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from agent_corporation_api.modules.observability.scope import CompanyScope, set_company_scope
from agent_corporation_api.modules.work.commands import create_work_order
from agent_corporation_api.modules.work.queue import claim_next, heartbeat_claim, task_action
from agent_corporation_api.settings import get_settings

pytestmark = pytest.mark.skipif(
    os.getenv("PHASE_QUEUE_TEST_ISOLATED") != "1",
    reason="Requires opt-in isolated PostgreSQL at migration head; never mutates shared DB",
)


@pytest.fixture
def queue_db():
    settings = get_settings()
    app_engine = create_engine(settings.database_url, pool_pre_ping=True)
    admin_engine = create_engine(settings.migration_database_url, pool_pre_ping=True)
    factory = sessionmaker(app_engine, expire_on_commit=False)
    scope = CompanyScope(uuid4(), uuid4())
    with admin_engine.begin() as connection:
        connection.execute(
            text("INSERT INTO environments(id,name,kind) VALUES(:id,:name,'demo')"),
            {"id": scope.environment_id, "name": f"queue-fixture-{scope.environment_id}"},
        )
        connection.execute(
            text("INSERT INTO companies(id,environment_id,name) VALUES(:id,:env,'queue fixture')"),
            {"id": scope.company_id, "env": scope.environment_id},
        )
    yield factory, scope, admin_engine
    with admin_engine.begin() as connection:
        for table in (
            "task_command_receipts", "task_queue_entries", "outbox_events", "events",
            "event_stream_counters", "task_execution_state", "task_revisions", "work_orders",
            "companies",
        ):
            connection.execute(text(f"DELETE FROM {table} WHERE environment_id=:env"), {"env": scope.environment_id})
        connection.execute(text("DELETE FROM environments WHERE id=:env"), {"env": scope.environment_id})
    app_engine.dispose()
    admin_engine.dispose()


def enqueue(factory, scope, *, goal, priority=0):
    created = create_work_order(
        factory,
        scope=scope,
        payload={
            "goal": goal,
            "expected_outputs": ["Fixture output"],
            "acceptance_criteria": [{"id": "AC01", "description": "Owner checks output", "evidence_kind": "owner_review"}],
            "scope": {"input_refs": ["fixture:brief"], "tool_capabilities": []},
            "budget_limits": {"max_model_requests": 0, "cost_basis": "unknown"},
            "stop_conditions": {"max_duration_seconds": 60},
        },
        dedup_key=f"queue-fixture:{uuid4()}",
    )
    return task_action(
        factory, scope=scope, task_id=created.work_order_id, owner_id="fixture-owner",
        action="enqueue", expected_version=1, idempotency_key=uuid4(), priority=priority,
    )


def test_claim_race_enforces_company_concurrency_and_priority(queue_db):
    factory, scope, admin = queue_db
    enqueue(factory, scope, goal="low priority", priority=1)
    enqueue(factory, scope, goal="high priority", priority=9)

    with ThreadPoolExecutor(max_workers=8) as pool:
        claims = list(pool.map(lambda i: claim_next(factory, scope=scope, worker_id=f"worker-{i}"), range(8)))
    claimed = [claim for claim in claims if claim]
    assert len(claimed) == 1
    lease = claimed[0]

    with factory() as session, session.begin():
        set_company_scope(session, scope)
        row = session.execute(text("""SELECT q.priority,q.claim_count,s.status FROM task_queue_entries q
            JOIN task_execution_state s USING(environment_id,company_id,task_id)
            WHERE q.task_id=:task_id"""), {"task_id": lease["task_id"]}).mappings().one()
        assert row["priority"] == 9
        assert row["claim_count"] == 1
        assert row["status"] == "queued"
        assert session.execute(text("SELECT count(*) FROM runs WHERE environment_id=:env AND company_id=:company"),
            {"env": scope.environment_id, "company": scope.company_id}).scalar_one() == 0
    assert claim_next(factory, scope=scope, worker_id="over-cap") is None
    assert heartbeat_claim(factory, scope=scope, task_id=lease["task_id"], worker_id=lease["worker_id"], lease_token=uuid4()) is False
    assert heartbeat_claim(factory, scope=scope, task_id=lease["task_id"], worker_id=lease["worker_id"], lease_token=lease["lease_token"]) is True


def test_pause_fences_worker_and_expired_lease_is_reclaimed(queue_db):
    factory, scope, admin = queue_db
    enqueued = enqueue(factory, scope, goal="safe requeue")
    task_id = enqueued["task_id"]
    lease = claim_next(factory, scope=scope, worker_id="old-worker", lease_seconds=5)
    assert lease and str(lease["task_id"]) == task_id

    task_action(factory, scope=scope, task_id=lease["task_id"], owner_id="fixture-owner",
        action="pause", expected_version=2, idempotency_key=uuid4())
    assert heartbeat_claim(factory, scope=scope, task_id=lease["task_id"], worker_id="old-worker", lease_token=lease["lease_token"]) is False
    assert claim_next(factory, scope=scope, worker_id="paused-worker") is None

    task_action(factory, scope=scope, task_id=lease["task_id"], owner_id="fixture-owner",
        action="resume", expected_version=3, idempotency_key=uuid4())
    reclaimed = claim_next(factory, scope=scope, worker_id="new-worker", lease_seconds=5)
    assert reclaimed and reclaimed["task_id"] == lease["task_id"]
    assert reclaimed["claim_count"] == 2
    assert reclaimed["lease_token"] != lease["lease_token"]
    assert heartbeat_claim(factory, scope=scope, task_id=lease["task_id"], worker_id="old-worker", lease_token=lease["lease_token"]) is False

    with admin.begin() as connection:
        connection.execute(text("""UPDATE task_queue_entries SET lease_until=CURRENT_TIMESTAMP-interval '1 second'
            WHERE environment_id=:env AND company_id=:company AND task_id=:task"""),
            {"env": scope.environment_id, "company": scope.company_id, "task": lease["task_id"]})
    next_claim = claim_next(factory, scope=scope, worker_id="recovery-worker", lease_seconds=5)
    assert next_claim and next_claim["task_id"] == lease["task_id"]
    assert next_claim["claim_count"] == 3
    assert next_claim["lease_token"] != reclaimed["lease_token"]
