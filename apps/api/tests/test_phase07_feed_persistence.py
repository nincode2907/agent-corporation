from uuid import uuid4

import pytest
from sqlalchemy import text

from test_phase03_persistence import databases, scoped_company, payload
from agent_corporation_api.modules.observability.events import append_event
from agent_corporation_api.modules.observability.feed import EventGap, read_event_page
from agent_corporation_api.modules.observability.scope import set_company_scope
from agent_corporation_api.modules.work.commands import create_work_order


def test_committed_pages_reconnect_no_mutations_or_uncommitted_events(databases, scoped_company):
    factory, admin, _ = databases
    scope = scoped_company.scope
    key = b"fixture-only-key"
    first = create_work_order(factory, scope=scope, payload=payload(), dedup_key=f"feed:{uuid4()}")
    with factory() as session, session.begin():
        set_company_scope(session, scope)
        append_event(session, scope=scope, event_type="RUN_STATE_CHANGED", task_id=first.work_order_id,
                     run_id=None, correlation_id=uuid4(), parent_event_id=None, source="app",
                     actor={"kind": "system"}, sensitivity="internal", payload={"to": "queued"},
                     evidence_refs=[], dedup_key=f"feed:{uuid4()}")
    page1 = read_event_page(factory, scope=scope, session_id="s", key=key, limit=1)
    page2 = read_event_page(factory, scope=scope, session_id="s", key=key, cursor=page1["cursor"])
    assert [e["stream_seq"] for e in page1["events"] + page2["events"]] == [1, 2]
    assert read_event_page(factory, scope=scope, session_id="s", key=key, cursor=page2["cursor"])["events"] == []
    # Uncommitted transaction is invisible to another feed reader and rollback preserves counter.
    with factory() as session:
        set_company_scope(session, scope)
        append_event(session, scope=scope, event_type="RUN_STATE_CHANGED", task_id=first.work_order_id,
                     run_id=None, correlation_id=uuid4(), parent_event_id=None, source="app",
                     actor={"kind": "system"}, sensitivity="internal", payload={"to": "running"},
                     evidence_refs=[], dedup_key=f"feed:{uuid4()}")
        assert read_event_page(factory, scope=scope, session_id="s", key=key, cursor=page2["cursor"])["events"] == []
        session.rollback()
    assert read_event_page(factory, scope=scope, session_id="s", key=key)["latest_seq"] == 2
    with admin() as session:
        assert session.execute(text("SELECT count(*) FROM outbox_events WHERE company_id=:id"), {"id": scope.company_id}).scalar_one() == 2
        assert session.execute(text("SELECT status FROM task_execution_state WHERE task_id=:id"), {"id": first.work_order_id}).scalar_one() == "draft"


def test_missing_sequence_reports_gap_and_wrong_scope_is_empty(databases, scoped_company):
    factory, admin, _ = databases
    scope = scoped_company.scope
    first = create_work_order(factory, scope=scope, payload=payload(), dedup_key=f"gap:{uuid4()}")
    previous = read_event_page(factory, scope=scope, session_id="s", key=b"key")
    with admin.begin() as session:
        session.execute(text("UPDATE event_stream_counters SET last_seq=2 WHERE company_id=:id"), {"id": scope.company_id})
    with pytest.raises(EventGap):
        read_event_page(factory, scope=scope, session_id="s", key=b"key", cursor=previous["cursor"])
    from agent_corporation_api.modules.observability.scope import CompanyScope
    other = CompanyScope(scope.environment_id, scoped_company.other_company_id)
    assert read_event_page(factory, scope=other, session_id="s", key=b"key")["events"] == []
