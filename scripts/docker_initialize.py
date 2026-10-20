"""One-shot Compose initializer. Generate once, import legacy secrets, never log values."""
from __future__ import annotations

import fcntl
import json
import os
from pathlib import Path
import re
import secrets
import shlex
import stat
import tempfile
from urllib.parse import quote

from dotenv import dotenv_values


def read_private(path: Path) -> bytes | None:
    if not path.exists() and not path.is_symlink():
        return None
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    with os.fdopen(fd, "rb") as stream:
        info = os.fstat(stream.fileno())
        if not stat.S_ISREG(info.st_mode) or stat.S_IMODE(info.st_mode) != 0o600 or info.st_size > 65536:
            raise ValueError("Operator secret/config must be a regular 0600 file, at most 64 KB")
        return stream.read(65537)


def write_private(path: Path, content: bytes, *, uid: int = 1000) -> None:
    # Identical configuration retains its inode/mtime as well as its value.
    if path.exists() and read_private(path) == content:
        return
    descriptor, name = tempfile.mkstemp(prefix=".init-", dir=path.parent)
    temporary = Path(name)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(content)
            stream.flush()
            os.fsync(stream.fileno())
            os.fchown(stream.fileno(), uid, uid)
            os.fchmod(stream.fileno(), 0o600)
        temporary.replace(path)
    finally:
        temporary.unlink(missing_ok=True)


def initialize(operator: Path, runtime: Path, database: Path, postgres: Path) -> None:
    for directory in (runtime, database):
        if directory.is_symlink():
            raise ValueError("Runtime config directory must not be a symlink")
        directory.mkdir(exist_ok=True)
        os.chown(directory, 1000, 1000)
        directory.chmod(0o700)
    if (operator / ".local").is_symlink():
        raise ValueError("Operator .local must not be a symlink")
    with (database / ".initialize.lock").open("a") as lock:
        os.chmod(lock.name, 0o600)
        fcntl.flock(lock, fcntl.LOCK_EX)
        env_file = operator / ".env"
        imported = {}
        if read_private(env_file) is not None:
            imported = dict(dotenv_values(env_file, interpolate=False))
        state_file = database / "state.json"
        stored = read_private(state_file)
        if stored:
            values = json.loads(stored)
            for key in values:
                if key in imported and imported[key] != values[key]:
                    raise ValueError("Database credentials differ from persisted configuration; deliberate migration required")
        else:
            old_database = any((postgres / path).exists() for path in ("PG_VERSION", "18/docker/PG_VERSION"))
            required = ("POSTGRES_USER", "POSTGRES_PASSWORD", "POSTGRES_DB", "APP_DATABASE_USER", "APP_DATABASE_PASSWORD")
            if old_database and not all(imported.get(key) for key in required):
                raise ValueError("Existing PostgreSQL requires its original .env or persisted database configuration")
            defaults = {"POSTGRES_USER": "agent_corporation", "POSTGRES_DB": "agent_corporation",
                        "APP_DATABASE_USER": "agent_corporation_app"}
            values = {key: imported.get(key) or defaults.get(key) or secrets.token_hex(32) for key in required}
        for key in ("POSTGRES_USER", "POSTGRES_DB", "APP_DATABASE_USER"):
            if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]{0,62}", values[key]):
                raise ValueError("Database identifier is invalid")
        if values["POSTGRES_USER"] == values["APP_DATABASE_USER"]:
            raise ValueError("Application database role must differ from migration admin")
        def url(user: str, password: str) -> str:
            return f"postgresql+psycopg://{quote(user, safe='')}:{quote(password, safe='')}@postgres:5432/{quote(values['POSTGRES_DB'], safe='')}"
        app = {"database_url": url(values["APP_DATABASE_USER"], values["APP_DATABASE_PASSWORD"]),
               "app_database_user": values["APP_DATABASE_USER"], "app_database_password": values["APP_DATABASE_PASSWORD"]}
        previous_app = read_private(runtime / "app.json")
        gateway_key = imported.get("CODEX_SERVER_API_KEY", json.loads(previous_app).get("codex_server_api_key") if previous_app else None)
        if gateway_key:
            app["codex_server_api_key"] = gateway_key
        migration = {**app, "migration_database_url": url(values["POSTGRES_USER"], values["POSTGRES_PASSWORD"])}
        # Admin credentials are never mounted into the API container.
        write_private(state_file, json.dumps(values, sort_keys=True).encode(), uid=0)
        write_private(database / "migration.json", json.dumps(migration, sort_keys=True).encode())
        shell = "".join(f"export {key}={shlex.quote(values[key])}\n" for key in ("POSTGRES_USER", "POSTGRES_PASSWORD", "POSTGRES_DB"))
        write_private(database / "postgres.env", shell.encode(), uid=0)
        write_private(runtime / "app.json", json.dumps(app, sort_keys=True).encode())
        owner = runtime / "owner-secret"
        source_owner = read_private(operator / ".local" / "owner-secret")
        if source_owner is not None:
            if not 40 <= len(source_owner.strip()) <= 128:
                raise ValueError("Owner secret length is invalid")
            write_private(owner, source_owner)
        elif read_private(owner) is None:
            write_private(owner, (secrets.token_urlsafe(48) + "\n").encode())
        # CG01 proof files have a separate explicit operator lifecycle. Normal
        # config/Owner bootstrap must neither install nor revoke a runtime proof.
    print("Cấu hình/Owner đã sẵn sàng; giữ credential đã có, không hiển thị secret.", flush=True)


if __name__ == "__main__":
    try:
        initialize(Path("/operator"), Path("/runtime-secrets"), Path("/database-secrets"), Path("/postgres-state"))
    except Exception:
        raise SystemExit("Khởi tạo bị chặn. Kiểm tra quyền file0600 và cấu hình DB cũ; không thay dữ liệu hoặc in secret.") from None
