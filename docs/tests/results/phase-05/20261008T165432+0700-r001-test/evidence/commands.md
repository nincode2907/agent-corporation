# Lệnh và kết quả — Phase 05 r001

Shell dùng `/Users/buivannin/.local/bin/rtk proxy`. Không restart API/PostgreSQL/gateway; không gọi inference.

| Kiểm tra | Lệnh / thao tác | Kết quả |
| --- | --- | --- |
| API health + gateway tests | `rtk proxy uv run --project apps/api pytest apps/api/tests/test_health.py apps/api/tests/test_codex_gateway.py -q` | Exit 0; 9 passed (1.33s) |
| Web lint | `rtk proxy npm run --prefix apps/web lint` | Exit 0; oxlint pass |
| Web build | `rtk proxy npm run --prefix apps/web build` | Exit 0; TypeScript + Vite 8.3.3 pass |
| Phase 05 API trên process đang chạy | `rtk proxy curl -sS --max-time 4 -w '\nHTTP %{http_code}\n' http://127.0.0.1:15501/api/v1/codex/probe` | Exit 0; JSON `{detail:Not Found}`, HTTP 404. Không restart server đang dùng Phase 04. |
| Codex live gateway | adapter `probe_gateway(ProbeSettings())`; output ở [live-probe](live-probe.md) | Exit 0; normalized status `offline`, cả hai GET không kết nối; không log exception/header. |
| Settings UI | Chrome, `http://127.0.0.1:15500/#settings`; click `Probe gateway` | GET route cũ trả 404; React unmount, tab thành trắng. Console ghi `TypeError: Cannot read properties of undefined (reading 'length') at App.tsx:1388:34`. Chi tiết đã lọc ở [UI finding](P05-02-ui-error.md). |

Fake adapter suite giữ nguyên 401, 429, offline, malformed catalog, external host, GET allowlist, proxy bypass/redirect deny và secret-canary checks. Không test DB-writing integrations vì PostgreSQL đang được Phase 04 dùng.
