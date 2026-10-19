# Lệnh và môi trường — Phase 07 r007

- Local runtime: Vite `127.0.0.1:15500`, API `127.0.0.1:15501`, PostgreSQL `127.0.0.1:15510`; Chromium `156.0.8078.4`; Windows; timezone Asia/Ho_Chi_Minh.
- Shell lệnh theo quy tắc repo: tiền tố `rtk proxy`.
- Isolated suite: `rtk proxy uv run --project apps/api python -X utf8 scripts/test_playground_isolated.py` — exit 0; **145 passed, 11 skipped, 1 warning**; disposable PostgreSQL DB/role được runner dọn.
- Targeted case nằm trong suite: `apps/api/tests/test_stabilization02_observability.py` — commit/SSE `event_id` + `stream_seq`; rollback absent in DB/page/SSE; Owner feed scope isolation; signed cursor valid/tampered/expired/cross-scope; retention gap/no cursor returns 409.
- Browser audit: `rtk proxy node docs/reviews/stabilization-02/evidence/authenticated_review.mjs` — exit 0; Owner login/logout ok; 21 screenshots; no page errors; 18 screen/viewport captures + 3 state captures; no grant/run/message/approval/profile change.
- Packaging: `rtk proxy uv run --project apps/api python -X utf8 docs/reviews/stabilization-02/evidence/package_authenticated_review.py` — exit 0; 18 screens packaged; 21 total screenshots.
- DB snapshot before/after: `rtk proxy uv run --project apps/api python -X utf8 docs/reviews/stabilization-02/evidence/read_only_db_snapshot.py docs/reviews/stabilization-02/evidence/replay-db-before.json` and same with `replay-db-after.json`; read-only transaction; 13 tables; no row count/fingerprint differences.
- Warning: Starlette TestClient currently uses deprecated httpx integration and recommends `httpx2`; unrelated to assertion results.
- Historical harness attempts before fixes did not pass and are excluded from pass count: initial event fixture/parser assertion defects; browser selector/cleanup/route/offline reset defects. Corrected test-only harness, then successful runs above. No runtime DB mutation was made by those failures.
- No inference/model/gateway request; no grant; no worker dispatch; no CG01 configuration change. Browser POSTs were Owner login/logout only. Read-only DB snapshot excludes session rows because login/logout naturally creates/revokes them.
