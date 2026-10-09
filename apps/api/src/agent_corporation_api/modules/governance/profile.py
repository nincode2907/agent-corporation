import json
from uuid import uuid4

from fastapi import HTTPException
from pydantic import BaseModel, ConfigDict, Field
from typing import Literal
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from ..observability.events import append_event, lock_event_stream
from ..observability.scope import set_company_scope
from .auth import OwnerPrincipal

class ProfileWrite(BaseModel):
    model_config = ConfigDict(extra="forbid")
    model: str = Field(min_length=1,max_length=100,pattern=r"^[A-Za-z0-9._:-]+$")
    reasoning_effort: Literal["minimal","low","medium","high","xhigh"]
    fallback_models: list[str] = Field(default_factory=list,max_length=10)
    expected_version: int = Field(ge=0)


def get_profile(factory, principal: OwnerPrincipal) -> dict:
    try:
        with factory() as session, session.begin():
            set_company_scope(session,principal.scope)
            row = session.execute(text("""SELECT version,model,reasoning_effort,fallback_models FROM owner_model_profiles
                WHERE environment_id=:env AND company_id=:company"""),
                {"env":principal.scope.environment_id,"company":principal.scope.company_id}).mappings().first()
            return dict(row) if row else {"version":0,"model":None,"reasoning_effort":None,"fallback_models":[]}
    except SQLAlchemyError:
        raise HTTPException(503,"Không đọc được profile Owner.") from None


def save_profile(factory, principal: OwnerPrincipal, body: ProfileWrite) -> dict:
    # Fallback configuration is an allowlist only; it never authorizes a call or automatic retry.
    import re
    if any(not re.fullmatch(r"[A-Za-z0-9._:-]{1,100}", model) for model in body.fallback_models) or len(set(body.fallback_models)) != len(body.fallback_models):
        raise HTTPException(422,"Fallback model không hợp lệ hoặc trùng.")
    scope = principal.scope
    params = {"env":scope.environment_id,"company":scope.company_id,"model":body.model,
        "effort":body.reasoning_effort,"fallback":json.dumps(body.fallback_models),"version":body.expected_version+1}
    try:
        with factory() as session, session.begin():
            set_company_scope(session,scope)
            lock_event_stream(session,scope)
            current = session.execute(text("SELECT version FROM owner_model_profiles WHERE environment_id=:env AND company_id=:company FOR UPDATE"),params).scalar_one_or_none() or 0
            if current != body.expected_version:
                raise HTTPException(409,"Profile đã thay đổi; tải lại phiên bản hiện tại.")
            session.execute(text("""INSERT INTO owner_model_profiles(environment_id,company_id,version,model,reasoning_effort,fallback_models)
                VALUES (:env,:company,:version,:model,:effort,CAST(:fallback AS jsonb))
                ON CONFLICT(environment_id,company_id) DO UPDATE SET version=:version,model=:model,
                reasoning_effort=:effort,fallback_models=CAST(:fallback AS jsonb),updated_at=CURRENT_TIMESTAMP"""),params)
            append_event(session,scope=scope,event_type="OWNER_MODEL_PROFILE_UPDATED",task_id=None,run_id=None,
                correlation_id=uuid4(),parent_event_id=None,source="app",actor={"kind":"owner","id":principal.owner_id},
                sensitivity="internal",payload={"version":params["version"],"model":body.model,"reasoning_effort":body.reasoning_effort,
                    "fallback_models":body.fallback_models,"tools_enabled":False,"inference_authorized":False},
                evidence_refs=[],dedup_key=f"owner-profile:{scope.company_id}:{params['version']}")
    except SQLAlchemyError:
        raise HTTPException(503,"Không lưu được profile; giao dịch đã rollback.") from None
    return {"version":params["version"],"model":body.model,"reasoning_effort":body.reasoning_effort,"fallback_models":body.fallback_models}
