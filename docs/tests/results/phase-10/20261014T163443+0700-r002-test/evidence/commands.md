# Phase10 r002 commands

All commands used `rtk proxy`; no DSN/password is retained in evidence.

- `uv run --project apps/api pytest apps/api/tests/test_phase10_approvals.py apps/api/tests/test_phase06_runtime.py apps/api/tests/test_phase07_feed.py apps/api/tests/test_phase09_work_orders.py apps/api/tests/test_owner_auth.py` — exit 0, **71 passed**, one Starlette/httpx deprecation warning (independently rerun 2026-10-14).
- Pure evaluator matrix `python3 evidence/permission-matrix.py` — all 12 checks pass: exact approval match allows; action type, task revision, company, environment, payload hash, run, policy mismatch, expired, consumed, default/unknown action deny.
- Prior command results in r001: `npm run --prefix apps/web lint` and `npm run --prefix apps/web build` both passed; see r001 command evidence. No source changes to web surface occurred after that result per source manifest comparison.
- Disposable PG schema/RLS metadata was independently inspected read-only in r001 and is carried forward; no DB row mutations.
- No inference/grant/gateway/executor/app runtime. Parent's 102 passed/10 skipped full-suite report is not tester-run.
