from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


REPOSITORY_ROOT = Path(__file__).resolve().parents[4]


class Settings(BaseSettings):
    database_url: str
    migration_database_url: str | None = None
    app_database_user: str = "agent_corporation_app"
    app_database_password: str
    codex_server_base_url: str = "http://127.0.0.1:15600"
    codex_server_api_key: str | None = None
    owner_secret_path: Path = REPOSITORY_ROOT / ".local" / "owner-secret"
    owner_session_ttl_seconds: int = 3600
    runtime_gate_path: Path = REPOSITORY_ROOT / ".local" / "cg01-proof.json"
    runtime_gateway_source_path: Path = REPOSITORY_ROOT.parent / "codex-server"

    model_config = SettingsConfigDict(
        env_file=REPOSITORY_ROOT / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


def get_settings() -> Settings:
    return Settings()
