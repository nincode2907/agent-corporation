# Commands and environment

Executed through `/Users/buivannin/.local/bin/rtk proxy`. No inference, grant, gateway call, app runtime or migration was started by tester.

- Focused API tests: `uv run --project apps/api pytest apps/api/tests/test_phase10_approvals.py apps/api/tests/test_phase06_runtime.py apps/api/tests/test_phase07_feed.py apps/api/tests/test_phase09_work_orders.py apps/api/tests/test_owner_auth.py` — exit 0; 71 passed, one Starlette/httpx deprecation warning.
- `npm run --prefix apps/web lint` — exit 0.
- `npm run --prefix apps/web build` — exit 0; production Vite build completed.
- Phase08 cursor probe — HTTP 400, `Cursor query và Last-Event-ID không khớp.`; mismatch rejected before DB access.
- Phase10 disposable PostgreSQL `ac-phase10-pg-20261014`, database `agent_corporation_test`: read-only metadata; PostgreSQL 18.6, Alembic 0008; all approval tables have FORCE RLS and scoped policies, app role is non-superuser/no BYPASSRLS. See [database observations](database-schema-rls.txt). No rows mutated. Password/DSN omitted.
- Parent reported full API suite 102 passed/10 skipped; not independently rerun and not counted here.
