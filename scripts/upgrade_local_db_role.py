from __future__ import annotations

import os
import secrets
from pathlib import Path

from sqlalchemy.engine import URL, make_url


ROOT = Path(__file__).resolve().parents[1]
ENV_FILE = ROOT / ".env"


def values_from_env() -> tuple[list[str], dict[str, str]]:
    lines = ENV_FILE.read_text(encoding="utf-8").splitlines()
    values = {}
    for line in lines:
        if line and not line.lstrip().startswith("#") and "=" in line:
            key, value = line.split("=", 1)
            values[key] = value
    return lines, values


def upgrade() -> None:
    if not ENV_FILE.is_file():
        raise SystemExit("Không tìm thấy .env; chạy scripts/bootstrap_local.py trước.")
    mode = ENV_FILE.stat().st_mode & 0o777
    if mode & 0o077:
        raise SystemExit(".env phải có quyền 0600 trước khi cập nhật database role.")

    lines, values = values_from_env()
    if all(key in values for key in ("MIGRATION_DATABASE_URL", "APP_DATABASE_USER", "APP_DATABASE_PASSWORD")):
        print(".env đã có URL migration và thông tin app role tách biệt.")
        return

    admin_url = make_url(values.get("MIGRATION_DATABASE_URL") or values["DATABASE_URL"])
    if not admin_url.host or not admin_url.username or not admin_url.password:
        raise SystemExit("DATABASE_URL hiện tại thiếu thông tin kết nối local cần thiết.")
    if admin_url.host not in {"127.0.0.1", "localhost"}:
        raise SystemExit("Chỉ tách database role cho PostgreSQL loopback local.")

    app_user = values.get("APP_DATABASE_USER", "agent_corporation_app")
    app_password = values.get("APP_DATABASE_PASSWORD") or secrets.token_hex(32)
    app_url = URL.create(
        drivername=admin_url.drivername,
        username=app_user,
        password=app_password,
        host=admin_url.host,
        port=admin_url.port,
        database=admin_url.database,
        query=admin_url.query,
    )
    replacements = {
        "DATABASE_URL": app_url.render_as_string(hide_password=False),
        "MIGRATION_DATABASE_URL": admin_url.render_as_string(hide_password=False),
        "APP_DATABASE_USER": app_user,
        "APP_DATABASE_PASSWORD": app_password,
    }
    pending = set(replacements)
    output = []
    for line in lines:
        key = line.split("=", 1)[0] if "=" in line and not line.lstrip().startswith("#") else None
        if key in replacements:
            output.append(f"{key}={replacements[key]}")
            pending.discard(key)
        else:
            output.append(line)
    output.extend(f"{key}={replacements[key]}" for key in sorted(pending))

    temporary = ENV_FILE.with_name(".env.phase03.tmp")
    descriptor = os.open(temporary, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(descriptor, "w", encoding="utf-8") as target:
        target.write("\n".join(output) + "\n")
    os.chmod(temporary, 0o600)
    os.replace(temporary, ENV_FILE)
    print("Đã tách app/migration database URL trong .env; secret giữ quyền 0600 và không hiển thị.")


if __name__ == "__main__":
    upgrade()
