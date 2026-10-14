"""Owner-reviewed action proposals. Decisions are records; this module never dispatches them."""
from __future__ import annotations

import hashlib
import json
import re
from datetime import UTC, datetime, timedelta
from uuid import UUID, uuid4

from sqlalchemy import text
from sqlalchemy.orm import Session, sessionmaker

from ..observability.events import append_event
from ..observability.redaction import SECRET_FIELD, SECRET_TEXT, redact_structure, redact_text
from ..observability.scope import CompanyScope, set_company_scope

ACTION_TYPES = frozenset({
    "tool_execution", "permission_change", "budget_change", "profile_change",
    "external_send", "deploy", "destructive_action", "chat_work_order_draft",
})
_SAFE_REF = re.compile(r"^[A-Za-z0-9:/_.-]{1,160}$")


class ApprovalNotFound(Exception):
    pass


class ApprovalConflict(Exception):
    pass


class ApprovalInvalid(Exception):
    pass


def _json_value(value: object, depth: int = 0) -> object:
    if depth > 12:
        raise ApprovalInvalid("Payload phê duyệt quá sâu.")
    if value is None or isinstance(value, (str, bool)):
        if isinstance(value, str) and (SECRET_TEXT.search(value) or "[REDACTED]" in value):
            raise ApprovalInvalid("Payload chứa dữ liệu giống secret; chỉ gửi secret reference đã cấp.")
        return value
    if type(value) is int:
        return value
    if isinstance(value, float):
        raise ApprovalInvalid("Payload chỉ nhận số nguyên; tiền tệ phải dùng integer micros.")
    if isinstance(value, list):
        if len(value) > 500:
            raise ApprovalInvalid("Payload có quá nhiều phần tử.")
        return [_json_value(item, depth + 1) for item in value]
    if isinstance(value, dict):
        if len(value) > 200:
            raise ApprovalInvalid("Payload có quá nhiều trường.")
        clean: dict[str, object] = {}
        for raw_key, item in value.items():
            if not isinstance(raw_key, str) or len(raw_key) > 100:
                raise ApprovalInvalid("Tên trường payload không hợp lệ.")
            key = raw_key.strip()
            if not key or (SECRET_FIELD.search(key) and key.lower() not in {"secret_ref", "credential_ref", "api_key_ref"}):
                raise ApprovalInvalid("Payload không được chứa giá trị secret.")
            if key.lower() in {"secret_ref", "credential_ref", "api_key_ref"}:
                if not isinstance(item, str) or not _SAFE_REF.fullmatch(item):
                    raise ApprovalInvalid("Secret reference không hợp lệ.")
            clean[key] = _json_value(item, depth + 1)
        return clean
    raise ApprovalInvalid("Payload phải là JSON thuần.")


def canonical_json(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)


def digest(value: object) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def _map_approval(row) -> dict[str, object]:
    result = dict(row)
    result["id"] = str(result["id"])
    for key in ("task_id", "run_id", "policy_id"):
        if result.get(key) is not None:
            result[key] = str(result[key])
    for key in ("created_at", "expires_at", "decided_at"):
        if result.get(key) is not None:
            result[key] = result[key].isoformat()
    for key in ("payload_hash", "decision_hash"):
        if result.get(key) is not None:
            result[key] = str(result[key]).strip()
    for key in ("action_payload", "budget_snapshot", "decided_by"):
        if result.get(key) is not None:
            result[key] = redact_structure(result[key])
    return result


def list_approvals(factory: sessionmaker[Session], *, scope: CompanyScope,
                   status: str | None = None, limit: int = 100) -> list[dict[str, object]]:
    if not 1 <= limit <= 200:
        raise ApprovalInvalid("limit phải nằm trong 1–200")
    if status is not None and status not in {"pending", "approved", "rejected", "expired", "stale", "consumed"}:
        raise ApprovalInvalid("Trạng thái phê duyệt không hợp lệ.")
    where = "a.environment_id=:environment_id AND a.company_id=:company_id"
    params: dict[str, object] = {"environment_id": scope.environment_id, "company_id": scope.company_id, "limit": limit}
    if status:
        where += " AND a.status=:status"
        params["status"] = status
    with factory() as session, session.begin():
        set_company_scope(session, scope)
        rows = session.execute(text(f"""SELECT a.id,a.task_id,a.run_id,a.task_revision,a.action_type,
            a.action_payload,a.payload_hash,a.summary,a.status,a.policy_id,a.policy_version,
            a.policy_snapshot_version,a.budget_snapshot,a.expires_at,a.decided_by,a.decided_at,
            a.decision_reason,a.decision_hash,a.created_at,r.goal AS task_goal
            FROM approvals a JOIN task_revisions r ON r.environment_id=a.environment_id
              AND r.company_id=a.company_id AND r.task_id=a.task_id
              AND r.revision=COALESCE(a.task_revision,(SELECT max(rr.revision) FROM task_revisions rr
                WHERE rr.environment_id=a.environment_id AND rr.company_id=a.company_id AND rr.task_id=a.task_id))
            WHERE {where} ORDER BY CASE WHEN a.status='pending' THEN 0 ELSE 1 END,
              a.created_at DESC,a.id LIMIT :limit"""), params).mappings().all()
        return [_map_approval(row) for row in rows]


def create_approval(factory: sessionmaker[Session], *, scope: CompanyScope, owner_id: str,
                    task_id: UUID, run_id: UUID | None, action_type: str, summary: str,
                    action_payload: dict[str, object], expires_at: datetime,
                    idempotency_key: UUID) -> dict[str, object]:
    if action_type not in ACTION_TYPES:
        raise ApprovalInvalid("Loại hành động chưa được hỗ trợ.")
    summary = redact_text(summary.strip())
    if not summary or len(summary) > 500 or SECRET_TEXT.search(summary):
        raise ApprovalInvalid("Mô tả phê duyệt không hợp lệ hoặc có dữ liệu nhạy cảm.")
    if expires_at.tzinfo is None:
        raise ApprovalInvalid("Thời hạn cần có múi giờ.")
    expires_at = expires_at.astimezone(UTC)
    now = datetime.now(UTC)
    if not now + timedelta(minutes=1) <= expires_at <= now + timedelta(days=7):
        raise ApprovalInvalid("Thời hạn phải nằm trong khoảng 1 phút đến 7 ngày.")
    payload = _json_value(action_payload)
    if not isinstance(payload, dict):
        raise ApprovalInvalid("Action payload phải là object.")
    if len(canonical_json(payload).encode("utf-8")) > 65536:
        raise ApprovalInvalid("Payload vượt quá 64 KiB.")

    request_hash = digest({"schema": "approval-request-v1", "environment_id": str(scope.environment_id),
        "company_id": str(scope.company_id), "task_id": str(task_id),
        "run_id": str(run_id) if run_id else None, "action_type": action_type,
        "summary": summary, "action_payload": payload, "expires_at": expires_at.isoformat(timespec="microseconds")})

    approval_id = uuid4()
    with factory() as session, session.begin():
        set_company_scope(session, scope)
        lock_key = f"approval-create:{scope.environment_id}:{scope.company_id}:{idempotency_key}"
        session.execute(text("SELECT pg_advisory_xact_lock(hashtextextended(:key,0))"), {"key": lock_key})
        receipt = session.execute(text("""SELECT request_hash,approval_id FROM approval_request_receipts
            WHERE environment_id=:env AND company_id=:company AND idempotency_key=:key"""),
            {"env": scope.environment_id, "company": scope.company_id, "key": idempotency_key}).mappings().first()
        if receipt:
            if receipt["request_hash"] != request_hash:
                raise ApprovalConflict("Idempotency-Key đã được dùng cho yêu cầu khác.")
            existing = session.execute(text("""SELECT a.id,a.task_id,a.run_id,a.task_revision,a.action_type,
                a.action_payload,a.payload_hash,a.summary,a.status,a.policy_id,a.policy_version,
                a.budget_snapshot,a.expires_at,a.created_at FROM approvals a
                WHERE a.environment_id=:env AND a.company_id=:company AND a.id=:id"""),
                {"env": scope.environment_id, "company": scope.company_id, "id": receipt["approval_id"]}).mappings().one()
            return {**_map_approval(existing), "dispatch_status": "not_dispatched", "idempotent_replay": True}
        task = session.execute(text("""SELECT s.status,s.revision,r.policy_id,r.policy_version,
            r.budget_limits FROM task_execution_state s JOIN task_revisions r
              ON r.environment_id=s.environment_id AND r.company_id=s.company_id
              AND r.task_id=s.task_id AND r.revision=s.revision
            WHERE s.environment_id=:env AND s.company_id=:company AND s.task_id=:task FOR UPDATE"""),
            {"env": scope.environment_id, "company": scope.company_id, "task": task_id}).mappings().first()
        if not task:
            raise ApprovalNotFound("Work Order không tồn tại trong scope Owner hiện tại.")
        if task["status"] != "awaiting_approval":
            raise ApprovalConflict("Work Order chưa ở trạng thái chờ phê duyệt.")
        if run_id is not None and not session.execute(text("""SELECT 1 FROM runs r
            JOIN run_execution_state rs ON rs.environment_id=r.environment_id AND rs.company_id=r.company_id
              AND rs.run_id=r.id AND rs.status='waiting_approval'
            WHERE r.environment_id=:env AND r.company_id=:company AND r.task_id=:task AND r.id=:run"""),
            {"env": scope.environment_id, "company": scope.company_id, "task": task_id, "run": run_id}).first():
            raise ApprovalConflict("Run không còn ở đúng Work Order hoặc không đang chờ phê duyệt.")
        current_policy = session.execute(text("""SELECT id,version FROM policies
            WHERE environment_id=:env AND company_id=:company ORDER BY version DESC,id LIMIT 1"""),
            {"env": scope.environment_id, "company": scope.company_id}).mappings().first()
        policy_id = current_policy["id"] if current_policy else None
        policy_version = current_policy["version"] if current_policy else None
        budget_snapshot = redact_structure(task["budget_limits"] or {"cost_basis": "unknown"})
        payload_hash = digest({
            "schema": "approval-payload-v1", "environment_id": str(scope.environment_id),
            "company_id": str(scope.company_id), "task_id": str(task_id), "task_revision": task["revision"],
            "run_id": str(run_id) if run_id else None, "action_type": action_type,
            "action_payload": payload, "policy_id": str(policy_id) if policy_id else None,
            "policy_version": policy_version, "budget_snapshot": budget_snapshot,
            "expires_at": expires_at.isoformat(timespec="microseconds"),
        })
        session.execute(text("""INSERT INTO approvals(id,environment_id,company_id,task_id,run_id,
            task_revision,policy_id,policy_version,policy_snapshot_version,action_type,action_payload,
            payload_hash,summary,status,budget_snapshot,expires_at)
            VALUES(:id,:env,:company,:task,:run,:revision,:policy_id,:policy_version,:policy_version,
              :action_type,CAST(:payload AS jsonb),:hash,:summary,'pending',CAST(:budget AS jsonb),:expires)"""),
            {"id": approval_id, "env": scope.environment_id, "company": scope.company_id,
             "task": task_id, "run": run_id, "revision": task["revision"], "policy_id": policy_id,
             "policy_version": policy_version, "action_type": action_type,
             "payload": canonical_json(payload), "hash": payload_hash, "summary": summary,
             "budget": canonical_json(budget_snapshot), "expires": expires_at})
        session.execute(text("""INSERT INTO approval_request_receipts(environment_id,company_id,
            idempotency_key,approval_id,request_hash)
            VALUES(:env,:company,:key,:id,:request_hash)"""),
            {"env": scope.environment_id, "company": scope.company_id, "key": idempotency_key,
             "id": approval_id, "request_hash": request_hash})
        append_event(session, scope=scope, event_type="APPROVAL_REQUESTED", task_id=task_id, run_id=run_id,
            correlation_id=approval_id, parent_event_id=None, source="app", actor={"kind": "owner", "id": owner_id},
            sensitivity="internal", payload={"approval_id": str(approval_id), "action_type": action_type,
                "payload_hash": payload_hash, "status": "pending", "policy_version": policy_version},
            evidence_refs=[], dedup_key=f"approval:{approval_id}:requested")
        return {"id": str(approval_id), "task_id": str(task_id), "run_id": str(run_id) if run_id else None,
            "task_revision": task["revision"], "action_type": action_type, "action_payload": redact_structure(payload),
            "payload_hash": payload_hash, "summary": summary, "status": "pending",
            "policy_id": str(policy_id) if policy_id else None, "policy_version": policy_version,
            "budget_snapshot": budget_snapshot, "expires_at": expires_at.isoformat(),
            "created_at": now.isoformat(), "dispatch_status": "not_dispatched", "idempotent_replay": False}


def decide_approval(factory: sessionmaker[Session], *, scope: CompanyScope, owner_id: str,
                    approval_id: UUID, decision: str, expected_payload_hash: str,
                    idempotency_key: UUID, reason: str | None = None) -> dict[str, object]:
    if decision not in {"approve", "reject"}:
        raise ApprovalInvalid("Quyết định chỉ nhận approve hoặc reject.")
    if not re.fullmatch(r"[0-9a-f]{64}", expected_payload_hash):
        raise ApprovalInvalid("Payload hash không hợp lệ.")
    reason_value = redact_text((reason or "").strip())
    if len(reason_value) > 500 or SECRET_TEXT.search(reason_value):
        raise ApprovalInvalid("Lý do quyết định không hợp lệ hoặc có dữ liệu nhạy cảm.")
    request_hash = digest({"schema": "approval-decision-v1", "approval_id": str(approval_id),
        "decision": decision, "expected_payload_hash": expected_payload_hash, "reason": reason_value})
    with factory() as session, session.begin():
        set_company_scope(session, scope)
        lock_key = f"approval-decision:{scope.environment_id}:{scope.company_id}:{idempotency_key}"
        session.execute(text("SELECT pg_advisory_xact_lock(hashtextextended(:key,0))"), {"key": lock_key})
        receipt = session.execute(text("""SELECT request_hash,response FROM approval_decision_receipts
            WHERE environment_id=:env AND company_id=:company AND idempotency_key=:key"""),
            {"env": scope.environment_id, "company": scope.company_id, "key": idempotency_key}).mappings().first()
        if receipt:
            if receipt["request_hash"] != request_hash:
                raise ApprovalConflict("Idempotency-Key đã được dùng cho quyết định khác.")
            return {**dict(receipt["response"]), "idempotent_replay": True}
        row = session.execute(text("""SELECT a.*,s.revision AS current_revision,s.status AS current_task_status,
              rs.status AS current_run_status
            FROM approvals a JOIN task_execution_state s ON s.environment_id=a.environment_id
              AND s.company_id=a.company_id AND s.task_id=a.task_id
            LEFT JOIN run_execution_state rs ON rs.environment_id=a.environment_id AND rs.company_id=a.company_id
              AND rs.run_id=a.run_id
            WHERE a.environment_id=:env AND a.company_id=:company AND a.id=:id FOR UPDATE OF a,s"""),
            {"env": scope.environment_id, "company": scope.company_id, "id": approval_id}).mappings().first()
        if not row:
            raise ApprovalNotFound("Yêu cầu phê duyệt không tồn tại trong scope hiện tại.")
        if row["payload_hash"] != expected_payload_hash:
            raise ApprovalConflict("Payload đã đổi; quyết định cũ không còn khớp.")
        if row["status"] != "pending":
            raise ApprovalConflict("Yêu cầu đã được quyết định hoặc không còn hiệu lực.")
        now = datetime.now(UTC)
        status = "approved" if decision == "approve" else "rejected"
        reason_code = decision
        current_policy = session.execute(text("""SELECT id,version FROM policies
            WHERE environment_id=:env AND company_id=:company ORDER BY version DESC,id LIMIT 1"""),
            {"env": scope.environment_id, "company": scope.company_id}).mappings().first()
        active_policy_id = current_policy["id"] if current_policy else None
        active_policy_version = current_policy["version"] if current_policy else None
        if row["expires_at"] is None or row["expires_at"] <= now:
            status, reason_code = "expired", "expired_before_decision"
        elif (row["task_revision"] != row["current_revision"] or row["current_task_status"] != "awaiting_approval"
              or (row["run_id"] is not None and row["current_run_status"] != "waiting_approval")
              or row["policy_id"] != active_policy_id or row["policy_version"] != active_policy_version):
            status, reason_code = "stale", "task_or_policy_changed"
        decision_hash = digest({"approval_payload_hash": expected_payload_hash, "decision": decision,
            "status": status, "reason": reason_value})
        decided_by = {"kind": "owner", "id": owner_id}
        session.execute(text("""UPDATE approvals SET status=:status,decided_by=CAST(:actor AS jsonb),
            decided_at=:now,decision_reason=:reason,decision_key=:key,decision_hash=:hash
            WHERE environment_id=:env AND company_id=:company AND id=:id"""),
            {"status": status, "actor": canonical_json(decided_by), "now": now,
             "reason": reason_value or None, "key": idempotency_key, "hash": decision_hash,
             "env": scope.environment_id, "company": scope.company_id, "id": approval_id})
        append_event(session, scope=scope, event_type="APPROVAL_DECIDED", task_id=row["task_id"],
            run_id=row["run_id"], correlation_id=approval_id, parent_event_id=None, source="app",
            actor=decided_by, sensitivity="internal", payload={"approval_id": str(approval_id),
                "decision": decision, "status": status, "payload_hash": expected_payload_hash,
                "decision_hash": decision_hash, "reason_code": reason_code}, evidence_refs=[],
            dedup_key=f"approval:{approval_id}:decision:{idempotency_key}")
        response = {"id": str(approval_id), "status": status, "decision": decision,
            "payload_hash": expected_payload_hash, "decision_hash": decision_hash,
            "decided_at": now.isoformat(), "dispatch_status": "not_dispatched", "reason_code": reason_code,
            "idempotent_replay": False}
        session.execute(text("""INSERT INTO approval_decision_receipts(environment_id,company_id,
            idempotency_key,approval_id,request_hash,response)
            VALUES(:env,:company,:key,:id,:request_hash,CAST(:response AS jsonb))"""),
            {"env": scope.environment_id, "company": scope.company_id, "key": idempotency_key,
             "id": approval_id, "request_hash": request_hash, "response": canonical_json(response)})
        return response


def consume_approval(factory: sessionmaker[Session], *, scope: CompanyScope,
                     approval_id: UUID, expected_payload_hash: str,
                     now: datetime | None = None) -> dict[str, object]:
    """Atomically consume one approved payload before a future executor dispatch.

    The caller must still handle an unknown external outcome without retrying the
    side effect. This function alone never dispatches an action.
    """
    if not re.fullmatch(r"[0-9a-f]{64}", expected_payload_hash):
        raise ApprovalInvalid("Payload hash không hợp lệ.")
    now = now or datetime.now(UTC)
    with factory() as session, session.begin():
        set_company_scope(session, scope)
        row = session.execute(text("""SELECT a.*,s.revision AS current_revision,
              s.status AS current_task_status,rs.status AS current_run_status
            FROM approvals a JOIN task_execution_state s ON s.environment_id=a.environment_id
              AND s.company_id=a.company_id AND s.task_id=a.task_id
            LEFT JOIN run_execution_state rs ON rs.environment_id=a.environment_id AND rs.company_id=a.company_id
              AND rs.run_id=a.run_id
            WHERE a.environment_id=:env AND a.company_id=:company AND a.id=:id FOR UPDATE OF a,s"""),
            {"env": scope.environment_id, "company": scope.company_id, "id": approval_id}).mappings().first()
        if not row:
            raise ApprovalNotFound("Yêu cầu phê duyệt không tồn tại trong scope hiện tại.")
        if row["status"] != "approved" or row["payload_hash"] != expected_payload_hash:
            raise ApprovalConflict("Approval chưa được duyệt, đã dùng hoặc payload không còn khớp.")
        current_policy = session.execute(text("""SELECT id,version FROM policies
            WHERE environment_id=:env AND company_id=:company ORDER BY version DESC,id LIMIT 1"""),
            {"env": scope.environment_id, "company": scope.company_id}).mappings().first()
        active_policy_id = current_policy["id"] if current_policy else None
        active_policy_version = current_policy["version"] if current_policy else None
        if row["expires_at"] is None or row["expires_at"] <= now:
            status, reason = "expired", "expired_before_consumption"
        elif (row["task_revision"] != row["current_revision"] or row["current_task_status"] != "awaiting_approval"
              or (row["run_id"] is not None and row["current_run_status"] != "waiting_approval")
              or row["policy_id"] != active_policy_id or row["policy_version"] != active_policy_version):
            status, reason = "stale", "scope_or_policy_changed_before_consumption"
        else:
            status, reason = "consumed", "single_use_approval_consumed"
        if status == "consumed":
            session.execute(text("""UPDATE approvals SET status='consumed',consumed_at=:now
                WHERE environment_id=:env AND company_id=:company AND id=:id AND status='approved'"""),
                {"now": now, "env": scope.environment_id, "company": scope.company_id, "id": approval_id})
        else:
            session.execute(text("""UPDATE approvals SET status=:status
                WHERE environment_id=:env AND company_id=:company AND id=:id AND status='approved'"""),
                {"status": status, "env": scope.environment_id, "company": scope.company_id, "id": approval_id})
        append_event(session, scope=scope, event_type="APPROVAL_CONSUMED" if status == "consumed" else "APPROVAL_INVALIDATED",
            task_id=row["task_id"], run_id=row["run_id"], correlation_id=approval_id, parent_event_id=None,
            source="app", actor={"kind": "system", "id": "permission-engine"}, sensitivity="internal",
            payload={"approval_id": str(approval_id), "status": status,
                "payload_hash": expected_payload_hash, "reason_code": reason}, evidence_refs=[],
            dedup_key=f"approval:{approval_id}:consume")
        return {"id": str(approval_id), "status": status, "payload_hash": expected_payload_hash,
            "consumed_at": now.isoformat() if status == "consumed" else None,
            "dispatch_status": "not_dispatched", "reason_code": reason}
