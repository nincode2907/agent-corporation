from datetime import UTC, datetime
from uuid import uuid4

import pytest

from agent_corporation_api.modules.observability.feed import (
    CursorError, EventGap, decode_cursor, encode_cursor, public_event, read_event_page,
)
from agent_corporation_api.modules.observability.scope import CompanyScope


def test_cursor_rejects_tamper_expiry_different_scope_and_session():
    scope = CompanyScope(uuid4(), uuid4())
    key = b"fixture cursor key"
    token = encode_cursor(key, scope, "session-one", 12, str(uuid4()), now=100)
    assert decode_cursor(token, key, scope, "session-one", now=101)["seq"] == 12
    for cursor, candidate_scope, session, now in (
        (token + "x", scope, "session-one", 101),
        (token, CompanyScope(scope.environment_id, uuid4()), "session-one", 101),
        (token, scope, "session-two", 101),
        (token, scope, "session-one", 86500),
        ("12", scope, "session-one", 101),
    ):
        with pytest.raises(CursorError):
            decode_cursor(cursor, key, candidate_scope, session, now=now)


def test_event_envelope_omits_raw_context_and_confidential_payloads():
    row = {"event_id": uuid4(), "schema_version": 1, "event_type": "LLM_CALL_COMPLETED", "stream_seq": 1,
           "occurred_at": datetime.now(UTC), "recorded_at": datetime.now(UTC), "task_id": None,
           "run_id": None, "agent_id": None, "employee_version_id": None, "correlation_id": uuid4(),
           "parent_event_id": None, "source": "app", "sensitivity": "internal",
           "payload": {"status": "completed", "input_tokens": 12, "prompt": "PRIVATE-CANARY",
                       "messages": ["PRIVATE-CANARY"], "authorization": "PRIVATE-CANARY"},
           "evidence_refs": [{"path": "/PRIVATE-CANARY"}]}
    result = public_event(row)
    assert "PRIVATE-CANARY" not in str(result)
    assert result["payload"] == {"status": "completed", "input_tokens": 12}
    assert result["evidence_refs"] == []
    row["sensitivity"] = "confidential"
    assert public_event(row)["payload"] == {}
    assert public_event(row)["content_withheld"] is True


def test_sse_frame_has_opaque_cursor_and_single_json_data():
    from agent_corporation_api.modules.observability.router import frame, reconnect_cursor
    value = frame("domain", {"stream_seq": 2, "text": "line1\nline2"}, "opaque.cursor")
    assert value.startswith("id: opaque.cursor\nevent: domain\ndata: ")
    assert value.endswith("\n\n")
    assert value.count("\ndata:") == 1
    initial_cursor = "cursor-at-first-connect"
    advanced_cursor = "cursor-after-delivered-event"
    assert reconnect_cursor(initial_cursor, advanced_cursor) == advanced_cursor
    assert reconnect_cursor(initial_cursor, None) == initial_cursor


def test_stream_uses_advanced_last_event_id_on_eventsource_reconnect(monkeypatch):
    from starlette.requests import Request
    from agent_corporation_api.modules.governance.auth import OwnerPrincipal
    from agent_corporation_api.modules.observability.router import stream

    initial_cursor = "signed-cursor-from-original-url"
    advanced_cursor = "signed-cursor-from-last-event-id"
    observed = []
    monkeypatch.setattr("agent_corporation_api.modules.observability.router.page",
                        lambda principal, cursor: observed.append(cursor) or
                        {"events": [], "cursor": cursor, "latest_seq": 2, "server_time": "now"})
    request = Request({"type": "http", "method": "GET", "path": "/api/v1/events/stream",
                       "query_string": f"cursor={initial_cursor}".encode(),
                       "headers": [(b"last-event-id", advanced_cursor.encode())]})
    principal = OwnerPrincipal(scope=CompanyScope(uuid4(), uuid4()), session_id=uuid4(), owner_id="owner")

    response = stream(request, initial_cursor, principal)

    assert response.status_code == 200
    assert observed == [advanced_cursor]


def test_usage_redaction_preserves_only_valid_numeric_measurements():
    from agent_corporation_api.modules.observability.redaction import redact_structure
    result = redact_structure({"input_tokens": 0, "output_tokens": None, "total_tokens": "secret-canary",
                               "api_token": 123, "refresh_token": "secret-canary"})
    assert result == {"input_tokens": 0, "output_tokens": None, "total_tokens": "[REDACTED]",
                      "api_token": "[REDACTED]", "refresh_token": "[REDACTED]"}
