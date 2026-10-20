# Integration Sprint 04 — Owner approval request for IG08 live test

## Current status

**No grant, profile change, or prompt has been created or sent.** Current local Runtime reports `mode=strict`, `verified=false`, `allowed=false`, reason `missing_or_invalid_proof`; the demo override setting is currently false. Strict CG01 therefore blocks this test today. The previously documented demo-only exception is an Owner-authorized option, but it is not enabled in the current runtime. This sprint did not toggle it or manufacture proof.

The local gateway catalog endpoint responded to a read-only `GET /api/models`. Its snapshot says `checked_on: 2026-10-02`; `gpt-6-luna` lists `chat_supported: true`, `availability: included`, and `medium` in its reasoning list. This establishes only what that stale catalog snapshot reports. It does not establish current entitlement, authentication capability, profile selection, or a current successful request. The current Owner profile could not be read because no authenticated Owner browser session was available. Gateway README documents stateless `POST /v1/chat/completions`; tools are disabled in the application request and `stream:false` is used. No live capability/entitlement probe was attempted.

## Proposed single test — requires a separate explicit Owner decision

| Field | Proposal |
|---|---|
| Runtime grant phase / batch | Phase 07 / `IG08-live-20261019-r001` (run is a Phase 07 Runtime execution observed by the Phase 08 IG08 gate) |
| Environment | Isolated demo only |
| Purpose | Demonstrate one text-only Runtime Run → saved events/SSE → Office → Inspector → Replay |
| Candidate model / effort | `gpt-6-luna` / `medium` (catalog entry only; current entitlement unverified) |
| Requests / concurrency | 1 / 1, including retries and child requests |
| Timeout / expiry | 120 seconds / 15 minutes from grant creation |
| Tools / fallback / retries | Disabled / disabled / disabled (`max_requeues=0`) |
| Input | Non-sensitive, trusted, fixed fixture to be shown in the approval decision |
| CG01 | Must be explicitly decided: strict is currently blocked; the demo-only test override would need a separate explicit authorization for this exact batch. It remains `verified=false`. |
| Stop condition | Stop on any timeout, disconnect, unknown outcome, request-count mismatch, scope mismatch or missing evidence; never resend an unknown request. |

Owner approval must separately confirm the exact Runtime grant phase (`07`), batch, model/effort, purpose/input, limits, expiry, isolated scope and CG01 mode, then create the scoped grant through an Owner-authenticated route. The existing Runtime API supports phase `07`, but its Owner UI shortcut is hardcoded to Phase 06 and cannot create this grant. Do not reuse or relabel a Phase 06 grant. If strict CG01 remains selected, no run can start until genuine proof is available. If the demo exception is selected, it is only a test override and does not prove CG01 or release readiness.

Even a successful single call proves only the happy path. It does not prove cancellation, crash recovery, usage/cost reconciliation, production isolation or all Runtime failure modes. The non-inference process test is separate evidence and remains synthetic.
