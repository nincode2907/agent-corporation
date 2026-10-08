# Commands và kết quả — Phase 05

Tất cả shell qua `/Users/buivannin/.local/bin/rtk proxy`, từ root repo trừ khi ghi khác. Không có inference grant; không chạy lệnh POST/chat/session, DB migration/reset hoặc suite có test DB-writing.

| Kiểm tra | Lệnh | Exit | Kết quả |
| --- | --- | ---: | --- |
| Gateway contract source | `rtk proxy sed -n ... codex-server/src/{server,schema,provider,config}.ts` và `docs/TECHNICAL.md` | 0 | GET health/models, Bearer optional, catalog không entitlement; no stream/max_tokens; tools là proposals; sandbox read-only không ngăn đọc user files; session JSON có messages |
| Owner identity/auth source | `rtk proxy rg -n "owner|auth|identity|actor|permission|request\.client|Authorization|api_key" apps/api/src/agent_corporation_api` | 0 | Không có auth principal/middleware; có actor kind trong command input, không đủ làm danh tính xác thực |
| Gateway runtime | `rtk proxy python3 -c ... probe_gateway(ProbeSettings())` tại `apps/api/` | 0 | status `offline`; health/catalog unavailable; không có model id |
| API unit/integration | `rtk proxy uv run --project apps/api pytest apps/api/tests/test_health.py apps/api/tests/test_codex_gateway.py -q` | 0 | 9 passed (0.77s) |
| Web lint | `rtk proxy npm run --prefix apps/web lint` | 0 | oxlint không báo lỗi |
| Web production build | `rtk proxy npm run --prefix apps/web build` | 0 | TypeScript + Vite 8.3.3; pass |
| Phase 01 README remediation | `rtk proxy python3 -c '... assert câu IPv4-only ...'` | 0 | C02 assertion PASS |
| Runtime không làm gián đoạn | `rtk proxy curl -sS -o /dev/null -w ... http://127.0.0.1:15500/settings` và `/api/v1/health/live` | 0 | web 200, API 200; không restart |

Fake adapter tests kiểm status `available`, offline, 401, 429 và schema mismatch; kiểm literal loopback rejection; kiểm spy cho đúng hai URL GET `/health` và `/v1/models`; secret canary không có trong output; `urllib` proxy từ environment bị vô hiệu và redirect bị chặn. Không test lại domain integration/DB-writing suite vì Phase 04 runtime đang dùng cùng database.
