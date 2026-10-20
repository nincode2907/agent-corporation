"""Owner-authorized demo exception: only fake transport and temporary files, no inference."""
import asyncio
import importlib.util
import os
import subprocess
import sys
from pathlib import Path
from types import SimpleNamespace
from uuid import uuid4

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from agent_corporation_api.modules.demo.factory import DEMO_SCOPE
from agent_corporation_api.modules.execution import gates, router, service, worker
from agent_corporation_api.modules.governance.auth import OwnerPrincipal, require_owner, require_owner_write
from agent_corporation_api.modules.observability.scope import CompanyScope
from agent_corporation_api.settings import Settings


def config(tmp_path, enabled=True, url="http://127.0.0.1:15600"):
    return SimpleNamespace(runtime_cg01_demo_test_override=enabled, codex_server_base_url=url,
                           runtime_gate_path=tmp_path / "missing-proof", runtime_gateway_source_path=tmp_path / "missing-gateway")


def test_default_is_strict_and_absent_proof_is_not_approved(tmp_path):
    settings = Settings(_env_file=None, database_url="fixture", app_database_password="fixture")
    assert settings.runtime_cg01_demo_test_override is False
    state = gates.runtime_gate(config(tmp_path, enabled=False), DEMO_SCOPE)
    assert state["allowed"] is False and state["mode"] == "strict" and state["verified"] is False


def test_demo_exception_needs_no_proof_and_never_claims_verified(tmp_path):
    state = gates.runtime_gate(config(tmp_path), DEMO_SCOPE)
    assert state == {"allowed": True, "reason": "owner_authorized_demo_test_override", "mode": "demo-test", "verified": False}
    assert not (tmp_path / "missing-proof").exists()


@pytest.mark.parametrize("scope", [None, CompanyScope(uuid4(), DEMO_SCOPE.company_id), CompanyScope(DEMO_SCOPE.environment_id, uuid4())])
def test_demo_exception_rejects_other_or_missing_scope(tmp_path, scope):
    assert gates.runtime_gate(config(tmp_path), scope)["reason"] == "demo_test_scope_required"
    assert gates.runtime_gate(config(tmp_path), scope)["allowed"] is False


@pytest.mark.parametrize("url", ["http://host.docker.internal:15600", "http://192.168.1.1:15600", "https://127.0.0.1:15600", "http://127.0.0.1:15600/redirect", "http://user:secret@127.0.0.1:15600"])
def test_exception_keeps_literal_loopback_endpoint_constraint(tmp_path, url):
    state = gates.runtime_gate(config(tmp_path, url=url), DEMO_SCOPE)
    assert state["allowed"] is False and state["reason"] == "invalid_local_gateway"


def test_unsupported_platform_strict_fails_closed_demo_still_explicit(tmp_path, monkeypatch):
    monkeypatch.delattr(os, "getuid", raising=False)
    strict = gates.runtime_gate(config(tmp_path, enabled=False), DEMO_SCOPE)
    assert strict["allowed"] is False and strict["reason"] == "unsupported_platform"
    assert gates.runtime_gate(config(tmp_path), DEMO_SCOPE)["verified"] is False


def test_api_status_override_does_not_create_grants_or_accept_body_override(tmp_path, monkeypatch):
    app = FastAPI()
    app.include_router(router.router)
    client = TestClient(app, base_url="http://127.0.0.1:15501")
    assert client.get("/api/v1/runtime/status").status_code == 401
    principal = OwnerPrincipal(DEMO_SCOPE, uuid4(), "fixture-owner")
    app.dependency_overrides[require_owner] = lambda: principal
    app.dependency_overrides[require_owner_write] = lambda: principal
    monkeypatch.setattr(router, "get_settings", lambda: config(tmp_path))
    monkeypatch.setattr(router, "get_session_factory", lambda: None)
    monkeypatch.setattr(service, "grants_list", lambda *args: [])
    monkeypatch.setattr(service, "runs_list", lambda *args: [])
    status = client.get("/api/v1/runtime/status").json()
    assert status["cg01"]["allowed"] is True and status["cg01"]["verified"] is False
    assert status["inference_grants"] == 0
    body = {"grant_id": str(uuid4()), "employee_id": str(uuid4()), "employee_version_id": str(uuid4()), "phase": "06", "batch_id": "fixture", "purpose": "fixture", "model": "fixture", "effort": "low", "input_text": "fixture", "idempotency_key": str(uuid4())}
    seen = []
    def denied(*args):
        seen.append(args[-1])
        raise service.RuntimeDenied("missing_or_revoked_grant")
    monkeypatch.setattr(service, "run_create", denied)
    response = client.post("/api/v1/runtime/runs", json=body)
    assert response.status_code == 409 and response.json()["detail"] == "missing_or_revoked_grant"
    assert seen[0]["mode"] == "demo-test" and seen[0]["verified"] is False
    for field in ("cg01_approved", "runtime_cg01_demo_test_override", "company_id"):
        assert client.post("/api/v1/runtime/runs", json={**body, field: True}).status_code == 422
    assert len(seen) == 1


def test_worker_checks_exception_scope_before_reservation(tmp_path, monkeypatch):
    monkeypatch.setattr(worker, "get_settings", lambda: config(tmp_path))
    monkeypatch.setattr(worker, "get_session_factory", lambda: None)
    monkeypatch.setattr(service, "recover_expired", lambda *args: 0)
    monkeypatch.setattr(service, "reserve_next", lambda *args: pytest.fail("Cannot reserve outside demo"))
    asyncio.run(worker.work(CompanyScope(uuid4(), uuid4()), once=True))


def test_worker_rechecks_gate_before_dispatch_and_relock_blocks(tmp_path, monkeypatch):
    settings = config(tmp_path)
    monkeypatch.setattr(worker, "get_settings", lambda: settings)
    monkeypatch.setattr(worker, "get_session_factory", lambda: None)
    monkeypatch.setattr(service, "recover_expired", lambda *args: 0)
    finished = []
    def reserve(*args):
        settings.runtime_cg01_demo_test_override = False
        return {"id": uuid4()}
    monkeypatch.setattr(service, "reserve_next", reserve)
    monkeypatch.setattr(service, "finish", lambda *args: finished.append(args[-1]))
    async def forbidden(*args):
        pytest.fail("Cannot dispatch after relock")
    monkeypatch.setattr(worker, "execute_reserved", forbidden)
    asyncio.run(worker.work(DEMO_SCOPE, once=True))
    assert finished[0].reason == "cg01_changed_after_reservation"


def mode_script():
    path = Path(__file__).resolve().parents[3] / "scripts" / "cg01_mode.py"
    spec = importlib.util.spec_from_file_location("cg01_mode", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_local_toggle_preserves_other_values_and_is_reversible(tmp_path):
    script = mode_script()
    env = tmp_path / ".env"
    original = "# fake secrets only\r\nFAKE_SECRET=fixture-canary\r\nOTHER=keep\r\n"
    env.write_bytes((original + "RUNTIME_CG01_DEMO_TEST_OVERRIDE=false\r\nexport RUNTIME_CG01_DEMO_TEST_OVERRIDE=false\n").encode())
    env.chmod(0o600)
    before = env.stat().st_mode
    script.set_mode(env, True)
    assert env.read_bytes() == (original + "RUNTIME_CG01_DEMO_TEST_OVERRIDE=true\n").encode()
    assert env.stat().st_mode == before
    script.set_mode(env, False)
    assert env.read_bytes() == (original + "RUNTIME_CG01_DEMO_TEST_OVERRIDE=false\n").encode()
    with pytest.raises(ValueError):
        script.set_mode(tmp_path / "missing", True)


def test_release_check_rejects_override_and_requires_strict_proof(tmp_path):
    script = mode_script()
    assert script.release_check(config(tmp_path))[0] is False
    assert script.release_check(config(tmp_path, enabled=False))[0] is False


def test_release_cli_vietnamese_diagnostic_with_windows_console_encoding():
    script = Path(__file__).resolve().parents[3] / "scripts" / "cg01_mode.py"
    # Import only the CLI, then substitute a fake release check; no real env/secrets.
    code = (
        "import importlib.util,sys;"
        f"spec=importlib.util.spec_from_file_location('mode_fixture',{str(script)!r});"
        "module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);"
        "module.release_check=lambda settings:(False,'Ngo\\u1ea1i l\\u1ec7 demo c\\u00f2n b\\u1eadt');"
        "import types;"
        "settings_module=types.ModuleType('agent_corporation_api.settings');"
        "settings_module.get_settings=lambda:None;"
        "sys.modules['agent_corporation_api.settings']=settings_module;"
        "sys.argv=['cg01_mode.py','release-check'];sys.exit(module.main())"
    )
    result = subprocess.run([sys.executable, "-c", code], env={**os.environ, "PYTHONIOENCODING": "cp1252", "PYTHONUTF8": "0"}, capture_output=True)
    assert result.returncode == 1
    assert "CG01 release: BLOCKED · Ngoại lệ demo còn bật" in result.stdout.decode("utf-8")
    assert result.stderr == b""
