import sys,json,tempfile
from pathlib import Path
from uuid import uuid4
sys.path.insert(0,str(Path('apps/api/src').resolve()))
from agent_corporation_api import settings
from agent_corporation_api.modules.codex_gateway import adapter
print('LIVE_PROBE',json.dumps(adapter.probe_gateway(adapter.ProbeSettings()),ensure_ascii=False))
caps=adapter.profile_model_capabilities(adapter.ProbeSettings());print('LIVE_CAPABILITIES',json.dumps(caps));assert 'max' in caps['gpt-6.1-sol'] and 'ultra' in caps['gpt-6.1-sol'] and 'minimal' not in caps['gpt-6.1-sol']
with tempfile.TemporaryDirectory(prefix='ac-p05-r005-canary-') as temp:
 secret=Path(temp)/'owner-secret';secret.write_text('fixture-owner-canary-'+'a'*64);secret.chmod(0o600)
 def conf(base='http://127.0.0.1:15600'):
  return settings.Settings(_env_file=None,database_url='postgresql+psycopg://agent_corporation_app:fixture_only_app@127.0.0.1:15591/qa_p05',migration_database_url='postgresql+psycopg://qa_owner:fixture_only_p05@127.0.0.1:15591/qa_p05',app_database_password='fixture_only_app',owner_secret_path=secret,codex_server_base_url=base)
 settings.get_settings=conf
 from sqlalchemy import create_engine,text
 admin=create_engine(conf().migration_database_url);env,company=uuid4(),uuid4()
 with admin.begin() as con:
  con.execute(text("INSERT INTO environments(id,name,kind) VALUES(:env,'P05 r005 profile','demo')"),{'env':env})
  con.execute(text("INSERT INTO companies(id,environment_id,name) VALUES(:company,:env,'Profile retest')"),{'env':env,'company':company})
  con.execute(text("INSERT INTO owner_scopes(owner_id,environment_id,company_id) VALUES('owner-local',:env,:company)"),{'env':env,'company':company})
 from fastapi import FastAPI
 from fastapi.testclient import TestClient
 from agent_corporation_api.modules.governance import auth_router,profile
 app=FastAPI();app.include_router(auth_router.router)
 from agent_corporation_api.modules.codex_gateway.router import router
 app.include_router(router)
 client=TestClient(app,base_url='http://127.0.0.1:15501',raise_server_exceptions=False);headers={'Origin':'http://127.0.0.1:15500'}
 original=adapter._get_json;requests=[]
 def tracked(url,key):
  requests.append(url)
  return original(url,key)
 adapter._get_json=tracked
 body={'model':'gpt-6.1-sol','reasoning_effort':'low','fallback_models':[],'expected_version':0}
 denied=client.put('/api/v1/owner/profile',json=body,headers={**headers,'X-Actor':'agent','X-Owner':'true'});assert denied.status_code==401 and not requests
 print('AGENT_HEADER_SPOOF',denied.status_code,'metadata_calls',len(requests))
 login=client.post('/api/v1/owner/login',json={'secret':secret.read_text(),'environment_id':str(env),'company_id':str(company)},headers=headers);assert login.status_code==200
 headers['X-CSRF-Token']=login.json()['csrf_token']
 assert not requests
 missing=client.put('/api/v1/owner/profile',json=body,headers={'Origin':headers['Origin']});assert missing.status_code==403 and not requests;print('MISSING_CSRF',missing.status_code)
 assert client.get('/api/v1/owner/profile').json()['version']==0 and not requests;print('PROFILE_VIEW_INITIAL_METADATA_CALLS',len(requests))
 for effort,fallback in [('low',[]),('max',[]),('ultra',['gpt-6-astra'])]:
  body['reasoning_effort']=effort;body['fallback_models']=fallback
  requests.clear();r=client.put('/api/v1/owner/profile',json=body,headers=headers);assert r.status_code==200,r.text
  assert requests==['http://127.0.0.1:15600/v1/models','http://127.0.0.1:15600/api/models']
  body['expected_version']=r.json()['version'];print('SUPPORTED_PROFILE',json.dumps(r.json()),'metadata_GET_count',len(requests))
 final=client.get('/api/v1/owner/profile').json();assert final['version']==3
 def audits():
  with admin.connect() as con:return con.execute(text('SELECT count(*) FROM events WHERE environment_id=:env'),{'env':env}).scalar_one()
 before=audits();assert before==3
 for name,change in [('unknown-primary',{'model':'not-in-catalog-p05-r004'}),('unsupported-minimal',{'reasoning_effort':'minimal'}),('unknown-fallback',{'fallback_models':['not-in-catalog']}),('fallback-effort-mismatch',{'fallback_models':['gpt-6-luna']})]:
  r=client.put('/api/v1/owner/profile',json={**body,**change},headers=headers);assert r.status_code==422,(name,r.text)
  assert client.get('/api/v1/owner/profile').json()==final and audits()==before
  print('INVALID_PROFILE_PRESERVED',name,r.status_code,'version3/audit3')
 stale=client.put('/api/v1/owner/profile',json={**body,'expected_version':0},headers=headers);assert stale.status_code==409 and audits()==before;print('STALE_VERSION',stale.status_code)
 profile.get_settings=lambda:conf('http://127.0.0.1:15599')
 offline=client.put('/api/v1/owner/profile',json=body,headers=headers);assert offline.status_code==503 and audits()==before
 requests.clear();read=client.get('/api/v1/owner/profile');assert read.json()==final and not requests
 print('OFFLINE_SAVE_PRESERVED',offline.status_code,'GETprofileversion3/audit3','read_metadata_calls',len(requests))
 profile.get_settings=conf
 print('ISOLATED_SCOPE',str(env),str(company))
 # Original invalid UTF8 route reproduction, now expected no unhandled 500.
 class Response:
  status=200
  def __enter__(self):return self
  def __exit__(self,*args):return False
  def read(self,*args):return b'\xff'
 class Opener:
  def open(self,*args,**kwargs):return Response()
 old_opener=adapter.build_opener;adapter.build_opener=lambda *args:Opener()
 malformed=client.get('/api/v1/codex/probe');assert malformed.status_code==200 and malformed.json()['status']=='contract_mismatch'
 print('ORIGINAL_UTF8_REPRO_FIXED',malformed.status_code,malformed.json()['status'])
 adapter.build_opener=old_opener
 from agent_corporation_api.modules.execution.gates import check_gate
 print('CG01_ACTUAL',json.dumps(check_gate(Path('.local/cg01-proof.json'),Path('../codex-server'),base_url='http://127.0.0.1:15600')))
