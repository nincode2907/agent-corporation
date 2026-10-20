# Single-Compose bootstrap independent review — r001

- Snapshot: 2026-10-19 09:15 Asia/Ho_Chi_Minh; worktree dirty.
- Scope: `scripts/docker_initialize.py`, API settings loader, `compose.yml`, initializer fixture tests, isolated runner and runtime Dockerfile.
- Source hashes: [manifest](evidence/source-manifest.txt). Commands: [evidence](evidence/commands.txt).
- Verdict: **no fixable source finding in the reviewed snapshot**. The requested credential separation and fail-closed paths are present in source and covered by safe fixture tests. This is not phase acceptance or Owner acceptance.

## Per-check tags

Each check below has one result tag; `clean` means the stated contract was supported by the fixture result or direct source/config evidence.

| ID | Check | Expected / actual | Tag |
| --- | --- | --- | --- |
| C01 | Single Compose config parses | `docker compose config --quiet` succeeds / exit 0 | `clean` |
| C02 | Empty checkout bootstrap is repeatable and does not write operator checkout | generated Owner/state persist identically after second initialize; operator fixture stays empty / passed | `clean` |
| C03 | Existing PostgreSQL without original or persisted credentials fails closed | initialization raises before writing state / passed | `clean` |
| C04 | Changed legacy DB credentials are rejected | mismatch raises and persisted state stays byte-identical / passed | `clean` |
| C05 | Legacy Owner import and shell/URI escaping | Owner bytes preserved; password round-trips through SQLAlchemy URL and sourced `postgres.env`, including literal shell-substitution text / passed | `clean` |
| C06 | API settings read private JSON and apply declared environment override | JSON settings load; runtime transport override is honored; unknown fields fail without secret echo / passed | `clean` |
| C07 | Admin credential separation in resolved Compose | API has app config only and no admin env/database-secret mount; migrate alone receives migration config / assertions passed | `clean` |
| C08 | Bootstrap execution boundary | bootstrap has network disabled; operator mount read-only; persisted volumes are separate / source/config inspection passed | `clean` |
| C09 | Docker gateway regression contracts | explicit Docker host allowlist, rejected alternative destinations, fixed Host header, proxy/redirect off, strict transport proof / focused tests passed | `clean` |

Focused command result: **17 passed**. No source case in this r001 snapshot is tagged `need-change` or `suggestion`.

## Source review

- Bootstrap is a one-shot, networkless Compose service. The root-only initializer reads operator files from a read-only project mount and writes persistent state into two distinct volumes. An advisory lock serializes initialization. Atomic temporary-file replacement, 0600 files, 0700 directories, and compare-before-write preserve generated values on repeated runs.
- A missing legacy `.env` is acceptable for a new PostgreSQL volume: credentials are generated once and persisted. If the data volume already contains a PostgreSQL marker and neither complete legacy credentials nor persisted config exists, initialization fails before it writes a new state file. If imported DB credential values later differ from persisted values, initialization rejects the change and leaves persisted state unchanged.
- URI credentials use percent encoding. `postgres.env` values use `shlex.quote` and identifiers are allowlisted before writing. Fixture coverage exercised a single quote and a literal shell-substitution payload; the sourced result remained the exact literal password.
- Runtime/API secret separation is confirmed from resolved Compose config: API mounts only `runtime_secrets` plus artifacts and read-only gateway source files; it has no migration secret mount or `MIGRATION_DATABASE_URL`. API settings read `app.json`, which the fixture test confirms has no migration URL and an app DB role distinct from the migration admin. The migration service alone mounts `database_secrets` and reads `migration.json`; PostgreSQL consumes only its generated `postgres.env`.
- `APP_CONFIG_FILE` parsing rejects unknown fields and masks underlying parse/config exceptions. Explicit Compose environment fields can override JSON settings, but the API service does not receive admin credentials. The reviewed Docker Compose path does not fall back to the host `.env` through the Settings loader.
- The isolated runner uses a temporary project name and fresh named volumes, replaces service environment values with synthetic values before writing its temporary Compose config, removes the worker, and cleans only that project. The reviewer did not execute it because root was running it separately.

## Checks and limits

- Fixture/regression suite: **17 passed** (`test_compose_initialize.py`, `test_docker_gateway.py`).
- `docker compose config --quiet`: PASS.
- Resolved Compose assertions: PASS for API/migration/bootstrap mounts and config paths.
- No production DB reads or writes, migrations, restarts, gateway calls, inference, or Owner acceptance were performed by this reviewer. Root's isolated runtime result is outside this report and should be recorded separately when available.
