from __future__ import annotations
from datetime import UTC, datetime
from typing import Literal
from uuid import UUID

from fastapi import APIRouter, Depends, Header, HTTPException, Query
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator
from sqlalchemy.exc import SQLAlchemyError

from ...database import get_session_factory
from ..governance.auth import OwnerPrincipal, require_owner, require_owner_write
from ..observability.scope import CompanyScope
from .commands import CompanyScopeNotFound, InvalidTaskTransition, StaleTaskState, create_work_order
from .queue import IdempotencyConflict, list_assignees, list_work_orders, task_action

router = APIRouter(prefix="/api/v1/work-orders", tags=["work-orders"])
TaskStatus = Literal["draft","queued","planning","awaiting_approval","executing","reviewing","rework","awaiting_acceptance","accepted","blocked","paused","failed","cancelled"]

class AcceptanceCriterion(BaseModel):
    model_config = ConfigDict(extra="forbid")
    id: str = Field(min_length=1,max_length=64)
    description: str = Field(min_length=1,max_length=500)
    evidence_kind: str = Field(min_length=1,max_length=100)

class WorkOrderScope(BaseModel):
    model_config = ConfigDict(extra="forbid")
    input_refs: list[str] = Field(min_length=1,max_length=50)
    tool_capabilities: list[str] = Field(default_factory=list, max_length=0)

    @field_validator("input_refs")
    @classmethod
    def references_are_not_paths(cls, values):
        for value in values:
            if not value.strip() or value.startswith(("/", "\\")) or ".." in value or "\\" in value:
                raise ValueError("Scope chỉ nhận reference đã cấp, không phải đường dẫn máy")
        return values

class WorkOrderBudget(BaseModel):
    model_config = ConfigDict(extra="forbid")
    max_model_requests: Literal[0] = 0
    cost_basis: Literal["unknown"] = "unknown"
    usd_limit_micros: None = None

class WorkOrderStops(BaseModel):
    model_config = ConfigDict(extra="forbid")
    max_duration_seconds: int = Field(ge=1,le=86400)
    max_rework_rounds: int = Field(ge=0,le=5)

class WorkOrderInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    goal: str = Field(min_length=1,max_length=8000)
    expected_outputs: list[str] = Field(min_length=1,max_length=20)
    acceptance_criteria: list[AcceptanceCriterion] = Field(min_length=1,max_length=30)
    scope: WorkOrderScope
    deadline_at: datetime | None = None
    budget_limits: WorkOrderBudget = Field(default_factory=WorkOrderBudget)
    stop_conditions: WorkOrderStops
    assignee_id: UUID | None = None
    reviewer_id: UUID | None = None
    autonomy: Literal["strict","supervised","delegated"] = "strict"

    @field_validator("goal")
    @classmethod
    def goal_not_blank(cls, value):
        if not value.strip(): raise ValueError("goal không được để trống")
        return value

    @field_validator("expected_outputs")
    @classmethod
    def outputs_are_not_blank(cls, values):
        if any(not value.strip() for value in values): raise ValueError("expected_outputs không được rỗng")
        return values

    @field_validator("deadline_at")
    @classmethod
    def deadline_is_timezone_aware(cls,value):
        if value is not None and value.tzinfo is None: raise ValueError("deadline_at cần timezone")
        return value

    @model_validator(mode="after")
    def deadline_is_future(self):
        if self.deadline_at is not None and self.deadline_at <= datetime.now(self.deadline_at.tzinfo):
            raise ValueError("deadline_at phải ở tương lai")
        return self


class TaskAction(BaseModel):
    model_config = ConfigDict(extra="forbid")
    action: Literal["enqueue","pause","resume","cancel","accept","request_rework"]
    expected_version: int = Field(ge=1)
    priority: int = Field(default=0,ge=-100,le=100)
    reason: str | None = Field(default=None,max_length=500)


def _map_error(error: Exception):
    if isinstance(error, CompanyScopeNotFound): raise HTTPException(404,"Work Order không tồn tại trong scope Owner.") from None
    if isinstance(error, (InvalidTaskTransition,StaleTaskState,IdempotencyConflict)): raise HTTPException(409,str(error)) from None
    if isinstance(error, ValueError): raise HTTPException(422,str(error)) from None

@router.get("")
def board(status: TaskStatus | None = None, assignee_id: UUID | None = None,
          query: str | None = Query(default=None,max_length=120), limit: int = Query(100,ge=1,le=200),
          principal: OwnerPrincipal = Depends(require_owner)):
    try:
        factory=get_session_factory()
        return {"tasks":list_work_orders(factory,scope=principal.scope,status=status,
            assignee_id=assignee_id,query=query,limit=limit),"assignees":list_assignees(factory,scope=principal.scope)}
    except SQLAlchemyError:
        raise HTTPException(503,"Không đọc được bảng Work Order.") from None

@router.post("",status_code=201)
def create(body: WorkOrderInput, idempotency_key: UUID = Header(alias="Idempotency-Key"),
           principal: OwnerPrincipal = Depends(require_owner_write)):
    try:
        result=create_work_order(get_session_factory(),scope=principal.scope,
            payload={**body.model_dump(mode="python"),"created_by":{"kind":"owner","id":principal.owner_id}},
            dedup_key=f"work:create:{idempotency_key}")
        return {"task_id":str(result.work_order_id),"revision":result.revision,
                "event_id":str(result.event_id),"stream_seq":result.stream_seq,"duplicate":result.duplicate}
    except (CompanyScopeNotFound,InvalidTaskTransition,StaleTaskState,ValueError) as error:
        _map_error(error)
    except SQLAlchemyError:
        raise HTTPException(503,"Không tạo được Work Order; tải lại bảng trước khi thử lại.") from None

@router.post("/{task_id}/actions")
def action(task_id: UUID, body: TaskAction, idempotency_key: UUID = Header(alias="Idempotency-Key"),
           principal: OwnerPrincipal = Depends(require_owner_write)):
    try:
        return task_action(get_session_factory(),scope=principal.scope,task_id=task_id,owner_id=principal.owner_id,
            action=body.action,expected_version=body.expected_version,idempotency_key=idempotency_key,
            priority=body.priority,reason=body.reason)
    except (CompanyScopeNotFound,InvalidTaskTransition,StaleTaskState,IdempotencyConflict,ValueError) as error:
        _map_error(error)
    except SQLAlchemyError:
        raise HTTPException(503,"Không cập nhật được Work Order; tải lại trạng thái trước khi thử lại.") from None
