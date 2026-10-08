from __future__ import annotations

import os
import secrets
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ENV_FILE = ROOT / ".env"


def bootstrap() -> None:
    if ENV_FILE.exists():
        os.chmod(ENV_FILE, 0o600)
        print("Đã có .env cục bộ; giữ nguyên nội dung và đặt quyền đọc/ghi cho chủ sở hữu.")
        return

    password = secrets.token_hex(32)
    app_password = secrets.token_hex(32)
    values = {
        "POSTGRES_USER": "agent_corporation",
        "POSTGRES_PASSWORD": password,
        "POSTGRES_DB": "agent_corporation",
        "DATABASE_URL": f"postgresql+psycopg://agent_corporation_app:{app_password}@127.0.0.1:15510/agent_corporation",
        "MIGRATION_DATABASE_URL": f"postgresql+psycopg://agent_corporation:{password}@127.0.0.1:15510/agent_corporation",
        "APP_DATABASE_USER": "agent_corporation_app",
        "APP_DATABASE_PASSWORD": app_password,
        "OWNER_BOOTSTRAP_TOKEN": secrets.token_urlsafe(48),
        "SESSION_SIGNING_KEY": secrets.token_hex(48),
    }
    payload = "# Secret local; không đưa vào Git.\n" + "".join(f"{key}={value}\n" for key, value in values.items())
    descriptor = os.open(ENV_FILE, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as env_file:
            env_file.write(payload)
    except BaseException:
        ENV_FILE.unlink(missing_ok=True)
        raise
    print("Đã tạo .env với secret ngẫu nhiên, quyền 0600. Không hiển thị secret trong terminal.")


if __name__ == "__main__":
    bootstrap()
