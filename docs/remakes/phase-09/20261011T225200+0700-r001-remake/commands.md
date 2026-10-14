# Commands and evidence — remake r001

| Command | Exit/result | Scope |
| --- | --- | --- |
| `rtk proxy python3 -X utf8 scripts/render_plan.py` | exit 0; 24 phases, 1 complete | Sync roadmap HTML from Markdown. |
| `rtk proxy git diff --check` | exit 0 | Whitespace validation. |
| `rtk proxy uv run --project apps/api pytest apps/api/tests/test_phase09_work_orders.py apps/api/tests/test_phase09_queue_leases.py` | exit 0; 12 passed, 2 skipped | Focused tests; integration skipped because `PHASE_QUEUE_TEST_ISOLATED` is unset. |

No migration, database write, browser demo, inference, or Phase 10 work was performed. The full docs batch validator remains blocked by the pre-existing machine-local Phase 01 link recorded in the independent r001 report.
