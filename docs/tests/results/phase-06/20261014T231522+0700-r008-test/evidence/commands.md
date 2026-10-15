# R008 — Lệnh và kết quả

Tester `/root/phase06_independent_review`; bắt đầu `2026-10-14T23:15:22+07:00` (Asia/Ho_Chi_Minh), Windows PowerShell. Chỉ chạy test fixtures, build và HTTP GET. Không login automation, không đọc/ghi Owner secret, không tạo grant trên runtime DB, không gọi inference, không migration/seed/reset/runtime DB writes.

1. `rtk proxy uv run --project apps/api --no-sync pytest apps/api/tests/test_owner_auth.py apps/api/tests/test_phase06_runtime.py apps/api/tests/test_cg01_demo_mode.py apps/api/tests/test_codex_gateway.py -q -rs`
   - Exit `0`: **67 passed, 9 skipped, 1 warning** in `1.81s`.
   - Windows private ACL case trong `test_owner_auth.py` được thực thi; POSIX-only permission/symlink cases skip trên Windows. Bảy POSIX gate fixtures trong `test_phase06_runtime.py` cũng skip.
   - Tests dùng Owner/test fixtures và fake transports; không kết nối DB runtime hoặc gửi request model.
2. `rtk proxy uv run --project apps/api --no-sync python -X utf8 docs/tests/results/phase-06/20261014T231522+0700-r008-test/evidence/grant-api-fixture.py`
   - Exit `0`: anonymous grant request `401` trước service; Owner dependency fixture gửi body hợp lệ và route trả `201`; giới hạn request/concurrency/timeout và không retry được chuyển đúng; bounds ngoài schema trả `422` trước service.
   - Service persistence được thay bằng fake trong fixture; không DB write. API schema tổng quát chấp nhận `max_requeues` 0–2; UI remake hiện gửi cố định `0`.
   - Lần chạy ban đầu của fixture có kỳ vọng sai rằng `max_requeues=1` sẽ bị reject. Source schema cho phép tối đa 2; fixture được sửa để kiểm cận ngoài `3` bị reject rồi chạy lại thành công. Đây là sửa test harness, không sửa product source.
3. `rtk proxy uv run --project apps/api --no-sync python -X utf8 docs/tests/results/phase-06/20261014T231522+0700-r008-test/evidence/windows-bootstrap-fixture.py`
   - Exit `0`: tạo Owner path trong TemporaryDirectory; protected ACL của thư mục và file xác minh đúng. Không đọc bytes của secret; thư mục tạm tự dọn.
4. `rtk proxy npm run --prefix apps/web build`
   - Exit `0`; `tsc -b`, Vite build thành công; 19 modules transformed. Build không thay thế browser UI QA.
5. Read-only `curl.exe`:
   - `GET http://127.0.0.1:15501/api/v1/health/ready` → `200`, database `ok`.
   - `GET http://127.0.0.1:15501/api/v1/runtime/status` → `401`, cần Owner login thủ công.
   - `GET http://127.0.0.1:15600/health` → `200`, `active_requests=0`.
6. Không chạy `test_phase06_runtime_persistence.py`: các bài test bật `PHASE_RUNTIME_TEST_ISOLATED=1` sẽ ghi fixture rows vào database đã cấu hình. Chưa có disposable DB riêng được xác minh cho lượt này, nên không bật opt-in.

