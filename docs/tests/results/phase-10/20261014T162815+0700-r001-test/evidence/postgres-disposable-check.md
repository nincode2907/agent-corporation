# Phase 10 PostgreSQL disposable check

- Test batch: `20261014T162815+0700-r001-test`
- Database: disposable PostgreSQL 18.6 container `ac-phase10-pg-20261014`, database `agent_corporation_test`, Docker published port `127.0.0.1:59996` only.
- Isolation: created for this batch; no connection to the project runtime database, shared gateway, or any company data.
- Migration command: `DATABASE_URL=<disposable DSN> MIGRATION_DATABASE_URL=<disposable DSN> APP_DATABASE_PASSWORD=<disposable value> rtk proxy uv run --project apps/api alembic -c apps/api/alembic.ini upgrade head`.
- Result: all migrations applied through `20261014_0008`; `alembic_version` returned `20261014_0008`.
- Schema checks: `approvals`, `approval_request_receipts`, and `approval_decision_receipts` have both RLS and FORCE RLS enabled. `agent_corporation_app` has SELECT/INSERT on both receipt tables and SELECT/INSERT/UPDATE on approvals.
- No secret or real DSN was stored. The disposable container is retained temporarily while independent lifecycle probes run, then removed.

This verifies migration execution and catalog configuration only. It does not verify API create/decision/consume lifecycle, RLS cross-scope behavior, audit completeness, concurrency, or dispatch safety.
