# Commands — Phase 07 preflight r001

| Lệnh | Exit | Kết quả |
| --- | ---: | --- |
| `rtk proxy uv run --project apps/api pytest apps/api/tests/test_health.py apps/api/tests/test_codex_gateway.py -q` | 0 | 9 passed in 0.48s; regression sanity only. |
| `rtk proxy sed -n '446,534p' docs/master-plan.md` | 0 | Phase 06 Bị chặn; Phase 07 phụ thuộc 06; scope, acceptance, log reviewed. |
| `rtk proxy sed -n '1,120p' docs/tests/phases/phase-07.md` | 0 | Dependency 06; 8 cases AC1–3 mapped. |
| `rtk proxy sed -n '260,390p' docs/product-spec.md` | 0 | Event envelope/SSE/session scope and auth contract reviewed. |
| `rtk proxy sed -n '1,180p' apps/api/src/agent_corporation_api/main.py` | 0 | Router registration reviewed; no Owner auth, event feed, or execution worker. |
| `rtk proxy python3 scripts/render_plan.py` | 0 | HTML synchronized: 24 phases, 1 complete. |
| `rtk proxy python3 docs/tests/scripts/validate.py` | 0 | All existing and current reports/links pass structural validation; limits listed in output. |

Không đọc `.env`, không truy vấn/ghi database, không gọi codex-server/model, không restart service.
