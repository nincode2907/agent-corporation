"""Explicit, audited CG01 proof lifecycle for the protected runtime volume.

Installation accepts proof bytes only on stdin; it does not create proof content.
Normal bootstrap never invokes this command. The API's strict gate remains the
only authorization decision for inference.
"""
from __future__ import annotations

import argparse
from contextlib import contextmanager
from datetime import UTC, datetime
import fcntl
import hashlib
import json
import os
from pathlib import Path
import stat
import tempfile

from agent_corporation_api.modules.execution.gates import check_gate


RUNTIME_DIR = Path("/runtime-secrets")
PROOF_PATH = RUNTIME_DIR / "cg01-proof.json"
GATEWAY_ROOT = Path("/gateway-source")
AUDIT_DIR = RUNTIME_DIR / "audit"
AUDIT_PATH = AUDIT_DIR / "cg01-proof-actions.jsonl"
LOCK_PATH = RUNTIME_DIR / ".cg01-proof-admin.lock"
BASE_URL = "http://host.docker.internal:15600"
TRANSPORT = "docker-host"


def sha256(data: bytes | None) -> str | None:
    return hashlib.sha256(data).hexdigest() if data is not None else None


def read_current() -> bytes | None:
    try:
        info = PROOF_PATH.lstat()
    except FileNotFoundError:
        return None
    if not stat.S_ISREG(info.st_mode) or stat.S_IMODE(info.st_mode) != 0o600 or info.st_uid != os.getuid():
        raise RuntimeError("runtime proof metadata is not a private regular file")
    return PROOF_PATH.read_bytes()


def gate_status(path: Path) -> dict[str, object]:
    return check_gate(path, GATEWAY_ROOT, base_url=BASE_URL, transport_mode=TRANSPORT)


def append_audit(action: str, result: str, *, before_sha256: str | None,
                 source_sha256: str | None = None, reason: str | None = None) -> None:
    AUDIT_DIR.mkdir(mode=0o700, exist_ok=True)
    if AUDIT_DIR.is_symlink():
        raise RuntimeError("CG01 audit directory must not be a symlink")
    os.chmod(AUDIT_DIR, 0o700)
    record = {
        "timestamp_utc": datetime.now(UTC).isoformat(),
        "actor": "local-operator-explicit-command",
        "action": action,
        "result": result,
        "proof_before_sha256": before_sha256,
        "source_sha256": source_sha256,
        "reason": reason,
    }
    fd = os.open(AUDIT_PATH, os.O_WRONLY | os.O_APPEND | os.O_CREAT | os.O_NOFOLLOW, 0o600)
    try:
        info = os.fstat(fd)
        if not stat.S_ISREG(info.st_mode) or info.st_uid != os.getuid() or stat.S_IMODE(info.st_mode) != 0o600:
            raise RuntimeError("CG01 audit file must be a private regular file")
        os.write(fd, (json.dumps(record, sort_keys=True) + "\n").encode())
        os.fsync(fd)
    finally:
        os.close(fd)


def confirmation(parser: argparse.ArgumentParser, supplied: str | None, expected: str) -> None:
    if supplied != expected:
        parser.error(f"explicit confirmation required: --confirm {expected}")


@contextmanager
def proof_lock():
    descriptor = os.open(LOCK_PATH, os.O_RDWR | os.O_CREAT | os.O_NOFOLLOW, 0o600)
    try:
        info = os.fstat(descriptor)
        if not stat.S_ISREG(info.st_mode) or info.st_uid != os.getuid() or stat.S_IMODE(info.st_mode) != 0o600:
            raise RuntimeError("CG01 lock must be a private regular file")
        with os.fdopen(descriptor, "r+") as lock:
            descriptor = -1
            fcntl.flock(lock, fcntl.LOCK_EX)
            yield
    finally:
        if descriptor >= 0:
            os.close(descriptor)


def install(parser: argparse.ArgumentParser, supplied_confirmation: str | None) -> int:
    confirmation(parser, supplied_confirmation, "install-cg01-proof")
    payload = os.read(0, 16385)
    if not payload or len(payload) > 16384:
        raise RuntimeError("proof input must be nonempty and at most 16 KiB")
    try:
        document = json.loads(payload)
    except (UnicodeDecodeError, json.JSONDecodeError):
        raise RuntimeError("proof input is not valid JSON") from None
    if not isinstance(document, dict):
        raise RuntimeError("proof input must be a JSON object")

    with proof_lock():
        existing = read_current()
        before_hash = sha256(existing)
        source_hash = sha256(payload)
        descriptor, temporary_name = tempfile.mkstemp(prefix=".cg01-proof-", dir=RUNTIME_DIR)
        temporary = Path(temporary_name)
        try:
            with os.fdopen(descriptor, "wb") as stream:
                stream.write(payload)
                stream.flush()
                os.fsync(stream.fileno())
                os.fchmod(stream.fileno(), 0o600)
            validation = gate_status(temporary)
            if not validation["allowed"]:
                append_audit("install", "rejected", before_sha256=before_hash,
                             source_sha256=source_hash, reason=str(validation["reason"]))
                print(f"CG01 proof not installed; strict gate remains blocked ({validation['reason']}).")
                return 1
            append_audit("install", "authorized-and-validated", before_sha256=before_hash,
                         source_sha256=source_hash, reason="operator supplied proof; runtime gate validation passed")
            os.replace(temporary, PROOF_PATH)
            os.chmod(PROOF_PATH, 0o600)
            print("CG01 proof bytes installed by explicit operator action; runtime inference still requires all separate grants/gates.")
            return 0
        finally:
            temporary.unlink(missing_ok=True)


def revoke(parser: argparse.ArgumentParser, supplied_confirmation: str | None) -> int:
    confirmation(parser, supplied_confirmation, "revoke-cg01-proof")
    with proof_lock():
        existing = read_current()
        append_audit("revoke", "requested", before_sha256=sha256(existing),
                     reason="explicit local-operator revocation")
        PROOF_PATH.unlink(missing_ok=True)
        append_audit("revoke", "completed", before_sha256=sha256(existing),
                     reason="runtime proof removed; no proof was synthesized")
    print("CG01 runtime proof revoked; strict inference gate is blocked.")
    return 0


def status() -> int:
    existing = read_current()
    if existing is None:
        validation = gate_status(PROOF_PATH)
        print(f"proof=absent allowed=false reason={validation['reason']}")
        return 0
    validation = gate_status(PROOF_PATH)
    print(f"proof=present sha256={sha256(existing)} allowed={str(validation['allowed']).lower()} reason={validation['reason']}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Explicit, audited local CG01 proof install/revoke/status")
    subparsers = parser.add_subparsers(dest="action", required=True)
    for action in ("install", "revoke"):
        sub = subparsers.add_parser(action)
        sub.add_argument("--confirm")
    subparsers.add_parser("status")
    args = parser.parse_args()
    if args.action == "install":
        return install(parser, args.confirm)
    if args.action == "revoke":
        return revoke(parser, args.confirm)
    return status()


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as error:
        raise SystemExit(f"CG01 proof operation failed: {type(error).__name__}; no secret or proof content was logged.") from None
