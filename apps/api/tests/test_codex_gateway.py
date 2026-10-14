import asyncio

import httpx
import pytest
from types import SimpleNamespace
from urllib.request import ProxyHandler, Request

from agent_corporation_api.modules.codex_gateway import adapter
from agent_corporation_api import main


def get_probe() -> httpx.Response:
    async def send() -> httpx.Response:
        transport = httpx.ASGITransport(app=main.app)
        async with httpx.AsyncClient(transport=transport, base_url="http://testserver") as client:
            return await client.get("/api/v1/codex/probe")

    return asyncio.run(send())


def test_probe_reads_only_allowlisted_get_endpoints_and_does_not_expose_auth(monkeypatch) -> None:
    calls: list[tuple[str, str | None]] = []

    def response(url: str, api_key: str | None):
        calls.append((url, api_key))
        if url.endswith("/health"):
            return 200, {"ok": True, "provider": "codex", "active_requests": 0}
        return 200, {"object": "list", "data": [{"id": "catalog-model", "owned_by": "local-codex"}]}

    monkeypatch.setattr(adapter, "_get_json", response)
    result = adapter.probe_gateway(adapter.ProbeSettings(api_key="secret-canary"))

    assert calls == [
        ("http://127.0.0.1:15600/health", "secret-canary"),
        ("http://127.0.0.1:15600/v1/models", "secret-canary"),
    ]
    assert result["status"] == "available"
    assert result["models"] == ["catalog-model"]
    assert result["entitlement_verified"] is False
    assert "secret-canary" not in repr(result)


def test_probe_reports_offline_without_leaking_transport_error(monkeypatch) -> None:
    monkeypatch.setattr(adapter, "_get_json", lambda _url, _key: (0, None))

    result = adapter.probe_gateway(adapter.ProbeSettings())

    assert result["status"] == "offline"
    assert "secret" not in repr(result).lower()


def test_probe_maps_auth_rate_limit_and_schema_mismatch(monkeypatch) -> None:
    scenarios = [
        ((401, None), (401, None), "auth_required"),
        ((200, {"ok": True}), (429, None), "rate_limited"),
        ((200, {"ok": True}), (200, {"data": []}), "contract_mismatch"),
    ]
    for health, models, expected in scenarios:
        calls = iter((health, models))
        monkeypatch.setattr(adapter, "_get_json", lambda _url, _key: next(calls))
        assert adapter.probe_gateway(adapter.ProbeSettings())["status"] == expected


def test_probe_rejects_non_loopback_and_never_opens_it(monkeypatch) -> None:
    monkeypatch.setattr(adapter, "_get_json", lambda *_args: (_ for _ in ()).throw(AssertionError("network call")))

    result = adapter.probe_gateway(adapter.ProbeSettings(base_url="http://example.com:4000"))

    assert result["status"] == "configuration_error"
    assert result["models"] == []


def test_http_get_bypasses_environment_proxies_and_uses_no_redirects(monkeypatch) -> None:
    captured: dict[str, object] = {}

    class Response:
        status = 200

        def __enter__(self):
            return self

        def __exit__(self, *_args):
            return False

        def read(self, _limit: int) -> bytes:
            return b'{"ok":true}'

    class Opener:
        def open(self, request: Request, timeout: float):
            captured["method"] = request.get_method()
            captured["auth"] = request.get_header("Authorization")
            captured["timeout"] = timeout
            return Response()

    def build(*handlers):
        captured["proxy_maps"] = [handler.proxies for handler in handlers if isinstance(handler, ProxyHandler)]
        captured["redirect_disabled"] = any(isinstance(handler, adapter._NoRedirect) for handler in handlers)
        return Opener()

    monkeypatch.setattr(adapter, "build_opener", build)

    status, payload = adapter._get_json("http://127.0.0.1:4000/health", "secret-canary")

    assert status == 200 and payload == {"ok": True}
    assert captured["method"] == "GET"
    assert captured["auth"] == "Bearer secret-canary"
    assert captured["proxy_maps"] == [{}]
    assert captured["redirect_disabled"] is True
    assert captured["timeout"] == adapter.TIMEOUT_SECONDS


def test_api_probe_is_manual_and_sanitized(monkeypatch) -> None:
    monkeypatch.setattr(adapter, "_get_json", lambda _url, _key: (0, None))

    response = get_probe()

    assert response.status_code == 200
    assert response.json()["status"] == "offline"
    assert "token" not in response.text.lower()


@pytest.mark.parametrize("body", [b"\xff", b"not-json", b"[" * 2000 + b"0" + b"]" * 2000])
def test_malformed_json_or_encoding_is_normalized_instead_of_http_500(monkeypatch, body) -> None:
    from agent_corporation_api.modules.codex_gateway import router

    class Response:
        status = 200
        def __enter__(self): return self
        def __exit__(self, *_args): return False
        def read(self, _limit): return body

    class Opener:
        def open(self, _request, timeout): return Response()

    monkeypatch.setattr(adapter, "build_opener", lambda *_args: Opener())
    monkeypatch.setattr(router, "get_settings", lambda: SimpleNamespace(codex_server_base_url="http://127.0.0.1:15600", codex_server_api_key=None))
    response = get_probe()
    assert response.status_code == 200
    assert response.json()["status"] == "contract_mismatch"


def test_profile_capabilities_intersect_live_catalog_and_model_efforts(monkeypatch):
    calls = []
    def response(url, _key):
        calls.append(url)
        if url.endswith("/v1/models"):
            return 200, {"object": "list", "data": [{"id": "supported"}, {"id": "disabled"}]}
        return 200, {"models": [
            {"id": "supported", "chat_supported": True, "reasoning": ["low", "max"], "price": "ignored-canary"},
            {"id": "disabled", "chat_supported": False, "reasoning": ["low"]},
            {"id": "not-live", "chat_supported": True, "reasoning": ["high"]},
        ]}
    monkeypatch.setattr(adapter, "_get_json", response)
    result = adapter.profile_model_capabilities(adapter.ProbeSettings())
    assert result == {"supported": ["low", "max"]}
    assert calls == ["http://127.0.0.1:15600/v1/models", "http://127.0.0.1:15600/api/models"]
    assert "ignored-canary" not in repr(result)


@pytest.mark.parametrize("item", [
    {"id": "model", "chat_supported": True, "reasoning": [None]},
    {"id": "model", "chat_supported": True, "reasoning": ["new-unknown-effort"]},
    {"id": "model", "chat_supported": "true", "reasoning": ["low"]},
])
def test_profile_capabilities_fail_closed_on_schema_change(monkeypatch, item):
    def response(url, _key):
        return (200, {"object": "list", "data": [{"id": "model"}]}) if url.endswith("/v1/models") else (200, {"models": [item]})
    monkeypatch.setattr(adapter, "_get_json", response)
    assert adapter.profile_model_capabilities(adapter.ProbeSettings()) is None
