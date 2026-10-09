"""Bounded HTTP transport; cancellation closes the socket, outcome remains unknown."""
from __future__ import annotations
import asyncio
import json
from dataclasses import dataclass
from urllib.parse import urlsplit
from ..codex_gateway.adapter import _validated_base_url

MAX_BODY = 256 * 1024

@dataclass(frozen=True)
class CallOutcome:
    status: str
    reason: str
    output: str | None = None
    gateway_call_id: str | None = None
    usage: dict | None = None


def parse_response(code: int, headers: dict, body: bytes) -> CallOutcome:
    call_id = headers.get("x-codex-call-id")
    if call_id and (len(call_id) > 128 or (not call_id.isascii() or not call_id.isprintable())):
        call_id = None
    if code == 429:
        return CallOutcome("rate_limited", "gateway_429", gateway_call_id=call_id)
    if code in (400,401,403):
        return CallOutcome("failed", f"gateway_{code}", gateway_call_id=call_id)
    if code != 200:
        return CallOutcome("unknown", f"gateway_{code}", gateway_call_id=call_id)
    try:
        data = json.loads(body)
        choices = data["choices"]
        if len(choices) != 1:
            raise ValueError()
        message = choices[0]["message"]
        output = message["content"]
        if message.get("tool_calls") or not isinstance(output, str) or not output.strip():
            raise ValueError()
        usage = data.get("usage")
        required = ("prompt_tokens", "completion_tokens", "total_tokens")
        if not isinstance(usage, dict) or not all(type(usage.get(k)) is int and usage[k] >= 0 for k in required):
            usage = None
        elif usage["total_tokens"] != usage["prompt_tokens"] + usage["completion_tokens"]:
            usage = None
        else:
            preserved = {key: usage[key] for key in required}
            for key in ("prompt_tokens_details", "completion_tokens_details"):
                details = usage.get(key)
                if isinstance(details, dict):
                    preserved[key] = {k:v for k,v in details.items() if k in ("cached_tokens", "reasoning_tokens", "cache_write_tokens") and (v is None or type(v) is int and v >= 0)}
            usage = preserved
        return CallOutcome("completed", "final_response", output, call_id, usage)
    except (ValueError, TypeError, KeyError, IndexError):
        return CallOutcome("unknown", "invalid_response", gateway_call_id=call_id)


async def post_text(base_url: str, api_key: str | None, payload: dict, timeout: int) -> CallOutcome:
    parsed = urlsplit(_validated_base_url(base_url))
    body = json.dumps(payload, ensure_ascii=False).encode()
    if len(body) > 64 * 1024:
        return CallOutcome("failed", "input_too_large")
    writer = None
    try:
        async with asyncio.timeout(timeout):
            reader, writer = await asyncio.open_connection(parsed.hostname, parsed.port, limit=16384)
            host = parsed.netloc
            headers = ["POST /v1/chat/completions HTTP/1.1", f"Host: {host}", "Content-Type: application/json", "Accept: application/json", f"Content-Length: {len(body)}", "Connection: close"]
            if api_key:
                if "\r" in api_key or "\n" in api_key:
                    return CallOutcome("failed", "invalid_auth_config")
                headers.append(f"Authorization: Bearer {api_key}")
            writer.write(("\r\n".join(headers) + "\r\n\r\n").encode() + body)
            await writer.drain()
            raw = await reader.readuntil(b"\r\n\r\n")
            lines = raw.decode("iso-8859-1").split("\r\n")
            code = int(lines[0].split()[1])
            response_headers = dict((line.split(":",1)[0].lower(),line.split(":",1)[1]) for line in lines[1:] if ":" in line)
            response_headers = {key: value.strip() for key,value in response_headers.items()}
            result = bytearray()
            if response_headers.get("transfer-encoding") == "chunked":
                while True:
                    size = int((await reader.readline()).split(b";",1)[0],16)
                    if not size:
                        break
                    if size < 0 or len(result)+size > MAX_BODY:
                        return CallOutcome("unknown", "response_too_large")
                    result.extend(await reader.readexactly(size))
                    if await reader.readexactly(2) != b"\r\n":
                        raise ValueError()
            elif "content-length" in response_headers:
                size = int(response_headers["content-length"])
                if not 0 <= size <= MAX_BODY:
                    return CallOutcome("unknown", "response_too_large")
                result.extend(await reader.readexactly(size))
            else:
                while chunk := await reader.read(8192):
                    result.extend(chunk)
                    if len(result) > MAX_BODY:
                        return CallOutcome("unknown", "response_too_large")
            return parse_response(code,response_headers,bytes(result))
    except (TimeoutError, OSError, ValueError, asyncio.IncompleteReadError, asyncio.LimitOverrunError):
        return CallOutcome("unknown", "timeout_or_disconnect")
    finally:
        if writer:
            writer.close()
            try:
                async with asyncio.timeout(1):
                    await writer.wait_closed()
            except (TimeoutError, OSError):
                pass
