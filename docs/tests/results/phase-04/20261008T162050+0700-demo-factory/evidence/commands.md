# Commands and results

Mọi lệnh shell qua `/Users/buivannin/.local/bin/rtk proxy`.

- Read-only GET `/api/v1/demo/dashboard` trước test: HTTP success; fixed demo env/company; v1; 2 departments, 3 employees, 5 tasks, 20 events; manifest `03e1126c…`; inference_requests=0.
- `uv run --project apps/api pytest apps/api/tests/test_phase03_persistence.py apps/api/tests/test_phase04_demo_factory.py -q` — exit 0; `7 passed, 1 warning in 2.49s` (5 Phase 03 + 2 Phase 04). Warning: Starlette TestClient/httpx deprecation.
- Read-only GET `/api/v1/demo/dashboard` after tests — same manifest `03e1126c…`, same v1 counts, inference_requests=0.
- `uv run --project apps/api alembic -c apps/api/alembic.ini current` — exit 0; `20261008_0003 (head)`; read-only.
- `npm run --prefix apps/web lint` — exit 0; oxlint.
- `npm run --prefix apps/web build` — exit 0; tsc + Vite.
- `python3 docs/tests/scripts/validate.py --batch docs/tests/results/phase-04/20261008T162050+0700-demo-factory` — exit 0; PASS checklist/hash/links và report Phase 04 batch có đủ 16 cases/tag/result/evidence links.

Không chạy API full suite; không đọc `.env`; không chạy migration upgrade/downgrade; không restart DB/API; không probe gateway/model.
