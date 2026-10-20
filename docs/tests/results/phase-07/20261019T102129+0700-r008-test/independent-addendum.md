# Independent addendum — Phase 07 r008

- Phase / batch / round: 07 / `20261019T102129+0700-r008-test` / r008
- Reviewer: independent agent `/root/stabilization03_independent`, separate from implementation agent.
- Scope: scoped observability snapshot/feed, UI recovery source review, gateway auth-expiry/context checkpoint regression.
- Source state: shared worktree dirty; no commit. Relevant source hashes are listed below. Other concurrent Docker/config edits were outside this review scope.
- Command: `rtk proxy uv run --project apps/api python scripts/test_playground_isolated.py` (exit 0). The runner created a random named disposable PostgreSQL database and role, migrated that database to head, ran the full API suite, then dropped only that database and role.
- Result: **244 passed, 3 skipped, 1 Starlette deprecation warning**. No live runtime access, no inference, and no grant use.
- Decision/source read: [Phase 07 checklist](../../../phases/phase-07.md), [test rules](../../../RULES.md), [ADR-0004](../../../../decisions/0004-scoped-observability-snapshot.md).

## Scoped checks

| Test ID | Criterion | Result | Tag | Severity | Evidence and finding |
|---|---|---|---|---|---|
| P07-02-snapshot | Snapshot watermark and reconnect ordering across a concurrent commit | pass | clean | info | `test_snapshot_watermark_survives_concurrent_commit` injects a committed event after watermark selection, verifies it is excluded from the snapshot and returned after the signed cursor. Existing `test_stream_uses_advanced_last_event_id_on_eventsource_reconnect` covers `Last-Event-ID` selection. Both ran in the disposable full suite. |
| P07-03-snapshot | Retention gap, cursor scope/session binding and bounded response | pass | clean | info | `test_retained_snapshot_marks_unrecoverable_replay_history_and_cursor_is_bound` verifies the retained projection reports a gap and a cursor cannot cross session. `test_snapshot_size_limit_returns_explicit_413` verifies explicit 413. `test_snapshot_is_scoped_bounded_and_read_only` verifies other-company event exclusion. |
| P07-06 | Gateway auth expiry/disconnect preserves app context and does not replay an uncertain call | pass | clean | info | `test_gateway_expiry_invalidation_and_disconnect_keep_app_checkpoint_without_replay` ran 401, 403 and disconnect variants. The injected transport sees `reserved["history"]`; the request span is checkpointed with `replay_allowed=false`; no second reservation is made. This exercises the app adapter boundary with a fake transport; it does not contact codex-server or claim live gateway session behavior. The gateway contract is stateless. |
| P07-02/P07-03-ui | Browser snapshot recovery, duplicate/order handling and historical-gap display | not-run | need-change | major | Source and [authenticated browser script](../../../../reviews/stabilization-03/evidence/authenticated-recovery.mjs) were inspected. The script logs into a live app using `.local/owner-secret` and mocks event/snapshot/stream routes; it was not executed because this assignment excludes live runtime operation. Therefore no browser recovery assertion or screenshot is claimed here. Run it against an explicitly authorized runtime/test browser batch and retain sanitized artifacts. |

## Source reviewed

| File | SHA-256 |
|---|---|
| `apps/api/src/agent_corporation_api/modules/observability/feed.py` | `ee06f42364d1ebb2a5219913f5d49477036bf913d8d1458ce001c1c44c10c1b1` |
| `apps/api/src/agent_corporation_api/modules/observability/router.py` | `c71e06e84c6aaed70a1b246fb4bd342978832ec98dafa427c3678bc9bfb1cd59` |
| `apps/api/tests/test_stabilization03_snapshot.py` | `69daa75071278d811a83c8d9d65a16b7d34970561dad8929dfa4080b11d7ee23` |
| `apps/api/tests/test_phase06_runtime_persistence.py` | `56a89248116a6b1017ab966ac4c28ce5d27cc4b01570f26be074263c7f79e036` |
| `apps/web/src/RuntimePanel.tsx` | `ebdcd62f012496c49aef18fe17bb63692aabf7852e801bb4c3ad1042bda7adb5` |
| `docs/reviews/stabilization-03/evidence/authenticated-recovery.mjs` | `beaf5bb9e32a20773f03495782a11cb83df0f37b31ecf40d744b791476fb0c7d` |

## Conclusion

The scoped backend feed/snapshot and app-side gateway checkpoint checks pass in a disposable PostgreSQL suite. Phase 07 remains **not sufficient for technical completion** from this addendum because the browser recovery behavior and required live Phase 07 run/crash evidence were not exercised. This is a test-scope limitation, not a confirmed product defect. No Phase status or acceptance is changed.
