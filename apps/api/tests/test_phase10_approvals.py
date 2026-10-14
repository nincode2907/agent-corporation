from datetime import UTC, datetime, timedelta
from uuid import uuid4

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from agent_corporation_api.modules.governance.approval_router import router
from agent_corporation_api.modules.governance.approvals import (
    ApprovalInvalid,
    _json_value,
    canonical_json,
    digest,
)
from agent_corporation_api.modules.governance.permission import evaluate_action


def test_approval_hash_uses_canonical_key_order_and_scope_fields():
    first = {"action": "permission_change", "payload": {"b": 2, "a": 1}, "company_id": "company-a"}
    reordered = {"company_id": "company-a", "payload": {"a": 1, "b": 2}, "action": "permission_change"}
    other_scope = {**reordered, "company_id": "company-b"}
    assert canonical_json(first) == canonical_json(reordered)
    assert digest(first) == digest(reordered)
    assert digest(first) != digest(other_scope)


@pytest.mark.parametrize("payload", [
    {"api_key": "secret-canary"},
    {"nested": {"access_token": "secret-canary"}},
    {"note": "Authorization: Bearer secret-canary"},
    {"amount_usd": 1.25},
])
def test_approval_payload_rejects_secrets_and_unstable_float_money(payload):
    with pytest.raises(ApprovalInvalid):
        _json_value(payload)


def test_approval_payload_accepts_secret_reference_without_secret_value():
    assert _json_value({"credential_ref": "local:codex:profile"}) == {"credential_ref": "local:codex:profile"}


def permission_context(**updates):
    value = {
        "action_type": "tool_execution", "payload_hash": "a" * 64,
        "environment_id": "env-a", "company_id": "company-a", "task_id": "task-a", "task_revision": 3, "run_id": "run-a",
        "policy_id": "policy-a", "policy_version": 4, "within_scope": True,
        "now": datetime.now(UTC),
    }
    value.update(updates)
    return value


def test_permission_engine_is_scope_checked_tiered_and_defaults_to_owner_review():
    automatic = evaluate_action(policy={"automatic_actions": ["tool_execution"]},
        **permission_context(action_type="tool_execution"))
    outside = evaluate_action(policy={"automatic_actions": ["tool_execution"]},
        **permission_context(action_type="tool_execution", within_scope=False))
    privileged = evaluate_action(policy={"automatic_actions": ["permission_change"]},
        **permission_context(action_type="permission_change"))
    unknown = evaluate_action(policy=None, **permission_context(action_type="tool_execution"))
    unsupported = evaluate_action(policy={"automatic_actions": ["read_fixture"]}, **permission_context(action_type="read_fixture"))
    assert automatic["allowed"] is True and automatic["tier"] == "automatic_in_scope"
    assert outside["allowed"] is False
    assert privileged["allowed"] is False and privileged["tier"] == "owner_approval"
    assert unknown["allowed"] is False and unknown["tier"] == "owner_approval"
    assert unsupported["allowed"] is False and unsupported["reason"] == "unknown_action"


def test_permission_engine_requires_exact_live_delegation_and_budget_reservation():
    now = datetime.now(UTC)
    delegation = {"status": "active", "action_type": "tool_execution", "environment_id": "env-a",
        "company_id": "company-a", "task_id": "task-a", "task_revision": 3, "run_id": "run-a", "policy_id": "policy-a",
        "policy_version": 4, "payload_hash": "a" * 64, "expires_at": now + timedelta(minutes=5)}
    context = permission_context(policy={"delegated_actions": ["tool_execution"]}, delegation=delegation, now=now)
    assert evaluate_action(**context, budget_reserved=False)["allowed"] is False
    result = evaluate_action(**context, budget_reserved=True)
    assert result["allowed"] is True and result["tier"] == "bounded_delegation"
    assert evaluate_action(**{**context, "delegation": {**delegation, "payload_hash": "b" * 64}}, budget_reserved=True)["allowed"] is False
    assert evaluate_action(**{**context, "delegation": {**delegation, "action_type": "external_send"}}, budget_reserved=True)["allowed"] is False
    assert evaluate_action(**{**context, "delegation": {**delegation, "task_revision": 2}}, budget_reserved=True)["allowed"] is False


def test_permission_engine_requires_current_approval_for_owner_only_action():
    now = datetime.now(UTC)
    approval = {"status": "approved", "payload_hash": "a" * 64, "environment_id": "env-a",
        "action_type": "permission_change", "company_id": "company-a", "task_id": "task-a", "task_revision": 3,
        "run_id": "run-a", "policy_id": "policy-a",
        "policy_version": 4, "expires_at": now + timedelta(minutes=5)}
    context = permission_context(action_type="permission_change", policy={"automatic_actions": ["permission_change"]},
        approval=approval, now=now)
    assert evaluate_action(**context)["allowed"] is True
    assert evaluate_action(**{**context, "approval": {**approval, "payload_hash": "b" * 64}})["allowed"] is False
    assert evaluate_action(**{**context, "approval": {**approval, "action_type": "budget_change"}})["allowed"] is False
    assert evaluate_action(**{**context, "approval": {**approval, "task_revision": 2}})["allowed"] is False
    assert evaluate_action(**{**context, "approval": {**approval, "consumed_at": now}})["allowed"] is False


def test_approval_routes_require_owner_before_database(monkeypatch):
    from agent_corporation_api.modules.governance import auth

    monkeypatch.setattr(auth, "get_session_factory", lambda: (_ for _ in ()).throw(AssertionError("database must not be reached")))
    app = FastAPI()
    app.include_router(router)
    client = TestClient(app, base_url="http://127.0.0.1:15501")
    assert client.get("/api/v1/approvals").status_code == 401
    body = {
        "task_id": str(uuid4()), "action_type": "permission_change", "summary": "Mở rộng quyền",
        "action_payload": {"capability": "tool:read"},
        "expires_at": (datetime.now(UTC) + timedelta(hours=1)).isoformat(),
    }
    assert client.post("/api/v1/approvals", json=body,
        headers={"Origin": "http://127.0.0.1:15500", "Idempotency-Key": str(uuid4())}).status_code == 401
    decision = {"decision": "approve", "expected_payload_hash": "a" * 64}
    assert client.post(f"/api/v1/approvals/{uuid4()}/decision", json=decision,
        headers={"Origin": "http://127.0.0.1:15500", "Idempotency-Key": str(uuid4())}).status_code == 401
