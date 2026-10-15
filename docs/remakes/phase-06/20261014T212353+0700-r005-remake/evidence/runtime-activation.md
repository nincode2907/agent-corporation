# Kích hoạt local ngoại lệ CG01 — parent observation

- Người thực hiện: `/root`, theo chỉ thị mở tạm gateway để test của Chủ tịch; đây là evidence thao tác parent, không tự khai independent test.
- Thời điểm xác minh: 14/10/2026 khoảng 21:22–21:26 +07:00. Không in/read secret để làm evidence; chỉ kết quả metadata/liveness.
- `rtk proxy python -X utf8 scripts/cg01_mode.py demo-test`: exit 0; bật `RUNTIME_CG01_DEMO_TEST_OVERRIDE=true` trong `.env` local, không tạo grant/proof.
- Settings thực + runtime_gate(DEMO_SCOPE): assert allowed true, mode demo-test, verified false pass; stdout chỉ metadata không secret.
- API cũ PID7772 identity khớp command reference workspace và app module, listener127.0.0.1:15501. Guard đầu expected venv exe không khớp nên từ chối stop; identity thực executable Python314 cùng project reference được xác minh trước lần stop sau.
- Đã dừng đúng API PID7772, khởi động bằng `rtk proxy uv run --project apps/api --no-sync uvicorn agent_corporation_api.main:app --app-dir apps/api/src --host 127.0.0.1 --port 15501`, terminal PTY session8745 giữ log. API mới PID28836 báo application startup complete.
- GET web15500 HTTP200, API health/live HTTP200 sau restart. GET API health/ready HTTP503 (database chưa ready); GET gateway15600/health unavailable. Không đọc response secrets hay sửa DB/gateway để thay điều kiện.
- Worker chưa chạy, model requests không gửi, không grant mới. Authenticated runtime/UI Windows vẫn chưa được xác minh và Owner secret code POSIX là dependency riêng; không bỏ Owner/CSRF để test.
- Release-check với flag bật phải BLOCKED/exit1; trước Phase23 bắt buộc strict, stop/restart worker, proof thật và release-check exit0.
