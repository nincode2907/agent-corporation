# Phase 08 independent retest r004

- **Batch:** `20261015T073129+0700-r004-test`
- **Snapshot:** 2026-10-15 07:31:29 +0700
- **Scope:** Inspector and Replay against the already-saved run `100bc3c8-3944-4bed-94aa-770364161b3c`; missing-summary/usage/gap copy; C01–C08; web lint/build and isolated API regression.
- **Constraints honored:** read-only UI review only; no Owner secret/cookie inspection, grant creation, inference, replayed calls, gateway access, or runtime database writes. No product-code edits. No live Office run was started.
- **Source state:** working tree was already dirty in unrelated Phase 06/07/Playground files and in the reviewed RuntimePanel/observability sources. Hashes are recorded in `evidence/source-manifest.txt`; no changes were made by this reviewer.
- **Upstream:** Phase 06 and 07 remain blocked. The saved Phase 06 run is not Phase 08 grant evidence; grants do not carry across phases.

## Batch summary

| Result | Count |
|---|---:|
| clean | 6 |
| need-change | 0 |
| blocked | 9 |
| suggestion | 0 |
| **Total** | **15** |

Blocked means required evidence was outside this batch's authorized scope or unavailable; it is not a confirmed product defect. Detailed evidence and commands are in `evidence/`.

## Common criteria

### C01 — Scope and source identity

- Expected: review only the assigned Phase 08 scope and record the inspected source identity.
- Actual: saved-run Inspector/Replay scope only; relevant UI/API/test hashes are recorded. Workspace has concurrent dirty changes, so this is a working-tree snapshot rather than a clean commit.
- Result: `pass`; severity: `info`; tag: `clean`.
- Evidence: `evidence/source-manifest.txt`, `evidence/browser-review.md`.

### C02 — Dependency and phase boundaries

- Expected: do not treat prior phase evidence or grant as Phase 08 acceptance.
- Actual: Phase 06/07 remain blocked; the only visible saved run was created in the earlier Phase 06 scope. No Phase 08 grant or live integration was available or created.
- Result: `blocked`; severity: `info`; tag: `need-change`.
- Evidence: `evidence/browser-review.md`; [Phase 07 r005](../../phase-07/20261015T071306+0700-r005-test/report.md).

### C03 — Side-effect and inference boundary

- Expected: this review must not create app state or dispatch model/tool calls.
- Actual: UI actions only changed the Inspector/Replay view (select run, navigate, seek, reload). No send/replay execution control was used. No grant or inference was created. UI and source describe these observation views as read-only; no independent network/DB side-effect spy was run.
- Result: `pass`; severity: `info`; tag: `clean`.
- Evidence: `evidence/browser-review.md`, `evidence/commands.txt`.

### C04 — ACL and redaction

- Expected: verify Owner scope, cross-company/environment isolation and sensitive actor redaction at the required API/data layer.
- Actual: the existing Owner session displayed the demo scope and selected run. No cross-scope actor, alternate company/environment, or backend ACL-negative case was exercised in this retest.
- Result: `blocked`; severity: `info`; tag: `need-change`.
- Evidence: `evidence/browser-review.md`.

### C05 — API regression

- Expected: relevant API regression runs without touching runtime data.
- Actual: isolated runner completed **143 passed, 11 skipped, 1 warning** on a freshly created disposable `ac_pgtest_*` database/role; runner reported exact disposable resources removed and runtime data unchanged.
- Result: `pass`; severity: `info`; tag: `clean`.
- Evidence: `evidence/commands.txt`.

### C06 — Web validation

- Expected: lint and production build succeed.
- Actual: `npm run --prefix apps/web lint` and `npm run --prefix apps/web build` both exited successfully; build emitted the production Vite bundle.
- Result: `pass`; severity: `info`; tag: `clean`.
- Evidence: `evidence/commands.txt`.

### C07 — Replay evidence completeness

- Expected: demonstrate a saved timeline and verify the replay boundary without inventing events.
- Actual: UI showed the selected saved run's 10 persisted events, seek to event 32, and reload retaining cursor 10/10. No browser network inspection or DB before/after snapshot was run, so the full no-side-effect criterion remains unproven.
- Result: `blocked`; severity: `info`; tag: `need-change`.
- Evidence: `evidence/browser-review.md`.

### C08 — Reporting and status boundary

- Expected: record Phase 08 results without changing official phase status or rendering the master plan.
- Actual: r004 report/evidence and phase 08 results ledger only; no master-plan edit/render and no phase acceptance claim.
- Result: `pass`; severity: `info`; tag: `clean`.
- Evidence: this report and phase 08 README.

## Phase 08 cases

### P08-01 — Live Office

- Expected: display agent/run activity from a currently running authorized Phase 08 execution.
- Actual: the only selected target was a completed Phase 06 run. No active run was visible or started; this batch does not claim Live Office running-agent evidence.
- Result: `blocked`; severity: `info`; tag: `need-change`.
- Evidence: `evidence/browser-review.md`.

### P08-02 — Inspector

- Expected: same run identity/source across dashboard/task/org entry points, with missing tools/profile/diff information made clear.
- Actual: Inspector showed exact target run `100bc3c8-3944-4bed-94aa-770364161b3c`, completed status, model/effort, usage, outcome, task ID, and 10 related events. It explicitly says no decision summary is available, no Phase 08 tools/file diff/messages source is allowed, and the detailed profile snapshot is not provided. Cross-entry navigation from dashboard/task/org was not tested.
- Result: `blocked`; severity: `info`; tag: `need-change`.
- Evidence: `evidence/browser-review.md`.

### P08-03 — Replay is read-only

- Expected: filter, seek, reload a persisted timeline and prove no mutation/model/tool side effects.
- Actual: filtered to the requested run; saw 10 persisted events; seeking to the final event moved the cursor to 10/10; “Tải lại từ đầu” reloaded while preserving the selected run and cursor. UI says it displays committed events and gaps require reload rather than interpolation. Source wires these controls to local view state/read refresh. No replay call was executed. No network spy or database before/after comparison was available, so the complete no-side-effect assertion remains blocked.
- Result: `blocked`; severity: `info`; tag: `need-change`.
- Evidence: `evidence/browser-review.md`; `evidence/source-manifest.txt`.

### P08-04 — ACL and redaction

- Expected: validate authorized and denied scopes/actors at API and persisted-data layers.
- Actual: only the existing Owner-authenticated demo scope was viewed. Cross-company/environment and sensitive-actor tests were not run. No ACL pass is claimed.
- Result: `blocked`; severity: `info`; tag: `need-change`.
- Evidence: `evidence/browser-review.md`.

### P08-05 — Missing summary behavior

- Expected: show an explicit Plan/Decision Summary when present; clearly say when absent without exposing hidden internal reasoning.
- Actual: Inspector explicitly displayed “Chưa có summary tường minh trong event projection hiện tại.” Replay event rows without an allowed summary displayed “Chưa có trường tóm tắt được phép hiển thị.” No raw internal chain-of-thought was exposed in these views.
- Result: `pass`; severity: `info`; tag: `clean`.
- Evidence: `evidence/browser-review.md`.

### P08-06 — Reload, usage and gap wording

- Expected: preserve same-run evidence after reload and distinguish confirmed/unknown data; communicate gaps without fabricating progress.
- Actual: Inspector and Replay showed the same run. Usage was reported as 10,435 total tokens (10,354 input, 81 output); cost basis was explicitly `unknown`. Replay copy states a gap requires reload and must not be interpolated. “Tải lại từ đầu” retained the selected run and cursor. No network drop/offline/reconnect was induced, so reconnection and gap recovery during a real interruption remain unverified.
- Result: `blocked`; severity: `info`; tag: `need-change`.
- Evidence: `evidence/browser-review.md`.

### P08-07 — IG08

- Expected: Phase 08-scoped authorized real run → persisted events/SSE → Live Office/Inspector/Replay, with upstream proof.
- Actual: Phase 06/07 and their upstream evidence remain blocked; the visible completed run belongs to Phase 06 and does not transfer authorization. No Phase 08 grant or inference was requested or used. IG08 remains BLOCKED.
- Result: `blocked`; severity: `info`; tag: `need-change`.
- Evidence: `evidence/browser-review.md`; [Phase 07 r005](../../phase-07/20261015T071306+0700-r005-test/report.md).

## Verdict

**Phase 08 remains blocked.** UI read-only filtering, seek/reload, explicit missing-summary text, usage provenance display and web/API regression were observed. Inspector cross-entry coverage, replay side-effect instrumentation, ACL-negative cases, network-drop/reconnect evidence, Live Office active run and IG08 Phase 08 authorization remain unverified. These are evidence gaps in this authorized retest, not confirmed implementation defects.

No official phase status was changed. No live grant, inference, gateway access, runtime DB write, or master-plan render occurred.
