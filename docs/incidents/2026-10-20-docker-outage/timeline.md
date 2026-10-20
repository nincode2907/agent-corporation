# Incident timeline

Times below are UTC. Host resource snapshots were collected later and are labeled separately. No causal link is inferred from temporal proximity alone.

| Time | Observation | Source / meaning |
|---|---|---|
| 01:59:00 | PostgreSQL 18.6 starts and reports ready. | PostgreSQL container log. |
| 03:39:05 | Last normal checkpoint completed before the outage. | PostgreSQL log. |
| 03:41:36–03:41:47 | Constraint, RLS and permissions errors appear from negative test cases. | PostgreSQL log; consistent with intentional denial tests, not evidence of server failure. |
| 03:42:28, 03:43:05 | PostgreSQL reports broken pipe and client connection lost. | PostgreSQL log; client/network cause is unknown. |
| 03:42:42–03:44:09 | Docker Desktop command telemetry records a `docker compose exec` CLI action lasting 87.76 seconds and exiting 1. | Docker Desktop log. This may correspond to a diagnostic `compose exec` attempted during the prior task, but telemetry does not include enough command/process identity to attribute it with certainty. The test runner itself does not invoke Docker CLI. |
| Through 03:42:55 | API readiness requests return HTTP 200. | API log; does not prove readiness after this time. |
| 03:44:07 | Docker Desktop Linux driver receives `SIGTERM`, requests graceful VM shutdown, and gets acknowledgement. | `com.docker.driver.amd64-linux.log.0` and stderr rotation. Initiating actor is unknown. |
| 03:44:27 | Hypervisor subprocess shuts down; Docker reports state `stopped` / engine stopped. | Docker Desktop driver/backend log. Confirms a common Docker VM/Engine interruption. |
| 03:44:33 | Docker Desktop log reports `Terminator: com.docker.backend cannot start`. | Downstream restart/startup issue; not enough context to identify cause. |
| 03:44:51 | Docker Desktop application/backend starts again. | Docker application/backend logs. |
| 03:44:57 | Driver reports Docker `starting`; VM launch follows. | Docker Desktop driver log. |
| 03:45:13.570–.584 | API, web and PostgreSQL container exit records all show code 255 and `OOMKilled=false`; finish times span 14 ms. | Docker container inspection. The nearly simultaneous exits do not show PostgreSQL first. |
| 03:45:21 onward | Worker repeatedly logs DB unavailable / no replay; Docker restarts it under `unless-stopped`. | Worker log. Test database/role cleanup may have failed. |
| After bounded Owner authorization | Stopped only the Runtime worker; started existing PostgreSQL on the same volume. Compose also ran the completed bootstrap dependency, whose log says existing config/Owner credentials were kept. | `docker compose stop --timeout 30 worker`; `docker compose start postgres`; bootstrap log. No API/web/migrate/worker restart. |
| 04:12:53–04:12:54 | PostgreSQL starts, detects improper shutdown, performs automatic WAL recovery, completes an immediate checkpoint and becomes ready. | PostgreSQL log; container health became `healthy`. |
| 04:13Z onward | Wrote and verified a new mode-0600 149,205-byte custom backup. Read-only inventory found DB at 0010, Demo Corporation with 3 employees/versions, no Runs/model calls/grants/held guard, and two retained `ac_pgtest_*` DB/role pairs at revisions 0010 and 0009. | `pg_dump`, pinned `pg_restore --list`, read-only `psql` inventory; details in [recovery-stage evidence](evidence/recovery-stage.md). |

The Docker Engine events query (`docker events --since 2026-10-20T03:40:00Z --until 2026-10-20T03:50:00Z`) returned no rows. Engine events are therefore not used to assign the trigger. At final review, PostgreSQL is healthy; API and web are still exited; worker is intentionally stopped. No action was taken on the two retained test DBs/roles.
