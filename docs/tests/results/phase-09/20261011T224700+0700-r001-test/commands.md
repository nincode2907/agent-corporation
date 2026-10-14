# Commands and evidence — r001

Commands were run from repository root through `rtk`. No `.env` content was read and no database URL was emitted.

| Command | Exit/result | Scope |
| --- | --- | --- |
| `rtk proxy git status --short` | exit 0 | Dirty files recorded in source manifest. |
| `rtk proxy git diff --check` | exit 0 | No whitespace errors in tracked diff. |
| `rtk proxy uv run --project apps/api pytest apps/api/tests/test_phase09_work_orders.py apps/api/tests/test_phase09_queue_leases.py -q` | exit 0; 12 passed, 2 skipped, 1 Starlette TestClient deprecation warning | Unit/schema/API regression. No database integration was enabled. |
| `rtk proxy uv run --project apps/api python -m compileall -q apps/api/src/agent_corporation_api/modules/work/queue.py apps/api/tests/test_phase09_queue_leases.py apps/api/migrations/versions/20261011_0008_queue_leases.py` | exit 0 | Python syntax/bytecode compilation only. |
| `rtk proxy python3 -X utf8 docs/tests/scripts/validate.py --batch docs/tests/results/phase-09/20261011T224700+0700-r001-test` | exit 1; stopped on a broken relative link in an existing Phase 01 report (`../../../../../../dev-hub/projects.yml`) | Full docs validator is blocked by pre-existing cross-workspace link outside Phase 09. |
| `rtk proxy python3 -X utf8 -c "import sys;from pathlib import Path;sys.path.insert(0,'docs/tests/scripts');import validate as v;p=Path('docs/tests/results/phase-09/20261011T224700+0700-r001-test/report.md');v.links(p);v.check_report(p,{*(f'C{i:02}' for i in range(1,9)),*(f'P09-{i:02}' for i in range(1,8))})"` | exit 0; own report links passed and 15 cases structurally validated | Focused local report structure only; it does not validate all docs/HTML. |
| `rtk proxy python3 -X utf8 scripts/render_plan.py` | Reported by implementation agent as completed after the Markdown update | Roadmap HTML synchronization; output/hash recorded in [source manifest](source-manifest.md). |

`test_phase09_queue_leases.py` is guarded by `PHASE_QUEUE_TEST_ISOLATED=1`. The variable was not set, so both tests skipped before fixture setup and made no database connection. No disposable PostgreSQL was positively identified; migrations/integration tests were not attempted. The passing test count does not include lease database behavior. `docs/tests/scripts/validate.py --batch` traverses links in pre-existing Markdown reports before its target report check; the failure points to a Phase 01 machine-local path, not a broken link in this r001 report.
