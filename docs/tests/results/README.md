# Nơi lưu các đợt kiểm định

Mỗi lần kiểm định một phase tạo `phase-NN/<test_batch_id>/report.md` và `evidence/` theo [rule](../RULES.md). Không ghi đè batch cũ; retest liên kết supersedes. Copy [mẫu báo cáo](../templates/report.md), giữ đủ C01–C08 và PNN-* của phase. Mọi test có tag/kết quả/evidence riêng.

Thư mục `framework/` chỉ chứa kiểm tra chất lượng **bộ tài liệu kiểm định**, không là kết quả test sản phẩm hoặc nghiệm thu Phase 00–23. Các phase chỉ có report khi được giao và đã kiểm định; không tạo report pass cho phase chưa chạy.

Report/evidence đã lọc là nguồn kiểm định. `docs/evidence/` tiếp tục giữ evidence bàn giao phase; trạng thái chính thức vẫn ở `docs/master-plan.md`.
