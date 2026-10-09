from fastapi.testclient import TestClient
from agent_corporation_api.main import app


def test_login_validation_never_echoes_sensitive_input():
    canary = "PRIVATE-OWNER-SECRET-CANARY"
    response = TestClient(app, base_url="http://127.0.0.1:15501").post(
        "/api/v1/owner/login", json={"secret": canary, "environment_id": "invalid-canary", "company_id": "bad"},
        headers={"Origin": "http://127.0.0.1:15500"},
    )
    assert response.status_code == 422
    assert canary not in response.text
    assert "invalid-canary" not in response.text
    assert all(set(error) == {"loc", "type", "msg"} for error in response.json()["detail"])


def test_database_failure_is_handled_without_sql_parameters(monkeypatch):
    from uuid import UUID
    from sqlalchemy.exc import StatementError
    from agent_corporation_api.modules.governance.auth import OwnerPrincipal, require_owner
    from agent_corporation_api.modules.observability.scope import CompanyScope
    from agent_corporation_api.modules.execution import router

    canary = "PRIVATE-HISTORY-DB-CANARY"
    principal = OwnerPrincipal(CompanyScope(UUID(int=1), UUID(int=2)), UUID(int=3), "owner")
    def fail(*_args):
        raise StatementError("database failure", "INSERT private_history", {"input": canary}, Exception(canary))
    monkeypatch.setattr(router, "get_session_factory", lambda: None)
    monkeypatch.setattr(router.service, "grants_list", fail)
    app.dependency_overrides[require_owner] = lambda: principal
    try:
        response = TestClient(app, base_url="http://127.0.0.1:15501").get("/api/v1/runtime/status")
        assert response.status_code == 503
        assert response.json() == {"detail": "Cơ sở dữ liệu tạm thời không khả dụng."}
        assert response.headers["cache-control"] == "no-store"
        assert canary not in response.text
    finally:
        app.dependency_overrides.pop(require_owner, None)


def test_worker_database_failure_halts_without_sensitive_traceback(monkeypatch, capsys):
    import sys
    import pytest
    from sqlalchemy.exc import StatementError
    from agent_corporation_api.modules.execution import worker

    canary = "PRIVATE-WORKER-DB-CANARY"
    async def fail(*_args):
        raise StatementError("database failure", "INSERT private_history", {"input": canary}, Exception(canary))
    monkeypatch.setattr(worker, "work", fail)
    monkeypatch.setattr(sys, "argv", ["worker", "--environment", "00000000-0000-0000-0000-000000000001", "--company", "00000000-0000-0000-0000-000000000002", "--once"])
    with pytest.raises(SystemExit) as error:
        worker.main()
    assert error.value.code == 1
    captured = capsys.readouterr()
    assert canary not in captured.err + captured.out
    assert "không phát lại call" in captured.err
