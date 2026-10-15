"""Deterministic HR proposal, assessment, and offboarding contracts.

These models describe proposals and required lifecycle work. They do not
authorize an API caller, create employees, revoke grants, or stop executions.
"""
from __future__ import annotations

import re
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class HRContractInvalid(ValueError):
    pass


class CostBasis(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True, frozen=True)

    status: Literal["confirmed", "estimated", "unknown"]
    amount_micros: int | None = Field(default=None, ge=0)
    currency: str | None = Field(default=None, pattern=r"^[A-Z]{3}$")
    basis: str | None = Field(default=None, min_length=1, max_length=120)
    source_ref: str | None = Field(default=None, min_length=1, max_length=160)

    @model_validator(mode="after")
    def amount_matches_status(self) -> "CostBasis":
        if self.status == "unknown":
            if any(value is not None for value in (self.amount_micros, self.currency, self.basis)):
                raise ValueError("unknown_cost_must_not_claim_amount")
        elif self.amount_micros is None or self.currency is None or self.basis is None:
            raise ValueError("known_cost_requires_amount_currency_and_basis")
        if self.status == "confirmed" and self.source_ref is None:
            raise ValueError("confirmed_cost_requires_source")
        if self.source_ref is not None and not _is_opaque_ref(self.source_ref):
            raise ValueError("cost_source_must_be_opaque_ref")
        return self


class ProbationCriterion(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True, frozen=True)

    id: str = Field(min_length=1, max_length=64, pattern=r"^[A-Za-z0-9._:-]+$")
    description: str = Field(min_length=1, max_length=500)
    evidence_kind: Literal["quality", "reliability", "scope", "need", "cost"]

    @field_validator("description")
    @classmethod
    def description_not_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("criterion_description_must_not_be_blank")
        return value


class HRProposal(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True, frozen=True)

    id: UUID
    environment_id: UUID
    company_id: UUID
    revision: int = Field(ge=1)
    need_statement: str = Field(min_length=1, max_length=2000)
    need_evidence_refs: list[str] = Field(min_length=1, max_length=30)
    contract_type: Literal["permanent", "on_demand", "contractor"]
    role: str = Field(min_length=1, max_length=120)
    model_profile_ref: str = Field(min_length=1, max_length=160)
    tool_capabilities: list[str] = Field(max_length=32)
    cost_basis: CostBasis
    probation_days: int = Field(ge=1, le=90)
    criteria: list[ProbationCriterion] = Field(min_length=1, max_length=20)
    proposed_by_employee_version_id: UUID | None = None

    @field_validator("need_statement", "role")
    @classmethod
    def required_text_not_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("required_text_must_not_be_blank")
        return value

    @field_validator("model_profile_ref")
    @classmethod
    def model_ref_is_opaque(cls, value: str) -> str:
        if not _is_opaque_ref(value):
            raise ValueError("model_profile_ref_must_be_opaque")
        return value

    @field_validator("need_evidence_refs")
    @classmethod
    def refs_are_unique_opaque(cls, values: list[str]) -> list[str]:
        if len(values) != len(set(values)):
            raise ValueError("duplicate_evidence_ref")
        for value in values:
            if not _is_opaque_ref(value):
                raise ValueError("evidence_refs_must_be_opaque")
        return values

    @field_validator("tool_capabilities")
    @classmethod
    def capabilities_are_unique(cls, values: list[str]) -> list[str]:
        if len(values) != len(set(values)):
            raise ValueError("duplicate_tool_capability")
        if any(not value or len(value) > 100 or not value.replace(":", "").replace("_", "").replace("-", "").isalnum() for value in values):
            raise ValueError("invalid_tool_capability")
        return values

    @field_validator("criteria")
    @classmethod
    def criterion_ids_are_unique(cls, values: list[ProbationCriterion]) -> list[ProbationCriterion]:
        ids = [criterion.id for criterion in values]
        if len(ids) != len(set(ids)):
            raise ValueError("duplicate_probation_criterion")
        return values


class HRDecision(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True, frozen=True)

    proposal_id: UUID
    proposal_revision: int = Field(ge=1)
    expected_company_id: UUID
    actor_role: Literal["owner", "agent"]
    decision: Literal["approve", "reject"]
    reason: str = Field(min_length=1, max_length=2000)
    decision_ref: str = Field(min_length=1, max_length=160)

    @field_validator("reason")
    @classmethod
    def reason_not_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("decision_reason_must_not_be_blank")
        return value

    @field_validator("decision_ref")
    @classmethod
    def decision_ref_is_opaque(cls, value: str) -> str:
        if not _is_opaque_ref(value):
            raise ValueError("decision_ref_must_be_opaque")
        return value


class HRProposalDecisionResult(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True, frozen=True)

    proposal_id: UUID
    proposal_revision: int
    state: Literal["approved_for_owner_execution", "rejected"]
    decision_ref: str
    employee_created: Literal[False] = False
    grants_changed: Literal[False] = False


def decide_hr_proposal(proposal: HRProposal, decision: HRDecision) -> HRProposalDecisionResult:
    """Record the proposal decision shape without applying a hire or permission."""
    if decision.actor_role != "owner":
        raise HRContractInvalid("owner_decision_required")
    if decision.proposal_id != proposal.id or decision.expected_company_id != proposal.company_id:
        raise HRContractInvalid("proposal_scope_mismatch")
    if decision.proposal_revision != proposal.revision:
        raise HRContractInvalid("stale_proposal_revision")
    state = "approved_for_owner_execution" if decision.decision == "approve" else "rejected"
    return HRProposalDecisionResult(
        proposal_id=proposal.id,
        proposal_revision=proposal.revision,
        state=state,
        decision_ref=decision.decision_ref,
    )


class ProbationCriterionResult(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True, frozen=True)

    criterion_id: str = Field(min_length=1, max_length=64)
    outcome: Literal["pass", "fail", "unknown"]
    evidence_refs: list[str] = Field(min_length=1, max_length=30)

    @field_validator("evidence_refs")
    @classmethod
    def evidence_refs_are_opaque(cls, values: list[str]) -> list[str]:
        if any(not _is_opaque_ref(value) for value in values):
            raise ValueError("assessment_evidence_must_be_opaque")
        return values


class ProbationAssessment(BaseModel):
    """Evidence assessment only; does not automatically retain or offboard."""
    model_config = ConfigDict(extra="forbid", strict=True, frozen=True)

    employee_id: UUID
    employee_version_id: UUID
    suite_version: str = Field(min_length=1, max_length=120)
    results: list[ProbationCriterionResult] = Field(min_length=1, max_length=20)
    quality_signal: Literal["positive", "mixed", "negative", "unknown"]
    ongoing_need: Literal["yes", "no", "unclear"]
    marginal_cost: CostBasis
    assessment_evidence_refs: list[str] = Field(min_length=1, max_length=30)

    @model_validator(mode="after")
    def result_ids_unique(self) -> "ProbationAssessment":
        ids = [result.criterion_id for result in self.results]
        if len(ids) != len(set(ids)):
            raise ValueError("duplicate_assessment_criterion")
        if any(not _is_opaque_ref(value) for value in self.assessment_evidence_refs):
            raise ValueError("assessment_evidence_must_be_opaque")
        return self


class ActiveRun(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True, frozen=True)

    run_id: UUID
    state: Literal["queued", "running", "unknown"]


class OffboardPlan(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True, frozen=True)

    employee_id: UUID
    expected_revision: int = Field(ge=1)
    next_lifecycle: Literal["draining"]
    deny_new_assignments: Literal[True] = True
    queued_run_ids_to_cancel: tuple[UUID, ...]
    running_run_ids_to_stop: tuple[UUID, ...]
    unknown_run_ids_to_reconcile: tuple[UUID, ...]
    preserve_history: Literal[True] = True


def begin_offboard(
    *, employee_id: UUID, current_lifecycle: str, current_revision: int,
    expected_revision: int, actor_role: str, active_runs: list[ActiveRun],
) -> OffboardPlan:
    """Plan owner-authorized drain/revoke work; no run action is executed here."""
    if actor_role != "owner":
        raise HRContractInvalid("owner_offboard_required")
    if current_lifecycle not in {"active", "probation"}:
        raise HRContractInvalid("employee_not_offboardable_from_current_state")
    if (
        type(current_revision) is not int
        or current_revision < 1
        or type(expected_revision) is not int
        or expected_revision < 1
        or expected_revision != current_revision
    ):
        raise HRContractInvalid("stale_employee_revision")
    run_ids = [run.run_id for run in active_runs]
    if len(run_ids) != len(set(run_ids)):
        raise HRContractInvalid("duplicate_active_run")
    return OffboardPlan(
        employee_id=employee_id,
        expected_revision=current_revision,
        next_lifecycle="draining",
        queued_run_ids_to_cancel=tuple(run.run_id for run in active_runs if run.state == "queued"),
        running_run_ids_to_stop=tuple(run.run_id for run in active_runs if run.state == "running"),
        unknown_run_ids_to_reconcile=tuple(run.run_id for run in active_runs if run.state == "unknown"),
    )


def complete_offboard(*, plan: OffboardPlan, current_revision: int, unresolved_run_ids: set[UUID]) -> int:
    """Return next employee revision only after all execution outcomes resolve."""
    if type(current_revision) is not int or current_revision < 1 or current_revision != plan.expected_revision:
        raise HRContractInvalid("stale_employee_revision")
    planned = set(plan.queued_run_ids_to_cancel + plan.running_run_ids_to_stop + plan.unknown_run_ids_to_reconcile)
    if unresolved_run_ids or planned & unresolved_run_ids:
        raise HRContractInvalid("runs_must_be_reconciled_before_offboard")
    return current_revision + 1


def _is_opaque_ref(value: str) -> bool:
    return bool(re.fullmatch(r"[A-Za-z][A-Za-z0-9_-]{0,31}:[A-Za-z0-9][A-Za-z0-9._:-]{0,127}", value)) and ".." not in value
