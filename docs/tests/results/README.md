# Nơi lưu các đợt kiểm định

Mỗi lần kiểm định một phase tạo `phase-NN/<timestamp>-rNNN-test/report.md` và `evidence/` theo [rule](../RULES.md). Không ghi đè batch cũ. Dùng [mẫu report](../templates/report.md), giữ đủ C01–C08 và PNN-*; mọi test có tag/kết quả/evidence riêng.

Report còn need-change giải quyết được → tạo remake cùng số vòng trong [docs/remakes](../../remakes/README.md) → retest với số vòng kế tiếp vào results mới. Report retest có `Supersedes` và `Remake nguồn`. Không đổi tag report cũ khi sửa code.

Mỗi phase có `README.md` làm sổ vòng; chỉ link artifact đã tồn tại:

| Vòng | Report test | Kết luận | Remake | Report retest | Trạng thái vòng |
| --- | --- | --- | --- | --- | --- |
| r001 | Đường dẫn report đã lưu | Kết luận report nguồn | Chưa tạo hoặc link remake | Chưa tạo hoặc link r002 | needs-remake / needs-retest / blocked / done |

`done` khi report đạt kỹ thuật, hoặc retest đã chứng minh toàn bộ findings vòng này được xử lý; không có nghĩa phase đã được Chủ tịch nghiệm thu. Nếu retest còn finding mới/khác, tiếp tục dòng vòng kế tiếp. Báo cáo trước flow có tên timestamp-purpose giữ nguyên như legacy; không đổi tên để ép theo naming mới.

Thư mục `framework/` chỉ chứa kiểm tra chất lượng **bộ tài liệu kiểm định**, không là kết quả test sản phẩm hoặc nghiệm thu Phase 00–23. Các phase chỉ có report khi được giao và đã kiểm định; không tạo report pass cho phase chưa chạy.

Report/evidence đã lọc là nguồn kiểm định. `docs/evidence/` tiếp tục giữ evidence bàn giao phase; trạng thái chính thức vẫn ở `docs/master-plan.md`.
