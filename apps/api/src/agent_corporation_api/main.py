from fastapi import FastAPI, Response, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError

from .database import database_is_ready
from .modules.demo.router import router as demo_router
from .modules.codex_gateway.router import router as codex_router
from .modules.governance.auth_router import router as owner_router
from .modules.observability.router import router as events_router
from .modules.execution.router import router as runtime_router


app = FastAPI(
    title="Agent Corporation API",
    description="API local cho nền tảng Agent Corporation.",
    version="0.1.0",
    docs_url=None,
    redoc_url=None,
)
app.include_router(demo_router)
app.include_router(codex_router)
app.include_router(owner_router)
app.include_router(events_router)
app.include_router(runtime_router)


@app.middleware("http")
async def private_runtime_responses(request, call_next):
    response = await call_next(request)
    if request.url.path.startswith(("/api/v1/owner", "/api/v1/runtime", "/api/v1/events")):
        response.headers["Cache-Control"] = "no-store"
    return response


@app.exception_handler(SQLAlchemyError)
async def database_error(_request, _error: SQLAlchemyError):
    # Handled exceptions must not emit SQL statements or bound private parameters.
    return JSONResponse(status_code=503, content={"detail": "Cơ sở dữ liệu tạm thời không khả dụng."})


@app.exception_handler(RequestValidationError)
async def validation_error(_request, error: RequestValidationError):
    # FastAPI's default detail echoes raw input (including Owner credentials/context).
    return JSONResponse(status_code=422, content={"detail": [
        {"loc": list(item["loc"]), "type": item["type"], "msg": "Giá trị không hợp lệ."}
        for item in error.errors()
    ]})


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
