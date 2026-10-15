from __future__ import annotations

import hashlib
import json
from datetime import UTC, datetime, timedelta
from uuid import uuid4

from sqlalchemy import text

from ..demo.factory import DEMO_SCOPE
from ..execution.service import RuntimeDenied, params, transaction
from ..observability.events import append_event
from ..observability.redaction import redact_text

POLICY_VERSION = 1
POLICY = {'mode': 'development-playground', 'verified': False, 'policy_version': POLICY_VERSION,
          'tools': False, 'network_tools': False, 'fallback': False, 'max_requeues': 0, 'max_concurrency': 1}
TERMINAL = {'completed', 'failed', 'cancelled', 'unknown'}


def gate(settings, scope):
    from ..codex_gateway.adapter import _validated_base_url
    if scope != DEMO_SCOPE:
        raise RuntimeDenied('playground_demo_only')
    try:
        _validated_base_url(settings.codex_server_base_url)
    except ValueError:
        raise RuntimeDenied('playground_local_gateway_required') from None
    return dict(POLICY)


def fingerprint(spec):
    return hashlib.sha256(json.dumps(spec, sort_keys=True, default=str).encode()).hexdigest()


def emit(db, scope, session_id, kind, *, turn_id=None, **payload):
    append_event(db, scope=scope, event_type='PLAYGROUND_' + kind, task_id=None, run_id=None,
                 correlation_id=session_id, parent_event_id=None, source='app',
                 actor={'kind': 'system', 'id': 'development-playground'}, sensitivity='internal',
                 payload={'session_id': str(session_id), 'turn_id': str(turn_id) if turn_id else None, **payload},
                 evidence_refs=[], dedup_key=f'playground:{session_id}:{turn_id}:{kind}:{uuid4()}')


def session_row(db, scope, session_id):
    row = db.execute(text('SELECT * FROM playground_sessions WHERE environment_id=:environment_id AND company_id=:company_id AND id=:id FOR UPDATE'), params(scope, id=session_id)).mappings().first()
    if not row:
        raise RuntimeDenied('playground_session_not_found')
    return dict(row)


def validate_grant(row, now, auth_active=True):
    if row['revoked']:
        raise RuntimeDenied('playground_grant_revoked')
    if row['expires_at'] <= now:
        raise RuntimeDenied('playground_grant_expired')
    if not auth_active:
        raise RuntimeDenied('playground_owner_session_expired')
    if row['used_requests'] >= row['max_requests']:
        raise RuntimeDenied('playground_limit_exceeded')


def auth_active(db, row):
    return bool(db.execute(text('SELECT 1 FROM owner_sessions s JOIN owner_scopes o ON o.owner_id=s.owner_id AND o.environment_id=s.environment_id AND o.company_id=s.company_id WHERE s.id=:id AND s.owner_id=:owner AND s.environment_id=:env AND s.company_id=:company AND s.revoked_at IS NULL AND s.expires_at>CURRENT_TIMESTAMP'), {'id': row['owner_session_id'], 'owner': row['owner_id'], 'env': row['environment_id'], 'company': row['company_id']}).first())


def create_session(factory, scope, principal, spec):
    if scope != DEMO_SCOPE:
        raise RuntimeDenied('playground_demo_only')
    if spec.get('accept_demo_policy') is not True:
        raise RuntimeDenied('playground_policy_acceptance_required')
    digest = fingerprint(spec)
    with transaction(factory, scope) as db:
        prior = db.execute(text('SELECT * FROM playground_sessions WHERE environment_id=:environment_id AND company_id=:company_id AND creation_key=:key'), params(scope, key=spec['idempotency_key'])).mappings().first()
        if prior:
            if prior['request_hash'] != digest:
                raise RuntimeDenied('idempotency_payload_mismatch')
            return dict(prior)
        owner_expiry = db.execute(text('SELECT expires_at FROM owner_sessions WHERE id=:id AND owner_id=:owner AND environment_id=:environment_id AND company_id=:company_id AND revoked_at IS NULL AND expires_at>CURRENT_TIMESTAMP'), params(scope, id=principal.session_id, owner=principal.owner_id)).scalar_one_or_none()
        if owner_expiry is None:
            raise RuntimeDenied('playground_owner_session_expired')
        profile = db.execute(text('SELECT version,model,reasoning_effort FROM owner_model_profiles WHERE environment_id=:environment_id AND company_id=:company_id'), params(scope)).mappings().first()
        if not profile or not profile['model'] or profile['version'] != spec['profile_version']:
            raise RuntimeDenied('playground_save_profile_first')
        employee = db.execute(text("""SELECT e.id,v.version,v.profile FROM employees e JOIN LATERAL
            (SELECT version,profile FROM employee_versions v WHERE v.environment_id=e.environment_id AND v.company_id=e.company_id AND v.employee_id=e.id ORDER BY version DESC LIMIT 1) v ON true
            WHERE e.environment_id=:environment_id AND e.company_id=:company_id AND e.id=:id AND e.lifecycle IN ('active','probation')"""), params(scope, id=spec['employee_id'])).mappings().first()
        if not employee:
            raise RuntimeDenied('playground_employee_not_found')
        fixture = db.execute(text("SELECT 1 FROM environments WHERE id=:id AND kind='demo'"), {'id': scope.environment_id}).first()
        if not fixture:
            raise RuntimeDenied('playground_demo_only')
        employee_snapshot = {'id': str(employee['id']), 'version': employee['version'], 'display_name': str(employee['profile'].get('display_name', 'Nhân viên demo'))[:200], 'role': str(employee['profile'].get('role', ''))[:200]}
        ident = uuid4()
        values = params(scope, id=ident, owner=principal.owner_id, auth=principal.session_id,
                        key=spec['idempotency_key'], hash=digest, employee=json.dumps(employee_snapshot),
                        profile=json.dumps(dict(profile)), policy=json.dumps(POLICY), max=spec['max_requests'],
                        timeout=spec['timeout_seconds'], expiry=min(owner_expiry, datetime.now(UTC)+timedelta(minutes=spec['expires_in_minutes'])))
        db.execute(text('''INSERT INTO playground_sessions(environment_id,company_id,id,owner_id,owner_session_id,creation_key,request_hash,employee_snapshot,profile_snapshot,policy_snapshot,max_requests,timeout_seconds,expires_at)
            VALUES(:environment_id,:company_id,:id,:owner,:auth,:key,:hash,CAST(:employee AS jsonb),CAST(:profile AS jsonb),CAST(:policy AS jsonb),:max,:timeout,:expiry)'''), values)
        emit(db, scope, ident, 'GRANT_CREATED', model=profile['model'], profile_version=profile['version'], max_requests=spec['max_requests'], expires_at=values['expiry'].isoformat(), policy_version=POLICY_VERSION, verified=False)
        return session_row(db, scope, ident)


def list_sessions(factory, scope):
    with transaction(factory, scope, write=False) as db:
        return [dict(r) for r in db.execute(text('SELECT * FROM playground_sessions WHERE environment_id=:environment_id AND company_id=:company_id ORDER BY created_at DESC LIMIT 30'), params(scope)).mappings()]


def detail(factory, scope, ident):
    # Read-only: session_row takes row locks and is deliberately not used here.
    with transaction(factory, scope, write=False) as db:
        row = db.execute(text('SELECT * FROM playground_sessions WHERE environment_id=:environment_id AND company_id=:company_id AND id=:id'), params(scope, id=ident)).mappings().first()
        if not row:
            raise RuntimeDenied('playground_session_not_found')
        turns = db.execute(text('SELECT id,session_id,idempotency_key,input_text,output,status,stop_requested,outcome,usage,usage_provenance,cost_basis,gateway_call_id,profile_snapshot,created_at,dispatched_at,finished_at,heartbeat_at,resolved_at FROM playground_turns WHERE environment_id=:environment_id AND company_id=:company_id AND session_id=:id ORDER BY created_at,id'), params(scope, id=ident)).mappings().all()
        events = db.execute(text("SELECT event_id,event_type,stream_seq,recorded_at,payload FROM events WHERE environment_id=:environment_id AND company_id=:company_id AND correlation_id=:id ORDER BY stream_seq DESC LIMIT 100"), params(scope, id=ident)).mappings().all()
        return {'session': dict(row), 'turns': [dict(t) for t in turns], 'events': [dict(e) for e in reversed(events)], 'owner_session_active': auth_active(db, row)}


def build_history(employee, previous, input_text):
    system = {'role': 'system', 'content': 'Development Playground: trò chuyện văn bản với nhân viên demo ' + json.dumps(employee, ensure_ascii=False) + '. Không tools, file, terminal, network tools, deploy hay thay đổi công ty. Chỉ dùng nội dung hội thoại được gửi.'}
    pairs = [[{'role': 'user', 'content': p['input_text']}, {'role': 'assistant', 'content': p['output']}] for p in previous[-10:]]
    history = [system] + [message for pair in pairs for message in pair] + [{'role': 'user', 'content': input_text}]
    while len(json.dumps(history, ensure_ascii=False).encode()) > 48000 and pairs:
        pairs.pop(0)
        history = [system] + [message for pair in pairs for message in pair] + [{'role': 'user', 'content': input_text}]
    if len(json.dumps(history, ensure_ascii=False).encode()) > 48000:
        raise RuntimeDenied('playground_input_too_large')
    return history


def send(factory, scope, ident, spec):
    digest = fingerprint({'input_text': spec['input_text']})
    with transaction(factory, scope) as db:
        row = session_row(db, scope, ident)
        prior = db.execute(text('SELECT * FROM playground_turns WHERE environment_id=:environment_id AND company_id=:company_id AND session_id=:id AND idempotency_key=:key'), params(scope, id=ident, key=spec['idempotency_key'])).mappings().first()
        if prior:
            if prior['request_hash'] != digest:
                raise RuntimeDenied('idempotency_payload_mismatch')
            return dict(prior)
        validate_grant(row, datetime.now(UTC), auth_active(db, row))
        if db.execute(text("SELECT 1 FROM playground_turns WHERE environment_id=:environment_id AND company_id=:company_id AND session_id=:id AND (status IN ('queued','dispatched') OR (status='unknown' AND resolved_at IS NULL))"), params(scope, id=ident)).first():
            raise RuntimeDenied('playground_concurrency_or_unknown')
        previous = list(reversed(db.execute(text("SELECT input_text,output FROM playground_turns WHERE environment_id=:environment_id AND company_id=:company_id AND session_id=:id AND status='completed' ORDER BY created_at DESC,id DESC LIMIT 10"), params(scope, id=ident)).mappings().all()))
        history = build_history(row['employee_snapshot'], previous, spec['input_text'])
        turn = uuid4()
        db.execute(text('''INSERT INTO playground_turns(environment_id,company_id,id,session_id,idempotency_key,request_hash,input_text,history,profile_snapshot,policy_snapshot,status)
            VALUES(:environment_id,:company_id,:id,:sid,:key,:hash,:input,CAST(:history AS jsonb),CAST(:profile AS jsonb),CAST(:policy AS jsonb),'queued')'''), params(scope, id=turn, sid=ident, key=spec['idempotency_key'], hash=digest, input=spec['input_text'], history=json.dumps(history, ensure_ascii=False), profile=json.dumps(row['profile_snapshot']), policy=json.dumps(row['policy_snapshot'])))
        emit(db, scope, ident, 'TURN_QUEUED', turn_id=turn, profile_version=row['profile_snapshot']['version'])
        return {'id': turn, 'status': 'queued', 'session_id': ident}


def mark_terminal(db, scope, turn, status, reason):
    db.execute(text('UPDATE playground_turns SET status=:status,outcome=:reason,finished_at=CURRENT_TIMESTAMP WHERE environment_id=:environment_id AND company_id=:company_id AND id=:id'), params(scope, id=turn['id'], status=status, reason=reason))
    emit(db, scope, turn['session_id'], 'TURN_' + status.upper(), turn_id=turn['id'], outcome=reason, usage_provenance='unknown')


def stop(factory, scope, ident, *, revoke=False):
    with transaction(factory, scope) as db:
        session_row(db, scope, ident)
        if revoke:
            db.execute(text('UPDATE playground_sessions SET revoked=true WHERE environment_id=:environment_id AND company_id=:company_id AND id=:id'), params(scope, id=ident))
        for turn in db.execute(text("SELECT * FROM playground_turns WHERE environment_id=:environment_id AND company_id=:company_id AND session_id=:id AND status IN ('queued','dispatched')"), params(scope, id=ident)).mappings():
            db.execute(text('UPDATE playground_turns SET stop_requested=true WHERE environment_id=:environment_id AND company_id=:company_id AND id=:id'), params(scope, id=turn['id']))
            if turn['status'] == 'queued':
                mark_terminal(db, scope, turn, 'cancelled', 'stop_before_dispatch')
        emit(db, scope, ident, 'GRANT_REVOKED' if revoke else 'STOP_REQUESTED')


def recover(factory, scope):
    with transaction(factory, scope) as db:
        rows = db.execute(text("SELECT * FROM playground_turns WHERE environment_id=:environment_id AND company_id=:company_id AND status='dispatched' AND lease_until<CURRENT_TIMESTAMP"), params(scope)).mappings().all()
        for row in rows:
            mark_terminal(db, scope, row, 'unknown', 'worker_lease_expired_no_replay')
        # Keep the global guard occupied until explicit Owner reconciliation.
        return len(rows)


def reserve(factory, scope):
    with transaction(factory, scope) as db:
        if db.execute(text('SELECT request_span_id FROM runtime_dispatch_guard WHERE id=1')).scalar_one() is not None:
            return None
        turn = db.execute(text("SELECT * FROM playground_turns WHERE environment_id=:environment_id AND company_id=:company_id AND status='queued' ORDER BY created_at,id LIMIT 1 FOR UPDATE"), params(scope)).mappings().first()
        if not turn:
            return None
        row = session_row(db, scope, turn['session_id'])
        try:
            validate_grant(row, datetime.now(UTC), auth_active(db, row))
        except RuntimeDenied as error:
            mark_terminal(db, scope, turn, 'cancelled', str(error))
            return None
        db.execute(text('UPDATE playground_sessions SET used_requests=used_requests+1 WHERE environment_id=:environment_id AND company_id=:company_id AND id=:id'), params(scope, id=row['id']))
        lease = datetime.now(UTC)+timedelta(seconds=row['timeout_seconds']+15)
        db.execute(text("UPDATE playground_turns SET status='dispatched',dispatched_at=CURRENT_TIMESTAMP,heartbeat_at=CURRENT_TIMESTAMP,lease_until=:lease WHERE environment_id=:environment_id AND company_id=:company_id AND id=:id"), params(scope, id=turn['id'], lease=lease))
        db.execute(text('UPDATE runtime_dispatch_guard SET request_span_id=:id,environment_id=:environment_id,company_id=:company_id WHERE id=1'), params(scope, id=turn['id']))
        emit(db, scope, row['id'], 'CALL_STARTED', turn_id=turn['id'], model=row['profile_snapshot']['model'], profile_version=row['profile_snapshot']['version'])
        return {**dict(turn), 'timeout_seconds': row['timeout_seconds']}


def should_stop(factory, scope, turn):
    with transaction(factory, scope, write=False) as db:
        row = db.execute(text('SELECT s.*,t.stop_requested FROM playground_sessions s JOIN playground_turns t ON t.environment_id=s.environment_id AND t.company_id=s.company_id AND t.session_id=s.id WHERE t.environment_id=:environment_id AND t.company_id=:company_id AND t.id=:id'), params(scope, id=turn['id'])).mappings().one()
        return row['stop_requested'] or row['revoked'] or row['expires_at'] <= datetime.now(UTC) or not auth_active(db, row)


def heartbeat(factory, scope, turn):
    with transaction(factory, scope, write=False) as db:
        db.execute(text("UPDATE playground_turns SET heartbeat_at=CURRENT_TIMESTAMP WHERE environment_id=:environment_id AND company_id=:company_id AND id=:id AND status='dispatched'"), params(scope, id=turn['id']))


def finish(factory, scope, turn, outcome):
    with transaction(factory, scope) as db:
        current = db.execute(text('SELECT * FROM playground_turns WHERE environment_id=:environment_id AND company_id=:company_id AND id=:id FOR UPDATE'), params(scope, id=turn['id'])).mappings().one()
        if current['status'] != 'dispatched':
            return  # Fence late completions after crash recovery.
        row = session_row(db, scope, turn['session_id'])
        stopped = current['stop_requested'] or row['revoked'] or row['expires_at'] <= datetime.now(UTC) or not auth_active(db, row)
        status = 'unknown' if stopped or outcome.status == 'unknown' else 'completed' if outcome.status == 'completed' else 'failed'
        reason = 'stop_or_expiry_after_dispatch' if stopped else outcome.reason
        db.execute(text('''UPDATE playground_turns SET status=:status,outcome=:reason,output=:output,usage=CAST(:usage AS jsonb),usage_provenance=:provenance,gateway_call_id=:gateway,finished_at=CURRENT_TIMESTAMP
            WHERE environment_id=:environment_id AND company_id=:company_id AND id=:id'''), params(scope, id=turn['id'], status=status, reason=reason, output=redact_text(outcome.output) if status == 'completed' and outcome.output else None, usage=json.dumps(outcome.usage) if outcome.usage is not None else None, provenance='gateway_final_response' if outcome.usage is not None else 'unknown', gateway=outcome.gateway_call_id))
        if status != 'unknown':
            db.execute(text('UPDATE runtime_dispatch_guard SET request_span_id=NULL,environment_id=NULL,company_id=NULL WHERE id=1 AND request_span_id=:id'), {'id': turn['id']})
        emit(db, scope, turn['session_id'], 'CALL_FINISHED', turn_id=turn['id'], status=status, outcome=reason, usage=outcome.usage, usage_provenance='gateway_final_response' if outcome.usage is not None else 'unknown', gateway_call_id=outcome.gateway_call_id)


def resolve_unknown(factory, scope, ident, turn_id):
    with transaction(factory, scope) as db:
        session_row(db, scope, ident)
        turn = db.execute(text("SELECT * FROM playground_turns WHERE environment_id=:environment_id AND company_id=:company_id AND session_id=:sid AND id=:id AND status='unknown' FOR UPDATE"), params(scope, sid=ident, id=turn_id)).mappings().first()
        if not turn:
            raise RuntimeDenied('playground_unknown_turn_not_found')
        if turn['resolved_at'] is None:
            db.execute(text('UPDATE playground_turns SET resolved_at=CURRENT_TIMESTAMP WHERE environment_id=:environment_id AND company_id=:company_id AND id=:id'), params(scope, id=turn_id))
            db.execute(text('UPDATE runtime_dispatch_guard SET request_span_id=NULL,environment_id=NULL,company_id=NULL WHERE id=1 AND request_span_id=:id'), {'id': turn_id})
            emit(db, scope, ident, 'UNKNOWN_ACKNOWLEDGED', turn_id=turn_id, usage_unchanged=True, request_not_refunded=True)
