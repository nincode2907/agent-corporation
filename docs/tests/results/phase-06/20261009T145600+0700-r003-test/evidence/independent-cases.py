import os
from uuid import uuid4
from sqlalchemy import create_engine,text
from fastapi.testclient import TestClient
from agent_corporation_api.main import app

def test_real_pg_owner_auth_profile_scope_csrf_expiry_logout():
    admin=create_engine(os.environ['MIGRATION_DATABASE_URL'])
    env,company,other=uuid4(),uuid4(),uuid4()
    with admin.begin() as c:
        c.execute(text("INSERT INTO environments(id,name,kind) VALUES(:env,'independent-qa067','demo')"),{'env':env})
        c.execute(text("INSERT INTO companies(id,environment_id,name) VALUES(:company,:env,'qa067-authorized'),(:other,:env,'qa067-denied')"),locals())
        c.execute(text("INSERT INTO owner_scopes VALUES('owner-local',:env,:company)"),locals())
    client=TestClient(app,base_url='http://127.0.0.1:15501')
    origin={'Origin':'http://127.0.0.1:15500'}
    secret=Path(os.environ['OWNER_SECRET_PATH']).read_text()
    assert client.get('/api/v1/events').status_code==401
    assert client.get('/api/v1/runtime/status').status_code==401
    bad=client.post('/api/v1/owner/login',json={'secret':secret,'environment_id':str(env),'company_id':str(other)},headers=origin)
    assert bad.status_code==403
    login=client.post('/api/v1/owner/login',json={'secret':secret,'environment_id':str(env),'company_id':str(company)},headers=origin)
    assert login.status_code==200,login.text
    assert 'HttpOnly' in login.headers['set-cookie'] and 'SameSite=strict' in login.headers['set-cookie']
    headers={**origin,'X-CSRF-Token':login.json()['csrf_token']}
    sessionid=login.json()['session_id']
    with admin.connect() as c:
        row=c.execute(text('SELECT token_hash,csrf_hash FROM owner_sessions WHERE id=:id'),{'id':sessionid}).one()
        assert row[0]!=client.cookies['ac_owner_session'] and row[1]!=headers['X-CSRF-Token']
    profile={'model':'fixture-model','reasoning_effort':'low','fallback_models':[],'expected_version':0}
    assert client.put('/api/v1/owner/profile',json=profile,headers=origin).status_code==403
    assert client.put('/api/v1/owner/profile',json=profile,headers=headers).status_code==200
    assert client.put('/api/v1/owner/profile',json=profile,headers=headers).status_code==409
    assert client.get('/api/v1/owner/profile').json()['version']==1
    page=client.get('/api/v1/events').json()
    assert len(page['events'])==1 and page['events'][0]['event_type']=='OWNER_MODEL_PROFILE_UPDATED'
    assert client.get('/api/v1/events',params={'cursor':page['cursor']}).json()['events']==[]
    assert client.get('/api/v1/events',params={'cursor':'invalid'}).status_code==400
    assert client.get('/api/v1/events/stream',params={'cursor':'a'},headers={'Last-Event-ID':'b'}).status_code==400
    status=client.get('/api/v1/runtime/status')
    assert status.status_code==200 and status.json()['cg01']['allowed'] is False and status.json()['inference_grants']==0
    with admin.begin() as c:
        c.execute(text("UPDATE owner_sessions SET expires_at=CURRENT_TIMESTAMP-interval '1 second' WHERE id=:id"),{'id':sessionid})
    assert client.get('/api/v1/owner/session').status_code==401
    login=client.post('/api/v1/owner/login',json={'secret':secret,'environment_id':str(env),'company_id':str(company)},headers=origin)
    assert login.status_code==200
    headers={**origin,'X-CSRF-Token':login.json()['csrf_token']}
    assert client.post('/api/v1/owner/logout',headers=headers).status_code==200
    assert client.get('/api/v1/owner/session').status_code==401
    with admin.begin() as c:
        for table in ('owner_sessions','owner_model_profiles','owner_scopes','outbox_events','events','event_stream_counters','companies'):
            c.execute(text(f'DELETE FROM {table} WHERE environment_id=:env'),{'env':env})
        c.execute(text('DELETE FROM environments WHERE id=:env'),{'env':env})
    admin.dispose()
from pathlib import Path

from datetime import UTC,datetime,timedelta
from sqlalchemy.orm import sessionmaker
from agent_corporation_api.modules.execution import service,gates
from agent_corporation_api.modules.execution.gateway import CallOutcome
from agent_corporation_api.modules.observability.scope import CompanyScope

def test_unknown_usage_retains_same_grant_reservation():
    admin=create_engine(os.environ['MIGRATION_DATABASE_URL'])
    factory=sessionmaker(create_engine(os.environ['DATABASE_URL']),expire_on_commit=False)
    scope=CompanyScope(uuid4(),uuid4())
    with admin.begin() as c:
        c.execute(text("INSERT INTO environments(id,name,kind) VALUES(:env,'independent-usage','demo')"),{'env':scope.environment_id})
        c.execute(text("INSERT INTO companies(id,environment_id,name) VALUES(:id,:env,'independent-usage')"),{'env':scope.environment_id,'id':scope.company_id})
    grant=service.grant_create(factory,scope,'fixture-owner',{'phase':'06','batch_id':'independent-fixture','purpose':'fake-only','model':'fixture-model','effort':'low','max_requests':2,'max_concurrency':1,'timeout_seconds':1,'max_requeues':0,'expires_at':datetime.now(UTC)+timedelta(minutes=1)})
    spec={k:grant[k] for k in ('phase','batch_id','purpose','model','effort')}
    spec.update(grant_id=grant['id'],input_text='fake input',idempotency_key=uuid4())
    service.run_create(factory,scope,'fixture-owner',spec)
    run=service.reserve_next(factory,scope)
    service.finish(factory,scope,run,CallOutcome('completed','fixture-final','fixture-output',gateway_call_id='qa-fixture',usage=None))
    service.run_create(factory,scope,'fixture-owner',{**spec,'idempotency_key':uuid4()})
    assert service.reserve_next(factory,scope) is None,'Missing usage must retain unresolved reservation; second same-grant dispatch was allowed'

def test_cg01_json_list_fails_closed(tmp_path):
    gateway=tmp_path/'gateway'
    for name in gates.FILES:
        p=gateway/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text('fixture only')
    proof=tmp_path/'proof.json';proof.write_text('[]');proof.chmod(0o600)
    assert gates.check_gate(proof,gateway,base_url='http://127.0.0.1:1')['allowed'] is False

import pytest
@pytest.fixture(autouse=True)
def clean_own_negative_cases():
    yield
    admin=create_engine(os.environ['MIGRATION_DATABASE_URL'])
    with admin.begin() as c:
        ids=c.execute(text("SELECT id FROM environments WHERE name IN ('independent-usage','independent-qa067','independent-stream','independent-crash')")).scalars().all()
        for env in ids:
            c.execute(text('UPDATE runtime_dispatch_guard SET request_span_id=NULL,environment_id=NULL,company_id=NULL WHERE environment_id=:env'),{'env':env})
            for table in ('runtime_usage_corrections','model_calls','runtime_runs','inference_grants','owner_sessions','owner_model_profiles','owner_scopes','outbox_events','events','artifacts','checkpoints','run_execution_state','runs','task_execution_state','task_revisions','work_orders','event_stream_counters','companies'):
                c.execute(text(f'DELETE FROM {table} WHERE environment_id=:env'),{'env':env})
            c.execute(text('DELETE FROM environments WHERE id=:env'),{'env':env})
    admin.dispose()

import socket,threading,time,json,httpx,uvicorn
from agent_corporation_api.modules.governance import auth

def test_actual_http_sse_reconnect_logout_no_duplicate_or_raw_content(monkeypatch):
    admin=create_engine(os.environ['MIGRATION_DATABASE_URL'])
    env,company=uuid4(),uuid4()
    with admin.begin() as c:
        c.execute(text("INSERT INTO environments(id,name,kind) VALUES(:env,'independent-stream','demo')"),{'env':env})
        c.execute(text("INSERT INTO companies(id,environment_id,name) VALUES(:company,:env,'independent-stream')"),locals())
        c.execute(text("INSERT INTO owner_scopes VALUES('owner-local',:env,:company)"),locals())
    sock=socket.socket();sock.bind(('127.0.0.1',0));sock.listen(128)
    origin='http://127.0.0.1:'+str(sock.getsockname()[1])
    monkeypatch.setattr(auth,'ALLOWED_ORIGINS',auth.ALLOWED_ORIGINS|{origin})
    server=uvicorn.Server(uvicorn.Config(app,log_level='error',lifespan='off'))
    thread=threading.Thread(target=lambda:server.run(sockets=[sock]),daemon=True);thread.start()
    for _ in range(100):
        if server.started:break
        time.sleep(.01)
    assert server.started
    try:
        with httpx.Client(base_url=origin,timeout=5) as client:
            login=client.post('/api/v1/owner/login',headers={'Origin':origin},json={'secret':Path(os.environ['OWNER_SECRET_PATH']).read_text(),'environment_id':str(env),'company_id':str(company)})
            assert login.status_code==200
            headers={'Origin':origin,'X-CSRF-Token':login.json()['csrf_token']}
            body={'model':'fixture-model','reasoning_effort':'low','expected_version':0,'fallback_models':[]}
            assert client.put('/api/v1/owner/profile',json=body,headers=headers).status_code==200
            def domain(lines):
                kind=None
                for line in lines:
                    if line.startswith('event: '):kind=line[7:]
                    if line.startswith('data: ') and kind=='domain':return json.loads(line[6:])
                raise AssertionError('SSE no domain frame')
            with client.stream('GET','/api/v1/events/stream') as stream:
                assert stream.status_code==200
                first=domain(stream.iter_lines())
                assert first['stream_seq']==1
            assert client.put('/api/v1/owner/profile',json={**body,'expected_version':1},headers=headers).status_code==200
            with client.stream('GET','/api/v1/events/stream',headers={'Last-Event-ID':first['cursor']}) as stream:
                assert stream.status_code==200
                lines=stream.iter_lines();second=domain(lines)
                assert second['stream_seq']==2 and second['event_id']!=first['event_id']
                with httpx.Client(base_url=origin,cookies=client.cookies,timeout=5) as control:
                    assert control.post('/api/v1/owner/logout',headers=headers).status_code==200
                assert any(line=='event: auth-expired' for line in lines)
            assert client.get('/api/v1/events',params={'cursor':second['cursor']}).status_code==401
            Path('/private/tmp/ac067-sse-observed.json').write_text(json.dumps({'first_id':first['event_id'],'second_id':second['event_id'],'sequences':[first['stream_seq'],second['stream_seq']],'reconnect_dedup':True,'logout_stream_auth_expired':True,'fake_transport_only':True}))
    finally:
        server.should_exit=True;thread.join(5);sock.close();admin.dispose()

import subprocess,sys,signal

def test_disposable_worker_sigkill_recovery_never_replays_model_attempt():
    admin=create_engine(os.environ['MIGRATION_DATABASE_URL'])
    factory=sessionmaker(create_engine(os.environ['DATABASE_URL']),expire_on_commit=False)
    scope=CompanyScope(uuid4(),uuid4())
    with admin.begin() as c:
        c.execute(text("INSERT INTO environments(id,name,kind) VALUES(:env,'independent-crash','demo')"),{'env':scope.environment_id})
        c.execute(text("INSERT INTO companies(id,environment_id,name) VALUES(:id,:env,'independent-crash')"),{'env':scope.environment_id,'id':scope.company_id})
    spec={'phase':'07','batch_id':'independent-crash-fixture','purpose':'fake-only','model':'fixture-model','effort':'low','max_requests':2,'max_concurrency':1,'timeout_seconds':120,'max_requeues':0,'expires_at':datetime.now(UTC)+timedelta(minutes=1)}
    grant=service.grant_create(factory,scope,'fixture-owner',spec)
    run_spec={k:grant[k] for k in ('phase','batch_id','purpose','model','effort')}
    run_id=service.run_create(factory,scope,'fixture-owner',{**run_spec,'grant_id':grant['id'],'input_text':'fake trusted crash text','idempotency_key':uuid4()})
    code="""import asyncio,sys
from uuid import UUID
from agent_corporation_api.settings import Settings
Settings.model_config['env_file']=None
from agent_corporation_api.database import get_session_factory
from agent_corporation_api.modules.observability.scope import CompanyScope
from agent_corporation_api.modules.execution import service,worker
factory=get_session_factory()
scope=CompanyScope(UUID(sys.argv[1]),UUID(sys.argv[2]))
run=service.reserve_next(factory,scope)
async def fake(*args):
 print('QA_FAKE_TRANSPORT_WAITING',flush=True)
 await asyncio.sleep(120)
asyncio.run(worker.execute_reserved(factory,scope,run,'http://127.0.0.1:1',None,fake))
"""
    proc=subprocess.Popen([sys.executable,'-c',code,str(scope.environment_id),str(scope.company_id)],stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
    try:
        assert proc.stdout.readline().strip()=='QA_FAKE_TRANSPORT_WAITING'
        proc.kill();proc.wait(timeout=5)
        assert proc.returncode==-signal.SIGKILL
        with admin.begin() as c:
            call=c.execute(text('SELECT id FROM model_calls WHERE run_id=:id'),{'id':run_id}).scalar_one()
            c.execute(text("UPDATE model_calls SET lease_until=CURRENT_TIMESTAMP-interval '1 second' WHERE id=:id"),{'id':call})
        assert service.recover_expired(factory,scope)==1
        assert service.recover_expired(factory,scope)==0
        assert service.reserve_next(factory,scope) is None
        result=service.run_get(factory,scope,run_id)
        assert result['status']=='interrupted' and result['output'] is None
        with admin.connect() as c:
            assert c.execute(text('SELECT count(*) FROM model_calls WHERE run_id=:id'),{'id':run_id}).scalar_one()==1
            assert c.execute(text('SELECT status FROM model_calls WHERE run_id=:id'),{'id':run_id}).scalar_one()=='unknown'
        Path('/private/tmp/ac067-crash-observed.json').write_text(json.dumps({'worker_pid':proc.pid,'signal':'SIGKILL','only_disposable_process':True,'outcome':'unknown','attempt_count':1,'recovered_once':True,'actual_gateway_calls':0,'run_id':str(run_id)}))
    finally:
        if proc.poll() is None:proc.kill();proc.wait(timeout=5)
        factory.kw['bind'].dispose();admin.dispose()
