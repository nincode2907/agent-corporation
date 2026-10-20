# Integration Fix 05.1 — Kế hoạch demo model thật (chưa chạy)

## Candidate đã kiểm tra

- `GET http://127.0.0.1:15600/v1/models` ngày 20/10/2026 trả `gpt-6-luna` trong catalog gateway.
- `GET http://127.0.0.1:15600/api/models` trả `gpt-6-luna`, `chat_supported=true`, reasoning có `medium`; snapshot này ghi `checked_on=2026-10-02`, nên không phải kiểm tra capability mới trong ngày.
- Gateway schema hiện nhận reasoning effort `medium` và `gpt-6-luna` là model configured/catalog item. Catalog/model list không chứng minh entitlement của tài khoản. Không có call thử.
- Gateway health trả `active_requests=0`, `queued_requests=0` tại thời điểm preflight. Health không xác nhận login/model entitlement.

## Thiết lập đề xuất

| Thuộc tính | Giá trị dự kiến |
|---|---|
| Environment | Demo cô lập, có Owner/config riêng nếu deployment dùng chung chưa được duyệt |
| Employee | Một employee demo đã được Owner chọn, EmployeeVersion hiện hành |
| Model / effort | `gpt-6-luna` / `medium` |
| Request | Một tin nhắn text-only, fixture tin cậy, không nhạy cảm |
| Concurrency / timeout | 1 / 120 giây |
| Grant | Một request, hết hạn 15 phút sau khi Owner tạo, đúng phase/batch/purpose/model/effort |
| Tools / fallback / retries | Tắt |
| Mục đích | Runtime Run → Events → Live Office → Inspector → Replay |

Chỉ Owner tạo grant sau khi duyệt deploy, môi trường, CG01 và nội dung fixture. Tài liệu này không tạo grant và UI không được mở quyền khi chưa có quyết định.

## CG01 và quyết định Owner còn thiếu

CG01 strict của shared container hiện không pass (`missing_or_invalid_proof`; `verified=false`). Ngoại lệ demo đã được ghi nhận cho test local ngày 14/10 không được tự mở rộng thành grant hoặc lần gọi model mới; cần Owner phê duyệt rõ scope/batch nếu muốn dùng ngoại lệ demo riêng. Không đổi policy/config trong batch này. Nếu Owner không phê duyệt ngoại lệ và strict proof vẫn thiếu, demo bị chặn.

Trước khi chạy, cần deploy Fix 05.1 theo thủ tục preflight, đúng một worker active, quyết định của Owner về môi trường cô lập/ngoại lệ CG01, grant tường minh và text fixture. Hệ thống cần không có unknown guard còn chiếm capacity trong chính environment đó. Run cũ không được replay. Nếu call phát sinh unknown, dừng lượt tiếp theo và giữ guard; thu thập gateway evidence hoặc chuyển sang runtime cô lập riêng.

**Trạng thái:** chuẩn bị xong ở mức cấu hình/flow; chưa được authorize, chưa deploy, chưa có grant, chưa gọi model.
