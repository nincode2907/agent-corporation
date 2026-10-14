# Source manifest — r002

- Repository HEAD: `f74320e2ff20516ec93fbfe3413cfb953695b51d`
- Worktree: dirty; implementation changes remain uncommitted. No product source was changed by this retest.
- Hash algorithm: SHA-256 over exact file bytes.

| File | SHA-256 | Status/relevance |
| --- | --- | --- |
| `apps/api/src/agent_corporation_api/modules/work/queue.py` | `0fbbd9ddb8b60e01fb4c6113209cc00c1a54f2294ebdff7fe646d32e1171da70` | Modified; Phase 09 queue lease implementation under review. |
| `apps/api/migrations/versions/20261011_0008_queue_leases.py` | `df85d9209bcb10f392db27ee285fd7e5214aa6feefdead19f1174d323f6a438c` | Untracked; lease migration; only revision graph checked. |
| `apps/api/tests/test_phase09_queue_leases.py` | `bb3a8b0842b33faea23b8135e75f9ce53b9da0e56bf6d9cd55c8b438c00696d8` | Untracked; opt-in disposable PostgreSQL tests, skipped in r002. |
| `apps/api/tests/test_phase09_work_orders.py` | `d666a8bd628e547714d7d84bfdf23fed27eaffb904109d8fac1074d796db9baa` | Existing; focused unit/API regression. |
| `docs/remakes/phase-09/20261011T225200+0700-r001-remake/remake.md` | `5c43ac51a122796968e5f34860532d1768109ca5e568a1865d650573b8ef9d35` | Remake source for r002. |
| `docs/evidence/phase-09.md` | `bd1cfa3b91f807a7f0d564781e370f2523aa6308e99537c43d332d9217910c24` | Implementation evidence; records DB/runtime gaps. |
| `docs/master-plan.md` | `f482269c3c054246f70052859227c907e801301bd9c45aab5957891d4e768929` | Status source; Phase 09 remains in progress. |
| `docs/master-plan.html` | `b00b54a5768dd24896585dfb0c55c4c4b1289df40218a6c88754aed29ee2650c` | Final fresh-render comparison passed after report r002 and README were rendered. |
| `docs/tests/phases/phase-09.md` | `bd2eb1fda372984a395defc403e53ea41e61f61bea4853948dd148a09cfc3567` | Phase checklist source. |
