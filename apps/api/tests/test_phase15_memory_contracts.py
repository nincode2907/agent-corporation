from datetime import datetime, timedelta, timezone
from uuid import UUID

import pytest
from pydantic import ValidationError

from agent_corporation_api.modules.memory.contracts import (
    ContextRequest,
    ContextScope,
    ContextSource,
    MemoryContractInvalid,
    MemoryProposal,
    MemoryVersion,
    PromotionDecision,
    build_context_manifest,
    memory_is_retrievable,
    promote_memory,
    rollback_memory,
)


ENV = UUID("00000000-0000-0000-0000-000000000001")
COMPANY = UUID("00000000-0000-0000-0000-000000000002")
EMPLOYEE = UUID("00000000-0000-0000-0000-000000000003")
DEPARTMENT = UUID("00000000-0000-0000-0000-000000000004")
TASK = UUID("00000000-0000-0000-0000-000000000005")
VERSION_1 = UUID("00000000-0000-0000-0000-000000000010")
VERSION_2 = UUID("00000000-0000-0000-0000-000000000011")
ACTOR = UUID("00000000-0000-0000-0000-000000000020")
NOW = datetime(2026, 10, 15, 9, 0, tzinfo=timezone.utc)
HASH_A = "a" * 64
HASH_B = "b" * 64


def context_source(ref="policy:base-v1", *, content_ref="artifact:ctx-1", scope=None, byte_count=12, trust="reviewed", digest=HASH_A):
    return ContextSource(
        ref=ref,
        version_id=VERSION_1,
        scope=scope or ContextScope(environment_id=ENV, company_id=COMPANY, layer="corporate"),
        content_sha256=digest,
        byte_count=byte_count,
        trust=trust,
        content_ref=content_ref,
    )


def context_request(**overrides):
    values = {
        "requester_employee_id": EMPLOYEE,
        "purpose_ref": "task:task-10",
        "max_sources": 5,
        "max_bytes": 100,
        "allowed_layers": ("corporate", "department", "employee", "task", "working"),
    }
    values.update(overrides)
    return ContextRequest(**values)


def proposal(**overrides):
    values = {
        "id": VERSION_2,
        "environment_id": ENV,
        "company_id": COMPANY,
        "layer": "department",
        "department_id": DEPARTMENT,
        "title": "Release checklist lesson",
        "content_ref": "memory:lesson-2",
        "source_refs": ("run:run-17",),
        "evidence_refs": ("test:report-17",),
        "source_trust": "agent_generated",
        "expires_at": NOW + timedelta(days=30),
    }
    values.update(overrides)
    return MemoryProposal(**values)


def memory(version, *, ident, digest, expires_at=None, layer="department", department_id=DEPARTMENT):
    return MemoryVersion(
        id=ident,
        environment_id=ENV,
        company_id=COMPANY,
        layer=layer,
        department_id=department_id if layer == "department" else None,
        employee_id=EMPLOYEE if layer == "employee" else None,
        version=version,
        title=f"Lesson {version}",
        content_ref=f"memory:lesson-{version}",
        content_sha256=digest,
        source_refs=(f"run:source-{version}",),
        evidence_refs=(f"test:evidence-{version}",),
        reviewed_by=ACTOR,
        decision_ref=f"decision:owner-{version}",
        created_at=NOW,
        expires_at=expires_at,
    )


def test_five_context_layers_require_their_own_scope_keys():
    for layer, key, value in [
        ("department", "department_id", DEPARTMENT),
        ("employee", "employee_id", EMPLOYEE),
        ("task", "task_id", TASK),
        ("working", "working_id", VERSION_2),
    ]:
        assert ContextScope(environment_id=ENV, company_id=COMPANY, layer=layer, **{key: value}).layer == layer
    with pytest.raises(ValidationError, match="scope_mismatch"):
        ContextScope(environment_id=ENV, company_id=COMPANY, layer="employee")
    with pytest.raises(ValidationError, match="scope_mismatch"):
        ContextScope(environment_id=ENV, company_id=COMPANY, layer="corporate", employee_id=EMPLOYEE)


def test_context_manifest_is_explicit_bounded_and_deterministic_for_same_selection():
    source = context_source()
    request = context_request()
    kwargs = dict(
        request=request,
        environment_id=ENV,
        company_id=COMPANY,
        sources=[source],
        authorized_refs=frozenset({source.ref}),
        now=NOW,
    )
    one = build_context_manifest(**kwargs)
    two = build_context_manifest(**kwargs)
    assert one.total_bytes == 12
    assert one.manifest_sha256 == two.manifest_sha256
    assert one.id != two.id
    with pytest.raises(MemoryContractInvalid, match="byte_budget_exceeded"):
        build_context_manifest(
            **{**kwargs, "request": request.model_copy(update={"max_bytes": 11})}
        )
    with pytest.raises(MemoryContractInvalid, match="source_count_out_of_bounds"):
        build_context_manifest(
            **{**kwargs, "request": request.model_copy(update={"max_sources": 0})}
        )


def test_context_selection_denies_unapproved_refs_cross_company_and_unallowed_layer():
    source = context_source()
    base = dict(
        request=context_request(), environment_id=ENV, company_id=COMPANY,
        sources=[source], now=NOW,
    )
    with pytest.raises(MemoryContractInvalid, match="context_acl_denied"):
        build_context_manifest(**base, authorized_refs=frozenset())

    cross_company = context_source(
        scope=ContextScope(environment_id=ENV, company_id=UUID("00000000-0000-0000-0000-000000000099"), layer="corporate")
    )
    with pytest.raises(MemoryContractInvalid, match="context_scope_mismatch"):
        build_context_manifest(**{**base, "sources": [cross_company]}, authorized_refs=frozenset({cross_company.ref}))

    employee_source = context_source(
        ref="employee:private-v1",
        scope=ContextScope(environment_id=ENV, company_id=COMPANY, layer="employee", employee_id=EMPLOYEE),
    )
    restricted = context_request(allowed_layers=("corporate",))
    with pytest.raises(MemoryContractInvalid, match="context_layer_not_allowed"):
        build_context_manifest(
            **{**base, "request": restricted, "sources": [employee_source]},
            authorized_refs=frozenset({employee_source.ref}),
        )


def test_context_selection_rejects_duplicate_and_malformed_references():
    source = context_source()
    with pytest.raises(MemoryContractInvalid, match="duplicate_context_source"):
        build_context_manifest(
            request=context_request(), environment_id=ENV, company_id=COMPANY,
            sources=[source, source], authorized_refs=frozenset({source.ref}), now=NOW,
        )
    with pytest.raises(ValidationError):
        context_source(ref="../../secret")
    with pytest.raises(ValidationError):
        context_source(content_ref="../../outside")


def test_promotion_requires_evidence_review_scope_and_never_accepts_policy_changes():
    proposal_value = proposal()
    reviewer = PromotionDecision(
        proposal_id=proposal_value.id,
        expected_proposal_sha256=proposal_value.payload_sha256,
        actor_role="reviewer",
        actor_id=ACTOR,
        outcome="approve",
        decision_ref="decision:review-1",
        reviewer_grant_ref="grant:memory-test-1",
    )
    created = promote_memory(
        proposal=proposal_value,
        decision=reviewer,
        current_version=0,
        expected_current_version=0,
        content_sha256=HASH_B,
        now=NOW,
        expected_scope=(ENV, COMPANY),
    )
    assert created is not None
    assert created.version == 1
    assert created.source_refs == proposal_value.source_refs
    assert created.evidence_refs == proposal_value.evidence_refs
    with pytest.raises(MemoryContractInvalid, match="stale_current_memory_version"):
        promote_memory(
            proposal=proposal_value, decision=reviewer, current_version=1, expected_current_version=0,
            content_sha256=HASH_B, now=NOW, expected_scope=(ENV, COMPANY),
        )
    changed_proposal = proposal(title="Changed after approval")
    with pytest.raises(MemoryContractInvalid, match="payload_changed_after_review"):
        promote_memory(
            proposal=changed_proposal, decision=reviewer, current_version=0, expected_current_version=0,
            content_sha256=HASH_B, now=NOW, expected_scope=(ENV, COMPANY),
        )
    with pytest.raises(MemoryContractInvalid, match="corporate_memory_requires_owner"):
        corporate_proposal = proposal(layer="corporate", department_id=None)
        promote_memory(
            proposal=corporate_proposal,
            decision=reviewer.model_copy(update={"proposal_id": corporate_proposal.id, "expected_proposal_sha256": corporate_proposal.payload_sha256}),
            current_version=0, expected_current_version=0, content_sha256=HASH_B, now=NOW,
            expected_scope=(ENV, COMPANY),
        )
    with pytest.raises(ValidationError):
        proposal(requested_policy_change=True)
    with pytest.raises(MemoryContractInvalid, match="reviewer_memory_grant_required"):
        promote_memory(
            proposal=proposal_value,
            decision=reviewer.model_copy(update={"reviewer_grant_ref": None}),
            current_version=0, expected_current_version=0, content_sha256=HASH_B, now=NOW,
            expected_scope=(ENV, COMPANY),
        )


def test_rejected_expired_or_cross_scope_memory_proposal_cannot_promote():
    proposal_value = proposal()
    rejected = PromotionDecision(
        proposal_id=proposal_value.id, expected_proposal_sha256=proposal_value.payload_sha256,
        actor_role="reviewer", actor_id=ACTOR,
        outcome="reject", decision_ref="decision:reject-1", reviewer_grant_ref="grant:g1",
    )
    assert promote_memory(
        proposal=proposal_value, decision=rejected, current_version=0,
        expected_current_version=0, content_sha256=HASH_B, now=NOW, expected_scope=(ENV, COMPANY),
    ) is None
    approved = rejected.model_copy(update={"outcome": "approve"})
    with pytest.raises(MemoryContractInvalid, match="memory_scope_mismatch"):
        promote_memory(
            proposal=proposal_value, decision=approved, current_version=0,
            expected_current_version=0, content_sha256=HASH_B, now=NOW,
            expected_scope=(ENV, UUID("00000000-0000-0000-0000-000000000099")),
        )
    expired = proposal(expires_at=NOW - timedelta(seconds=1))
    with pytest.raises(MemoryContractInvalid, match="proposal_expired"):
        promote_memory(
            proposal=expired,
            decision=approved.model_copy(update={"proposal_id": expired.id, "expected_proposal_sha256": expired.payload_sha256}),
            current_version=0, expected_current_version=0, content_sha256=HASH_B, now=NOW,
            expected_scope=(ENV, COMPANY),
        )


def test_rollback_appends_a_new_version_and_does_not_mutate_prior_versions():
    version1 = memory(1, ident=VERSION_1, digest=HASH_A)
    version2 = memory(2, ident=VERSION_2, digest=HASH_B)
    rolled_back = rollback_memory(current=version2, target=version1, expected_current_version=2, now=NOW)
    assert rolled_back.version == 3
    assert rolled_back.rollback_of_version_id == version1.id
    assert rolled_back.supersedes_version_id == version2.id
    assert version1.version == 1 and version1.content_sha256 == HASH_A
    assert version2.version == 2 and version2.content_sha256 == HASH_B
    with pytest.raises(MemoryContractInvalid, match="rollback_target_scope_or_order_invalid"):
        rollback_memory(current=version2, target=version2, expected_current_version=2, now=NOW)


def test_retrieval_requires_exact_authorized_version_and_unexpired_company_scope():
    expiry = NOW + timedelta(days=1)
    version = memory(1, ident=VERSION_1, digest=HASH_A, expires_at=expiry)
    assert memory_is_retrievable(
        version, now=NOW, authorized_scope=(ENV, COMPANY), authorized_version_ids=frozenset({VERSION_1})
    )
    assert not memory_is_retrievable(
        version, now=NOW, authorized_scope=(ENV, COMPANY), authorized_version_ids=frozenset()
    )
    assert not memory_is_retrievable(
        version, now=NOW, authorized_scope=(ENV, UUID("00000000-0000-0000-0000-000000000099")),
        authorized_version_ids=frozenset({VERSION_1}),
    )
    assert not memory_is_retrievable(
        version, now=expiry, authorized_scope=(ENV, COMPANY), authorized_version_ids=frozenset({VERSION_1})
    )
