# Independent addendum — Phase 08 r007

- Phase / batch / round: 08 / `20261019T102129+0700-r007-test` / r007
- Reviewer: independent agent `/root/stabilization03_independent`, separate from implementation agent.
- Scope: snapshot-backed replay recovery and read-only boundary; browser recovery source review.
- Source state: shared worktree dirty; no commit. Relevant source hashes are listed below. Other concurrent Docker/config edits were outside this review scope.
- Command: `rtk proxy uv run --project apps/api python scripts/test_playground_isolated.py` (exit 0). The runner created a random named disposable PostgreSQL database and role, migrated that database to head, ran the full API suite, then dropped only that database and role.
- Result: **244 passed, 3 skipped, 1 Starlette deprecation warning**. No live runtime access, no inference, and no grant use.
- Decision/source read: [Phase 08 checklist](../../../phases/phase-08.md), [test rules](../../../RULES.md), [ADR-0004](../../../../decisions/0004-scoped-observability-snapshot.md).

## Scoped checks

| Test ID | Criterion | Result | Tag | Severity | Evidence and finding |
|---|---|---|---|---|---|
| P08-03-snapshot | Snapshot read-only behavior and scope/bounds | pass | clean | info | `test_snapshot_is_scoped_bounded_and_read_only` compares scoped event and model-call counts before/after the endpoint; other-company content is absent. Source `read_snapshot` uses `REPEATABLE READ, READ ONLY` and only SELECTs, builds a bounded projection, and contains no dispatch/gateway/tool call. This check is limited to the new snapshot endpoint; it is not a full Replay DB before/after audit of all runtime state. |
| P08-03/P08-06-ui | Browser Replay recovery, history-gap and event dedup/order | not-run | need-change | major | The browser recovery script and `RuntimePanel` source were inspected. The script requires an authenticated live app and was not run under the no-live-runtime boundary. No browser screenshot or browser assertions are attributed to this report. |
| P08-06-live | Same-run live Office/Inspector reconnect and usage display | not-run | need-change | major | No authorized live run/browser evidence was available in this independent test scope. Mocked transport/unit tests do not satisfy the Phase 08 checklist’s run correlation and runtime UI criteria. |
| IG08 | Live text-only run → saved events → SSE → Office/Inspector/Replay; audit IG03 | not-run | need-change | major | Gate remains **BLOCKED** for this addendum: no current batch grant, live run, or runtime UI evidence was used. No inference was called. This report cannot provide IG08 PASS from fixture/database tests. |

## Source reviewed

| File | SHA-256 |
|---|---|
| `apps/api/src/agent_corporation_api/modules/observability/feed.py` | `ee06f42364d1ebb2a5219913f5d49477036bf913d8d1458ce001c1c44c10c1b1` |
| `apps/api/src/agent_corporation_api/modules/observability/router.py` | `c71e06e84c6aaed70a1b246fb4bd342978832ec98dafa427c3678bc9bfb1cd59` |
| `apps/api/tests/test_stabilization03_snapshot.py` | `69daa75071278d811a83c8d9d65a16b7d34970561dad8929dfa4080b11d7ee23` |
| `apps/web/src/RuntimePanel.tsx` | `ebdcd62f012496c49aef18fe17bb63692aabf7852e801bb4c3ad1042bda7adb5` |
| `docs/reviews/stabilization-03/evidence/authenticated-recovery.mjs` | `beaf5bb9e32a20773f03495782a11cb83df0f37b31ecf40d744b791476fb0c7d` |

## Conclusion

The scoped snapshot read path passed its disposable database checks. Phase 08 UI recovery, live run correlation, and IG08 remain **not sufficiently evidenced** by this addendum. That is a scope/evidence gap, not a confirmed product defect. No Phase status or acceptance is changed.
