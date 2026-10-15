# Evidence commands — Phase 07 remake r004

- `uv run --project apps/api pytest apps/api/tests/test_phase07_feed.py -q` — exit 0, 5 passed.
- `npm run --prefix apps/web lint` — exit 0.
- `npm run --prefix apps/web build` — exit 0.
- `uv run --project apps/api python -X utf8 scripts/test_playground_isolated.py` — exit 0, 143 passed, 11 skipped; disposable PostgreSQL database/role removed.
- `git diff --check -- apps/api/src/agent_corporation_api/modules/observability/router.py apps/api/tests/test_phase07_feed.py apps/web/src/RuntimePanel.tsx` — exit 0.

All API tests used local/fake transports; no live inference, gateway call, grant, or shared DB write was performed. Browser check verified Work renders existing malformed fixture input/criteria safely; it did not simulate an SSE network drop.
