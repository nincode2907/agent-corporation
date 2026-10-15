"""Create one ignored local Owner secret; never print credentials or touch the DB."""
import os
from pathlib import Path
import secrets
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "apps" / "api" / "src"))
from agent_corporation_api.modules.governance.windows_acl import secure_windows_acl


def bootstrap(root: Path) -> Path:
    directory = root / ".local"
    directory.mkdir(mode=0o700,exist_ok=True)
    if directory.is_symlink():
        raise RuntimeError("Owner directory must not be a symlink")
    if os.name == "nt":
        secure_windows_acl(directory, directory=True)
    else:
        directory.chmod(0o700)
    path = directory / "owner-secret"
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_BINARY", 0)
    fd = os.open(path,flags,0o600)
    try:
        if os.name == "nt":
            secure_windows_acl(path, directory=False)
        with os.fdopen(fd,"w") as stream:
            fd = -1
            stream.write(secrets.token_urlsafe(48) + "\n")
    except BaseException:
        if fd >= 0:
            os.close(fd)
        path.unlink(missing_ok=True)
        raise
    return path

if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    try:
        bootstrap(Path(__file__).resolve().parents[1])
        print("Đã tạo secret Owner tại .local/owner-secret (0600); mở file local để đăng nhập, không gửi qua chat.")
    except FileExistsError:
        print("Secret Owner đã tồn tại; giữ nguyên, không xoay secret tự động.")
