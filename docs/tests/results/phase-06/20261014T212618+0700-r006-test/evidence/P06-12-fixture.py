"""Independent no-DB CSRF/limits fixture. Does not load real settings or secrets."""
from uuid import uuid4
from datetime import datetime, UTC, timedelta
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[6] / "apps" / "api" / "src"))
from starlette.requests import Request
from fastapi import HTTPException
from pydantic import ValidationError
from agent_corporation_api.modules.governance import auth
from agent_corporation_api.modules.demo.factory import DEMO_SCOPE
from agent_corporation_api.modules.execution.router import GrantInput

principal = auth.OwnerPrincipal(DEMO_SCOPE, uuid4(), "fixture-owner")
def owner(request):
    request.state.owner_csrf_hash = "fixture-valid"
    return principal
auth.require_owner = owner
auth.digest_token = lambda token: "fixture-valid" if token == "fixture-token" else "fixture-invalid"
def request(headers):
    return Request({"type": "http", "headers": [(k.encode(), v.encode()) for k,v in headers.items()]})
base = {"host": "127.0.0.1:15501", "origin": "http://127.0.0.1:15500", "x-csrf-token": "fixture-token"}
assert auth.require_owner_write(request(base)) == principal
for change in ({"x-csrf-token": ""}, {"x-csrf-token": "wrong"}, {"origin": "https://evil.example"}, {"host": "evil.example"}, {"sec-fetch-site": "cross-site"}):
    try:
        auth.require_owner_write(request({**base, **change}))
    except HTTPException as error:
        assert error.status_code == 403
    else:
        raise AssertionError("CSRF/boundary bypass")
missing_origin = {k:v for k,v in base.items() if k != "origin"}
try:
    auth.require_owner_write(request(missing_origin))
except HTTPException as error:
    assert error.status_code == 403
else:
    raise AssertionError("Missing Origin allowed")
body = dict(phase="06", batch_id="fixture", purpose="fixture", model="fixture", effort="low", max_requests=1, max_concurrency=1, timeout_seconds=1, expires_at=datetime.now(UTC)+timedelta(minutes=1))
assert GrantInput(**body).max_requests == 1
for change in ({"phase": "23"}, {"max_requests": 0}, {"max_requests": 11}, {"max_concurrency": 2}, {"timeout_seconds": 121}, {"runtime_cg01_demo_test_override": True}):
    try:
        GrantInput(**{**body, **change})
    except ValidationError:
        pass
    else:
        raise AssertionError("Grant limit/override bypass")
print("Independent fixture: CSRF/Origin/Host/cross-site denials=6; grant input boundary denials=6; happy paths=2; PASS. No DB/secrets/network.")
from contextlib import contextmanager
from types import SimpleNamespace
import asyncio
import json
from agent_corporation_api.modules.execution import service, worker, gates
from tempfile import TemporaryDirectory

spec = {**body, "grant_id":uuid4(), "idempotency_key":uuid4(), "input_text":"fixture-only"}
grant = {**body, "revoked":False, "used_requests":0, "max_requeues":0}
recorded=[]
class Result:
    def __init__(self, row): self.row=row
    def mappings(self): return self
    def first(self): return self.row
class Session:
    def execute(self, sql, values):
        text=str(sql)
        recorded.append((text,values))
        return Result(grant if text.startswith("SELECT * FROM inference_grants") else None)
@contextmanager
def transaction(*args, **kwargs): yield Session()
service.transaction=transaction
checkpoints=[]
service.checkpoint=lambda session, scope, run, boundary, data: checkpoints.append(data)
service.event=lambda *args: None
state={"allowed":True,"reason":"owner_authorized_demo_test_override","mode":"demo-test","verified":False}
service.run_create(None, DEMO_SCOPE, "fixture-owner", spec, state)
insert=[values for sql,values in recorded if sql.startswith("INSERT INTO runtime_runs")][0]
assert json.loads(insert["policy"])["cg01_at_creation"] == state
assert checkpoints[0]["policy"]["cg01_at_creation"] == state
assert json.loads(insert["policy"])["tools"] is False
print("Independent fixture: policy JSON SQL parameter and before_dispatch checkpoint retain unverified demo state; PASS. No DB persistence claimed.")
with TemporaryDirectory() as temp:
    config=SimpleNamespace(runtime_cg01_demo_test_override=True, codex_server_base_url="http://127.0.0.1:15600", codex_server_api_key=None, runtime_gate_path=Path(temp)/"missing",runtime_gateway_source_path=Path(temp)/"missing")
    worker.get_settings=lambda: config
    worker.get_session_factory=lambda: None
    service.recover_expired=lambda *args: 0
    service.reserve_next=lambda *args: {"id": uuid4()}
    dispatched=[]
    async def fake_execute(*args): dispatched.append(args)
    worker.execute_reserved=fake_execute
    asyncio.run(worker.work(DEMO_SCOPE,once=True))
    assert len(dispatched)==1
print("Independent fixture: demo worker gate reaches exactly one fake executor; PASS. No network/model call.")
