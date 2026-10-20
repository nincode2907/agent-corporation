# Agent Corporation — Integration Sprint 04

**Date:** 19/10/2026 · **Scope:** targeted Phase 07/08 integration readiness · **Verdict:** non-inference readiness advanced; IG08 remains blocked pending an explicit Owner decision and missing integration dependencies.

## Findings

- Playground messages are persisted turns, not first-class Runs. Their events have `run_id=null` and correlate to the session; see [runtime traceability](runtime-traceability.md).
- The direct bounded Runtime route can create a first-class Run and the RuntimePanel can submit one when an Owner grant and CG01 allow it. The normal Work Order queue has no bridge to that worker; Runtime Runs lack employee/profile-version identity, so Office cannot name an active employee.
- Added an isolated real-process Runtime worker crash/restart test using a fake transport. It observed a persisted heartbeat, a dispatch checkpoint, worker termination, lease recovery to `unknown`/`interrupted`, stable event sequence and no second model call/reservation. The final run's IDs and state are in [synthetic evidence](evidence/synthetic-runtime-restart.json). This is synthetic test data, not IG08.
- Replaced the stale shell badge `Cần session Owner` with the neutral requirement `Yêu cầu quyền Owner`. No authentication or authorization behavior changed.
- Current Runtime CG01 is `strict`, `verified=false`, `allowed=false`; its demo override is off. The gateway catalog snapshot reports `gpt-6-luna` and `medium` as chat-supported, but its `checked_on` is 2026-10-02 and does not establish entitlement. No current Owner profile could be read.

## Verification

- Implementation isolated PostgreSQL/API suite: **245 passed, 3 skipped, 1 existing warning**. Disposable DB/role created and removed by `scripts/test_playground_isolated.py`; shared Runtime DB was not used.
- Web production build: passed (`tsc -b && vite build`).
- Independent verification: see [independent addendum](evidence/independent-addendum.md) after completion.
- Existing Compose API/PostgreSQL/web containers were already healthy; read-only health checks passed. No container restart/rebuild or shared gateway change was made.
- Browser: current Office showed an Owner login form and current Overview reported demo fixture unavailable. No Owner secret was read or entered. Therefore no authenticated Sprint 04 Run screenshots, active-state visual check or mobile UI check are claimed. Prior Sprint 03 screenshots are historical evidence only.
- Gemini tab was signed out; no feedback is claimed. A sanitized mentor package is in [evidence](evidence/ux-review-package.md).

## Criteria status

Phase 07 r009: **11 clean / 4 blocked / 0 fail**. The worker process restart blocker is closed for the isolated fake-transport path. Network-drop UI proof and a live authorized Run remain blocked.

Phase 08 r008: **8 clean / 7 blocked / 0 fail**. Read-only scope/runtime behavior and the Owner label are verified. Employee/Run correlation, full authenticated Replay side-effect browser evidence, and IG08 live acceptance remain blocked.

No Phase 07/08 acceptance decision was made; phase statuses are unchanged. No grant, inference, live run, CG01 change, Phase 09/10 remediation, Phase 11 work, commit or push occurred.

## Changed files

- `apps/api/tests/test_phase06_runtime_persistence.py` — isolated real-subprocess worker crash/restart, heartbeat, ordered events and no-replay assertions; optional sanitized evidence output.
- `apps/web/src/App.tsx` — neutral Owner access requirement label.
- `docs/reviews/integration-04/report.md`, `runtime-traceability.md`, `ig08-rehearsal.md`, `live-test-approval.md`, `next-actions.md` — sprint findings, actual path, blocked rehearsal and proposed Owner decision.
- `docs/reviews/integration-04/evidence/commands.md`, `independent-addendum.md`, `synthetic-runtime-restart.json`, `ux-review-package.md` — command/results, final independent retest, synthetic IDs/state and sanitized mentor questions.
- `docs/tests/results/phase-07/20261019T1132+0700-r009-test/report.md` and `evidence/{commands.md,source-manifest.json}` — Phase 07 results, exact commands and source hashes.
- `docs/tests/results/phase-08/20261019T1132+0700-r008-test/report.md` and `evidence/{commands.md,source-manifest.json}` — Phase 08 results, exact commands and source hashes.
- `docs/tests/results/phase-07/README.md`, `docs/tests/results/phase-08/README.md`, `docs/master-plan.md` — round indexes and evidence-based counts; `docs/master-plan.html` rendered from Markdown.

Full commands and their boundaries: [evidence/commands.md](evidence/commands.md). The next step is an explicit Owner decision in [live-test-approval.md](live-test-approval.md), not another automated sprint.
