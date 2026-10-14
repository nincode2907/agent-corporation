"""Safe route-level regression probe: no database, gateway, or inference."""
from uuid import uuid4
from fastapi import FastAPI
from fastapi.testclient import TestClient
from agent_corporation_api.modules.governance.auth import OwnerPrincipal, require_owner
from agent_corporation_api.modules.observability.scope import CompanyScope
from agent_corporation_api.modules.observability.router import router

app = FastAPI()
app.include_router(router)
app.dependency_overrides[require_owner] = lambda: OwnerPrincipal(
    CompanyScope(uuid4(), uuid4()), uuid4(), "fixture-owner"
)
response = TestClient(app, base_url="http://127.0.0.1:15501").get(
    "/api/v1/events/stream?cursor=initial-cursor",
    headers={"Last-Event-ID": "advanced-cursor"},
)
print(f"status={response.status_code}")
print(f"body={response.json()}")
assert response.status_code == 400
assert "không khớp" in response.json()["detail"]
