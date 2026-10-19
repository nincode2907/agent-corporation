# Lệnh và môi trường — Phase 08 r006

- Local UI/API/PostgreSQL: `127.0.0.1:15500`, `127.0.0.1:15501`, `127.0.0.1:15510`; Chromium `156.0.8078.4`; Windows; Asia/Ho_Chi_Minh.
- API suite: `rtk proxy uv run --project apps/api python -X utf8 scripts/test_playground_isolated.py` — exit 0; **145 passed, 11 skipped, 1 warning**; disposable DB/role removed by runner.
- Browser: `rtk proxy node docs/reviews/stabilization-02/evidence/authenticated_review.mjs` — exit 0; 9 screens × 2 viewports + cursor-gap/offline/stale; Owner logout succeeded; no page error.
- Replay DB snapshots: `rtk proxy uv run --project apps/api python -X utf8 docs/reviews/stabilization-02/evidence/read_only_db_snapshot.py docs/reviews/stabilization-02/evidence/replay-db-before.json` then repeat with `replay-db-after.json`; 13 table counts/fingerprints equal.
- Package: `rtk proxy uv run --project apps/api python -X utf8 docs/reviews/stabilization-02/evidence/package_authenticated_review.py` — exit 0; sanitized ZIP and linked contact sheet created.
- Replay journey: 2 event GETs; slider present; reload recovery true; `businessWrites=[]`. Whole session POST list contains login/logout only. No gateway/tool/model request.
- Warning: Starlette TestClient/httpx deprecation; not a failed assertion.
- No inference, grant, worker dispatch, approval decision, profile write or run creation. Login/logout session rows are intentionally excluded from DB snapshot equality; snapshots use read-only transaction.
- Initial evidence harness attempts failed before correction (manifest parser field mismatch and literal newline in manifest; earlier UI test-harness fixes are documented in Sprint02 report). They are not reported as passing tests and did not make application writes.
