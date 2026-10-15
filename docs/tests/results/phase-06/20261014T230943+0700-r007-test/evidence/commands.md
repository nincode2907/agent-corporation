# r007 — Lệnh và kết quả

AI kiểm định độc lập `/root/phase06_independent_review`; bắt đầu `2026-10-14T23:09:43+07:00`, Windows PowerShell. Chỉ chạy fixture/unit tests, read-only HTTP checks và web production build. Không login automation, không đọc `.env`/secret, không tạo grant, không gọi inference, không chạy migration/seed, không bật opt-in PostgreSQL integration fixture và không ghi DB.

1. `rtk proxy uv run --project apps/api --no-sync pytest apps/api/tests/test_owner_auth.py apps/api/tests/test_phase06_runtime.py apps/api/tests/test_phase06_runtime_persistence.py apps/api/tests/test_cg01_demo_mode.py -q`
   - Exit `0`; `54 passed, 19 skipped, 1 warning` in `1.70s`.
   - Bao gồm Owner auth/Windows ACL fixtures, runtime grant/stop/gateway fake transport, CG01 demo-mode fixture; không có inference.
   - `test_phase06_runtime_persistence.py` là opt-in và mặc định skip nếu `PHASE_RUNTIME_TEST_ISOLATED` khác `1`. Không bật biến đó để tránh sửa database. Các case persistence/race thật không được tính pass. Một số strict filesystem proof chỉ chạy POSIX và bị skip trên Windows.
   - Warning: Starlette TestClient cảnh báo dùng `httpx` sẽ deprecated.
2. `rtk proxy npm run --prefix apps/web build`
   - Exit `0`; `tsc -b` và Vite production build thành công, 19 modules transformed.
   - Chỉ kiểm tra compile/build; không chứng minh authenticated UI hoặc interaction.
3. Read-only HTTP checks bằng `rtk proxy curl.exe -sS -i --max-time 3`:
   - `GET http://127.0.0.1:15501/api/v1/health/live` → `200`, service `api`.
   - `GET http://127.0.0.1:15501/api/v1/health/ready` → `200`, database `ok`.
   - `GET http://127.0.0.1:15501/api/v1/demo/dashboard` → `200`, seeded demo dashboard; response được tóm tắt tại [runtime checks](runtime-checks.md), không lưu toàn bộ fixture data.
   - `GET http://127.0.0.1:15501/api/v1/runtime/status` → `401`, cần Owner login; không tự đăng nhập.
   - Gateway `GET /health` và `GET /v1/models` tại `127.0.0.1:15600` → `200`. Models catalog không xác nhận entitlement; không gửi `POST`.
4. Không chạy `PHASE_RUNTIME_TEST_ISOLATED=1`; test persistence trong report này chưa xác minh trên database. Database health/dashboard checks chỉ đọc trạng thái đã được thiết lập trước batch này.

