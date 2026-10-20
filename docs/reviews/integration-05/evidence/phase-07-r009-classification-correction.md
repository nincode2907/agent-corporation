# Phase 07 r009 classification correction

Date: 2026-10-19 (Asia/Ho_Chi_Minh)

The Phase 07 r009 report describes a narrower worker-recovery follow-up, but its case table changes P07-03 from the checklist's cursor/gap boundary test to browser network-drop/reconnect. That is a scope/mapping error, not evidence of a regression.

| Criterion | r008 evidence | r009 report | Correct interpretation |
| --- | --- | --- | --- |
| P07-03 | Invalid/stale/retention-gap/other-scope cursor rejection and visible gap passed against disposable PostgreSQL and UI evidence. | Replaced by browser network-drop and marked blocked. | Keep P07-03 clean from r008; r009 did not rerun its actual criterion. Network-drop remains a separate open reconnect check under P07-02/demo. |
| P07-05 | Worker process restart was blocked for lack of child-process evidence. | Child process was terminated during fake transport; restart reconciled the expired lease to unknown, with one call and no redispatch. | New evidence closes the synthetic process-recovery blocker for P07-05. |
| C03, P07-07 | Authorized live Run blocked by Owner grant/CG01. | Still blocked. | No change. |

The r009 report's summary (11 clean/4 blocked) also disagrees with its 15 detailed case records: those records contain 12 clean and 3 blocked. When P07-03 is mapped back to its actual checklist meaning and its r008 evidence is retained (the r009 worker-only diff did not change cursor handling), the cumulative latest-evidence count is **13 clean / 2 blocked / 0 fail**. The two remaining blockers are C03 and P07-07. This correction does not edit the closed r009 report or claim a network-drop test.

Comparison by criterion: P07-03 remains clean; P07-05 improves from blocked to clean; the other listed criteria retain their status. The reported decrease from 12 to 11 clean is therefore not a product regression. It came from changed P07-03 scope plus an aggregate-count mismatch. Phase 07 remains **Bị chặn**; no phase acceptance or inference permission follows from this note.
