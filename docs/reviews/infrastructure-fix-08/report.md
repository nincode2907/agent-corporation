# Infrastructure Fix 08 — implementation report

**Current status (2026-10-20): isolated runtime verification passed; Infrastructure Fix 08 is ready for Owner deployment review.** The initial blocked result recorded below is historical and was superseded after a bounded VM memory probe made capacity measurable. No shared Agent Corporation service, volume, database, gateway, proof, grant, or worker was changed. No phase or roadmap status was changed. See [final verification results](../infrastructure-fix-08-1/verification-results.md) and [combined deployment plan](../infrastructure-fix-08-1/final-deployment-plan.md).

## Implemented

- `compose.yml` places bootstrap and Alembic migration behind the explicit `setup` profile and removes them from PostgreSQL/API/Runtime worker dependency chains. API still waits for healthy PostgreSQL; web still waits for healthy API. The Work Order Runtime worker is opt-in through `runtime-worker` and still waits for API and PostgreSQL health.
- API process startup now validates required config and a read-only PostgreSQL catalog schema contract, including the `runtime_reconciliation_decisions` table introduced in `20261020_0010`. Readiness reports `schema_incompatible`; startup stops with a safe message pointing to the explicit migration procedure. It does not migrate or seed.
- The standalone Runtime worker validates config/schema before polling. The existing Playground supervisor remains separately controlled by `PLAYGROUND_WORKER_ENABLED` as before.
- `docker_initialize.py` no longer synchronizes or removes CG01 proof. Added `proof-admin` behind the explicit `operator` profile and `scripts/manage_cg01_proof.py` for status, explicitly confirmed install, and explicitly confirmed revoke. Install reads stdin, validates against the existing strict gate, writes atomically, and audits only action metadata and SHA-256 hashes. No proof was created, installed, restored, or revoked in this task.
- Replaced the prior same-server PostgreSQL runner with unique Compose projects and dedicated disposable PostgreSQL, volume, and internal network. Database targets are fully checked before connector creation; pytest and Alembic run in a bounded test container with synthetic DB credentials and no shared secret/gateway mounts. Cleanup is label-scoped and verified; full sanitized logs and independent counts are retained when tests run.
- Updated README and Windows/macOS startup instructions to document explicit setup, ordinary restarts, proof operations, and isolated verification.

## Initial verification results (historical; superseded)

| Check | Result |
|---|---|
| Python syntax compilation for changed Python sources/tests | Passed |
| Runtime and disposable `compose.test.yml` config validation | Passed |
| `git diff --check` | Passed |
| Disposable startup-contract Compose smoke | Not run; blocked by Docker resource preflight |
| Isolated PostgreSQL migration + full API/Runtime/Playground suite | Not run; blocked before Compose startup |
| Passed / failed / skipped API tests | N/A; pytest did not start |
| Pytest warnings | N/A; pytest did not start |
| Disposable project cleanup | Not needed; no Compose resources were created |
| Live proof-admin install/revoke behavior | Not run; no runtime proof was touched |

The first isolated runner stopped before `docker compose up`, with blocker `Docker VM capacity is below the isolated test budget`. The first manifest preserved the stop but its old exception path failed to retain the capacity sample; this bookkeeping path is corrected in source, and the original manifest is preserved with an adjacent review note. A read-only retry reported 5,173,080,064 bytes Docker memory and 4 CPUs, but `docker stats --no-stream` then timed out after 40 seconds, so current memory usage/free could not be sampled reliably. Host disk reported 78,314,304 KiB free at 82% use. The configured 2.5 GiB estimated-free requirement was not lowered. See `evidence/20261020T062710Z-b2d1babc/` and `evidence/resource-preflight-current.json`.

There are no application test failures to classify because the suite never ran. Existing tests for expired/mismatched proof remain in the API suite, but the new disposable end-to-end startup proof-persistence test is also unexecuted. Static validation is not represented as runtime acceptance.

## Current shared stack observation (read-only)

Docker inspection showed PostgreSQL running/healthy, web running/healthy, and API running/unhealthy. Existing container image IDs do not match current local image tags:

| Service | Running container image ID | Current local tag image ID | State |
|---|---|---|---|
| API | `sha256:284d0aa93e378c76ebf176d154ef3722d958ba5e01992ee5c178ae5588d510b9` | `sha256:4430971cf6a69fd745c55bb5cf7623b1d82bf569e01408d1b32dfa674f202875` (`agent-corporation-api:local`) | running, unhealthy |
| Web | `sha256:e8bb4264a40e5177541498959f37bd887c93ab287896591214af2811f1db8f29` | `sha256:70a7ccd83dd4cb80ae4e3cadc90873507aff94aced331cb97d4ccaf690eb9921` (`agent-corporation-web:local`) | running, healthy |
| PostgreSQL | `sha256:d7a8005067f55a2f8ea369e767545fd467b1943a4f0f1a48b7dc44f06c366109` | pinned PostgreSQL `18.6-alpine` digest | running, healthy |

This task did not connect to or mutate the shared database. Prior recovery-stage evidence records revision `20261020_0010` and the three Demo Corporation employees; deploy planning must re-check those facts and the backup before a later authorized deployment. The observed API health issue remains unresolved here. No worker start, rebuild, migration, browser check, or UI Fix 07 deployment was attempted.

## Remaining Owner decisions

1. Arrange Docker Desktop capacity/health so `docker stats --no-stream` responds and the preflight has at least 2.5 GiB estimated free Docker memory; then rerun isolated verification serially.
2. Review the verified isolated results before authorizing deployment of this startup contract and UI Fix 07.
3. Authorize any later supervised Runtime worker start separately. CG01 must remain strict and no inference grant is created by this task.

## Final verification disposition

The previously missing isolated verification is now complete. Final API/Runtime/Playground tests: **279 passed, 0 failed, 1 platform skip, 1 deprecation warning**; disposable migration reached `20261020_0010`; startup smoke passed; focused isolation/schema guards passed 22 tests; test and smoke project resources were independently removed. The final source correction fixes the schema contract's mistaken expectation that `employee_version_id` belongs to `runtime_runs` instead of `runs`.

The deployment readiness and image table above are historical read-only observations and must be rechecked immediately before any later authorized deployment. The next requested action is Owner review and explicit authorization of the combined Fix 08 / UI Fix 07 deployment plan.
