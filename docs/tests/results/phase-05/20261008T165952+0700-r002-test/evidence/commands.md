# Lệnh và quan sát — Phase 05 r002

Shell qua `rtk proxy`; không restart API/PostgreSQL/codex-server, không inference.

| Kiểm tra | Lệnh / thao tác | Kết quả |
| --- | --- | --- |
| API health + gateway tests | `rtk proxy uv run --project apps/api pytest apps/api/tests/test_health.py apps/api/tests/test_codex_gateway.py -q` | Exit 0; 9 passed (0.61s) |
| Web lint | `rtk proxy npm run --prefix apps/web lint` | Exit 0; oxlint pass |
| Web build | `rtk proxy npm run --prefix apps/web build` | Exit 0; TypeScript + Vite 8.3.3 pass |
| API gateway endpoint | `rtk proxy curl -sS --max-time 4 -w '\nHTTP %{http_code}\n' http://127.0.0.1:15501/api/v1/codex/probe` | HTTP 404 `{detail: Not Found}`; API đang chạy source cũ, không restart |
| Codex gateway health | `rtk proxy curl -sS --max-time 3 -w '\nHTTP %{http_code}\n' http://127.0.0.1:4000/health` | Connect refused; HTTP 000; live gateway offline |
| Settings UI | Chrome QA tab `127.0.0.1:15500/#settings`, reload, bấm Probe gateway | Hiện thông báo HTTP 404, Settings còn hiển thị đầy đủ; xem [UI observation](P05-02-ui-error.md) |
| Diff validation | `rtk proxy git diff --check` | Exit 0 |

Screenshot browser được quan sát trực tiếp trong QA, nhưng CUA không có API lưu ảnh ra thư mục evidence. Bằng chứng text/accessibility tree giữ trong file UI observation; browser console còn log exception cũ từ lần test trước remediation (09:53–09:55Z), không xuất hiện thêm trên lần retest sau reload.
