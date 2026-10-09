# Lệnh và kết quả — retest Phase 01

## Môi trường clean-room

Xem [evidence remake r001](../../../../../remakes/phase-01/20261009T085800+0700-r001-remake/evidence/commands.md) để biết chi tiết lệnh và output của clean copy:

- `rtk proxy npm ci` — PASS trong thư mục web copy sạch.
- `rtk proxy npm run build` — PASS.
- `rtk proxy uv sync --project <copy>/apps/api --locked` — PASS.
- `rtk proxy uv run --project <copy>/apps/api pytest apps/api/tests/test_health.py -q` — PASS, 3 tests.
- PostgreSQL `18.6-alpine` digest đúng `compose.yml`, container/database mới, port host ephemeral do Docker cấp trên IPv4 loopback; Alembic upgrade tới `20261008_0001`, current kiểm tra đúng head, chỉ có `alembic_version`, upgrade lặp lại PASS. Container và temp copy đã cleanup.
- Một lần gọi thử `npm ci --prefix <copy>/apps/web` từ root không dùng được ngữ cảnh lockfile của npm 11; lệnh canonical `npm ci` chạy từ chính thư mục web copy đã thành công. Đây là khác biệt cách gọi test, không phải thay đổi project/lockfile.

## Regression trên checkout hiện tại

- `rtk proxy uv run --project apps/api pytest apps/api/tests/test_health.py -q` — exit 0, 3 passed.
- `rtk proxy npm run --prefix apps/web build` — exit 0, TypeScript và Vite build thành công.
- `rtk proxy npm run --prefix apps/web lint` — exit 0, không có finding.
- GET direct/same-origin/proxy/favicon results: xem [routes](routes.md).
- `.env` metadata: mode `600`; `git check-ignore -v .env` khớp `.gitignore`. Không đọc giá trị.
- Inference/agent: grant hiện tại 0; batch không gọi gateway/model, chỉ GET health/pages và static/unit checks.
