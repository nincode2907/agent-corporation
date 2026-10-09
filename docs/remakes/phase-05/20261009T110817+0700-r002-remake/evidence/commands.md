# Kiểm tra trong remake Phase 05 r002

Không khởi động/restart API, PostgreSQL hoặc codex-server; không gọi inference.

| Kiểm tra | Lệnh | Kết quả |
| --- | --- | --- |
| API health + gateway | `rtk proxy uv run --project apps/api pytest apps/api/tests/test_health.py apps/api/tests/test_codex_gateway.py -q` | Exit 0; 9 passed (0.53s) |
| Web lint | `rtk proxy npm run --prefix apps/web lint` | Exit 0 |
| Web build | `rtk proxy npm run --prefix apps/web build` | Exit 0; TypeScript + Vite 8.3.3 |
| Diff whitespace | `rtk proxy git diff --check` | Exit 0 trước khi thêm evidence remake |
| Gateway/API live | Không gọi | Giữ nguyên blocker nguồn: gateway offline; không restart shared process |
