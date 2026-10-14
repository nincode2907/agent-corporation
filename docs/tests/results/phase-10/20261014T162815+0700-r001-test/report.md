# Independent test — Phase 10 — 20261014T162815+0700-r001-test

- Phase: 10; round `001`; run 2026-10-14 16:28:15–16:31:22 Asia/Ho_Chi_Minh.
- Tester: `/root/phase06_09_independent_check`, independent; no product edits.
- Scope: current source/UI regression and safe local checks; Phase10 also read-only schema/RLS checks against explicitly authorized isolated DB. No inference/grant/gateway, app runtime, migration, row mutation or master-plan changes.
- Source: dirty shared worktree; see [manifest](evidence/source-manifest.json). Commands: [evidence](evidence/commands.md).
- Supersedes: No prior batch. Remake source: none. Technical result: **cần sửa**.

## Acceptance mapping

| Criterion | IDs | Outcome |
| --- | --- | --- |
| AC1 bypass/Owner config | P10-01, P10-06 | Initial evaluator issue found; auth checks pass, executor/browser blocked. |
| AC2 hash/scope/replay/side effect | P10-02–P10-05 | Pure negatives + schema metadata; persisted lifecycle/race blocked. |
| AC3 owner audit/secrets | P10-06, P10-07 | Auth/secret unit tests; browser/audit lifecycle blocked. |
| Required approve/tamper demo | P10-02, P10-03 | Not run end-to-end. |
| Common criteria | C01–C08 | All recorded below. |

## Totals

| Tag | Count |
| --- | ---: |
| clean | 4 |
| need-change | 11 |
| suggestion | 0 |

| Result | Count |
| --- | ---: |
| pass | 5 |
| fail | 1 |
| blocked | 10 |
| not-run | 0 |

## Test results

### C01

- Source: [RULES §5](../../../RULES.md). Required: yes.
- Expected: verify at the required layer with evidence; missing proof is not clean.
- Actual: Dirty Phase10 implementation belongs to parent; tester only created test evidence.
- Result: `pass`; severity: `info`; tag: `clean`.
- Evidence: [manifest](evidence/source-manifest.json), [commands](evidence/commands.md), [source/UI review](evidence/current-source-ui-regression.md), [database schema/RLS](evidence/database-schema-rls.txt).
- Follow-up: None.

### C02

- Source: [RULES §5](../../../RULES.md). Required: yes.
- Expected: verify at the required layer with evidence; missing proof is not clean.
- Actual: Phase09 dependency unaccepted; worker/retry gaps remain.
- Result: `blocked`; severity: `major`; tag: `need-change`.
- Evidence: [manifest](evidence/source-manifest.json), [commands](evidence/commands.md), [source/UI review](evidence/current-source-ui-regression.md), [database schema/RLS](evidence/database-schema-rls.txt).
- Follow-up: Keep open until the stated integration/runtime evidence is available.

### C03

- Source: [RULES §5](../../../RULES.md). Required: yes.
- Expected: verify at the required layer with evidence; missing proof is not clean.
- Actual: Approval demo propose→approve→tamper→reject reuse not executed end-to-end.
- Result: `blocked`; severity: `major`; tag: `need-change`.
- Evidence: [manifest](evidence/source-manifest.json), [commands](evidence/commands.md), [source/UI review](evidence/current-source-ui-regression.md), [database schema/RLS](evidence/database-schema-rls.txt).
- Follow-up: Keep open until the stated integration/runtime evidence is available.

### C04

- Source: [RULES §5](../../../RULES.md). Required: yes.
- Expected: verify at the required layer with evidence; missing proof is not clean.
- Actual: Owner auth/evaluator unit checks pass. Approval decision module states it never dispatches; no inference/tool action called.
- Result: `pass`; severity: `info`; tag: `clean`.
- Evidence: [manifest](evidence/source-manifest.json), [commands](evidence/commands.md), [source/UI review](evidence/current-source-ui-regression.md), [database schema/RLS](evidence/database-schema-rls.txt).
- Follow-up: None.

### C05

- Source: [RULES §5](../../../RULES.md). Required: yes.
- Expected: verify at the required layer with evidence; missing proof is not clean.
- Actual: Isolated DB schema/RLS metadata checked; no populated cross-scope row behavior tested.
- Result: `blocked`; severity: `major`; tag: `need-change`.
- Evidence: [manifest](evidence/source-manifest.json), [commands](evidence/commands.md), [source/UI review](evidence/current-source-ui-regression.md), [database schema/RLS](evidence/database-schema-rls.txt).
- Follow-up: Keep open until the stated integration/runtime evidence is available.

### C06

- Source: [RULES §5](../../../RULES.md). Required: yes.
- Expected: verify at the required layer with evidence; missing proof is not clean.
- Actual: Phase10 checklist/spec/roadmap reviewed; no status edit.
- Result: `pass`; severity: `info`; tag: `clean`.
- Evidence: [manifest](evidence/source-manifest.json), [commands](evidence/commands.md), [source/UI review](evidence/current-source-ui-regression.md), [database schema/RLS](evidence/database-schema-rls.txt).
- Follow-up: None.

### C07

- Source: [RULES §5](../../../RULES.md). Required: yes.
- Expected: verify at the required layer with evidence; missing proof is not clean.
- Actual: Focused API suite and web lint/build pass; schema/RLS metadata inspected.
- Result: `blocked`; severity: `major`; tag: `need-change`.
- Evidence: [manifest](evidence/source-manifest.json), [commands](evidence/commands.md), [source/UI review](evidence/current-source-ui-regression.md), [database schema/RLS](evidence/database-schema-rls.txt).
- Follow-up: None.

### C08

- Source: [RULES §5](../../../RULES.md). Required: yes.
- Expected: verify at the required layer with evidence; missing proof is not clean.
- Actual: Manifest, commands, outputs, mappings and blockers recorded.
- Result: `pass`; severity: `info`; tag: `clean`.
- Evidence: [manifest](evidence/source-manifest.json), [commands](evidence/commands.md), [source/UI review](evidence/current-source-ui-regression.md), [database schema/RLS](evidence/database-schema-rls.txt).
- Follow-up: None.

### P10-01

- Source: [checklist](../../../phases/phase-10.md). Required: yes.
- Expected: verify at the required layer with evidence; missing proof is not clean.
- Actual: Initial independent evaluation found action_type and task_revision binding omissions in owner approval/delegation evaluator, allowing mismatched action/revision context to satisfy the pure authorization evaluator. Parent subsequently added both bindings and negative tests; this r001 finding is preserved for the r002 retest.
- Result: `fail`; severity: `major`; tag: `need-change`.
- Evidence: [manifest](evidence/source-manifest.json), [commands](evidence/commands.md), [source/UI review](evidence/current-source-ui-regression.md), [database schema/RLS](evidence/database-schema-rls.txt), [initial source manifest](evidence/source-manifest.json); initial mismatch finding is preserved as the r001 P10-01 observation..
- Follow-up: Implement missing Phase09 behavior and retest.

### P10-02

- Source: [checklist](../../../phases/phase-10.md). Required: yes.
- Expected: verify at the required layer with evidence; missing proof is not clean.
- Actual: Canonical ordering and payload validation covered by unit tests, but persisted exact payload snapshot/tamper lifecycle was not run.
- Result: `blocked`; severity: `major`; tag: `need-change`.
- Evidence: [manifest](evidence/source-manifest.json), [commands](evidence/commands.md), [source/UI review](evidence/current-source-ui-regression.md), [database schema/RLS](evidence/database-schema-rls.txt).
- Follow-up: Keep open until the stated integration/runtime evidence is available.

### P10-03

- Source: [checklist](../../../phases/phase-10.md). Required: yes.
- Expected: verify at the required layer with evidence; missing proof is not clean.
- Actual: Pure expiry/consumption/scope/run/policy/hash/revision evaluator negatives were exercised; persisted stale/replay/cross-scope side-effect assertions not run.
- Result: `blocked`; severity: `major`; tag: `need-change`.
- Evidence: [manifest](evidence/source-manifest.json), [commands](evidence/commands.md), [source/UI review](evidence/current-source-ui-regression.md), [database schema/RLS](evidence/database-schema-rls.txt).
- Follow-up: Keep open until the stated integration/runtime evidence is available.

### P10-04

- Source: [checklist](../../../phases/phase-10.md). Required: yes.
- Expected: verify at the required layer with evidence; missing proof is not clean.
- Actual: Atomic consume/reserve double-submit race requires DB-backed service/executor test; not run.
- Result: `blocked`; severity: `major`; tag: `need-change`.
- Evidence: [manifest](evidence/source-manifest.json), [commands](evidence/commands.md), [source/UI review](evidence/current-source-ui-regression.md), [database schema/RLS](evidence/database-schema-rls.txt).
- Follow-up: Keep open until the stated integration/runtime evidence is available.

### P10-05

- Source: [checklist](../../../phases/phase-10.md). Required: yes.
- Expected: verify at the required layer with evidence; missing proof is not clean.
- Actual: No executor epoch/stop race test; in-flight/unknown outcome unverified.
- Result: `blocked`; severity: `major`; tag: `need-change`.
- Evidence: [manifest](evidence/source-manifest.json), [commands](evidence/commands.md), [source/UI review](evidence/current-source-ui-regression.md), [database schema/RLS](evidence/database-schema-rls.txt).
- Follow-up: Keep open until the stated integration/runtime evidence is available.

### P10-06

- Source: [checklist](../../../phases/phase-10.md). Required: yes.
- Expected: verify at the required layer with evidence; missing proof is not clean.
- Actual: Owner auth tests pass; browser Host/Origin/CSRF/cookie/session mutation and actual actor scope not independently exercised.
- Result: `blocked`; severity: `major`; tag: `need-change`.
- Evidence: [manifest](evidence/source-manifest.json), [commands](evidence/commands.md), [source/UI review](evidence/current-source-ui-regression.md), [database schema/RLS](evidence/database-schema-rls.txt).
- Follow-up: Keep open until the stated integration/runtime evidence is available.

### P10-07

- Source: [checklist](../../../phases/phase-10.md). Required: yes.
- Expected: verify at the required layer with evidence; missing proof is not clean.
- Actual: Secret-reference unit coverage passes; inbox empty/history/status UI and persisted audit actor/hash plus deny-no-side-effect not exercised.
- Result: `blocked`; severity: `major`; tag: `need-change`.
- Evidence: [manifest](evidence/source-manifest.json), [commands](evidence/commands.md), [source/UI review](evidence/current-source-ui-regression.md), [database schema/RLS](evidence/database-schema-rls.txt).
- Follow-up: Keep open until the stated integration/runtime evidence is available.

## Gate and handoff

No separate IG gate. Schema/RLS metadata verified; approval lifecycle and executor integration remain blocked.

Blocker details: [blockers](evidence/blockers.md). No phase acceptance/status update.
