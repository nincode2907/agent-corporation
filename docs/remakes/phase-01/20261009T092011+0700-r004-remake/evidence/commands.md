# Commands — remake Phase 01 r004

## Frontend install command

- Working copy contained only `apps/web/package.json` and `apps/web/package-lock.json` under a temporary root, matching the README path.
- Exact command tested: `rtk proxy npm --prefix apps/web ci` from that root.
- Result: exit 0; 28 packages installed; npm lifecycle warning only; temp directory removed after the check.
- The repository's existing `node_modules` was not replaced.

## Isolated baseline and DB-down check

- Created disposable PostgreSQL 18.6-alpine container `ac-p01-r004-pg`, pinned to `compose.yml` digest, with no named volume and Docker-selected loopback port `61530`; dummy credentials only.
- Copied API/web source to `/tmp/ac-p01-r004-copy`, installed dependencies in the copy, migrated only its empty test database to `20261008_0001` twice, and confirmed `current=20261008_0001` with only `alembic_version` in `public`.
- Started API copy on OS-selected `127.0.0.1:64268` and Vite copy on OS-selected `127.0.0.1:50658`; Vite proxy targeted the API copy.
- With database up, direct readiness returned HTTP 200 / `database=ok`. Stopped only `ac-p01-r004-pg`; liveness stayed HTTP 200, readiness returned HTTP 503 / `database=unavailable` without exception details, and web proxy returned the same statuses.
- Chrome CUA opened the isolated UI settings page. Accessibility tree showed API `Đang hoạt động`, PostgreSQL `Chưa kết nối`, and the readiness explanation. No gateway probe or POST.
- Stopped API/Vite test processes, auto-removed the container, deleted the temporary copy. The project DB/API/Vite remained running on their original listeners.

## Scope

- No API/DB project process was stopped or restarted.
- No migration ran on the project database.
- No gateway request, model call, inference, or secret read.
