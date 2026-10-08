from fastapi import APIRouter

from ...settings import get_settings
from .adapter import ProbeSettings, probe_gateway


router = APIRouter(prefix="/api/v1/codex", tags=["codex"])


@router.get("/probe")
def gateway_probe() -> dict[str, object]:
    settings = get_settings()
    return probe_gateway(ProbeSettings(
        base_url=settings.codex_server_base_url,
        api_key=settings.codex_server_api_key,
    ))
