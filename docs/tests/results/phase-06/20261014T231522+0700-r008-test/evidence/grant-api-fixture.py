"""Route contract fixture for the one-turn UI grant; never touches DB/model."""
from datetime import UTC, datetime, timedelta
from pathlib import Path
import sys
from uuid import uuid4

from fastapi import FastAPI
from fastapi.testclient import TestClient
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[6] / "apps" / "api" / "src"))

from agent_corporation_api.modules.execution import router
from agent_corporation_api.modules.governance.auth import OwnerPrincipal, require_owner_write
from agent_corporation_api.modules.observability.scope import CompanyScope


def main():
    app = FastAPI()
    app.include_router(router.router)
    client = TestClient(app, base_url="http://127.0.0.1:15501")
    calls = []
    principal = OwnerPrincipal(CompanyScope(uuid4(), uuid4()), uuid4(), "fixture-owner")
    body = {
        "phase": "06",
        "batch_id": "phase06-ui-fixture",
        "purpose": "Fixture only: one-turn text test",
        "model": "fixture-model",
        "effort": "high",
        "max_requests": 1,
        "max_concurrency": 1,
        "timeout_seconds": 120,
        "max_requeues": 0,
        "expires_at": (datetime.now(UTC) + timedelta(minutes=15)).isoformat(),
    }

    def fake_create(factory, scope, owner_id, spec):
        calls.append((factory, scope, owner_id, spec))
        return {"id": uuid4(), **spec, "used_requests": 0, "revoked": False}

    with pytest.MonkeyPatch.context() as patch:
        patch.setattr(router.service, "grant_create", fake_create)
        patch.setattr(router, "get_session_factory", lambda: "never-used-fixture")

        denied = client.post(
            "/api/v1/runtime/grants",
            json=body,
            headers={"origin": "http://127.0.0.1:15500"},
        )
        assert denied.status_code == 401, denied.text
        assert calls == [], "Unauthenticated grant must not reach service"

        app.dependency_overrides[require_owner_write] = lambda: principal
        accepted = client.post("/api/v1/runtime/grants", json=body)
        assert accepted.status_code == 201, accepted.text
        assert len(calls) == 1
        factory, scope, owner_id, spec = calls[0]
        assert factory == "never-used-fixture"
        assert scope == principal.scope and owner_id == principal.owner_id
        assert spec["phase"] == "06" and spec["max_requests"] == 1
        assert spec["max_concurrency"] == 1 and spec["timeout_seconds"] == 120
        assert spec["max_requeues"] == 0 and spec["model"] == "fixture-model"

        for field, invalid in (
            ("max_requests", 0),
            ("max_concurrency", 2),
            ("timeout_seconds", 121),
            ("max_requeues", 3),
        ):
            response = client.post("/api/v1/runtime/grants", json={**body, field: invalid})
            assert response.status_code == 422, (field, response.status_code, response.text)
        assert len(calls) == 1, "Invalid grant bounds must not reach service"

    print("PASS unauthenticated grant denied before service; authenticated route fixture accepted 1 request/120s/concurrency 1/no retry; invalid bounds denied before service; no DB/model")


if __name__ == "__main__":
    main()
