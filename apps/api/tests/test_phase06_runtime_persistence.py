"""Opt-in PG fixture only; requires disposable database/migrations prepared by runner."""
import os
import json
import select
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import UTC, datetime, timedelta
from pathlib import Path
from uuid import uuid4
import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.exc import DBAPIError
from sqlalchemy.orm import sessionmaker
from agent_corporation_api.settings import get_settings
from agent_corporation_api.modules.observability.scope import CompanyScope, set_company_scope
from agent_corporation_api.modules.execution import service
from agent_corporation_api.modules.execution.gateway import CallOutcome, parse_response

pytestmark=pytest.mark.skipif(os.getenv("PHASE_RUNTIME_TEST_ISOLATED")!="1",reason="Requires opt-in isolated PostgreSQL; never mutates shared DB")

@pytest.fixture
def runtime_db():
    settings=get_settings()
    app=create_engine(settings.database_url)
    admin=create_engine(settings.migration_database_url)
    factory=sessionmaker(app,expire_on_commit=False)
    scope=CompanyScope(uuid4(),uuid4())
    with admin.begin() as con:
        con.execute(text("INSERT INTO environments(id,name,kind,release_locked) VALUES(:id,:name,'demo',true)"),{"id":scope.environment_id,"name":f"runtime-fixture-{scope.environment_id}"})
        con.execute(text("INSERT INTO companies(id,environment_id,name) VALUES(:id,:env,'fixture runtime')"),{"id":scope.company_id,"env":scope.environment_id})
        employee,version=uuid4(),uuid4()
        con.execute(text("INSERT INTO employees(id,environment_id,company_id,lifecycle) VALUES(:id,:env,:company,'active')"),{"id":employee,"env":scope.environment_id,"company":scope.company_id})
        con.execute(text("INSERT INTO employee_versions(id,environment_id,company_id,employee_id,version,profile) VALUES(:id,:env,:company,:employee,1,'{\"display_name\":\"Fixture employee\",\"role\":\"Analyst\"}')"),{"id":version,"env":scope.environment_id,"company":scope.company_id,"employee":employee})
    yield factory,scope,admin
    with admin.begin() as con:
        con.execute(text("UPDATE runtime_dispatch_guard SET request_span_id=NULL,environment_id=NULL,company_id=NULL WHERE environment_id=:env"),{"env":scope.environment_id})
        for table in ("runtime_reconciliation_decisions","runtime_usage_corrections","model_calls","runtime_runs","inference_grants","outbox_events","events","artifacts","checkpoints","run_execution_state","runs","task_execution_state","task_revisions","work_orders","event_stream_counters","owner_model_profiles","employee_versions","employees","companies"):
            con.execute(text(f"DELETE FROM {table} WHERE environment_id=:env"),{"env":scope.environment_id})
        con.execute(text("DELETE FROM environments WHERE id=:env"),{"env":scope.environment_id})
    app.dispose()
    admin.dispose()


def grant_spec(requests=1,requeues=0):
    return {"phase":"06","batch_id":"fake-runtime-pg","purpose":"isolated-fixture-only","model":"fixture-model","effort":"low","max_requests":requests,"max_concurrency":1,"timeout_seconds":1,"max_requeues":requeues,"expires_at":datetime.now(UTC)+timedelta(minutes=1)}


def create(factory,scope,grant,**overrides):
    spec={key:grant[key] for key in ("phase","batch_id","purpose","model","effort")}
    with factory() as ses,ses.begin():
        set_company_scope(ses,scope)
        employee=ses.execute(text("SELECT e.id AS employee_id,v.id AS employee_version_id FROM employees e JOIN employee_versions v ON v.environment_id=e.environment_id AND v.company_id=e.company_id AND v.employee_id=e.id WHERE e.environment_id=:env AND e.company_id=:company ORDER BY e.id LIMIT 1"),{"env":scope.environment_id,"company":scope.company_id}).mappings().one()
    return service.run_create(factory,scope,"fixture-owner",{**spec,**employee,"grant_id":grant["id"],"input_text":"Văn bản fixture tin cậy, không đọc file.","idempotency_key":uuid4(),**overrides},synthetic_test_data=True)


def rows(factory,scope,query,**values):
    with factory() as ses,ses.begin():
        set_company_scope(ses,scope)
        return ses.execute(text(query),values).mappings().all()


def test_atomic_grant_race_complete_artifact_snapshot_and_scope(runtime_db):
    factory,scope,admin=runtime_db
    grant=service.grant_create(factory,scope,"fixture-owner",grant_spec())
    with admin.begin() as con:
        con.execute(text("INSERT INTO owner_model_profiles(environment_id,company_id,version,model,reasoning_effort,fallback_models) VALUES(:env,:company,7,'other-profile-model','medium','[\"allowlisted-other-model\"]')"),{"env":scope.environment_id,"company":scope.company_id})
    key=uuid4()
    run_id=create(factory,scope,grant,idempotency_key=key)
    assert create(factory,scope,grant,idempotency_key=key)==run_id
    with pytest.raises(service.RuntimeDenied,match="idempotency_payload_mismatch"):
        create(factory,scope,grant,idempotency_key=key,input_text="other")
    with ThreadPoolExecutor(max_workers=4) as pool:
        attempts=list(pool.map(lambda _:service.reserve_next(factory,scope),range(4)))
    reserved=[call for call in attempts if call]
    assert len(reserved)==1
    assert service.grants_list(factory,scope)[0]["used_requests"]==1
    service.finish(factory,scope,reserved[0],CallOutcome("completed","final_response","Fixture artifact","FiXtUrE-CaLl",{"prompt_tokens":2,"completion_tokens":3,"total_tokens":5}))
    result=service.run_get(factory,scope,run_id)
    assert result["status"]=="completed" and result["gateway_call_id"]=="FiXtUrE-CaLl" and result["artifact_id"]
    assert result["usage"]["total_tokens"]==5
    task=rows(factory,scope,"SELECT status,transition_version FROM task_execution_state WHERE task_id=:id",id=result["task_id"])[0]
    assert task["status"]=="reviewing" and task["transition_version"]==4
    assert len(rows(factory,scope,"SELECT * FROM events WHERE task_id=:id AND event_type='TASK_STARTED'",id=result["task_id"]))==1
    assert rows(factory,scope,"SELECT payload FROM events WHERE task_id=:id AND event_type='TASK_STATE_CHANGED' ORDER BY stream_seq",id=result["task_id"])[-1]["payload"]["to"]=="reviewing"
    assert len(rows(factory,scope,"SELECT * FROM checkpoints WHERE run_id=:id",id=run_id))==3
    snapshot=rows(factory,scope,"SELECT profile_snapshot FROM runs WHERE id=:id",id=run_id)[0]["profile_snapshot"]
    assert snapshot["tools"] is False and snapshot["owner_profile"]["version"]==7
    assert snapshot["model"]=="fixture-model" and snapshot["effective_source"]=="explicit_owner_grant"
    assert service.runs_list(factory,CompanyScope(scope.environment_id,uuid4()))==[]
    with factory() as ses,ses.begin():
        assert ses.execute(text("SELECT count(*) FROM runtime_runs")).scalar_one()==0
    with pytest.raises(service.RuntimeDenied,match="request_limit"):
        create(factory,scope,grant)


def test_missing_wrong_grant_stop_and_revocation_before_dispatch(runtime_db):
    factory,scope,_=runtime_db
    grant=service.grant_create(factory,scope,"fixture-owner",grant_spec())
    with pytest.raises(service.RuntimeDenied):
        create(factory,scope,grant,grant_id=uuid4())
    with pytest.raises(service.RuntimeDenied,match="scope_mismatch"):
        create(factory,scope,grant,batch_id="different")
    stopped=create(factory,scope,grant)
    service.run_stop(factory,scope,stopped)
    service.run_stop(factory,scope,stopped)
    assert service.run_get(factory,scope,stopped)["status"]=="cancelled"
    assert service.reconciliation_get(factory,scope,stopped)["classification"]=="confirmed_cancellation"
    stopped_task=service.run_get(factory,scope,stopped)["task_id"]
    assert rows(factory,scope,"SELECT status FROM task_execution_state WHERE task_id=:id",id=stopped_task)[0]["status"]=="cancelled"
    assert service.reserve_next(factory,scope) is None
    waiting=create(factory,scope,grant)
    service.revoke_grant(factory,scope,grant["id"])
    assert service.run_get(factory,scope,waiting)["status"]=="cancelled"
    assert service.reserve_next(factory,scope) is None
    assert rows(factory,scope,"SELECT * FROM model_calls")==[]


def test_unknown_reconciliation_is_owner_audited_idempotent_and_keeps_guard(runtime_db):
    factory,scope,_=runtime_db
    grant=service.grant_create(factory,scope,"fixture-owner",grant_spec())
    run_id=create(factory,scope,grant)
    reserved=service.reserve_next(factory,scope)
    assert reserved and reserved["id"]==run_id
    gateway_id=str(uuid4())
    service.finish(factory,scope,reserved,CallOutcome("unknown","transport_interrupted",gateway_call_id=gateway_id))
    before=service.reconciliation_get(factory,scope,run_id)
    assert before["classification"]=="unresolved"
    assert before["gateway_call_id"]==gateway_id
    assert before["dispatch_guard"]["held_for_this_call"] is True
    assert before["usage_status"]=="unknown" and before["cost_status"]=="unknown"
    assert before["available_actions"]==["record_unresolved_keep_guard"]
    assert all("history" not in checkpoint for checkpoint in before["checkpoints"])

    key=uuid4()
    action=lambda:service.record_unresolved_reconciliation(factory,scope,run_id,"fixture-owner",key,"Gateway outcome cannot be proven.")
    with ThreadPoolExecutor(max_workers=2) as pool:
        decisions=list(pool.map(lambda _:action(),range(2)))
    assert decisions[0]["id"]==decisions[1]["id"]
    assert sorted(item["idempotent_replay"] for item in decisions)==[False,True]
    assert decisions[0]["guard_released"] is False
    with pytest.raises(service.RuntimeDenied,match="idempotency_payload_mismatch"):
        service.record_unresolved_reconciliation(factory,scope,run_id,"fixture-owner",key,"different assertion")
    after=service.reconciliation_get(factory,scope,run_id)
    assert after["dispatch_guard"]["held_for_this_call"] is True
    assert after["classification"]=="unresolved" and after["usage_status"]=="unknown"
    assert len(after["decisions"])==1
    assert any(event["event_type"]=="RUNTIME_RECONCILIATION_RECORDED" for event in after["evidence"])

    late_usage={"prompt_tokens":2,"completion_tokens":3,"total_tokens":5}
    service.finish(factory,scope,reserved,CallOutcome("completed","late_final_response","late text must not replace outcome",gateway_id,late_usage))
    late=service.reconciliation_get(factory,scope,run_id)
    run=service.run_get(factory,scope,run_id)
    stored_call=rows(factory,scope,"SELECT status,usage FROM model_calls WHERE run_id=:id",id=run_id)[0]
    correction=rows(factory,scope,"SELECT gateway_call_id,usage FROM runtime_usage_corrections WHERE request_span_id=:id",id=reserved["request_span_id"])
    assert run["status"]=="interrupted" and run["outcome"]=="transport_interrupted" and run["output"] is None
    assert stored_call["status"]=="unknown" and stored_call["usage"] is None
    assert correction and str(correction[0]["gateway_call_id"])==gateway_id and correction[0]["usage"]==late_usage
    assert late["classification"]=="unresolved" and late["usage_status"]=="confirmed" and late["usage"]["total_tokens"]==5
    assert late["dispatch_guard"]["held_for_this_call"] is True and len(late["decisions"])==1
    assert any(event["event_type"]=="TOKEN_USAGE_RECORDED" for event in late["evidence"])
    assert service.reserve_next(factory,scope) is None
    decision_id=late["decisions"][0]["id"]
    with pytest.raises(DBAPIError):
        with factory() as ses,ses.begin():
            set_company_scope(ses,scope)
            ses.execute(text("UPDATE runtime_reconciliation_decisions SET reason='rewritten' WHERE id=:id"),{"id":decision_id})


def test_employee_assignment_is_scoped_current_and_immutable(runtime_db):
    factory,scope,admin=runtime_db
    grant=service.grant_create(factory,scope,"fixture-owner",grant_spec(3))
    run_id=create(factory,scope,grant)
    run=service.run_get(factory,scope,run_id)
    assert run["employee"]["id"] and run["employee"]["version"]==1
    snapshot=rows(factory,scope,"SELECT employee_version_id,profile_snapshot FROM runs WHERE id=:id",id=run_id)[0]
    original_version=snapshot["employee_version_id"]
    assert str(original_version)==run["employee"]["version_id"]
    foreign_company,foreign_employee,foreign_version=uuid4(),uuid4(),uuid4()
    with admin.begin() as con:
        con.execute(text("INSERT INTO companies(id,environment_id,name) VALUES(:company,:env,'foreign employee company')"),{"company":foreign_company,"env":scope.environment_id})
        con.execute(text("INSERT INTO employees(id,environment_id,company_id,lifecycle) VALUES(:employee,:env,:company,'active')"),{"employee":foreign_employee,"env":scope.environment_id,"company":foreign_company})
        con.execute(text("INSERT INTO employee_versions(id,environment_id,company_id,employee_id,version,profile) VALUES(:version,:env,:company,:employee,1,'{\"display_name\":\"Foreign fixture\",\"role\":\"Analyst\"}')"),{"version":foreign_version,"env":scope.environment_id,"company":foreign_company,"employee":foreign_employee})
    with pytest.raises(service.RuntimeDenied,match="employee_not_found_stale_or_not_assignable"):
        create(factory,scope,grant,employee_id=foreign_employee,employee_version_id=foreign_version)
    event_rows=rows(factory,scope,"SELECT run_id,task_id,agent_id,employee_version_id FROM events WHERE run_id=:id",id=run_id)
    assert event_rows and all(str(row["run_id"])==str(run_id) and str(row["task_id"])==run["task_id"] for row in event_rows)
    assert all(str(row["agent_id"])==run["employee"]["id"] and row["employee_version_id"]==original_version for row in event_rows)
    employee=rows(factory,scope,"SELECT employee_id FROM employee_versions WHERE id=:id",id=original_version)[0]["employee_id"]
    # A newer version never rewrites a historical Run; stale and offboarded versions cannot be assigned.
    with admin.begin() as con:
        con.execute(text("INSERT INTO employee_versions(id,environment_id,company_id,employee_id,version,profile) VALUES(:id,:env,:company,:employee,2,'{\"display_name\":\"Renamed\",\"role\":\"Lead\"}')"),{"id":uuid4(),"env":scope.environment_id,"company":scope.company_id,"employee":employee})
    assert service.run_get(factory,scope,run_id)["employee"]["version_id"]==str(original_version)
    current=service.demo_employees(factory,scope)[0]
    with pytest.raises(service.RuntimeDenied,match="employee_not_found_stale_or_not_assignable"):
        create(factory,scope,grant,employee_id=current["employee_id"],employee_version_id=original_version)
    with admin.begin() as con:
        con.execute(text("UPDATE employees SET lifecycle='offboarded' WHERE id=:id"),{"id":employee})
    with pytest.raises(service.RuntimeDenied,match="employee_not_found_stale_or_not_assignable"):
        create(factory,scope,grant)


def test_supervised_fake_worker_waits_completes_and_correlates_one_employee_run(runtime_db):
    import asyncio
    from agent_corporation_api.modules.execution import worker

    factory,scope,_=runtime_db
    grant=service.grant_create(factory,scope,"fixture-owner",grant_spec())
    run_id=create(factory,scope,grant)
    entered=asyncio.Event()
    release=asyncio.Event()
    stop=asyncio.Event()
    calls=[]
    proof={"allowed":True,"mode":"strict","verified":True,"reason":"synthetic fixture gate"}

    async def fake_transport(_base,_key,payload,_timeout):
        calls.append(payload)
        entered.set()
        await release.wait()
        return CallOutcome("completed","final_response","Synthetic report",str(uuid4()),{"prompt_tokens":2,"completion_tokens":3,"total_tokens":5})

    async def exercise():
        task=asyncio.create_task(worker.supervise(scope,stop_event=stop,transport=fake_transport,
            gate_check=lambda _settings,_scope:proof,factory=factory,poll_interval=0.01))
        await asyncio.wait_for(entered.wait(),timeout=5)
        pending=await asyncio.to_thread(service.run_get,factory,scope,run_id)
        assert pending["status"]=="waiting_model"
        assert pending["employee"]["id"]
        release.set()
        deadline=asyncio.get_running_loop().time()+5
        while asyncio.get_running_loop().time()<deadline:
            current=await asyncio.to_thread(service.run_get,factory,scope,run_id)
            if current["status"]=="completed":
                break
            await asyncio.sleep(0.01)
        assert current["status"]=="completed"
        stop.set()
        assert await asyncio.wait_for(task,timeout=5) is True
        return current

    result=asyncio.run(exercise())
    assert len(calls)==1 and calls[0]["tools"]==[] and calls[0]["tool_choice"]=="none"
    assert result["employee"]["name"] in calls[0]["messages"][0]["content"]
    assert result["employee"]["role"] in calls[0]["messages"][0]["content"]
    assert result["output"]=="Synthetic report" and result["usage"]["total_tokens"]==5
    assert result["usage_provenance"]=="gateway_final_response" and result["cost_basis"]=="unknown"
    correlated=rows(factory,scope,"SELECT run_id,task_id,agent_id,employee_version_id FROM events WHERE run_id=:id ORDER BY stream_seq",id=run_id)
    assert correlated and all(str(row["run_id"])==str(run_id) and str(row["task_id"])==result["task_id"] for row in correlated)
    assert all(str(row["agent_id"])==result["employee"]["id"] and str(row["employee_version_id"])==result["employee"]["version_id"] for row in correlated)
    evidence_path=os.getenv("INTEGRATION05_EVIDENCE_PATH")
    if evidence_path:
        event_detail=rows(factory,scope,"SELECT event_id,event_type,stream_seq,run_id,task_id,agent_id,employee_version_id FROM events WHERE run_id=:id ORDER BY stream_seq",id=run_id)
        Path(evidence_path).write_text(json.dumps({
            "classification":"synthetic_test_data","database":"unique disposable PostgreSQL database/role",
            "transport":"injected deterministic fake coroutine; no network or model inference",
            "supervised_worker":"PostgreSQL advisory-lock supervise loop","fake_transport_entries":len(calls),
            "run_id":run_id,"task_id":result["task_id"],"employee":result["employee"],
            "run_status":result["status"],"output":result["output"],"usage":result["usage"],
            "usage_provenance":result["usage_provenance"],"cost_basis":result["cost_basis"],
            "events":[{**row,"event_id":str(row["event_id"]),"run_id":str(row["run_id"]),
                "task_id":str(row["task_id"]),"agent_id":str(row["agent_id"]),
                "employee_version_id":str(row["employee_version_id"])} for row in event_detail],
            "identity_correlation_verified":True
        },ensure_ascii=False,indent=2,default=str)+"\n",encoding="utf-8")


def test_supervised_worker_cg01_denial_keeps_run_queued(runtime_db):
    import asyncio
    from agent_corporation_api.modules.execution import worker

    factory,scope,_=runtime_db
    grant=service.grant_create(factory,scope,"fixture-owner",grant_spec())
    run_id=create(factory,scope,grant)
    denied={"allowed":False,"mode":"strict","verified":False,"reason":"fixture_denied"}
    stop=asyncio.Event()
    calls=[]
    async def fake_transport(*_args): calls.append(True)
    async def exercise():
        task=asyncio.create_task(worker.supervise(scope,stop_event=stop,transport=fake_transport,
            gate_check=lambda _settings,_scope:denied,factory=factory,poll_interval=0.01))
        await asyncio.sleep(0.05)
        stop.set()
        assert await asyncio.wait_for(task,timeout=2) is True
    asyncio.run(exercise())
    assert calls==[] and service.run_get(factory,scope,run_id)["status"]=="queued"
    assert rows(factory,scope,"SELECT * FROM model_calls WHERE run_id=:id",id=run_id)==[]


def test_supervised_worker_advisory_lock_contender_release_and_reacquire(runtime_db):
    import asyncio
    from agent_corporation_api.modules.execution import worker

    factory,scope,_=runtime_db
    entered=asyncio.Event()
    denied={"allowed":False,"mode":"strict","verified":False,"reason":"fixture_denied"}
    def gate(*_args):
        entered.set()
        return denied

    async def exercise():
        stop=asyncio.Event()
        active=asyncio.create_task(worker.supervise(scope,stop_event=stop,gate_check=gate,
            factory=factory,poll_interval=0.01))
        await asyncio.wait_for(entered.wait(),timeout=2)
        assert await worker.supervise(scope,stop_event=asyncio.Event(),gate_check=gate,
            factory=factory,poll_interval=0.01) is False
        stop.set()
        assert await asyncio.wait_for(active,timeout=2) is True
        # A pre-set stop event acquires then immediately releases without dispatch.
        already_stopped=asyncio.Event()
        already_stopped.set()
        assert await worker.supervise(scope,stop_event=already_stopped,gate_check=gate,
            factory=factory,poll_interval=0.01) is True

    asyncio.run(exercise())


def test_worker_shutdown_before_http_is_known_failure_and_releases_dispatch_guard(runtime_db):
    import asyncio
    from agent_corporation_api.modules.execution import worker

    factory,scope,_=runtime_db
    grant=service.grant_create(factory,scope,"fixture-owner",grant_spec())
    run_id=create(factory,scope,grant)
    reserved=service.reserve_next(factory,scope)
    stop=asyncio.Event()
    stop.set()
    calls=[]
    async def fake_transport(*_args): calls.append(True)
    asyncio.run(worker.execute_reserved(factory,scope,reserved,"http://fake.invalid",None,fake_transport,stop))
    assert calls==[]
    assert rows(factory,scope,"SELECT status,reason FROM model_calls WHERE run_id=:id",id=run_id)[0]["status"]=="failed"
    assert service.run_get(factory,scope,run_id)["status"]=="failed"
    assert rows(factory,scope,"SELECT request_span_id FROM runtime_dispatch_guard WHERE id=1")[0]["request_span_id"] is None


def test_crash_recovery_is_fenced_unknown_and_no_replay(runtime_db):
    factory,scope,admin=runtime_db
    grant=service.grant_create(factory,scope,"fixture-owner",grant_spec(2))
    run_id=create(factory,scope,grant)
    reserved=service.reserve_next(factory,scope)
    with admin.begin() as con:
        con.execute(text("UPDATE model_calls SET lease_until=CURRENT_TIMESTAMP-interval '1 second' WHERE id=:id"),{"id":reserved["request_span_id"]})
    assert service.recover_expired(factory,scope)==1
    assert service.recover_expired(factory,scope)==0
    assert service.run_get(factory,scope,run_id)["status"]=="interrupted"
    assert rows(factory,scope,"SELECT status FROM task_execution_state WHERE task_id=:id",id=reserved["task_id"])[0]["status"]=="blocked"
    service.finish(factory,scope,reserved,CallOutcome("completed","late_stale_response","must not overwrite unknown"))
    assert service.run_get(factory,scope,run_id)["output"] is None
    # A new grant must not bypass the unknown in-flight call from the first grant.
    second=service.grant_create(factory,scope,"fixture-owner",grant_spec())
    create(factory,scope,second)
    assert service.reserve_next(factory,scope) is None
    assert service.grants_list(factory,scope)[0]["used_requests"]==0


def test_runtime_worker_process_restart_heartbeats_and_never_replays_unknown_post(runtime_db):
    """Kill a real worker subprocess while fake transport holds an unknown outcome."""
    factory,scope,admin=runtime_db
    grant=service.grant_create(factory,scope,"fixture-owner",grant_spec())
    run_id=create(factory,scope,grant)
    source=str(__import__("pathlib").Path(__file__).resolve().parents[1] / "src")
    bootstrap=(f"import sys;sys.path.insert(0,{source!r});from uuid import UUID;"
      "from agent_corporation_api.database import get_session_factory;"
      "from agent_corporation_api.modules.observability.scope import CompanyScope;"
      "from agent_corporation_api.modules.execution import worker,service;")
    child=bootstrap+f"scope=CompanyScope(UUID({str(scope.environment_id)!r}),UUID({str(scope.company_id)!r}));"
    child+="run=service.reserve_next(get_session_factory(),scope);assert run;"
    child+="import asyncio\n"
    child+="async def fake(*args):\n print('FAKE_TRANSPORT_ENTERED',flush=True)\n await asyncio.Event().wait()\n"
    child+="asyncio.run(worker.execute_reserved(get_session_factory(),scope,run,'http://fake.invalid',None,fake))"
    process=subprocess.Popen([sys.executable,"-u","-c",child],stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
    returncode=None
    heartbeat_advanced=False
    try:
        assert process.stdout is not None
        ready,_,_=select.select([process.stdout],[],[],10)
        assert ready and process.stdout.readline().strip()=="FAKE_TRANSPORT_ENTERED"
        before=rows(factory,scope,"SELECT heartbeat_at FROM model_calls WHERE run_id=:id",id=run_id)[0]["heartbeat_at"]
        deadline=time.monotonic()+15
        heartbeat=before
        while time.monotonic()<deadline and heartbeat==before:
            time.sleep(.2)
            heartbeat=rows(factory,scope,"SELECT heartbeat_at FROM model_calls WHERE run_id=:id",id=run_id)[0]["heartbeat_at"]
        heartbeat_advanced=heartbeat>before
    finally:
        if process.poll() is None:
            process.kill()
        returncode=process.wait(timeout=5)
        if process.stdout:
            process.stdout.close()
        if process.stderr:
            process.stderr.close()
    assert heartbeat_advanced, "worker subprocess heartbeat did not advance"
    assert returncode < 0
    assert rows(factory,scope,"SELECT status FROM model_calls WHERE run_id=:id",id=run_id)[0]["status"]=="dispatched"
    assert rows(factory,scope,"SELECT boundary FROM checkpoints WHERE run_id=:id ORDER BY sequence",id=run_id)==[
        {"boundary":"before_dispatch"},{"boundary":"dispatch_reserved"}]
    with admin.begin() as con:
        con.execute(text("UPDATE model_calls SET lease_until=CURRENT_TIMESTAMP-interval '1 second' WHERE run_id=:id"),{"id":run_id})
    restart=bootstrap+f"scope=CompanyScope(UUID({str(scope.environment_id)!r}),UUID({str(scope.company_id)!r}));"
    restart+="import asyncio;asyncio.run(worker.work(scope,once=True));"
    restarted=subprocess.run([sys.executable,"-c",restart],capture_output=True,text=True,timeout=15)
    assert restarted.returncode==0,restarted.stderr
    call=rows(factory,scope,"SELECT status,usage FROM model_calls WHERE run_id=:id",id=run_id)
    run=service.run_get(factory,scope,run_id)
    assert len(call)==1 and call[0]["status"]=="unknown" and call[0]["usage"] is None
    assert run["status"]=="interrupted" and run["outcome"]=="worker_lease_expired"
    assert service.reserve_next(factory,scope) is None
    event_rows=rows(factory,scope,"SELECT stream_seq FROM events ORDER BY stream_seq")
    latest=rows(factory,scope,"SELECT last_seq FROM event_stream_counters WHERE environment_id=:env AND company_id=:company",env=scope.environment_id,company=scope.company_id)[0]["last_seq"]
    assert [row["stream_seq"] for row in event_rows]==list(range(1,latest+1))
    ordered_events=rows(factory,scope,"SELECT event_type FROM events WHERE run_id=:id ORDER BY stream_seq",id=run_id)
    assert [item["event_type"] for item in ordered_events]==[
      "RUN_CREATED","TASK_STATE_CHANGED","TASK_STATE_CHANGED","TASK_STARTED","RUN_STATE_CHANGED",
      "LLM_CALL_STARTED","RUN_STATE_CHANGED","TASK_STATE_CHANGED","LLM_CALL_FAILED"]
    evidence_path=os.getenv("IG08_EVIDENCE_PATH")
    if evidence_path:
        call_detail=rows(factory,scope,"SELECT id,status,usage FROM model_calls WHERE run_id=:id",id=run_id)[0]
        events=rows(factory,scope,"SELECT event_id,event_type,stream_seq,correlation_id FROM events WHERE run_id=:id ORDER BY stream_seq",id=run_id)
        checkpoints=rows(factory,scope,"SELECT sequence,boundary FROM checkpoints WHERE run_id=:id ORDER BY sequence",id=run_id)
        Path(evidence_path).write_text(json.dumps({
          "classification":"synthetic_test_data",
          "infrastructure":"unique disposable PostgreSQL database/role; user runtime unchanged",
          "transport":"injected fake coroutine; no network or inference",
          "run_id":str(run_id),"task_id":str(run["task_id"]),"request_span_id":str(call_detail["id"]),
          "worker_process_returncode":returncode,"restart_process_returncode":restarted.returncode,
          "fake_transport_entries":1,"model_call_count":len(rows(factory,scope,"SELECT id FROM model_calls WHERE run_id=:id",id=run_id)),
          "model_call_status":call_detail["status"],"usage":call_detail["usage"],
          "run_status":run["status"],"run_outcome":run["outcome"],"events":[
            {**event,"event_id":str(event["event_id"]),"correlation_id":str(event["correlation_id"])} for event in events],
          "checkpoints":[dict(item) for item in checkpoints],
          "event_stream_sequence_contiguous":True,"event_type_order_verified":True,"recovered_run_was_not_reserved_again":True
        },ensure_ascii=False,indent=2,default=str)+"\n",encoding="utf-8")


@pytest.mark.parametrize(("http_status", "expected"), [(401, "failed"), (403, "failed"), (None, "unknown")])
def test_gateway_expiry_invalidation_and_disconnect_keep_app_checkpoint_without_replay(runtime_db, http_status, expected):
    """Gateway is stateless: auth rejection is visible; disconnect stays unknown and is never replayed."""
    import asyncio
    from agent_corporation_api.modules.execution import worker

    factory,scope,_=runtime_db
    grant=service.grant_create(factory,scope,"fixture-owner",grant_spec(2))
    run_id=create(factory,scope,grant)
    reserved=service.reserve_next(factory,scope)
    calls=[]

    async def fake_transport(_base,_key,payload,_timeout):
        calls.append(payload)
        assert payload["messages"] == reserved["history"]
        if http_status is None:
            # Request reached the fake peer, then the peer closed without a final response.
            return CallOutcome("unknown", "timeout_or_disconnect")
        return parse_response(http_status, {"x-codex-call-id":"fixture-auth-response"}, b"{}")

    asyncio.run(worker.execute_reserved(factory,scope,reserved,"http://127.0.0.1:1",None,fake_transport))
    assert len(calls)==1
    run=service.run_get(factory,scope,run_id)
    call=rows(factory,scope,"SELECT id,status,usage,gateway_call_id FROM model_calls WHERE run_id=:id",id=run_id)[0]
    checkpoint_rows=rows(factory,scope,"SELECT boundary,checkpoint FROM checkpoints WHERE run_id=:id ORDER BY sequence",id=run_id)
    assert run["status"] == ("interrupted" if expected=="unknown" else "failed")
    assert call["status"] == expected and call["usage"] is None
    assert call["id"] == reserved["request_span_id"]
    assert checkpoint_rows[-1]["checkpoint"]["request_span_id"] == str(reserved["request_span_id"])
    assert checkpoint_rows[-1]["checkpoint"]["replay_allowed"] is False
    assert service.reserve_next(factory,scope) is None


def test_429_requeue_bounded_without_fallback_and_usage_unknown(runtime_db):
    factory,scope,admin=runtime_db
    grant=service.grant_create(factory,scope,"fixture-owner",grant_spec(2,1))
    run_id=create(factory,scope,grant)
    reserved=service.reserve_next(factory,scope)
    service.finish(factory,scope,reserved,CallOutcome("rate_limited","gateway_429"))
    assert service.run_get(factory,scope,run_id)["status"]=="queued"
    assert service.reserve_next(factory,scope) is None
    with admin.begin() as con:
        con.execute(text("UPDATE runtime_runs SET available_at=CURRENT_TIMESTAMP WHERE id=:id"),{"id":run_id})
    second=service.reserve_next(factory,scope)
    assert second["attempt"]==2 and second["model"]=="fixture-model"
    service.finish(factory,scope,second,CallOutcome("rate_limited","gateway_429"))
    result=service.run_get(factory,scope,run_id)
    assert result["status"]=="failed" and result["usage"] is None
    assert service.reserve_next(factory,scope) is None
    assert service.grants_list(factory,scope)[0]["used_requests"]==2


def test_dispatch_transaction_rollback_no_reservation_or_events(runtime_db,monkeypatch):
    factory,scope,_=runtime_db
    grant=service.grant_create(factory,scope,"fixture-owner",grant_spec())
    run_id=create(factory,scope,grant)
    before=rows(factory,scope,"SELECT * FROM events")
    def fail(*args,**kwargs):
        raise RuntimeError("fixture atomic rollback")
    monkeypatch.setattr(service,"checkpoint",fail)
    with pytest.raises(RuntimeError):
        service.reserve_next(factory,scope)
    assert rows(factory,scope,"SELECT * FROM model_calls")==[]
    assert len(rows(factory,scope,"SELECT * FROM events"))==len(before)
    assert service.grants_list(factory,scope)[0]["used_requests"]==0
    assert service.run_get(factory,scope,run_id)["status"]=="queued"


def test_global_dispatch_guard_cross_company_race_and_heartbeat(runtime_db):
    factory,scope,admin=runtime_db
    other_scope=CompanyScope(scope.environment_id,uuid4())
    with admin.begin() as con:
        con.execute(text("INSERT INTO companies(id,environment_id,name) VALUES(:id,:env,'other fixture runtime')"),{"id":other_scope.company_id,"env":other_scope.environment_id})
        other_employee,other_version=uuid4(),uuid4()
        con.execute(text("INSERT INTO employees(id,environment_id,company_id,lifecycle) VALUES(:id,:env,:company,'active')"),{"id":other_employee,"env":other_scope.environment_id,"company":other_scope.company_id})
        con.execute(text("INSERT INTO employee_versions(id,environment_id,company_id,employee_id,version,profile) VALUES(:id,:env,:company,:employee,1,'{\"display_name\":\"Other fixture employee\",\"role\":\"Analyst\"}')"),{"id":other_version,"env":other_scope.environment_id,"company":other_scope.company_id,"employee":other_employee})
    grant1=service.grant_create(factory,scope,"fixture-owner",grant_spec())
    grant2=service.grant_create(factory,other_scope,"fixture-owner",grant_spec())
    create(factory,scope,grant1)
    create(factory,other_scope,grant2)
    with ThreadPoolExecutor(max_workers=2) as pool:
        calls=list(pool.map(lambda item:service.reserve_next(factory,item),(scope,other_scope)))
    assert len([call for call in calls if call])==1
    index=0 if calls[0] else 1
    chosen=(scope,other_scope)[index]
    not_chosen=(scope,other_scope)[1-index]
    run=calls[index]
    with admin.begin() as con:
        con.execute(text("UPDATE model_calls SET heartbeat_at=CURRENT_TIMESTAMP-interval '20 seconds' WHERE id=:id"),{"id":run["request_span_id"]})
    service.heartbeat(factory,chosen,run)
    detail=service.run_get(factory,chosen,run["id"])
    assert datetime.now(UTC)-detail["worker_heartbeat_at"]<timedelta(seconds=2)
    assert detail["lease_until"]>datetime.now(UTC)
    assert service.reserve_next(factory,not_chosen) is None
    service.finish(factory,chosen,run,CallOutcome("completed","fixture_final","Fixture global guard artifact"))
    assert service.reserve_next(factory,not_chosen) is not None


def test_missing_usage_holds_same_grant_reservation_read_is_side_effect_free(runtime_db):
    factory,scope,admin=runtime_db
    grant=service.grant_create(factory,scope,"fixture-owner",grant_spec(3))
    run_id=create(factory,scope,grant)
    call=service.reserve_next(factory,scope)
    service.finish(factory,scope,call,CallOutcome("completed","final_response","Fixture no usage"))
    assert service.run_get(factory,scope,run_id)["status"]=="completed"
    assert service.run_get(factory,scope,run_id)["usage"] is None
    waiting=create(factory,scope,grant)
    assert service.reserve_next(factory,scope) is None
    assert service.grants_list(factory,scope)[0]["used_requests"]==1
    assert service.run_get(factory,scope,waiting)["outcome"]=="usage_unresolved"
    # GET/list does not create a stream counter or fail on an unprovisioned scope.
    absent=CompanyScope(uuid4(),uuid4())
    assert service.runs_list(factory,absent)==[]
    assert service.grants_list(factory,absent)==[]
    with pytest.raises(service.RuntimeDenied,match="run_not_found"):
        service.run_get(factory,absent,uuid4())
    with admin.begin() as con:
        assert con.execute(text("SELECT count(*) FROM event_stream_counters WHERE environment_id=:env"),{"env":absent.environment_id}).scalar_one()==0


def test_grant_expires_while_queued_task_blocks_without_span(runtime_db):
    factory,scope,admin=runtime_db
    grant=service.grant_create(factory,scope,"fixture-owner",grant_spec())
    run_id=create(factory,scope,grant)
    with admin.begin() as con:
        con.execute(text("UPDATE inference_grants SET expires_at=CURRENT_TIMESTAMP-interval '1 second' WHERE id=:id"),{"id":grant["id"]})
    assert service.reserve_next(factory,scope) is None
    detail=service.run_get(factory,scope,run_id)
    assert detail["status"]=="failed" and detail["outcome"]=="expired_grant"
    assert rows(factory,scope,"SELECT status FROM task_execution_state WHERE task_id=:id",id=detail["task_id"])[0]["status"]=="blocked"
    assert rows(factory,scope,"SELECT * FROM model_calls")==[]
    assert service.grants_list(factory,scope)[0]["used_requests"]==0


def test_late_usage_correction_is_immutable_dedup_and_gateway_bound(runtime_db):
    from sqlalchemy.exc import DBAPIError
    factory,scope,admin=runtime_db
    grant=service.grant_create(factory,scope,"fixture-owner",grant_spec(3))
    run_id=create(factory,scope,grant)
    call=service.reserve_next(factory,scope)
    gateway_id=str(uuid4())
    service.finish(factory,scope,call,CallOutcome("completed","final_response","Original fixture output",gateway_id,None))
    next_id=create(factory,scope,grant)
    assert service.reserve_next(factory,scope) is None
    usage={"prompt_tokens":2,"completion_tokens":3,"total_tokens":5}
    with pytest.raises(service.RuntimeDenied,match="gateway_mismatch"):
        service.finish(factory,scope,call,CallOutcome("completed","late_usage",gateway_call_id=str(uuid4()),usage=usage))
    service.finish(factory,scope,call,CallOutcome("completed","late_usage",gateway_call_id=gateway_id,usage=usage))
    service.finish(factory,scope,call,CallOutcome("completed","duplicate",gateway_call_id=gateway_id,usage=usage))
    with pytest.raises(service.RuntimeDenied,match="conflicting_usage"):
        service.finish(factory,scope,call,CallOutcome("completed","conflict",gateway_call_id=gateway_id,usage={"prompt_tokens":3,"completion_tokens":3,"total_tokens":6}))
    detail=service.run_get(factory,scope,run_id)
    assert detail["status"]=="completed" and detail["original_usage"] is None and detail["usage"]==usage
    assert detail["usage_provenance"]=="gateway_final_response_correction"
    assert detail["output"]=="Original fixture output" and detail["outcome"]=="final_response"
    assert len(rows(factory,scope,"SELECT * FROM runtime_usage_corrections"))==1
    original=rows(factory,scope,"SELECT status,usage FROM model_calls WHERE id=:id",id=call["request_span_id"])[0]
    assert original=={"status":"completed","usage":None}
    assert service.grants_list(factory,scope)[0]["used_requests"]==1
    with factory() as ses,ses.begin():
        set_company_scope(ses,scope)
        with pytest.raises(DBAPIError):
            ses.execute(text("UPDATE runtime_usage_corrections SET source='gateway_final_response'"))
    reserved=service.reserve_next(factory,scope)
    assert reserved["id"]==next_id
    assert service.grants_list(factory,scope)[0]["used_requests"]==2


def test_fenced_late_usage_never_revives_unknown_call_or_grant(runtime_db):
    factory,scope,admin=runtime_db
    grant=service.grant_create(factory,scope,"fixture-owner",grant_spec(3))
    run_id=create(factory,scope,grant)
    call=service.reserve_next(factory,scope)
    with admin.begin() as con:
        con.execute(text("UPDATE model_calls SET lease_until=CURRENT_TIMESTAMP-interval '1 second' WHERE id=:id"),{"id":call["request_span_id"]})
        con.execute(text("UPDATE inference_grants SET revoked=true,expires_at=CURRENT_TIMESTAMP-interval '1 second' WHERE id=:id"),{"id":grant["id"]})
    assert service.recover_expired(factory,scope)==1
    usage={"prompt_tokens":0,"completion_tokens":0,"total_tokens":0}
    gateway_id=str(uuid4())
    late=CallOutcome("completed","late_final","Do not revive output",gateway_id,usage)
    service.finish(factory,scope,call,late)
    service.finish(factory,scope,call,late)
    detail=service.run_get(factory,scope,run_id)
    assert detail["status"]=="interrupted" and detail["output"] is None and detail["outcome"]=="worker_lease_expired"
    assert detail["usage"]==usage and detail["original_usage"] is None
    assert rows(factory,scope,"SELECT status,usage FROM model_calls WHERE id=:id",id=call["request_span_id"])[0]=={"status":"unknown","usage":None}
    with admin.begin() as con:
        assert con.execute(text("SELECT request_span_id FROM runtime_dispatch_guard WHERE id=1")).scalar_one()==call["request_span_id"]
    old=service.grants_list(factory,scope)[0]
    assert old["revoked"] is True and old["expires_at"]<datetime.now(UTC) and old["used_requests"]==1
    with pytest.raises(service.RuntimeDenied):
        create(factory,scope,grant)
    fresh=service.grant_create(factory,scope,"fixture-owner",grant_spec())
    create(factory,scope,fresh)
    assert service.reserve_next(factory,scope) is None
