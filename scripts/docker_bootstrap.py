"""Docker-only initial setup; preserve existing local credentials."""
from pathlib import Path
import stat

from bootstrap_local import bootstrap as bootstrap_env
from bootstrap_owner import bootstrap as bootstrap_owner


def main():
    root = Path(__file__).resolve().parents[1]
    env = root / ".env"
    if env.is_symlink() or (env.exists() and not env.is_file()):
        raise RuntimeError(".env phải là file thường, không dùng symlink.")
    if (root / ".local").is_symlink():
        raise RuntimeError(".local không được là symlink.")
    bootstrap_env()
    secret = root / ".local" / "owner-secret"
    if secret.exists():
        info = secret.lstat()
        if not stat.S_ISREG(info.st_mode) or stat.S_IMODE(info.st_mode) != 0o600:
            raise RuntimeError("Owner secret phải là file thường mode 0600; giữ nguyên và kiểm tra local.")
        print("Giữ nguyên secret Owner hiện có.")
    else:
        bootstrap_owner(root)
        print("Đã bootstrap secret Owner local; không hiển thị giá trị.")


if __name__ == "__main__":
    main()
