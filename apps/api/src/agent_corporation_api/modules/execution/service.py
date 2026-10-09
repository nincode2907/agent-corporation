from __future__ import annotations
import hashlib
import json
from contextlib import contextmanager
from datetime import UTC, datetime, timedelta
from uuid import UUID, uuid4
from sqlalchemy import text
from ..observability.scope import CompanyScope, set_company_scope
from ..observability.events import append_event, lock_event_stream
from ..observability.redaction import redact_text
from .gateway import CallOutcome
from ..work.commands import TASK_TRANSITIONS

class RuntimeDenied(ValueError):
    pass


def params(scope, **values):
    return {"environment_id":scope.environment_id,"company_id":scope.company_id,**values}


@contextmanager
def transaction(factory, scope, *, write=True):
    with factory() as session, session.begin():
        set_company_scope(session,scope)
        if write:
            session.execute(text("SELECT id FROM runtime_dispatch_guard WHERE id=1 FOR UPDATE")).scalar_one()
            # Consistent ordering with the shared event allocator and concurrent scope commands.
            lock_event_stream(session,scope)
        yield session


def event(session, scope, run, event_type, payload, key):
    append_event(session,scope=scope,event_type=event_type,task_id=run["task_id"],run_id=run["id"],
        correlation_id=run["id"],parent_event_id=None,source="app",actor={"kind":"system","id":"bounded-runtime"},
        sensitivity="internal",payload=payload,evidence_refs=[],dedup_key=key)


def change_state(session,scope,run,target,reason):
    old = session.execute(text("SELECT status FROM run_execution_state WHERE environment_id=:environment_id AND company_id=:company_id AND run_id=:id FOR UPDATE"),params(scope,id=run["id"])).scalar_one()
    if old == target:
        return
    version = session.execute(text("UPDATE run_execution_state SET status=:status,transition_version=transition_version+1,updated_at=CURRENT_TIMESTAMP WHERE environment_id=:environment_id AND company_id=:company_id AND run_id=:id RETURNING transition_version"),params(scope,id=run["id"],status=target)).scalar_one()
    event(session,scope,run,"RUN_STATE_CHANGED",{"from":old,"to":target,"reason":reason,"new_version":version},f"runtime:{run['id']}:state:{version}")


def change_task(session,scope,run,target,reason):
    row=session.execute(text("SELECT status,transition_version FROM task_execution_state WHERE environment_id=:environment_id AND company_id=:company_id AND task_id=:id FOR UPDATE"),params(scope,id=run["task_id"])).mappings().one()
    old=row["status"]
    if old==target:
        return
    if target not in TASK_TRANSITIONS.get(old,set()):
        raise RuntimeDenied(f"illegal_runtime_task_transition:{old}:{target}")
    version=row["transition_version"]+1
    session.execute(text("UPDATE task_execution_state SET status=:status,transition_version=:version,resume_target=NULL,updated_at=CURRENT_TIMESTAMP WHERE environment_id=:environment_id AND company_id=:company_id AND task_id=:id"),params(scope,id=run["task_id"],status=target,version=version))
    event(session,scope,run,"TASK_STATE_CHANGED",{"from":old,"to":target,"reason":reason,"expected_version":row["transition_version"],"new_version":version},f"runtime:{run['id']}:task:{version}")


def block_task(session,scope,run,reason):
    current=session.execute(text("SELECT status FROM task_execution_state WHERE environment_id=:environment_id AND company_id=:company_id AND task_id=:id"),params(scope,id=run["task_id"])).scalar_one()
    if current=="queued":
        change_task(session,scope,run,"planning","runtime_preflight")
    change_task(session,scope,run,"blocked",reason)


def checkpoint(session,scope,run,boundary,data):
    sequence = session.execute(text("SELECT coalesce(max(sequence),0)+1 FROM checkpoints WHERE environment_id=:environment_id AND company_id=:company_id AND run_id=:id"),params(scope,id=run["id"])).scalar_one()
    session.execute(text("INSERT INTO checkpoints(id,environment_id,company_id,run_id,sequence,boundary,checkpoint) VALUES(:checkpoint_id,:environment_id,:company_id,:id,:sequence,:boundary,CAST(:checkpoint AS jsonb))"),params(scope,id=run["id"],checkpoint_id=uuid4(),sequence=sequence,boundary=boundary,checkpoint=json.dumps(data)))


def validate_grant(grant, run, now, active):
    if not grant or grant["revoked"]:
        raise RuntimeDenied("missing_or_revoked_grant")
    if grant["expires_at"] <= now:
        raise RuntimeDenied("expired_grant")
    if any(grant[key] != run[key] for key in ("phase","batch_id","purpose","model","effort")):
        raise RuntimeDenied("grant_scope_mismatch")
    if run.get("stop_requested"):
        raise RuntimeDenied("stop_active")
    if grant["used_requests"] >= grant["max_requests"]:
        raise RuntimeDenied("request_limit")
    if active >= grant["max_concurrency"]:
        raise RuntimeDenied("concurrency_limit")


def grant_create(factory,scope,owner_id,spec):
    now = datetime.now(UTC)
    if spec["expires_at"] <= now or spec["expires_at"] > now+timedelta(hours=1):
        raise RuntimeDenied("grant_expiry_must_be_within_one_hour")
    with transaction(factory,scope) as session:
        grant_id=uuid4()
        session.execute(text("""INSERT INTO inference_grants(environment_id,company_id,id,phase,batch_id,purpose,model,effort,max_requests,max_concurrency,timeout_seconds,max_requeues,expires_at,owner_id)
          VALUES(:environment_id,:company_id,:id,:phase,:batch_id,:purpose,:model,:effort,:max_requests,:max_concurrency,:timeout_seconds,:max_requeues,:expires_at,:owner_id)"""),params(scope,id=grant_id,owner_id=owner_id,**spec))
        append_event(session,scope=scope,event_type="EXECUTION_GRANT_CREATED",task_id=None,run_id=None,correlation_id=grant_id,parent_event_id=None,source="app",actor={"kind":"owner","id":owner_id},sensitivity="internal",payload={"grant_id":str(grant_id),"phase":spec["phase"],"batch_id":spec["batch_id"],"max_requests":spec["max_requests"],"expiry":spec["expires_at"].isoformat()},evidence_refs=[],dedup_key=f"runtime:grant:{grant_id}")
        return {"id":grant_id,**spec,"used_requests":0,"revoked":False}


def grants_list(factory,scope):
    with transaction(factory,scope,write=False) as session:
        return [dict(row) for row in session.execute(text("SELECT id,phase,batch_id,purpose,model,effort,max_requests,used_requests,max_concurrency,timeout_seconds,max_requeues,expires_at,revoked FROM inference_grants WHERE environment_id=:environment_id AND company_id=:company_id ORDER BY created_at DESC LIMIT 20"),params(scope)).mappings()]


def revoke_grant(factory,scope,grant_id):
    with transaction(factory,scope) as session:
        if not session.execute(text("UPDATE inference_grants SET revoked=true WHERE environment_id=:environment_id AND company_id=:company_id AND id=:id RETURNING id"),params(scope,id=grant_id)).first():
            raise RuntimeDenied("grant_not_found")
        # Stop queued work; active worker notices revoked grants during its cancellation poll.
        runs=session.execute(text("SELECT * FROM runtime_runs WHERE environment_id=:environment_id AND company_id=:company_id AND grant_id=:id"),params(scope,id=grant_id)).mappings().all()
        for run in runs:
            stop_in_transaction(session,scope,run)


def run_create(factory,scope,owner_id,spec):
    encoded=json.dumps({key:str(value) for key,value in spec.items() if key != "idempotency_key"},sort_keys=True).encode()
    request_hash=hashlib.sha256(encoded).hexdigest()
    with transaction(factory,scope) as session:
        prior=session.execute(text("SELECT id,request_hash FROM runtime_runs WHERE environment_id=:environment_id AND company_id=:company_id AND idempotency_key=:key"),params(scope,key=spec["idempotency_key"])).mappings().first()
        if prior:
            if prior["request_hash"] != request_hash:
                raise RuntimeDenied("idempotency_payload_mismatch")
            return prior["id"]
        grant=session.execute(text("SELECT * FROM inference_grants WHERE environment_id=:environment_id AND company_id=:company_id AND id=:id FOR UPDATE"),params(scope,id=spec["grant_id"])).mappings().first()
        validate_grant(grant,spec,datetime.now(UTC),0)
        task_id,run_id=uuid4(),uuid4()
        actor=json.dumps({"kind":"owner","id":owner_id})
        session.execute(text("INSERT INTO work_orders(id,environment_id,company_id,created_by) VALUES(:id,:environment_id,:company_id,CAST(:actor AS jsonb))"),params(scope,id=task_id,actor=actor))
        session.execute(text("""INSERT INTO task_revisions(task_id,environment_id,company_id,revision,goal,expected_outputs,acceptance_criteria,autonomy,created_by,execution_grant_id,budget_limits)
          VALUES(:id,:environment_id,:company_id,1,'Phân tích văn bản được cấp','["Kết quả văn bản"]','["Text-only; cần Chủ tịch nghiệm thu"]','strict',CAST(:actor AS jsonb),:grant_id,CAST(:limits AS jsonb))"""),params(scope,id=task_id,actor=actor,grant_id=spec["grant_id"],limits=json.dumps({"max_turns":1,"cost_basis":"unknown"})))
        session.execute(text("INSERT INTO task_execution_state(task_id,environment_id,company_id,revision,status) VALUES(:id,:environment_id,:company_id,1,'queued')"),params(scope,id=task_id))
        owner_profile=session.execute(text("SELECT version,model,reasoning_effort,fallback_models FROM owner_model_profiles WHERE environment_id=:environment_id AND company_id=:company_id"),params(scope)).mappings().first()
        profile={"owner_profile":dict(owner_profile) if owner_profile else None,"effective_source":"explicit_owner_grant","model":spec["model"],"effort":spec["effort"],"tools":False,"fallback_models":[],"grant_id":str(spec["grant_id"])}
        session.execute(text("INSERT INTO runs(id,environment_id,company_id,task_id,task_revision,attempt,profile_snapshot) VALUES(:id,:environment_id,:company_id,:task_id,1,1,CAST(:profile AS jsonb))"),params(scope,id=run_id,task_id=task_id,profile=json.dumps(profile)))
        session.execute(text("INSERT INTO run_execution_state(run_id,environment_id,company_id,status,current_step) VALUES(:id,:environment_id,:company_id,'queued',0)"),params(scope,id=run_id))
        history=[{"role":"system","content":"Chỉ phân tích văn bản được cấp. Không công cụ, không đọc file, không truy cập dữ liệu khác."},{"role":"user","content":spec["input_text"]}]
        policy={"tools":False,"max_turns":1,"timeout_seconds":grant["timeout_seconds"],"max_requeues":grant["max_requeues"],"cost_basis":"unknown","fallback":False}
        session.execute(text("""INSERT INTO runtime_runs(environment_id,company_id,id,task_id,grant_id,phase,batch_id,purpose,model,effort,input_text,idempotency_key,request_hash,policy_snapshot,history)
          VALUES(:environment_id,:company_id,:id,:task_id,:grant_id,:phase,:batch_id,:purpose,:model,:effort,:input_text,:idempotency_key,:request_hash,CAST(:policy AS jsonb),CAST(:history AS jsonb))"""),params(scope,id=run_id,task_id=task_id,request_hash=request_hash,policy=json.dumps(policy),history=json.dumps(history,ensure_ascii=False),**spec))
        run={"id":run_id,"task_id":task_id}
        checkpoint(session,scope,run,"before_dispatch",{"history":history,"policy":policy,"profile":profile})
        event(session,scope,run,"RUN_CREATED",{"status":"queued","mode":"text_only","grant_id":str(spec["grant_id"])},f"runtime:{run_id}:created")
        return run_id


RUN_SELECT="""SELECT r.id,r.task_id,s.status,r.model,r.effort,r.batch_id,r.purpose,r.created_at,r.stop_requested,r.outcome,
 coalesce(r.usage,(SELECT u.usage FROM runtime_usage_corrections u JOIN model_calls c ON c.environment_id=u.environment_id AND c.company_id=u.company_id AND c.id=u.request_span_id WHERE c.environment_id=r.environment_id AND c.company_id=r.company_id AND c.run_id=r.id ORDER BY c.attempt DESC LIMIT 1)) AS usage,
 r.usage AS original_usage,
 CASE WHEN r.usage IS NOT NULL THEN 'gateway_final_response' WHEN EXISTS(SELECT 1 FROM runtime_usage_corrections u JOIN model_calls c ON c.environment_id=u.environment_id AND c.company_id=u.company_id AND c.id=u.request_span_id WHERE c.environment_id=r.environment_id AND c.company_id=r.company_id AND c.run_id=r.id) THEN 'gateway_final_response_correction' ELSE 'unknown' END AS usage_provenance,
 r.artifact_id,r.output,
 (SELECT gateway_call_id FROM model_calls c WHERE c.environment_id=r.environment_id AND c.company_id=r.company_id AND c.run_id=r.id ORDER BY attempt DESC LIMIT 1) AS gateway_call_id,
 (SELECT heartbeat_at FROM model_calls c WHERE c.environment_id=r.environment_id AND c.company_id=r.company_id AND c.run_id=r.id ORDER BY attempt DESC LIMIT 1) AS worker_heartbeat_at,
 (SELECT lease_until FROM model_calls c WHERE c.environment_id=r.environment_id AND c.company_id=r.company_id AND c.run_id=r.id ORDER BY attempt DESC LIMIT 1) AS lease_until
 FROM runtime_runs r JOIN run_execution_state s ON s.environment_id=r.environment_id AND s.company_id=r.company_id AND s.run_id=r.id
 WHERE r.environment_id=:environment_id AND r.company_id=:company_id"""


def run_get(factory,scope,run_id):
    with transaction(factory,scope,write=False) as session:
        row=session.execute(text(RUN_SELECT+" AND r.id=:id"),params(scope,id=run_id)).mappings().first()
        if not row:
            raise RuntimeDenied("run_not_found")
        return {**dict(row),"worker_lease_until":row["lease_until"]}


def runs_list(factory,scope):
    with transaction(factory,scope,write=False) as session:
        return [{**dict(row),"worker_lease_until":row["lease_until"]} for row in session.execute(text(RUN_SELECT+" ORDER BY r.created_at DESC LIMIT 20"),params(scope)).mappings()]


def stop_in_transaction(session,scope,run):
    status=session.execute(text("SELECT status FROM run_execution_state WHERE environment_id=:environment_id AND company_id=:company_id AND run_id=:id"),params(scope,id=run["id"])).scalar_one()
    if status in ("completed","failed","cancelled","interrupted") or run["stop_requested"]:
        return
    session.execute(text("UPDATE runtime_runs SET stop_requested=true,stop_epoch=stop_epoch+1 WHERE environment_id=:environment_id AND company_id=:company_id AND id=:id"),params(scope,id=run["id"]))
    if status == "queued":
        change_state(session,scope,run,"cancelled","stop_before_dispatch")
        change_task(session,scope,run,"cancelled","stop_before_dispatch")
    event(session,scope,run,"RUN_STOP_REQUESTED",{"in_flight":status=="waiting_model","cancellation_verified":False},f"runtime:{run['id']}:stop")


def run_stop(factory,scope,run_id):
    with transaction(factory,scope) as session:
        run=session.execute(text("SELECT * FROM runtime_runs WHERE environment_id=:environment_id AND company_id=:company_id AND id=:id FOR UPDATE"),params(scope,id=run_id)).mappings().first()
        if not run:
            raise RuntimeDenied("run_not_found")
        stop_in_transaction(session,scope,run)


def reserve_next(factory,scope):
    with transaction(factory,scope) as session:
        if session.execute(text("SELECT request_span_id FROM runtime_dispatch_guard WHERE id=1")).scalar_one_or_none() is not None:
            return None
        run=session.execute(text("""SELECT r.* FROM runtime_runs r JOIN run_execution_state s ON s.environment_id=r.environment_id AND s.company_id=r.company_id AND s.run_id=r.id
          WHERE r.environment_id=:environment_id AND r.company_id=:company_id AND s.status='queued' AND r.available_at<=CURRENT_TIMESTAMP AND NOT r.stop_requested ORDER BY r.created_at LIMIT 1 FOR UPDATE OF r"""),params(scope)).mappings().first()
        if not run:
            return None
        run=dict(run)
        grant=session.execute(text("SELECT * FROM inference_grants WHERE environment_id=:environment_id AND company_id=:company_id AND id=:id FOR UPDATE"),params(scope,id=run["grant_id"])).mappings().first()
        active=session.execute(text("SELECT count(*) FROM model_calls WHERE environment_id=:environment_id AND company_id=:company_id AND status IN ('dispatched','unknown')"),params(scope,id=run["grant_id"])).scalar_one()
        try:
            validate_grant(grant,run,datetime.now(UTC),active)
        except RuntimeDenied as error:
            if str(error)=="concurrency_limit":
                return None
            change_state(session,scope,run,"failed",str(error))
            block_task(session,scope,run,str(error))
            session.execute(text("UPDATE runtime_runs SET outcome=:reason WHERE environment_id=:environment_id AND company_id=:company_id AND id=:id"),params(scope,id=run["id"],reason=str(error)))
            return None
        unresolved=session.execute(text("SELECT count(*) FROM model_calls WHERE environment_id=:environment_id AND company_id=:company_id AND grant_id=:id AND status='completed' AND usage IS NULL AND NOT EXISTS(SELECT 1 FROM runtime_usage_corrections u WHERE u.environment_id=model_calls.environment_id AND u.company_id=model_calls.company_id AND u.request_span_id=model_calls.id)"),params(scope,id=run["grant_id"])).scalar_one()
        if unresolved:
            session.execute(text("UPDATE runtime_runs SET outcome='usage_unresolved' WHERE environment_id=:environment_id AND company_id=:company_id AND id=:id"),params(scope,id=run["id"]))
            # A final response with no usage settles execution, never settles its resource reservation as zero.
            return None
        attempt=session.execute(text("SELECT coalesce(max(attempt),0)+1 FROM model_calls WHERE environment_id=:environment_id AND company_id=:company_id AND run_id=:id"),params(scope,id=run["id"])).scalar_one()
        if attempt > grant["max_requeues"]+1:
            change_state(session,scope,run,"failed","retry_limit")
            block_task(session,scope,run,"retry_limit")
            return None
        span_id=uuid4()
        session.execute(text("UPDATE inference_grants SET used_requests=used_requests+1 WHERE environment_id=:environment_id AND company_id=:company_id AND id=:id"),params(scope,id=run["grant_id"]))
        session.execute(text("""INSERT INTO model_calls(environment_id,company_id,id,run_id,grant_id,attempt,status,lease_until)
          VALUES(:environment_id,:company_id,:id,:run_id,:grant_id,:attempt,'dispatched',:lease_until)"""),params(scope,id=span_id,run_id=run["id"],grant_id=run["grant_id"],attempt=attempt,lease_until=datetime.now(UTC)+timedelta(seconds=grant["timeout_seconds"]+10)))
        session.execute(text("UPDATE runtime_dispatch_guard SET request_span_id=:id,environment_id=:environment_id,company_id=:company_id WHERE id=1"),params(scope,id=span_id))
        task_status=session.execute(text("SELECT status FROM task_execution_state WHERE environment_id=:environment_id AND company_id=:company_id AND task_id=:id"),params(scope,id=run["task_id"])).scalar_one()
        if task_status=="queued":
            change_task(session,scope,run,"planning","bounded_text_runtime_start")
            change_task(session,scope,run,"executing","text_only_dispatch")
            event(session,scope,run,"TASK_STARTED",{"task_revision":1,"request_span_id":str(span_id),"mode":"text_only"},f"runtime:{run['id']}:task_started")
        change_state(session,scope,run,"waiting_model","reserved_before_http")
        event(session,scope,run,"LLM_CALL_STARTED",{"request_span_id":str(span_id),"attempt":attempt,"model":run["model"],"usage":"unknown"},f"runtime:call:{span_id}:started")
        checkpoint(session,scope,run,"dispatch_reserved",{"request_span_id":str(span_id),"attempt":attempt,"replay_allowed":False})
        return {**run,"request_span_id":span_id,"attempt":attempt,"timeout_seconds":grant["timeout_seconds"],"max_requeues":grant["max_requeues"]}


def should_stop(factory,scope,run):
    with transaction(factory,scope,write=False) as session:
        row=session.execute(text("""SELECT r.stop_requested,g.revoked,g.expires_at FROM runtime_runs r JOIN inference_grants g ON g.environment_id=r.environment_id AND g.company_id=r.company_id AND g.id=r.grant_id WHERE r.environment_id=:environment_id AND r.company_id=:company_id AND r.id=:id"""),params(scope,id=run["id"])).mappings().one()
        return row["stop_requested"] or row["revoked"] or row["expires_at"] <= datetime.now(UTC)


def _validated_usage(usage):
    required=("prompt_tokens","completion_tokens","total_tokens")
    if not isinstance(usage,dict) or not all(type(usage.get(k)) is int and usage[k]>=0 for k in required):
        raise RuntimeDenied("invalid_usage_correction")
    if usage["total_tokens"]!=usage["prompt_tokens"]+usage["completion_tokens"]:
        raise RuntimeDenied("invalid_usage_correction")
    normalized={key:usage[key] for key in required}
    for key,maximum in (("prompt_tokens_details",usage["prompt_tokens"]),("completion_tokens_details",usage["completion_tokens"])):
        details=usage.get(key)
        if details is not None:
            if not isinstance(details,dict):
                raise RuntimeDenied("invalid_usage_correction")
            normalized[key]={}
            for name,value in details.items():
                if name not in ("cached_tokens","reasoning_tokens","cache_write_tokens") or value is not None and (type(value) is not int or not 0<=value<=maximum):
                    raise RuntimeDenied("invalid_usage_correction")
                normalized[key][name]=value
    return normalized


def usage_event_payload(run,gateway_id,usage,**extra):
    return {"request_span_id":str(run["request_span_id"]),"gateway_call_id":str(gateway_id) if gateway_id else None,
        "input_tokens":usage["prompt_tokens"],"output_tokens":usage["completion_tokens"],
        "total_tokens":usage["total_tokens"],"cached_tokens":usage.get("prompt_tokens_details",{}).get("cached_tokens"),
        "reasoning_tokens":usage.get("completion_tokens_details",{}).get("reasoning_tokens"),
        "usage_status":"confirmed","measurement":"confirmed","source":"gateway_final_response","cost_basis":"unknown",**extra}


def record_usage_correction(session,scope,run,outcome):
    """Internal trusted adapter boundary only; intentionally has no HTTP endpoint.

    An adapter keeps the reserved request-span when handling its final response.
    Known call IDs must match; if the connection had no original header, record
    its first observed final call ID only in this immutable correction.
    Execution outcome, original usage and consumed request count never change.
    """
    if outcome.usage is None:
        return False
    usage=_validated_usage(outcome.usage)
    try:
        gateway_id=UUID(outcome.gateway_call_id)
    except (ValueError,TypeError,AttributeError):
        raise RuntimeDenied("usage_correction_requires_gateway_id") from None
    call=session.execute(text("SELECT status,gateway_call_id,usage,run_id FROM model_calls WHERE environment_id=:environment_id AND company_id=:company_id AND id=:id FOR UPDATE"),params(scope,id=run["request_span_id"])).mappings().one()
    if call["run_id"]!=run["id"]:
        raise RuntimeDenied("usage_correction_span_mismatch")
    if call["gateway_call_id"] is not None:
        try:
            original_id=UUID(call["gateway_call_id"])
        except (ValueError,TypeError):
            raise RuntimeDenied("usage_correction_gateway_mismatch") from None
        if original_id!=gateway_id:
            raise RuntimeDenied("usage_correction_gateway_mismatch")
    if call["status"] not in ("completed","unknown"):
        raise RuntimeDenied("usage_correction_outcome_mismatch")
    if call["usage"] is not None:
        if _validated_usage(call["usage"])!=usage:
            raise RuntimeDenied("conflicting_usage_correction")
        return False
    encoded=json.dumps(usage,sort_keys=True,separators=(",",":"))
    usage_hash=hashlib.sha256(encoded.encode()).hexdigest()
    prior=session.execute(text("SELECT gateway_call_id,usage_hash FROM runtime_usage_corrections WHERE environment_id=:environment_id AND company_id=:company_id AND request_span_id=:id"),params(scope,id=run["request_span_id"])).mappings().first()
    if prior:
        if prior["gateway_call_id"]!=gateway_id or prior["usage_hash"]!=usage_hash:
            raise RuntimeDenied("conflicting_usage_correction")
        return False
    reference=f"gateway-final:{gateway_id}:span:{run['request_span_id']}"
    session.execute(text("INSERT INTO runtime_usage_corrections(environment_id,company_id,request_span_id,gateway_call_id,usage,usage_hash,source,correction_reference) VALUES(:environment_id,:company_id,:id,:gateway_id,CAST(:usage AS jsonb),:usage_hash,'gateway_final_response',:reference)"),params(scope,id=run["request_span_id"],gateway_id=gateway_id,usage=encoded,usage_hash=usage_hash,reference=reference))
    event(session,scope,run,"TOKEN_USAGE_RECORDED",usage_event_payload(run,gateway_id,usage,correction_reference=reference,execution_outcome_unchanged=True),f"runtime:call:{run['request_span_id']}:usage_correction")
    return True


def finish(factory,scope,run,outcome:CallOutcome):
    with transaction(factory,scope) as session:
        call=session.execute(text("SELECT status FROM model_calls WHERE environment_id=:environment_id AND company_id=:company_id AND id=:id FOR UPDATE"),params(scope,id=run["request_span_id"])).scalar_one()
        if call != "dispatched":
            # Keep adapter-sourced late usage, but never overwrite a fenced outcome or replay it.
            if outcome.usage is not None:
                record_usage_correction(session,scope,run,outcome)
            return
        if outcome.usage is not None:
            try:
                checked_usage=_validated_usage(outcome.usage)
            except RuntimeDenied:
                checked_usage=None
            outcome=CallOutcome(outcome.status,outcome.reason,outcome.output,outcome.gateway_call_id,checked_usage)
        stopped=session.execute(text("SELECT stop_requested FROM runtime_runs WHERE environment_id=:environment_id AND company_id=:company_id AND id=:id"),params(scope,id=run["id"])).scalar_one()
        if stopped and outcome.status == "completed":
            outcome=CallOutcome("unknown","stop_raced_with_response",gateway_call_id=outcome.gateway_call_id,usage=outcome.usage)
        usage=json.dumps(outcome.usage) if outcome.usage is not None else None
        if outcome.usage is not None:
            event(session,scope,run,"TOKEN_USAGE_RECORDED",usage_event_payload(run,outcome.gateway_call_id,outcome.usage),f"runtime:call:{run['request_span_id']}:usage_final")
        session.execute(text("UPDATE model_calls SET status=:status,reason=:reason,gateway_call_id=:gateway_call_id,usage=CAST(:usage AS jsonb),usage_provenance=:provenance,finished_at=CURRENT_TIMESTAMP WHERE environment_id=:environment_id AND company_id=:company_id AND id=:id"),params(scope,id=run["request_span_id"],status=outcome.status,reason=outcome.reason,gateway_call_id=outcome.gateway_call_id,usage=usage,provenance="gateway_final_response" if outcome.usage is not None else "unknown"))
        if outcome.status != "unknown":
            session.execute(text("UPDATE runtime_dispatch_guard SET request_span_id=NULL,environment_id=NULL,company_id=NULL WHERE id=1 AND request_span_id=:id"),{"id":run["request_span_id"]})
        target={"completed":"completed","failed":"failed","unknown":"interrupted","rate_limited":"failed"}[outcome.status]
        if outcome.status=="rate_limited" and not stopped and run["attempt"]<=run["max_requeues"]:
            target="queued"
            session.execute(text("UPDATE runtime_runs SET available_at=:available WHERE environment_id=:environment_id AND company_id=:company_id AND id=:id"),params(scope,id=run["id"],available=datetime.now(UTC)+timedelta(seconds=(1,3)[run["attempt"]-1])))
        output=redact_text(outcome.output) if outcome.output is not None else None
        artifact_id=None
        if target=="completed":
            artifact_id=uuid4()
            encoded=output.encode()
            session.execute(text("""INSERT INTO artifacts(id,environment_id,company_id,task_id,run_id,storage_key,sha256,mime_type,size_bytes,sensitivity)
              VALUES(:artifact_id,:environment_id,:company_id,:task_id,:id,:storage_key,:sha,'text/plain; charset=utf-8',:size,'internal')"""),params(scope,id=run["id"],task_id=run["task_id"],artifact_id=artifact_id,storage_key=f"db/runtime/{run['id']}/{artifact_id}",sha=hashlib.sha256(encoded).hexdigest(),size=len(encoded)))
        session.execute(text("UPDATE runtime_runs SET output=:output,artifact_id=:artifact_id,outcome=:reason,usage=CAST(:usage AS jsonb) WHERE environment_id=:environment_id AND company_id=:company_id AND id=:id"),params(scope,id=run["id"],output=output,artifact_id=artifact_id,reason=outcome.reason,usage=usage))
        change_state(session,scope,run,target,outcome.reason)
        if target=="completed":
            change_task(session,scope,run,"reviewing","output_ready_for_review_not_accepted")
        elif target in ("failed","interrupted"):
            change_task(session,scope,run,"blocked",outcome.reason)
        checkpoint(session,scope,run,"response_or_unknown",{"status":target,"request_span_id":str(run["request_span_id"]),"replay_allowed":False,"artifact_id":str(artifact_id) if artifact_id else None})
        event(session,scope,run,"LLM_CALL_COMPLETED" if target=="completed" else "LLM_CALL_FAILED",{"request_span_id":str(run["request_span_id"]),"gateway_call_id":outcome.gateway_call_id,"outcome":outcome.status,"reason":outcome.reason,"usage":outcome.usage,"usage_provenance":"gateway_final_response" if outcome.usage is not None else "unknown","cost_basis":"unknown"},f"runtime:call:{run['request_span_id']}:finished")


def recover_expired(factory,scope):
    with transaction(factory,scope) as session:
        rows=session.execute(text("""SELECT r.*,c.id AS request_span_id FROM runtime_runs r JOIN model_calls c ON c.environment_id=r.environment_id AND c.company_id=r.company_id AND c.run_id=r.id WHERE r.environment_id=:environment_id AND r.company_id=:company_id AND c.status='dispatched' AND c.lease_until<CURRENT_TIMESTAMP FOR UPDATE OF c,r"""),params(scope)).mappings().all()
        for run in rows:
            session.execute(text("UPDATE model_calls SET status='unknown',reason='worker_lease_expired',finished_at=CURRENT_TIMESTAMP WHERE environment_id=:environment_id AND company_id=:company_id AND id=:id"),params(scope,id=run["request_span_id"]))
            session.execute(text("UPDATE runtime_runs SET outcome='worker_lease_expired' WHERE environment_id=:environment_id AND company_id=:company_id AND id=:id"),params(scope,id=run["id"]))
            change_state(session,scope,run,"interrupted","worker_lease_expired")
            change_task(session,scope,run,"blocked","worker_lease_expired")
            checkpoint(session,scope,run,"interrupted_unknown",{"request_span_id":str(run["request_span_id"]),"replay_allowed":False})
            event(session,scope,run,"LLM_CALL_FAILED",{"request_span_id":str(run["request_span_id"]),"outcome":"unknown","reason":"worker_lease_expired"},f"runtime:call:{run['request_span_id']}:finished")
        return len(rows)


def heartbeat(factory,scope,run):
    with transaction(factory,scope) as session:
        session.execute(text("UPDATE model_calls SET heartbeat_at=CURRENT_TIMESTAMP WHERE environment_id=:environment_id AND company_id=:company_id AND id=:id AND status='dispatched'"),params(scope,id=run["request_span_id"]))
