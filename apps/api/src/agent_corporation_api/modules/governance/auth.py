"""Local Owner sessions. Identity and scope are server-controlled, never request role flags."""
from dataclasses import dataclass
from datetime import UTC, datetime
import hashlib
import hmac
import os
import stat
from uuid import UUID

from fastapi import HTTPException, Request
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from ...database import get_session_factory
from ...settings import get_settings
from ..observability.scope import CompanyScope, set_company_scope

COOKIE_NAME = "ac_owner_session"
ALLOWED_ORIGINS = frozenset({"http://127.0.0.1:15500", "http://127.0.0.1:15501", "http://localhost:15500", "http://localhost:15501", "http://agent-corporation.localhost", "https://agent-corporation.localhost"})

@dataclass(frozen=True)
class OwnerPrincipal:
    scope: CompanyScope
    session_id: UUID
    owner_id: str


def check_boundary(request: Request, *, write: bool = False) -> None:
    host = request.headers.get("host", "").lower()
    from urllib.parse import urlsplit
    allowed_hosts = {urlsplit(origin).netloc for origin in ALLOWED_ORIGINS}
    if host not in allowed_hosts:
        raise HTTPException(403, "Host local không được phép.")
    origin = request.headers.get("origin")
    if origin is not None and origin not in ALLOWED_ORIGINS:
        raise HTTPException(403, "Origin không được phép.")
    if write and origin is None:
        raise HTTPException(403, "Thao tác ghi cần Origin local.")
    if request.headers.get("sec-fetch-site") == "cross-site":
        raise HTTPException(403, "Yêu cầu cross-site bị từ chối.")


def read_owner_secret() -> str:
    path = get_settings().owner_secret_path
    try:
        if path.parent.is_symlink():
            raise ValueError("invalid secret directory")
        fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW)
        with os.fdopen(fd, "r") as stream:
            info = os.fstat(stream.fileno())
            if not stat.S_ISREG(info.st_mode) or stat.S_IMODE(info.st_mode) != 0o600 or info.st_uid != os.getuid():
                raise ValueError("invalid secret permissions")
            secret = stream.read(256).strip()
        if len(secret) < 40 or len(secret) > 128:
            raise ValueError("invalid secret")
        return secret
    except (OSError, ValueError):
        raise HTTPException(503, "Chưa bootstrap Owner local an toàn.") from None


def digest_token(token: str) -> str:
    return hmac.new(read_owner_secret().encode(), token.encode(), hashlib.sha256).hexdigest()


def require_owner(request: Request) -> OwnerPrincipal:
    check_boundary(request)
    token = request.cookies.get(COOKIE_NAME, "")
    if not token or len(token) > 128:
        raise HTTPException(401, "Cần đăng nhập Chủ tịch.")
    token_hash = digest_token(token)
    try:
        with get_session_factory()() as session, session.begin():
            row = session.execute(text("""SELECT s.id,s.owner_id,s.environment_id,s.company_id,s.expires_at,s.csrf_hash
                FROM owner_sessions s JOIN owner_scopes o ON o.owner_id=s.owner_id
                AND o.environment_id=s.environment_id AND o.company_id=s.company_id
                WHERE s.token_hash=:token AND s.revoked_at IS NULL AND s.expires_at>CURRENT_TIMESTAMP"""), {"token": token_hash}).mappings().first()
            if row is not None:
                set_company_scope(session, CompanyScope(row["environment_id"], row["company_id"]))
                known = session.execute(text("SELECT id FROM companies WHERE id=:company AND environment_id=:environment"), {"company": row["company_id"], "environment": row["environment_id"]}).first()
                if known is None:
                    row = None
    except SQLAlchemyError:
        raise HTTPException(503, "Không xác minh được session Chủ tịch.") from None
    if row is None or row["expires_at"] <= datetime.now(UTC):
        raise HTTPException(401, "Session hết hạn hoặc không còn quyền scope.")
    request.state.owner_csrf_hash = row["csrf_hash"]
    return OwnerPrincipal(CompanyScope(row["environment_id"], row["company_id"]), row["id"], row["owner_id"])


def require_owner_write(request: Request) -> OwnerPrincipal:
    check_boundary(request, write=True)
    principal = require_owner(request)
    csrf = request.headers.get("x-csrf-token", "")
    if not csrf or len(csrf) > 128 or not hmac.compare_digest(digest_token(csrf), request.state.owner_csrf_hash):
        raise HTTPException(403, "CSRF token không hợp lệ.")
    return principal


def cursor_signing_key() -> bytes:
    return hmac.new(read_owner_secret().encode(), b"event-cursor-v1", hashlib.sha256).digest()
