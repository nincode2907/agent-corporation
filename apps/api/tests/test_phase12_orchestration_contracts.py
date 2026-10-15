from uuid import UUID

import pytest
from pydantic import ValidationError

from agent_corporation_api.modules.orchestration.contracts import (
    DelegationLimits,
    DelegationPlan,
    Handoff,
    OrchestrationInvalid,
    RoutingPolicy,
    RoutingRequest,
    SubtaskNode,
    route_task,
    validate_delegation_plan,
)


ENV = UUID("00000000-0000-0000-0000-000000000001")
COMPANY = UUID("00000000-0000-0000-0000-000000000002")
PARENT = UUID("00000000-0000-0000-0000-000000000003")
CORRELATION = UUID("00000000-0000-0000-0000-000000000004")
A = UUID("00000000-0000-0000-0000-000000000010")
B = UUID("00000000-0000-0000-0000-000000000011")
C = UUID("00000000-0000-0000-0000-000000000012")
LIMITS = DelegationLimits(max_nodes=8, max_fanout=3, max_depth=4, max_iterations=2)


def plan(*nodes: SubtaskNode) -> DelegationPlan:
    return DelegationPlan(
        environment_id=ENV,
        company_id=COMPANY,
        parent_task_id=PARENT,
        correlation_id=CORRELATION,
        nodes=list(nodes),
    )


def test_routing_is_deterministic_and_respects_policy_caps():
    policy = RoutingPolicy(
        simple_task_max_steps=3, max_task_steps=20, max_workers=3, delegation_enabled=True
    )
    assert route_task(RoutingRequest(estimated_steps=2, required_roles=1), policy) == "direct"
    assert route_task(RoutingRequest(estimated_steps=4, required_roles=1), policy) == "supervisor"
    assert route_task(RoutingRequest(estimated_steps=2, required_roles=2), policy) == "supervisor"
    assert route_task(
        RoutingRequest(estimated_steps=21, required_roles=1), policy
    ) == "blocked"
    assert route_task(
        RoutingRequest(estimated_steps=4, required_roles=1),
        policy.model_copy(update={"delegation_enabled": False}),
    ) == "blocked"


def test_valid_dag_returns_stable_parent_before_child_order():
    value = plan(
        SubtaskNode(id=B, parent_id=A, dependencies=[A]),
        SubtaskNode(id=A, parent_id=PARENT),
        SubtaskNode(id=C, parent_id=PARENT, dependencies=[A]),
    )
    order = validate_delegation_plan(value, LIMITS)
    assert order.index(A) < order.index(B)
    assert order.index(A) < order.index(C)
    assert validate_delegation_plan(value, LIMITS) == order


def test_cycle_unknown_parent_dependency_and_duplicate_dependency_are_rejected():
    cyclic = plan(
        SubtaskNode(id=A, parent_id=PARENT, dependencies=[B]),
        SubtaskNode(id=B, parent_id=A, dependencies=[A]),
    )
    with pytest.raises(OrchestrationInvalid, match="cyclic_delegation_plan"):
        validate_delegation_plan(cyclic, LIMITS)

    unknown = plan(SubtaskNode(id=A, parent_id=C))
    with pytest.raises(OrchestrationInvalid, match="unknown_parent_or_dependency"):
        validate_delegation_plan(unknown, LIMITS)

    duplicate_dependency = plan(SubtaskNode(id=A, parent_id=PARENT, dependencies=[B, B]))
    with pytest.raises(OrchestrationInvalid, match="duplicate_dependency"):
        validate_delegation_plan(duplicate_dependency, LIMITS)


def test_fanout_depth_iteration_and_node_limits_are_enforced():
    with pytest.raises(OrchestrationInvalid, match="limits_must_be_integers"):
        validate_delegation_plan(
            plan(SubtaskNode(id=A, parent_id=PARENT)),
            DelegationLimits(max_nodes=True, max_fanout=1, max_depth=1, max_iterations=1),
        )

    wide = plan(
        SubtaskNode(id=A, parent_id=PARENT),
        SubtaskNode(id=B, parent_id=PARENT),
        SubtaskNode(id=C, parent_id=PARENT),
    )
    with pytest.raises(OrchestrationInvalid, match="fanout_limit_exceeded"):
        validate_delegation_plan(wide, DelegationLimits(8, 2, 4, 2))

    deep = plan(
        SubtaskNode(id=A, parent_id=PARENT),
        SubtaskNode(id=B, parent_id=A),
        SubtaskNode(id=C, parent_id=B),
    )
    with pytest.raises(OrchestrationInvalid, match="depth_limit_exceeded"):
        validate_delegation_plan(deep, DelegationLimits(8, 3, 2, 2))

    too_many_iterations = plan(SubtaskNode(id=A, parent_id=PARENT, iteration=3))
    with pytest.raises(OrchestrationInvalid, match="iteration_limit_exceeded"):
        validate_delegation_plan(too_many_iterations, LIMITS)

    with pytest.raises(OrchestrationInvalid, match="node_limit_exceeded"):
        validate_delegation_plan(wide, DelegationLimits(2, 2, 2, 2))


def test_handoff_requires_parent_correlation_summary_and_opaque_evidence_refs():
    handoff = Handoff(
        parent_task_id=PARENT,
        subtask_id=A,
        correlation_id=CORRELATION,
        from_employee_version_id=UUID("00000000-0000-0000-0000-000000000020"),
        to_employee_version_id=UUID("00000000-0000-0000-0000-000000000021"),
        decision_summary="Review findings and requested one correction.",
        evidence_refs=["artifact:abc123", "run:run-42"],
    )
    assert handoff.correlation_id == CORRELATION
    with pytest.raises(ValidationError):
        Handoff.model_validate({**handoff.model_dump(), "decision_summary": "  "})
    with pytest.raises(ValidationError):
        Handoff.model_validate({**handoff.model_dump(), "evidence_refs": ["../../secret"]})
    with pytest.raises(ValidationError):
        Handoff.model_validate({**handoff.model_dump(), "evidence_refs": []})
    with pytest.raises(ValidationError):
        Handoff.model_validate({**handoff.model_dump(), "evidence_refs": ["artifact:"]})


def test_contracts_reject_unreviewed_fields_instead_of_accepting_scope_claims():
    with pytest.raises(ValidationError):
        RoutingRequest(estimated_steps=1, required_roles=1, company_id=COMPANY)
