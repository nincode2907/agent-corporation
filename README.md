# Agent Corporation

Kế hoạch xây nền tảng quản trị tập đoàn AI, sử dụng HTTP gateway `codex-server` local đang có tại `127.0.0.1:4000`. Chưa triển khai sản phẩm.

- [Mở trang theo dõi phase](docs/master-plan.html)
- [Kế hoạch và nguồn trạng thái chính thức](docs/master-plan.md)
- [Hướng dẫn cho agent](AGENTS.md)

Mở `docs/master-plan.html` trực tiếp bằng trình duyệt, không cần server. Chọn phase, xem phần mới và nghiệm thu, rồi dùng nút sao chép yêu cầu để giao Codex triển khai. Ghi chú cá nhân lưu riêng trong trình duyệt và có thể xuất JSON; không tự sửa file kế hoạch.

Đồng bộ HTML sau khi sửa kế hoạch: `rtk proxy python3 scripts/render_plan.py` (chạy ở root, cần Python 3; không cài dependency).
