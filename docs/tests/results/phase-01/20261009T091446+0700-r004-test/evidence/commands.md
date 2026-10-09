# Lệnh và kết quả — Phase 01 r004

Thời gian kiểm định: 2026-10-09 09:14–09:16 +07:00. Shell chạy qua `/Users/buivannin/.local/bin/rtk proxy`.

| Kiểm tra | Lệnh / cách làm | Kết quả |
| --- | --- | --- |
| Health unit suite | `rtk proxy uv run --project apps/api pytest apps/api/tests/test_health.py -q` | exit 0; 3 passed trong 1.06s. Source test dùng ASGI transport và monkeypatch DB probe; không kết nối hoặc ghi DB. |
| Web production build | `rtk proxy npm run --prefix apps/web build` | exit 0; TypeScript/Vite build thành công. |
| Alembic version hiện tại | `rtk proxy uv run --project apps/api alembic -c apps/api/alembic.ini current` | exit 0; `20261008_0003 (head)`. Đây chỉ là đọc version DB dùng chung, không chứng minh migration từ DB sạch. |
| Bind listener | `rtk proxy lsof -nP -iTCP:15500-15599 -sTCP:LISTEN` | Chỉ có 15500/node, 15501/Python, 15510/Docker; tất cả `127.0.0.1` IPv4. |
| Secret metadata | `rtk proxy stat -f '%Sp %N' .env`; `rtk proxy git check-ignore -v .env` | `.env` mode `0600`, bị `.gitignore` bỏ qua. Không đọc giá trị. |
| Cài frontend — đúng README | Bản sao sạch của `apps/web`; chạy từ root: `rtk proxy npm ci --prefix <temp>/web` | exit 1; npm 11.19.0 báo `EUSAGE`, `Missing: web@0.0.0 from lock file`. Không sửa lockfile hay checkout. |
| Cài frontend — cách khắc phục kiểm chứng | Trên chính bản sao sạch, cwd `<temp>/web`: `rtk proxy npm ci` | exit 0; 28 packages added, audit 0 vulnerabilities. Chỉ bản sao tạm được ghi; tự cleanup bởi TemporaryDirectory. |
| HTTP GET | Xem [routes.md](routes.md) | Các URL Phase 01 đã thử chỉ GET; không gửi model/tool request. |

Tool versions: macOS arm64; Node `v24.21.0`, npm `11.19.0`, uv `0.12.23`, Docker `20.10.23`.

Không chạy toàn bộ backend suite: test Phase 03–04 dùng DB URL của dự án và có fixture INSERT/DELETE; không an toàn với DB Phase 04 đang dùng. Không dừng DB, migrate, seed, reset hoặc gây lỗi runtime. Không gọi gateway probe/inference.
