# P0 Recovery Stage 2 — API and web

**Date:** 2026-10-20 (UTC timestamps below)  
**Scope:** Start and verify the existing Agent Corporation API and web containers only. No worker start, image rebuild, database restore, test run, grant, inference, or deployment was authorized.

## Outcome

The existing API and web containers are running and healthy. The API readiness endpoint reports PostgreSQL ready. The existing web container serves the current Overview and demo dashboard. The Runtime worker container remains stopped.

One Compose behavior is material: `docker compose start api` started the completed `bootstrap` and `migrate` dependencies before it started API. The migrate container ran its configured `alembic upgrade head` command and exited 0. Timestamped logs for this invocation show Alembic initializing its PostgreSQL context but no `Running upgrade` line. The shared database was at `20261020_0010` before this action and remains at `20261020_0010`; no revision change or data-count change was observed. This was a no-op at the current head, but the dependency command did run and is recorded as an unexpected Compose side effect. No further Compose start command was used; the existing web container was started directly by container name after API readiness passed.

## Exact actions

1. Read the P0 report, recovery plan and previous recovery evidence; checked `compose.yml`, existing container state, startup command/source, image IDs, the backup, database state, worker state and dispatch-capable queue state.
2. Confirmed the existing backup still has mode `0600`, size `149205` bytes and SHA-256 `9f79139089206c6972345a6c95fca6863ee4d9d49330befe6ddaf9baa852f500`.
3. Ran `rtk docker compose start api`. Compose started bootstrap, then migrate, and then API. Bootstrap reported that existing config/Owner credentials were retained. Migrate exited 0. API became healthy.
4. Checked API readiness at `http://127.0.0.1:15501/api/v1/health/ready`; it returned HTTP 200 with database `ok`.
5. After API passed, ran `rtk docker start agent-corporation-web` to start the existing web container without invoking Compose dependencies again.
6. Verified web health and Overview through `http://127.0.0.1:15500/`. No Owner secret was read or entered. The Office route showed the Owner authentication prompt, so authenticated Office/Inspector/Replay data was not accessed.
7. Rechecked the database and all service states after browser navigation. No tests, migration command issued directly, restore, grant creation, Runtime call, worker start, image rebuild, or UI Fix 07 deployment was performed.

## Service state

| Service | Before | After | Image used by existing container |
|---|---|---|---|
| PostgreSQL | Running, healthy | Running, healthy | `postgres:18.6-alpine@sha256:77f585114c32fbca283dc835b0596f4e52b51b4c6662d7810b2f4084f60a1873` |
| API | Exited (255) | Running, healthy | `sha256:284d0aa93e378c76ebf176d154ef3722d958ba5e01992ee5c178ae5588d510b9` |
| Web | Exited (255) | Running, healthy | `sha256:e8bb4264a40e5177541498959f37bd887c93ab287896591214af2811f1db8f29` |
| Runtime worker | Exited (1) | Exited (1), still stopped | `sha256:284d0aa93e378c76ebf176d154ef3722d958ba5e01992ee5c178ae5588d510b9` |
| Bootstrap | Exited (0) | Exited (0), reran during API start | `sha256:284d0aa93e378c76ebf176d154ef3722d958ba5e01992ee5c178ae5588d510b9` |
| Migrate | Exited (0) | Exited (0), reran during API start | `sha256:284d0aa93e378c76ebf176d154ef3722d958ba5e01992ee5c178ae5588d510b9` |

The current local image tags do not point to the images in the existing API/web containers: `agent-corporation-api:local` is `sha256:4430971cf6a69fd745c55bb5cf7623b1d82bf569e01408d1b32dfa674f202875`; `agent-corporation-web:local` is `sha256:70a7ccd83dd4cb80ae4e3cadc90873507aff94aced331cb97d4ccaf690eb9921`. The containers were not recreated. This running web version is not evidence of UI Fix 07 deployment.

## Database and backup verification

The shared database remains on the original Compose PostgreSQL volume and reports Alembic revision `20261020_0010` both before and after startup. Post-start read-only counts:

| Check | Result |
|---|---:|
| Demo Corporation rows | 1 |
| Employees / EmployeeVersion rows | 3 / 3 |
| Departments | 2 |
| Runtime runs | 0 |
| Model calls | 0 |
| Inference grants / eligible grants | 0 / 0 |
| Dispatch guard held | No |
| Active Playground sessions / queued or dispatched turns | 0 / 0 |

The backup remains `.local/backups/pre-recovery-20261020T041305Z.dump`, mode `0600`, 149,205 bytes, SHA-256 `9f79139089206c6972345a6c95fca6863ee4d9d49330befe6ddaf9baa852f500`. Its prior `pg_restore --list` verification remains archive-readability evidence, not a restore rehearsal.

The two retained test database/role pairs were not modified or deleted:

| Database | Owner | Size | Revision | Role flags | Activity at check |
|---|---|---:|---|---|---|
| `ac_pgtest_b5a524b249704b46` | `agent_corporation` | 10 MB | `20261020_0010` | LOGIN; not SUPERUSER; cannot CREATEDB | No sessions |
| `ac_pgtest_c96cbe5c98704b10` | `agent_corporation` | 10,182 kB | `20261014_0009` | LOGIN; not SUPERUSER; cannot CREATEDB | No sessions |

The interrupted integration run remains inconclusive. This stage did not use the shared-server test runner or change its historical result.

## API, web and authentication checks

- API `/api/v1/health/ready`: HTTP 200, `{"status":"ok","checks":{"database":"ok"}}`.
- Web `/healthz`: HTTP 200, body `ok`; `/`: HTTP 200; same-origin proxied API readiness: HTTP 200.
- Web access logs show HTTP 200 for the page, JS/CSS assets, health endpoints and `/api/v1/demo/dashboard`.
- Overview rendered Demo Corporation, three personnel records, two departments, five demo Work Orders and 20 fixture events. The page states that demo data does not create a real agent or call a model.
- Office showed the Owner login prompt and made an unauthenticated `GET /api/v1/owner/session` that returned HTTP 401. This is expected authentication behavior. The Owner credential was not read, exposed or entered, so authenticated Office, Runtime, Inspector and Replay content was not checked.
- No request created a Work Order, grant, Run, Playground turn or synthetic record.

## CG01, grants and dispatch state

- The existing API container environment has `RUNTIME_CG01_DEMO_TEST_OVERRIDE=false`, `CODEX_SERVER_TRANSPORT=docker-host`, `CODEX_SERVER_BASE_URL=http://host.docker.internal:15600`, and `PLAYGROUND_WORKER_ENABLED=true`.
- `/runtime-secrets/cg01-proof.json` is absent in the running API container. The effective Runtime gate is therefore strict and blocked (`allowed=false`, `verified=false`); no CG01 policy was changed intentionally.
- The host source `.local/cg01-proof.json` was absent at preflight. Compose reran bootstrap, and `scripts/docker_initialize.py` unlinks `/runtime-secrets/cg01-proof.json` when that source file is absent. The runtime proof was not inspected before bootstrap ran, so I cannot prove that bootstrap left the pre-start proof file unchanged. The current effective state is strict and blocked, but this implicit bootstrap side effect is an unresolved policy-file change risk and should be reviewed by the Owner.
- The API process supervises the Development Playground worker internally because `PLAYGROUND_WORKER_ENABLED=true`. Before and after startup there were no Playground sessions, queued turns or dispatched turns. No Playground model call was observed.
- The separately supervised Runtime worker container remains stopped. Runtime runs, model calls and inference grants remain zero, and the global dispatch guard is unheld.

## Sanitized diagnostics and unresolved points

- API and web health checks pass. No application HTTP failure was observed in the browser smoke or service logs. The expected unauthenticated Owner session request returned 401.
- Web entrypoint logged that it could not modify Nginx's default configuration on the read-only filesystem. Nginx then reported configuration complete, became healthy, and served the page and assets successfully; this is a startup warning with no observed functional impact.
- Browser console showed one `TypeError` from the installed Chrome extension (`chrome-extension://…/executors/200.js`, reading `M_ID`). It is outside the Agent Corporation origin and is classified as extension noise; no app-origin console error was observed.
- The current API image and the current `:local` image tag differ. The existing container was intentionally preserved. The current web container likewise predates the current local web tag.
- Compose's `start api` starts `bootstrap` and `migrate` dependencies even though API was the requested target. The bootstrap run reported retaining existing config/Owner credentials. The migration container executed its configured Alembic command; timestamped output for this start has no upgrade statement, exit was 0, and the revision remained `20261020_0010`. Avoid `docker compose start api` for future recovery until dependency behavior is explicitly accounted for.
- The bootstrap's CG01 proof synchronization could not be compared to its pre-start runtime-volume state; see the CG01 section. The current state is blocked, but no claim of unchanged proof-file bytes is made.
- No Owner login was established, no authenticated route data was inspected, and no UI Fix 07 visual acceptance was performed.

## Readiness recommendation

Keep the Runtime worker stopped. Do not run the interrupted integration suite against the shared PostgreSQL service. First give PostgreSQL regression tests a dedicated disposable PostgreSQL server/project and volume, independent of the application database; retain full test output and verify cleanup there. Preserve the current backup and both retained test database/role pairs until their provenance is established.

Before a separately authorized UI Fix 07 deployment, reconcile the stopped-container/current-tag image mismatch, verify the deployment's migration behavior without automatic dependency execution, and create a fresh verified backup. Then deploy only the approved Agent Corporation services and perform the separately scoped Owner UI acceptance. This recovery stage does not authorize that deployment or starting the Runtime worker.
