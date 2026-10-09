# Quan sát browser — Phase 01 r005

## Stack demo sạch, DB sẵn sàng

Chrome mở `http://127.0.0.1:56118/#settings` từ bản sao web/API riêng. Accessibility tree ghi tiêu đề `Agent Corporation · Cấu hình & sức khỏe`, demo `Demo Corporation · fixture`, inference grant `Chưa được cấp`; API và PostgreSQL đều “Đang hoạt động”. Fixture được khởi tạo tường minh chỉ trong DB thử nghiệm.

## DB thử nghiệm dừng

Sau khi dừng container `ac-p01-r005-db` và reload cùng tab: API nội bộ “Đang hoạt động”, PostgreSQL “Chưa kết nối”; status message là “API có phản hồi nhưng readiness chưa đạt.”. Banner môi trường demo nêu “Không đọc được demo” và trang cài đặt giữ lỗi rõ ràng. Browser không bấm gateway probe hay reset; các request tự động là GET health/dashboard.

## Hostname local hiện hành

Chrome mở `http://agent-corporation.localhost/#settings`; accessibility tree hiển thị đúng trang Cấu hình & sức khỏe, API/DB hoạt động và inference grant 0. Đây là GET-only kiểm tra runtime hiện có; runtime dùng chung không bị thay đổi.

