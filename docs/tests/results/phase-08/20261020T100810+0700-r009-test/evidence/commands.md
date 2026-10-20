# Phase 08 r009 — Lệnh và kết quả

Batch bắt đầu lúc 2026-10-20 10:08:10 ICT trong browser regression; machine date format trong JSON là UTC.

| Lệnh | Exit | Kết quả / giới hạn |
|---|---:|---|
| `rtk uv run --project apps/api python scripts/test_integration05_stack.py --worker-script scripts/ui_fix07_fake_worker.py` | 0 | Disposable Compose/DB/volume dựng riêng; CG01 override false; fake gate/transport chỉ mount vào stack kiểm định. |
| `rtk node docs/reviews/ui-fix-07/evidence/ui-regression.mjs` | 0 | 29 assertions pass; synthetic only; 1 fake dispatch cho waiting/completed Run và 1 fake dispatch cho unknown Run. Trong `finally`, browser harness gọi `rtk proxy docker compose ... down --volumes --remove-orphans` trên project riêng; Compose project/volume và control file đã xóa (`cleanup: true`). |
| `rtk npm run --prefix apps/web build` | 0 | `tsc -b && vite build`; production build pass. |
| `rtk uv run --project apps/api pytest apps/api/tests` | 0 | 217 passed, 38 skipped, 1 Starlette deprecation warning, 4.76s. Các skipped cần database/điều kiện persistence riêng. |
| `rtk git diff --check` | 0 | Không có whitespace error trong diff. |
| `rtk proxy python3 scripts/render_plan.py` | 0 | Đồng bộ HTML từ Markdown; 24 phase, 1 hoàn tất; Phase 08 vẫn Bị chặn. |

Browser assertions gồm roster 3 employee/0 Run; department/version/profile; Runtime deep link và stale link; no-grant/CG01 deny; fake waiting/completed/history; same Run ID Inspector/Replay; old-version isolation; unknown recovery/reconciliation; SSE disconnect; no duplicate dispatch; 1440×900/390×844 overflow; keyboard focus; page errors. Exact outcomes nằm trong [ui-regression.json](../../../../../reviews/ui-fix-07/evidence/ui-regression.json).

Post-run audit recomputed all source-manifest hashes and matched them; all 29 assertions are true, `cleanup` is true, and TCP port 15502 is no longer listening after teardown.

Console: expected HTTP 401 trước login, HTTP 409 của no-grant negative POST và `net::ERR_FAILED` do abort SSE có chủ ý. `pageErrors` rỗng. Không ghi cookie, Owner canary, native auth hay secret vào artifact.

