# Lệnh và kết quả đã chạy

`rtk` không có trong PATH; mọi lệnh vẫn qua `/Users/buivannin/.local/bin/rtk`. Tất cả chạy từ root repo.

| Kiểm tra | Lệnh | Exit | Kết quả |
| --- | --- | --- | --- |
| Health unit | `rtk proxy uv run --project apps/api pytest apps/api/tests/test_health.py -q` | 0 | 3 passed (0.63s) |
| Web build | `rtk proxy npm run --prefix apps/web build` | 0 | TypeScript + Vite v8.3.3 production build |
| Web lint | `rtk proxy npm run --prefix apps/web lint` | 0 | oxlint |
| Migration current | `rtk proxy uv run --project apps/api alembic -c apps/api/alembic.ini current` | 0 | 20261008_0003 (head) |
| Migration graph | `rtk proxy uv run --project apps/api alembic -c apps/api/alembic.ini history` | 0 | `<base>` → `0001` → `0002` → `0003` |
| Secret metadata | `rtk proxy stat -f '%Lp' .env` / `rtk proxy git check-ignore .env` | 0 | `600`; ignored; value never read |
| Web start | `rtk proxy npm run --prefix apps/web dev` | running | Ready in 197 ms, port 15500, visible PTY session |
| Route probes | GET only | 0 for IPv4 / 7 for IPv6 | Statuses and context in [routes.md](routes.md) |

`test_health.py` dùng ASGI in-process và mock DB success/unavailable. Không gây database outage. Alembic `current/history` chỉ đọc migration status; chain đã tới 0003 do Phase 03/04.

Không chạy `uv sync`, `npm ci` hoặc fresh PostgreSQL migration trên DB sạch: các thao tác sửa environment/DB đang được Phase 04 dùng. Không suy fresh-install PASS từ evidence lịch sử Phase 01.

Không chạy toàn bộ `apps/api/tests` vì suite hiện có test DB-writing Phase 03/04; chỉ chạy health tests cho yêu cầu Phase 01.
