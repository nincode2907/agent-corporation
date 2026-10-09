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
    from agent_corporation_api.modules.observability.router import frame
    value = frame("domain", {"stream_seq": 2, "text": "line1\nline2"}, "opaque.cursor")
    assert value.startswith("id: opaque.cursor\nevent: domain\ndata: ")
    assert value.endswith("\n\n")
    assert value.count("\ndata:") == 1


def test_usage_redaction_preserves_only_valid_numeric_measurements():
    from agent_corporation_api.modules.observability.redaction import redact_structure
    result = redact_structure({"input_tokens": 0, "output_tokens": None, "total_tokens": "secret-canary",
                               "api_token": 123, "refresh_token": "secret-canary"})
    assert result == {"input_tokens": 0, "output_tokens": None, "total_tokens": "[REDACTED]",
                      "api_token": "[REDACTED]", "refresh_token": "[REDACTED]"}
