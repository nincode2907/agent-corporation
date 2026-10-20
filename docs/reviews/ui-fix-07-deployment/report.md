# UI Fix 07 closure and local deployment

**Result: deployment stopped at preflight.** The shared stack lost PostgreSQL, API and web during the isolated PostgreSQL test run. The Runtime worker reports that the database is unavailable and was in `Restarting (1)` on the final Compose inspection because of its existing `unless-stopped` policy. No deployment, manual service action, database write, inference, grant creation, CG01 change, phase transition, commit or push was performed.

## Work completed

- Compared the Fix 05.1 and UI Fix 07 test commands and identified all 35 opt-in persistence test cases whose status accounts for the 217/38 versus 252/3 count difference.
- Ran the supported `scripts/test_playground_isolated.py` runner. It created a disposable database and applied migrations through `20261020_0010`, but the shared PostgreSQL container and other non-worker services exited before the run completed. The test suite reported 227 passed, 1 failed, 25 errors, 3 skipped and 1 warning; cleanup could not confirm dropping the disposable database after losing its database connection.
- Compared Phase 08 r008 and r009 by criterion. The phase remains **Bị chặn**.
- Inspected Compose service state, worker logs, existing backups and the project working tree. No files outside this deployment review and the requested roadmap record were intentionally modified by this closure task.

## Safety decision

Deployment preconditions are not met. The only inspected backup is `.local/backups/before-single-compose-20261019.dump` (mode 0600), documented as taken at Alembic revision `20261014_0009`, before `20261020_0010`; it is not a fresh pre-deployment backup. A fresh recoverable backup could not be made while PostgreSQL was stopped. The current database revision, grants, active calls, dispatch guard and employee rows could not be queried. The shared volume remains attached and was not removed or changed intentionally.

See [deployment verification](deployment-verification.md), [test reconciliation](test-coverage-reconciliation.md), [UI review](ui-review.md), and [next actions](next-actions.md). Screenshots requested for the *deployed* version were not captured because the deployment did not occur. Earlier disposable UI Fix 07 evidence remains in `../ui-fix-07/` and is not presented as evidence of this deployment.
