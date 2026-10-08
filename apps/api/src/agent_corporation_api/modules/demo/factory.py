from __future__ import annotations

import hashlib
import json
from datetime import UTC, datetime
from uuid import UUID, uuid5

from sqlalchemy import text
from sqlalchemy.orm import Session, sessionmaker

from ..observability.events import append_event
from ..observability.scope import CompanyScope, set_company_scope

SEED_VERSION = 1
SEED_NAME = "agent-corporation-phase-04-v1"
DEMO_ENVIRONMENT_ID = UUID("b93f752e-7b69-5e8b-8f74-1498a15a5609")
DEMO_COMPANY_ID = UUID("b4375333-b12b-5fca-b984-87864032d3a8")
DEMO_SCOPE = CompanyScope(DEMO_ENVIRONMENT_ID, DEMO_COMPANY_ID)
FIXTURE_TIME = datetime(2026, 10, 8, 8, 0, tzinfo=UTC)
_NAMESPACE = UUID("e07bf511-7261-4b94-a25e-854ce07b0ad0")


def _id(key: str) -> UUID:
    return uuid5(_NAMESPACE, f"{SEED_NAME}:{key}")


def ensure_demo_scope(admin_session_factory: sessionmaker[Session]) -> None:
    """Create the fixed demo scope using the migration/admin DB role only."""
    with admin_session_factory() as session, session.begin():
        session.execute(
            text("""INSERT INTO environments(id, name, kind, release_locked)
                    VALUES (:id, 'Agent Corporation · Demo', 'demo', true)
                    ON CONFLICT (id) DO NOTHING"""),
            {"id": DEMO_ENVIRONMENT_ID},
        )
        environment = session.execute(
            text("SELECT kind, release_locked, name FROM environments WHERE id=:id"),
            {"id": DEMO_ENVIRONMENT_ID},
        ).mappings().one()
        if environment["kind"] != "demo" or not environment["release_locked"] or environment["name"] != "Agent Corporation · Demo":
            raise RuntimeError("Fixed demo environment exists with unexpected properties; refusing to overwrite")
        session.execute(
            text("""INSERT INTO companies(id, environment_id, name, mission)
                    VALUES (:id, :environment_id, 'Demo Corporation', 'Fixture bất hoạt để kiểm tra giao diện và quy trình.')
                    ON CONFLICT (id) DO NOTHING"""),
            {"id": DEMO_COMPANY_ID, "environment_id": DEMO_ENVIRONMENT_ID},
        )
        company = session.execute(
            text("SELECT environment_id, name FROM companies WHERE id=:id"),
            {"id": DEMO_COMPANY_ID},
        ).mappings().one()
        if company["environment_id"] != DEMO_ENVIRONMENT_ID or company["name"] != "Demo Corporation":
            raise RuntimeError("Fixed demo company exists with unexpected properties; refusing to overwrite")


def _event(
    session: Session,
    *,
    event_type: str,
    task_id: UUID,
    run_id: UUID | None,
    key: str,
    payload: dict[str, object],
) -> None:
    append_event(
        session,
        scope=DEMO_SCOPE,
        event_type=event_type,
        task_id=task_id,
        run_id=run_id,
        correlation_id=task_id or _id("seed-correlation"),
        parent_event_id=None,
        source="app",
        actor={"kind": "fixture", "id": SEED_NAME},
        sensitivity="internal",
        payload={"fixture": True, "seed_version": SEED_VERSION, **payload},
        evidence_refs=[],
        dedup_key=f"{SEED_NAME}:{key}",
        event_id=_id(f"event:{key}"),
        occurred_at=FIXTURE_TIME,
    )


def _insert_task(session: Session, key: str, goal: str, employee_id: UUID) -> UUID:
    task_id = _id(f"task:{key}")
    session.execute(
        text("""INSERT INTO work_orders(id, environment_id, company_id, created_by, created_at)
                VALUES (:id, :environment_id, :company_id, CAST(:created_by AS jsonb), :created_at)"""),
        {"id": task_id, "environment_id": DEMO_ENVIRONMENT_ID, "company_id": DEMO_COMPANY_ID,
         "created_by": json.dumps({"kind": "fixture", "id": SEED_NAME}), "created_at": FIXTURE_TIME},
    )
    session.execute(
        text("""INSERT INTO task_revisions(
                    task_id, environment_id, company_id, revision, goal, expected_outputs,
                    acceptance_criteria, scope, budget_limits, stop_conditions,
                    assignee_id, reviewer_id, autonomy, created_by, created_at
                ) VALUES (
                    :task_id, :environment_id, :company_id, 1, :goal, '["Bản ghi fixture"]'::jsonb,
                    '["fixture only"]'::jsonb, CAST(:scope AS jsonb),
                    CAST(:budget_limits AS jsonb),
                    '{"inference":"disabled"}'::jsonb, :employee_id, :employee_id, 'strict',
                    CAST(:created_by AS jsonb), :created_at
                )"""),
        {"task_id": task_id, "environment_id": DEMO_ENVIRONMENT_ID, "company_id": DEMO_COMPANY_ID,
         "goal": goal, "employee_id": employee_id,
         "scope": json.dumps({"fixture": True}),
         "budget_limits": json.dumps({"cost_basis": "unknown", "max_model_requests": 0, "usd_limit_micros": None}),
         "created_by": json.dumps({"kind": "fixture", "id": SEED_NAME}), "created_at": FIXTURE_TIME},
    )
    return task_id


def _task_state(session: Session, task_id: UUID, status: str, version: int) -> None:
    session.execute(
        text("""INSERT INTO task_execution_state(task_id, environment_id, company_id, revision, status, transition_version, updated_at)
                VALUES (:task_id, :environment_id, :company_id, 1, :status, :version, :updated_at)"""),
        {"task_id": task_id, "environment_id": DEMO_ENVIRONMENT_ID, "company_id": DEMO_COMPANY_ID,
         "status": status, "version": version, "updated_at": FIXTURE_TIME},
    )


def _run(session: Session, task_id: UUID, key: str, attempt: int, employee_version_id: UUID, status: str) -> UUID:
    run_id = _id(f"run:{key}:{attempt}")
    session.execute(
        text("""INSERT INTO runs(id, environment_id, company_id, task_id, task_revision, attempt,
                                  employee_version_id, profile_snapshot, created_at)
                VALUES (:id, :environment_id, :company_id, :task_id, 1, :attempt,
                        :employee_version_id, CAST(:profile AS jsonb), :created_at)"""),
        {"id": run_id, "environment_id": DEMO_ENVIRONMENT_ID, "company_id": DEMO_COMPANY_ID,
         "task_id": task_id, "attempt": attempt, "employee_version_id": employee_version_id,
         "profile": json.dumps({"fixture": True}),
         "created_at": FIXTURE_TIME},
    )
    session.execute(
        text("""INSERT INTO run_execution_state(run_id, environment_id, company_id, status, current_step, updated_at)
                VALUES (:run_id, :environment_id, :company_id, :status, 0, :updated_at)"""),
        {"run_id": run_id, "environment_id": DEMO_ENVIRONMENT_ID, "company_id": DEMO_COMPANY_ID,
         "status": status, "updated_at": FIXTURE_TIME},
    )
    return run_id


def _transition_events(session: Session, task_id: UUID, transitions: list[str]) -> None:
    for index, (previous, target) in enumerate(zip(transitions, transitions[1:]), start=1):
        _event(session, event_type="TASK_STATE_CHANGED", task_id=task_id, run_id=None,
               key=f"{task_id}:state:{index}", payload={"from": previous, "to": target})


def _seed(session: Session) -> None:
    set_company_scope(session, DEMO_SCOPE)
    departments = {name: _id(f"department:{name}") for name in ("operations", "research")}
    for key, name in (("operations", "Vận hành"), ("research", "Nghiên cứu")):
        session.execute(
            text("INSERT INTO departments(id, environment_id, company_id, name, created_at) VALUES (:id,:env,:company,:name,:created_at)"),
            {"id": departments[key], "env": DEMO_ENVIRONMENT_ID, "company": DEMO_COMPANY_ID, "name": name, "created_at": FIXTURE_TIME},
        )
    employees = {
        "mai": ("Mai Nguyễn", "Chief of Staff"),
        "an": ("An Trần", "Điều phối viên"),
        "linh": ("Linh Phạm", "Chuyên viên phân tích"),
    }
    versions: dict[str, UUID] = {}
    for key, (name, role) in employees.items():
        employee_id = _id(f"employee:{key}")
        version_id = _id(f"employee-version:{key}:1")
        versions[key] = version_id
        department = departments["research"] if key == "linh" else departments["operations"]
        session.execute(
            text("INSERT INTO employees(id,environment_id,company_id,department_id,lifecycle,created_at) VALUES (:id,:env,:company,:department,'active',:created_at)"),
            {"id": employee_id, "env": DEMO_ENVIRONMENT_ID, "company": DEMO_COMPANY_ID, "department": department, "created_at": FIXTURE_TIME},
        )
        session.execute(
            text("INSERT INTO employee_versions(id,environment_id,company_id,employee_id,version,profile,created_at) VALUES (:id,:env,:company,:employee,1,CAST(:profile AS jsonb),:created_at)"),
            {"id": version_id, "env": DEMO_ENVIRONMENT_ID, "company": DEMO_COMPANY_ID, "employee": employee_id,
             "profile": json.dumps({"display_name": name, "role": role, "fixture": True, "seed_version": SEED_VERSION}, ensure_ascii=False), "created_at": FIXTURE_TIME},
        )

    definitions = [
        ("idle", "draft", ["draft"], None),
        ("running", "executing", ["draft", "queued", "planning", "executing"], "running"),
        ("approval", "awaiting_approval", ["draft", "queued", "planning", "awaiting_approval"], "waiting_approval"),
        ("failed", "failed", ["draft", "queued", "planning", "executing", "failed"], "failed"),
        ("retry", "rework", ["draft", "queued", "planning", "executing", "reviewing", "rework"], "queued"),
    ]
    for key, status, path, run_status in definitions:
        assignee = _id("employee:an" if key in {"idle", "running", "approval"} else "employee:linh")
        task = _insert_task(session, key, f"[DEMO] Mẫu công việc {key}", assignee)
        _task_state(session, task, status, len(path))
        if len(path) > 1:
            _transition_events(session, task, path)
        run_id: UUID | None = None
        if key == "retry":
            failed_run = _run(session, task, key, 1, versions["linh"], "failed")
            _event(session, event_type="RUN_STATE_CHANGED", task_id=task, run_id=failed_run,
                   key=f"{key}:attempt-1-failed", payload={"from": "running", "to": "failed", "fixture_error": "DEMO_TRANSIENT_FAILURE"})
            _event(session, event_type="TASK_REWORK_REQUESTED", task_id=task, run_id=failed_run,
                   key=f"{key}:rework", payload={"reason": "Fixture minh họa retry; không thực thi.", "fixture_error": "DEMO_TRANSIENT_FAILURE"})
            run_id = _run(session, task, key, 2, versions["linh"], "queued")
        elif run_status:
            run_id = _run(session, task, key, 1, versions["an" if key in {"running", "approval"} else "linh"], run_status)
        if key == "approval":
            approval_id = _id("approval:approval")
            session.execute(
                text("""INSERT INTO approvals(id,environment_id,company_id,task_id,run_id,action_type,payload_hash,summary,status,created_at)
                        VALUES (:id,:env,:company,:task,:run,'tool_execution',:hash,'Fixture cần Chủ tịch duyệt','pending',:created_at)"""),
                {"id": approval_id, "env": DEMO_ENVIRONMENT_ID, "company": DEMO_COMPANY_ID, "task": task,
                 "run": run_id, "hash": hashlib.sha256(b"demo-approval-v1").hexdigest(), "created_at": FIXTURE_TIME},
            )
            _event(session, event_type="APPROVAL_REQUESTED", task_id=task, run_id=run_id,
                   key="approval:requested", payload={"approval_id": str(approval_id), "status": "pending"})
        if key == "failed":
            _event(session, event_type="TASK_FAILED", task_id=task, run_id=run_id,
                   key="failed:failure", payload={"error_code": "DEMO_VALIDATION_FAILED", "message": "Fixture lỗi có chủ đích."})
            artifact_id = _id("artifact:failure")
            session.execute(
                text("""INSERT INTO artifacts(id,environment_id,company_id,task_id,run_id,storage_key,sha256,mime_type,size_bytes,sensitivity,created_at)
                        VALUES (:id,:env,:company,:task,:run,:storage,:sha,'application/json',72,'internal',:created_at)"""),
                {"id": artifact_id, "env": DEMO_ENVIRONMENT_ID, "company": DEMO_COMPANY_ID, "task": task, "run": run_id,
                 "storage": f"demo/{SEED_VERSION}/failure-summary.json", "sha": hashlib.sha256(b'{"fixture":true}').hexdigest(), "created_at": FIXTURE_TIME},
            )
    _event(session, event_type="DEMO_SEEDED", task_id=None, run_id=None, key="seeded",
           payload={"seed": SEED_NAME, "seed_version": SEED_VERSION})


def reset_demo_dataset(session_factory: sessionmaker[Session]) -> dict[str, object]:
    """Atomically reset and reseed the pre-provisioned fixed demo scope."""
    with session_factory() as session, session.begin():
        session.execute(text("SELECT public.reset_agent_corporation_demo()"))
        _seed(session)
        return read_demo_dashboard_from_session(session)


def read_demo_dashboard_from_session(session: Session) -> dict[str, object]:
    set_company_scope(session, DEMO_SCOPE)
    company = session.execute(
        text("""SELECT c.id, c.name, e.id AS environment_id, e.name AS environment_name,
                         e.kind, e.release_locked
                  FROM companies c JOIN environments e ON e.id=c.environment_id
                 WHERE c.id=:company AND c.environment_id=:env"""),
        {"company": DEMO_COMPANY_ID, "env": DEMO_ENVIRONMENT_ID},
    ).mappings().first()
    if not company or company["kind"] != "demo" or not company["release_locked"]:
        return {"available": False, "seed_version": SEED_VERSION, "message": "Demo chưa được khởi tạo."}
    tasks = session.execute(
        text("""SELECT w.id, r.goal, s.status,
                         COALESCE((SELECT json_agg(json_build_object('attempt',run.attempt,'status',rs.status) ORDER BY run.attempt)
                                    FROM runs run JOIN run_execution_state rs ON rs.run_id=run.id AND rs.environment_id=run.environment_id AND rs.company_id=run.company_id
                                   WHERE run.task_id=w.id AND run.environment_id=w.environment_id AND run.company_id=w.company_id), '[]'::json) AS runs,
                         COALESCE((SELECT count(*) FROM approvals a WHERE a.task_id=w.id AND a.environment_id=w.environment_id AND a.company_id=w.company_id AND a.status='pending'),0) AS pending_approvals,
                         EXISTS(SELECT 1 FROM artifacts a WHERE a.task_id=w.id AND a.environment_id=w.environment_id AND a.company_id=w.company_id) AS has_artifact
                    FROM work_orders w JOIN task_revisions r ON r.task_id=w.id AND r.environment_id=w.environment_id AND r.company_id=w.company_id
                    JOIN task_execution_state s ON s.task_id=w.id AND s.environment_id=w.environment_id AND s.company_id=w.company_id
                   WHERE w.environment_id=:env AND w.company_id=:company ORDER BY r.goal"""),
        {"env": DEMO_ENVIRONMENT_ID, "company": DEMO_COMPANY_ID},
    ).mappings().all()
    departments = session.execute(
        text("""SELECT d.id,d.name,count(e.id) AS employee_count
                  FROM departments d LEFT JOIN employees e ON e.department_id=d.id AND e.environment_id=d.environment_id AND e.company_id=d.company_id
                 WHERE d.environment_id=:env AND d.company_id=:company GROUP BY d.id,d.name ORDER BY d.name"""),
        {"env": DEMO_ENVIRONMENT_ID, "company": DEMO_COMPANY_ID},
    ).mappings().all()
    employees = session.execute(
        text("""SELECT e.id, v.profile, v.version, d.name AS department
                  FROM employees e JOIN employee_versions v ON v.employee_id=e.id AND v.environment_id=e.environment_id AND v.company_id=e.company_id
                  LEFT JOIN departments d ON d.id=e.department_id AND d.environment_id=e.environment_id AND d.company_id=e.company_id
                 WHERE e.environment_id=:env AND e.company_id=:company ORDER BY e.id"""),
        {"env": DEMO_ENVIRONMENT_ID, "company": DEMO_COMPANY_ID},
    ).mappings().all()
    events = session.execute(text("SELECT count(*) FROM events WHERE environment_id=:env AND company_id=:company"),
                             {"env": DEMO_ENVIRONMENT_ID, "company": DEMO_COMPANY_ID}).scalar_one()
    event_manifest = session.execute(
        text("""SELECT event_id, event_type, task_id, run_id, correlation_id, dedup_key, payload, evidence_refs
                  FROM events WHERE environment_id=:env AND company_id=:company ORDER BY dedup_key"""),
        {"env": DEMO_ENVIRONMENT_ID, "company": DEMO_COMPANY_ID},
    ).mappings().all()
    payload: dict[str, object] = {
        "available": True, "seed": SEED_NAME, "seed_version": SEED_VERSION,
        "environment": {"id": str(company["environment_id"]), "name": company["environment_name"], "kind": "demo"},
        "company": {"id": str(company["id"]), "name": company["name"]},
        "departments": [{"id": str(item["id"]), "name": item["name"], "employee_count": item["employee_count"]} for item in departments],
        "employees": [{"id": str(item["id"]), "profile": item["profile"], "version": item["version"], "department": item["department"]} for item in employees],
        "tasks": [{"id": str(item["id"]), "goal": item["goal"], "status": item["status"], "runs": item["runs"],
                   "pending_approvals": item["pending_approvals"], "has_artifact": item["has_artifact"],
                   "usage_status": "unknown", "cost_basis": "unknown", "usd_cost_micros": None, "fixture": True} for item in tasks],
        "usage": {"status": "unknown", "cost_basis": "unknown", "usd_cost_micros": None},
        "event_count": events,
        "events": [{"id": str(item["event_id"]), "type": item["event_type"],
                    "task_id": str(item["task_id"]) if item["task_id"] else None,
                    "run_id": str(item["run_id"]) if item["run_id"] else None,
                    "correlation_id": str(item["correlation_id"]), "dedup_key": item["dedup_key"],
                    "payload": item["payload"], "evidence_refs": item["evidence_refs"]} for item in event_manifest],
        "inference_requests": 0,
    }
    canonical = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"), default=str)
    payload["manifest_sha256"] = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    return payload


def read_demo_dashboard(session_factory: sessionmaker[Session]) -> dict[str, object]:
    with session_factory() as session, session.begin():
        return read_demo_dashboard_from_session(session)
