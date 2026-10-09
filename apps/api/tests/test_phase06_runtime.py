"""Unit transport is explicit local fake; no inference or grant on shared runtime."""
import asyncio
import json
from datetime import UTC, datetime, timedelta
from uuid import uuid4
import pytest
from agent_corporation_api.modules.execution.gateway import parse_response, post_text, CallOutcome
from agent_corporation_api.modules.execution.gates import check_gate, gateway_fingerprint, FILES
from agent_corporation_api.modules.execution.service import RuntimeDenied, validate_grant
from agent_corporation_api.modules.execution import worker, service


def fixture_grant():
    return {"phase":"06","batch_id":"fixture-batch","purpose":"unit-test","model":"fixture-model","effort":"low","expires_at":datetime.now(UTC)+timedelta(minutes=1),"revoked":False,"used_requests":0,"max_requests":1,"max_concurrency":1}

@pytest.mark.parametrize("field,value",[("phase","07"),("batch_id","other"),("purpose","other"),("model","other"),("effort","high"),("stop_requested",True)])
def test_grant_mismatch_deny(field,value):
    grant=fixture_grant()
    run={**grant,field:value}
    with pytest.raises(RuntimeDenied):
        validate_grant(grant,run,datetime.now(UTC),0)

@pytest.mark.parametrize("change",[{"revoked":True},{"used_requests":1},{"expires_at":datetime.now(UTC)-timedelta(seconds=1)}])
def test_grant_resource_deny(change):
    grant={**fixture_grant(),**change}
    with pytest.raises(RuntimeDenied):
        validate_grant(grant,grant,datetime.now(UTC),0)


def test_missing_and_concurrency_grant_deny():
    with pytest.raises(RuntimeDenied):
        validate_grant(None,{},datetime.now(UTC),0)
    grant=fixture_grant()
    with pytest.raises(RuntimeDenied):
        validate_grant(grant,grant,datetime.now(UTC),1)


def test_gate_missing_stale_world_readable_and_unverified(tmp_path):
    root=tmp_path/"gateway"
    for name in FILES:
        file=root/name
        file.parent.mkdir(parents=True,exist_ok=True)
        file.write_text("test fixture only")
    proof=tmp_path/"proof.json"
    assert check_gate(proof,root)["allowed"] is False
    data={"gateway_fingerprint":gateway_fingerprint(root),"expires_at":(datetime.now(UTC)+timedelta(minutes=1)).isoformat(),"evidence_refs":["fixture-test-only"],"isolation_verified":True,"privacy_retention_verified":True,"cancellation_verified":True}
    proof.write_text(json.dumps(data))
    proof.chmod(0o644)
    assert check_gate(proof,root)["allowed"] is False
    proof.chmod(0o600)
    assert check_gate(proof,root)["allowed"] is True
    (root/FILES[0]).write_text("changed")
    assert check_gate(proof,root)["reason"]=="fingerprint_mismatch"
    data["gateway_fingerprint"]=gateway_fingerprint(root)
    data["isolation_verified"]=False
    proof.write_text(json.dumps(data))
    assert check_gate(proof,root)["allowed"] is False


def test_usage_null_zero_and_tool_proposal_never_success():
    data={"choices":[{"message":{"content":"fixture output"}}],"usage":None}
    result=parse_response(200,{"x-codex-call-id":"fixture-call"},json.dumps(data).encode())
    assert result.status=="completed" and result.usage is None and result.gateway_call_id=="fixture-call"
    data["usage"]={"prompt_tokens":0,"completion_tokens":0,"total_tokens":0}
    assert parse_response(200,{},json.dumps(data).encode()).usage["total_tokens"]==0
    data["usage"]={"prompt_tokens":2,"completion_tokens":3,"total_tokens":6}
    assert parse_response(200,{},json.dumps(data).encode()).usage is None
    data["usage"]={"prompt_tokens":2,"completion_tokens":3,"total_tokens":5,"prompt_tokens_details":{"cached_tokens":None},"completion_tokens_details":{"reasoning_tokens":2}}
    rich=parse_response(200,{},json.dumps(data).encode()).usage
    assert rich["prompt_tokens_details"]["cached_tokens"] is None
    assert rich["completion_tokens_details"]["reasoning_tokens"]==2
    data["choices"][0]["message"]["tool_calls"]=[{"id":"outside-scope"}]
    assert parse_response(200,{},json.dumps(data).encode()).status=="unknown"
    assert parse_response(502,{},b"{}").status=="unknown"
    assert parse_response(504,{},b"{}").status=="unknown"
    assert parse_response(429,{},b"{}").status=="rate_limited"
    assert parse_response(401,{},b"{}").status=="failed"


def test_fake_http_redirect_does_not_follow_and_cancel_closes_socket():
    async def exercise():
        seen=[]
        closed=asyncio.Event()
        async def handle(reader,writer):
            raw=await reader.readuntil(b"\r\n\r\n")
            size=int([line for line in raw.split(b"\r\n") if line.lower().startswith(b"content-length:")][0].split(b":")[1])
            seen.append(json.loads(await reader.readexactly(size)))
            writer.write(b"HTTP/1.1 302 Found\r\nLocation: http://example.com/secret\r\nContent-Length: 0\r\n\r\n")
            await writer.drain()
            await reader.read()
            closed.set()
            writer.close()
            await writer.wait_closed()
        server=await asyncio.start_server(handle,"127.0.0.1",0)
        port=server.sockets[0].getsockname()[1]
        async with server:
            result=await post_text(f"http://127.0.0.1:{port}",None,{"model":"fixture","messages":[]},1)
            assert result.status=="unknown" and result.reason=="gateway_302"
            await asyncio.wait_for(closed.wait(),1)
            assert len(seen)==1
        cancelled_closed=asyncio.Event()
        async def waiting(reader,writer):
            await reader.readuntil(b"\r\n\r\n")
            await reader.read()
            cancelled_closed.set()
            writer.close()
        server=await asyncio.start_server(waiting,"127.0.0.1",0)
        port=server.sockets[0].getsockname()[1]
        async with server:
            task=asyncio.create_task(post_text(f"http://127.0.0.1:{port}",None,{},1))
            await asyncio.sleep(0.03)
            task.cancel()
            with pytest.raises(asyncio.CancelledError):
                await task
            await asyncio.wait_for(cancelled_closed.wait(),1)
    asyncio.run(exercise())


def test_worker_stop_cancels_fake_inflight_without_retry(monkeypatch):
    calls=[]
    finished=[]
    poll=[False,True]
    monkeypatch.setattr(service,"should_stop",lambda *args:poll.pop(0) if poll else True)
    monkeypatch.setattr(service,"finish",lambda factory,scope,run,result:finished.append(result))
    async def fake(*args):
        calls.append(args)
        await asyncio.sleep(5)
        return CallOutcome("completed","fixture","unreachable")
    run={"model":"fixture","effort":"low","history":[],"timeout_seconds":1}
    asyncio.run(worker.execute_reserved(None,None,run,"http://127.0.0.1:1",None,fake))
    assert len(calls)==1 and finished[0].status=="unknown"
    assert finished[0].reason=="stop_or_grant_expiry_http_closed"


def test_runtime_http_requires_owner_and_cg01_cannot_be_self_approved(monkeypatch):
    from fastapi import FastAPI
    from fastapi.testclient import TestClient
    from agent_corporation_api.modules.execution import router
    from agent_corporation_api.modules.governance.auth import OwnerPrincipal, require_owner_write
    from agent_corporation_api.modules.observability.scope import CompanyScope
    app=FastAPI()
    app.include_router(router.router)
    client=TestClient(app,base_url="http://127.0.0.1:15501")
    body={"grant_id":str(uuid4()),"phase":"06","batch_id":"fake","purpose":"fixture-test","model":"fixture-model","effort":"low","input_text":"fixture-text","idempotency_key":str(uuid4())}
    assert client.get("/api/v1/runtime/status").status_code==401
    assert client.post("/api/v1/runtime/runs",json=body,headers={"origin":"http://127.0.0.1:15500"}).status_code==401
    app.dependency_overrides[require_owner_write]=lambda:OwnerPrincipal(CompanyScope(uuid4(),uuid4()),uuid4(),"fixture-owner")
    monkeypatch.setattr(router,"gate",lambda:{"allowed":False,"reason":"fixture blocked"})
    monkeypatch.setattr(router,"get_session_factory",lambda:(_ for _ in ()).throw(AssertionError("Must deny before DB or POST")))
    assert client.post("/api/v1/runtime/runs",json=body).status_code==409
    assert client.post("/api/v1/runtime/runs",json={**body,"cg01_approved":True}).status_code==422
    assert client.post("/api/v1/runtime/runs",json={**body,"company_id":str(uuid4())}).status_code==422


@pytest.mark.parametrize("kind",["list","null","string","invalid_json","directory","fifo","symlink"])
def test_gate_malformed_and_nonregular_metadata_fails_closed(tmp_path,kind):
    import os
    root=tmp_path/"gateway"
    for name in FILES:
        file=root/name
        file.parent.mkdir(parents=True,exist_ok=True)
        file.write_text("only isolated fixture")
    proof=tmp_path/"proof"
    if kind=="directory":
        proof.mkdir()
    elif kind=="fifo":
        os.mkfifo(proof,0o600)
    elif kind=="symlink":
        target=tmp_path/"target"
        target.write_text("{}")
        target.chmod(0o600)
        proof.symlink_to(target)
    else:
        proof.write_text({"list":"[]","null":"null","string":"\"fixture\"","invalid_json":"{"}[kind])
        proof.chmod(0o600)
    started=datetime.now(UTC)
    result=check_gate(proof,root,base_url="http://127.0.0.1:1")
    assert result["allowed"] is False
    assert datetime.now(UTC)-started<timedelta(seconds=1)
    assert str(proof) not in result["reason"]


@pytest.mark.parametrize("usage",[
    {"prompt_tokens":1,"completion_tokens":1,"total_tokens":3},
    {"prompt_tokens":True,"completion_tokens":1,"total_tokens":2},
    {"prompt_tokens":1,"completion_tokens":1,"total_tokens":2,"prompt_tokens_details":{"cached_tokens":2}},
    {"prompt_tokens":1,"completion_tokens":1,"total_tokens":2,"completion_tokens_details":{"reasoning_tokens":-1}},
])
def test_late_usage_validation_rejects_guesses_inconsistent_or_out_of_bound_details(usage):
    with pytest.raises(RuntimeDenied,match="invalid_usage_correction"):
        service._validated_usage(usage)


def test_usage_flat_event_preserves_null_cache_and_reasoning_without_adding_to_total():
    usage=service._validated_usage({"prompt_tokens":2,"completion_tokens":3,"total_tokens":5,"prompt_tokens_details":{"cached_tokens":None},"completion_tokens_details":{"reasoning_tokens":2}})
    payload=service.usage_event_payload({"request_span_id":uuid4()},None,usage)
    assert payload["cached_tokens"] is None and payload["reasoning_tokens"]==2
    assert payload["input_tokens"]==2 and payload["output_tokens"]==3 and payload["total_tokens"]==5
