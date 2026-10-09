from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from typing import Any
from uuid import UUID, uuid4

from sqlalchemy import text
from sqlalchemy.orm import Session, sessionmaker

from ..observability.events import append_event, lock_event_stream
from ..observability.redaction import redact_structure, redact_text
from ..observability.scope import CompanyScope, set_company_scope


class CompanyScopeNotFound(Exception):
    pass


class InvalidTaskTransition(Exception):
    pass


class StaleTaskState(Exception):
    pass


@dataclass(frozen=True)
class WorkOrderCreated:
    work_order_id: UUID
    revision: int
    event_id: UUID
    stream_seq: int
    duplicate: bool = False


TASK_TRANSITIONS: dict[str, set[str]] = {
    "draft": {"queued", "cancelled"},
    "queued": {"planning", "paused", "cancelled"},
    "planning": {"awaiting_approval", "executing", "blocked", "paused", "cancelled"},
    "awaiting_approval": {"executing", "blocked", "paused", "cancelled"},
    "executing": {"reviewing", "blocked", "failed", "paused", "cancelled"},
    "reviewing": {"awaiting_acceptance", "rework", "blocked", "paused", "cancelled"},
    "rework": {"planning", "executing", "blocked", "paused", "cancelled"},
    "awaiting_acceptance": {"accepted", "rework", "paused", "cancelled"},
    "blocked": {"queued", "paused", "cancelled"},
    "paused": {"queued", "cancelled"},
    "accepted": set(),
    "failed": set(),
    "cancelled": set(),
}


def _validate_payload(payload: dict[str, Any]) -> dict[str, Any]:
    goal = payload.get("goal")
    outputs = payload.get("expected_outputs")
    criteria = payload.get("acceptance_criteria")
    autonomy = payload.get("autonomy", "strict")
    if not isinstance(goal, str) or not goal.strip():
        raise ValueError("goal phải có nội dung")
    if not isinstance(outputs, list) or not outputs:
        raise ValueError("expected_outputs phải có ít nhất một đầu ra")
    if not isinstance(criteria, list) or not criteria:
        raise ValueError("acceptance_criteria phải có ít nhất một tiêu chí")
    if autonomy not in {"strict", "supervised", "delegated"}:
        raise ValueError("autonomy không hợp lệ")
    return {
        "goal": redact_text(goal.strip()),
        "expected_outputs": redact_structure(outputs),
        "acceptance_criteria": redact_structure(criteria),
        "scope": redact_structure(payload.get("scope", {})),
        "deadline_at": payload.get("deadline_at"),
        "execution_grant_id": payload.get("execution_grant_id"),
        "budget_limits": redact_structure(payload.get("budget_limits", {"max_model_requests": 0, "cost_basis": "unknown"})),
        "stop_conditions": redact_structure(payload.get("stop_conditions", {})),
        "assignee_id": payload.get("assignee_id"),
        "reviewer_id": payload.get("reviewer_id"),
        "autonomy": autonomy,
        "created_by": redact_structure(payload.get("created_by", {"kind": "owner", "id": "owner-local"})),
    }


def create_work_order(
    session_factory: sessionmaker[Session],
    *,
    scope: CompanyScope,
    payload: dict[str, Any],
    dedup_key: str,
    correlation_id: UUID | None = None,
) -> WorkOrderCreated:
    if not dedup_key.strip():
        raise ValueError("dedup_key không được để trống")
    spec = _validate_payload(payload)
    correlation = correlation_id or uuid4()

    with session_factory() as session, session.begin():
        set_company_scope(session, scope)
        company_exists = session.execute(
            text("SELECT 1 FROM companies WHERE environment_id=:environment_id AND id=:company_id"),
            {"environment_id": scope.environment_id, "company_id": scope.company_id},
        ).scalar_one_or_none()
        if company_exists is None:
            raise CompanyScopeNotFound("company không tồn tại trong environment được chọn")

        lock_event_stream(session, scope)
        duplicate = session.execute(
            text("""SELECT task_id, event_id, stream_seq, payload FROM events
                     WHERE environment_id=:environment_id AND company_id=:company_id AND dedup_key=:dedup_key"""),
            {"environment_id": scope.environment_id, "company_id": scope.company_id, "dedup_key": dedup_key},
        ).mappings().first()
        if duplicate:
            request_hash = hashlib.sha256(json.dumps(spec,ensure_ascii=False,sort_keys=True,default=str,separators=(",",":")).encode()).hexdigest()
            if duplicate["payload"].get("request_hash") != request_hash:
                raise ValueError("Idempotency-Key đã được dùng cho Work Order có nội dung khác")
            return WorkOrderCreated(
                work_order_id=duplicate["task_id"],
                revision=1,
                event_id=duplicate["event_id"],
                stream_seq=duplicate["stream_seq"],
                duplicate=True,
            )

        for member_id, label in ((spec["assignee_id"], "assignee"), (spec["reviewer_id"], "reviewer")):
            if member_id is not None:
                member = session.execute(text("""SELECT lifecycle FROM employees
                    WHERE environment_id=:environment_id AND company_id=:company_id AND id=:id FOR SHARE"""),
                    {"environment_id":scope.environment_id,"company_id":scope.company_id,"id":member_id}).scalar_one_or_none()
                if member not in {"active","probation"}:
                    raise ValueError(f"{label} phải là nhân sự đang active/probation trong scope hiện tại")

        task_id = uuid4()
        session.execute(
            text("""INSERT INTO work_orders(id, environment_id, company_id, created_by)
                     VALUES (:id, :environment_id, :company_id, CAST(:created_by AS jsonb))"""),
            {
                "id": task_id,
                "environment_id": scope.environment_id,
                "company_id": scope.company_id,
                "created_by": json.dumps(spec["created_by"]),
            },
        )
        session.execute(
            text("""INSERT INTO task_revisions(
                        task_id, environment_id, company_id, revision, goal, expected_outputs,
                        acceptance_criteria, scope, deadline_at, execution_grant_id, budget_limits,
                        stop_conditions, assignee_id, reviewer_id, autonomy, created_by
                    ) VALUES (
                        :task_id, :environment_id, :company_id, 1, :goal, CAST(:expected_outputs AS jsonb),
                        CAST(:acceptance_criteria AS jsonb), CAST(:scope AS jsonb), :deadline_at,
                        :execution_grant_id, CAST(:budget_limits AS jsonb), CAST(:stop_conditions AS jsonb),
                        :assignee_id, :reviewer_id, :autonomy, CAST(:created_by AS jsonb)
                    )"""),
            {
                "task_id": task_id,
                "environment_id": scope.environment_id,
                "company_id": scope.company_id,
                "goal": spec["goal"],
                "expected_outputs": json.dumps(spec["expected_outputs"]),
                "acceptance_criteria": json.dumps(spec["acceptance_criteria"]),
                "scope": json.dumps(spec["scope"]),
                "deadline_at": spec["deadline_at"],
                "execution_grant_id": spec["execution_grant_id"],
                "budget_limits": json.dumps(spec["budget_limits"]),
                "stop_conditions": json.dumps(spec["stop_conditions"]),
                "assignee_id": spec["assignee_id"],
                "reviewer_id": spec["reviewer_id"],
                "autonomy": spec["autonomy"],
                "created_by": json.dumps(spec["created_by"]),
            },
        )
        session.execute(
            text("""INSERT INTO task_execution_state(task_id, environment_id, company_id, revision, status)
                     VALUES (:task_id, :environment_id, :company_id, 1, 'draft')"""),
            {"task_id": task_id, "environment_id": scope.environment_id, "company_id": scope.company_id},
        )
        goal_ref = hashlib.sha256(spec["goal"].encode("utf-8")).hexdigest()
        request_hash = hashlib.sha256(json.dumps(spec,ensure_ascii=False,sort_keys=True,default=str,separators=(",",":")).encode()).hexdigest()
        event = append_event(
            session,
            scope=scope,
            event_type="TASK_CREATED",
            task_id=task_id,
            run_id=None,
            correlation_id=correlation,
            parent_event_id=None,
            source="app",
            actor=spec["created_by"],
            sensitivity="internal",
            payload={"task_revision": 1, "goal_ref": goal_ref, "criteria_count": len(spec["acceptance_criteria"]), "request_hash":request_hash},
            evidence_refs=[],
            dedup_key=dedup_key,
        )
        return WorkOrderCreated(task_id, 1, event.event_id, event.stream_seq)


def transition_task(
    session_factory: sessionmaker[Session],
    *,
    scope: CompanyScope,
    task_id: UUID,
    target_status: str,
    expected_version: int,
    actor: dict[str, object],
    dedup_key: str,
) -> int:
    actor = redact_structure(actor)
    if actor.get("kind") not in {"owner", "system"}:
        raise InvalidTaskTransition("actor không được phép đổi trạng thái task")
    with session_factory() as session, session.begin():
        set_company_scope(session, scope)
        state = session.execute(
            text("""SELECT status, transition_version FROM task_execution_state
                     WHERE environment_id=:environment_id AND company_id=:company_id AND task_id=:task_id
                     FOR UPDATE"""),
            {"environment_id": scope.environment_id, "company_id": scope.company_id, "task_id": task_id},
        ).mappings().first()
        if not state:
            raise CompanyScopeNotFound("task không tồn tại trong scope hiện tại")
        current = state["status"]
        if target_status not in TASK_TRANSITIONS.get(current, set()):
            raise InvalidTaskTransition(f"không cho chuyển task từ {current} sang {target_status}")
        if state["transition_version"] != expected_version:
            raise StaleTaskState("task state đã thay đổi; tải lại trước khi quyết định")
        next_version = expected_version + 1
        session.execute(
            text("""UPDATE task_execution_state SET status=:target_status,
                         resume_target=CASE WHEN :target_status='paused' THEN :current ELSE NULL END,
                         transition_version=:next_version, updated_at=CURRENT_TIMESTAMP
                     WHERE environment_id=:environment_id AND company_id=:company_id AND task_id=:task_id"""),
            {
                "target_status": target_status,
                "current": current,
                "next_version": next_version,
                "environment_id": scope.environment_id,
                "company_id": scope.company_id,
                "task_id": task_id,
            },
        )
        append_event(
            session,
            scope=scope,
            event_type="TASK_STATE_CHANGED",
            task_id=task_id,
            run_id=None,
            correlation_id=uuid4(),
            parent_event_id=None,
            source="app",
            actor=actor,
            sensitivity="internal",
            payload={"from": current, "to": target_status, "expected_version": expected_version, "new_version": next_version},
            evidence_refs=[],
            dedup_key=dedup_key,
        )
    return next_version
