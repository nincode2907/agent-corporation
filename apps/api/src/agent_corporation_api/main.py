from fastapi import FastAPI, Response, status
from sqlalchemy.exc import SQLAlchemyError

from .database import database_is_ready
from .modules.demo.router import router as demo_router
from .modules.codex_gateway.router import router as codex_router


app = FastAPI(
    title="Agent Corporation API",
    description="API local cho nền tảng Agent Corporation.",
    version="0.1.0",
    docs_url=None,
    redoc_url=None,
)
app.include_router(demo_router)
app.include_router(codex_router)


@app.get("/api/v1/health/live", tags=["health"])
def live() -> dict[str, str]:
    return {"status": "ok", "service": "api"}


@app.get("/api/v1/health/ready", tags=["health"])
def ready(response: Response) -> dict[str, object]:
    try:
        database_is_ready()
    except SQLAlchemyError:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        return {"status": "degraded", "checks": {"database": "unavailable"}}
    return {"status": "ok", "checks": {"database": "ok"}}
