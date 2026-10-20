# Independent source/evidence addendum — Phase 08 r009

Reviewer: `/root/ui_fix07_independent`, independent of the implementation changes.

The reviewer inspected final source and `docs/reviews/ui-fix-07/evidence/ui-regression.json` plus the corresponding screenshots:

- `oldVersionRunDoesNotSetCurrentActive` passes. Office status filters Runs by exact current `employee_version_id`; historical Runs from another version remain visible with their old version label and Inspector link.
- `staleEmployeeVersionLinkNeverSubstitutes` passes. A deep link to the old version leaves the selector blank and displays a stale-version alert; the Start guard requires a matching current employee/version selection.
- All 29 browser assertions pass. Two dispatches correspond to the two synthetic Runs; read/navigation did not add dispatches. Cleanup is true; viewport evidence is 1440×900 and 390×844 with no horizontal overflow; no page errors.

Scope limit: this independently verifies source and synthetic UI behavior only. It does not establish live gateway/model execution, CG01 verification, grant authorization or IG08 acceptance.
