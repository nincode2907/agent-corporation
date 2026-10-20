# P0 incident diagnosis — 2026-10-20 Docker outage

## Summary

The verified failure boundary is a **Docker Desktop Linux VM / Docker Engine graceful shutdown and restart**, not a PostgreSQL process shown to fail first. Docker Desktop driver logs record receipt of `SIGTERM` at 03:44:07 UTC, a graceful VM shutdown request acknowledged at 03:44:08, and hypervisor shutdown / Docker state `stopped` at 03:44:27. Docker Desktop starts its backend at 03:44:51 and the VM at 03:44:57. The Agent Corporation PostgreSQL, API and web containers have exit code 255 and finish timestamps within 14 ms of one another at 03:45:13. The Runtime worker has `unless-stopped`, so it continued restarting against the unavailable DB.

The event that caused Docker Desktop to receive SIGTERM is **not identified**. The isolated test runner targeted a disposable database on the same PostgreSQL server as the shared Agent Corporation database. This creates a plausible shared-resource contention path, but no incident-time resource telemetry proves it caused the Docker Desktop shutdown. The runner was not coded to stop/restart Docker; the direct process trigger remains unknown.

After the Owner authorized the bounded first recovery stage, I stopped the worker, started the existing PostgreSQL container on the original volume, created and verified a fresh backup, and ran only read-only database inventory. The database recovered WAL and is healthy at revision `20261020_0010`; Demo Corporation and its three employees/versions are present, with zero Runtime runs, model calls, grants and held dispatch guard. API/web remain stopped; the worker remains stopped. Two `ac_pgtest_*` database/role pairs remain and were not modified. No inference, grant, CG01 change, restore, migration, app start, deployment or phase transition was performed.

## Findings

### VERIFIED

- Docker Desktop Engine responds now (`desktop-linux`, Engine 20.10.23, 4 CPUs, 4.818 GiB reported Engine memory); the Docker VM was stopped and restarted during the incident window per local Docker Desktop logs.
- `SIGTERM` → graceful VM shutdown acknowledgement → hypervisor stopped → Docker state stopped is logged at 03:44:07–03:44:27 UTC. Docker Desktop/backend then starts again at 03:44:51 and the VM starts at 03:44:57.
- PostgreSQL, API and web exit records are `255`, `OOMKilled=false`, with finish times 03:45:13.570Z, .582Z and .584Z. The exit records are effectively simultaneous; PostgreSQL is not evidenced as the first container to exit.
- PostgreSQL logs show it ready from 01:59Z, routine checkpoints through 03:39:05Z, expected test rejection errors, then broken-pipe/client-loss errors at 03:42:28Z and 03:43:05Z. There is no Postgres shutdown record before the Docker VM shutdown.
- API readiness probes returned 200 through 03:42:55Z. The web container's application access log contains traffic before the outage. These logs do not establish service health at the exact SIGTERM time.
- The worker logs repeatedly say the database is unavailable and that it stopped without replaying a call. It is the only Agent Corporation service configured with `restart: unless-stopped`; `docker stats` later showed one worker container at about 45.6% CPU and 21.61 MiB, while its DB peers were stopped. The CPU sample is after the incident and is not an incident-time measurement.
- Following explicit Owner approval, the worker was stopped with `docker compose stop --timeout 30 worker` and remains stopped. `docker compose start postgres` started the existing PostgreSQL container on the same persistent volume. Compose also ran its completed bootstrap dependency once; its log says configuration/Owner already existed and credentials were kept, with no secret shown.
- PostgreSQL logged an interrupted database, automatic WAL recovery, redo completion, end-of-recovery checkpoint and `database system is ready to accept connections` at 04:12:54Z. The existing PostgreSQL container is healthy. No API, web, migration or worker service was started by this recovery stage.
- A fresh custom-format backup `.local/backups/pre-recovery-20261020T041305Z.dump` was written, mode 0600, 149,205 bytes, SHA-256 `9f79139089206c6972345a6c95fca6863ee4d9d49330befe6ddaf9baa852f500`. Pinned-image `pg_restore --list` exited successfully. No restore rehearsal was done.
- Read-only queries confirm database `agent_corporation` at Alembic `20261020_0010`, one Demo Corporation, 3 employees and 3 EmployeeVersion rows, zero Runtime runs, zero model calls (including unfinished calls), zero inference grants, zero eligible grants, and one `runtime_dispatch_guard` row with no held span.
- Two test database/role pairs remain: `ac_pgtest_b5a524b249704b46` (10 MB, revision `20261020_0010`, 33 public tables) and `ac_pgtest_c96cbe5c98704b10` (about 10 MB, revision `20261014_0009`, 32 public tables). Both database owners are `agent_corporation`; both matching roles can log in but are neither superuser nor database creator. The 0010 DB matches the interrupted runner's migration, but its precise creation run is unproven. Neither pair was deleted or modified.
- Compose has `restart: "no"` on PostgreSQL/API/web and health checks for PostgreSQL/API/web. API and worker depend on PostgreSQL health; web depends on API health. Health checks do not restart a service whose restart policy is `no`.
- The PostgreSQL volume `agent-corporation_agent_corporation_postgres` exists (created 2026-10-08); runtime secrets, database secrets and artifacts volumes also exist. No volume was removed or pruned.
- Existing dumps are Oct 15 and Oct 19, both mode 0600. The Oct 19 record documents Alembic `20261014_0009`; it predates the latest shared migration. A new current backup was created and verified after PostgreSQL recovery; details are below.
- The supported test runner uses `settings.migration_database_url or settings.database_url` as the admin connection, creates a random `ac_pgtest_*` database and same-named role in that PostgreSQL server, runs Alembic and the test suite, and tries `DROP DATABASE ... WITH (FORCE)` then `DROP ROLE` in `finally`. If DB reconnect or the first DROP fails, the role drop and its success message are skipped. The interrupted output was 227 passed, 1 failed, 25 errors, 3 skipped, 1 warning; complete failing traceback was not retained. It cannot establish a code regression or a successful cleanup.
- Docker Engine `events` returned no event rows for the requested interval. Because the Docker VM/Engine itself stopped and restarted, this empty result is an evidence gap, not proof that no Docker event occurred.
- Host snapshot after the incident: 78 GiB filesystem space available; swap used 21,788.5 MiB of 23,552 MiB. Docker Desktop settings logged around restart show a 5,120 MiB VM and 1,024 MiB configured VM swap. These are not incident-time pressure measurements.

### POSSIBLE causes

- An operator, host process, lifecycle/watchdog, update path or other Docker Desktop control path sent/caused the SIGTERM. The logs identify the signal and graceful shutdown, but not its initiator.
- Host or Docker VM memory pressure may have contributed. High host swap use was measured later and the VM is limited to 5 GiB; no incident-time pressure sample, VM kernel OOM record, or cgroup evidence was recovered. `OOMKilled=false` only rules out the recorded per-container OOM kill flag.
- The isolated API suite may have caused resource contention because it ran a database and application workload on the same PostgreSQL server/VM. The runner did not create a separate server or apply explicit Compose resource limits. No historical CPU/memory/IO telemetry ties it to the shutdown.
- The Docker Desktop application/backend restart sequence may have had a second startup problem (`Terminator: com.docker.backend cannot start` at 03:44:33Z) before the app/backend started again. This message is downstream of the graceful shutdown and does not identify its trigger.

### RULED-OUT causes

- **A PostgreSQL-first container exit is not supported by evidence.** PostgreSQL logs continue until 03:43:05Z, Docker records a VM SIGTERM at 03:44:07Z, and PostgreSQL/API/web share exit 255 timestamps within 14 ms. The current record points to common VM/Engine interruption. It does not rule out earlier transient PostgreSQL connection faults.
- **A recorded per-container OOM kill is absent** (`OOMKilled=false` for the three exited containers). Host/VM resource pressure is not ruled out.
- A deliberate `docker compose down --volumes`, data reset, reseed, Alembic downgrade, or database restore was not performed by this diagnostic task. No evidence in the test runner source indicates that it runs any of these operations.

### UNVERIFIED conditions

- Who or what sent SIGTERM; whether an operator action or Docker Desktop lifecycle triggered it.
- Incident-time host/VM memory, swap, disk IO, CPU and filesystem pressure.
- Whether the PostgreSQL storage is fully sound beyond successful WAL recovery, readiness, read-only inventory and a readable logical backup; no restore rehearsal/integrity scrub was run.
- Which execution created the older `ac_pgtest_c96cbe5c98704b10` database/role; the runner's creation timestamp is not retained. Both test DBs are identified and preserved, but their precise provenance does not prove they are safe to remove.
- Current image-to-container alignment for a recovered application stack: stopped API/web containers retain image IDs different from the current `:local` image tags. Do not recreate them until separately approved and backed up.
- Effective CG01 proof/config was not re-read during this bounded recovery stage; no CG01 setting or proof was changed.
- Complete traceback for the one failed test and 25 errors. The prior run output was not persisted as a complete, retained artifact.

## OWNER APPROVAL REQUIRED

The Owner-approved worker stop, existing PostgreSQL start, fresh backup and read-only database inventory are complete. The recovery plan records exact evidence. API/web/worker restart, test DB/role cleanup, test rerun, migration, restore and deployment still require separate authorization. Starting PostgreSQL replayed WAL as expected; no application services have been resumed.

## Evidence index

- [Incident timeline](timeline.md)
- [Recovery proposal and scoped commands](recovery-plan.md)
- [Test isolation review](test-isolation-review.md)
- [Sanitized observations and source pointers](evidence/observations.md)
- [Authorized recovery-stage outputs](evidence/recovery-stage.md)
