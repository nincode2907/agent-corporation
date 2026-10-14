"""Fail-closed policy evaluation shared by future action executors.

The current runtime has no tool executor. This evaluator is a backend contract and
is not itself evidence that external actions are dispatched or sandboxed.
"""
from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

OWNER_ONLY_ACTIONS = frozenset({
    "permission_change", "budget_change", "profile_change", "external_send",
    "deploy", "destructive_action", "chat_work_order_draft",
})
KNOWN_ACTIONS = OWNER_ONLY_ACTIONS | {"tool_execution"}


def _matches_expiry(value: Any, now: datetime) -> bool:
    if not isinstance(value, datetime) or value.tzinfo is None:
        return False
    return value.astimezone(UTC) > now.astimezone(UTC)


def evaluate_action(*, policy: dict[str, Any] | None, action_type: str, payload_hash: str,
                    environment_id: str, company_id: str, task_id: str | None, task_revision: int,
                    run_id: str | None,
                    policy_id: str | None, policy_version: int | None, within_scope: bool,
                    delegation: dict[str, Any] | None = None,
                    approval: dict[str, Any] | None = None,
                    budget_reserved: bool = False,
                    now: datetime | None = None) -> dict[str, object]:
    """Evaluate authorization from server-loaded evidence; absent facts deny.

    An agent cannot supply `policy`, `within_scope`, `delegation`, or `approval`;
    callers must derive them from current scoped database state.
    """
    now = now or datetime.now(UTC)
    if within_scope is not True:
        return {"allowed": False, "tier": "denied", "reason": "outside_scope"}
    if action_type not in KNOWN_ACTIONS:
        return {"allowed": False, "tier": "denied", "reason": "unknown_action"}
    policy = policy if isinstance(policy, dict) else {}
    automatic = policy.get("automatic_actions", [])
    delegated = policy.get("delegated_actions", [])
    owner_approval = policy.get("owner_approval_actions", [])
    if not all(isinstance(items, list) and all(isinstance(item, str) for item in items)
               for items in (automatic, delegated, owner_approval)):
        return {"allowed": False, "tier": "denied", "reason": "invalid_policy"}

    requires_owner = action_type in OWNER_ONLY_ACTIONS or action_type in owner_approval
    if requires_owner or (action_type not in automatic and action_type not in delegated):
        valid = bool(
            isinstance(approval, dict)
            and approval.get("status") == "approved"
            and approval.get("consumed_at") is None
            and approval.get("payload_hash") == payload_hash
            and approval.get("environment_id") == environment_id
            and approval.get("company_id") == company_id
            and approval.get("task_id") == task_id
            and approval.get("task_revision") == task_revision
            and approval.get("action_type") == action_type
            and approval.get("run_id") == run_id
            and approval.get("policy_id") == policy_id
            and approval.get("policy_version") == policy_version
            and _matches_expiry(approval.get("expires_at"), now)
        )
        if valid:
            return {"allowed": True, "tier": "chairman_approval", "reason": "matching_current_approval"}
        return {"allowed": False, "tier": "owner_approval", "reason": "approval_missing_or_stale"}
    if action_type in delegated:
        valid = bool(
            isinstance(delegation, dict)
            and delegation.get("status") == "active"
            and delegation.get("action_type") == action_type
            and delegation.get("environment_id") == environment_id
            and delegation.get("company_id") == company_id
            and delegation.get("task_id") == task_id
            and delegation.get("task_revision") == task_revision
            and delegation.get("run_id") == run_id
            and delegation.get("policy_id") == policy_id
            and delegation.get("policy_version") == policy_version
            and delegation.get("payload_hash") == payload_hash
            and _matches_expiry(delegation.get("expires_at"), now)
            and budget_reserved is True
        )
        if valid:
            return {"allowed": True, "tier": "bounded_delegation", "reason": "matching_delegation_and_reservation"}
        return {"allowed": False, "tier": "denied", "reason": "delegation_missing_or_stale"}
    if action_type in automatic:
        return {"allowed": True, "tier": "automatic_in_scope", "reason": "explicit_policy_allow"}
    return {"allowed": False, "tier": "denied", "reason": "default_deny"}
