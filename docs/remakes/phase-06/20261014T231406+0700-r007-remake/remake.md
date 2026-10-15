# Remake Phase 06 — 20261014T231406+0700-r007-remake

- Phase: 06; Vòng: r007; AI remake: `/root`.
- Bắt đầu: 2026-10-14T23:14:06+07:00, Asia/Saigon.
- Report nguồn: [r007](../../../tests/results/phase-06/20261014T230943+0700-r007-test/report.md).
- Phạm vi: khắc phục phần chuẩn bị Windows Owner và thiếu luồng cấp grant trên UI; không gọi inference, không sửa gateway chung, không đổi trạng thái phase.
- Hạn mức đã được Chủ tịch chọn: một request, timeout tối đa 120 giây; profile/model do Chủ tịch chọn trong UI, tools tắt.

## Thay đổi

- Bổ sung `apps/api/src/agent_corporation_api/modules/governance/windows_acl.py`; auth và `scripts/bootstrap_owner.py` xác minh protected Windows DACL thay cho POSIX-only checks. Test ACL Windows và UTF-8 console đã nằm trong implementation hiện tại.
- Runtime UI có nút cấp grant tường minh sau khi profile đang hiển thị đã được lưu. Grant cố định Phase 06, một request, concurrency 1, timeout 120 giây, không retry, tools tắt, hết hạn sau 15 phút; gắn batch/purpose test riêng và chỉ tạo một grant cho batch UI đó. Cấp grant ghi audit, không dispatch model.
- Gửi run vẫn là hành động riêng và chỉ bật khi CG01 cho phép, grant còn hiệu lực, model/profile đã chọn và có văn bản đầu vào.
- Cập nhật README và nhật ký master plan để phản ánh Windows DACL, tình trạng runtime hiện tại và các blocker còn mở.

## Bằng chứng và giới hạn

- R007 cho biết Owner login/profile/grant chưa sẵn sàng trong UI; đây là lý do thêm luồng cấp grant, không phải quyền tự chạy inference.
- Chưa đăng nhập UI, chưa tạo grant trên runtime DB và chưa gọi model. Không chứng minh inference isolation; CG01 demo vẫn `verified=false`.
- Chờ agent kiểm định độc lập r008 xác minh source/build/API permission paths và cập nhật kết quả riêng. Phase 06 vẫn Bị chặn cho tới khi có evidence live phù hợp và Chủ tịch nghiệm thu.
