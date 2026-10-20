# Sanitized evidence notes

No raw Docker Desktop logs, SQL statements, signed cursors, environment dumps, secrets or test transcripts are copied here. Source logs remain on the host. The rows below are derived observations from read-only inspection.

## Docker Engine / containers

- `rtk docker info`: context `desktop-linux`; Docker Desktop Engine 20.10.23; 4 CPUs; reported memory 4.818 GiB; engine currently responds.
- `rtk docker events --since 2026-10-20T03:40:00Z --until 2026-10-20T03:50:00Z`: no rows returned. Docker Desktop itself stopped/restarted in this interval, so event absence is not evidence of no event.
- Before recovery: PostgreSQL, API and web exited 255; one Runtime worker was restarting. After the authorized bounded stage: PostgreSQL is healthy, API/web remain exited, and the worker is stopped; bootstrap exited 0 after Compose started the dependency again; migrate remains the prior exited-0 container.
- Inspect state finish timestamps: API `03:45:13.570Z`; web `03:45:13.582Z`; PostgreSQL `03:45:13.584Z`; all have `OOMKilled=false`, restart policy `no`. Worker restart policy is `unless-stopped`.
- Container image IDs: stopped API `sha256:284d0aa9…` and web `sha256:e8bb4264…`; current local image tags resolve to API `sha256:4430971c…` and web `sha256:70a7ccd8…`. No container was recreated.
- Docker Desktop driver log derived events: `03:44:07Z` SIGTERM and graceful VM shutdown request; `03:44:08Z` acknowledgement; `03:44:27Z` hypervisor shutdown and Docker state stopped; `03:44:51Z` app/backend start; `03:44:57Z` VM starting. No log evidence identifies who sent SIGTERM.
- Docker Desktop CLI telemetry includes one `docker compose exec` action starting `03:42:42Z`, lasting 87.76 seconds and exiting 1 at approximately `03:44:09Z`. It may be the database diagnostic `compose exec` attempted in the previous turn; the available record cannot prove attribution. The test runner source itself does not invoke Docker CLI.

## Application logs

- PostgreSQL latest normal checkpoint before shutdown: `03:39:05Z`.
- PostgreSQL errors between 03:41–03:42Z include expected check-constraint, RLS and permission denials from tests, plus broken pipe/client lost at `03:42:28Z` and `03:43:05Z`. No shutdown record precedes Docker VM shutdown.
- API readiness endpoint returned 200 through `03:42:55Z`.
- Worker repeated “database unavailable; worker stopped, no call replay” messages from `03:45:21Z` through `04:00:46Z` in the captured log. No model response, credential, grant or secret was copied into this evidence file.

## Host / VM resources (measured after incident)

- macOS `df -h`: 78 GiB available on the Data volume (82% used); no host disk-full signal was found in the sampled output.
- macOS `sysctl vm.swapusage`: 21,788.50 MiB used of 23,552 MiB. `vm_stat` is a cumulative/current snapshot.
- Docker Desktop settings around restart show VM memory 5,120 MiB and configured VM swap 1,024 MiB. The current worker sample used 21.61 MiB; CPU varied and was about 45.6% at one `docker stats` sample.
- These samples are after the shutdown and cannot establish incident-time resource pressure. `OOMKilled=false` is not treated as ruling out host/VM pressure.

## Persistent state / backups

- PostgreSQL volume `agent-corporation_agent_corporation_postgres`, created `2026-10-08T06:38:09Z`; still present. Runtime secrets, database secrets and artifacts volumes also present; no contents inspected.
- Existing `.local/backups/`: Oct 15 dump (121,123 bytes) and Oct 19 dump (141,864 bytes), both mode 0600. Oct 19 evidence records revision `20261014_0009`; neither older backup was modified.
- After Owner authorization, PostgreSQL was started on the same volume and completed WAL recovery; it is healthy at Alembic `20261020_0010`. Demo Corporation is present with 3 employees and 3 EmployeeVersion rows. There are zero Runtime runs, model calls (including unfinished calls), inference grants, eligible grants, or held dispatch guards.
- Fresh backup `.local/backups/pre-recovery-20261020T041305Z.dump`: 149,205 bytes, mode 0600, SHA-256 `9f79139089206c6972345a6c95fca6863ee4d9d49330befe6ddaf9baa852f500`; pinned-image `pg_restore --list` succeeded with network disabled.
- Two matching DB/role pairs remain: `ac_pgtest_b5a524b249704b46` (10 MB, owner `agent_corporation`, revision 0010, 33 public tables) and `ac_pgtest_c96cbe5c98704b10` (~10 MB, owner `agent_corporation`, revision 0009, 32 public tables). Matching roles can log in but are not superuser and cannot create databases. The 0010 database is consistent with the interrupted runner's migration, but exact creation run is unproven. No cleanup performed.
- DB revision/data inventory are now known; integrity beyond successful WAL recovery/readiness, read-only inventory and a readable dump has not been independently restore-tested. Effective CG01 proof was not re-read.

## Test runner

- Source: `scripts/test_playground_isolated.py`; it connects admin operations to the app's configured PostgreSQL URL, creates a uniquely named DB/role on that same server, runs migration and tests, and drops DB/role in `finally`.
- The failed run reached disposable migration `20261020_0010`, then reported 227 passed, 1 failed, 25 errors, 3 skipped, 1 warning. PostgreSQL connection loss followed; cleanup could not confirm a database/role drop.
- Complete failing traceback was not retained. No test rerun was performed during this incident review.

## Working tree

The workspace already contained extensive staged, unstaged and untracked application, UI, roadmap, review and evidence work. This diagnosis added report/evidence files under `docs/incidents/2026-10-20-docker-outage/` and wrote the ignored fresh dump in `.local/backups/`; it did not stage or commit any file.
