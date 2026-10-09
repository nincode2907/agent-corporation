"""Create one ignored local Owner secret; never print credentials or touch the DB."""
import os
from pathlib import Path
import secrets


def bootstrap(root: Path) -> Path:
    directory = root / ".local"
    directory.mkdir(mode=0o700,exist_ok=True)
    if directory.is_symlink():
        raise RuntimeError("Owner directory must not be a symlink")
    directory.chmod(0o700)
    path = directory / "owner-secret"
    fd = os.open(path,os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW,0o600)
    with os.fdopen(fd,"w") as stream:
        stream.write(secrets.token_urlsafe(48) + "\n")
    return path

if __name__ == "__main__":
    try:
        bootstrap(Path(__file__).resolve().parents[1])
        print("Đã tạo secret Owner tại .local/owner-secret (0600); mở file local để đăng nhập, không gửi qua chat.")
    except FileExistsError:
        print("Secret Owner đã tồn tại; giữ nguyên, không xoay secret tự động.")
