# Commands and evidence — r002

All shell commands were invoked through `rtk`. No `.env` contents were read; no database URL was emitted.

| Command | Exit/result | Scope |
| --- | --- | --- |
| `rtk proxy uv run --project apps/api pytest apps/api/tests/test_phase09_work_orders.py apps/api/tests/test_phase09_queue_leases.py -q` | exit 0; 12 passed, 2 skipped, one Starlette TestClient deprecation warning | Focused Work Order/API regression; opt-in DB lease tests skipped before fixture setup. |
| `rtk proxy uv run --project apps/api python -m compileall -q apps/api/src/agent_corporation_api/modules/work/queue.py apps/api/tests/test_phase09_queue_leases.py apps/api/migrations/versions/20261011_0008_queue_leases.py` | exit 0 | Syntax compilation only. |
| `rtk proxy uv run --project apps/api alembic -c apps/api/alembic.ini history` | exit 0; `20261009_0007 -> 20261011_0008 (head)` | Migration graph only; no database connection/apply. |
| Fresh-render compare: import `scripts/render_plan.py`, point `TARGET` at a temporary file under repo root, call `build()`, compare bytes against `docs/master-plan.html`, unlink temporary file | exit 0 at initial and final check; byte-identical `True`; final renderer output: 24 phases / 1 complete | C06. Repository roadmap HTML was not written by this comparison. Final hash is in [source manifest](source-manifest.md). |
| `rtk proxy python3 -X utf8 docs/tests/scripts/validate.py --batch docs/tests/results/phase-09/20261011T225600+0700-r002-test` | exit 1; old Phase 01 report link failure at `../../../../../../dev-hub/projects.yml` | Full docs validator remains blocked outside Phase 09. |
| Focused `validate.links(report)` + `validate.check_report(report, expected C01–C08/P09-01…07)` | exit 0; 15 cases | r002 report links/structure only; does not validate full docs or HTML. |
| `rtk proxy git diff --check` | exit 0 | No whitespace errors in tracked source diff. |

The opt-in marker `PHASE_QUEUE_TEST_ISOLATED` was not set. The two skipped tests do not load fixture settings or connect to PostgreSQL. No migration, database write, worker restart, browser session or inference occurred.
