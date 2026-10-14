# Independent test — Phase 08 — 20261014T162815+0700-r003-test

- Phase: 08; round `003`; run 2026-10-14 16:28:15–16:31:22 Asia/Ho_Chi_Minh.
- Tester: `/root/phase06_09_independent_check`, independent; no product edits.
- Scope: current source/UI regression and safe local checks; Phase10 also read-only schema/RLS checks against explicitly authorized isolated DB. No inference/grant/gateway, app runtime, migration, row mutation or master-plan changes.
- Source: dirty shared worktree; see [manifest](evidence/source-manifest.json). Commands: [evidence](evidence/commands.md).
- Supersedes: [r002](../20261014T161904+0700-r002-test/report.md). Remake source: none. Technical result: **chưa đủ bằng chứng**.

## Acceptance mapping

| Criterion | IDs | Outcome |
| --- | --- | --- |
| AC1 live event UI | P08-01, P08-02, P08-06 | Blocked; no live run/browser. |
| AC2 read-only replay/ACL | P08-03, P08-04 | Blocked; no state/network/DB integration evidence. |
| AC3 explicit summary | P08-05 | Blocked; no live payload comparison. |
| IG08 | P08-07 | BLOCKED; no live run/upstream proof/grant. |
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
| fail | 0 |
| blocked | 10 |
| not-run | 0 |

## Test results

### C01

- Source: [RULES §5](../../../RULES.md). Required: yes.
- Expected: verify at the required layer with evidence; missing proof is not clean.
- Actual: Dirty scope reviewed; tester wrote only this results batch.
- Result: `pass`; severity: `info`; tag: `clean`.
- Evidence: [manifest](evidence/source-manifest.json), [commands](evidence/commands.md), [source/UI review](evidence/current-source-ui-regression.md).
- Follow-up: None.

### C02

- Source: [RULES §5](../../../RULES.md). Required: yes.
- Expected: verify at the required layer with evidence; missing proof is not clean.
- Actual: Dependency 07 and IG08 evidence remain unresolved; Phase07 reconnect finding persists.
- Result: `blocked`; severity: `major`; tag: `need-change`.
- Evidence: [manifest](evidence/source-manifest.json), [commands](evidence/commands.md), [source/UI review](evidence/current-source-ui-regression.md).
- Follow-up: Keep open until the stated integration/runtime evidence is available.

### C03

- Source: [RULES §5](../../../RULES.md). Required: yes.
- Expected: verify at the required layer with evidence; missing proof is not clean.
- Actual: No authorized persisted run/demo correlating events with Office/Inspector.
- Result: `blocked`; severity: `major`; tag: `need-change`.
- Evidence: [manifest](evidence/source-manifest.json), [commands](evidence/commands.md), [source/UI review](evidence/current-source-ui-regression.md).
- Follow-up: Keep open until the stated integration/runtime evidence is available.

### C04

- Source: [RULES §5](../../../RULES.md). Required: yes.
- Expected: verify at the required layer with evidence; missing proof is not clean.
- Actual: Source shows opening Office/Inspector/replay paths does not itself dispatch model or tools.
- Result: `pass`; severity: `info`; tag: `clean`.
- Evidence: [manifest](evidence/source-manifest.json), [commands](evidence/commands.md), [source/UI review](evidence/current-source-ui-regression.md).
- Follow-up: None.

### C05

- Source: [RULES §5](../../../RULES.md). Required: yes.
- Expected: verify at the required layer with evidence; missing proof is not clean.
- Actual: No isolated DB/browser canary checks for cross-company/environment redaction.
- Result: `blocked`; severity: `major`; tag: `need-change`.
- Evidence: [manifest](evidence/source-manifest.json), [commands](evidence/commands.md), [source/UI review](evidence/current-source-ui-regression.md).
- Follow-up: Keep open until the stated integration/runtime evidence is available.

### C06

- Source: [RULES §5](../../../RULES.md). Required: yes.
- Expected: verify at the required layer with evidence; missing proof is not clean.
- Actual: Checklist/spec/roadmap reviewed; no status edits.
- Result: `pass`; severity: `info`; tag: `clean`.
- Evidence: [manifest](evidence/source-manifest.json), [commands](evidence/commands.md), [source/UI review](evidence/current-source-ui-regression.md).
- Follow-up: None.

### C07

- Source: [RULES §5](../../../RULES.md). Required: yes.
- Expected: verify at the required layer with evidence; missing proof is not clean.
- Actual: Focused API suite 71 passed; web lint/build pass. Separate reconnect probe returns HTTP 400 on changed Last-Event-ID.
- Result: `pass`; severity: `info`; tag: `clean`.
- Evidence: [manifest](evidence/source-manifest.json), [commands](evidence/commands.md), [source/UI review](evidence/current-source-ui-regression.md).
- Follow-up: None.

### C08

- Source: [RULES §5](../../../RULES.md). Required: yes.
- Expected: verify at the required layer with evidence; missing proof is not clean.
- Actual: Manifest, commands, evidence, tags and links recorded.
- Result: `pass`; severity: `info`; tag: `clean`.
- Evidence: [manifest](evidence/source-manifest.json), [commands](evidence/commands.md), [source/UI review](evidence/current-source-ui-regression.md).
- Follow-up: None.

### P08-01

- Source: [checklist](../../../phases/phase-08.md). Required: yes.
- Expected: verify at the required layer with evidence; missing proof is not clean.
- Actual: Live Office requires authorized persisted run; none available.
- Result: `blocked`; severity: `major`; tag: `need-change`.
- Evidence: [manifest](evidence/source-manifest.json), [commands](evidence/commands.md), [source/UI review](evidence/current-source-ui-regression.md).
- Follow-up: Keep open until the stated integration/runtime evidence is available.

### P08-02

- Source: [checklist](../../../phases/phase-08.md). Required: yes.
- Expected: verify at the required layer with evidence; missing proof is not clean.
- Actual: Inspector shared IDs from dashboard/task/org need live run and browser; not run.
- Result: `blocked`; severity: `major`; tag: `need-change`.
- Evidence: [manifest](evidence/source-manifest.json), [commands](evidence/commands.md), [source/UI review](evidence/current-source-ui-regression.md).
- Follow-up: Keep open until the stated integration/runtime evidence is available.

### P08-03

- Source: [checklist](../../../phases/phase-08.md). Required: yes.
- Expected: verify at the required layer with evidence; missing proof is not clean.
- Actual: Read-only replay network spy and state before/after evidence not run.
- Result: `blocked`; severity: `major`; tag: `need-change`.
- Evidence: [manifest](evidence/source-manifest.json), [commands](evidence/commands.md), [source/UI review](evidence/current-source-ui-regression.md).
- Follow-up: Keep open until the stated integration/runtime evidence is available.

### P08-04

- Source: [checklist](../../../phases/phase-08.md). Required: yes.
- Expected: verify at the required layer with evidence; missing proof is not clean.
- Actual: Cross-scope ACL/redaction API/UI on isolated DB not run.
- Result: `blocked`; severity: `major`; tag: `need-change`.
- Evidence: [manifest](evidence/source-manifest.json), [commands](evidence/commands.md), [source/UI review](evidence/current-source-ui-regression.md).
- Follow-up: Keep open until the stated integration/runtime evidence is available.

### P08-05

- Source: [checklist](../../../phases/phase-08.md). Required: yes.
- Expected: verify at the required layer with evidence; missing proof is not clean.
- Actual: No live event payload to compare with explicit summary/provenance UI.
- Result: `blocked`; severity: `major`; tag: `need-change`.
- Evidence: [manifest](evidence/source-manifest.json), [commands](evidence/commands.md), [source/UI review](evidence/current-source-ui-regression.md).
- Follow-up: Keep open until the stated integration/runtime evidence is available.

### P08-06

- Source: [checklist](../../../phases/phase-08.md). Required: yes.
- Expected: verify at the required layer with evidence; missing proof is not clean.
- Actual: Reconnect/error/gap/unknown usage browser flow not verified; isolated mismatch cursor probe yields HTTP 400.
- Result: `blocked`; severity: `major`; tag: `need-change`.
- Evidence: [manifest](evidence/source-manifest.json), [commands](evidence/commands.md), [source/UI review](evidence/current-source-ui-regression.md), [reconnect probe](evidence/reconnect-probe.txt).
- Follow-up: Keep open until the stated integration/runtime evidence is available.

### P08-07

- Source: [checklist](../../../phases/phase-08.md). Required: yes.
- Expected: verify at the required layer with evidence; missing proof is not clean.
- Actual: IG08 live saved events→SSE→Office/Inspector and upstream proof absent; no grant.
- Result: `blocked`; severity: `major`; tag: `need-change`.
- Evidence: [manifest](evidence/source-manifest.json), [commands](evidence/commands.md), [source/UI review](evidence/current-source-ui-regression.md).
- Follow-up: Keep open until the stated integration/runtime evidence is available.

## Gate and handoff

IG08 **BLOCKED**: P08-07; live run, upstream proof and scoped grant absent.

Blocker details: [blockers](evidence/blockers.md). No phase acceptance/status update.
