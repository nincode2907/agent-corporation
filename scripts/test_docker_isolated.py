"""Exercise Compose with disposable volumes and synthetic credentials only.

Resolved operator config stays in memory; every environment value is replaced
before writing a temporary Compose file. No production ports or volumes are used.
"""
from __future__ import annotations

import json
from pathlib import Path
import subprocess
import tempfile
from uuid import uuid4

ROOT = Path(__file__).resolve().parents[1]


def main():
    project = "ac-docker-test-" + uuid4().hex[:10]
    raw = subprocess.run(["docker", "compose", "config", "--format", "json"], cwd=ROOT,
                         capture_output=True, text=True, check=True).stdout
    config = json.loads(raw)
    config["name"] = project
    config.pop("networks", None)
    config["services"].pop("worker", None)
    fixture_env = {
        "CODEX_SERVER_BASE_URL": "http://host.docker.internal:15600", "CODEX_SERVER_TRANSPORT": "docker-host",
        "CODEX_SERVER_API_KEY": "", "OWNER_SECRET_PATH": "/runtime-secrets/owner-secret",
        "RUNTIME_GATE_PATH": "/runtime-secrets/cg01-proof.json", "RUNTIME_GATEWAY_SOURCE_PATH": "/gateway-source",
        "RUNTIME_CG01_DEMO_TEST_OVERRIDE": "false", "PLAYGROUND_WORKER_ENABLED": "false",
        "APP_CONFIG_FILE": "/runtime-secrets/app.json",
    }
    with tempfile.TemporaryDirectory(prefix=project) as temporary:
        directory = Path(temporary)
        (directory / ".local").mkdir()
        owner = directory / ".local" / "owner-secret"
        owner.write_text("synthetic-owner-secret-" + "a" * 48)
        owner.chmod(0o600)
        for service_name, service in config["services"].items():
            for key in list(service):
                if service[key] is None:
                    del service[key]
            for key in ("build", "container_name", "ports", "networks"):
                service.pop(key, None)
            service["environment"] = {}
            if service_name in {"api", "migrate"}:
                service["environment"] = dict(fixture_env)
            if service_name == "migrate":
                service["environment"]["APP_CONFIG_FILE"] = "/database-secrets/migration.json"
            if service_name == "bootstrap":
                for mount in service["volumes"]:
                    if mount["target"] == "/operator":
                        mount["source"] = str(directory)
        for key in config.get("volumes", {}):
            config["volumes"][key] = {"name": project + "_" + key}
        path = directory / "compose.json"
        path.write_text(json.dumps(config))
        path.chmod(0o600)
        command = ["docker", "compose", "-p", project, "-f", str(path)]
        def run(*args, code=None):
            result = subprocess.run([*command, *args], input=code, text=True, capture_output=True, cwd=ROOT)
            if result.returncode:
                print(result.stdout[-4000:]); print(result.stderr[-4000:])
                raise RuntimeError("Isolated Docker command failed: " + " ".join(args[:3]))
            return result.stdout
        try:
            run("up", "--wait")
            print("PASS one-file startup with no .env: generated config + PostgreSQL + migration + API + Nginx")
            # A second up must reuse generated credentials, not reset PostgreSQL or Owner.
            fingerprint = "import hashlib,pathlib; print(hashlib.sha256(pathlib.Path('/runtime-secrets/owner-secret').read_bytes()+pathlib.Path('/runtime-secrets/app.json').read_bytes()).hexdigest())"
            before = run("exec", "-T", "api", "python", "-c", fingerprint)
            run("up", "--wait")
            assert before == run("exec", "-T", "api", "python", "-c", fingerprint)
            print("PASS repeated compose up preserves generated credentials and Owner")
            run("run", "--rm", "-T", "migrate", "python", "-c", "from sqlalchemy import create_engine; from sqlalchemy.orm import sessionmaker; from agent_corporation_api.settings import get_settings; from agent_corporation_api.database import get_session_factory; from agent_corporation_api.modules.demo.factory import ensure_demo_scope,reset_demo_dataset; s=get_settings(); ensure_demo_scope(sessionmaker(create_engine(s.migration_database_url))); reset_demo_dataset(get_session_factory()); print('Synthetic demo scope ready')")
            output = run("exec", "-T", "api", "python", "-", code=ISOLATED_HTTP_CHECKS)
            print(output.strip())
            run("restart", "api")
            run("exec", "-T", "api", "python", "-", code=ISOLATED_WAIT_READY)
            print(run("exec", "-T", "api", "python", "-", code=ISOLATED_RESTART_CHECK).strip())
            run("up", "-d", "--no-deps", "--force-recreate", "api")
            run("exec", "-T", "api", "python", "-", code=ISOLATED_WAIT_READY)
            run("exec", "-T", "api", "python", "-", code=ISOLATED_WAIT_READY.replace(
                "http://127.0.0.1:15501/api/v1/health/ready", "http://web:15500/api/v1/health/ready"))
            print("PASS API recreate: Nginx resolves current Docker service address")
            run("stop", "postgres")
            print(run("exec", "-T", "api", "python", "-", code=ISOLATED_DB_DOWN_CHECK).strip())
        finally:
            run("down", "--volumes", "--remove-orphans")
            print("CLEANUP: removed only disposable project " + project)


ISOLATED_HTTP_CHECKS = r'''
import http.client, json, os, time
from pathlib import Path
from agent_corporation_api.modules.demo.factory import DEMO_SCOPE
from agent_corporation_api.modules.governance.auth import read_owner_secret
from agent_corporation_api.database import get_session_factory
from agent_corporation_api.modules.observability.scope import set_company_scope
from sqlalchemy import text
headers = {'Host':'127.0.0.1:15500','Origin':'http://127.0.0.1:15500','Content-Type':'application/json'}
def request(method,path,body=None,extra=None):
    connection=http.client.HTTPConnection('web',15500,timeout=15)
    connection.request(method,path,json.dumps(body) if body is not None else None,{**headers,**(extra or {})})
    response=connection.getresponse(); data=response.read(); status=response.status; meta=response.getheaders(); connection.close()
    return status,data,meta
assert os.getuid()==1000
assert request('GET','/api/v1/health/ready')[0]==200
assert request('GET','/api/v1/owner/session')[0]==401
assert request('GET','/api/v1/owner/session',extra={'Origin':'http://evil.example'})[0]==403
body={'secret':read_owner_secret(),'environment_id':str(DEMO_SCOPE.environment_id),'company_id':str(DEMO_SCOPE.company_id)}
status,data,meta=request('POST','/api/v1/owner/login',body)
assert status==200,(status,data)
cookie=next(value for key,value in meta if key.lower()=='set-cookie').split(';')[0]
csrf=json.loads(data)['csrf_token']
assert request('GET','/api/v1/owner/session',extra={'Cookie':cookie})[0]==200
assert request('POST','/api/v1/owner/logout',extra={'Cookie':cookie})[0]==403
connection=http.client.HTTPConnection('web',15500,timeout=15)
start=time.monotonic()
connection.request('GET','/api/v1/events/stream',headers={**headers,'Cookie':cookie})
response=connection.getresponse()
assert response.status==200 and response.getheader('Content-Type').startswith('text/event-stream')
assert response.readline().startswith(b'id:')
assert time.monotonic()-start<5, 'Nginx buffered SSE'
connection.close()
with get_session_factory()() as db,db.begin():
    set_company_scope(db,DEMO_SCOPE)
    assert db.execute(text('SELECT count(*) FROM model_calls')).scalar_one()==0
    assert db.execute(text('SELECT count(*) FROM playground_turns')).scalar_one()==0
saved=Path('/app/storage/qa-session.json'); saved.write_text(json.dumps({'cookie':cookie,'csrf':csrf})); saved.chmod(0o600)
print('PASS nonroot UID1000 + Owner secret600 + login/session + Host/Origin/CSRF + SSE first frame<5s + zero model calls')
'''

ISOLATED_RESTART_CHECK = r'''
import http.client,json
from pathlib import Path
saved=Path('/app/storage/qa-session.json'); data=json.loads(saved.read_text())
headers={'Host':'127.0.0.1:15500','Origin':'http://127.0.0.1:15500','Cookie':data['cookie'],'X-CSRF-Token':data['csrf']}
for method,path,expected in [('GET','/api/v1/owner/session',200),('POST','/api/v1/owner/logout',200),('GET','/api/v1/owner/session',401)]:
    connection=http.client.HTTPConnection('web',15500,timeout=10); connection.request(method,path,headers=headers)
    response=connection.getresponse(); assert response.status==expected,(path,response.status); response.read(); connection.close()
saved.unlink()
print('PASS restart preserves Owner cookie, signing secret and database; authenticated logout revokes session')
'''

ISOLATED_WAIT_READY = r'''
import time, urllib.request, urllib.error
deadline=time.monotonic()+30
while time.monotonic()<deadline:
    try:
        if urllib.request.urlopen('http://127.0.0.1:15501/api/v1/health/ready',timeout=1).status==200:
            break
    except (urllib.error.URLError, OSError):
        pass
    time.sleep(.25)
else:
    raise RuntimeError('API readiness timed out after restart')
'''

ISOLATED_DB_DOWN_CHECK = r'''
import urllib.request,urllib.error
assert urllib.request.urlopen('http://127.0.0.1:15501/api/v1/health/live').status==200
try:
    urllib.request.urlopen('http://127.0.0.1:15501/api/v1/health/ready')
    raise AssertionError('Readiness must fail without PostgreSQL')
except urllib.error.HTTPError as error:
    assert error.code==503
print('PASS isolated PostgreSQL-down: liveness200/readiness503')
'''


if __name__ == "__main__":
    main()
