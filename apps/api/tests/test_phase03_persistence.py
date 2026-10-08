from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID, uuid4

import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session, sessionmaker

from agent_corporation_api.modules.observability.redaction import redact_structure
from agent_corporation_api.modules.observability.scope import CompanyScope, set_company_scope
from agent_corporation_api.modules.work import commands
from agent_corporation_api.modules.work.commands import (
    CompanyScopeNotFound,
    InvalidTaskTransition,
    StaleTaskState,
    create_work_order,
    transition_task,
)
from agent_corporation_api.settings import get_settings


@dataclass(frozen=True)
class ScopedFixture:
    scope: CompanyScope
    other_company_id: UUID
    other_environment_id: UUID


@pytest.fixture
def databases() -> tuple[sessionmaker[Session], sessionmaker[Session], object]:
    settings = get_settings()
    app_engine = create_engine(settings.database_url, pool_pre_ping=True)
    migration_engine = create_engine(settings.migration_database_url or settings.database_url, pool_pre_ping=True)
    yield sessionmaker(app_engine, expire_on_commit=False), sessionmaker(migration_engine, expire_on_commit=False), (app_engine, migration_engine)
    app_engine.dispose()
    migration_engine.dispose()


@pytest.fixture
def scoped_company(databases) -> ScopedFixture:
    _, migration_factory, _ = databases
    environment_id, company_id, other_company_id, other_environment_id = uuid4(), uuid4(), uuid4(), uuid4()
    with migration_factory.begin() as connection:
        connection.execute(
            text("INSERT INTO environments(id,name,kind,release_locked) VALUES (:id,:name,'demo',true),(:other_id,:other_name,'demo',true)"),
            {
                "id": environment_id,
                "name": f"phase03-test-{environment_id}",
                "other_id": other_environment_id,
                "other_name": f"phase03-other-{other_environment_id}",
            },
        )
        connection.execute(
            text("INSERT INTO companies(id,environment_id,name) VALUES (:id,:environment_id,:name)"),
            {"id": company_id, "environment_id": environment_id, "name": f"test-{company_id}"},
        )
        connection.execute(
            text("INSERT INTO companies(id,environment_id,name) VALUES (:id,:environment_id,:name),(:other_id,:other_environment_id,:other_name)"),
            {
                "id": other_company_id,
                "environment_id": environment_id,
                "name": f"other-{other_company_id}",
                "other_id": uuid4(),
                "other_environment_id": other_environment_id,
                "other_name": f"other-env-company-{other_environment_id}",
            },
        )
    yield ScopedFixture(CompanyScope(environment_id, company_id), other_company_id, other_environment_id)
    with migration_factory.begin() as connection:
        for test_environment_id in (environment_id, other_environment_id):
            for table in (
                "outbox_events", "events", "artifacts", "approvals", "checkpoints", "run_execution_state",
                "runs", "task_execution_state", "task_revisions", "work_orders", "event_stream_counters",
                "policies", "employee_versions", "employees", "departments", "companies",
            ):
                connection.execute(text(f"DELETE FROM {table} WHERE environment_id=:environment_id"), {"environment_id": test_environment_id})
            connection.execute(text("DELETE FROM environments WHERE id=:environment_id"), {"environment_id": test_environment_id})


def payload() -> dict[str, object]:
    return {
        "goal": "Tổng hợp tài liệu được cấp",
        "expected_outputs": ["Báo cáo có nguồn"],
        "acceptance_criteria": [{"id": "AC01", "description": "Có liên kết nguồn", "evidence_kind": "source_reference"}],
        "scope": {"input_refs": ["fixture/doc-a"], "tool_capabilities": []},
        "budget_limits": {"max_model_requests": 0, "cost_basis": "unknown"},
        "stop_conditions": {"max_duration_seconds": 120},
        "created_by": {"kind": "owner", "id": "owner-local"},
    }


def scoped_rows(factory: sessionmaker[Session], scope: CompanyScope, query: str, params: dict[str, object] | None = None):
    with factory() as session, session.begin():
        set_company_scope(session, scope)
        return session.execute(text(query), params or {}).mappings().all()


def test_app_role_is_non_privileged_and_rls_filters_other_company(databases, scoped_company) -> None:
    app_factory, migration_factory, _ = databases
    role = scoped_rows(app_factory, scoped_company.scope, "SELECT rolsuper, rolbypassrls FROM pg_roles WHERE rolname=current_user")
    assert role == [{"rolsuper": False, "rolbypassrls": False}]

    with migration_factory.begin() as connection:
        other_task_id = uuid4()
        connection.execute(
            text("INSERT INTO work_orders(id,environment_id,company_id,created_by) VALUES (:id,:environment_id,:company_id,'{}'::jsonb)"),
            {"id": other_task_id, "environment_id": scoped_company.scope.environment_id, "company_id": scoped_company.other_company_id},
        )
        other_environment_task_id = uuid4()
        other_environment_company_id = connection.execute(
            text("SELECT id FROM companies WHERE environment_id=:environment_id"),
            {"environment_id": scoped_company.other_environment_id},
        ).scalar_one()
        connection.execute(
            text("INSERT INTO work_orders(id,environment_id,company_id,created_by) VALUES (:id,:environment_id,:company_id,'{}'::jsonb)"),
            {
                "id": other_environment_task_id,
                "environment_id": scoped_company.other_environment_id,
                "company_id": other_environment_company_id,
            },
        )
    visible = scoped_rows(
        app_factory,
        scoped_company.scope,
        "SELECT id FROM work_orders WHERE company_id=:other_company_id",
        {"other_company_id": scoped_company.other_company_id},
    )
    assert visible == []
    visible_other_environment = scoped_rows(
        app_factory,
        scoped_company.scope,
        "SELECT id FROM work_orders WHERE environment_id=:environment_id",
        {"environment_id": scoped_company.other_environment_id},
    )
    assert visible_other_environment == []


def test_task_state_event_and_outbox_commit_dedup_and_fresh_connection(databases, scoped_company) -> None:
    app_factory, _, (app_engine, _) = databases
    first = create_work_order(app_factory, scope=scoped_company.scope, payload=payload(), dedup_key="acceptance:phase03:task-1")
    duplicate = create_work_order(app_factory, scope=scoped_company.scope, payload=payload(), dedup_key="acceptance:phase03:task-1")

    assert duplicate.duplicate is True
    assert duplicate.work_order_id == first.work_order_id
    assert duplicate.event_id == first.event_id
    assert first.stream_seq == 1

    fresh_engine = create_engine(get_settings().database_url, pool_pre_ping=True)
    try:
        fresh_factory = sessionmaker(fresh_engine, expire_on_commit=False)
        fresh = scoped_rows(
            fresh_factory,
            scoped_company.scope,
            """SELECT state.status, state.transition_version, event.stream_seq, outbox.status AS outbox_status
                 FROM task_execution_state AS state
                 JOIN events AS event ON event.task_id=state.task_id AND event.environment_id=state.environment_id AND event.company_id=state.company_id
                 JOIN outbox_events AS outbox ON outbox.event_id=event.event_id AND outbox.environment_id=event.environment_id AND outbox.company_id=event.company_id
                 WHERE state.task_id=:task_id""",
            {"task_id": first.work_order_id},
        )
    finally:
        fresh_engine.dispose()
    assert fresh == [{"status": "draft", "transition_version": 1, "stream_seq": 1, "outbox_status": "pending"}]

    next_version = transition_task(
        app_factory, scope=scoped_company.scope, task_id=first.work_order_id, target_status="queued",
        expected_version=1, actor={"kind": "owner", "id": "owner-local"}, dedup_key="acceptance:phase03:transition-1",
    )
    assert next_version == 2
    with pytest.raises(InvalidTaskTransition):
        transition_task(
            app_factory, scope=scoped_company.scope, task_id=first.work_order_id, target_status="accepted",
            expected_version=2, actor={"kind": "owner", "id": "owner-local"}, dedup_key="acceptance:phase03:invalid-transition",
        )
    with pytest.raises(StaleTaskState):
        transition_task(
            app_factory, scope=scoped_company.scope, task_id=first.work_order_id, target_status="planning",
            expected_version=1, actor={"kind": "owner", "id": "owner-local"}, dedup_key="acceptance:phase03:stale-transition",
        )
    state = scoped_rows(app_factory, scoped_company.scope, "SELECT status, transition_version FROM task_execution_state WHERE task_id=:task_id", {"task_id": first.work_order_id})
    assert state == [{"status": "queued", "transition_version": 2}]


def test_event_failure_rolls_back_work_order_revision_state_and_counter(databases, scoped_company, monkeypatch) -> None:
    app_factory, _, _ = databases

    def fail_after_state_write(*args, **kwargs):
        raise RuntimeError("simulated event store failure")

    monkeypatch.setattr(commands, "append_event", fail_after_state_write)
    with pytest.raises(RuntimeError, match="simulated event store failure"):
        create_work_order(app_factory, scope=scoped_company.scope, payload=payload(), dedup_key="acceptance:phase03:rollback")

    assert scoped_rows(app_factory, scoped_company.scope, "SELECT id FROM work_orders") == []
    assert scoped_rows(app_factory, scoped_company.scope, "SELECT task_id FROM task_execution_state") == []
    assert scoped_rows(app_factory, scoped_company.scope, "SELECT last_seq FROM event_stream_counters") == []


def test_secret_fields_are_redacted_before_event_and_revision_storage(databases, scoped_company) -> None:
    app_factory, _, _ = databases
    spec = payload()
    spec["goal"] = "Tổng hợp tài liệu; password=topsecret123"
    spec["scope"] = {"api_key": "private-key-value", "source": "Bearer abc.def.ghi"}
    result = create_work_order(app_factory, scope=scoped_company.scope, payload=spec, dedup_key="acceptance:phase03:redaction")
    revision = scoped_rows(app_factory, scoped_company.scope, "SELECT goal, scope::text AS scope FROM task_revisions WHERE task_id=:task_id", {"task_id": result.work_order_id})
    events = scoped_rows(app_factory, scoped_company.scope, "SELECT payload::text AS payload FROM events WHERE event_id=:event_id", {"event_id": result.event_id})
    assert "topsecret123" not in revision[0]["goal"]
    assert "private-key-value" not in revision[0]["scope"]
    assert "abc.def.ghi" not in revision[0]["scope"]
    assert "topsecret123" not in events[0]["payload"]
    assert redact_structure({"password": "never-store-this"}) == {"password": "[REDACTED]"}


def test_invalid_work_order_is_rejected_before_write(databases, scoped_company) -> None:
    app_factory, _, _ = databases
    invalid = payload()
    invalid["acceptance_criteria"] = []
    with pytest.raises(ValueError, match="acceptance_criteria"):
        create_work_order(app_factory, scope=scoped_company.scope, payload=invalid, dedup_key="acceptance:phase03:invalid")
    assert scoped_rows(app_factory, scoped_company.scope, "SELECT id FROM work_orders") == []
