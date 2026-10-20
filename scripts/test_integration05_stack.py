"""Start a disposable, fake-transport-only browser stack; cleanup with --down."""
from __future__ import annotations

import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
from uuid import uuid4

ROOT = Path(__file__).resolve().parents[1]
PORT = 15502


def run(command: list[str], *, capture: bool = False) -> str:
    result = subprocess.run(command, cwd=ROOT, text=True, capture_output=True)
    if result.returncode:
        if capture:
            print((result.stdout + result.stderr)[-5000:])
        raise SystemExit(result.returncode)
    return result.stdout if capture else ""


def main() -> None:
    if len(sys.argv) > 1 and sys.argv[1] == "--down":
        control = json.loads(Path(sys.argv[2]).read_text())
        run(["docker", "compose", "-p", control["project"], "-f", control["compose"], "down", "--volumes", "--remove-orphans"])
        shutil.rmtree(Path(control["compose"]).parent, ignore_errors=True)
        Path(sys.argv[2]).unlink(missing_ok=True)
        print("Removed the named disposable Integration 05 Compose project and its volumes.")
        return
    worker_script = Path(sys.argv[2]).resolve() if len(sys.argv) > 2 and sys.argv[1] == "--worker-script" else ROOT / "scripts/integration05_fake_worker.py"
    if not worker_script.is_file():
        raise SystemExit(f"Fake worker script not found: {worker_script}")
    project = "ac-integration05-" + uuid4().hex[:10]
    resolved = json.loads(run(["docker", "compose", "config", "--format", "json"], capture=True))
    resolved["name"] = project
    resolved.pop("networks", None)
    temp = Path(tempfile.mkdtemp(prefix=project + "-"))
    (temp / ".local").mkdir(mode=0o700)
    owner_path = temp / ".local" / "owner-secret"
    owner_path.write_text("synthetic-owner-secret-" + "a" * 48 + "\n")
    owner_path.chmod(0o600)

    synthetic_environment = {
        "APP_CONFIG_FILE": "/runtime-secrets/app.json",
        "CODEX_SERVER_BASE_URL": "http://host.docker.internal:15600",
        "CODEX_SERVER_TRANSPORT": "docker-host",
        "OWNER_SECRET_PATH": "/runtime-secrets/owner-secret",
        "RUNTIME_GATE_PATH": "/runtime-secrets/cg01-proof.json",
        "RUNTIME_GATEWAY_SOURCE_PATH": "/gateway-source",
        "RUNTIME_CG01_DEMO_TEST_OVERRIDE": "false",
        "PLAYGROUND_WORKER_ENABLED": "false",
    }
    for name, service in resolved["services"].items():
        for key in list(service):
            if service[key] is None:
                del service[key]
        service.pop("container_name", None)
        service.pop("ports", None)
        if name in {"api", "migrate", "worker"}:
            service["environment"] = dict(synthetic_environment)
        if name == "migrate":
            service["environment"]["APP_CONFIG_FILE"] = "/database-secrets/migration.json"
        if name == "bootstrap":
            for volume in service["volumes"]:
                if volume.get("target") == "/operator":
                    volume["source"] = str(temp)
        if name in {"api", "worker"}:
            service.setdefault("volumes", []).append({"type": "bind", "source": str(ROOT / "scripts/integration05_fake_api.py"), "target": "/test/integration05_fake_api.py", "read_only": True})
            service["volumes"].append({"type": "bind", "source": str(worker_script), "target": "/test/integration05_fake_worker.py", "read_only": True})
        if name == "api":
            service["command"] = ["python", "/test/integration05_fake_api.py"]
        if name == "worker":
            service["entrypoint"] = ["python", "/test/integration05_fake_worker.py"]
            service["command"] = []
    resolved["services"]["web"]["ports"] = [f"127.0.0.1:{PORT}:15500"]
    for key in resolved.get("volumes", {}):
        resolved["volumes"][key] = {"name": project + "_" + key}
    compose_path = temp / "compose.json"
    compose_path.write_text(json.dumps(resolved))
    compose_path.chmod(0o600)
    control_path = ROOT / "docs/reviews/integration-05/evidence/disposable-stack.json"
    control_path.parent.mkdir(parents=True, exist_ok=True)
    control_path.write_text(json.dumps({"project": project, "compose": str(compose_path)}, indent=2) + "\n")
    command = ["docker", "compose", "-p", project, "-f", str(compose_path)]
    try:
        run([*command, "up", "--build", "--wait"])
        run([*command, "run", "--rm", "-T", "migrate", "python", "-c",
             "from sqlalchemy import create_engine; from sqlalchemy.orm import sessionmaker; from agent_corporation_api.settings import get_settings; from agent_corporation_api.database import get_session_factory; from agent_corporation_api.modules.demo.factory import ensure_demo_scope,reset_demo_dataset; s=get_settings(); ensure_demo_scope(sessionmaker(create_engine(s.migration_database_url))); reset_demo_dataset(get_session_factory()); print('Disposable synthetic demo fixture ready')"])
    except BaseException:
        try:
            run([*command, "down", "--volumes", "--remove-orphans"])
        except BaseException:
            pass
        finally:
            shutil.rmtree(temp, ignore_errors=True)
            control_path.unlink(missing_ok=True)
        raise
    print(f"Disposable stack ready at http://127.0.0.1:{PORT}/#runtime")
    print(f"Control file: {control_path}")
    print("CG01 override environment remains false; only isolated harness monkeypatches the API gate and worker transport.")
    print("Cleanup after browser QA: rtk uv run --project apps/api python scripts/test_integration05_stack.py --down " + str(control_path))


if __name__ == "__main__":
    main()
