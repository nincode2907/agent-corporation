from pathlib import Path
import json
import os
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


REPOSITORY_ROOT = Path(__file__).resolve().parents[4]


class Settings(BaseSettings):
    database_url: str
    migration_database_url: str | None = None
    app_database_user: str = "agent_corporation_app"
    app_database_password: str
    codex_server_base_url: str = "http://127.0.0.1:15600"
    codex_server_api_key: str | None = None
    codex_server_transport: Literal["loopback", "docker-host"] = "loopback"
    owner_secret_path: Path = REPOSITORY_ROOT / ".local" / "owner-secret"
    owner_session_ttl_seconds: int = 3600
    runtime_gate_path: Path = REPOSITORY_ROOT / ".local" / "cg01-proof.json"
    runtime_gateway_source_path: Path = REPOSITORY_ROOT.parent / "codex-server"
    runtime_cg01_demo_test_override: bool = False
    playground_worker_enabled: bool = True

    model_config = SettingsConfigDict(
        env_file=REPOSITORY_ROOT / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


def get_settings() -> Settings:
    config_path = os.getenv("APP_CONFIG_FILE")
    if config_path:
        try:
            data = json.loads(Path(config_path).read_text())
            if not isinstance(data, dict) or set(data) - set(Settings.model_fields):
                raise ValueError("Invalid runtime config")
            for field in Settings.model_fields:
                if field.upper() in os.environ:
                    data[field] = os.environ[field.upper()]
            return Settings(_env_file=None, **data)
        except Exception:
            raise RuntimeError("Không đọc được cấu hình runtime Docker hợp lệ.") from None
    return Settings()
