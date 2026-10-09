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
