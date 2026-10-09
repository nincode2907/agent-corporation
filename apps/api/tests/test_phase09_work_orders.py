from datetime import UTC, datetime, timedelta

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import ValidationError

from agent_corporation_api.modules.work.router import TaskAction, WorkOrderInput
from agent_corporation_api.modules.work.router import router as work_orders_router


def valid_work_order(**updates):
    value = {
        "goal": "Tổng hợp báo cáo đã cấp",
        "expected_outputs": ["Báo cáo"],
        "acceptance_criteria": [{"id": "AC01", "description": "Có nguồn", "evidence_kind": "owner_review"}],
        "scope": {"input_refs": ["demo:brief-01"], "tool_capabilities": []},
        "deadline_at": None,
        "budget_limits": {"max_model_requests": 0, "cost_basis": "unknown", "usd_limit_micros": None},
        "stop_conditions": {"max_duration_seconds": 120, "max_rework_rounds": 0},
        "assignee_id": None,
        "reviewer_id": None,
        "autonomy": "strict",
    }
    value.update(updates)
    return value


def test_work_order_contract_accepts_bounded_no_inference_task():
    result = WorkOrderInput.model_validate(valid_work_order())
    assert result.budget_limits.max_model_requests == 0
    assert result.budget_limits.cost_basis == "unknown"
    assert result.scope.tool_capabilities == []


@pytest.mark.parametrize("updates", [
    {"goal": "  "},
    {"expected_outputs": [" "]},
    {"scope": {"input_refs": ["/etc/passwd"], "tool_capabilities": []}},
    {"scope": {"input_refs": ["demo:../secret"], "tool_capabilities": []}},
    {"scope": {"input_refs": ["demo:brief"], "tool_capabilities": ["shell"]}},
    {"budget_limits": {"max_model_requests": 1, "cost_basis": "unknown"}},
    {"stop_conditions": {"max_duration_seconds": 0, "max_rework_rounds": 0}},
    {"autonomy": "unrestricted"},
])
def test_work_order_contract_rejects_invalid_scope_or_authority(updates):
    with pytest.raises(ValidationError):
        WorkOrderInput.model_validate(valid_work_order(**updates))


def test_work_order_deadline_must_be_timezone_aware_and_future():
    with pytest.raises(ValidationError):
        WorkOrderInput.model_validate(valid_work_order(deadline_at=datetime.now() + timedelta(hours=1)))
    with pytest.raises(ValidationError):
        WorkOrderInput.model_validate(valid_work_order(deadline_at=datetime.now(UTC) - timedelta(seconds=1)))


def test_task_action_contract_bounds_priority_and_requires_version():
    assert TaskAction.model_validate({"action": "enqueue", "expected_version": 1, "priority": 100})
    for payload in (
        {"action": "enqueue", "expected_version": 0},
        {"action": "enqueue", "expected_version": 1, "priority": 101},
        {"action": "accepted", "expected_version": 1},
        {"action": "cancel", "expected_version": 1, "extra": True},
    ):
        with pytest.raises(ValidationError):
            TaskAction.model_validate(payload)


def test_work_order_routes_require_owner_session_before_database(monkeypatch):
    from agent_corporation_api.modules.governance import auth

    monkeypatch.setattr(auth, "get_session_factory", lambda: (_ for _ in ()).throw(AssertionError("database must not be reached")))
    app = FastAPI()
    app.include_router(work_orders_router)
    client = TestClient(app, base_url="http://127.0.0.1:15501")

    assert client.get("/api/v1/work-orders").status_code == 401
    response = client.post("/api/v1/work-orders", json=valid_work_order(), headers={"Origin": "http://127.0.0.1:15500"})
    assert response.status_code == 401
