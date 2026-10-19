# Lệnh và môi trường — Phase 08 r005

Môi trường/commands dùng chung với Phase 07 r006: [bằng chứng commands](../../../../phase-07/20261018T221600+0700-r006-test/evidence/commands.md).

## Kiểm tra riêng Phase 08

- UI Lens `0.1.0`: `rtk proxy npm run capture -- agent-corporation --preset product-review` → 18/18 screen/viewport success. Final capture: [`artifacts/ui-review/2026-10-18T15-28-04-437Z_c80b5d46-9af9-4eb2-8155-e3d97c33cd0d`](../../../../../artifacts/ui-review/2026-10-18T15-28-04-437Z_c80b5d46-9af9-4eb2-8155-e3d97c33cd0d/manifest.json).
- Authenticated browser: Chromium `156.0.8078.4`, app `http://127.0.0.1:15500`; 9 screens × desktop 1440×900/mobile 390×844; Owner auth success, product logout success, page overflow false 18/18. Manifest and screenshots: [authenticated evidence](../../../../../reviews/stabilization-01/evidence/authenticated/manifest.json).
- Request monitor summary: owner login/logout are the only POSTs; all screen/view/replay requests were GET. No gateway/model/tool endpoint was requested.
- `rtk proxy npm run --prefix apps/web build` → exit 0 after responsive fixes.
- `rtk proxy uv run --project apps/api python scripts/test_playground_isolated.py` → 143 passed, 11 skipped, 1 warning; disposable PostgreSQL DB/role removed by runner.

## Scope limits

- Authenticated Inspector reads saved Phase 06 run `100bc3c8…`; it does not establish Phase 08 live-run acceptance.
- Replay was opened/captured only. We did not seek/reload the timeline or capture a database before/after snapshot; P08-03 stays blocked.
- No separate company/environment actor was created; P08-04 stays blocked.
- IG08 needs its own acceptance evidence and, if needed, explicit Phase08 grant. No grant or inference was used here.
