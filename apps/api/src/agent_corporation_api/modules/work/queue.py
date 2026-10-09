"""Owner-scoped Work Order board and durable queue commands (no automatic dispatch)."""
from __future__ import annotations

import hashlib
import json
from datetime import UTC, datetime
from uuid import UUID, uuid4

from sqlalchemy import text
from sqlalchemy.orm import Session, sessionmaker

from .commands import TASK_TRANSITIONS, CompanyScopeNotFound, InvalidTaskTransition, StaleTaskState
from ..observability.events import append_event
from ..observability.scope import CompanyScope, set_company_scope


class IdempotencyConflict(Exception):
    pass


def list_work_orders(factory: sessionmaker[Session], *, scope: CompanyScope,
                     status: str | None = None, assignee_id: UUID | None = None,
                     query: str | None = None, limit: int = 100) -> list[dict]:
    if not 1 <= limit <= 200:
        raise ValueError("limit phải nằm trong 1–200")
    filters = ["w.environment_id=:environment_id", "w.company_id=:company_id"]
    params: dict[str, object] = {"environment_id": scope.environment_id, "company_id": scope.company_id, "limit": limit}
    if status:
        filters.append("s.status=:status"); params["status"] = status
    if assignee_id:
        filters.append("r.assignee_id=:assignee_id"); params["assignee_id"] = assignee_id
    if query:
        filters.append("r.goal ILIKE :query"); params["query"] = f"%{query}%"
    sql = f"""SELECT w.id AS task_id, w.created_at, s.status, s.revision, s.transition_version,
        r.goal, r.expected_outputs, r.acceptance_criteria, r.scope, r.deadline_at,
        r.budget_limits, r.stop_conditions, r.assignee_id, r.reviewer_id, r.autonomy,
        q.priority, q.queue_status, q.ready_at,
        (SELECT count(*) FROM runs run WHERE run.environment_id=w.environment_id
          AND run.company_id=w.company_id AND run.task_id=w.id) AS run_count
        FROM work_orders w
        JOIN task_execution_state s ON s.environment_id=w.environment_id AND s.company_id=w.company_id AND s.task_id=w.id
        JOIN task_revisions r ON r.environment_id=s.environment_id AND r.company_id=s.company_id
          AND r.task_id=s.task_id AND r.revision=s.revision
        LEFT JOIN task_queue_entries q ON q.environment_id=w.environment_id AND q.company_id=w.company_id AND q.task_id=w.id
        WHERE {' AND '.join(filters)}
        ORDER BY CASE WHEN q.queue_status='pending' THEN 0 WHEN s.status='paused' THEN 1 ELSE 2 END,
          q.priority DESC NULLS LAST, q.ready_at ASC NULLS LAST, w.created_at DESC, w.id
        LIMIT :limit"""
    with factory() as session, session.begin():
        set_company_scope(session, scope)
        return [dict(row) for row in session.execute(text(sql), params).mappings()]


def _record_state(session: Session, *, scope: CompanyScope, task_id: UUID, old: str, target: str,
                  version: int, actor_id: str, key: str, reason: str | None) -> None:
    session.execute(text("""UPDATE task_execution_state SET status=:target, transition_version=:version,
        resume_target=CASE WHEN :target='paused' THEN :old ELSE NULL END, updated_at=CURRENT_TIMESTAMP
        WHERE environment_id=:environment_id AND company_id=:company_id AND task_id=:task_id"""),
        {"target": target, "version": version, "old": old, "environment_id": scope.environment_id,
         "company_id": scope.company_id, "task_id": task_id})
    append_event(session, scope=scope, event_type="TASK_STATE_CHANGED", task_id=task_id, run_id=None,
        correlation_id=uuid4(), parent_event_id=None, source="app", actor={"kind":"owner","id":actor_id},
        sensitivity="internal", payload={"from":old,"to":target,"expected_version":version-1,
        "new_version":version,"reason_code":reason or key}, evidence_refs=[],
        dedup_key=f"task:{task_id}:state:{version}")


def task_action(factory: sessionmaker[Session], *, scope: CompanyScope, task_id: UUID, owner_id: str,
                action: str, expected_version: int, idempotency_key: UUID, priority: int = 0,
                reason: str | None = None) -> dict:
    if action not in {"enqueue", "pause", "resume", "cancel", "accept", "request_rework"}:
        raise ValueError("Hành động task không hợp lệ")
    if type(expected_version) is not int or expected_version < 1:
        raise ValueError("expected_version không hợp lệ")
    if action == "enqueue" and not -100 <= priority <= 100:
        raise ValueError("priority phải nằm trong -100..100")
    canonical = json.dumps({"task_id":str(task_id),"action":action,"expected_version":expected_version,
        "priority":priority,"reason":reason}, ensure_ascii=False, sort_keys=True, separators=(",",":"))
    payload_hash = hashlib.sha256(canonical.encode()).hexdigest()
    with factory() as session, session.begin():
        set_company_scope(session, scope)
        state = session.execute(text("""SELECT status,transition_version FROM task_execution_state
            WHERE environment_id=:environment_id AND company_id=:company_id AND task_id=:task_id FOR UPDATE"""),
            {"environment_id":scope.environment_id,"company_id":scope.company_id,"task_id":task_id}).mappings().first()
        if not state:
            raise CompanyScopeNotFound("task không tồn tại trong scope Owner hiện tại")
        # Serialize same-task commands before checking receipts so concurrent
        # retries with one key observe the committed result after the row lock.
        receipt = session.execute(text("""SELECT payload_hash,response FROM task_command_receipts
            WHERE environment_id=:environment_id AND company_id=:company_id AND idempotency_key=:key"""),
            {"environment_id":scope.environment_id,"company_id":scope.company_id,"key":idempotency_key}).mappings().first()
        if receipt:
            if receipt["payload_hash"] != payload_hash:
                raise IdempotencyConflict("Idempotency-Key đã được dùng cho nội dung khác")
            return {**dict(receipt["response"]), "idempotent_replay":True}
        current, version = state["status"], state["transition_version"]
        if version != expected_version:
            raise StaleTaskState("task state đã thay đổi; tải lại trước khi quyết định")
        if action == "enqueue":
            target = "queued"
            if target not in TASK_TRANSITIONS.get(current,set()) or current != "draft":
                raise InvalidTaskTransition("Chỉ Work Order nháp có thể được đưa vào queue lần đầu")
        elif action == "pause":
            target = "paused"
            if current != "queued":
                raise InvalidTaskTransition("Chỉ task đang chờ trong queue mới có thể pause an toàn")
        elif action == "resume":
            target = "queued"
            if current != "paused":
                raise InvalidTaskTransition("Chỉ task đã pause mới có thể tiếp tục")
        elif action == "cancel":
            target = "cancelled"
            if current not in {"draft","queued","paused"}:
                raise InvalidTaskTransition("Task không ở ranh giới an toàn để hủy; cần đối chiếu run trước")
        elif action == "accept":
            target = "accepted"
            if current != "awaiting_acceptance":
                raise InvalidTaskTransition("Task chưa ở trạng thái chờ Chủ tịch nghiệm thu")
            completed = session.execute(text("""SELECT 1 FROM run_execution_state rs JOIN runs r
                ON r.environment_id=rs.environment_id AND r.company_id=rs.company_id AND r.id=rs.run_id
                WHERE r.environment_id=:environment_id AND r.company_id=:company_id AND r.task_id=:task_id
                  AND rs.status='completed' LIMIT 1"""),
                {"environment_id":scope.environment_id,"company_id":scope.company_id,"task_id":task_id}).first()
            if not completed:
                raise InvalidTaskTransition("Cần run hoàn tất làm evidence trước khi nghiệm thu")
        else:
            target = "rework"
            if current != "awaiting_acceptance" or not reason or not reason.strip():
                raise InvalidTaskTransition("Yêu cầu rework cần task chờ nghiệm thu và lý do")
        next_version = version + 1
        _record_state(session, scope=scope, task_id=task_id, old=current, target=target,
                      version=next_version, actor_id=owner_id, key=str(idempotency_key), reason=reason)
        queue = session.execute(text("""SELECT priority,queue_status FROM task_queue_entries
            WHERE environment_id=:environment_id AND company_id=:company_id AND task_id=:task_id FOR UPDATE"""),
            {"environment_id":scope.environment_id,"company_id":scope.company_id,"task_id":task_id}).mappings().first()
        queue_status = queue["queue_status"] if queue else None
        if action in {"pause","resume"} and queue is None:
            raise InvalidTaskTransition("Task chưa có entry queue để pause/resume")
        event_type = None
        if action == "enqueue":
            queue_status = "pending"
            session.execute(text("""INSERT INTO task_queue_entries(environment_id,company_id,task_id,priority,queue_status,ready_at)
                VALUES(:environment_id,:company_id,:task_id,:priority,'pending',CURRENT_TIMESTAMP)"""),
                {"environment_id":scope.environment_id,"company_id":scope.company_id,"task_id":task_id,"priority":priority})
            event_type = "TASK_QUEUED"
        elif action == "pause":
            queue_status = "paused"
            session.execute(text("""UPDATE task_queue_entries SET queue_status='paused',updated_at=CURRENT_TIMESTAMP
                WHERE environment_id=:environment_id AND company_id=:company_id AND task_id=:task_id"""),
                {"environment_id":scope.environment_id,"company_id":scope.company_id,"task_id":task_id})
            event_type = "TASK_PAUSED"
        elif action == "resume":
            queue_status = "pending"
            session.execute(text("""UPDATE task_queue_entries SET queue_status='pending',ready_at=CURRENT_TIMESTAMP,updated_at=CURRENT_TIMESTAMP
                WHERE environment_id=:environment_id AND company_id=:company_id AND task_id=:task_id"""),
                {"environment_id":scope.environment_id,"company_id":scope.company_id,"task_id":task_id})
            event_type = "TASK_RESUMED"
        elif action == "cancel":
            queue_status = "cancelled" if queue else None
            if queue:
                session.execute(text("""UPDATE task_queue_entries SET queue_status='cancelled',updated_at=CURRENT_TIMESTAMP
                    WHERE environment_id=:environment_id AND company_id=:company_id AND task_id=:task_id"""),
                    {"environment_id":scope.environment_id,"company_id":scope.company_id,"task_id":task_id})
            event_type = "TASK_CANCELLED"
        elif action == "accept":
            if queue:
                session.execute(text("""UPDATE task_queue_entries SET queue_status='completed',updated_at=CURRENT_TIMESTAMP
                    WHERE environment_id=:environment_id AND company_id=:company_id AND task_id=:task_id"""),
                    {"environment_id":scope.environment_id,"company_id":scope.company_id,"task_id":task_id})
            event_type = "TASK_ACCEPTED"
        elif action == "request_rework":
            event_type = "TASK_REWORK_REQUESTED"
        assert event_type
        append_event(session, scope=scope, event_type=event_type, task_id=task_id, run_id=None,
            correlation_id=uuid4(), parent_event_id=None, source="app", actor={"kind":"owner","id":owner_id},
            sensitivity="internal", payload={"to":target,"priority":priority if action == "enqueue" else (queue["priority"] if queue else None),
            "reason_code":reason or action,"expected_version":version,"new_version":next_version},
            evidence_refs=[], dedup_key=f"task:{task_id}:command:{idempotency_key}")
        response = {"task_id":str(task_id),"status":target,"transition_version":next_version,
                    "queue_status":queue_status,"priority":priority if action == "enqueue" else (queue["priority"] if queue else None),
                    "idempotent_replay":False}
        session.execute(text("""INSERT INTO task_command_receipts(environment_id,company_id,idempotency_key,task_id,payload_hash,response)
            VALUES(:environment_id,:company_id,:key,:task_id,:payload_hash,CAST(:response AS jsonb))"""),
            {"environment_id":scope.environment_id,"company_id":scope.company_id,"key":idempotency_key,
             "task_id":task_id,"payload_hash":payload_hash,"response":json.dumps(response,ensure_ascii=False)})
        return response


def list_assignees(factory: sessionmaker[Session], *, scope: CompanyScope) -> list[dict]:
    with factory() as session, session.begin():
        set_company_scope(session, scope)
        return [dict(row) for row in session.execute(text("""SELECT e.id,e.lifecycle,d.name AS department,
            latest.profile->>'display_name' AS display_name,latest.profile->>'role' AS role
            FROM employees e LEFT JOIN departments d ON d.environment_id=e.environment_id
              AND d.company_id=e.company_id AND d.id=e.department_id
            LEFT JOIN LATERAL (SELECT profile FROM employee_versions v
              WHERE v.environment_id=e.environment_id AND v.company_id=e.company_id AND v.employee_id=e.id
              ORDER BY version DESC LIMIT 1) latest ON true
            WHERE e.environment_id=:environment_id AND e.company_id=:company_id
              AND e.lifecycle IN ('active','probation') ORDER BY latest.profile->>'display_name',e.id LIMIT 100"""),
            {"environment_id":scope.environment_id,"company_id":scope.company_id}).mappings()]
