# Quan sát runtime r007

- Thời điểm: `2026-10-14T23:09:43+07:00` (Asia/Ho_Chi_Minh).
- API liveness: HTTP `200`.
- API readiness: HTTP `200`; `checks.database=ok`.
- Demo dashboard: HTTP `200`; seed `agent-corporation-phase-04-v1`, dữ liệu gắn nhãn fixture, 3 employees, 5 tasks, 20 events; `inference_requests=0`; usage/cost hiển thị unknown. Chỉ đọc endpoint; không reset/reseed.
- Runtime status: HTTP `401` với “Cần đăng nhập Chủ tịch.” Không tự đăng nhập, không đọc secret/cookie.
- Codex server: `/health` HTTP `200`, provider `codex`, `active_requests=0`; `/v1/models` HTTP `200`. Catalog không chứng minh model entitlement hoặc account usage.
- Web build: thành công; build không tương đương kiểm tra UI đã xác thực.
- Không có run mới, grant mới hoặc request inference được tạo trong batch.

Chủ tịch đã nói rõ có thể bỏ proof CG01 để chạy thử demo. Batch này ghi nhận ngoại lệ đó; **P06-02 vẫn blocked**, vì waiver chỉ cho phép test demo, không tạo bằng chứng isolation/privacy/cancellation và không xác minh CG01.

