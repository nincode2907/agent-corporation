"""Copy operator-owned metadata into a narrowly mounted runtime volume."""
import os
from pathlib import Path
import stat
import tempfile


def copy_secret(source: Path, destination: Path) -> None:
    descriptor = os.open(source, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    with os.fdopen(descriptor, "rb") as stream:
        info = os.fstat(stream.fileno())
        if not stat.S_ISREG(info.st_mode) or stat.S_IMODE(info.st_mode) != 0o600 or info.st_size > 16384:
            raise RuntimeError("Secret/metadata source phải là file thường mode 0600, tối đa 16 KB.")
        payload = stream.read(16385)
    fd, name = tempfile.mkstemp(prefix=".secret-", dir=destination.parent)
    temporary = Path(name)
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(payload)
            stream.flush()
            os.fsync(stream.fileno())
            os.fchown(stream.fileno(), 1000, 1000)
            os.fchmod(stream.fileno(), 0o600)
        temporary.replace(destination)
    finally:
        temporary.unlink(missing_ok=True)


def main():
    source = Path("/host-secrets")
    destination = Path("/runtime-secrets")
    if source.is_symlink() or destination.is_symlink():
        raise RuntimeError("Secret directories must not be symlinks")
    os.chown(destination, 1000, 1000)
    os.chmod(destination, 0o700)
    copy_secret(source / "owner-secret", destination / "owner-secret")
    proof = source / "cg01-proof.json"
    if proof.exists() or proof.is_symlink():
        copy_secret(proof, destination / "cg01-proof.json")
    else:
        # Removed operator proof must not survive in the runtime volume.
        (destination / "cg01-proof.json").unlink(missing_ok=True)
    print("Đã đồng bộ Owner secret/CG01 metadata; không thay nội dung hoặc cấp quyền inference.")


if __name__ == "__main__":
    main()
