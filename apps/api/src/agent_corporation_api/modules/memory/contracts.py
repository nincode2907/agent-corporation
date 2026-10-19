"""Scoped context selection and append-only memory promotion contracts.

All ACL decisions are supplied by the trusted caller. These models do not
persist data, retrieve sources, or grant memory/policy authority.
"""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from typing import Literal
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class MemoryContractInvalid(ValueError):
    pass


ContextLayer = Literal["corporate", "department", "employee", "task", "working"]


class ContextScope(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True, frozen=True)

    environment_id: UUID
    company_id: UUID
    layer: ContextLayer
    department_id: UUID | None = None
    employee_id: UUID | None = None
    task_id: UUID | None = None
    working_id: UUID | None = None

    @model_validator(mode="after")
    def layer_has_exact_scope(self) -> "ContextScope":
        required = {
            "corporate": (),
            "department": ("department_id",),
            "employee": ("employee_id",),
            "task": ("task_id",),
            "working": ("working_id",),
        }[self.layer]
        for field_name in ("department_id", "employee_id", "task_id", "working_id"):
            value = getattr(self, field_name)
            if (field_name in required) != (value is not None):
                raise ValueError("context_layer_scope_mismatch")
        return self


class ContextSource(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True, frozen=True)

    ref: str = Field(min_length=1, max_length=160, pattern=r"^[A-Za-z][A-Za-z0-9_-]{0,31}:[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$")
    version_id: UUID
    scope: ContextScope
    content_sha256: str = Field(pattern=r"^[a-f0-9]{64}$")
    byte_count: int = Field(ge=0, le=10_000_000)
    trust: Literal["owner_authored", "reviewed", "user_input", "agent_generated", "imported"]
    content_ref: str = Field(min_length=1, max_length=160)

    @field_validator("content_ref")
    @classmethod
    def content_locator_is_opaque(cls, value: str) -> str:
        if not _is_opaque_ref(value):
            raise ValueError("context_content_ref_must_be_opaque")
        return value


class ContextRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True, frozen=True)

    requester_employee_id: UUID
    purpose_ref: str = Field(min_length=1, max_length=160)
    max_sources: int = Field(ge=1, le=100)
    max_bytes: int = Field(ge=1, le=1_000_000)
    allowed_layers: tuple[ContextLayer, ...] = Field(min_length=1, max_length=5)

    @field_validator("allowed_layers")
    @classmethod
    def layers_unique(cls, values: tuple[ContextLayer, ...]) -> tuple[ContextLayer, ...]:
        if len(values) != len(set(values)):
            raise ValueError("duplicate_context_layer")
        return values


class ContextManifest(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True, frozen=True)

    id: UUID
    environment_id: UUID
    company_id: UUID
    requester_employee_id: UUID
    purpose_ref: str
    sources: tuple[ContextSource, ...] = Field(min_length=1, max_length=100)
    total_bytes: int = Field(ge=0)
    max_bytes: int = Field(ge=1)
    manifest_sha256: str = Field(pattern=r"^[a-f0-9]{64}$")
    created_at: datetime


def build_context_manifest(
    *,
    request: ContextRequest,
    environment_id: UUID,
    company_id: UUID,
    sources: list[ContextSource],
    authorized_refs: frozenset[str],
    now: datetime | None = None,
) -> ContextManifest:
    """Build explicit, bounded snapshots only from caller-authorized refs."""
    if not sources or len(sources) > request.max_sources:
        raise MemoryContractInvalid("context_source_count_out_of_bounds")
    refs = [source.ref for source in sources]
    if len(refs) != len(set(refs)):
        raise MemoryContractInvalid("duplicate_context_source")
    if any(ref not in authorized_refs for ref in refs):
        raise MemoryContractInvalid("context_acl_denied")
    if any(source.scope.environment_id != environment_id or source.scope.company_id != company_id for source in sources):
        raise MemoryContractInvalid("context_scope_mismatch")
    if any(source.scope.layer not in request.allowed_layers for source in sources):
        raise MemoryContractInvalid("context_layer_not_allowed")
    total_bytes = sum(source.byte_count for source in sources)
    if total_bytes > request.max_bytes:
        raise MemoryContractInvalid("context_byte_budget_exceeded")
    timestamp = now or datetime.now(timezone.utc)
    if timestamp.tzinfo is None:
        raise MemoryContractInvalid("context_timestamp_must_be_timezone_aware")
    payload = {
        "environment_id": str(environment_id),
        "company_id": str(company_id),
        "requester_employee_id": str(request.requester_employee_id),
        "purpose_ref": request.purpose_ref,
        "sources": [
            {
                "ref": source.ref,
                "version_id": str(source.version_id),
                "content_sha256": source.content_sha256,
                "content_ref": source.content_ref,
                "byte_count": source.byte_count,
                "trust": source.trust,
                "scope": source.scope.model_dump(mode="json"),
            }
            for source in sources
        ],
        "total_bytes": total_bytes,
    }
    digest = hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    return ContextManifest(
        id=uuid4(),
        environment_id=environment_id,
        company_id=company_id,
        requester_employee_id=request.requester_employee_id,
        purpose_ref=request.purpose_ref,
        sources=tuple(sources),
        total_bytes=total_bytes,
        max_bytes=request.max_bytes,
        manifest_sha256=digest,
        created_at=timestamp,
    )


class MemoryProposal(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True, frozen=True)

    id: UUID
    environment_id: UUID
    company_id: UUID
    layer: Literal["corporate", "department", "employee"]
    department_id: UUID | None = None
    employee_id: UUID | None = None
    title: str = Field(min_length=1, max_length=200)
    content_ref: str = Field(min_length=1, max_length=160)
    source_refs: tuple[str, ...] = Field(min_length=1, max_length=50)
    evidence_refs: tuple[str, ...] = Field(min_length=1, max_length=50)
    source_trust: Literal["reviewed", "agent_generated", "user_input", "imported"]
    requested_policy_change: Literal[False] = False
    expires_at: datetime | None = None

    @model_validator(mode="after")
    def scope_matches_layer(self) -> "MemoryProposal":
        if not self.title.strip():
            raise ValueError("memory_title_must_not_be_blank")
        if self.layer == "department" and self.department_id is None:
            raise ValueError("department_memory_requires_department")
        if self.layer != "department" and self.department_id is not None:
            raise ValueError("unexpected_department_scope")
        if self.layer == "employee" and self.employee_id is None:
            raise ValueError("employee_memory_requires_employee")
        if self.layer != "employee" and self.employee_id is not None:
            raise ValueError("unexpected_employee_scope")
        if len(self.source_refs) != len(set(self.source_refs)) or len(self.evidence_refs) != len(set(self.evidence_refs)):
            raise ValueError("duplicate_memory_reference")
        for ref in (*self.source_refs, *self.evidence_refs):
            if not _is_opaque_ref(ref):
                raise ValueError("memory_references_must_be_scoped_opaque_refs")
        if not _is_opaque_ref(self.content_ref):
            raise ValueError("memory_content_ref_must_be_opaque")
        if self.expires_at is not None and self.expires_at.tzinfo is None:
            raise ValueError("memory_expiry_must_be_timezone_aware")
        return self

    @property
    def payload_sha256(self) -> str:
        payload = self.model_dump(mode="json")
        return hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


class PromotionDecision(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True, frozen=True)

    proposal_id: UUID
    expected_proposal_sha256: str = Field(pattern=r"^[a-f0-9]{64}$")
    actor_role: Literal["reviewer", "owner"]
    actor_id: UUID
    outcome: Literal["approve", "reject"]
    decision_ref: str = Field(min_length=1, max_length=160)
    reviewer_grant_ref: str | None = Field(default=None, max_length=160)


class MemoryVersion(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True, frozen=True)

    id: UUID
    environment_id: UUID
    company_id: UUID
    layer: Literal["corporate", "department", "employee"]
    department_id: UUID | None = None
    employee_id: UUID | None = None
    version: int = Field(ge=1)
    title: str = Field(min_length=1, max_length=200)
    content_ref: str
    content_sha256: str = Field(pattern=r"^[a-f0-9]{64}$")
    source_refs: tuple[str, ...]
    evidence_refs: tuple[str, ...]
    reviewed_by: UUID
    decision_ref: str
    created_at: datetime
    expires_at: datetime | None = None
    supersedes_version_id: UUID | None = None
    rollback_of_version_id: UUID | None = None

    @model_validator(mode="after")
    def scoped_layer(self) -> "MemoryVersion":
        if self.layer == "department" and self.department_id is None:
            raise ValueError("department_memory_requires_department")
        if self.layer != "department" and self.department_id is not None:
            raise ValueError("unexpected_department_scope")
        if self.layer == "employee" and self.employee_id is None:
            raise ValueError("employee_memory_requires_employee")
        if self.layer != "employee" and self.employee_id is not None:
            raise ValueError("unexpected_employee_scope")
        if not _is_opaque_ref(self.content_ref) or any(not _is_opaque_ref(ref) for ref in (*self.source_refs, *self.evidence_refs)):
            raise ValueError("memory_references_must_be_scoped_opaque_refs")
        if self.created_at.tzinfo is None or (self.expires_at is not None and self.expires_at.tzinfo is None):
            raise ValueError("memory_timestamps_must_be_timezone_aware")
        return self


def promote_memory(
    *, proposal: MemoryProposal, decision: PromotionDecision, current_version: int, expected_current_version: int,
    content_sha256: str, now: datetime, expected_scope: tuple[UUID, UUID],
) -> MemoryVersion | None:
    """Approve into an immutable version; reviewer authority is layer-scoped."""
    if decision.proposal_id != proposal.id:
        raise MemoryContractInvalid("proposal_decision_mismatch")
    if decision.expected_proposal_sha256 != proposal.payload_sha256:
        raise MemoryContractInvalid("proposal_payload_changed_after_review")
    if decision.outcome == "reject":
        return None
    if (proposal.environment_id, proposal.company_id) != expected_scope:
        raise MemoryContractInvalid("memory_scope_mismatch")
    if proposal.layer == "corporate" and decision.actor_role != "owner":
        raise MemoryContractInvalid("corporate_memory_requires_owner")
    if decision.actor_role == "reviewer" and not decision.reviewer_grant_ref:
        raise MemoryContractInvalid("reviewer_memory_grant_required")
    if proposal.requested_policy_change:
        raise MemoryContractInvalid("memory_cannot_change_policy")
    if proposal.expires_at is not None and proposal.expires_at <= now:
        raise MemoryContractInvalid("memory_proposal_expired")
    if now.tzinfo is None:
        raise MemoryContractInvalid("promotion_timestamp_must_be_timezone_aware")
    if type(current_version) is not int or current_version < 0:
        raise MemoryContractInvalid("invalid_current_memory_version")
    if expected_current_version != current_version:
        raise MemoryContractInvalid("stale_current_memory_version")
    if len(content_sha256) != 64 or any(char not in "0123456789abcdef" for char in content_sha256):
        raise MemoryContractInvalid("invalid_content_hash")
    return MemoryVersion(
        id=uuid4(),
        environment_id=proposal.environment_id,
        company_id=proposal.company_id,
        layer=proposal.layer,
        department_id=proposal.department_id,
        employee_id=proposal.employee_id,
        version=current_version + 1,
        title=proposal.title,
        content_ref=proposal.content_ref,
        content_sha256=content_sha256,
        source_refs=proposal.source_refs,
        evidence_refs=proposal.evidence_refs,
        reviewed_by=decision.actor_id,
        decision_ref=decision.decision_ref,
        created_at=now,
        expires_at=proposal.expires_at,
        supersedes_version_id=None,
    )


def rollback_memory(
    *, current: MemoryVersion, target: MemoryVersion, expected_current_version: int, now: datetime
) -> MemoryVersion:
    """Append a new version reusing an earlier reviewed snapshot; never mutate history."""
    if current.version != expected_current_version:
        raise MemoryContractInvalid("stale_current_memory_version")
    if now.tzinfo is None:
        raise MemoryContractInvalid("rollback_timestamp_must_be_timezone_aware")
    scope_current = (current.environment_id, current.company_id, current.layer, current.department_id, current.employee_id)
    scope_target = (target.environment_id, target.company_id, target.layer, target.department_id, target.employee_id)
    if scope_current != scope_target or target.version >= current.version:
        raise MemoryContractInvalid("rollback_target_scope_or_order_invalid")
    return MemoryVersion(
        id=uuid4(),
        environment_id=target.environment_id,
        company_id=target.company_id,
        layer=target.layer,
        department_id=target.department_id,
        employee_id=target.employee_id,
        version=current.version + 1,
        title=target.title,
        content_ref=target.content_ref,
        content_sha256=target.content_sha256,
        source_refs=target.source_refs,
        evidence_refs=target.evidence_refs,
        reviewed_by=current.reviewed_by,
        decision_ref=current.decision_ref,
        created_at=now,
        expires_at=target.expires_at,
        supersedes_version_id=current.id,
        rollback_of_version_id=target.id,
    )


def memory_is_retrievable(
    version: MemoryVersion,
    *,
    now: datetime,
    authorized_scope: tuple[UUID, UUID],
    authorized_version_ids: frozenset[UUID],
) -> bool:
    if now.tzinfo is None:
        raise MemoryContractInvalid("retrieval_timestamp_must_be_timezone_aware")
    return (
        (version.environment_id, version.company_id) == authorized_scope
        and version.id in authorized_version_ids
        and (version.expires_at is None or version.expires_at > now)
    )


def _is_opaque_ref(value: str) -> bool:
    import re

    return bool(re.fullmatch(r"[A-Za-z][A-Za-z0-9_-]{0,31}:[A-Za-z0-9][A-Za-z0-9._:-]{0,127}", value)) and ".." not in value
