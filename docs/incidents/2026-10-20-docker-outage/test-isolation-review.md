# Isolated PostgreSQL runner review

## Current behavior

`scripts/test_playground_isolated.py` is **database-name isolated, but not PostgreSQL-server isolated**:

1. Loads app settings and selects `migration_database_url` or `database_url` as the admin URL.
2. Creates a random `ac_pgtest_<16 hex>` database on that server. The database name is asserted against a strict pattern, and a same-named role plus random password is prepared for the test app.
3. Removes inherited `APP_CONFIG_FILE`, overrides both application and migration URLs to point at that database, opts into Playground/Phase 06 persistence tests, and disables the Playground worker.
4. Runs Alembic head and the API test suite as subprocesses, capturing output and redacting the generated password, configured app password and source URL password.
5. In `finally`, reconnects to the original server, drops the named database `WITH (FORCE)`, then drops the role. If reconnect or database drop fails, later cleanup and the success message are skipped; there is no cleanup verification. A failure return code is preserved only if cleanup succeeds. Full runner/test output was not saved for the interrupted run.

This architecture can contend for CPU, memory, connections, disk IO and WAL on the same PostgreSQL server and Docker VM as the shared runtime. Random database naming prevents collision with the runtime database but does not isolate server resources, network, Docker project or PostgreSQL cluster. It explains why an isolated DB test can interrupt shared service availability; it does **not** prove the test caused the Docker Desktop SIGTERM.

## Safer architecture proposal

1. Add a test-only Compose file and unique project name, e.g. `ac-pgtest-<run-id>`. It defines only a pinned PostgreSQL test service and a test-runner service built from the API source.
2. Keep both on a project-private network with no external/shared Docker network, no `host.docker.internal`, no host bind mount, and no application runtime secrets. The test runner talks only to the test service DNS name. Where a test specifically needs a fake gateway, use an in-project fake service; otherwise deny outbound network.
3. Use a project-scoped disposable volume or tmpfs data directory, unique database/role/password per run. Never mount `agent-corporation_agent_corporation_postgres`, runtime secrets, artifacts or gateway auth.
4. Add fail-closed startup checks in the runner: require the expected unique project/test service hostname, test DB name prefix and test-role prefix; reject the shared DB host/port, `host.docker.internal`, `agent-corporation-postgres`, runtime DB name and production-like connection targets. Check the live `current_database()`, `current_user`, server address and Compose project labels before migration and again before pytest.
5. Apply explicit CPU/memory/PID limits on PostgreSQL and runner containers sized to actual suite requirements. Observe test server health and host load; if the test project or shared stack becomes unhealthy, stop test execution and preserve logs.
6. Make cleanup idempotent and verifiable: terminate only the unique runner project, assert its project label/name and random run ID, remove only that project's named test volume/network/containers, then verify no resources with that exact label remain. Do not call global prune or touch the app project.
7. Preserve complete, sanitized test output and cleanup status outside the shared DB. If test runner exits abnormally, report test exit and cleanup result separately; never convert cleanup failure into a passing or clean test result.

The architecture should first be validated with a dry-run resource inventory and an isolation test that deliberately gives the runner the shared URL and proves it exits before connecting. Do not rerun the current runner against the shared PostgreSQL server; the Owner's bounded authorization did not include a test rerun, and the architecture still has shared-server resource exposure. This incident diagnosis did not modify the runner or tests.
