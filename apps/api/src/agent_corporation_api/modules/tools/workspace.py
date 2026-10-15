"""Read-only, task-rooted text access for a future isolated executor.

The workspace root must come from trusted server state. Path traversal,
symlinks, special files, and oversized/non-UTF-8 content fail closed. This is
not an OS sandbox for arbitrary code and must not be used to run commands.
"""
from __future__ import annotations

import errno
import hashlib
import os
import stat
from pathlib import Path

from ..observability.redaction import redact_text
from .registry import ToolDenied, validate_proposal


_DIRECTORY_FLAGS = os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_NOFOLLOW", 0)
_FILE_FLAGS = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)


class WorkspaceReader:
    def __init__(self, root: str | os.PathLike[str], *, max_bytes: int = 64 * 1024):
        if type(max_bytes) is not int or not 1 <= max_bytes <= 1024 * 1024:
            raise ValueError("max_bytes must be between 1 and 1048576")
        if os.open not in getattr(os, "supports_dir_fd", set()) or not getattr(os, "O_NOFOLLOW", 0):
            raise RuntimeError("safe workspace access is unavailable on this platform")
        trusted_root = Path(root).resolve(strict=True)
        if not trusted_root.is_dir():
            raise ValueError("workspace root must be a directory")
        self.root = trusted_root
        self.max_bytes = max_bytes
        self._root_fd = os.open(self.root, _DIRECTORY_FLAGS)

    def close(self) -> None:
        if self._root_fd is not None:
            os.close(self._root_fd)
            self._root_fd = None

    def __enter__(self) -> "WorkspaceReader":
        return self

    def __exit__(self, *_: object) -> None:
        self.close()

    @staticmethod
    def _parts(path: object) -> list[str]:
        if not isinstance(path, str) or not path or len(path) > 1024:
            raise ToolDenied("invalid_workspace_path")
        if path.startswith(("/", "\\")) or "\\" in path or "\x00" in path:
            raise ToolDenied("workspace_path_outside_root")
        parts = path.split("/")
        if any(part in ("", ".", "..") for part in parts):
            raise ToolDenied("workspace_path_outside_root")
        return parts

    def read_text(self, path: object) -> tuple[str, str, int]:
        if self._root_fd is None:
            raise ToolDenied("workspace_closed")
        parts = self._parts(path)
        parent_fd = os.dup(self._root_fd)
        file_fd: int | None = None
        try:
            for component in parts[:-1]:
                next_fd = os.open(component, _DIRECTORY_FLAGS, dir_fd=parent_fd)
                os.close(parent_fd)
                parent_fd = next_fd
            file_fd = os.open(parts[-1], _FILE_FLAGS, dir_fd=parent_fd)
            metadata = os.fstat(file_fd)
            if not stat.S_ISREG(metadata.st_mode):
                raise ToolDenied("workspace_target_not_regular_file")
            if metadata.st_size > self.max_bytes:
                raise ToolDenied("workspace_output_limit")
            chunks: list[bytes] = []
            remaining = self.max_bytes + 1
            while remaining:
                chunk = os.read(file_fd, min(8192, remaining))
                if not chunk:
                    break
                chunks.append(chunk)
                remaining -= len(chunk)
            raw = b"".join(chunks)
            if len(raw) > self.max_bytes:
                raise ToolDenied("workspace_output_limit")
            try:
                content = raw.decode("utf-8", errors="strict")
            except UnicodeDecodeError:
                raise ToolDenied("workspace_text_encoding_required") from None
            content = redact_text(content)
            encoded = content.encode("utf-8")
            return content, hashlib.sha256(encoded).hexdigest(), len(encoded)
        except OSError as exc:
            # Do not reflect host paths or OS error strings into tool output.
            reason = "workspace_symlink_denied" if exc.errno == errno.ELOOP else "workspace_read_denied"
            raise ToolDenied(reason) from None
        finally:
            if file_fd is not None:
                os.close(file_fd)
            os.close(parent_fd)


def execute_read_file(
    workspace: WorkspaceReader,
    *,
    schema_version: int,
    arguments: object,
    allowed_capabilities: frozenset[str],
) -> dict[str, object]:
    """Run only the read-only file adapter; no proposal is implicitly trusted."""
    definition, validated = validate_proposal(
        name="workspace.read_file",
        schema_version=schema_version,
        arguments=arguments,
        allowed_capabilities=allowed_capabilities,
    )
    content, content_hash, byte_count = workspace.read_text(validated.path)
    return {
        "tool": definition.name,
        "schema_version": definition.schema_version,
        "content": content,
        "sha256": content_hash,
        "byte_count": byte_count,
    }
