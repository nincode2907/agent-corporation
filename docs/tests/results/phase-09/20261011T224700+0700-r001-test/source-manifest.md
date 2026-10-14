# Source manifest — r001

- Repository HEAD: `f74320e2ff20516ec93fbfe3413cfb953695b51d`
- Worktree: dirty; current source was re-read after the parent agent changed claim serialization to an advisory lock.
- Hash algorithm: SHA-256 over exact file bytes.

| File | SHA-256 | Status/relevance |
| --- | --- | --- |
| `apps/api/src/agent_corporation_api/modules/work/queue.py` | `0fbbd9ddb8b60e01fb4c6113209cc00c1a54f2294ebdff7fe646d32e1171da70` | Modified; Phase 09 queue/lease code. |
| `apps/api/migrations/versions/20261011_0008_queue_leases.py` | `df85d9209bcb10f392db27ee285fd7e5214aa6feefdead19f1174d323f6a438c` | Untracked; Phase 09 lease migration. |
| `apps/api/tests/test_phase09_queue_leases.py` | `bb3a8b0842b33faea23b8135e75f9ce53b9da0e56bf6d9cd55c8b438c00696d8` | Untracked; opt-in PostgreSQL tests. |
| `apps/api/tests/test_phase09_work_orders.py` | `d666a8bd628e547714d7d84bfdf23fed27eaffb904109d8fac1074d796db9baa` | Existing; focused regression tests. |
| `apps/api/migrations/versions/20261009_0007_task_queue.py` | `cee4f9254c60323d0d565146306475451f14c9afdc78bcf20c2f72df4af34a2d` | Existing migration parent for lease migration. |
| `docs/tests/phases/phase-09.md` | `bd2eb1fda372984a395defc403e53ea41e61f61bea4853948dd148a09cfc3567` | Checklist source. |
| `docs/master-plan.md` | `8c9497c53b908433702a92f6bfcf06b075a25ad959e8c75a3f514913c18581eb` | Roadmap/dependency source. |
| `docs/master-plan.md` (source at report close) | `f482269c3c054246f70052859227c907e801301bd9c45aab5957891d4e768929` | Updated by implementation agent during this review; Phase 09 remains in progress; no Phase 10 changes. |
| `docs/evidence/phase-09.md` | `bd1cfa3b91f807a7f0d564781e370f2523aa6308e99537c43d332d9217910c24` | Updated by implementation agent during review; records current unverified lease state. |
| `docs/master-plan.html` | `a8856927b77b38698415cd2ac2628ae58d4008f7fe03577b332d0c30dc275c88` | Rendered by implementation agent after the Markdown update; hash recorded at report close. |
| `docs/product-spec.md` | `de6e91effa5ac2c1e6010bee23ed81aa33048493e69cf25a2e6eaf116d59c4cf` | Product contract source. |
| `docs/decisions/0001-v1-foundation.md` | `1c38d06bdacf306d4ceac7f535702938a42b510fc24f4dabd6cc99a00739db2c` | ADR source. |
| `docs/start-windows-macos.md` | `2f7ac0d1f092e9577db51cb9f5e012e9152c8fd1b57c370123e08c415007209e` | Untracked and outside this Phase 09 review; preserved. |
