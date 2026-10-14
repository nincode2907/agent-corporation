# Independent test — Phase 09 — 20261014T162815+0700-r002-test

- Phase: 09; round `002`; run 2026-10-14 16:28:15–16:31:22 Asia/Ho_Chi_Minh.
- Tester: `/root/phase06_09_independent_check`, independent; no product edits.
- Scope: current source/UI regression and safe local checks; Phase10 also read-only schema/RLS checks against explicitly authorized isolated DB. No inference/grant/gateway, app runtime, migration, row mutation or master-plan changes.
- Source: dirty shared worktree; see [manifest](evidence/source-manifest.json). Commands: [evidence](evidence/commands.md).
- Supersedes: [r001](../20261014T161904+0700-r001-test/report.md). Remake source: none. Technical result: **cần sửa**.

## Acceptance mapping

| Criterion | IDs | Outcome |
| --- | --- | --- |
| AC1 lease/concurrency | P09-02, P09-03 | Fail; worker claim/recovery absent. |
| AC2 pause/resume/retry | P09-04, P09-05 | Checkpoint blocked; retry fail. |
| AC3 review/rework/accept | P09-06, P09-07 | DB/UI blocked. |
| Required demo | P09-01–P09-07 | Not demonstrated. |
| Common criteria | C01–C08 | All recorded below. |

## Totals

| Tag | Count |
| --- | ---: |
| clean | 5 |
| need-change | 10 |
| suggestion | 0 |

| Result | Count |
| --- | ---: |
| pass | 5 |
| fail | 3 |
| blocked | 7 |
| not-run | 0 |

## Test results

### C01

- Source: [RULES §5](../../../RULES.md). Required: yes.
- Expected: verify at the required layer with evidence; missing proof is not clean.
- Actual: Tester changed only this results batch; dirty worktree includes parent Phase10 code.
- Result: `pass`; severity: `info`; tag: `clean`.
- Evidence: [manifest](evidence/source-manifest.json), [commands](evidence/commands.md), [source/UI review](evidence/current-source-ui-regression.md).
- Follow-up: None.

### C02

- Source: [RULES §5](../../../RULES.md). Required: yes.
- Expected: verify at the required layer with evidence; missing proof is not clean.
- Actual: Phase08 dependency remains unaccepted/IG08 blocked.
- Result: `blocked`; severity: `major`; tag: `need-change`.
- Evidence: [manifest](evidence/source-manifest.json), [commands](evidence/commands.md), [source/UI review](evidence/current-source-ui-regression.md).
- Follow-up: Keep open until the stated integration/runtime evidence is available.

### C03

- Source: [RULES §5](../../../RULES.md). Required: yes.
- Expected: verify at the required layer with evidence; missing proof is not clean.
- Actual: Two-task pause/restart/resume/retry demo absent.
- Result: `blocked`; severity: `major`; tag: `need-change`.
- Evidence: [manifest](evidence/source-manifest.json), [commands](evidence/commands.md), [source/UI review](evidence/current-source-ui-regression.md).
- Follow-up: Keep open until the stated integration/runtime evidence is available.

### C04

- Source: [RULES §5](../../../RULES.md). Required: yes.
- Expected: verify at the required layer with evidence; missing proof is not clean.
- Actual: WorkBoard open does not dispatch inference; no worker started.
- Result: `pass`; severity: `info`; tag: `clean`.
- Evidence: [manifest](evidence/source-manifest.json), [commands](evidence/commands.md), [source/UI review](evidence/current-source-ui-regression.md).
- Follow-up: None.

### C05

- Source: [RULES §5](../../../RULES.md). Required: yes.
- Expected: verify at the required layer with evidence; missing proof is not clean.
- Actual: No scoped DB fixture available for cross-scope persistence/API tests.
- Result: `blocked`; severity: `major`; tag: `need-change`.
- Evidence: [manifest](evidence/source-manifest.json), [commands](evidence/commands.md), [source/UI review](evidence/current-source-ui-regression.md).
- Follow-up: Keep open until the stated integration/runtime evidence is available.

### C06

- Source: [RULES §5](../../../RULES.md). Required: yes.
- Expected: verify at the required layer with evidence; missing proof is not clean.
- Actual: Current checklist/spec/roadmap reviewed; no status edit.
- Result: `pass`; severity: `info`; tag: `clean`.
- Evidence: [manifest](evidence/source-manifest.json), [commands](evidence/commands.md), [source/UI review](evidence/current-source-ui-regression.md).
- Follow-up: None.

### C07

- Source: [RULES §5](../../../RULES.md). Required: yes.
- Expected: verify at the required layer with evidence; missing proof is not clean.
- Actual: 71 focused API tests pass; web lint/build pass. Worker/retry gaps remain.
- Result: `pass`; severity: `info`; tag: `clean`.
- Evidence: [manifest](evidence/source-manifest.json), [commands](evidence/commands.md), [source/UI review](evidence/current-source-ui-regression.md).
- Follow-up: None.

### C08

- Source: [RULES §5](../../../RULES.md). Required: yes.
- Expected: verify at the required layer with evidence; missing proof is not clean.
- Actual: Manifest, commands and per-case evidence/links included.
- Result: `pass`; severity: `info`; tag: `clean`.
- Evidence: [manifest](evidence/source-manifest.json), [commands](evidence/commands.md), [source/UI review](evidence/current-source-ui-regression.md).
- Follow-up: None.

### P09-01

- Source: [checklist](../../../phases/phase-09.md). Required: yes.
- Expected: verify at the required layer with evidence; missing proof is not clean.
- Actual: Validation unit coverage exists; persisted task create/queue/revision integration not run.
- Result: `blocked`; severity: `major`; tag: `need-change`.
- Evidence: [manifest](evidence/source-manifest.json), [commands](evidence/commands.md), [source/UI review](evidence/current-source-ui-regression.md).
- Follow-up: Keep open until the stated integration/runtime evidence is available.

### P09-02

- Source: [checklist](../../../phases/phase-09.md). Required: yes.
- Expected: verify at the required layer with evidence; missing proof is not clean.
- Actual: queue source has no worker claim/lease or unique lease concurrency path.
- Result: `fail`; severity: `major`; tag: `need-change`.
- Evidence: [manifest](evidence/source-manifest.json), [commands](evidence/commands.md), [source/UI review](evidence/current-source-ui-regression.md).
- Follow-up: Implement missing Phase09 behavior and retest.

### P09-03

- Source: [checklist](../../../phases/phase-09.md). Required: yes.
- Expected: verify at the required layer with evidence; missing proof is not clean.
- Actual: No worker restart/recovery/lease expiry implementation or evidence.
- Result: `fail`; severity: `major`; tag: `need-change`.
- Evidence: [manifest](evidence/source-manifest.json), [commands](evidence/commands.md), [source/UI review](evidence/current-source-ui-regression.md).
- Follow-up: Implement missing Phase09 behavior and retest.

### P09-04

- Source: [checklist](../../../phases/phase-09.md). Required: yes.
- Expected: verify at the required layer with evidence; missing proof is not clean.
- Actual: Worker checkpoint lifecycle and recheck need runtime/DB integration.
- Result: `blocked`; severity: `major`; tag: `need-change`.
- Evidence: [manifest](evidence/source-manifest.json), [commands](evidence/commands.md), [source/UI review](evidence/current-source-ui-regression.md).
- Follow-up: Keep open until the stated integration/runtime evidence is available.

### P09-05

- Source: [checklist](../../../phases/phase-09.md). Required: yes.
- Expected: verify at the required layer with evidence; missing proof is not clean.
- Actual: task_action allows enqueue/pause/resume/cancel/accept/request_rework; no retry/attempt lineage.
- Result: `fail`; severity: `major`; tag: `need-change`.
- Evidence: [manifest](evidence/source-manifest.json), [commands](evidence/commands.md), [source/UI review](evidence/current-source-ui-regression.md).
- Follow-up: Implement missing Phase09 behavior and retest.

### P09-06

- Source: [checklist](../../../phases/phase-09.md). Required: yes.
- Expected: verify at the required layer with evidence; missing proof is not clean.
- Actual: Owner acceptance/rework persistence and evidence retention not tested on DB.
- Result: `blocked`; severity: `major`; tag: `need-change`.
- Evidence: [manifest](evidence/source-manifest.json), [commands](evidence/commands.md), [source/UI review](evidence/current-source-ui-regression.md).
- Follow-up: Keep open until the stated integration/runtime evidence is available.

### P09-07

- Source: [checklist](../../../phases/phase-09.md). Required: yes.
- Expected: verify at the required layer with evidence; missing proof is not clean.
- Actual: WorkBoard source/lint/build pass; browser actions and API state comparison not run.
- Result: `blocked`; severity: `major`; tag: `need-change`.
- Evidence: [manifest](evidence/source-manifest.json), [commands](evidence/commands.md), [source/UI review](evidence/current-source-ui-regression.md).
- Follow-up: Keep open until the stated integration/runtime evidence is available.

## Gate and handoff

No separate IG gate; P09-02/P09-03/P09-05 fail, so Phase09 remains incomplete.

Blocker details: [blockers](evidence/blockers.md). No phase acceptance/status update.
