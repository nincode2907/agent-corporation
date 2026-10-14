# Independent retest — Phase 10 — 20261014T163443+0700-r002-test

- Phase: 10; round r002; time 2026-10-14 16:34:43 Asia/Ho_Chi_Minh.
- Tester: `/root/phase06_09_independent_check`, separate from implementation agent.
- Source snapshot: current dirty worktree; [manifest](evidence/source-manifest.json).
- Supersedes: [r001](../20261014T162815+0700-r001-test/report.md). Remake source: [r001 remake](../../../../remakes/phase-10/20261014T163334+0700-r001-remake/remake.md); no product file edits by tester.
- Scope: pure evaluator/unit/API checks and read-only isolated DB schema/RLS inspection. No inference, grant, gateway, runtime, migration, DB row mutation or master-plan update.
- Result: **chưa đủ bằng chứng**. P10-01 is now clean at evaluator/unit layer; lifecycle/executor/UI cases remain blocked.

## Acceptance mapping

| Criterion | Test IDs | Outcome |
| --- | --- | --- |
| AC1 bypass denial / Owner-only configuration | P10-01, P10-06 | Evaluator/auth checks pass; executor/browser checks blocked. |
| AC2 payload/hash/scope/expiry/replay/side effects | P10-02–P10-05 | Pure negative checks and schema metadata pass; persisted lifecycle/race blocked. |
| AC3 owner audit/secrets | P10-06, P10-07 | Unit checks pass; browser/audit lifecycle blocked. |
| Demo approve then tamper and reject reuse | P10-02, P10-03 | Not run end-to-end. |
| Shared criteria | C01–C08 | Recorded below. |

## Totals

| Tag | Count |
| --- | ---: |
| clean | 6 |
| need-change | 9 |
| suggestion | 0 |

| Result | Count |
| --- | ---: |
| pass | 6 |
| fail | 0 |
| blocked | 9 |
| not-run | 0 |

## Results

### C01

- Expected: verify criteria at required layer; lack of integration evidence is not clean.
- Actual: Scope and dirty source reviewed; test changes limited to result files.
- Result: `pass`; severity: `info`; tag: `clean`.
- Evidence: [manifest](evidence/source-manifest.json), [commands](evidence/commands.md), [matrix output](evidence/permission-matrix-output.txt), [fix verification](evidence/fix-verification.md), [schema/RLS](evidence/database-schema-rls.txt).

### C02

- Expected: verify criteria at required layer; lack of integration evidence is not clean.
- Actual: Phase09 dependency remains unaccepted; current source/docs indicate unresolved worker/retry gaps.
- Result: `blocked`; severity: `major`; tag: `need-change`.
- Evidence: [manifest](evidence/source-manifest.json), [commands](evidence/commands.md), [matrix output](evidence/permission-matrix-output.txt), [fix verification](evidence/fix-verification.md), [schema/RLS](evidence/database-schema-rls.txt).

### C03

- Expected: verify criteria at required layer; lack of integration evidence is not clean.
- Actual: Required approval/tamper demo not executed.
- Result: `blocked`; severity: `major`; tag: `need-change`.
- Evidence: [manifest](evidence/source-manifest.json), [commands](evidence/commands.md), [matrix output](evidence/permission-matrix-output.txt), [fix verification](evidence/fix-verification.md), [schema/RLS](evidence/database-schema-rls.txt).

### C04

- Expected: verify criteria at required layer; lack of integration evidence is not clean.
- Actual: Unit/API route auth and evaluator guard pass; approvals module explicitly does not dispatch actions.
- Result: `pass`; severity: `info`; tag: `clean`.
- Evidence: [manifest](evidence/source-manifest.json), [commands](evidence/commands.md), [matrix output](evidence/permission-matrix-output.txt), [fix verification](evidence/fix-verification.md), [schema/RLS](evidence/database-schema-rls.txt).

### C05

- Expected: verify criteria at required layer; lack of integration evidence is not clean.
- Actual: Schema has FORCE RLS and correct scope policies, but no populated row isolation test.
- Result: `blocked`; severity: `major`; tag: `need-change`.
- Evidence: [manifest](evidence/source-manifest.json), [commands](evidence/commands.md), [matrix output](evidence/permission-matrix-output.txt), [fix verification](evidence/fix-verification.md), [schema/RLS](evidence/database-schema-rls.txt).

### C06

- Expected: verify criteria at required layer; lack of integration evidence is not clean.
- Actual: Phase checklist, product spec and roadmap reviewed; no status changed.
- Result: `pass`; severity: `info`; tag: `clean`.
- Evidence: [manifest](evidence/source-manifest.json), [commands](evidence/commands.md), [matrix output](evidence/permission-matrix-output.txt), [fix verification](evidence/fix-verification.md), [schema/RLS](evidence/database-schema-rls.txt).

### C07

- Expected: verify criteria at required layer; lack of integration evidence is not clean.
- Actual: 71 focused tests pass; prior current-source web lint/build pass; isolated schema/RLS inspected.
- Result: `pass`; severity: `info`; tag: `clean`.
- Evidence: [manifest](evidence/source-manifest.json), [commands](evidence/commands.md), [matrix output](evidence/permission-matrix-output.txt), [fix verification](evidence/fix-verification.md), [schema/RLS](evidence/database-schema-rls.txt).

### C08

- Expected: verify criteria at required layer; lack of integration evidence is not clean.
- Actual: Has source hashes, commands, exact test IDs/tags, evidence and blocker conditions.
- Result: `pass`; severity: `info`; tag: `clean`.
- Evidence: [manifest](evidence/source-manifest.json), [commands](evidence/commands.md), [matrix output](evidence/permission-matrix-output.txt), [fix verification](evidence/fix-verification.md), [schema/RLS](evidence/database-schema-rls.txt).

### P10-01

- Expected: verify criteria at required layer; lack of integration evidence is not clean.
- Actual: The initial r001 action_type/task_revision mismatch finding is fixed in current evaluator and new negative tests; focused suite and 12-case pure matrix pass. This is evaluator-level only, not executor bypass proof.
- Result: `pass`; severity: `info`; tag: `clean`.
- Evidence: [manifest](evidence/source-manifest.json), [commands](evidence/commands.md), [matrix output](evidence/permission-matrix-output.txt), [fix verification](evidence/fix-verification.md), [schema/RLS](evidence/database-schema-rls.txt).

### P10-02

- Expected: verify criteria at required layer; lack of integration evidence is not clean.
- Actual: Canonical key order/scope binding and invalid secret/float payload tests pass; persisted approval hash against real WorkOrder/Policy snapshots and tamper invalidation not run.
- Result: `blocked`; severity: `major`; tag: `need-change`.
- Evidence: [manifest](evidence/source-manifest.json), [commands](evidence/commands.md), [matrix output](evidence/permission-matrix-output.txt), [fix verification](evidence/fix-verification.md), [schema/RLS](evidence/database-schema-rls.txt).

### P10-03

- Expected: verify criteria at required layer; lack of integration evidence is not clean.
- Actual: Pure matrix denies expiry/consumed/stale hash/scope/run/policy/revision mismatches; persisted replay/stale/cross-scope side-effect evidence not run.
- Result: `blocked`; severity: `major`; tag: `need-change`.
- Evidence: [manifest](evidence/source-manifest.json), [commands](evidence/commands.md), [matrix output](evidence/permission-matrix-output.txt), [fix verification](evidence/fix-verification.md), [schema/RLS](evidence/database-schema-rls.txt).

### P10-04

- Expected: verify criteria at required layer; lack of integration evidence is not clean.
- Actual: Atomic consume/reserve double-submit concurrency requires isolated DB service/executor test; not run.
- Result: `blocked`; severity: `major`; tag: `need-change`.
- Evidence: [manifest](evidence/source-manifest.json), [commands](evidence/commands.md), [matrix output](evidence/permission-matrix-output.txt), [fix verification](evidence/fix-verification.md), [schema/RLS](evidence/database-schema-rls.txt).

### P10-05

- Expected: verify criteria at required layer; lack of integration evidence is not clean.
- Actual: Executor stop/policy epoch race and in-flight/unknown outcome not exercised.
- Result: `blocked`; severity: `major`; tag: `need-change`.
- Evidence: [manifest](evidence/source-manifest.json), [commands](evidence/commands.md), [matrix output](evidence/permission-matrix-output.txt), [fix verification](evidence/fix-verification.md), [schema/RLS](evidence/database-schema-rls.txt).

### P10-06

- Expected: verify criteria at required layer; lack of integration evidence is not clean.
- Actual: Owner auth suite passes; browser Host/Origin/CSRF/cookie/session mutation and actual actor scope not independently exercised.
- Result: `blocked`; severity: `major`; tag: `need-change`.
- Evidence: [manifest](evidence/source-manifest.json), [commands](evidence/commands.md), [matrix output](evidence/permission-matrix-output.txt), [fix verification](evidence/fix-verification.md), [schema/RLS](evidence/database-schema-rls.txt).

### P10-07

- Expected: verify criteria at required layer; lack of integration evidence is not clean.
- Actual: Secret-ref/redaction unit coverage passes; empty/history/decision status UI and persisted audit actor/hash plus deny-no-side-effect not tested.
- Result: `blocked`; severity: `major`; tag: `need-change`.
- Evidence: [manifest](evidence/source-manifest.json), [commands](evidence/commands.md), [matrix output](evidence/permission-matrix-output.txt), [fix verification](evidence/fix-verification.md), [schema/RLS](evidence/database-schema-rls.txt).

## Handoff

No separate IG gate. Phase10 remains **not technically complete**: approval persistence, DB row isolation, atomic replay/consume, executor enforcement, stop race and UI evidence remain blocked. See [blockers](evidence/blockers.md). No phase acceptance/status update.
