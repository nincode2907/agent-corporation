import sys,json,tempfile
from pathlib import Path
from uuid import uuid4
sys.path.insert(0,str(Path('apps/api/src').resolve()))
from agent_corporation_api import settings
from agent_corporation_api.modules.codex_gateway.adapter import ProbeSettings,probe_gateway
probe=probe_gateway(ProbeSettings())
print('LIVE_PROBE',json.dumps(probe,ensure_ascii=False))
with tempfile.TemporaryDirectory(prefix='ac-p05-r004-canary-') as temp:
 secret=Path(temp)/'owner-secret';secret.write_text('fixture-owner-canary-'+'a'*64);secret.chmod(0o600)
 settings.get_settings=lambda:settings.Settings(_env_file=None,database_url='postgresql+psycopg://agent_corporation_app:fixture_only_app@127.0.0.1:15591/qa_p05',migration_database_url='postgresql+psycopg://qa_owner:fixture_only_p05@127.0.0.1:15591/qa_p05',app_database_password='fixture_only_app',owner_secret_path=secret)
 from sqlalchemy import create_engine,text
 admin=create_engine(settings.get_settings().migration_database_url)
 env,company=uuid4(),uuid4()
 with admin.begin() as con:
  con.execute(text("INSERT INTO environments(id,name,kind) VALUES(:env,'P05 r004 isolated profile','demo')"),{'env':env})
  con.execute(text("INSERT INTO companies(id,environment_id,name) VALUES(:company,:env,'Profile fixture')"),{'env':env,'company':company})
  con.execute(text("INSERT INTO owner_scopes(owner_id,environment_id,company_id) VALUES('owner-local',:env,:company)"),{'env':env,'company':company})
 from fastapi import FastAPI
 from fastapi.testclient import TestClient
 from agent_corporation_api.modules.governance import auth_router
 app=FastAPI();app.include_router(auth_router.router)
 client=TestClient(app,base_url='http://127.0.0.1:15501');headers={'Origin':'http://127.0.0.1:15500'}
 body={'model':'not-in-catalog-p05-r004','reasoning_effort':'low','fallback_models':[],'expected_version':0}
 deny=client.put('/api/v1/owner/profile',json=body,headers={**headers,'X-Actor':'agent','X-Owner':'true'})
 assert deny.status_code==401
 print('AGENT_SPOOFED_FLAGS_PUT',deny.status_code)
 logged=client.post('/api/v1/owner/login',json={'secret':secret.read_text(),'environment_id':str(env),'company_id':str(company)},headers=headers)
 assert logged.status_code==200
 headers['X-CSRF-Token']=logged.json()['csrf_token']
 csrf=client.put('/api/v1/owner/profile',json=body,headers={'Origin':headers['Origin']})
 assert csrf.status_code==403
 print('OWNER_MISSING_CSRF_PUT',csrf.status_code)
 body['model']=probe['models'][0] if probe['models'] else 'catalog-fixture-model'
 saved=client.put('/api/v1/owner/profile',json=body,headers=headers)
 assert saved.status_code==200
 print('OWNER_VALID_PROFILE_PUT',saved.status_code,json.dumps(saved.json()))
 stale=client.put('/api/v1/owner/profile',json=body,headers=headers)
 assert stale.status_code==409
 print('STALE_VERSION_PUT',stale.status_code)
 body['expected_version']=1;body['model']='not-in-catalog-p05-r004'
 unsupported=client.put('/api/v1/owner/profile',json=body,headers=headers)
 print('UNSUPPORTED_MODEL_PUT',unsupported.status_code,json.dumps(unsupported.json()))
 assert unsupported.status_code==200 and unsupported.json()['model'] not in probe['models']
 read=client.get('/api/v1/owner/profile');assert read.json()['model']==body['model']
 print('UNSUPPORTED_MODEL_PERSISTED_READBACK',json.dumps(read.json()))
 with admin.connect() as con:
  rows=con.execute(text("SELECT event_type,payload FROM events WHERE environment_id=:env ORDER BY stream_seq"),{'env':env}).mappings().all()
  print('OWNER_AUDIT_EVENTS',json.dumps([dict(r) for r in rows]))
 body['expected_version']=2;body['reasoning_effort']='max'
 maxresult=client.put('/api/v1/owner/profile',json=body,headers=headers)
 print('GATEWAY_SCHEMA_MAX_APP_PROFILE',maxresult.status_code)
 body['reasoning_effort']='low';body['fallback_models']=['duplicate','duplicate']
 duplicate=client.put('/api/v1/owner/profile',json=body,headers=headers);assert duplicate.status_code==422
 print('DUPLICATE_FALLBACK',duplicate.status_code)
 from agent_corporation_api.modules.execution.gateway import parse_response
 for code in (409,429,502,504):
  outcome=parse_response(code,{},b'{}');print('HTTP_OUTCOME',code,outcome.status,outcome.reason)
 print('ISOLATED_PROFILE_SCOPE',str(env),str(company),'destroyed with disposable container after evidence collection')
