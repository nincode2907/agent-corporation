from __future__ import annotations

import json

import pytest

from agent_corporation_api.modules.tools.registry import ToolDenied, list_tools, validate_proposal
from agent_corporation_api.modules.tools.workspace import WorkspaceReader, execute_read_file


READ = frozenset({"workspace:read"})


def test_registry_is_versioned_and_does_not_advertise_unimplemented_tools():
    tools = list_tools()
    assert [(tool.name, tool.schema_version, tool.capability) for tool in tools] == [
        ("workspace.read_file", 1, "workspace:read")
    ]
    assert all(tool.side_effect is False for tool in tools)


@pytest.mark.parametrize(
    ("name", "version", "arguments", "capabilities", "reason"),
    [
        ("terminal.run", 1, {"command": "id"}, READ, "unknown_tool"),
        ("workspace.read_file", 2, {"path": "notes.txt"}, READ, "unsupported_schema_version"),
        ("workspace.read_file", 1, {"path": "notes.txt"}, frozenset(), "capability_not_granted"),
        ("workspace.read_file", 1, {"path": "notes.txt", "extra": True}, READ, "invalid_arguments"),
        ("workspace.read_file", True, {"path": "notes.txt"}, READ, "unsupported_schema_version"),
    ],
)
def test_proposals_fail_closed(name, version, arguments, capabilities, reason):
    with pytest.raises(ToolDenied) as error:
        validate_proposal(
            name=name,
            schema_version=version,
            arguments=arguments,
            allowed_capabilities=capabilities,
        )
    assert error.value.reason == reason


def test_workspace_read_returns_redacted_content_and_correlated_metadata(tmp_path):
    (tmp_path / "report.txt").write_text("Result: ok\napi_key=canary-secret\n", encoding="utf-8")
    with WorkspaceReader(tmp_path) as workspace:
        result = execute_read_file(
            workspace,
            schema_version=1,
            arguments={"path": "report.txt"},
            allowed_capabilities=READ,
        )
    assert result["content"] == "Result: ok\napi_key=[REDACTED]\n"
    assert result["byte_count"] == len(result["content"].encode())
    assert len(result["sha256"]) == 64


@pytest.mark.parametrize(
    ("content", "canaries"),
    [
        ("Authorization: Basic auth-canary\n", ("auth-canary",)),
        ("proxy-authorization: Bearer proxy-canary\n", ("proxy-canary",)),
        ("cookie=session=session-canary; theme=dark\n", ("session-canary", "theme=dark")),
        ("Set-Cookie: sid=set-cookie-canary; HttpOnly; Secure\n", ("set-cookie-canary", "HttpOnly")),
        ('{"api_key": "json-key-canary", "credential": "json-credential-canary"}',
         ("json-key-canary", "json-credential-canary")),
        ('{"token": "json-token-canary", "authorization": "json-auth-canary"}',
         ("json-token-canary", "json-auth-canary")),
        ("-----BEGIN PRIVATE KEY-----\nprivate-key-canary\n-----END PRIVATE KEY-----", ("private-key-canary",)),
    ],
)
def test_workspace_redacts_credential_formats_before_returning_file_content(tmp_path, content, canaries):
    (tmp_path / "sensitive.txt").write_text(content, encoding="utf-8")
    with WorkspaceReader(tmp_path) as workspace:
        result = execute_read_file(
            workspace,
            schema_version=1,
            arguments={"path": "sensitive.txt"},
            allowed_capabilities=READ,
        )
    assert all(canary not in result["content"] for canary in canaries)
    assert "[REDACTED]" in result["content"]
    assert result["byte_count"] == len(result["content"].encode())


def test_workspace_redacts_entire_escaped_json_secret_value(tmp_path):
    canary = "json-escaped-token-canary"
    content = json.dumps({"token": f'before "quoted" backslash \\ {canary}'})
    (tmp_path / "escaped.json").write_text(content, encoding="utf-8")
    with WorkspaceReader(tmp_path) as workspace:
        result = execute_read_file(
            workspace,
            schema_version=1,
            arguments={"path": "escaped.json"},
            allowed_capabilities=READ,
        )
    assert canary not in result["content"]
    assert result["content"] == '{"token": "[REDACTED]"}'
    assert result["sha256"]
    assert result["byte_count"] == len(result["content"].encode())


@pytest.mark.parametrize("path", ["../outside.txt", "/etc/passwd", "a/../../outside", "a\\..\\outside", "a//b"])
def test_workspace_rejects_absolute_and_traversal_paths(tmp_path, path):
    with WorkspaceReader(tmp_path) as workspace:
        with pytest.raises(ToolDenied):
            workspace.read_text(path)


def test_workspace_rejects_symlink_escape(tmp_path):
    outside = tmp_path.parent / f"outside-{tmp_path.name}.txt"
    outside.write_text("must not be read", encoding="utf-8")
    try:
        (tmp_path / "escape.txt").symlink_to(outside)
    except (OSError, NotImplementedError):
        pytest.skip("symlinks unavailable on this filesystem")
    with WorkspaceReader(tmp_path) as workspace:
        with pytest.raises(ToolDenied):
            workspace.read_text("escape.txt")


def test_workspace_rejects_symlinked_parent_and_output_overflow(tmp_path):
    outside = tmp_path.parent / f"outside-dir-{tmp_path.name}"
    outside.mkdir()
    (outside / "secret.txt").write_text("secret", encoding="utf-8")
    try:
        (tmp_path / "linked").symlink_to(outside, target_is_directory=True)
    except (OSError, NotImplementedError):
        pytest.skip("symlinks unavailable on this filesystem")
    (tmp_path / "large.txt").write_text("x" * 20, encoding="utf-8")
    with WorkspaceReader(tmp_path, max_bytes=10) as workspace:
        with pytest.raises(ToolDenied):
            workspace.read_text("linked/secret.txt")
        with pytest.raises(ToolDenied) as error:
            workspace.read_text("large.txt")
    assert error.value.reason == "workspace_output_limit"


def test_workspace_rejects_binary_and_non_file_targets(tmp_path):
    (tmp_path / "binary.bin").write_bytes(b"\xff\xfe")
    (tmp_path / "directory").mkdir()
    with WorkspaceReader(tmp_path) as workspace:
        with pytest.raises(ToolDenied) as binary:
            workspace.read_text("binary.bin")
        with pytest.raises(ToolDenied) as directory:
            workspace.read_text("directory")
    assert binary.value.reason == "workspace_text_encoding_required"
    assert directory.value.reason == "workspace_target_not_regular_file"
