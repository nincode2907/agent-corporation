"""CG01 proof is trusted operator metadata, never a request-controlled override."""
from __future__ import annotations
import hashlib
import json
import os
import stat
from datetime import UTC, datetime
from pathlib import Path

FILES = ("package.json", "src/server.ts", "src/schema.ts", "src/provider.ts", "src/config.ts")


def gateway_fingerprint(root: Path) -> str:
    digest = hashlib.sha256()
    for name in FILES:
        digest.update(name.encode())
        digest.update((root/name).read_bytes())
    return digest.hexdigest()


def check_gate(path: Path, gateway_root: Path, now: datetime | None = None, base_url: str | None = None) -> dict:
    now = now or datetime.now(UTC)
    fingerprint = "unavailable"
    try:
        fingerprint = gateway_fingerprint(gateway_root)
        if path.parent.is_symlink():
            raise ValueError("untrusted_metadata")
        fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
        with os.fdopen(fd, "r") as stream:
            info = os.fstat(stream.fileno())
            if not stat.S_ISREG(info.st_mode) or info.st_uid != os.getuid() or stat.S_IMODE(info.st_mode) != 0o600 or info.st_size > 16384:
                raise ValueError("untrusted_metadata")
            proof = json.loads(stream.read(16385))
        if not isinstance(proof, dict):
            raise ValueError("invalid_metadata_type")
        if base_url is not None and proof.get("gateway_base_url") != base_url.rstrip("/"):
            raise ValueError("gateway_endpoint_mismatch")
        expiry = datetime.fromisoformat(proof["expires_at"])
        if expiry.tzinfo is None or expiry <= now:
            raise ValueError("expired_metadata")
        if proof.get("gateway_fingerprint") != fingerprint:
            raise ValueError("fingerprint_mismatch")
        if not proof.get("evidence_refs") or not isinstance(proof.get("evidence_refs"),list):
            raise ValueError("missing_evidence")
        if not all(proof.get(key) is True for key in ("isolation_verified", "privacy_retention_verified", "cancellation_verified")):
            raise ValueError("capability_unverified")
        return {"allowed":True,"reason":"operator_evidence_verified","fingerprint":fingerprint}
    except (OSError,ValueError,TypeError,KeyError) as error:
        safe_reasons={"untrusted_metadata","invalid_metadata_type","gateway_endpoint_mismatch","expired_metadata","fingerprint_mismatch","missing_evidence","capability_unverified"}
        reason = str(error) if str(error) in safe_reasons else "missing_or_invalid_proof"
        return {"allowed":False,"reason":reason,"fingerprint":fingerprint}
