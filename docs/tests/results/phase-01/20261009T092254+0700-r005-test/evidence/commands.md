# Lệnh và kết quả — kiểm định độc lập Phase 01 r005

AI kiểm định: `/root/independent_phase01_test`; AI remake r004: `/root`. Node 24.21.0/npm 11.19.0, Python 3.14.8/uv 0.12.23, Docker Server 20.10.23.

## Bản sao sạch và lệnh README

- Copy `apps/web` và `apps/api` vào `/tmp/ac-p01-r005.vXLKHO/apps/`, không mang `.env`, `node_modules`, `dist` hoặc `.venv`.
- Đúng lệnh README từ root bản sao: `npm --prefix apps/web ci` — exit 0; cài 28 packages; audit 0 vulnerabilities.
- `npm --prefix apps/web run build` — exit 0; TypeScript/Vite build đạt.
- `npm --prefix apps/web run lint` — exit 0.
- `uv sync --project apps/api --locked` — exit 0; 35 packages theo lock.
- `uv run --project apps/api pytest apps/api/tests/test_health.py -q` — exit 0; 3 passed.

## Demo và DB-down trong stack cô lập

- PostgreSQL `postgres:18.6-alpine` pinned digest, container `ac-p01-r005-db`, host bind Docker cấp `127.0.0.1:53425`; không project volume. Hai DB riêng: `p01_r005_demo` và `p01_r005_baseline`.
- Demo DB: upgrade hiện hành `head` tới `20261008_0003`; provision fixed demo scope bằng migration/admin connection trong DB thử nghiệm; start API bản sao trên `127.0.0.1:56117` bằng app role test-only; seed fixture bằng POST tường minh `/api/v1/demo/reset` với `{"confirmed":true}` chỉ trên DB này. Kết quả HTTP 200, fixture `Demo Corporation`, 3 employees, 5 Work Orders. GET dashboard HTTP 200, `available=true`, `environment.kind=demo`.
- Bản sao Vite chạy trên `127.0.0.1:56118`. Chỉ trong **bản sao tạm**, proxy target được đổi sang API test port 56117; không sửa Vite config trong repo. UI mở từ `/#settings`, ban đầu cho thấy API và PostgreSQL hoạt động.
- DB-down: `docker stop ac-p01-r005-db` chỉ dừng container do test tạo; API/Vite vẫn chạy. API direct và Vite same-origin proxy: GET liveness HTTP 200 `{"status":"ok","service":"api"}`; GET readiness HTTP 503 `{"status":"degraded","checks":{"database":"unavailable"}}`; GET demo dashboard HTTP 503 với lỗi tổng quát đã lọc. Reload browser: API “Đang hoạt động”, PostgreSQL “Chưa kết nối”, thông báo “API có phản hồi nhưng readiness chưa đạt.”, dữ liệu demo không đọc được.
- Cleanup: API và Vite test process dừng; container đã dừng và tự xóa do `--rm`; copy tạm được xóa sau khi ghi evidence. Không dừng/restart API, PostgreSQL, Vite hoặc proxy của dự án.

## Migration baseline Phase 01 trên DB rỗng

- DB `p01_r005_baseline` không chứa schema demo; chạy Alembic `upgrade 20261008_0001` hai lần — cả hai exit 0.
- `alembic current` và `alembic_version.version_num` đều `20261008_0001`; bảng schema `public` duy nhất là `alembic_version`.
- Test này tách khỏi demo DB đã nâng lên `head`, không mutate DB dùng chung.

## Regression checkout và local routes

- `uv run --project apps/api pytest apps/api/tests/test_health.py -q` — 3 passed.
- `npm run --prefix apps/web build` và `npm run --prefix apps/web lint` — exit 0.
- GET web `127.0.0.1:15500`, API liveness/readiness `127.0.0.1:15501`, hostname `agent-corporation.localhost`, hostname readiness và `/favicon.svg` — HTTP 200; favicon `image/svg+xml`.
- `.env` chỉ được kiểm metadata: mode `600`; `git check-ignore -v .env` xác nhận bị ignore. Không đọc giá trị.
- Inference/gateway: không gọi, grant 0; không bấm probe.
