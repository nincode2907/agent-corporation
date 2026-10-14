# C06 / C08 — Validation

Renderer exit0:24 phase,1 hoàn tất; Phase05 giữ Chờ nghiệm thu. Lần validator đầu phát hiện file validation.md chưa tạo, đã bổ sung file này trước chạy lại. Không phải lỗi sản phẩm.

Lần validator tiếp phát hiện bảng thống kê thiếu khoảng trắng đúng format parser; đã sửa format, không đổi kết quả cases. Final:

```text
PASS cấu trúc:24 checklist,171 test riêng,C01–C08,AC/source refs/hash,IG/R và local links.
PASS HTML:deterministic/đồng bộ,đủ phase,lang=vi/favicon,IDs/links.
PASS report phase-05/20261014T144929+0700-r004-test/report.md:15 cases có fields/tag/result/evidence links.
LIMIT:1 report phase;validator chỉ cấu trúc,không đánh giá nội dung evidence hoặc nghiệm thu.
```

Source manifest chốt trước source remake. Không cập nhật hash report cũ sau remake.
