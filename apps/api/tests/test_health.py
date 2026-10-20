import asyncio

import httpx
from sqlalchemy.exc import OperationalError

from agent_corporation_api import main
from agent_corporation_api.database import DatabaseSchemaError


def request(path: str) -> httpx.Response:
    async def send() -> httpx.Response:
        transport = httpx.ASGITransport(app=main.app)
        async with httpx.AsyncClient(transport=transport, base_url="http://testserver") as client:
            return await client.get(path)

    return asyncio.run(send())


def test_liveness_does_not_depend_on_database() -> None:
    response = request("/api/v1/health/live")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "api"}


def test_readiness_reports_database_available(monkeypatch) -> None:
    monkeypatch.setattr(main, "database_is_ready", lambda: True)

    response = request("/api/v1/health/ready")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "checks": {"database": "ok"}}


def test_readiness_returns_sanitized_unavailable_status(monkeypatch) -> None:
    def unavailable() -> bool:
        raise OperationalError("SELECT 1", {}, RuntimeError("private database connection details"))

    monkeypatch.setattr(main, "database_is_ready", unavailable)

    response = request("/api/v1/health/ready")

    assert response.status_code == 503
    assert response.json() == {"status": "degraded", "checks": {"database": "unavailable"}}
    assert "private database connection details" not in response.text


def test_readiness_reports_incompatible_schema(monkeypatch) -> None:
    def incompatible_schema():
        raise DatabaseSchemaError("private schema detail")

    monkeypatch.setattr(main, "database_is_ready", incompatible_schema)

    response = request("/api/v1/health/ready")

    assert response.status_code == 503
    assert response.json() == {"status": "degraded", "checks": {"database": "schema_incompatible"}}
    assert "private schema detail" not in response.text


def test_startup_stops_clearly_on_incompatible_schema(monkeypatch) -> None:
    monkeypatch.setattr(main, "get_settings", lambda: object())

    def incompatible_schema():
        raise DatabaseSchemaError("private detail")

    monkeypatch.setattr(main, "database_is_ready", incompatible_schema)

    try:
        main.validate_runtime_startup()
    except RuntimeError as error:
        assert "schema is missing or incompatible" in str(error)
        assert "explicit migration procedure" in str(error)
        assert "private detail" not in str(error)
    else:
        raise AssertionError("API startup must stop for an incompatible database schema")
