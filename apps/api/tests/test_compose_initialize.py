"""First-run/idempotency regressions; only temporary synthetic credentials."""
import importlib.util
import json
import os
from pathlib import Path
import subprocess

import pytest
from sqlalchemy.engine import make_url

from agent_corporation_api.settings import get_settings


@pytest.fixture
def initializer(tmp_path, monkeypatch):
    spec = importlib.util.spec_from_file_location("compose_initializer", Path(__file__).resolve().parents[3] / "scripts/docker_initialize.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    # UID1000 is enforced by the real isolated Docker stack. Unit checks run on
    # both a nonroot Mac host and Linux, so ownership calls are stubbed here.
    monkeypatch.setattr(os, "chown", lambda *_: None)
    monkeypatch.setattr(os, "fchown", lambda *_: None)
    paths = tuple(tmp_path / name for name in ("operator", "runtime", "database", "postgres"))
    for path in paths: path.mkdir()
    return module, paths


def test_empty_checkout_generates_once_without_writing_host(initializer):
    module, paths = initializer
    module.initialize(*paths)
    operator, runtime, database, _ = paths
    assert list(operator.iterdir()) == []
    owner = (runtime / "owner-secret").read_bytes()
    state = (database / "state.json").read_bytes()
    assert len(owner.strip()) >= 40
    assert (runtime / "owner-secret").stat().st_mode & 0o777 == 0o600
    module.initialize(*paths)
    assert (runtime / "owner-secret").read_bytes() == owner
    assert (database / "state.json").read_bytes() == state
    app = json.loads((runtime / "app.json").read_text())
    assert "migration_database_url" not in app
    assert app["app_database_user"] != json.loads(state)["POSTGRES_USER"]


def test_legacy_env_and_owner_are_preserved_and_shell_values_are_quoted(initializer):
    module, paths = initializer
    operator, runtime, database, postgres = paths
    password = "literal'$(printf INJECTION)"
    env = operator / ".env"
    env.write_text("POSTGRES_USER=old_admin\nPOSTGRES_DB=old_db\nAPP_DATABASE_USER=old_app\nAPP_DATABASE_PASSWORD=app_fixture\nPOSTGRES_PASSWORD=\"" + password + "\"\n")
    env.chmod(0o600)
    (operator / ".local").mkdir()
    owner = operator / ".local/owner-secret"
    owner.write_text("synthetic-existing-owner-" + "x" * 40); owner.chmod(0o600)
    (postgres / "PG_VERSION").write_text("18")
    module.initialize(*paths)
    assert (runtime / "owner-secret").read_bytes() == owner.read_bytes()
    migration = json.loads((database / "migration.json").read_text())
    assert make_url(migration["migration_database_url"]).password == password
    result = subprocess.run(["/bin/sh", "-c", '. "$1"; printf "%s" "$POSTGRES_PASSWORD"', "fixture", str(database / "postgres.env")], capture_output=True, text=True, check=True)
    assert result.stdout == password
    original = (database / "state.json").read_bytes()
    env.write_text(env.read_text().replace("app_fixture", "changed_fixture"))
    with pytest.raises(ValueError, match="credentials differ"):
        module.initialize(*paths)
    assert (database / "state.json").read_bytes() == original


def test_existing_database_without_its_credentials_is_blocked(initializer):
    module, paths = initializer
    (paths[3] / "PG_VERSION").write_text("18")
    with pytest.raises(ValueError, match="Existing PostgreSQL"):
        module.initialize(*paths)
    assert not (paths[2] / "state.json").exists()


def test_initialize_never_installs_or_removes_runtime_cg01_proof(initializer):
    module, paths = initializer
    operator, runtime, _, _ = paths
    proof = runtime / "cg01-proof.json"
    original = b'{"expires_at":"2000-01-01T00:00:00+00:00","fixture":"stale"}'
    proof.write_bytes(original)
    proof.chmod(0o600)
    module.initialize(*paths)
    assert proof.read_bytes() == original
    assert proof.stat().st_mode & 0o777 == 0o600
    assert not (operator / ".local" / "cg01-proof.json").exists()


def test_docker_settings_reads_private_json_and_environment_overrides(monkeypatch, tmp_path):
    config = tmp_path / "app.json"
    config.write_text(json.dumps({"database_url": "postgresql+psycopg://fixture@postgres/db", "app_database_password": "fixture"}))
    monkeypatch.setenv("APP_CONFIG_FILE", str(config))
    monkeypatch.delenv("DATABASE_URL", raising=False)
    monkeypatch.delenv("MIGRATION_DATABASE_URL", raising=False)
    monkeypatch.setenv("CODEX_SERVER_TRANSPORT", "docker-host")
    result = get_settings()
    assert result.database_url.endswith("@postgres/db")
    assert result.codex_server_transport == "docker-host"
    assert result.migration_database_url is None
    config.write_text('{"unknown_secret_field":"fixture-secret-canary"}')
    with pytest.raises(RuntimeError, match="cấu hình") as error:
        get_settings()
    assert "fixture-secret-canary" not in str(error.value)
