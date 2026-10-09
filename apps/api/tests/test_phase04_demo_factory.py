from __future__ import annotations

from uuid import uuid4

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session, sessionmaker

from agent_corporation_api.main import app
from agent_corporation_api.modules.demo.factory import (
    DEMO_COMPANY_ID,
    DEMO_ENVIRONMENT_ID,
    ensure_demo_scope,
    reset_demo_dataset,
)
from agent_corporation_api.settings import get_settings


@pytest.fixture
def databases():
    settings = get_settings()
    app_engine = create_engine(settings.database_url, pool_pre_ping=True)
    admin_engine = create_engine(settings.migration_database_url or settings.database_url, pool_pre_ping=True)
    yield sessionmaker(app_engine, expire_on_commit=False), sessionmaker(admin_engine, expire_on_commit=False)
    app_engine.dispose()
    admin_engine.dispose()


def test_demo_seed_and_reset_are_deterministic_and_scope_limited(databases):
    app_factory, admin_factory = databases
    ensure_demo_scope(admin_factory)
    first = reset_demo_dataset(app_factory)

    benchmark_environment = uuid4()
    benchmark_company = uuid4()
    benchmark_task = uuid4()
    benchmark_artifact = uuid4()
    real_environment = uuid4()
    real_company = uuid4()
    real_task = uuid4()
    real_artifact = uuid4()
    with admin_factory.begin() as connection:
        connection.execute(text("INSERT INTO environments(id,name,kind,release_locked) VALUES (:id,:name,'benchmark',true)"),
                           {"id": benchmark_environment, "name": f"phase04-canary-{benchmark_environment}"})
        connection.execute(text("INSERT INTO companies(id,environment_id,name) VALUES (:id,:env,:name)"),
                           {"id": benchmark_company, "env": benchmark_environment, "name": f"canary-{benchmark_company}"})
        connection.execute(text("INSERT INTO work_orders(id,environment_id,company_id,created_by) VALUES (:id,:env,:company,'{}'::jsonb)"),
                           {"id": benchmark_task, "env": benchmark_environment, "company": benchmark_company})
        connection.execute(text("""INSERT INTO artifacts(id,environment_id,company_id,task_id,storage_key,sha256,mime_type,size_bytes,sensitivity)
                                 VALUES (:id,:env,:company,:task,'benchmark/canary.json',:sha,'application/json',2,'internal')"""),
                           {"id": benchmark_artifact, "env": benchmark_environment, "company": benchmark_company, "task": benchmark_task, "sha": "a" * 64})
        connection.execute(text("INSERT INTO environments(id,name,kind,release_locked) VALUES (:id,:name,'real',true)"),
                           {"id": real_environment, "name": f"phase04-synthetic-real-canary-{real_environment}"})
        connection.execute(text("INSERT INTO companies(id,environment_id,name) VALUES (:id,:env,:name)"),
                           {"id": real_company, "env": real_environment, "name": f"synthetic-canary-{real_company}"})
        connection.execute(text("INSERT INTO work_orders(id,environment_id,company_id,created_by) VALUES (:id,:env,:company,'{}'::jsonb)"),
                           {"id": real_task, "env": real_environment, "company": real_company})
        connection.execute(text("""INSERT INTO artifacts(id,environment_id,company_id,task_id,storage_key,sha256,mime_type,size_bytes,sensitivity)
                                 VALUES (:id,:env,:company,:task,'real-canary/canary.json',:sha,'application/json',2,'internal')"""),
                           {"id": real_artifact, "env": real_environment, "company": real_company, "task": real_task, "sha": "b" * 64})

    second = reset_demo_dataset(app_factory)
    third = reset_demo_dataset(app_factory)
    assert first["manifest_sha256"] == second["manifest_sha256"] == third["manifest_sha256"]
    assert first["seed_version"] == 1
    assert len(third["departments"]) == 2
    assert len(third["employees"]) == 3
    tasks = {task["status"]: task for task in third["tasks"]}
    assert set(tasks) == {"draft", "executing", "awaiting_approval", "failed", "rework"}
    assert tasks["awaiting_approval"]["pending_approvals"] == 1
    assert tasks["failed"]["has_artifact"] is True
    assert [run["attempt"] for run in tasks["rework"]["runs"]] == [1, 2]
    assert all(task["usage_status"] == "unknown" and task["usd_cost_micros"] is None for task in tasks.values())
    assert third["inference_requests"] == 0

    with admin_factory.begin() as connection:
        canary = connection.execute(text("SELECT sha256, storage_key FROM artifacts WHERE id=:id"), {"id": benchmark_artifact}).mappings().one()
        assert canary == {"sha256": "a" * 64, "storage_key": "benchmark/canary.json"}
        real_canary = connection.execute(text("SELECT sha256, storage_key FROM artifacts WHERE id=:id"), {"id": real_artifact}).mappings().one()
        assert real_canary == {"sha256": "b" * 64, "storage_key": "real-canary/canary.json"}
        assert connection.execute(text("SELECT count(*) FROM environments WHERE id=:id AND kind='demo' AND release_locked"), {"id": DEMO_ENVIRONMENT_ID}).scalar_one() == 1
        connection.execute(text("DELETE FROM artifacts WHERE id=:id"), {"id": benchmark_artifact})
        connection.execute(text("DELETE FROM work_orders WHERE id=:id"), {"id": benchmark_task})
        connection.execute(text("DELETE FROM companies WHERE id=:id"), {"id": benchmark_company})
        connection.execute(text("DELETE FROM environments WHERE id=:id"), {"id": benchmark_environment})
        connection.execute(text("DELETE FROM artifacts WHERE id=:id"), {"id": real_artifact})
        connection.execute(text("DELETE FROM work_orders WHERE id=:id"), {"id": real_task})
        connection.execute(text("DELETE FROM companies WHERE id=:id"), {"id": real_company})
        connection.execute(text("DELETE FROM environments WHERE id=:id"), {"id": real_environment})
        assert connection.execute(text("SELECT count(*) FROM environments WHERE kind='real'")).scalar_one() == 0


def test_demo_reset_http_requires_confirmation_and_rejects_scope_targets(databases, monkeypatch):
    app_factory, _ = databases
    monkeypatch.setattr("agent_corporation_api.modules.demo.router.get_session_factory", lambda: app_factory)
    client = TestClient(app)
    from agent_corporation_api.modules.governance.auth import OwnerPrincipal, require_owner_write
    from agent_corporation_api.modules.demo.factory import DEMO_SCOPE
    assert client.post("/api/v1/demo/reset", json={"confirmed": True}).status_code == 403
    app.dependency_overrides[require_owner_write] = lambda: OwnerPrincipal(DEMO_SCOPE, uuid4(), "owner-local")
    try:
        rejected = client.post("/api/v1/demo/reset", json={"confirmed": False})
        assert rejected.status_code == 400
        forged = client.post("/api/v1/demo/reset", json={"confirmed": True, "environment_id": "real", "company_id": "other"})
        assert forged.status_code == 422
    finally:
        app.dependency_overrides.pop(require_owner_write, None)
    dashboard = client.get("/api/v1/demo/dashboard")
    assert dashboard.status_code == 200
    assert dashboard.json()["environment"]["kind"] == "demo"
    assert dashboard.json()["company"]["id"] == str(DEMO_COMPANY_ID)
    assert dashboard.json()["environment"]["id"] == str(DEMO_ENVIRONMENT_ID)
