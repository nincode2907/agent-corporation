# Lệnh và môi trường — Phase 07 r006 / Phase 08 r005

## Môi trường

- OS: Windows native; workspace `F:\Workspace\dev\projects\agent-corporation`.
- Node `v24.21.0`; npm `11.19.0`; Python `3.14.3`; Chromium `156.0.8078.4`.
- UI Lens `0.1.0`, repo local `F:\Workspace\dev\projects\local-tools\ui-lens`.
- Web: React/Vite/TypeScript theo lockfile dự án; API suite chạy cùng lock `uv.lock`.
- Runtime: Vite `http://127.0.0.1:15500`; API `http://127.0.0.1:15501`; PostgreSQL `127.0.0.1:15510`; UI Lens service `127.0.0.1:15900`.
- Readiness đã có trong lượt làm: API `/api/v1/health/ready` trả 200, database `ok`; UI Lens `/api/health` trả 200. Không probe Codex gateway, không gửi inference.
- Tất cả shell command được chạy qua `rtk proxy` theo AGENTS.md.

## Lệnh đã chạy

| Lệnh | Exit/kết quả | Ý nghĩa/giới hạn |
| --- | --- | --- |
| `rtk proxy npm run capture -- agent-corporation --preset product-review` (cwd UI Lens) | 18/18 success; manifest ID `c80b5d46-9af9-4eb2-8155-e3d97c33cd0d` | 9 target × desktop 1440×900 + mobile 390×844; screenshots và diagnostics ở `artifacts/ui-review/2026-10-18T15-28-04-437Z_c80b5d46-9af9-4eb2-8155-e3d97c33cd0d/`. UI Lens báo một số 401 auth probe và hai request abort trong từng capture; xem phần diagnostics. |
| `rtk proxy node -e "…import('file:///F:/Workspace/dev/projects/agent-corporation/docs/reviews/stabilization-01/evidence/browser_audit.mjs')"` (cwd UI Lens; biến đường dẫn local được gán trong process) | exit 0 | Chromium 156; keyboard skip link; 9 màn mobile; document width 390 trên cả 9 màn; nav là vùng cuộn ngang được thiết kế. `evidence/browser-audit-after.json`. |
| `rtk proxy node -e "…import('file:///F:/Workspace/dev/projects/agent-corporation/docs/reviews/stabilization-01/evidence/authenticated_review.mjs')"` (cwd project; script đọc secret cục bộ, không in/lưu) | exit 0; auth ok; logout ok; 18 screenshot states | Đã đọc profile/sessions/runtime/events; không lưu profile, grant, gửi message, tạo run hoặc decision. `POST` duy nhất trong luồng là Owner login/logout. Authenticated screenshots/manifest ở `docs/reviews/stabilization-01/evidence/authenticated/`. Cùng script chặn SSE endpoint để thử reconnect. |
| `rtk proxy uv run --project apps/api python scripts/test_playground_isolated.py` | 143 passed, 11 skipped, 1 warning; exit 0 | Migrate + pytest trên DB/role disposable; runner xác nhận DB/role đã xóa. Test transport là fake; không inference; runtime DB không đổi. Warning: Starlette khuyến nghị `httpx2` thay `httpx` trong TestClient. |
| `rtk proxy npm run --prefix apps/web build` | exit 0 | `tsc -b` và `vite build`, chạy lại sau UI fixes cuối. |

## UI Lens diagnostics

- Tái hiện trước sửa: selector `a[href="#settings"]` match link điều hướng và profile Owner, dẫn Playwright strict-locator failure. Đổi target sang `a.nav-link[href="#settings"]`; áp dụng selector nav cụ thể cho các screen targets. Capture sau sửa 18/18 success.
- Cấu hình cũ chỉ có 4 screens, desktop height 1000 và chưa có mobile cho Organization/Settings. Cấu hình sprint đủ 9 screens × 2 viewport, desktop height 900.
- UI Lens vẫn ghi GET `/api/v1/owner/session` → 401 cho trang auth-gated khi capture anonymous; đây là default-deny/session probe hiện rõ trong source, không phải `pageerror`. `PlaygroundPanel` có hai component độc lập kiểm session nên có thể thấy hai 401 trên một target.
- Diagnostics cũng ghi GET health/dashboard là `net::ERR_ABORTED` trong vòng capture/navigate. Authenticated Playwright audit sau đó hoàn tất các GET health/dashboard/runtime/feed; không có page errors.
- Không xem UI Lens `success` một mình là pass của page flow; authenticated browser manifest và screenshots được dùng riêng.

## Owner browser boundary

- Dùng file secret local đã có sẵn, không tạo credential mới; secret được fill trực tiếp vào field password trong browser context tạm.
- `POST /api/v1/owner/login` tạo session cần thiết để kiểm tra Owner UI; cuối bài gọi `POST /api/v1/owner/logout` và xác nhận login field trở lại.
- Không ghi request body, cookie, CSRF token, secret, event cursor value hay transcript ra log. Manifest chỉ ghi pathname và boolean `hasCursor`/`hasLastEventId`.
- Các screenshot có dữ liệu run lịch sử Phase 06; không có model output mới trong batch.
