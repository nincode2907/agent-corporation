"""Isolated persistence/SSE/authorization evidence for Stabilization Sprint 02."""
from __future__ import annotations

import asyncio
import json
import time
from types import SimpleNamespace
from uuid import uuid4

import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient
from sqlalchemy import text

from test_phase03_persistence import databases, scoped_company
from agent_corporation_api.modules.governance.auth import OwnerPrincipal
from agent_corporation_api.modules.observability import router as events_router
from agent_corporation_api.modules.observability.events import append_event
from agent_corporation_api.modules.observability.feed import encode_cursor
from agent_corporation_api.modules.observability.scope import CompanyScope, set_company_scope
from agent_corporation_api.main import app
from agent_corporation_api.modules.governance.auth import require_owner


def _append(factory, scope: CompanyScope, event_id):
    with factory() as session, session.begin():
        set_company_scope(session, scope)
        return append_event(
            session,
            scope=scope,
            event_type="RUN_STATE_CHANGED",
            task_id=None,
            run_id=None,
            correlation_id=uuid4(),
            parent_event_id=None,
            source="app",
            actor={"kind": "system"},
            sensitivity="internal",
            payload={"to": "completed"},
            evidence_refs=[],
            dedup_key=f"stabilization02:{event_id}",
            event_id=event_id,
        )


def _domain_frames(frames):
    result = []
    for frame in frames:
        if "event: domain\n" in frame:
            data = next(line[6:] for line in frame.splitlines() if line.startswith("data: "))
            result.append(json.loads(data))
    return result


def _stream_frames(response):
    async def collect():
        return [frame async for frame in response.body_iterator]

    return asyncio.run(collect())


def test_committed_event_id_and_sequence_match_sse_and_rollback_is_never_emitted(
    databases, scoped_company, monkeypatch
):
    factory, migration_factory, _ = databases
    scope = scoped_company.scope
    principal = OwnerPrincipal(scope=scope, session_id=uuid4(), owner_id="isolated-test-owner")
    signing_key = b"stabilization02-isolated-cursor-key"
    monkeypatch.setattr(events_router, "get_session_factory", lambda: factory)
    monkeypatch.setattr(events_router, "cursor_signing_key", lambda: signing_key)
    monkeypatch.setattr(events_router, "require_owner", lambda request: principal)
    monkeypatch.setattr(events_router, "POLL_SECONDS", 0)
    monkeypatch.setattr(events_router, "HEARTBEAT_SECONDS", 0)

    committed_id = uuid4()
    record = _append(factory, scope, committed_id)
    with migration_factory() as session:
        persisted = session.execute(
            text("SELECT event_id, stream_seq FROM events WHERE event_id=:id"), {"id": committed_id}
        ).mappings().one()
    assert str(persisted["event_id"]) == str(committed_id)
    assert persisted["stream_seq"] == record.stream_seq == 1

    checks = 0

    async def disconnected():
        nonlocal checks
        checks += 1
        return checks > 1

    async def no_wait(_seconds):
        return None

    monkeypatch.setattr(events_router.asyncio, "sleep", no_wait)
    request = SimpleNamespace(headers={}, is_disconnected=disconnected)
    response = events_router.stream(request, principal=principal)
    streamed = _domain_frames(_stream_frames(response))
    assert [(event["event_id"], event["stream_seq"]) for event in streamed] == [(str(committed_id), 1)]

    rolled_back_id = uuid4()
    with factory() as session:
        set_company_scope(session, scope)
        append_event(
            session,
            scope=scope,
            event_type="RUN_STATE_CHANGED",
            task_id=None,
            run_id=None,
            correlation_id=uuid4(),
            parent_event_id=None,
            source="app",
            actor={"kind": "system"},
            sensitivity="internal",
            payload={"to": "must-rollback"},
            evidence_refs=[],
            dedup_key=f"stabilization02-rollback:{rolled_back_id}",
            event_id=rolled_back_id,
        )
        session.rollback()
    with migration_factory() as session:
        assert session.execute(
            text("SELECT count(*) FROM events WHERE event_id=:id"), {"id": rolled_back_id}
        ).scalar_one() == 0

    page = events_router.page(principal, None)
    assert [event["event_id"] for event in page["events"]] == [str(committed_id)]
    checks = 0
    response = events_router.stream(request, principal=principal)
    after_rollback = _domain_frames(_stream_frames(response))
    assert str(rolled_back_id) not in {event["event_id"] for event in after_rollback}


def test_cursor_boundaries_and_scope_filtered_http_feed(databases, scoped_company, monkeypatch):
    from agent_corporation_api.modules.observability.feed import read_event_page

    factory, migration_factory, _ = databases
    scope = scoped_company.scope
    other_scope = CompanyScope(scope.environment_id, scoped_company.other_company_id)
    principal = OwnerPrincipal(scope=scope, session_id=uuid4(), owner_id="isolated-test-owner")
    key = b"stabilization02-isolated-cursor-key"
    monkeypatch.setattr(events_router, "get_session_factory", lambda: factory)
    monkeypatch.setattr(events_router, "cursor_signing_key", lambda: key)
    monkeypatch.setitem(app.dependency_overrides, require_owner, lambda: principal)

    first_id = uuid4()
    _append(factory, scope, first_id)
    hidden_id = uuid4()
    _append(factory, other_scope, hidden_id)
    response = TestClient(app).get("/api/v1/events")
    assert response.status_code == 200
    visible = response.json()
    assert [event["event_id"] for event in visible["events"]] == [str(first_id)]
    assert str(hidden_id) not in json.dumps(visible)

    valid = visible["cursor"]
    assert events_router.page(principal, valid)["events"] == []
    for bad in (
        valid + "x",
        encode_cursor(key, scope, str(principal.session_id), 1, str(first_id), now=int(time.time()) - 86401),
        encode_cursor(key, other_scope, str(principal.session_id), 0, None),
    ):
        with pytest.raises(HTTPException) as error:
            events_router.page(principal, bad)
        assert error.value.status_code == 400

    second_id = uuid4()
    with migration_factory.begin() as session:
        session.execute(text("DELETE FROM outbox_events WHERE event_id=:id"), {"id": first_id})
        session.execute(text("DELETE FROM events WHERE event_id=:id"), {"id": first_id})
    _append(factory, scope, second_id)
    with pytest.raises(HTTPException) as cursor_gap:
        events_router.page(principal, valid)
    assert cursor_gap.value.status_code == 409
    with pytest.raises(HTTPException) as snapshot_gap:
        events_router.page(principal, None)
    assert snapshot_gap.value.status_code == 409

    # The isolated app role cannot read another company's rows even when given its ID.
    with factory() as session, session.begin():
        set_company_scope(session, scope)
        assert session.execute(text("SELECT count(*) FROM events WHERE event_id=:id"), {"id": hidden_id}).scalar_one() == 0
    other_page = read_event_page(factory, scope=other_scope, session_id="other", key=key)
    assert [event["event_id"] for event in other_page["events"]] == [str(hidden_id)]
