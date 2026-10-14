# Kiểm tra trong remake r004

Tất cả lệnh qua `/Users/buivannin/.local/bin/rtk proxy` tại root. Không inference/ghi DB dùng chung hoặc thay service chung.

| Lệnh | Exit | Thực tế |
| --- | --- | --- |
| `uv run --project apps/api pytest apps/api/tests/test_codex_gateway.py apps/api/tests/test_owner_auth.py apps/api/tests/test_health.py apps/api/tests/test_sensitive_validation.py -q` | 0 | 37 passed; gồm malformed UTF8/JSON/deep nesting không500, catalog intersection, model/effort/fallback validation trước transaction, offline503 không ghi |
| `npm run --prefix apps/web lint` | 0 | oxlint đạt |
| `npm run --prefix apps/web build` | 0 | TypeScript + Vite8.3.3 đạt,19modules |
| `git diff --check` | 0 | Không whitespace errors |

Capability contract được đọc từ gateway `src/server.ts` (`/v1/models`), `src/dashboard.ts` (`GET /api/models`), `src/catalog.ts` (`chat_supported`, `reasoning`) và `src/schema.ts` (effort enums). GET `/api/models` trả snapshot checked_on2026-10-02; không đưa giá/usage vào app, không suy entitlement. API hiện mới là metadata chuẩn hóa, không inference. File gateway không bị sửa.
