from __future__ import annotations

from typing import Literal
from uuid import UUID

from fastapi import APIRouter, Depends
from pydantic import BaseModel, ConfigDict, Field, field_validator

from ...database import get_session_factory
from ...settings import get_settings
from ..execution.router import invoke
from ..governance.auth import OwnerPrincipal, require_owner, require_owner_write
from . import service, worker

router = APIRouter(prefix='/api/v1/playground', tags=['development-playground'])


class SessionInput(BaseModel):
    model_config = ConfigDict(extra='forbid')
    employee_id: UUID
    profile_version: int = Field(ge=1)
    max_requests: int = Field(ge=1, le=100)
    expires_in_minutes: int = Field(ge=1, le=240)
    timeout_seconds: int = Field(default=120, ge=1, le=120)
    accept_demo_policy: Literal[True]
    idempotency_key: UUID


class MessageInput(BaseModel):
    model_config = ConfigDict(extra='forbid')
    input_text: str = Field(min_length=1, max_length=8000)
    idempotency_key: UUID

    @field_validator('input_text')
    @classmethod
    def nonempty(cls, value):
        if not value.strip():
            raise ValueError('Tin nhắn cần nội dung.')
        return value


class ResolveInput(BaseModel):
    model_config = ConfigDict(extra='forbid')
    gateway_settled: Literal[True]


def boundary(principal):
    return invoke(service.gate, get_settings(), principal.scope)


@router.get('/sessions')
def sessions(principal: OwnerPrincipal = Depends(require_owner)):
    policy = boundary(principal)
    return {'sessions': invoke(service.list_sessions, get_session_factory(), principal.scope), 'policy': policy,
            'worker': {**worker.STATE, 'enabled': get_settings().playground_worker_enabled}}


@router.post('/sessions', status_code=201)
def create(body: SessionInput, principal: OwnerPrincipal = Depends(require_owner_write)):
    boundary(principal)
    return invoke(service.create_session, get_session_factory(), principal.scope, principal, body.model_dump())


@router.get('/sessions/{ident}')
def detail(ident: UUID, principal: OwnerPrincipal = Depends(require_owner)):
    boundary(principal)
    return invoke(service.detail, get_session_factory(), principal.scope, ident)


@router.post('/sessions/{ident}/messages', status_code=201)
def send(ident: UUID, body: MessageInput, principal: OwnerPrincipal = Depends(require_owner_write)):
    boundary(principal)
    return invoke(service.send, get_session_factory(), principal.scope, ident, body.model_dump())


@router.post('/sessions/{ident}/stop')
def stop(ident: UUID, principal: OwnerPrincipal = Depends(require_owner_write)):
    boundary(principal)
    invoke(service.stop, get_session_factory(), principal.scope, ident)
    return {'stop_requested': True}


@router.post('/sessions/{ident}/revoke')
def revoke(ident: UUID, principal: OwnerPrincipal = Depends(require_owner_write)):
    boundary(principal)
    invoke(lambda: service.stop(get_session_factory(), principal.scope, ident, revoke=True))
    return {'revoked': True}


@router.post('/sessions/{ident}/unknown/{turn_id}/resolve')
def resolve(ident: UUID, turn_id: UUID, body: ResolveInput, principal: OwnerPrincipal = Depends(require_owner_write)):
    boundary(principal)
    invoke(service.resolve_unknown, get_session_factory(), principal.scope, ident, turn_id)
    return {'outcome_still_unknown': True, 'request_refunded': False}
