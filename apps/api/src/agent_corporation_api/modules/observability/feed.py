"""Read-only committed event pages and session-bound opaque cursors."""
from __future__ import annotations

import base64
import hashlib
import hmac
import json
import time
from datetime import UTC, datetime
from uuid import UUID

from sqlalchemy import text

from .redaction import redact_structure
from .scope import CompanyScope, set_company_scope

CURSOR_TTL_SECONDS = 86400
SNAPSHOT_MAX_EVENTS = 200
SNAPSHOT_MAX_RUNS = 20
SNAPSHOT_MAX_BYTES = 512 * 1024


class CursorError(ValueError):
    pass


class EventGap(CursorError):
    pass


class SnapshotTooLarge(ValueError):
    pass


def encode_cursor(key: bytes, scope: CompanyScope, session_id: str, sequence: int, anchor: str | None,
                  *, now: int | None = None) -> str:
    body = json.dumps({"v": 1, "env": str(scope.environment_id), "company": str(scope.company_id),
                       "session": str(session_id), "seq": sequence, "anchor": anchor,
                       "expires": (int(time.time()) if now is None else now) + CURSOR_TTL_SECONDS},
                      sort_keys=True, separators=(",", ":")).encode()
    payload = base64.urlsafe_b64encode(body).rstrip(b"=")
    signature = hmac.new(key, payload, hashlib.sha256).hexdigest().encode()
    return (payload + b"." + signature).decode()


def decode_cursor(value: str, key: bytes, scope: CompanyScope, session_id: str,
                  *, now: int | None = None) -> dict:
    try:
        if len(value) > 2048:
            raise ValueError
        payload, signature = value.encode("ascii").split(b".")
        if not hmac.compare_digest(hmac.new(key, payload, hashlib.sha256).hexdigest().encode(), signature):
            raise ValueError
        data = json.loads(base64.urlsafe_b64decode(payload + b"=" * (-len(payload) % 4)))
        if (data["v"] != 1 or data["env"] != str(scope.environment_id)
                or data["company"] != str(scope.company_id) or data["session"] != str(session_id)
                or type(data["seq"]) is not int or data["seq"] < 0
                or type(data["expires"]) is not int
                or data["expires"] <= (int(time.time()) if now is None else now)):
            raise ValueError
        return data
    except (ValueError, TypeError, KeyError, UnicodeError) as error:
        raise CursorError("Cursor không hợp lệ, hết hạn hoặc thuộc phiên/phạm vi khác.") from error


# SSE contains state/correlation metadata, never raw prompts, outputs, messages or host paths.
SAFE_PAYLOAD_KEYS = {
    "from", "to", "status", "outcome", "error_code", "reason_code", "request_span_id",
    "gateway_call_id", "model", "reasoning_effort", "grant_id", "reservation_id",
    "attempt", "retry_count", "ready_at", "usage_status", "measurement", "usage_available",
    "input_tokens", "output_tokens", "cached_tokens", "reasoning_tokens", "total_tokens", "cost_basis",
    "usage_provenance", "source", "correction_reference", "execution_outcome_unchanged",
    "task_revision", "expected_version", "new_version", "criteria_count", "goal_ref", "priority",
    "fixture", "seed", "seed_version", "stop_epoch", "checkpoint_id", "heartbeat_at",
}


def public_event(row: dict) -> dict:
    payload = {} if row["sensitivity"] == "confidential" else {
        k: v for k, v in row["payload"].items()
        if k in SAFE_PAYLOAD_KEYS and (v is None or isinstance(v, (str, int, float, bool)))
    }
    metadata = {key: row[key] for key in (
        "event_id", "schema_version", "event_type", "stream_seq", "occurred_at", "recorded_at",
        "task_id", "run_id", "agent_id", "employee_version_id", "correlation_id", "parent_event_id", "source",
    )}
    return {**json.loads(json.dumps(metadata, default=str)), "payload": redact_structure(payload),
            "sensitivity": row["sensitivity"], "content_withheld": row["sensitivity"] == "confidential",
            "evidence_refs": []}


def read_event_page(session_factory, *, scope: CompanyScope, session_id: str, key: bytes,
                    cursor: str | None = None, limit: int = 100) -> dict:
    if type(limit) is not int or not 1 <= limit <= 200:
        raise ValueError("limit phải nằm trong 1–200")
    decoded = decode_cursor(cursor, key, scope, session_id) if cursor else None
    after = decoded["seq"] if decoded else 0
    with session_factory() as session, session.begin():
        session.execute(text("SET TRANSACTION ISOLATION LEVEL REPEATABLE READ, READ ONLY"))
        set_company_scope(session, scope)
        params = {"env": scope.environment_id, "company": scope.company_id}
        first = session.execute(text("""SELECT event_id,stream_seq FROM events
            WHERE environment_id=:env AND company_id=:company ORDER BY stream_seq LIMIT 1"""), params).mappings().first()
        latest = session.execute(text("""SELECT last_seq FROM event_stream_counters
            WHERE environment_id=:env AND company_id=:company"""), params).scalar_one_or_none() or 0
        anchor = str(first["event_id"]) if first else None
        if decoded and (after > latest or (decoded["anchor"] is not None and decoded["anchor"] != anchor)):
            raise EventGap("Nguồn event đã reset hoặc mất lịch sử; cần tải lại từ đầu.")
        if first and first["stream_seq"] > after + 1:
            raise EventGap("Có khoảng trống event trước cursor; cần đối chiếu lịch sử.")
        rows = session.execute(text("""SELECT * FROM events WHERE environment_id=:env AND company_id=:company
            AND stream_seq>:after ORDER BY stream_seq LIMIT :limit"""), {**params, "after": after, "limit": limit}).mappings().all()
        events = []
        for row in rows:
            if row["stream_seq"] != after + 1:
                raise EventGap("Chuỗi event thiếu sequence; không nội suy tiến độ.")
            after = row["stream_seq"]
            event = public_event(dict(row))
            event["cursor"] = encode_cursor(key, scope, session_id, after, anchor)
            events.append(event)
        if after < latest and not rows:
            raise EventGap("Counter và lịch sử event không khớp.")
        return {"events": events, "cursor": encode_cursor(key, scope, session_id, after, anchor),
                "latest_seq": latest, "server_time": datetime.now(UTC).isoformat()}


def read_snapshot(session_factory, *, scope: CompanyScope, session_id: str, key: bytes) -> dict:
    """Read the current observability projection and its event watermark atomically."""
    from ..execution.service import RUN_SELECT, _project_run

    with session_factory() as session, session.begin():
        session.execute(text("SET TRANSACTION ISOLATION LEVEL REPEATABLE READ, READ ONLY"))
        set_company_scope(session, scope)
        params = {"environment_id": scope.environment_id, "company_id": scope.company_id}
        counter = session.execute(text("""SELECT last_seq FROM event_stream_counters
            WHERE environment_id=:environment_id AND company_id=:company_id"""), params).scalar_one_or_none()
        watermark = counter or 0
        retained = session.execute(text("""SELECT event_id,stream_seq FROM events
            WHERE environment_id=:environment_id AND company_id=:company_id
            ORDER BY stream_seq LIMIT 1"""), params).mappings().first()
        retained_count = session.execute(text("""SELECT count(*) FROM events
            WHERE environment_id=:environment_id AND company_id=:company_id"""), params).scalar_one()
        rows = session.execute(text("""SELECT * FROM events
            WHERE environment_id=:environment_id AND company_id=:company_id
            ORDER BY stream_seq DESC LIMIT :limit"""),
            {**params, "limit": SNAPSHOT_MAX_EVENTS}).mappings().all()
        rows = list(reversed(rows))
        events = [public_event(dict(row)) for row in rows]
        first_retained = retained["stream_seq"] if retained else None
        runs = session.execute(text(RUN_SELECT + " ORDER BY r.created_at DESC LIMIT :limit"),
            {**params, "limit": SNAPSHOT_MAX_RUNS}).mappings().all()
        run_projection = [_project_run(row) for row in runs]
        first_event_id = str(retained["event_id"]) if retained else None
        history_gap = (watermark > 0 and (first_retained is None or first_retained > 1
                                         or retained_count != watermark - first_retained + 1))
        snapshot = {
            "version": 1,
            "events": events,
            "runs": run_projection,
            "watermark_seq": watermark,
            "first_retained_seq": first_retained,
            "history_gap": history_gap,
            "replay_window_start_seq": rows[0]["stream_seq"] if rows else None,
            "cursor": encode_cursor(key, scope, session_id, watermark, first_event_id),
            "server_time": datetime.now(UTC).isoformat(),
        }
        encoded = json.dumps(snapshot, ensure_ascii=False, default=str, separators=(",", ":")).encode()
        if len(encoded) > SNAPSHOT_MAX_BYTES:
            raise SnapshotTooLarge("Snapshot vượt giới hạn 512 KiB; cần hạ số bản ghi được giữ hoặc giới hạn field.")
        return snapshot
