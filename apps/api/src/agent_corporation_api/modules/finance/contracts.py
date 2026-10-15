"""Immutable finance and budget value contracts.

These pure contracts do not persist a ledger or provide transactional budget
reservation. Runtime/database atomicity remains an integration requirement.
"""
from __future__ import annotations

import hashlib
import json
import re
from datetime import date, datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, model_validator


class FinanceContractInvalid(ValueError):
    pass


OpaqueRef = str
CostBasis = Literal["actual_api", "subscription", "api_equivalent", "local_compute", "unknown"]
Measurement = Literal["confirmed", "estimated", "unknown"]


class UsageSnapshot(BaseModel):
    """A versioned source observation; cached/reasoning are subdivisions."""
    model_config = ConfigDict(extra="forbid", strict=True, frozen=True)

    environment_id: UUID
    company_id: UUID
    call_ref: OpaqueRef = Field(pattern=r"^[A-Za-z][A-Za-z0-9_-]{0,31}:[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$")
    source_ref: OpaqueRef = Field(pattern=r"^[A-Za-z][A-Za-z0-9_-]{0,31}:[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$")
    sequence: int = Field(ge=0)
    observed_at: datetime
    input_tokens: int | None = Field(default=None, ge=0)
    output_tokens: int | None = Field(default=None, ge=0)
    total_tokens: int | None = Field(default=None, ge=0)
    cached_input_tokens: int | None = Field(default=None, ge=0)
    reasoning_output_tokens: int | None = Field(default=None, ge=0)
    source_payload_sha256: str = Field(pattern=r"^[a-f0-9]{64}$")

    @model_validator(mode="after")
    def validate_observation(self) -> "UsageSnapshot":
        if self.observed_at.tzinfo is None:
            raise ValueError("usage_timestamp_must_be_timezone_aware")
        if self.total_tokens is not None:
            if self.input_tokens is None or self.output_tokens is None:
                raise ValueError("total_usage_requires_input_and_output")
            if self.total_tokens != self.input_tokens + self.output_tokens:
                raise ValueError("usage_total_mismatch")
        if self.cached_input_tokens is not None and self.input_tokens is not None and self.cached_input_tokens > self.input_tokens:
            raise ValueError("cached_tokens_exceed_input_tokens")
        if self.reasoning_output_tokens is not None and self.output_tokens is not None and self.reasoning_output_tokens > self.output_tokens:
            raise ValueError("reasoning_tokens_exceed_output_tokens")
        return self


def reconcile_usage_snapshots(snapshots: tuple[UsageSnapshot, ...]) -> UsageSnapshot:
    """Select the newest cumulative observation for one source and call."""
    if not snapshots:
        raise FinanceContractInvalid("usage_snapshot_required")
    first = snapshots[0]
    scope = (first.environment_id, first.company_id, first.call_ref, first.source_ref)
    if any((s.environment_id, s.company_id, s.call_ref, s.source_ref) != scope for s in snapshots):
        raise FinanceContractInvalid("usage_snapshot_scope_mismatch")
    by_sequence: dict[int, UsageSnapshot] = {}
    for snapshot in snapshots:
        prior = by_sequence.get(snapshot.sequence)
        if prior is not None and prior != snapshot:
            raise FinanceContractInvalid("conflicting_usage_snapshot_sequence")
        by_sequence[snapshot.sequence] = snapshot
    return by_sequence[max(by_sequence)]


class PricingSnapshot(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True, frozen=True)

    id: UUID
    provider_ref: OpaqueRef = Field(pattern=r"^[A-Za-z][A-Za-z0-9_-]{0,31}:[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$")
    model_ref: OpaqueRef = Field(pattern=r"^[A-Za-z][A-Za-z0-9_-]{0,31}:[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$")
    version: str = Field(min_length=1, max_length=120)
    currency: str = Field(pattern=r"^[A-Z]{3}$")
    input_micros_per_million: int | None = Field(default=None, ge=0)
    output_micros_per_million: int | None = Field(default=None, ge=0)
    effective_at: datetime
    source_ref: OpaqueRef = Field(pattern=r"^[A-Za-z][A-Za-z0-9_-]{0,31}:[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$")

    @model_validator(mode="after")
    def timestamp_aware(self) -> "PricingSnapshot":
        if self.effective_at.tzinfo is None:
            raise ValueError("pricing_timestamp_must_be_timezone_aware")
        return self


class CostFact(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True, frozen=True)

    call_ref: OpaqueRef
    basis: CostBasis
    measurement: Measurement
    amount_micros: int | None = Field(default=None, ge=0)
    currency: str | None = Field(default=None, pattern=r"^[A-Z]{3}$")
    pricing_snapshot_id: UUID | None = None
    source_ref: OpaqueRef | None = None

    @model_validator(mode="after")
    def fields_match_certainty(self) -> "CostFact":
        if self.measurement == "unknown":
            if self.amount_micros is not None or self.currency is not None:
                raise ValueError("unknown_cost_must_not_be_zero_or_amount")
        elif self.amount_micros is None or self.currency is None:
            raise ValueError("known_cost_requires_amount_and_currency")
        if self.measurement == "confirmed" and self.source_ref is None:
            raise ValueError("confirmed_cost_requires_source")
        if self.basis == "unknown" and self.measurement != "unknown":
            raise ValueError("unknown_basis_cannot_have_known_measurement")
        if self.basis == "subscription" and self.pricing_snapshot_id is not None:
            raise ValueError("subscription_cost_must_not_claim_token_pricing")
        if self.basis == "api_equivalent" and self.measurement == "confirmed":
            raise ValueError("api_equivalent_is_not_confirmed_invoice_cost")
        return self


class FinanceLedgerEntry(BaseModel):
    """One observed call linked to its complete subject and reporting dates."""
    model_config = ConfigDict(extra="forbid", strict=True, frozen=True)

    environment_id: UUID
    company_id: UUID
    department_ref: OpaqueRef | None = None
    employee_ref: OpaqueRef
    task_ref: OpaqueRef | None = None
    model_ref: OpaqueRef
    call_ref: OpaqueRef
    occurred_at: datetime
    cost: CostFact
    accepted_at: datetime | None = None
    accepted_task_ref: OpaqueRef | None = None
    parent_task_ref: OpaqueRef | None = None
    chat_conversation_ref: OpaqueRef | None = None

    @model_validator(mode="after")
    def scope_and_subject(self) -> "FinanceLedgerEntry":
        if self.occurred_at.tzinfo is None or (self.accepted_at is not None and self.accepted_at.tzinfo is None):
            raise ValueError("ledger_timestamps_must_be_timezone_aware")
        if self.cost.call_ref != self.call_ref:
            raise ValueError("ledger_cost_call_mismatch")
        if self.accepted_at is not None and (self.accepted_task_ref is None or self.task_ref is None):
            raise ValueError("accepted_cohort_requires_task_and_acceptance")
        if self.chat_conversation_ref is not None and (self.task_ref is not None or self.accepted_task_ref is not None):
            raise ValueError("chat_calls_must_not_enter_task_cohort")
        return self


class CorrectionFact(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True, frozen=True)

    call_ref: OpaqueRef
    correction_ref: OpaqueRef
    source_ref: OpaqueRef
    corrected_cost: CostFact
    occurred_at: datetime

    @model_validator(mode="after")
    def linked_and_timed(self) -> "CorrectionFact":
        if self.corrected_cost.call_ref != self.call_ref:
            raise ValueError("correction_call_mismatch")
        if self.occurred_at.tzinfo is None:
            raise ValueError("correction_timestamp_must_be_timezone_aware")
        return self


class BudgetReservation(BaseModel):
    """State transition input; callers must persist it under a DB transaction."""
    model_config = ConfigDict(extra="forbid", strict=True, frozen=True)

    id: UUID
    grant_ref: OpaqueRef
    resource: Literal["requests", "tokens", "cost"]
    limit_amount: int = Field(ge=0)
    reserved_amount: int = Field(ge=0)
    settled_amount: int | None = Field(default=None, ge=0)
    state: Literal["reserved", "settled", "released", "unresolved"]
    revision: int = Field(ge=1)
    call_ref: OpaqueRef | None = Field(default=None, pattern=r"^[A-Za-z][A-Za-z0-9_-]{0,31}:[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$")

    @model_validator(mode="after")
    def state_is_consistent(self) -> "BudgetReservation":
        if self.reserved_amount > self.limit_amount:
            raise ValueError("reservation_exceeds_limit")
        if self.state == "settled" and (self.settled_amount is None or self.call_ref is None):
            raise ValueError("settled_reservation_requires_amount_and_call")
        if self.state == "unresolved" and self.settled_amount is not None:
            raise ValueError("unresolved_reservation_must_not_settle_as_zero")
        if self.state == "unresolved" and self.call_ref is None:
            raise ValueError("unresolved_reservation_requires_dispatched_call")
        if self.call_ref is not None and (not re.fullmatch(r"[A-Za-z][A-Za-z0-9_-]{0,31}:[A-Za-z0-9][A-Za-z0-9._:-]{0,127}", self.call_ref) or ".." in self.call_ref):
            raise ValueError("reservation_call_ref_must_be_opaque")
        if self.state == "released" and self.call_ref is not None:
            raise ValueError("dispatched_reservation_cannot_be_released")
        if self.state in {"reserved", "released"} and self.settled_amount is not None:
            raise ValueError("unsettled_reservation_has_settlement")
        return self


def transition_reservation(
    current: BudgetReservation, *, expected_revision: int,
    action: Literal["settle", "release", "mark_unresolved"], settled_amount: int | None = None,
    call_ref: str | None = None,
) -> BudgetReservation:
    if type(expected_revision) is not int or current.revision != expected_revision:
        raise FinanceContractInvalid("stale_reservation_revision")
    if current.state != "reserved":
        raise FinanceContractInvalid("reservation_already_terminal")
    if action == "settle":
        if type(settled_amount) is not int or settled_amount < 0 or call_ref is None:
            raise FinanceContractInvalid("settlement_requires_amount_and_call")
        if not re.fullmatch(r"[A-Za-z][A-Za-z0-9_-]{0,31}:[A-Za-z0-9][A-Za-z0-9._:-]{0,127}", call_ref) or ".." in call_ref:
            raise FinanceContractInvalid("settlement_call_ref_must_be_opaque")
        if settled_amount > min(current.limit_amount, current.reserved_amount):
            raise FinanceContractInvalid("settlement_exceeds_limit")
        return BudgetReservation.model_validate({**current.model_dump(), "state": "settled", "settled_amount": settled_amount, "call_ref": call_ref, "revision": current.revision + 1})
    if action == "release":
        if current.call_ref is not None:
            raise FinanceContractInvalid("dispatched_reservation_cannot_be_released")
        return BudgetReservation.model_validate({**current.model_dump(), "state": "released", "revision": current.revision + 1})
    if current.call_ref is None:
        raise FinanceContractInvalid("unresolved_reservation_requires_dispatched_call")
    return BudgetReservation.model_validate({**current.model_dump(), "state": "unresolved", "revision": current.revision + 1})


class AggregateResult(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True, frozen=True)
    amount_micros: int | None
    currency: str | None
    basis: CostBasis
    measurement: Literal["confirmed", "estimated", "unknown", "mixed"]
    entry_count: int = Field(ge=0)
    missing_count: int = Field(ge=0)
    as_of: datetime


def aggregate_period(entries: tuple[FinanceLedgerEntry, ...], *, start: datetime, end: datetime, as_of: datetime) -> AggregateResult:
    if any(x.tzinfo is None for x in (start, end, as_of)) or end <= start:
        raise FinanceContractInvalid("invalid_reporting_window")
    selected = tuple(e for e in entries if start <= e.occurred_at < end and e.occurred_at <= as_of and e.chat_conversation_ref is None)
    _require_single_company_scope(selected)
    return _aggregate(selected, as_of)


def aggregate_accepted_task_lifetime(entries: tuple[FinanceLedgerEntry, ...], *, accepted_task_ref: str, as_of: datetime) -> AggregateResult:
    if as_of.tzinfo is None:
        raise FinanceContractInvalid("as_of_must_be_timezone_aware")
    selected = tuple(e for e in entries if e.accepted_task_ref == accepted_task_ref and e.occurred_at <= as_of and e.chat_conversation_ref is None)
    _require_single_company_scope(selected)
    return _aggregate(selected, as_of)


def _aggregate(entries: tuple[FinanceLedgerEntry, ...], as_of: datetime) -> AggregateResult:
    if not entries:
        return AggregateResult(amount_micros=None, currency=None, basis="unknown", measurement="unknown", entry_count=0, missing_count=0, as_of=as_of)
    calls = [entry.call_ref for entry in entries]
    if len(calls) != len(set(calls)):
        raise FinanceContractInvalid("duplicate_ledger_call")
    costs = [entry.cost for entry in entries]
    known = [cost for cost in costs if cost.measurement != "unknown"]
    combinations = {(cost.basis, cost.currency) for cost in known}
    same_unit = len(combinations) == 1
    missing = sum(cost.measurement == "unknown" for cost in costs)
    amount = sum(cost.amount_micros or 0 for cost in known) if same_unit and not missing else None
    bases = {cost.basis for cost in costs}
    basis = next(iter(bases)) if len(bases) == 1 else "unknown"
    currencies = {cost.currency for cost in known}
    currency = next(iter(currencies)) if same_unit and len(currencies) == 1 else None
    measurements = {cost.measurement for cost in costs}
    measurement = next(iter(measurements)) if len(measurements) == 1 else "mixed"
    if not same_unit:
        measurement = "mixed"
    return AggregateResult(amount_micros=amount, currency=currency, basis=basis, measurement=measurement, entry_count=len(entries), missing_count=missing, as_of=as_of)


def _require_single_company_scope(entries: tuple[FinanceLedgerEntry, ...]) -> None:
    scopes = {(entry.environment_id, entry.company_id) for entry in entries}
    if len(scopes) > 1:
        raise FinanceContractInvalid("aggregate_scope_mismatch")


def canonical_ledger_digest(entries: tuple[FinanceLedgerEntry, ...]) -> str:
    payload = [entry.model_dump(mode="json") for entry in sorted(entries, key=lambda item: item.call_ref)]
    return hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
