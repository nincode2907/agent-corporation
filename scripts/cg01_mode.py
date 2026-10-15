"""Toggle the local demo exception or check strict CG01 before Phase 23. No inference."""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
KEY = "RUNTIME_CG01_DEMO_TEST_OVERRIDE"


def set_mode(env_path: Path, enabled: bool) -> None:
    if env_path.is_symlink() or not env_path.is_file():
        raise ValueError("Cần .env local là file thường; bootstrap trước khi đổi chế độ.")
    # Update in place to preserve the existing ACL/mode and all other secret values.
    with env_path.open("r+", encoding="utf-8", newline="") as stream:
        lines = stream.readlines()
        pattern = re.compile(rf"^\s*(?:export\s+)?{KEY}\s*=", re.IGNORECASE)
        kept = [line for line in lines if not pattern.match(line)]
        payload = "".join(kept)
        if payload and not payload.endswith(("\n", "\r")):
            payload += "\n"
        payload += f"{KEY}={'true' if enabled else 'false'}\n"
        stream.seek(0)
        stream.write(payload)
        stream.truncate()


def release_check(settings) -> tuple[bool, str]:
    from agent_corporation_api.modules.execution.gates import check_gate

    if settings.runtime_cg01_demo_test_override:
        return False, "Ngoại lệ demo còn bật. Chuyển strict và dừng/restart worker trước Phase 23."
    state = check_gate(settings.runtime_gate_path, settings.runtime_gateway_source_path, base_url=settings.codex_server_base_url)
    return state["allowed"], state["reason"]


def main() -> int:
    # Windows console defaults may not encode Vietnamese; keep diagnostics readable.
    for output in (sys.stdout, sys.stderr):
        if hasattr(output, "reconfigure"):
            output.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description="CG01 local: mở demo, khóa lại hoặc kiểm tra trước Phase 23; không gọi AI.")
    parser.add_argument("mode", choices=("demo-test", "strict", "release-check"))
    args = parser.parse_args()
    try:
        if args.mode == "release-check":
            sys.path.insert(0, str(ROOT / "apps" / "api" / "src"))
            from agent_corporation_api.settings import get_settings

            allowed, reason = release_check(get_settings())
            print(f"CG01 release: {'PASS' if allowed else 'BLOCKED'} · {reason}")
            return 0 if allowed else 1
        set_mode(ROOT / ".env", args.mode == "demo-test")
    except (OSError, ValueError):
        print("Không đổi/kiểm tra được cấu hình CG01 local; kiểm tra .env và môi trường API. Không hiển thị secret.", file=sys.stderr)
        return 2
    print(f"CG01: {args.mode}. Khởi động lại API và worker để dùng cấu hình mới. Owner/grant/hạn mức/dừng vẫn bắt buộc.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
