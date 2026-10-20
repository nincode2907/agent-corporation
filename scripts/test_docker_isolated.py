"""Exercise Compose with disposable volumes and synthetic credentials only.

Resolved operator config stays in memory; every environment value is replaced
before writing a temporary Compose file. No production ports or volumes are used.
"""
from __future__ import annotations

import json
import os
import re
from pathlib import Path
import subprocess
import tempfile
from datetime import UTC, datetime
from uuid import uuid4

from test_playground_isolated import require_capacity, resource_preflight

ROOT = Path(__file__).resolve().parents[1]
DOCKER = ["rtk", "proxy", "docker"]


def main():
    project = "ac-docker-test-" + uuid4().hex[:10]
    evidence_dir = ROOT / "docs/reviews/infrastructure-fix-08-1/startup-smoke"
    evidence_dir.mkdir(parents=True, exist_ok=True)
    manifest = {"project": project, "started_at_utc": datetime.now(UTC).isoformat(),
                "preflight": None, "commands": [], "smoke_checks": "pending",
                "cleanup": {"status": "pending"}}
    run_dir = evidence_dir / project
    run_dir.mkdir(mode=0o700)
    run_dir.chmod(0o700)
    preflight = resource_preflight()
    manifest["preflight"] = preflight
    if preflight.get("classification") != "CAPACITY_CONFIRMED":
        manifest["status"] = "blocked"
        manifest["failure"] = "Docker VM capacity was not confirmed; smoke created no Compose resources"
        manifest["cleanup"] = {"status": "not_needed"}
        (run_dir / "run-manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
        return 2
    require_capacity(preflight)
    raw = subprocess.run([*DOCKER, "compose", "--profile", "setup", "config", "--format", "json"], cwd=ROOT,
                         capture_output=True, text=True, check=True).stdout
    config = json.loads(raw)
    config["name"] = project
    config.pop("networks", None)
    api_dependencies = set(config["services"]["api"].get("depends_on", {}))
    assert "bootstrap" not in api_dependencies and "migrate" not in api_dependencies, api_dependencies
    assert "worker" not in api_dependencies, api_dependencies
    assert "setup" in config["services"]["bootstrap"].get("profiles", [])
    assert "setup" in config["services"]["migrate"].get("profiles", [])
    runtime_profile_raw = subprocess.run([*DOCKER, "compose", "--profile", "runtime-worker", "config", "--format", "json"],
                                        cwd=ROOT, capture_output=True, text=True, check=True).stdout
    runtime_profile_config = json.loads(runtime_profile_raw)
    assert "runtime-worker" in runtime_profile_config["services"]["worker"].get("profiles", [])
    manifest["runtime_worker"] = {"compose_profile": "runtime-worker", "included_in_smoke": False,
                                  "api_dependency": False}
    for name in ("worker", "proof-admin"):
        config["services"].pop(name, None)
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
            for key in ("container_name", "ports", "networks"):
                service.pop(key, None)
            if service_name in {"bootstrap", "migrate", "api"}:
                service["image"] = project + "-api:isolated"
                service["profiles"] = []
            elif service_name == "web":
                service["image"] = project + "-web:isolated"
            if service_name == "api":
                service["volumes"] = [mount for mount in service.get("volumes", [])
                                      if not str(mount.get("target", "")).startswith("/gateway-source/")]
            limits = {
                "postgres": {"mem_limit": "512m", "memswap_limit": "768m", "cpus": 0.75, "pids_limit": 96},
                "api": {"mem_limit": "768m", "memswap_limit": "1g", "cpus": 0.75, "pids_limit": 128},
                "web": {"mem_limit": "192m", "memswap_limit": "256m", "cpus": 0.25, "pids_limit": 64},
            }
            service.update(limits.get(service_name, {}))
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
        command = [*DOCKER, "compose", "-p", project, "-f", str(path)]
        def run(*args, code=None, timeout=180):
            started = datetime.now(UTC).isoformat()
            result = subprocess.run([*command, *args], input=code, text=True, capture_output=True,
                                    cwd=ROOT, timeout=timeout)
            command_record = {"args": list(args), "started_at_utc": started,
                              "exit_code": result.returncode,
                              "stdout_chars": len(result.stdout),
                              "stderr_chars": len(result.stderr)}
            if args and args[0] == "run":
                safe_output = (result.stdout + result.stderr).replace(owner.read_text().strip(), "[REDACTED_OWNER_SECRET]")
                safe_output = re.sub(r"(postgres(?:ql)?(?:\+\w+)?://[^:/\s]+:)[^@/\s]+@",
                                     r"\1[REDACTED]@", safe_output, flags=re.IGNORECASE)
                command_record["sanitized_output_tail"] = safe_output[-6000:]
            manifest["commands"].append(command_record)
            if result.returncode:
                print(result.stdout[-4000:]); print(result.stderr[-4000:])
                manifest["failure"] = {"command": list(args), "exit_code": result.returncode}
                if args and args[0] == "up" and "api" in args:
                    logs = subprocess.run([*command, "logs", "--no-color", "--tail", "100", "api"],
                                          capture_output=True, text=True, cwd=ROOT, timeout=30)
                    api_log = logs.stdout + logs.stderr
                    api_log = api_log.replace(owner.read_text().strip(), "[REDACTED_OWNER_SECRET]")
                    (run_dir / "api-startup.log").write_text(api_log[-20000:], encoding="utf-8")
                    (run_dir / "api-startup.log").chmod(0o600)
                raise RuntimeError("Isolated Docker command failed: " + " ".join(args[:3]))
            return result.stdout
        try:
            run("build", "bootstrap", "migrate", "api", "web", timeout=900)
            run("run", "--rm", "--no-deps", "bootstrap")
            # A stale proof in the disposable runtime volume must survive a
            # normal bootstrap. It remains expired and the strict gate denies it.
            install_stale_proof = (
                "import json,os; from pathlib import Path; "
                "from agent_corporation_api.modules.execution.gates import FILES,gateway_fingerprint; "
                "root=Path('/runtime-secrets/test-gateway'); root.mkdir(exist_ok=True); "
                "[(root/name).parent.mkdir(parents=True,exist_ok=True) for name in FILES]; "
                "[(root/name).write_text('synthetic gateway fixture') for name in FILES]; "
                "proof={'gateway_base_url':'http://host.docker.internal:15600','gateway_transport':'docker-host',"
                "'expires_at':'2000-01-01T00:00:00+00:00','gateway_fingerprint':gateway_fingerprint(root),"
                "'evidence_refs':['synthetic-expired-fixture'],'isolation_verified':True,"
                "'privacy_retention_verified':True,'cancellation_verified':True}; "
                "p=Path('/runtime-secrets/cg01-proof.json'); p.write_text(json.dumps(proof)); p.chmod(0o600); os.chown(p,1000,1000)"
            )
            run("run", "--rm", "--no-deps", "bootstrap", "python", "-c",
                install_stale_proof)
            run("run", "--rm", "--no-deps", "bootstrap")
            proof_check = run("run", "--rm", "--no-deps", "api", "python", "-c",
                              "from pathlib import Path; from agent_corporation_api.modules.execution.gates import check_gate; p=Path('/runtime-secrets/cg01-proof.json'); assert p.exists(); print(check_gate(p,Path('/runtime-secrets/test-gateway'),base_url='http://host.docker.internal:15600',transport_mode='docker-host')['reason'])")
            assert "expired_metadata" in proof_check
            run("up", "-d", "--wait", "postgres")
            run("run", "--rm", "--no-deps", "migrate")
            migration_revision_probe = (
                "from agent_corporation_api.settings import get_settings; from sqlalchemy import create_engine,text; "
                "s=get_settings(); e=create_engine(s.migration_database_url); c=e.connect(); "
                "print('database='+c.execute(text('select current_database()')).scalar_one()); "
                "print('revision='+c.execute(text('select version_num from alembic_version')).scalar_one()); "
                "c.close(); e.dispose()"
            )
            migration_output = run("run", "--rm", "--no-deps", "migrate", "python", "-c", migration_revision_probe)
            manifest["migration"] = {"exit_code": 0, "output": migration_output.strip()}
            schema_probe = """from agent_corporation_api.database import missing_schema_elements,REQUIRED_SCHEMA_COLUMNS
from agent_corporation_api.settings import get_settings
from sqlalchemy import create_engine,text
s=get_settings(); e=create_engine(s.database_url); c=e.connect()
print('database='+c.execute(text('select current_database()')).scalar_one())
print('role='+c.execute(text('select current_user')).scalar_one())
query=\"select relation.relname,attribute.attname from pg_catalog.pg_class relation join pg_catalog.pg_namespace schema on schema.oid=relation.relnamespace join pg_catalog.pg_attribute attribute on attribute.attrelid=relation.oid where schema.nspname='public' and relation.relkind in ('r','p') and attribute.attnum>0 and not attribute.attisdropped and relation.relname=any(:tables)\"
rows=c.execute(text(query),{'tables':list(REQUIRED_SCHEMA_COLUMNS)}).all()
actual={}
for table,column in rows: actual.setdefault(table,set()).add(column)
print('missing='+str(missing_schema_elements(actual)))
c.close(); e.dispose()"""
            run("run", "--rm", "--no-deps", "api", "python", "-c", schema_probe)
            run("up", "-d", "--wait", "api", "web")
            print("PASS fresh isolated setup explicitly ran bootstrap, PostgreSQL and migration before API/web")
            # A second up must reuse generated credentials, not reset PostgreSQL or Owner.
            fingerprint = "import hashlib,pathlib; print(hashlib.sha256(pathlib.Path('/runtime-secrets/owner-secret').read_bytes()+pathlib.Path('/runtime-secrets/app.json').read_bytes()).hexdigest())"
            before = run("exec", "-T", "api", "python", "-c", fingerprint)
            run("up", "-d", "--wait", "api", "web")
            assert before == run("exec", "-T", "api", "python", "-c", fingerprint)
            print("PASS normal compose up preserves generated credentials and Owner without setup dependencies")
            run("run", "--rm", "-T", "--no-deps", "migrate", "python", "-c", "from sqlalchemy import create_engine; from sqlalchemy.orm import sessionmaker; from agent_corporation_api.settings import get_settings; from agent_corporation_api.database import get_session_factory; from agent_corporation_api.modules.demo.factory import ensure_demo_scope,reset_demo_dataset; s=get_settings(); ensure_demo_scope(sessionmaker(create_engine(s.migration_database_url))); reset_demo_dataset(get_session_factory()); print('Synthetic demo scope ready')")
            output = run("exec", "-T", "api", "python", "-", code=ISOLATED_HTTP_CHECKS)
            print(output.strip())
            run("restart", "api", "web")
            run("exec", "-T", "api", "python", "-", code=ISOLATED_WAIT_READY)
            print(run("exec", "-T", "api", "python", "-", code=ISOLATED_RESTART_CHECK).strip())
            run("up", "-d", "--no-deps", "--force-recreate", "api")
            run("exec", "-T", "api", "python", "-", code=ISOLATED_WAIT_READY)
            run("exec", "-T", "api", "python", "-", code=ISOLATED_WAIT_READY.replace(
                "http://127.0.0.1:15501/api/v1/health/ready", "http://web:15500/api/v1/health/ready"))
            print("PASS API recreate: Nginx resolves current Docker service address")
            run("stop", "postgres")
            print(run("exec", "-T", "api", "python", "-", code=ISOLATED_DB_DOWN_CHECK).strip())
            actual_services = run("ps", "--services", "--filter", "status=running").splitlines()
            assert "worker" not in actual_services, actual_services
            manifest["runtime_worker"]["running_after_smoke"] = False
            manifest["smoke_checks"] = "passed"
        finally:
            cleanup_result = subprocess.run([*command, "down", "--volumes", "--remove-orphans", "--timeout", "10"],
                                            cwd=ROOT, capture_output=True, text=True, timeout=90)
            def labels(kind):
                result = subprocess.run([*DOCKER, kind, "ls", "-q", "--filter",
                                         "label=com.docker.compose.project=" + project],
                                        cwd=ROOT, capture_output=True, text=True, timeout=15)
                if result.returncode:
                    raise RuntimeError("Could not independently verify disposable " + kind + " cleanup")
                return [item for item in result.stdout.splitlines() if item.strip()]
            remaining_containers = labels("container")
            remaining_volumes = labels("volume")
            remaining_networks = labels("network")
            removed_images = []
            remaining_images = []
            for image_tag in (project + "-api:isolated", project + "-web:isolated"):
                image_result = subprocess.run([*DOCKER, "image", "rm", image_tag], cwd=ROOT,
                                              capture_output=True, text=True, timeout=60)
                if image_result.returncode and "No such image" not in image_result.stderr:
                    raise RuntimeError("Could not remove disposable image tag " + image_tag)
                inspect = subprocess.run([*DOCKER, "image", "inspect", image_tag], cwd=ROOT,
                                         capture_output=True, text=True, timeout=15)
                if inspect.returncode == 0:
                    remaining_images.append(image_tag)
                removed_images.append({"tag": image_tag, "exit_code": image_result.returncode,
                                       "result": image_result.stdout.strip() or image_result.stderr.strip()})
            manifest["cleanup"] = {"compose_down_exit_code": cleanup_result.returncode,
                                   "remaining_labeled_containers": remaining_containers,
                                   "remaining_labeled_volumes": remaining_volumes,
                                   "remaining_labeled_networks": remaining_networks,
                                   "remaining_images": remaining_images,
                                   "removed_images": removed_images,
                                   "status": "complete" if cleanup_result.returncode == 0 and not any((remaining_containers, remaining_volumes, remaining_networks, remaining_images)) else "incomplete",
                                   "compose_down_tail": (cleanup_result.stdout + cleanup_result.stderr)[-4000:]}
            print("CLEANUP: removed only disposable project " + project)
            manifest["completed_at_utc"] = datetime.now(UTC).isoformat()
            manifest["status"] = "passed" if manifest["cleanup"].get("status") == "complete" and manifest["smoke_checks"] == "passed" else "incomplete"
            manifest_path = run_dir / "run-manifest.json"
            manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
            manifest_path.chmod(0o600)
            print("Sanitized evidence: " + str(manifest_path.relative_to(ROOT)))


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
