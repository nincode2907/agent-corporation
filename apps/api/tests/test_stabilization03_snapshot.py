"""PostgreSQL evidence for scoped, watermark-consistent observability snapshots."""
from __future__ import annotations

from uuid import uuid4

import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient
from sqlalchemy import event, text

from test_phase03_persistence import databases, scoped_company
from agent_corporation_api.main import app
from agent_corporation_api.modules.governance.auth import OwnerPrincipal, require_owner
from agent_corporation_api.modules.observability import router as events_router
from agent_corporation_api.modules.observability.events import append_event
from agent_corporation_api.modules.observability.feed import (
    CursorError,
    read_event_page,
    read_snapshot,
)
from agent_corporation_api.modules.observability.scope import CompanyScope, set_company_scope


def append(factory, scope: CompanyScope, label: str):
    with factory() as session, session.begin():
        set_company_scope(session, scope)
        return append_event(
            session, scope=scope, event_type="RUN_STATE_CHANGED", task_id=None, run_id=None,
            correlation_id=uuid4(), parent_event_id=None, source="app", actor={"kind": "system"},
            sensitivity="internal", payload={"to": label}, evidence_refs=[],
            dedup_key=f"stabilization03:{uuid4()}",
        )


def test_snapshot_is_scoped_bounded_and_read_only(databases, scoped_company, monkeypatch):
    factory, admin, _ = databases
    scope = scoped_company.scope
    other = CompanyScope(scope.environment_id, scoped_company.other_company_id)
    visible = append(factory, scope, "visible")
    hidden = append(factory, other, "hidden")
    principal = OwnerPrincipal(scope=scope, session_id=uuid4(), owner_id="snapshot-test-owner")
    monkeypatch.setattr(events_router, "get_session_factory", lambda: factory)
    monkeypatch.setattr(events_router, "cursor_signing_key", lambda: b"snapshot-fixture-key")
    monkeypatch.setitem(app.dependency_overrides, require_owner, lambda: principal)
    before = admin()
    with before as session:
        event_count = session.execute(text("SELECT count(*) FROM events WHERE environment_id=:env AND company_id=:company"),
                                      {"env": scope.environment_id, "company": scope.company_id}).scalar_one()
        call_count = session.execute(text("SELECT count(*) FROM model_calls WHERE environment_id=:env AND company_id=:company"),
                                     {"env": scope.environment_id, "company": scope.company_id}).scalar_one()
    response = TestClient(app).get("/api/v1/events/snapshot-v1")
    assert response.status_code == 200
    snapshot = response.json()
    assert snapshot["version"] == 1
    assert snapshot["watermark_seq"] == visible.stream_seq
    assert [row["event_id"] for row in snapshot["events"]] == [str(visible.event_id)]
    assert str(hidden.event_id) not in response.text
    assert snapshot["history_gap"] is False
    assert snapshot["replay_window_start_seq"] == 1
    assert snapshot["cursor"]
    assert len(response.content) <= events_router.SNAPSHOT_MAX_BYTES if hasattr(events_router, "SNAPSHOT_MAX_BYTES") else len(response.content) <= 512 * 1024
    after = admin()
    with after as session:
        assert session.execute(text("SELECT count(*) FROM events WHERE environment_id=:env AND company_id=:company"),
                               {"env": scope.environment_id, "company": scope.company_id}).scalar_one() == event_count
        assert session.execute(text("SELECT count(*) FROM model_calls WHERE environment_id=:env AND company_id=:company"),
                               {"env": scope.environment_id, "company": scope.company_id}).scalar_one() == call_count


def test_snapshot_watermark_survives_concurrent_commit(databases, scoped_company):
    factory, _, engines = databases
    scope = scoped_company.scope
    app_engine, _ = engines
    before = append(factory, scope, "before")
    committed = []
    injected = False

    def commit_after_watermark(_conn, _cursor, statement, _parameters, _context, _many):
        nonlocal injected
        if not injected and "SELECT last_seq FROM event_stream_counters" in statement:
            injected = True
            committed.append(append(factory, scope, "concurrent"))

    event.listen(app_engine, "after_cursor_execute", commit_after_watermark)
    try:
        snapshot = read_snapshot(factory, scope=scope, session_id="snapshot-race", key=b"snapshot-race-key")
    finally:
        event.remove(app_engine, "after_cursor_execute", commit_after_watermark)
    assert injected and committed
    assert snapshot["watermark_seq"] == before.stream_seq
    assert [row["stream_seq"] for row in snapshot["events"]] == [before.stream_seq]
    replay = read_event_page(factory, scope=scope, session_id="snapshot-race", key=b"snapshot-race-key",
                             cursor=snapshot["cursor"])
    assert [row["stream_seq"] for row in replay["events"]] == [committed[0].stream_seq]


def test_retained_snapshot_marks_unrecoverable_replay_history_and_cursor_is_bound(databases, scoped_company):
    factory, admin, _ = databases
    scope = scoped_company.scope
    first = append(factory, scope, "first")
    append(factory, scope, "second")
    last = append(factory, scope, "last")
    with admin.begin() as session:
        session.execute(text("DELETE FROM outbox_events WHERE event_id IN (:a,:b)"),
                        {"a": first.event_id, "b": uuid4()})
        # A retained source can be sparse after retention; the counter remains monotonic.
        session.execute(text("DELETE FROM events WHERE event_id=:id"), {"id": first.event_id})
        session.execute(text("DELETE FROM outbox_events WHERE event_id=(SELECT event_id FROM events WHERE company_id=:company AND stream_seq=2)"),
                        {"company": scope.company_id})
        session.execute(text("DELETE FROM events WHERE company_id=:company AND stream_seq=2"), {"company": scope.company_id})
    key = b"snapshot-retention-key"
    snapshot = read_snapshot(factory, scope=scope, session_id="owner-a", key=key)
    assert snapshot["watermark_seq"] == last.stream_seq
    assert snapshot["first_retained_seq"] == last.stream_seq
    assert snapshot["history_gap"] is True
    assert [row["stream_seq"] for row in snapshot["events"]] == [last.stream_seq]
    assert read_event_page(factory, scope=scope, session_id="owner-a", key=key, cursor=snapshot["cursor"])["events"] == []
    with pytest.raises(CursorError):
        read_event_page(factory, scope=scope, session_id="owner-b", key=key, cursor=snapshot["cursor"])


def test_snapshot_size_limit_returns_explicit_413(databases, scoped_company, monkeypatch):
    factory, _, _ = databases
    principal = OwnerPrincipal(scope=scoped_company.scope, session_id=uuid4(), owner_id="snapshot-test-owner")
    monkeypatch.setattr(events_router, "get_session_factory", lambda: factory)
    monkeypatch.setattr(events_router, "cursor_signing_key", lambda: b"snapshot-fixture-key")
    monkeypatch.setattr("agent_corporation_api.modules.observability.feed.SNAPSHOT_MAX_BYTES", 1)
    with pytest.raises(HTTPException) as error:
        events_router.snapshot(principal)
    assert error.value.status_code == 413
    assert error.value.detail["code"] == "snapshot_too_large"
