from datetime import datetime, timedelta, timezone
from uuid import UUID

import pytest
from pydantic import ValidationError

from agent_corporation_api.modules.finance.contracts import (
    BudgetReservation,
    CostFact,
    FinanceContractInvalid,
    FinanceLedgerEntry,
    PricingSnapshot,
    UsageSnapshot,
    aggregate_accepted_task_lifetime,
    aggregate_period,
    reconcile_usage_snapshots,
    transition_reservation,
)


ENV = UUID("00000000-0000-0000-0000-000000000001")
COMPANY = UUID("00000000-0000-0000-0000-000000000002")
NOW = datetime(2026, 10, 15, tzinfo=timezone.utc)
HASH = "a" * 64


def usage(sequence, *, tokens=12, source="gateway:final", digest=HASH):
    return UsageSnapshot(
        environment_id=ENV, company_id=COMPANY, call_ref="call:one", source_ref=source,
        sequence=sequence, observed_at=NOW + timedelta(seconds=sequence),
        input_tokens=tokens - 4, output_tokens=4, total_tokens=tokens,
        cached_input_tokens=2, reasoning_output_tokens=1, source_payload_sha256=digest,
    )


def entry(call, amount, *, occurred_at=NOW, accepted_task="task:accepted", basis="actual_api", currency="USD", measurement="confirmed", chat=None, company=COMPANY):
    cost = CostFact(call_ref=call, basis=basis, measurement=measurement,
                    amount_micros=amount, currency=currency if measurement != "unknown" else None,
                    source_ref="invoice:line-1" if measurement == "confirmed" else None)
    return FinanceLedgerEntry(
        environment_id=ENV, company_id=company, employee_ref="employee:one", task_ref=None if chat else "task:work",
        accepted_task_ref=None if chat else accepted_task, accepted_at=NOW if not chat else None,
        model_ref="model:one", call_ref=call, occurred_at=occurred_at, cost=cost,
        chat_conversation_ref=chat,
    )


def test_usage_dedup_selects_highest_cumulative_sequence_and_never_sums_subdivisions():
    old = usage(1, tokens=12)
    latest = usage(2, tokens=18, digest="b" * 64)
    assert reconcile_usage_snapshots((old, latest, old)).total_tokens == 18
    assert latest.cached_input_tokens == 2
    assert latest.reasoning_output_tokens == 1
    with pytest.raises(FinanceContractInvalid, match="conflicting_usage_snapshot_sequence"):
        reconcile_usage_snapshots((old, usage(1, tokens=13, digest="c" * 64)))


def test_usage_unknown_is_null_and_invalid_totals_are_rejected():
    unknown = UsageSnapshot(environment_id=ENV, company_id=COMPANY, call_ref="call:x", source_ref="adapter:one",
                            sequence=0, observed_at=NOW, source_payload_sha256=HASH)
    assert unknown.total_tokens is None
    with pytest.raises(ValidationError, match="usage_total_mismatch"):
        UsageSnapshot(environment_id=ENV, company_id=COMPANY, call_ref="call:x", source_ref="adapter:one",
                      sequence=0, observed_at=NOW, input_tokens=2, output_tokens=3, total_tokens=4,
                      source_payload_sha256=HASH)


def test_pricing_snapshots_are_versioned_and_cost_basis_does_not_claim_subscription_invoice():
    price = PricingSnapshot(id=UUID("00000000-0000-0000-0000-000000000011"), provider_ref="provider:gw",
                            model_ref="model:x", version="2026-10-a", currency="USD",
                            input_micros_per_million=100, output_micros_per_million=200,
                            effective_at=NOW, source_ref="price:published")
    assert price.version == "2026-10-a"
    with pytest.raises(ValidationError, match="subscription_cost_must_not_claim_token_pricing"):
        CostFact(call_ref="call:x", basis="subscription", measurement="confirmed", amount_micros=10,
                 currency="USD", pricing_snapshot_id=price.id, source_ref="invoice:line")
    with pytest.raises(ValidationError, match="api_equivalent_is_not_confirmed"):
        CostFact(call_ref="call:x", basis="api_equivalent", measurement="confirmed", amount_micros=10,
                 currency="USD", source_ref="gateway:usage")


def test_unknown_cost_is_not_zero_and_confirmed_cost_requires_source():
    unknown = CostFact(call_ref="call:x", basis="unknown", measurement="unknown")
    assert unknown.amount_micros is None
    with pytest.raises(ValidationError, match="unknown_cost_must_not"):
        CostFact(call_ref="call:x", basis="unknown", measurement="unknown", amount_micros=0, currency="USD")
    with pytest.raises(ValidationError, match="confirmed_cost_requires_source"):
        CostFact(call_ref="call:x", basis="actual_api", measurement="confirmed", amount_micros=1, currency="USD")


def test_budget_transition_is_revision_fenced_and_unresolved_does_not_settle_zero():
    reservation = BudgetReservation(id=UUID("00000000-0000-0000-0000-000000000010"), grant_ref="grant:g",
                                   resource="requests", limit_amount=1, reserved_amount=1,
                                   state="reserved", revision=1, call_ref="call:1")
    unresolved = transition_reservation(reservation, expected_revision=1, action="mark_unresolved")
    assert unresolved.state == "unresolved" and unresolved.settled_amount is None
    with pytest.raises(FinanceContractInvalid, match="reservation_already_terminal"):
        transition_reservation(unresolved, expected_revision=2, action="release")
    with pytest.raises(FinanceContractInvalid, match="stale_reservation_revision"):
        transition_reservation(reservation, expected_revision=2, action="release")
    with pytest.raises(FinanceContractInvalid, match="stale_reservation_revision"):
        transition_reservation(reservation, expected_revision=True, action="release")
    with pytest.raises(FinanceContractInvalid, match="settlement_requires_amount"):
        transition_reservation(reservation, expected_revision=1, action="settle", settled_amount=0.5, call_ref="call:1")
    with pytest.raises(FinanceContractInvalid, match="dispatched_reservation_cannot_be_released"):
        transition_reservation(reservation, expected_revision=1, action="release")
    with pytest.raises(FinanceContractInvalid, match="settlement_call_ref_must_be_opaque"):
        transition_reservation(reservation, expected_revision=1, action="settle", settled_amount=1, call_ref="../bad")


def test_period_cost_and_accepted_task_lifetime_are_separate_and_exclude_chat():
    entries = (
        entry("call:old", 2_000_000, occurred_at=NOW - timedelta(days=30)),
        entry("call:new", 3_000_000),
        entry("call:child", 500_000, accepted_task="task:accepted"),
        entry("call:chat", 900_000, chat="conversation:private"),
    )
    period = aggregate_period(entries, start=NOW - timedelta(days=1), end=NOW + timedelta(days=1), as_of=NOW + timedelta(days=1))
    lifetime = aggregate_accepted_task_lifetime(entries, accepted_task_ref="task:accepted", as_of=NOW + timedelta(days=1))
    assert period.amount_micros == 3_500_000
    assert lifetime.amount_micros == 5_500_000
    assert period.currency == lifetime.currency == "USD"


def test_period_and_lifetime_aggregates_report_unknown_instead_of_partial_zero():
    rows = (entry("call:known", 10), entry("call:unknown", None, measurement="unknown", basis="unknown"))
    result = aggregate_accepted_task_lifetime(rows, accepted_task_ref="task:accepted", as_of=NOW + timedelta(days=1))
    assert result.amount_micros is None and result.missing_count == 1
    assert result.measurement == "mixed"


def test_aggregate_does_not_combine_mixed_currency_and_rejects_duplicate_call_entries():
    mixed = aggregate_period((entry("call:usd", 1), entry("call:eur", 1, currency="EUR")),
                             start=NOW - timedelta(days=1), end=NOW + timedelta(days=1), as_of=NOW + timedelta(days=1))
    assert mixed.amount_micros is None and mixed.currency is None
    with pytest.raises(FinanceContractInvalid, match="duplicate_ledger_call"):
        aggregate_period((entry("call:dup", 1), entry("call:dup", 1)),
                         start=NOW - timedelta(days=1), end=NOW + timedelta(days=1), as_of=NOW + timedelta(days=1))


def test_empty_period_is_unknown_and_company_scope_cannot_be_combined():
    empty = aggregate_period((), start=NOW - timedelta(days=1), end=NOW + timedelta(days=1), as_of=NOW + timedelta(days=1))
    assert empty.amount_micros is None and empty.measurement == "unknown"
    cross_company = (entry("call:a", 10), entry("call:b", 30, company=UUID("00000000-0000-0000-0000-000000000099")))
    with pytest.raises(FinanceContractInvalid, match="aggregate_scope_mismatch"):
        aggregate_period(cross_company, start=NOW - timedelta(days=1), end=NOW + timedelta(days=1), as_of=NOW + timedelta(days=1))
    with pytest.raises(FinanceContractInvalid, match="aggregate_scope_mismatch"):
        aggregate_accepted_task_lifetime(cross_company, accepted_task_ref="task:accepted", as_of=NOW + timedelta(days=1))
