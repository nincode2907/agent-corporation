from datetime import UTC, datetime, timedelta
from types import SimpleNamespace
from uuid import uuid4

import pytest
from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient
from starlette.requests import Request

from agent_corporation_api.modules.governance import auth, auth_router
from agent_corporation_api.modules.governance.profile import ProfileWrite


def request(headers=None, cookie=None):
    values={"host":"127.0.0.1:15501", **(headers or {})}
    if cookie:
        values["cookie"]="ac_owner_session="+cookie
    return Request({"type":"http","method":"GET","scheme":"http","path":"/","headers":[(k.encode(),v.encode()) for k,v in values.items()]})

@pytest.fixture
def owner_secret(tmp_path,monkeypatch):
    path=tmp_path/"secret"
    path.write_text("a"*64+"\n")
    path.chmod(0o600)
    monkeypatch.setattr(auth,"get_settings",lambda:SimpleNamespace(owner_secret_path=path))
    return path


def test_owner_secret_default_deny_and_permission_symlink(owner_secret):
    assert auth.read_owner_secret()=="a"*64
    key=auth.cursor_signing_key()
    assert len(key)==32
    owner_secret.chmod(0o644)
    with pytest.raises(HTTPException) as error: auth.read_owner_secret()
    assert error.value.status_code==503
    owner_secret.chmod(0o600)
    link=owner_secret.parent/"link"
    owner_secret.rename(link)
    owner_secret.symlink_to(link)
    with pytest.raises(HTTPException): auth.read_owner_secret()

@pytest.mark.parametrize("headers",[{"host":"evil.test"},{"origin":"https://evil.test"},{"sec-fetch-site":"cross-site"}])
def test_host_origin_and_fetch_site_rejected(headers):
    with pytest.raises(HTTPException) as error: auth.check_boundary(request(headers))
    assert error.value.status_code==403


def test_missing_cookie_and_missing_origin_denied():
    with pytest.raises(HTTPException) as error: auth.require_owner(request())
    assert error.value.status_code==401
    with pytest.raises(HTTPException) as error: auth.require_owner_write(request())
    assert error.value.status_code==403


class Result:
    def __init__(self,row): self.row=row
    def mappings(self): return self
    def first(self): return self.row

class FakeSession:
    def __init__(self,row): self.row=row
    def __enter__(self): return self
    def __exit__(self,*args): return False
    def begin(self): return self
    def execute(self,statement,params):
        if "FROM owner_sessions" in str(statement): return Result(self.row)
        return Result({"id":self.row["company_id"]} if self.row else None)


def test_session_scope_from_store_csrf_logout_and_expiry(owner_secret,monkeypatch):
    token="cookie-token"
    csrf=auth.digest_token("csrf:"+token)
    row={"id":uuid4(),"owner_id":"owner-local","environment_id":uuid4(),"company_id":uuid4(),
        "expires_at":datetime.now(UTC)+timedelta(hours=1),"csrf_hash":auth.digest_token(csrf)}
    monkeypatch.setattr(auth,"get_session_factory",lambda:lambda:FakeSession(row))
    monkeypatch.setattr(auth,"set_company_scope",lambda *args:None)
    req=request({"origin":"http://127.0.0.1:15500","x-csrf-token":csrf},token)
    principal=auth.require_owner_write(req)
    assert principal.scope.company_id==row["company_id"]
    assert principal.session_id==row["id"]
    with pytest.raises(HTTPException) as error:
        auth.require_owner_write(request({"origin":"http://127.0.0.1:15500","x-csrf-token":"wrong"},token))
    assert error.value.status_code==403
    row["expires_at"]=datetime.now(UTC)-timedelta(seconds=1)
    with pytest.raises(HTTPException) as error: auth.require_owner(req)
    assert error.value.status_code==401
    monkeypatch.setattr(auth,"get_session_factory",lambda:lambda:FakeSession(None))
    with pytest.raises(HTTPException): auth.require_owner(req)


def test_login_failure_has_no_session_and_extra_owner_flag_rejected(owner_secret):
    app=FastAPI();app.include_router(auth_router.router)
    client=TestClient(app,base_url="http://127.0.0.1:15501")
    body={"secret":"wrong","environment_id":str(uuid4()),"company_id":str(uuid4())}
    result=client.post("/api/v1/owner/login",json=body,headers={"Origin":"http://127.0.0.1:15500"})
    assert result.status_code==401
    assert "set-cookie" not in result.headers
    body["owner"]=True
    assert client.post("/api/v1/owner/login",json=body,headers={"Origin":"http://127.0.0.1:15500"}).status_code==422


def test_profile_no_privilege_or_secret_fields_allowed():
    from pydantic import ValidationError
    with pytest.raises(ValidationError):
        ProfileWrite(model="gpt-test",reasoning_effort="low",expected_version=0,api_key="secret")
    with pytest.raises(ValidationError):
        ProfileWrite(model="arbitrary model prompt",reasoning_effort="low",expected_version=0)


def test_valid_login_uses_durable_scope_checks_cookie_and_no_secret(owner_secret,monkeypatch):
    inserted=[]
    class LoginSession(FakeSession):
        def execute(self,statement,params):
            inserted.append((str(statement),params))
            if "SELECT c.id" in str(statement): return Result({"id":params["company"]})
            return Result(None)
    monkeypatch.setattr(auth_router,"get_session_factory",lambda:lambda:LoginSession(None))
    monkeypatch.setattr(auth_router,"set_company_scope",lambda *args:None)
    monkeypatch.setattr(auth_router,"get_settings",lambda:SimpleNamespace(owner_session_ttl_seconds=3600))
    app=FastAPI();app.include_router(auth_router.router)
    client=TestClient(app,base_url="http://127.0.0.1:15501")
    environment,company=uuid4(),uuid4()
    result=client.post("/api/v1/owner/login",json={"secret":"a"*64,"environment_id":str(environment),"company_id":str(company)},headers={"Origin":"http://127.0.0.1:15500"})
    assert result.status_code==200
    assert result.json()["scope"]=={"environment_id":str(environment),"company_id":str(company)}
    cookie=result.headers["set-cookie"]
    assert "HttpOnly" in cookie and "SameSite=strict" in cookie and "Path=/api" in cookie
    assert "a"*64 not in result.text
    stored=next(params for statement,params in inserted if "INSERT INTO owner_sessions" in statement)
    assert stored["token"]!=client.cookies.get("ac_owner_session")
    assert stored["csrf"]!=result.json()["csrf_token"]


def test_owner_cannot_select_unknown_company_scope(owner_secret,monkeypatch):
    monkeypatch.setattr(auth_router,"get_session_factory",lambda:lambda:FakeSession(None))
    monkeypatch.setattr(auth_router,"set_company_scope",lambda *args:None)
    monkeypatch.setattr(auth_router,"get_settings",lambda:SimpleNamespace(owner_session_ttl_seconds=3600))
    app=FastAPI();app.include_router(auth_router.router)
    client=TestClient(app,base_url="http://127.0.0.1:15501")
    result=client.post("/api/v1/owner/login",json={"secret":"a"*64,"environment_id":str(uuid4()),"company_id":str(uuid4())},headers={"Origin":"http://127.0.0.1:15500"})
    assert result.status_code==403
    assert "set-cookie" not in result.headers
