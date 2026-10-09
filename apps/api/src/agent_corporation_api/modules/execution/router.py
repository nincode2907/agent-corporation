from __future__ import annotations
from datetime import UTC, datetime
from typing import Literal
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, ConfigDict, Field, field_validator
from ...database import get_session_factory
from ...settings import get_settings
from ..governance.auth import OwnerPrincipal, require_owner, require_owner_write
from .gates import check_gate
from . import service

router=APIRouter(prefix="/api/v1/runtime",tags=["runtime"])
Effort=Literal["minimal","low","medium","high","xhigh","max","ultra","persistent"]

class GrantInput(BaseModel):
    model_config=ConfigDict(extra="forbid")
    phase:Literal["06","07"]
    batch_id:str=Field(min_length=1,max_length=120)
    purpose:str=Field(min_length=1,max_length=240)
    model:str=Field(min_length=1,max_length=128)
    effort:Effort
    max_requests:int=Field(ge=1,le=10)
    max_concurrency:int=Field(ge=1,le=1)
    timeout_seconds:int=Field(ge=1,le=120)
    max_requeues:int=Field(default=0,ge=0,le=2)
    expires_at:datetime
    @field_validator("expires_at")
    @classmethod
    def timezone_required(cls,value):
        if value.tzinfo is None:
            raise ValueError("Expiry cần timezone")
        return value

class RunInput(BaseModel):
    model_config=ConfigDict(extra="forbid")
    grant_id:UUID
    phase:Literal["06","07"]
    batch_id:str=Field(min_length=1,max_length=120)
    purpose:str=Field(min_length=1,max_length=240)
    model:str=Field(min_length=1,max_length=128)
    effort:Effort
    input_text:str=Field(min_length=1,max_length=16000)
    idempotency_key:UUID


def gate():
    settings=get_settings()
    return check_gate(settings.runtime_gate_path,settings.runtime_gateway_source_path,base_url=settings.codex_server_base_url)


def invoke(call,*args):
    try:
        return call(*args)
    except service.RuntimeDenied as error:
        raise HTTPException(status_code=404 if str(error).endswith("not_found") else 409,detail=str(error)) from None

@router.get("/status")
def runtime_status(principal:OwnerPrincipal=Depends(require_owner)):
    grants=service.grants_list(get_session_factory(),principal.scope)
    return {"cg01":gate(),"inference_grants":len([g for g in grants if not g["revoked"] and g["expires_at"] > datetime.now(UTC) and g["used_requests"] < g["max_requests"]]),"limits":{"max_turns":1,"tools":False,"cost_basis":"unknown"},"runs":service.runs_list(get_session_factory(),principal.scope)}

@router.get("/grants")
def grants(principal:OwnerPrincipal=Depends(require_owner)):
    return {"grants":service.grants_list(get_session_factory(),principal.scope)}

@router.post("/grants",status_code=201)
def grant_create(body:GrantInput,principal:OwnerPrincipal=Depends(require_owner_write)):
    # Explicitly creating a grant never changes CG01; current user test grant stays zero.
    return invoke(service.grant_create,get_session_factory(),principal.scope,principal.owner_id,body.model_dump())

@router.post("/grants/{grant_id}/revoke")
def revoke(grant_id:UUID,principal:OwnerPrincipal=Depends(require_owner_write)):
    invoke(service.revoke_grant,get_session_factory(),principal.scope,grant_id)
    return {"revoked":True}

@router.post("/runs",status_code=201)
def run_create(body:RunInput,principal:OwnerPrincipal=Depends(require_owner_write)):
    if not gate()["allowed"]:
        raise HTTPException(409,"CG01 chưa có bằng chứng capability/isolation/privacy/cancellation hợp lệ; chưa dispatch.")
    run_id=invoke(service.run_create,get_session_factory(),principal.scope,principal.owner_id,body.model_dump())
    return invoke(service.run_get,get_session_factory(),principal.scope,run_id)

@router.get("/runs/{run_id}")
def run_get(run_id:UUID,principal:OwnerPrincipal=Depends(require_owner)):
    return invoke(service.run_get,get_session_factory(),principal.scope,run_id)

@router.post("/runs/{run_id}/stop")
def run_stop(run_id:UUID,principal:OwnerPrincipal=Depends(require_owner_write)):
    invoke(service.run_stop,get_session_factory(),principal.scope,run_id)
    return invoke(service.run_get,get_session_factory(),principal.scope,run_id)
