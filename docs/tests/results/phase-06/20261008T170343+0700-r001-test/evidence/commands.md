# Lệnh và kết quả — Phase 06 r001 preflight

Shell dùng `rtk proxy`. Không khởi động/restart service, không DB writes, không HTTP POST và không inference.

| Kiểm tra | Lệnh / thao tác | Kết quả |
| --- | --- | --- |
| API sanity regression | `rtk proxy uv run --project apps/api pytest apps/api/tests/test_health.py apps/api/tests/test_codex_gateway.py -q` | Exit 0; 9 passed (0.42s) |
| Dispatcher/routes hiện có | `rtk proxy rg -n 'include_router|chat/completions|BudgetGrant|ModelCall|execution_grant_id|inference grant' apps/api/src/agent_corporation_api apps/api/migrations/versions` | Chỉ main.py đăng ký demo + codex read-only routes; chưa có execution dispatcher, BudgetGrant hoặc ModelCall; `execution_grant_id` hiện chỉ nullable ref/Work Order field |
| Gateway liveness | `rtk proxy curl -sS --max-time 3 -w '\nHTTP %{http_code}\n' http://127.0.0.1:4000/health` | Connection refused; HTTP 000 |
| Dependency/rule review | Đọc master-plan Phase 04–06, report Phase 05 r002, Phase 06 checklist, product-spec §§6, 7, 10–11, ADR D06/CG01 | Phase 04 pending, Phase 05 chưa đủ bằng chứng, CG01 blocked, grant 0 |
| Documentation HTML | `rtk proxy python3 scripts/render_plan.py` | Exit 0; đồng bộ 24 phase, 4 hoàn tất |
| Test report structure | `rtk proxy python3 docs/tests/scripts/validate.py --batch docs/tests/results/phase-06/20261008T170343+0700-r001-test` | Exit 0; 16 cases, checklist/hash/links và HTML pass. Lần đầu phát hiện link thiếu và summary count sai; đã sửa rồi chạy lại. |

Không chạy API integration suite có DB, vì không có Phase 06 code cần verify và phase đã bị chặn tại preflight. Không dùng kết quả Phase 05 fake tests làm bằng chứng model turn.
