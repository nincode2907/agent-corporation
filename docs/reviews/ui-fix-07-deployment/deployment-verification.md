# Deployment verification

## Preflight and outcome

| Check | Observation | Result |
|---|---|---|
| Working tree | Substantial staged and unstaged project work existed before this closure. It was preserved; no commit or push. | Inspected |
| Compose state | At inspection, `agent-corporation-postgres`, `agent-corporation-api`, and `agent-corporation-web` were exited (255); worker was running after restart. All three exited at the same timestamp. | **Failed; stop** |
| Worker dispatch safety | Worker logs: “Cơ sở dữ liệu không khả dụng; worker đã dừng, không phát lại call.” On final Compose inspection the worker was `Restarting (1)` under its `unless-stopped` policy. | **Failed; restart loop observed.** No dispatch established in the logs, but DB guard/grant state unavailable |
| Persistent volume | Compose still declares `agent-corporation_agent_corporation_postgres`; no `down`, volume removal or reset was run. | Preserved; data state not queried |
| Backup | Existing Oct 19 dump is mode 0600, but its recorded revision is `20261014_0009`. A current dump and restore-list validation could not be completed with PostgreSQL down. | **Failed; no fresh recoverable backup** |
| Migration | Supported runner upgraded its disposable database to `20261020_0010`. The shared runtime DB was unavailable for revision query. | Disposable migration valid; runtime revision unverified |
| Grants / active calls / dispatch guard | Could not query after shared DB exited. No inference, grant, Run or CG01 action was initiated by this closure. | **Unverified; stop** |
| Owner session / employee rows | No authenticated shared UI inspection was performed because API/web were down. | Not verified |
| CG01 | No config write or override was made. Runtime database proof could not be re-read. | Unchanged by this task; current effective runtime state unverified |

## Deployment action

No `docker compose up`, rebuild, recreate, database migration, manual service restart/stop, or UI session action was performed. This follows the task's explicit stop condition: backup, database state and dispatch/grant safety could not be established. Docker's existing `unless-stopped` worker policy continued its automatic restart attempts; I did not intervene. The shared PostgreSQL volume and Owner credentials were not intentionally modified.

## Required before a later deployment attempt

Restore/inspect the existing stack under the Owner's control; confirm the PostgreSQL volume and current revision, employee and grant state, dispatch guard and absence of active calls; create and validate a fresh recoverable backup; then resume this narrowly scoped web deployment and Owner UI verification. No inference grant or CG01 change is needed for UI verification.
