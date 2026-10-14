from __future__ import annotations

from datetime import datetime
from uuid import UUID

from fastapi import APIRouter, Depends, Header, HTTPException, Query
from pydantic import BaseModel, ConfigDict, Field, field_validator
from sqlalchemy.exc import SQLAlchemyError

from ...database import get_session_factory
from .auth import OwnerPrincipal, require_owner, require_owner_write
from .approvals import (ACTION_TYPES, ApprovalConflict, ApprovalInvalid, ApprovalNotFound,
                        create_approval, decide_approval, list_approvals)

router = APIRouter(prefix="/api/v1/approvals", tags=["approvals"])


class ApprovalCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")
    task_id: UUID
    run_id: UUID | None = None
    action_type: str
    summary: str = Field(min_length=1, max_length=500)
    action_payload: dict[str, object] = Field(max_length=200)
    expires_at: datetime

    @field_validator("action_type")
    @classmethod
    def known_action(cls, value: str) -> str:
        if value not in ACTION_TYPES:
            raise ValueError("Loại hành động chưa được hỗ trợ.")
        return value


class ApprovalDecision(BaseModel):
    model_config = ConfigDict(extra="forbid")
    decision: str
    expected_payload_hash: str = Field(pattern=r"^[0-9a-f]{64}$")
    reason: str | None = Field(default=None, max_length=500)


def _raise(error: Exception):
    if isinstance(error, ApprovalNotFound):
        raise HTTPException(404, str(error)) from None
    if isinstance(error, ApprovalConflict):
        raise HTTPException(409, str(error)) from None
    if isinstance(error, (ApprovalInvalid, ValueError)):
        raise HTTPException(422, str(error)) from None


@router.get("")
def inbox(status: str | None = Query(default=None), limit: int = Query(default=100, ge=1, le=200),
          principal: OwnerPrincipal = Depends(require_owner)):
    try:
        return {"approvals": list_approvals(get_session_factory(), scope=principal.scope, status=status, limit=limit)}
    except ApprovalInvalid as error:
        _raise(error)
    except SQLAlchemyError:
        raise HTTPException(503, "Không đọc được hộp phê duyệt.") from None


@router.post("", status_code=201)
def request_review(body: ApprovalCreate, idempotency_key: UUID = Header(alias="Idempotency-Key"),
                   principal: OwnerPrincipal = Depends(require_owner_write)):
    try:
        return create_approval(get_session_factory(), scope=principal.scope, owner_id=principal.owner_id,
            task_id=body.task_id, run_id=body.run_id, action_type=body.action_type, summary=body.summary,
            action_payload=body.action_payload, expires_at=body.expires_at, idempotency_key=idempotency_key)
    except (ApprovalNotFound, ApprovalConflict, ApprovalInvalid) as error:
        _raise(error)
    except SQLAlchemyError:
        raise HTTPException(503, "Không ghi được yêu cầu phê duyệt; tải lại inbox trước khi gửi lại.") from None


@router.post("/{approval_id}/decision")
def decide(approval_id: UUID, body: ApprovalDecision, idempotency_key: UUID = Header(alias="Idempotency-Key"),
           principal: OwnerPrincipal = Depends(require_owner_write)):
    try:
        return decide_approval(get_session_factory(), scope=principal.scope, owner_id=principal.owner_id,
            approval_id=approval_id, decision=body.decision, expected_payload_hash=body.expected_payload_hash,
            idempotency_key=idempotency_key, reason=body.reason)
    except (ApprovalNotFound, ApprovalConflict, ApprovalInvalid) as error:
        _raise(error)
    except SQLAlchemyError:
        raise HTTPException(503, "Không ghi được quyết định; đối chiếu inbox trước khi thử lại.") from None
