"""Docker transport regressions; fake sockets only, no inference."""
import asyncio
from datetime import UTC, datetime, timedelta
import json
from pathlib import Path
import runpy
from types import SimpleNamespace

import pytest

from agent_corporation_api.modules.codex_gateway import adapter
from agent_corporation_api.modules.execution import gateway
from agent_corporation_api.modules.execution.gates import FILES, check_gate, gateway_fingerprint


@pytest.mark.parametrize("url", [
    "http://host.docker.internal:15600", "http://host.docker.internal:15600/",
])
def test_docker_endpoint_requires_explicit_operator_mode(url):
    with pytest.raises(ValueError):
        adapter._validated_base_url(url)
    assert adapter._validated_base_url(url, transport_mode="docker-host") == url.rstrip("/")


@pytest.mark.parametrize("url", [
    "http://host.docker.internal:15601", "https://host.docker.internal:15600",
    "http://host.docker.internal:15600/path", "http://host.docker.internal:15600?x=1",
    "http://host.docker.internal.evil:15600", "http://192.168.1.1:15600",
    "http://user:pass@host.docker.internal:15600", "http://127.0.0.1:15600",
])
def test_docker_mode_rejects_every_other_destination(url):
    with pytest.raises(ValueError):
        adapter._validated_base_url(url, transport_mode="docker-host")


def test_probe_keeps_loopback_http_host_and_disables_proxy_and_redirect(monkeypatch):
    captured = {}
    class Response:
        status = 200
        def __enter__(self): return self
        def __exit__(self, *_): pass
        def read(self, _): return b'{"ok":true}'
    class Opener:
        def open(self, request, timeout):
            captured["host"] = request.get_header("Host")
            captured["url"] = request.full_url
            return Response()
    def build(*handlers):
        captured["proxy"] = [h.proxies for h in handlers if isinstance(h, adapter.ProxyHandler)]
        captured["redirect"] = any(isinstance(h, adapter._NoRedirect) for h in handlers)
        return Opener()
    monkeypatch.setattr(adapter, "build_opener", build)
    assert adapter._get_json("http://host.docker.internal:15600/health", None)[0] == 200
    assert captured == {"host": "127.0.0.1:15600", "url": "http://host.docker.internal:15600/health", "proxy": [{}], "redirect": True}


def test_post_uses_same_bounded_docker_route_and_loopback_host(monkeypatch):
    captured = {}
    body = json.dumps({"choices": [{"message": {"content": "fixture"}}]}).encode()
    class Writer:
        def write(self, data): captured["request"] = data
        async def drain(self): pass
        def close(self): pass
        async def wait_closed(self): pass
    async def connect(host, port, **kwargs):
        captured["destination"] = (host, port)
        reader = asyncio.StreamReader()
        reader.feed_data(b"HTTP/1.1 200 OK\r\nContent-Length: " + str(len(body)).encode() + b"\r\n\r\n" + body)
        reader.feed_eof()
        return reader, Writer()
    monkeypatch.setattr(gateway.asyncio, "open_connection", connect)
    result = asyncio.run(gateway.post_text("http://host.docker.internal:15600", None, {}, 1, transport_mode="docker-host"))
    assert result.status == "completed"
    assert captured["destination"] == ("host.docker.internal", 15600)
    assert b"Host: 127.0.0.1:15600\r\n" in captured["request"]


def test_strict_proof_is_bound_to_docker_endpoint_and_transport(tmp_path):
    root = tmp_path / "gateway"
    for name in FILES:
        path = root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("fixture")
    proof = tmp_path / "proof.json"
    data = {"expires_at": (datetime.now(UTC) + timedelta(minutes=10)).isoformat(),
            "gateway_fingerprint": gateway_fingerprint(root), "evidence_refs": ["fixture:proof"],
            "isolation_verified": True, "privacy_retention_verified": True, "cancellation_verified": True,
            "gateway_base_url": "http://host.docker.internal:15600"}
    proof.write_text(json.dumps(data)); proof.chmod(0o600)
    kwargs = {"base_url": data["gateway_base_url"], "transport_mode": "docker-host"}
    assert check_gate(proof, root, **kwargs)["reason"] == "gateway_transport_mismatch"
    data["gateway_transport"] = "docker-host"
    proof.write_text(json.dumps(data))
    assert check_gate(proof, root, **kwargs)["allowed"] is True
    release_check = runpy.run_path(str(Path(__file__).resolve().parents[3] / "scripts" / "cg01_mode.py"))["release_check"]
    settings = SimpleNamespace(runtime_cg01_demo_test_override=False, runtime_gate_path=proof,
                               runtime_gateway_source_path=root, codex_server_base_url=data["gateway_base_url"],
                               codex_server_transport="docker-host")
    assert release_check(settings) == (True, "operator_evidence_verified")
