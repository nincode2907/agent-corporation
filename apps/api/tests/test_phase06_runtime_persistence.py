"""Opt-in PG fixture only; requires disposable database/migrations prepared by runner."""
import os
from concurrent.futures import ThreadPoolExecutor
from datetime import UTC, datetime, timedelta
from uuid import uuid4
import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from agent_corporation_api.settings import get_settings
from agent_corporation_api.modules.observability.scope import CompanyScope, set_company_scope
from agent_corporation_api.modules.execution import service
from agent_corporation_api.modules.execution.gateway import CallOutcome

pytestmark=pytest.mark.skipif(os.getenv("PHASE_RUNTIME_TEST_ISOLATED")!="1",reason="Requires opt-in isolated PostgreSQL; never mutates shared DB")

@pytest.fixture
def runtime_db():
    settings=get_settings()
    app=create_engine(settings.database_url)
    admin=create_engine(settings.migration_database_url)
    factory=sessionmaker(app,expire_on_commit=False)
    scope=CompanyScope(uuid4(),uuid4())
    with admin.begin() as con:
        con.execute(text("INSERT INTO environments(id,name,kind) VALUES(:id,:name,'demo')"),{"id":scope.environment_id,"name":f"runtime-fixture-{scope.environment_id}"})
        con.execute(text("INSERT INTO companies(id,environment_id,name) VALUES(:id,:env,'fixture runtime')"),{"id":scope.company_id,"env":scope.environment_id})
    yield factory,scope,admin
    with admin.begin() as con:
        con.execute(text("UPDATE runtime_dispatch_guard SET request_span_id=NULL,environment_id=NULL,company_id=NULL WHERE environment_id=:env"),{"env":scope.environment_id})
        for table in ("runtime_usage_corrections","model_calls","runtime_runs","inference_grants","outbox_events","events","artifacts","checkpoints","run_execution_state","runs","task_execution_state","task_revisions","work_orders","event_stream_counters","owner_model_profiles","companies"):
            con.execute(text(f"DELETE FROM {table} WHERE environment_id=:env"),{"env":scope.environment_id})
        con.execute(text("DELETE FROM environments WHERE id=:env"),{"env":scope.environment_id})
    app.dispose()
    admin.dispose()


def grant_spec(requests=1,requeues=0):
    return {"phase":"06","batch_id":"fake-runtime-pg","purpose":"isolated-fixture-only","model":"fixture-model","effort":"low","max_requests":requests,"max_concurrency":1,"timeout_seconds":1,"max_requeues":requeues,"expires_at":datetime.now(UTC)+timedelta(minutes=1)}


def create(factory,scope,grant,**overrides):
    spec={key:grant[key] for key in ("phase","batch_id","purpose","model","effort")}
    return service.run_create(factory,scope,"fixture-owner",{**spec,"grant_id":grant["id"],"input_text":"Văn bản fixture tin cậy, không đọc file.","idempotency_key":uuid4(),**overrides})


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
    stopped_task=service.run_get(factory,scope,stopped)["task_id"]
    assert rows(factory,scope,"SELECT status FROM task_execution_state WHERE task_id=:id",id=stopped_task)[0]["status"]=="cancelled"
    assert service.reserve_next(factory,scope) is None
    waiting=create(factory,scope,grant)
    service.revoke_grant(factory,scope,grant["id"])
    assert service.run_get(factory,scope,waiting)["status"]=="cancelled"
    assert service.reserve_next(factory,scope) is None
    assert rows(factory,scope,"SELECT * FROM model_calls")==[]


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
    # New grant must not bypass unknown in-flight concurrency from older grant.
    second=service.grant_create(factory,scope,"fixture-owner",grant_spec())
    create(factory,scope,second)
    assert service.reserve_next(factory,scope) is None
    assert service.grants_list(factory,scope)[0]["used_requests"]==0


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
