# Integration Sprint 04 — independent verification addendum

**Date:** 19/10/2026 · **Result:** final independent retest passed after the test robustness edits.

An independent verifier reran the implementation's isolated PostgreSQL/API suite and web production build against the final working tree.

| Check | Result |
|---|---|
| `rtk proxy uv run --project apps/api python scripts/test_playground_isolated.py` | 245 passed, 3 skipped, 1 warning (27.71s). Disposable database and role removed. |
| `rtk proxy npm run --prefix apps/web build` | Passed. |
| Existing Docker Compose services | API, PostgreSQL and web remained healthy; read-only liveness/readiness checks passed. |
| Shared runtime | No service restart, secret access, user database write or inference. |
| Restart/no-replay assertions | Heartbeat persisted; process recovery produced unknown/interrupted state, preserved event ordering and did not redispatch the unknown call. |

The JSON artifact in this folder is synthetic test data emitted by the implementation run. The independent run did not set `IG08_EVIDENCE_PATH`; it independently verified the assertions without overwriting that artifact. This evidence does not satisfy a live Owner-authorized Run, browser network-drop test, Phase 07/08 acceptance or IG08.
