# Quan sát runtime và UI r008

- Thời điểm: `2026-10-14T23:15:43+07:00`, Windows host.
- API readiness: HTTP `200`, database `ok`.
- `/api/v1/runtime/status`: HTTP `401`, yêu cầu đăng nhập Chủ tịch. Không tạo cookie/session.
- Codex gateway `/health`: HTTP `200`, `active_requests=0`; không gửi POST. Health không xác nhận entitlement.
- Web production build pass. Không mở UI để đăng nhập hoặc thao tác grant.
- Source review: nút grant chỉ khả dụng khi profile có model đã lưu và khớp lựa chọn; grant UI dùng model/effort của profile, một request, concurrency 1, timeout 120s, `max_requeues=0`, expiry 15 phút. UI kiểm tra batch grant đã tồn tại trước khi cấp; thao tác grant tách khỏi nút gửi run.
- Không thể kiểm tra browser authenticated state, actual profile/model selection hoặc grant persistence; **UI live verification blocked**.
- Không có Owner login, runtime grant, run, inference hay DB mutation trong batch.

