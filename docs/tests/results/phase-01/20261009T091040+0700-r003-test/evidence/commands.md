# Lệnh và kết quả — kiểm định độc lập Phase 01 r003

Thực thi độc lập bởi `/root/independent_phase01_test`; remake nguồn do agent `/root` thực hiện. Không gọi inference, không probe Codex Server, không đọc secret value và không sửa source sản phẩm.

## Clean-room install/build/start

- Phiên bản: Node v24.21.0/npm 11.19.0, Python 3.14.8/uv 0.12.23, Docker Server 20.10.23.
- Bản sao tạm tạo từ `apps/web` và `apps/api`; loại trừ `.env`, `node_modules`, `dist`, `.venv`.
- `npm ci` (cwd bản sao web, Node 24) — exit 0; 28 packages, 0 vulnerabilities.
- `npm run build` (bản sao web) — exit 0; TypeScript và Vite build đạt.
- `npm run lint` (bản sao web) — exit 0.
- `uv sync --project <copy>/api --locked` — exit 0; cài 35 packages theo lock.
- `uv run --project <copy>/api pytest <copy>/api/tests/test_health.py -q` — exit 0; 3 passed.
- PostgreSQL 18.6-alpine đúng digest Compose trong container mới `ac-p01-r003-db`; Docker cấp cổng loopback ephemeral `127.0.0.1:56946`, DB `p01_r003`, không gắn project volume.
- Alembic `upgrade 20261008_0001` chạy 2 lần trên DB mới — cả hai exit 0. `current` = `20261008_0001`; schema public chỉ có `alembic_version`.
- Khởi động API từ bản sao sạch tại `127.0.0.1:58670`; GET `/api/v1/health/ready` trả HTTP 200 `{"status":"ok","checks":{"database":"ok"}}` với DB cô lập. Dừng đúng tiến trình do batch tạo.
- Khởi động Vite từ bản sao sạch tại `127.0.0.1:61370`; `/` trả HTTP 200 `text/html`; `/favicon.svg` trả HTTP 200 `image/svg+xml`. Dừng đúng tiến trình do batch tạo.
- Lần cài đầu được gọi nhầm trong login shell dùng Node 16; build/lint lỗi do sai môi trường. Lần chạy lại với Node 24 theo README thành công; lỗi thiết lập đó không phản ánh source dự án.
- Tái hiện đúng command trong README bằng bản sao sạch mới từ repo root: `npm ci --prefix /tmp/ac-p01-prefix-r003.6xmgPP/web` — exit 1, npm 11.19.0 báo `EUSAGE` và `Missing: web@0.0.0 from lock file`. Sau đó chạy `npm ci` với cwd là chính thư mục `web/` đó — exit 0, 28 packages, 0 vulnerabilities. Đây là lỗi hướng dẫn setup có workaround; chưa sửa README theo yêu cầu dừng ở bước test.
- Cleanup: dừng container kiểm thử và hai tiến trình riêng; xóa bản sao `/tmp/ac-p01-r003.UwHuK2`. Không dừng/restart runtime hay DB dự án.

## Regression checkout và runtime hiện có

- `uv run --project apps/api pytest apps/api/tests/test_health.py -q` — exit 0, 3 passed.
- `npm run --prefix apps/web build` — exit 0.
- `npm run --prefix apps/web lint` — exit 0.
- `curl` GET readiness/liveness trực tiếp API `127.0.0.1:15501` và readiness qua hostname proxy `agent-corporation.localhost` — HTTP 200; body readiness ghi database `ok`.
- `stat .env` — mode `600`; `git check-ignore -v .env` — bị rule `.gitignore:1:.env` ignore. Không đọc giá trị.
