# Bounded recovery stage evidence

Owner response authorized: stop the looping worker, start existing PostgreSQL on its old volume, create/verify a current backup, then read-only inventory. No app, worker, migration or deployment restart was authorized.

## Process actions actually taken

```text
rtk docker compose stop --timeout 30 worker
Container agent-corporation-runtime-worker Stopping
Container agent-corporation-runtime-worker Stopped

rtk docker compose start postgres
Container agent-corporation-bootstrap-1 Starting / Started / Waiting / Exited
Container agent-corporation-postgres Starting / Started
```

Compose ran the already-completed bootstrap dependency while starting PostgreSQL. Bootstrap logs twice report that configuration/Owner were ready, the existing credential was kept, and no secret was printed. PostgreSQL remained the only app service started. Worker remains stopped; API/web remain exited; `migrate` was not run.

PostgreSQL startup log (sanitized): database was interrupted; automatic recovery started; redo completed; end-of-recovery checkpoint completed; server ready at `2026-10-20 04:12:54 UTC`. Container state was `running health=healthy`. The original volume name `agent-corporation_agent_corporation_postgres` remains attached and unchanged.

## Backup

```text
rtk docker compose exec -T postgres sh -ec '. /database-secrets/postgres.env; exec pg_dump -U "$POSTGRES_USER" -d "$POSTGRES_DB" -Fc' > .local/backups/pre-recovery-20261020T041305Z.dump
rtk chmod 600 .local/backups/pre-recovery-20261020T041305Z.dump
rtk docker run --rm -i --network none postgres:18.6-alpine@sha256:77f585114c32fbca283dc835b0596f4e52b51b4c6662d7810b2f4084f60a1873 pg_restore --list < .local/backups/pre-recovery-20261020T041305Z.dump > /dev/null
```

All commands exited 0. Backup metadata: 149,205 bytes, mode `0600`, SHA-256 `9f79139089206c6972345a6c95fca6863ee4d9d49330befe6ddaf9baa852f500`. The file is in the ignored `.local/backups/` directory and was not added to Git. `pg_restore --list` validated archive readability only; no restore rehearsal was performed.

## Read-only inventory results

Read using `psql` with credentials sourced inside the PostgreSQL container; password/config content was not printed.

| Query | Result |
|---|---|
| Current DB and DB role | `agent_corporation` / `agent_corporation` |
| Alembic revision | `20261020_0010` |
| Matching company | `Demo Corporation`, 1 row |
| Employees / EmployeeVersion rows | 3 / 3 |
| Runtime runs | 0 |
| Model calls / unfinished model calls | 0 / 0 |
| Inference grants / eligible grants | 0 / 0 |
| Global `runtime_dispatch_guard` rows / held spans | 1 / 0 |
| Test DB and matching role count | 2 pairs |

Retained test objects (not modified):

| Database | Owner | Size | Revision | Public tables | Matching role flags |
|---|---|---:|---|---:|---|
| `ac_pgtest_b5a524b249704b46` | `agent_corporation` | 10 MB | `20261020_0010` | 33 | LOGIN; not SUPERUSER; cannot CREATEDB |
| `ac_pgtest_c96cbe5c98704b10` | `agent_corporation` | ~10 MB | `20261014_0009` | 32 | LOGIN; not SUPERUSER; cannot CREATEDB |

The 0010 disposable DB is consistent with the interrupted runner's migration. The older 0009 DB may be from an earlier run. PostgreSQL does not retain a creation timestamp in this inventory; exact run attribution is not proved. Do not delete either until the Owner authorizes a separate, targeted cleanup after attribution.

No query or action read or changed CG01 configuration/proof. No API or web container was started, no inference grant/model call was created, and no Runtime worker was started.
