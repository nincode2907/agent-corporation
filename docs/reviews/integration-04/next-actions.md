# Integration Sprint 04 — Next actions

## Owner decision required

Review [`live-test-approval.md`](live-test-approval.md). Choose whether to authorize one Phase 07 Runtime run for the Phase 08 IG08 observation, and explicitly select the CG01 mode. The current runtime is strict and blocked; the demo-only override is off. The Runtime API accepts a Phase 07 grant, but the current UI grant shortcut is Phase 06-only. Do not create a grant or send a prompt until that exact decision and grant exist.

## Engineering dependencies

1. Before an IG08 rehearsal can show an assigned employee, add/approve a Run-to-employee and employee-profile-version contract and project it through the Runtime read model, event snapshot, Inspector and Office.
2. Decide whether Work Orders should remain non-dispatching for Phase 09 or whether a bounded, authorized queue-to-Runtime executor is approved. Implement only under a Phase 09 task; do not conflate queue lease with model-call lease.
3. When Owner authorizes the live test, recover an authenticated Owner session, use a clear Phase 07 scoped-grant flow (current one-click UI grant is Phase 06-only), verify demo scope/profile and current model capability, then capture run/task/request-span/event IDs, redacted HTTP trace, DB before/after, and authenticated desktop/mobile screenshots. Record unknown usage explicitly.
4. Re-run Phase 08 Replay filter/seek/reload with a full read-only DB snapshot and request spy, and run cross-company browser denials for currently implemented routes. There is no artifact-content route to test until one is intentionally added.
5. Preserve strict CG01 as unverified unless genuine proof passes. Before Phase 23, follow the approved strict-mode release check; this sprint did not change CG01.

No Phase 09/10 remediation or Phase 11 work was started in this sprint.
