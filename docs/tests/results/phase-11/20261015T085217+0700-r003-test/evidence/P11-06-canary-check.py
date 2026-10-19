"""Synthetic file-adapter canary matrix; prints field names, never values."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from tempfile import TemporaryDirectory

from agent_corporation_api.modules.tools.workspace import WorkspaceReader, execute_read_file


newline = chr(10)
cases = {
    "auth_basic": "Authorization: Basic basic-canary" + newline,
    "auth_bearer": "Authorization: Bearer bearer-canary" + newline,
    "proxy_auth": "Proxy-Authorization: Bearer proxy-canary" + newline,
    "cookie": "Cookie: session=cookie-canary; theme=dark" + newline,
    "set_cookie": "Set-Cookie: sid=set-canary; HttpOnly; Secure" + newline,
    "json_credentials": json.dumps(
        {
            "password": "json-pass-canary",
            "api_key": "json-key-canary",
            "credential": "json-cred-canary",
            "access_token": "json-access-token-canary",
            "secret": "json-secret-canary",
            "private_key": "json-private-key-canary",
            "token": "json-token-canary",
            "authorization": "json-auth-canary",
            "escaped_token": 'before "quoted" backslash \\ json-escaped-token-canary',
        }
    )
    + newline,
    "private_key_block": (
        "-----BEGIN PRIVATE KEY-----"
        + newline
        + "private-key-canary"
        + newline
        + "-----END PRIVATE KEY-----"
        + newline
    ),
}
canaries = {
    "auth_basic": "basic-canary",
    "auth_bearer": "bearer-canary",
    "proxy_auth": "proxy-canary",
    "cookie": "cookie-canary",
    "set_cookie": "set-canary",
    "json_password": "json-pass-canary",
    "json_api_key": "json-key-canary",
    "json_credential": "json-cred-canary",
    "json_access_token": "json-access-token-canary",
    "json_secret": "json-secret-canary",
    "json_private_key": "json-private-key-canary",
    "json_token": "json-token-canary",
    "json_authorization": "json-auth-canary",
    "json_escaped_token": "json-escaped-token-canary",
    "pem_private_key": "private-key-canary",
}

with TemporaryDirectory() as directory:
    path = Path(directory) / "synthetic-canaries.txt"
    path.write_text("".join(cases.values()), encoding="utf-8")
    with WorkspaceReader(directory) as workspace:
        result = execute_read_file(
            workspace,
            schema_version=1,
            arguments={"path": path.name},
            allowed_capabilities=frozenset({"workspace:read"}),
        )

    output = result["content"]
    leaking_cases = [name for name, value in canaries.items() if value in output]
    print(
        json.dumps(
            {
                "leaking_cases": leaking_cases,
                "sha256_present": len(result.get("sha256", "")) == 64,
                "sha256_matches_redacted_output": result.get("sha256")
                == hashlib.sha256(output.encode()).hexdigest(),
                "byte_count_matches_redacted_output": result.get("byte_count")
                == len(output.encode()),
                "redacted_output_bytes": result.get("byte_count"),
            },
            sort_keys=True,
        )
    )
