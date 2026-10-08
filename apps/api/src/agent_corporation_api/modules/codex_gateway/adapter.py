from __future__ import annotations

import ipaddress
import json
from dataclasses import dataclass
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import HTTPRedirectHandler, ProxyHandler, Request, build_opener


TIMEOUT_SECONDS = 2.0
MAX_RESPONSE_BYTES = 256 * 1024


@dataclass(frozen=True)
class ProbeSettings:
    base_url: str = "http://127.0.0.1:4000"
    api_key: str | None = None


class _NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def _validated_base_url(value: str) -> str:
    try:
        parsed = urlsplit(value)
        address = ipaddress.ip_address(parsed.hostname or "")
        valid = (
            parsed.scheme == "http"
            and address.is_loopback
            and parsed.port is not None
            and parsed.path in ("", "/")
            and not parsed.username
            and not parsed.password
            and not parsed.query
            and not parsed.fragment
        )
    except ValueError:
        valid = False
    if not valid:
        raise ValueError("Gateway URL must be plain HTTP on a literal loopback IP and contain no path or credentials.")
    return value.rstrip("/")


def _get_json(url: str, api_key: str | None) -> tuple[int, object | None]:
    headers = {"Accept": "application/json"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    request = Request(url, headers=headers, method="GET")
    # Environment proxy variables must never route loopback traffic or its Bearer header elsewhere.
    opener = build_opener(ProxyHandler({}), _NoRedirect())
    try:
        with opener.open(request, timeout=TIMEOUT_SECONDS) as response:
            if response.status < 200 or response.status >= 300:
                return response.status, None
            body = response.read(MAX_RESPONSE_BYTES + 1)
            if len(body) > MAX_RESPONSE_BYTES:
                return response.status, None
            return response.status, json.loads(body)
    except HTTPError as error:
        return error.code, None
    except (URLError, TimeoutError, OSError, json.JSONDecodeError):
        return 0, None


def _models_shape(payload: object) -> list[str] | None:
    if not isinstance(payload, dict) or payload.get("object") != "list":
        return None
    data = payload.get("data")
    if not isinstance(data, list):
        return None
    ids: list[str] = []
    for item in data:
        if not isinstance(item, dict) or not isinstance(item.get("id"), str):
            return None
        ids.append(item["id"][:128])
    return ids


def probe_gateway(settings: ProbeSettings) -> dict[str, object]:
    """Read health and model catalog only. Never dispatch chat/session requests."""
    try:
        base_url = _validated_base_url(settings.base_url)
    except ValueError:
        return {
            "status": "configuration_error",
            "health": "unknown",
            "catalog": "unknown",
            "models": [],
            "auth_configured": bool(settings.api_key),
            "entitlement_verified": False,
            "message": "Cấu hình gateway không hợp lệ; chỉ chấp nhận IP loopback literal.",
        }

    health_code, health_payload = _get_json(f"{base_url}/health", settings.api_key)
    models_code, models_payload = _get_json(f"{base_url}/v1/models", settings.api_key)

    health_ok = health_code == 200 and isinstance(health_payload, dict) and health_payload.get("ok") is True
    models = _models_shape(models_payload) if models_code == 200 else None
    if health_code == 401 or models_code == 401:
        status_value, message = "auth_required", "Gateway yêu cầu xác thực; kiểm tra secret reference phía backend."
    elif health_code == 429 or models_code == 429:
        status_value, message = "rate_limited", "Gateway đang giới hạn yêu cầu kiểm tra; thử lại thủ công sau."
    elif health_code == 0 or models_code == 0:
        status_value, message = "offline", "Không kết nối được gateway local; kiểm tra dịch vụ mà không thay cấu hình dùng chung."
    elif not health_ok or models is None:
        status_value, message = "contract_mismatch", "Phản hồi gateway không khớp contract health/models đã xác nhận."
    else:
        status_value, message = "available", "Gateway trả lời health và catalog; catalog không xác nhận quyền dùng model."

    return {
        "status": status_value,
        "health": "ok" if health_ok else "unavailable",
        "catalog": "ok" if models is not None else "unavailable",
        "models": models or [],
        "auth_configured": bool(settings.api_key),
        "entitlement_verified": False,
        "message": message,
    }
