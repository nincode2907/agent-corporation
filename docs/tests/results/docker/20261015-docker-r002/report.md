# Docker deployment independent retest — r002

- Supersedes: [r001 independent review](../20261015-docker-r001/report.md).
- Remake: [r001 remediation record](../../../../remakes/docker/20261015-docker-r001/remake.md).
- Snapshot: 2026-10-15 11:50–11:52 Asia/Ho_Chi_Minh; dirty worktree; relevant source hashes in [manifest](evidence/source-manifest-r002.txt). The Nginx resolver addition arrived after the focused pytest run; its current config was inspected and Compose syntax revalidated.
- Evidence: [commands and execution boundaries](evidence/commands.txt).
- Verdict: **no remaining source finding in reviewed Docker scope on this snapshot**. R001 findings DKR-01 and DKR-02 pass their scoped retests. The fixed Nginx resolver/upstream passed source/config inspection and root's final isolated API-recreate recovery case. This is a technical deployment review, not phase acceptance or Owner approval.

## R001 finding retests

### DKR-01 — Docker-host CG01 release check

`test_strict_proof_is_bound_to_docker_endpoint_and_transport` constructs a valid synthetic Docker-host proof in a temporary directory, checks that a mismatched transport is denied, then checks that a proof with `gateway_transport="docker-host"` is accepted by `scripts/cg01_mode.py::release_check`. The focused suite passed. This verifies the transport identity boundary and release-check wiring without inference or network dispatch.

### DKR-02 — bootstrap owner mapping

On POSIX, `run.sh` exports the host `id -u`/`id -g`; Compose uses those values as the bootstrap service user. With this host's UID/GID 503:20, rendered Compose config resolved `user` to `503:20`. A disposable networkless container using UID/GID 503:20 created only fixture data on tmpfs; observed directory 0700 and file 0600, owned by UID503. No host bind mount or real secret was used. This proves effective nonroot container identity and file modes. It does not establish Windows ACL or Docker Desktop host-file ownership mapping.

## Safe checks and running deployment read

- Focused suite covering Docker gateway, gateway contracts, Phase 06 runtime, Playground, Owner auth, CG01 mode and health: **99 passed, 1 skipped**, one Starlette/httpx deprecation warning.
- Normal Compose and bootstrap overlay `config --quiet`: PASS.
- Read-only `docker compose ps`: API, web and PostgreSQL report healthy.
- Read-only GETs to `/api/v1/health/live` and `/api/v1/health/ready`: both HTTP 200.
- Root separately reports the final isolated Docker runner completed ALL PASS for fresh migration, UID1000/Owner secret mode600, Owner auth/CSRF/SSE under five seconds, zero model calls, cookie persistence/revocation after API restart, API recreation followed by Nginx proxy recovery, PostgreSQL-down liveness/readiness, and cleanup limited to disposable project `ac-docker-test-e101adacd0`. The reviewer did not run the isolated runner or touch the database.
- Source follow-up: Nginx resolves only the fixed `api` service through Docker's embedded resolver (`127.0.0.11`, 5-second cache) and uses a fixed upstream variable to refresh the API address after container recreation. Compose config is valid; the root-run isolated recreation case passed.

## Review boundaries and unresolved platform limits

- Windows was not tested. `run.bat` leaves the Compose default bootstrap UID/GID at 1000:1000, and Windows Docker Desktop ACL/ownership behavior has not been validated. Treat Windows first-run secret ownership as unverified until exercised on Windows.
- The isolated runner and fake-transport tests do not prove real gateway entitlements, actual inference, or release acceptance. No inference grant or Owner acceptance is implied.
- The running app health probe confirms only liveness/readiness; this reviewer did not call Owner/private endpoints, run worker dispatch, migration, DB mutation or restart.
