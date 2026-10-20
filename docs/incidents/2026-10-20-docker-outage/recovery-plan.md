# Recovery plan — first bounded stage completed; remaining actions await Owner authorization

This plan preserves the current PostgreSQL volume and does not restore the Oct 19 dump. It does not deploy UI Fix 07, run tests, change CG01, or enable inference. The Owner authorized and the operator completed only the worker stop, existing PostgreSQL start, fresh backup and read-only DB inventory. API/web/worker startup, test DB cleanup, test rerun, migration, restore and deployment remain unperformed and need separate authorization.

## Approvals and action classes

| Action | Class | Owner approval |
|---|---|---|
| Read-only `docker inspect`, `compose ps`, container logs, `df`, SQL SELECTs after PG is online | Read-only (the latter requires process start first) | Read-only diagnostics authorized; PG start still requires approval. |
| Stop only the Runtime worker container to end its DB retry loop | Process/container state | Authorized and completed. This takes the worker offline; no configuration changes. |
| Start the existing PostgreSQL container on the existing volume | Process state **and automatic WAL recovery/database-file writes** | Authorized and completed. No `down`, recreation, new volume, reset or restore. |
| Write a new custom-format `pg_dump` file under `.local/backups/` and chmod 0600 | Local backup file write; database read | Authorized and completed with a unique filename and archive-list verification. |
| Start existing API/web containers | Process state | Required after backup and preflight verification. |
| Start the worker | Process state and dispatch-capable service | Required after DB/API/grant/guard checks; verify CG01 remains strict and no dispatchable grant/unknown guard exists first. |
| Run `migrate`, restore any backup, recreate/rebuild/deploy images | Persistent DB or application state | Separate explicit approval for each. None is part of this recovery proposal. |

## Completed bounded stage

- Stopped only the worker retry loop. It remains stopped.
- Started the existing PostgreSQL container using the existing volume. PostgreSQL completed WAL recovery and is healthy. Compose also ran the existing bootstrap dependency once; its output confirms it retained existing config/Owner credentials.
- Created `.local/backups/pre-recovery-20261020T041305Z.dump` (149,205 bytes, mode 0600, SHA-256 `9f79139089206c6972345a6c95fca6863ee4d9d49330befe6ddaf9baa852f500`). `pg_restore --list` with the pinned PostgreSQL image succeeded.
- Read-only inventory confirmed revision 0010, Demo Corporation, 3 employees and versions, no Runtime runs or model calls, no grants/eligible grants, and no held dispatch guard.
- Found and preserved two `ac_pgtest_*` DB/role pairs, one at 0010 and one at 0009. Do not drop either; the interrupted runner's output lacks enough metadata to prove the older pair belongs to a specific run.
- API and web remain exited; no service image was recreated. Effective CG01 proof was not re-read.

## Recovery procedure and status

### A. Stop the retrying worker and start only PostgreSQL — completed

```sh
rtk docker compose stop --timeout 30 worker
rtk docker compose start postgres
rtk docker compose ps --all
rtk docker inspect --format '{{.Name}} {{.State.Status}} {{if .State.Health}}{{.State.Health.Status}}{{end}}' agent-corporation-postgres
```

The worker stop succeeded. Starting PostgreSQL also ran its already-completed bootstrap dependency; bootstrap confirmed it retained the existing config/Owner credential. The existing PostgreSQL container became healthy after WAL recovery on its original volume. No other runtime service was started. See [recovery-stage evidence](evidence/recovery-stage.md).

### B. Create and verify a fresh backup before application startup — completed

Choose a new filename using the actual UTC time, verify it does not exist, and keep output inside the existing private `.local/backups/` directory:

```sh
rtk docker compose exec -T postgres sh -ec '. /database-secrets/postgres.env; exec pg_dump -U "$POSTGRES_USER" -d "$POSTGRES_DB" -Fc' > .local/backups/pre-recovery-20261020-HHMMSS.dump
rtk chmod 600 .local/backups/pre-recovery-20261020-HHMMSS.dump
rtk docker run --rm -i --network none postgres:18.6-alpine@sha256:77f585114c32fbca283dc835b0596f4e52b51b4c6662d7810b2f4084f60a1873 pg_restore --list < .local/backups/pre-recovery-20261020-HHMMSS.dump
rtk ls -lT .local/backups/pre-recovery-20261020-HHMMSS.dump
```

The pinned-image `docker run` used a one-shot container with no network or mounted data volume and parsed the backup archive list successfully. This verifies archive readability, not restore correctness; a restore rehearsal must use a separately approved disposable server/project. Exact size, mode and checksum are in [recovery-stage evidence](evidence/recovery-stage.md).

### C. Inspect DB state read-only; do not migrate automatically — completed

```sh
rtk docker compose exec -T postgres sh -ec '. /database-secrets/postgres.env; psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -v ON_ERROR_STOP=1 -Atqc "SELECT version_num FROM alembic_version"'
```

The revision query and subsequent read-only inventory completed. Results are recorded above. The two `ac_pgtest_*` database/role pairs are identified but attribution of the older pair is incomplete; neither was dropped. CG01 proof was not re-read. API/web/worker remain stopped pending separate approval and disposition of the remaining checks.

If a migration is actually needed, stop and request separate Owner authorization before `rtk docker compose run --rm migrate`; migration is a persistent database write. Do not downgrade.

### D. Start API and web, then verify; start worker last

Only after backup validation, healthy database, expected revision and Owner review of grants/calls/guard:

```sh
rtk docker compose start api web
rtk docker compose ps --all
rtk curl --fail http://127.0.0.1:15501/api/v1/health/ready
rtk curl --fail http://127.0.0.1:15500/healthz
```

Do not recreate images here: the stopped containers' image IDs differ from the current `:local` tags. Use the existing containers only unless separately authorized to rebuild/recreate. After API/web health and state checks, the Owner may authorize:

```sh
rtk docker compose start worker
rtk docker compose ps --status running worker
rtk docker stats --no-stream agent-corporation-runtime-worker
```

Verify exactly one worker container, healthy DB/API, no grant/model call was created, strict CG01 remains in force, no stale/unknown dispatch guard exists, and no network/model call was dispatched. Keep the process logs visible during recovery.

## Abort and recovery options

- On any PostgreSQL recovery/corruption error, stop. Preserve the original volume and logs; ask the Owner to choose a recovery specialist or a separately approved clone/restore rehearsal.
- If a temporary database/role is discovered, record its exact name and ownership; do not delete it until matched to the interrupted runner and confirmed disposable.
- If verification finds a wrong migration, unexpected employees, grant, active call or unknown guard, do not start the worker or run the UI deployment. Capture sanitized evidence and return for a new decision.
- If API/web fail after starting, stop at the failed service and retain logs. Do not rebuild or migrate as an automatic retry.
- Rollback is to stop only services started in this recovery and preserve both the original volume and new backup. Restoring the older Oct 19 dump is not a rollback option for the current database without an explicit Owner decision and a fresh pre-restore backup.

The worker retry loop was stopped during approved PostgreSQL recovery because it had `restart: unless-stopped`, repeatedly logged unavailable DB and used CPU while unable to work. The scoped command in section A succeeded; worker remains stopped.

## UI Fix 07 deployment readiness after recovery

The following required preconditions are currently missing or unverified:

- PostgreSQL healthy and WAL recovery/readiness established. DB is at Alembic 0010; full integrity scrub/restore test has not been run.
- Fresh verified backup exists; the Oct 19/0009 dump remains stale.
- Demo Corporation and exactly three employees/versions confirmed.
- Grants, model calls and dispatch guard inspected: zero grants, zero calls, no held dispatch guard.
- Two retained `ac_pgtest_*` DB/role pairs are identified but provenance of the older 0009 pair is unresolved; no cleanup authorization.
- Effective CG01 strict proof/config needs re-read before dispatch-capable worker startup; it was not examined in the bounded stage.
- One healthy supervised Runtime worker after startup; worker is currently intentionally stopped.
- Full supported isolated PostgreSQL regression completion; the latest supported run was interrupted with a failed test and 25 errors, with traceback/cleanup gap.
- Current Owner authenticated session, deployed browser verification and screenshots. These were not performed during diagnosis.
- Stopped API/web container image IDs differ from current local tags; their intended deployment/recreation is not yet authorized in this incident task.

The previously completed web build and disposable browser checks remain historical UI Fix 07 evidence only. They do not satisfy the deployed-stack checks above.
