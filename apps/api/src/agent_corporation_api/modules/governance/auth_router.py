from datetime import UTC, datetime, timedelta
import hmac
import secrets
from uuid import UUID, uuid4

from fastapi import APIRouter, Depends, HTTPException, Request, Response
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from ...database import get_session_factory
from ...settings import get_settings
from ..observability.scope import CompanyScope, set_company_scope
from .auth import COOKIE_NAME, OwnerPrincipal, check_boundary, digest_token, read_owner_secret, require_owner, require_owner_write
from .profile import ProfileWrite, get_profile, save_profile

router = APIRouter(prefix="/api/v1/owner", tags=["owner"])

class LoginRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    secret: str = Field(min_length=1, max_length=128, repr=False)
    environment_id: UUID
    company_id: UUID


def session_payload(request: Request, principal: OwnerPrincipal) -> dict:
    token = request.cookies.get(COOKIE_NAME, "")
    return {"authenticated": True, "owner_id": principal.owner_id, "session_id": str(principal.session_id),
        "scope": {"environment_id": str(principal.scope.environment_id), "company_id": str(principal.scope.company_id)},
        "csrf_token": digest_token("csrf:" + token)}

@router.post("/login")
def login(body: LoginRequest, request: Request, response: Response) -> dict:
    check_boundary(request, write=True)
    if not hmac.compare_digest(body.secret, read_owner_secret()):
        raise HTTPException(401, "Thông tin Owner không hợp lệ.")
    token, session_id = secrets.token_urlsafe(32), uuid4()
    ttl = max(60, min(get_settings().owner_session_ttl_seconds, 86400))
    scope = CompanyScope(body.environment_id, body.company_id)
    try:
        with get_session_factory()() as session, session.begin():
            set_company_scope(session, scope)
            known = session.execute(text("""SELECT c.id FROM companies c JOIN owner_scopes o
                ON c.id=o.company_id AND c.environment_id=o.environment_id
                WHERE o.owner_id='owner-local' AND c.id=:company AND c.environment_id=:environment"""),
                {"company": scope.company_id, "environment": scope.environment_id}).first()
            if known is None:
                raise HTTPException(403, "Owner chưa được cấp scope này.")
            # Signing-key rotation invalidates every old token, including existing sessions.
            session.execute(text("""INSERT INTO owner_sessions(id,owner_id,environment_id,company_id,token_hash,csrf_hash,expires_at)
                VALUES (:id,'owner-local',:environment,:company,:token,:csrf,:expiry)"""),
                {"id": session_id,"environment": scope.environment_id,"company": scope.company_id,
                 "token": digest_token(token),"csrf": digest_token(digest_token("csrf:" + token)),
                 "expiry": datetime.now(UTC)+timedelta(seconds=ttl)})
    except SQLAlchemyError:
        raise HTTPException(503, "Không tạo được session Owner.") from None
    response.set_cookie(COOKIE_NAME, token, max_age=ttl, httponly=True, samesite="strict", secure=request.url.scheme == "https", path="/api")
    return {"authenticated": True,"owner_id":"owner-local","session_id":str(session_id),
        "scope":{"environment_id":str(scope.environment_id),"company_id":str(scope.company_id)},
        "csrf_token":digest_token("csrf:" + token)}

@router.get("/session")
def owner_session(request: Request, principal: OwnerPrincipal = Depends(require_owner)) -> dict:
    return session_payload(request, principal)

@router.post("/logout")
def logout(response: Response, principal: OwnerPrincipal = Depends(require_owner_write)) -> dict:
    try:
        with get_session_factory()() as session, session.begin():
            session.execute(text("UPDATE owner_sessions SET revoked_at=CURRENT_TIMESTAMP WHERE id=:id"), {"id":principal.session_id})
    except SQLAlchemyError:
        raise HTTPException(503,"Không thu hồi được session.") from None
    response.delete_cookie(COOKIE_NAME,path="/api")
    return {"authenticated":False}

@router.get("/profile")
def profile(principal: OwnerPrincipal = Depends(require_owner)) -> dict:
    return get_profile(get_session_factory(),principal)

@router.put("/profile")
def update_profile(body: ProfileWrite, principal: OwnerPrincipal = Depends(require_owner_write)) -> dict:
    return save_profile(get_session_factory(),principal,body)
