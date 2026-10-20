# Deployment readiness — report only

## Verdict

**Historical verdict: not ready, before isolated runtime verification completed. Current verdict: ready for Owner deployment review, not deployment.** The final isolated PostgreSQL suite and disposable startup smoke have now passed; see [final results](../infrastructure-fix-08-1/verification-results.md) and the [combined minimal plan](../infrastructure-fix-08-1/final-deployment-plan.md). The shared-service state and image IDs in this file are dated historical observations and must be rechecked before any later deployment.

## Minimal plan after isolated verification and separate Owner authorization

1. Resolve Docker Desktop resource reporting and run the isolated API suite and startup Compose smoke test serially. Require a clean project-label cleanup manifest.
2. Before touching the shared stack, inspect the working tree and current Compose project. Verify the existing database backup and checksum, confirm the shared schema revision is `20261020_0010`, and record the three Demo Corporation employees/EmployeeVersion associations. Re-check that there is no active model call, grant, held dispatch guard, or worker requiring intervention. Stop if any precondition fails.
3. Preserve all existing PostgreSQL, runtime-secret, and artifact volumes. Do not run `down --volumes`. Because the database is already reported at `20261020_0010`, do not invoke `migrate` unless a reviewed schema comparison proves it is required. The new API performs read-only compatibility checks and fails closed if the schema is missing/incompatible.
4. Deploy only the API and web source with `rtk proxy docker compose up --build -d api web`. This builds fresh project image tags and recreates requested services. PostgreSQL is only a healthy dependency; bootstrap and migration are not in the normal start dependency chain. Do not start the Runtime worker in this deployment step.
5. Verify API/web health, database revision/data, strict CG01 state, no new inference grants/model calls/runs, and no held dispatch guard. Keep the Runtime worker stopped until separately authorized.
6. After the UI Fix 07 source is loaded and these checks pass, use a local Owner session for the requested read-only desktop/mobile Office, Runtime, Inspector, and Replay verification. Do not create synthetic shared Runs or grants.

## Image identity observed before deployment

Docker inspection showed that the running API and web containers use different image IDs from the current local image tags. A later deployment must therefore build the current source explicitly; plain `docker compose start` cannot load these source changes.

| Service | Running container ID | Local tag ID |
|---|---|---|
| API | `sha256:284d0aa93e378c76ebf176d154ef3722d958ba5e01992ee5c178ae5588d510b9` | `agent-corporation-api:local` → `sha256:4430971cf6a69fd745c55bb5cf7623b1d82bf569e01408d1b32dfa674f202875` |
| Web | `sha256:e8bb4264a40e5177541498959f37bd887c93ab287896591214af2811f1db8f29` | `agent-corporation-web:local` → `sha256:70a7ccd83dd4cb80ae4e3cadc90873507aff94aced331cb97d4ccaf690eb9921` |
| PostgreSQL | `sha256:d7a8005067f55a2f8ea369e767545fd467b1943a4f0f1a48b7dc44f06c366109` | `postgres:18.6-alpine@sha256:77f585114c32fbca283dc835b0596f4e52b51b4c6662d7810b2f4084f60a1873` |

At inspection time API was `running/unhealthy`; web and PostgreSQL were `running/healthy`. Treat the API health issue as an unresolved pre-deployment blocker and diagnose it without running migrations or changing shared services. The current image IDs and health state are from read-only `docker inspect` evidence collected 2026-10-20.

## Invariants for the later operation

- Preserve the existing `agent-corporation_agent_corporation_postgres`, `runtime_secrets`, `database_secrets`, and `artifacts` volumes and all Demo Corporation data/Owner credentials.
- Keep CG01 strict and unchanged; do not install/restore proof or create an inference grant.
- Keep one Runtime worker stopped until a separate Owner action authorizes supervised startup.
- Do not deploy until the isolated suite and disposable startup test pass and a recoverable backup is confirmed.
