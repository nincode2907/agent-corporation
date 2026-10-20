# PostgreSQL regression isolation — Infrastructure Fix 08

## Isolation design

`scripts/test_playground_isolated.py` now provisions a unique Compose project per invocation from `compose.test.yml`. It creates a dedicated `isolated-postgres` container, project-scoped named volume and an internal-only network. PostgreSQL publishes only an ephemeral port on `127.0.0.1` for the runner's guarded setup probe. It has limits of 512 MiB RAM, 768 MiB memory plus swap, 0.75 CPU, and 96 PIDs.

The API test image is built with a project-unique image tag and runs in its own bounded container (1.5 GiB RAM, 2 GiB memory plus swap, 1 CPU, 256 PIDs). It joins only the internal Compose network, has a read-only root and temporary filesystem, and receives generated disposable database credentials. It has no mounts of the checkout, Owner/runtime/database secrets, artifacts, gateway source, or host credentials. `HOME` and temporary paths are inside its tmpfs. The gateway URL is a closed local port, the API key is empty, the CG01 override is false, and the worker is disabled.

All PostgreSQL URLs are parsed and compared field by field before SQLAlchemy creates a connector. The expected target includes host, port, database, user, and password. Shared runtime hostnames, database name, and port are explicitly rejected. A test supplies a shared database URL and proves the connector callback is never invoked. Admin role/database creation occurs only through the isolated PostgreSQL's loopback-published ephemeral port; migration and pytest run in the network-isolated test container against `isolated-postgres`.

Cleanup uses only the unique Compose project name and Compose project labels, then verifies that no labeled container, volume, or network remains. The generated API-test image tag includes the unique project ID and is removed by that exact tag; there is no global prune or image removal of shared tags. If cleanup fails, the runner retains the exact resource inventory and marks the run incomplete. It retains full sanitized logs for PostgreSQL startup, migration, pytest, cleanup, and isolated image removal, with independent passed/failed/skipped/warning counts when pytest ran.

## Resource safety

Before creating Compose resources, the runner records Docker VM memory/CPU, current container memory samples, and host filesystem free space. It requires at least 4 GiB total Docker memory, 2.5 GiB estimated free memory, 2 CPUs, and 2 GiB host free disk. Before tests, it checks at least 1 GiB available in the disposable PostgreSQL data filesystem. During the run it samples CPU/RAM for project containers, PostgreSQL volume usage, and host free disk every ten seconds.

The PostgreSQL separation prevents tests from connecting to or mutating Agent Corporation's server; it does not prevent Docker Desktop VM exhaustion or host-level pressure. The API regression suite and startup-contract Compose smoke test must run serially. Existing project containers were observed busy/unhealthy during this attempt, so the configured budget was not lowered to force a run.

## Verification status

The first runner invocation stopped before `docker compose up`: it reported that Docker VM capacity was below the isolated test budget. No test PostgreSQL container, project volume, or project network was created, and cleanup was not needed. Its first manifest did not retain the resource sample because the preflight exception path dropped it; the manifest is preserved and an explanatory review note is adjacent to it.

A follow-up read-only resource sample reported Docker total memory `5,173,080,064` bytes and 4 CPUs. The host filesystem had `78,314,304` KiB free at 82% use. A `docker stats --no-stream` retry exceeded its 40-second timeout, so current Docker memory use/free could not be established. The sample and limitation are in `evidence/resource-preflight-current.json`. The API suite, migration regression, negative connector guard test, cleanup path, and startup-contract Compose smoke test therefore have no execution result in this run; they are blocked, not passed or failed.

Existing `ac_pgtest_*` database/role pairs were not inspected or changed by this runner. The test runner creates new test names only inside the disposable server, and it does not connect to the shared PostgreSQL container.
