from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "apps" / "api" / "src"))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from agent_corporation_api.database import get_session_factory
from agent_corporation_api.modules.demo.factory import ensure_demo_scope, reset_demo_dataset
from agent_corporation_api.settings import get_settings


def main() -> int:
    parser = argparse.ArgumentParser(description="Khởi tạo fixture demo Phase 04 (không gọi inference).")
    parser.add_argument("--seed", action="store_true", help="Xác nhận chạy seed/reset trên database local đã cấu hình.")
    args = parser.parse_args()
    if not args.seed:
        parser.error("cần --seed rõ ràng; script không tự chạy khi khởi động ứng dụng")
    settings = get_settings()
    admin_engine = create_engine(settings.migration_database_url or settings.database_url, pool_pre_ping=True)
    admin_factory = sessionmaker(bind=admin_engine, expire_on_commit=False)
    try:
        ensure_demo_scope(admin_factory)
    finally:
        admin_engine.dispose()
    print(json.dumps(reset_demo_dataset(get_session_factory()), ensure_ascii=False, sort_keys=True, indent=2, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
