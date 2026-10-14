# Lệnh kiểm định đã chạy

- `/Users/buivannin/.local/bin/rtk proxy uv run --project apps/api pytest apps/api/tests/test_phase06_runtime.py apps/api/tests/test_phase07_feed.py apps/api/tests/test_phase09_work_orders.py apps/api/tests/test_owner_auth.py` — exit 0; 61 passed, 1 deprecation warning. Các file này dùng fake/unit/TestClient; không bật opt-in PostgreSQL fixtures.
- `/Users/buivannin/.local/bin/rtk proxy npm run --prefix apps/web lint` — exit 0.
- `/Users/buivannin/.local/bin/rtk proxy npm run --prefix apps/web build` — exit 0 (TypeScript + Vite 8.3.3).
- `/Users/buivannin/.local/bin/rtk proxy python3 scripts/validate_phase00.py` — exit 0; Markdown/spec/ADR/document output validation passed, không kiểm định product runtime.
- `/Users/buivannin/.local/bin/rtk proxy git diff --check` — exit 0.
- `/Users/buivannin/.local/bin/rtk proxy env PYTHONPATH=apps/api/src uv run --project apps/api python docs/tests/results/phase-07/20261014T161904+0700-r004-test/evidence/reconnect_last_event_id.py` — exit 0 as a regression probe; observed route status 400 with `Cursor query và Last-Event-ID không khớp.` (the script asserts the observed failure).

No live inference, gateway POST, DB migration, DB write, shared runtime restart, grant creation, or browser session was used. PostgreSQL persistence tests import configured database settings and perform INSERT/UPDATE/DELETE cleanup, so they were not run without a confirmed disposable DB.
