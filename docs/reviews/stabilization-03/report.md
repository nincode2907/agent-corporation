# Agent Corporation — Stabilization Sprint 03

## Kết luận

Sprint 03 đã triển khai và kiểm chứng snapshot recovery có scope cho Phase 07; fake gateway tests xác nhận checkpoint/request correlation được giữ và inference không tự gửi lại sau session rejection hoặc disconnect. Owner đăng nhập một lần rồi điều hướng qua bảy màn hình mà không phải nhập lại secret. Browser recovery fixture xác nhận gap state, event đồng thời, dedupe, out-of-order recovery và lịch sử đã mất vẫn được báo rõ.

Kết luận kỹ thuật cho Phase 07 và Phase 08 đều **chưa đủ bằng chứng**. Phase 07 r008: **12 clean / 3 blocked / 0 fail**. Phase 08 r007: **8 clean / 7 blocked / 0 fail**; IG08 **BLOCKED** vì không có grant/live run theo phạm vi sprint. Phase status không đổi. Không có inference, grant mới, live run, Phase 11, commit hoặc push.

## Đã triển khai

- [ADR-0004](../../decisions/0004-scoped-observability-snapshot.md): Owner-scoped snapshot + watermark cursor, rationale, invariants and failure behavior.
- [Snapshot API](../../../apps/api/src/agent_corporation_api/modules/observability/router.py) and [projection reader](../../../apps/api/src/agent_corporation_api/modules/observability/feed.py): Owner session and DB scope, repeatable-read/read-only transaction, up to 200 redacted events, 20 run projections, signed cursor at watermark, 512 KiB payload cap, explicit 413/503 behavior.
- [Runtime UI recovery](../../../apps/web/src/RuntimePanel.tsx): recovers from cursor 400/409, SSE gap and ordering faults; atomically replaces run/event state, reconnects at the watermark, deduplicates IDs and reports unrecoverable Replay history gaps.
- [Snapshot integration tests](../../../apps/api/tests/test_stabilization03_snapshot.py): scope, read-only, concurrent commit, retention holes, cursor binding and size limit.
- [Gateway checkpoint tests](../../../apps/api/tests/test_phase06_runtime_persistence.py): fake 401/403/disconnect; context/request span retained; unknown outcomes are not replayed.
- Investigation and forward plan: [Owner auth UX](auth-ux-investigation.md), [recovery contract](snapshot-recovery-contract.md), [next actions](next-actions.md).

## Verification and evidence

- Isolated API suite: **244 passed, 3 skipped, 1 warning**, both implementation and independent disposable-runner executions. The runner created and removed its temporary DB/role.
- Web production build passed. Browser runner passed on Chrome 155 at 1440×900 and 390×844: Owner session navigation 7/7, 14 screenshots, 0 page errors. Synthetic stream delivered #42 after watermark 41, duplicated #42, then supplied out-of-order #44; UI replaced the projection at watermark 43 and kept the retention warning. The real read-only Owner stream showed offline and stale states and returned to connected after network/heartbeat recovery.
- Local compose runtime was rebuilt with the new API/web source. PostgreSQL retained its existing volume, migration completed, readiness returned 200. Read-only SQL before/after found no active model calls or Playground queued/dispatched turns; after browser capture there were no model-call or Playground-turn rows. Owner browser session logged out.
- Browser capture: [commands and screenshot index](evidence/commands.md), [sanitized run metadata](evidence/browser-result.json), [Office mobile](evidence/screenshots/office-before-390x844.png), [Inspector desktop](evidence/screenshots/inspector-before-1440x900.png), [Replay after recovery desktop](evidence/screenshots/replay-after-recovery-1440x900.png), [Replay after recovery mobile](evidence/screenshots/replay-after-recovery-390x844.png).
- Test batches: [Phase 07 r008](../../tests/results/phase-07/20261019T102129+0700-r008-test/report.md) and [Phase 08 r007](../../tests/results/phase-08/20261019T102129+0700-r007-test/report.md). Each has source hashes and an independent test addendum.

## Owner authentication finding

The 19/10 UI Lens secret forms were captured in a new anonymous browser context. Protected routes had no Owner cookie and returned 401; their restricted state correctly offered local login. A new authorized test Owner session succeeded, remained valid across Overview, Playground, Office, Work Orders, Inspector, Replay and Approvals, and logged out at the end. No authentication or cookie controls were changed.

The shell's `Cần session Owner` label is static route metadata and can look stale while the protected panel already shows an authenticated Owner session. This is a small UX follow-up, not a second login prompt. No Gemini feedback is claimed because no authorized Gemini integration was available.

## Remaining blockers and risks

- Phase 07: actual worker/server process restart reconciliation and a real authorized run through the event UI remain open. Lease-expiry crash recovery passed in the disposable API suite. Fake gateway tests establish no-replay policy, not gateway cancellation or resume capability.
- Phase 08: no active run was available to correlate Office→Inspector→Replay. Browser cross-company Inspector/artifact denial and a full Replay filter/seek before/after DB comparison still need evidence.
- IG08 needs a new Owner-controlled batch/grant with exact demo scope, profile/model, purpose, one request, concurrency 1, maximum 120 seconds, expiry, and CG01 mode. The procedure is in [next actions](next-actions.md). A fixture cannot pass IG08.
- Snapshot responses intentionally cap at 512 KiB. Oversized scopes return 413 and require visible recovery failure; this batch tests the API size rejection but does not exercise large real tenant data.

## Scope and handoff

The implementation respected the phase boundary and preserved existing Docker work and user-created UI Lens artifacts. Full current test details, blockers and evidence links are recorded in the Phase 07/08 batch reports and [master plan](../../master-plan.md). Sprint 03 stops here for mentor/Owner review; no phase was accepted or opened.
