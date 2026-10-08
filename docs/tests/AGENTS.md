# Hướng dẫn trong docs/tests

- Rule kiểm định chuẩn ở [RULES.md](RULES.md); điểm vào và lệnh ở [README.md](README.md).
- Chỉ đọc checklist của phase được giao trong `phases/`; đọc dependency/evidence khi cần, không nạp cả 24 phase vào mỗi lượt.
- Sau triển khai phase, dùng rule và checklist để kiểm định rồi ghi `results/phase-NN/<test_batch_id>/report.md`. Chỉ việc tạo/sửa bộ tài liệu không kích hoạt test sản phẩm hoặc inference.
- Mọi test trong báo cáo có đúng một tag `clean`, `need-change`, `suggestion` và kết quả thực thi riêng. Không gán tag trước khi kiểm định, không ghi đè lịch sử batch.
- Giữ roadmap/spec là nguồn chuẩn; không tự nghiệm thu, đổi phase hoặc dùng checklist để cấp quyền vượt AGENTS.md root.
