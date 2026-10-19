from uuid import UUID

import pytest
from pydantic import ValidationError

from agent_corporation_api.modules.hr.contracts import (
    ActiveRun,
    CostBasis,
    HRContractInvalid,
    HRDecision,
    HRProposal,
    ProbationAssessment,
    ProbationCriterion,
    ProbationCriterionResult,
    begin_offboard,
    complete_offboard,
    decide_hr_proposal,
)


ENV = UUID("00000000-0000-0000-0000-000000000001")
COMPANY = UUID("00000000-0000-0000-0000-000000000002")
PROPOSAL = UUID("00000000-0000-0000-0000-000000000010")
EMPLOYEE = UUID("00000000-0000-0000-0000-000000000020")
VERSION = UUID("00000000-0000-0000-0000-000000000021")
RUN_QUEUED = UUID("00000000-0000-0000-0000-000000000030")
RUNNING = UUID("00000000-0000-0000-0000-000000000031")
RUN_UNKNOWN = UUID("00000000-0000-0000-0000-000000000032")


def proposal(**overrides):
    values = {
        "id": PROPOSAL,
        "environment_id": ENV,
        "company_id": COMPANY,
        "revision": 2,
        "need_statement": "Need QA coverage during the release window.",
        "need_evidence_refs": ["workload:forecast-4"],
        "contract_type": "on_demand",
        "role": "QA specialist",
        "model_profile_ref": "model:qa-profile-v2",
        "tool_capabilities": ["workspace:read"],
        "cost_basis": {"status": "unknown"},
        "probation_days": 14,
        "criteria": [
            {"id": "quality", "description": "Find seeded defects.", "evidence_kind": "quality"},
            {"id": "scope", "description": "Stay within assigned workspace.", "evidence_kind": "scope"},
        ],
    }
    values.update(overrides)
    return HRProposal(**values)


def test_proposal_requires_need_evidence_probation_criteria_and_cost_provenance():
    value = proposal()
    assert value.cost_basis.status == "unknown"
    assert value.contract_type == "on_demand"
    assert len(value.criteria) == 2
    with pytest.raises(ValidationError):
        proposal(need_evidence_refs=[])
    with pytest.raises(ValidationError):
        proposal(probation_days=0)
    with pytest.raises(ValidationError):
        proposal(cost_basis={"status": "confirmed", "amount_micros": 200, "currency": "USD", "basis": "guess"})
    with pytest.raises(ValidationError):
        proposal(cost_basis={"status": "unknown", "amount_micros": 0})
    with pytest.raises(ValidationError):
        proposal(model_profile_ref="../../model")
    with pytest.raises(ValidationError):
        proposal(need_evidence_refs=["artifact:"])


def test_owner_decision_only_records_proposal_outcome_and_never_creates_employee_or_grants():
    value = proposal()
    approved = HRDecision(
        proposal_id=PROPOSAL,
        proposal_revision=2,
        expected_company_id=COMPANY,
        actor_role="owner",
        decision="approve",
        reason="Need and criteria were reviewed.",
        decision_ref="decision:owner-01",
    )
    result = decide_hr_proposal(value, approved)
    assert result.state == "approved_for_owner_execution"
    assert result.employee_created is False
    assert result.grants_changed is False

    with pytest.raises(HRContractInvalid, match="owner_decision_required"):
        decide_hr_proposal(value, approved.model_copy(update={"actor_role": "agent"}))
    with pytest.raises(HRContractInvalid, match="stale_proposal_revision"):
        decide_hr_proposal(value, approved.model_copy(update={"proposal_revision": 1}))
    with pytest.raises(HRContractInvalid, match="proposal_scope_mismatch"):
        decide_hr_proposal(value, approved.model_copy(update={"expected_company_id": ENV}))


def test_rejection_is_auditable_but_does_not_change_employee_state():
    rejected = HRDecision(
        proposal_id=PROPOSAL,
        proposal_revision=2,
        expected_company_id=COMPANY,
        actor_role="owner",
        decision="reject",
        reason="The need evidence is insufficient.",
        decision_ref="decision:owner-02",
    )
    result = decide_hr_proposal(proposal(), rejected)
    assert result.state == "rejected"
    assert result.employee_created is False
    assert result.grants_changed is False


def test_probation_assessment_uses_criteria_evidence_and_keeps_unknown_cost_explicit():
    assessment = ProbationAssessment(
        employee_id=EMPLOYEE,
        employee_version_id=VERSION,
        suite_version="qa-suite-v1",
        results=[
            ProbationCriterionResult(criterion_id="quality", outcome="pass", evidence_refs=["test:report-1"]),
            ProbationCriterionResult(criterion_id="scope", outcome="unknown", evidence_refs=["audit:trace-1"]),
        ],
        quality_signal="mixed",
        ongoing_need="yes",
        marginal_cost=CostBasis(status="unknown"),
        assessment_evidence_refs=["assessment:batch-1"],
    )
    assert assessment.quality_signal == "mixed"
    assert assessment.results[1].outcome == "unknown"
    with pytest.raises(ValidationError):
        ProbationCriterionResult(criterion_id="quality", outcome="pass", evidence_refs=[])
    with pytest.raises(ValidationError):
        ProbationAssessment.model_validate({**assessment.model_dump(), "token_usage": 999})


def test_offboard_plan_blocks_new_assignments_and_partitions_active_run_outcomes():
    plan = begin_offboard(
        employee_id=EMPLOYEE,
        current_lifecycle="probation",
        current_revision=7,
        expected_revision=7,
        actor_role="owner",
        active_runs=[
            ActiveRun(run_id=RUN_QUEUED, state="queued"),
            ActiveRun(run_id=RUNNING, state="running"),
            ActiveRun(run_id=RUN_UNKNOWN, state="unknown"),
        ],
    )
    assert plan.deny_new_assignments is True
    assert plan.queued_run_ids_to_cancel == (RUN_QUEUED,)
    assert plan.running_run_ids_to_stop == (RUNNING,)
    assert plan.unknown_run_ids_to_reconcile == (RUN_UNKNOWN,)
    assert plan.preserve_history is True
    with pytest.raises(HRContractInvalid, match="owner_offboard_required"):
        begin_offboard(
            employee_id=EMPLOYEE, current_lifecycle="active", current_revision=7,
            expected_revision=7, actor_role="agent", active_runs=[]
        )
    with pytest.raises(HRContractInvalid, match="stale_employee_revision"):
        begin_offboard(
            employee_id=EMPLOYEE, current_lifecycle="active", current_revision=7,
            expected_revision=6, actor_role="owner", active_runs=[]
        )
    with pytest.raises(HRContractInvalid, match="stale_employee_revision"):
        begin_offboard(
            employee_id=EMPLOYEE, current_lifecycle="active", current_revision=1,
            expected_revision=True, actor_role="owner", active_runs=[]
        )


def test_offboard_completion_waits_for_run_reconciliation_and_is_versioned():
    plan = begin_offboard(
        employee_id=EMPLOYEE,
        current_lifecycle="active",
        current_revision=7,
        expected_revision=7,
        actor_role="owner",
        active_runs=[ActiveRun(run_id=RUNNING, state="running")],
    )
    with pytest.raises(HRContractInvalid, match="runs_must_be_reconciled"):
        complete_offboard(plan=plan, current_revision=7, unresolved_run_ids={RUNNING})
    assert complete_offboard(plan=plan, current_revision=7, unresolved_run_ids=set()) == 8
    with pytest.raises(HRContractInvalid, match="stale_employee_revision"):
        complete_offboard(plan=plan, current_revision=8, unresolved_run_ids=set())
    with pytest.raises(HRContractInvalid, match="stale_employee_revision"):
        complete_offboard(plan=plan, current_revision=True, unresolved_run_ids=set())
