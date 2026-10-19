# Docker deployment independent review — r001

- Snapshot: 2026-10-15 11:46 Asia/Ho_Chi_Minh; dirty worktree.
- Scope: Docker Compose/bootstrap, API and web images, Nginx, secret init, run scripts, settings, gateway transport, CG01 checks and worker startup/propagation.
- Snapshot hashes: [source manifest](evidence/source-manifest-r001.txt).
- Command evidence: [commands and run boundaries](evidence/commands.txt).
- Verdict: **need-change at the reviewed source snapshot**. Two concrete defects were found and reported; root remediated both while the review was running. The report preserves those findings and their source-before/source-after state. Final remediated snapshot needs independent r002 retest.

## Findings

### DKR-01 — Docker-host CG01 proof rejected by release-check

- Severity: P2, release-gate correctness.
- Before: `scripts/cg01_mode.py` called `check_gate(..., base_url=...)` without `transport_mode`; `check_gate` defaulted to `loopback` while Docker settings and valid proof use `docker-host`. A valid Docker-host proof was therefore reported `gateway_transport_mismatch`, blocking strict release verification. This was fail-closed (no dispatch bypass), but Docker deployment could not pass its required release check.
- Evidence: pre-change `scripts/cg01_mode.py` HEAD SHA-256 `feba332e22c32ba233f617929cb01e6903fbeaebb45cc69f534b3edb21602561`; current-at-report hash `a3e0acfdf0c19737609faf8d5b5f7dc69121e24dc792bb69cc8f12cb0dbdab37`. Current code at lines 35–36 passes `settings.codex_server_transport`. Runtime Dockerfile now copies `scripts/cg01_mode.py` into the image.
- Status: root remediation applied during review; synthetic Docker-proof retest pending in r002. Do not treat as independently retested here.

### DKR-02 — bootstrap created inaccessible host secret files on Linux

- Severity: P2, first-run setup.
- Before: `compose.bootstrap.yml` ran the helper as default root while bind-mounting the repository read/write. `docker_bootstrap.py` delegates to `bootstrap_local.py` / `bootstrap_owner.py`, which create `.env` and `.local/owner-secret` mode 0600 without changing owner. On Linux this leaves the files owned by container UID 0; the invoking host user cannot read or manage the Owner credential and may be unable to rerun setup.
- Evidence: pre-fix compose hash `bbba66c6b13c0d285461c9b05131fc5c9c23b6e7933be268542ce70e47da0ebc`; `bootstrap_local.py` creates with mode 0600 and `bootstrap_owner.py` creates owner secret with mode 0600. The compose helper was root by default.
- Status: root remediation applied during review: bootstrap service now uses `${BOOTSTRAP_UID:-1000}:${BOOTSTRAP_GID:-1000}`; `run.sh` exports actual host `id -u`/`id -g`; `run.bat` defaults to 1000. Static config passes after the change. Windows ownership behavior remains unverified and should be retested on Windows.

## Security and boundary review

- Gateway destination validation is a strict allowlist: Docker mode accepts only `http://host.docker.internal:15600`; loopback mode requires a literal loopback IP. Probe traffic disables environment proxies and redirects; gateway POST uses bounded request/response bodies, preserves the required gateway `Host`, rejects CR/LF in API key, and does not replay uncertain calls.
- CG01 transport identity is checked against proof metadata. The demo override remains explicit and scoped; Docker defaults it off. Work Order worker is opt-in under the `worker` Compose profile. The API-owned Playground worker may start by default but only processes the Playground queue under its separate Owner grant/session checks; it does not run Work Orders.
- API runtime is UID 1000, read-only root, dropped capabilities, no-new-privileges, readonly gateway source mounts and readonly runtime-secret mount. The secret init is a one-shot root helper with no network, verifies regular-file/mode/size, uses no-follow opens, and copies into a UID-1000-owned 0700 volume. PostgreSQL uses the explicit existing volume name for durable reuse. Nginx forwards the original Host for the API local Host/Origin checks, disables buffering for SSE, and is published only on IPv4 loopback.
- Compose configuration checks passed. No Docker build or container start was performed by this reviewer. Root independently reported an isolated-runner pass for startup, migration, security/session/SSE, restart preservation, database-down readiness, and disposable-only cleanup; final rebuilt-image rerun was pending at report time.

## Test evidence and limits

- Focused safe API suite: **79 passed, 1 skipped**, one Starlette/httpx deprecation warning. Exact command is in the evidence file. Windows was not run.
- `docker compose config --quiet`: PASS. Bootstrap overlay config: PASS before and after the UID change.
- The focused suite proves contract/unit behavior only; it is not proof of a running Docker deployment. The isolated Docker test was not run by this reviewer to avoid concurrent execution. No production database, migration, restart, gateway dispatch or inference was used.
- Technical review only; no Owner acceptance or deployment approval is implied.
