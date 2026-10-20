# Infrastructure Fix 08 / 08.1 — final verification results

**Captured:** 2026-10-20 UTC. The prior Fix 08 and Fix 08.1 blocked reports are historical; reliable Docker VM memory was subsequently measured and the authorized isolated verification completed. Shared Agent Corporation services and data were not touched.

## Docker capacity and memory probe

The bounded probe ran from the pre-existing pinned PostgreSQL image `sha256:d7a8005067f55a2f8ea369e767545fd467b1943a4f0f1a48b7dc44f06c366109`. It used no network or mounts, a read-only root filesystem, 64 MiB memory and swap, 0.25 CPU, 16 PIDs, UID 65534, dropped all capabilities, and an 8-second timeout.

| Source and scope | MemTotal | MemAvailable | CPUs | Workspace free | Result |
|---|---:|---:|---:|---:|---|
| Docker Engine / Docker Desktop Linux VM `/proc/meminfo`, 2026-10-20 09:10:33 UTC | 7.76 GiB | 4.91 GiB | 4 | 86.99 GiB | Capacity confirmed |
| Startup smoke fresh preflight, same VM scope | 7.76 GiB | 4.92 GiB | 4 | 86.98 GiB | Capacity confirmed |

The probe's `MemTotal` exactly matched Engine total; its cgroup cap remained 64 MiB, so the measurement is VM-wide rather than the probe limit. Available memory exceeded the unchanged 2.5 GiB threshold. `/proc/pressure/memory` was not exposed by this Docker VM (`UNSUPPORTED`); the measured `MemAvailable` source remained reliable and fresh. Each probe removed its unique labeled container and independently verified no matching container remained. See [final probe evidence](evidence/docker-vm-memory-probe-final.json).

## Isolated PostgreSQL migration and API/Runtime/Playground tests

Run: `20261020T091031Z-a64b7877`; disposable Compose project: `ac-pgtest-47781bf06436`.

| Result | Count |
|---|---:|
| Passed | 279 |
| Failed | 0 |
| Skipped | 1 |
| Pytest warnings | 1 |
| Errors | 0 |

The one skip is `apps/api/tests/test_owner_auth.py:50` (`Windows ACL contract`), which is platform-specific. The warning is Starlette's `TestClient` deprecation notice for the installed `httpx` integration. Neither hides an isolated PostgreSQL persistence test: both Phase 09 queue lease tests were enabled and executed after fixing a real test `NameError`.

Migration from an empty disposable PostgreSQL database succeeded through `20261020_0010`. The application role could read `employee_versions`; the database identity probe confirmed it connected only to the generated `ac_pgtest_*` database over the private Compose network. No host port was published. Runtime tests use a dead local gateway endpoint or fakes; the smoke database reported zero model calls and zero Playground turns.

Evidence includes [full pytest log](../infrastructure-fix-08/evidence/20261020T091031Z-a64b7877/api-tests.log), [migration log](../infrastructure-fix-08/evidence/20261020T091031Z-a64b7877/migration.log), database provisioning/identity logs, run manifest, cleanup log, and resource observations.

## Focused isolation and schema-contract guards

Command: `rtk proxy uv run --project apps/api pytest apps/api/tests/test_isolated_runner_guards.py apps/api/tests/test_database_schema_contract.py -q`.

**22 passed, 0 failed, 0 skipped, 0 warnings.** The full API suite also includes these tests.

## Disposable Compose startup smoke

Run: project `ac-docker-test-abd336ffca`; status **passed**. It built and ran isolated bootstrap, PostgreSQL, explicit migration, API and Nginx web services. Migration identity was `agent_corporation` / `20261020_0010`; API `database_is_ready()` passed after correcting the schema contract.

The smoke verified explicit initialization/migration order, normal API/web restart without setup dependencies, strict expired-proof preservation, non-root UID 1000, Owner secret permissions, login/session, Host/Origin/CSRF boundaries, SSE first frame under 5 seconds, restart-preserved auth/logout, API recreate and Nginx service discovery, plus liveness/readiness behavior with PostgreSQL stopped. Database model calls remained zero. The Runtime worker profile stayed excluded and no worker was running.

Cleanup independently found zero remaining project-labeled containers, volumes, networks, or tagged API/web images. See [startup smoke manifest](startup-smoke/ac-docker-test-abd336ffca/run-manifest.json).

## Source corrections found during execution

- The API startup schema contract required `runtime_runs.employee_version_id`, while migration 0005 stores that identity on `runs`. This caused a genuine fresh-install API startup failure. The contract now checks `runs.employee_version_id` and only requires the runtime run's own key columns; a regression test documents the correct relation.
- The isolated test image now includes `compose.test.yml`, which one guard test reads from the repository root. Its assertion matches the PostgreSQL 18 data-volume parent path.
- The lifespan and worker database-sanitization tests now explicitly bypass only the independent startup schema guard they do not intend to test.
- The opt-in Phase 09 queue suite is enabled by the isolated runner; its expired lease test's `_admin` fixture binding was corrected after it failed on execution.
- The startup smoke helper now uses `os.chown` and keeps probe logs/manifests bounded and sanitized.

No test was weakened to reduce counts. The final full suite and smoke were rerun after the source corrections.

## Diff and disposition

`rtk proxy git diff --check` passed. Python compilation passed for changed API/test/runner sources. Disposable API and web images built successfully during smoke. Startup smoke also ran the current API/web routes against a synthetic Owner and isolated demo data.

**Infrastructure Fix 08 is ready for Owner deployment review.** This is not deployment approval, phase acceptance, a Runtime worker start, inference authorization, or UI Fix 07 acceptance. See the [minimal combined deployment plan](final-deployment-plan.md).
