"""Synthetic redaction matrix through the Phase 11 file adapter."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from tempfile import TemporaryDirectory

from agent_corporation_api.modules.tools.workspace import WorkspaceReader, execute_read_file


newline = chr(10)
escaped_token = 'before "quoted" backslash \\ json-escaped-token-canary'
json_fields = {
    "password": "json-pass-canary",
    "api_key": "json-key-canary",
    "credential": "json-cred-canary",
    "access_token": "json-access-token-canary",
    "secret": "json-secret-canary",
    "private_key": "json-private-key-canary",
    "token": escaped_token,
    "authorization": "json-auth-canary",
    "proxy-authorization": "json-proxy-auth-canary",
    "cookie": "json-cookie-canary",
    "set-cookie": "json-set-cookie-canary",
}
input_text = "".join(
    (
        "Authorization: Basic basic-canary" + newline,
        "Authorization: Bearer bearer-canary" + newline,
        "Proxy-Authorization: Bearer proxy-canary" + newline,
        "Cookie: session=cookie-canary; theme=dark" + newline,
        "Set-Cookie: sid=set-canary; HttpOnly; Secure" + newline,
        json.dumps(json_fields) + newline,
        "-----BEGIN PRIVATE KEY-----" + newline,
        "pem-private-key-canary" + newline,
        "-----END PRIVATE KEY-----" + newline,
    )
)
canaries = {
    "auth_basic": "basic-canary",
    "auth_bearer": "bearer-canary",
    "proxy_auth": "proxy-canary",
    "cookie_header": "cookie-canary",
    "set_cookie_header": "set-canary",
    "json_password": json_fields["password"],
    "json_api_key": json_fields["api_key"],
    "json_credential": json_fields["credential"],
    "json_access_token": json_fields["access_token"],
    "json_secret": json_fields["secret"],
    "json_private_key": json_fields["private_key"],
    "json_token_suffix": "json-escaped-token-canary",
    "json_authorization": json_fields["authorization"],
    "json_proxy_authorization": json_fields["proxy-authorization"],
    "json_cookie": json_fields["cookie"],
    "json_set_cookie": json_fields["set-cookie"],
    "pem_private_key": "pem-private-key-canary",
}

with TemporaryDirectory() as directory:
    path = Path(directory) / "synthetic-canaries.txt"
    path.write_text(input_text, encoding="utf-8")
    with WorkspaceReader(directory) as workspace:
        result = execute_read_file(
            workspace,
            schema_version=1,
            arguments={"path": path.name},
            allowed_capabilities=frozenset({"workspace:read"}),
        )

    output = result["content"]
    json_line = next((line for line in output.splitlines() if line.startswith("{")), "")
    parsed_json: dict[str, str] | None = None
    try:
        parsed_json = json.loads(json_line)
    except json.JSONDecodeError:
        pass
    leaking_cases = [name for name, value in canaries.items() if value in output]
    expected_json_keys = set(json_fields)
    print(
        json.dumps(
            {
                "leaking_cases": leaking_cases,
                "escaped_token_value_replaced_entirely": parsed_json is not None
                and parsed_json.get("token") == "[REDACTED]",
                "output_json_valid": parsed_json is not None,
                "all_json_credential_values_replaced": parsed_json is not None
                and expected_json_keys == set(parsed_json)
                and all(value == "[REDACTED]" for value in parsed_json.values()),
                "sha256_present": len(result.get("sha256", "")) == 64,
                "sha256_matches_redacted_bytes": result.get("sha256")
                == hashlib.sha256(output.encode()).hexdigest(),
                "byte_count_matches_redacted_bytes": result.get("byte_count")
                == len(output.encode()),
                "redacted_output_bytes": result.get("byte_count"),
            },
            sort_keys=True,
        )
    )
