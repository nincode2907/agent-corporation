# Evidence remake r001

- `rtk proxy uv run --project apps/api pytest apps/api/tests -q` — 102 passed, 10 skipped.
- `rtk proxy npm run --prefix apps/web lint` — pass.
- `rtk proxy npm run --prefix apps/web build` — pass.
- `rtk proxy uv run --project apps/api python -m compileall -q apps/api/src/agent_corporation_api` — pass.
- `rtk proxy git diff --check` — pass.

The independent AI tester must separately verify action type and task revision mismatches against the current source. The test suite is evidence of the change, not a substitute for that retest.
