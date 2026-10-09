# Quan sát browser — Phase 01 r003

Đọc tab Chrome tại `http://agent-corporation.localhost/` qua accessibility tree, không thao tác nút, không nhập dữ liệu.

- Tiêu đề: `Agent Corporation · Tổng quan`.
- UI hiển thị `Demo Corporation · fixture`, `Inference grant Chưa được cấp`, và trạng thái API nội bộ/PostgreSQL readiness đang hoạt động.
- Nội dung demo ghi rõ không tạo agent thật, không gọi model; usage chưa biết và inference 0.
- Tab là môi trường demo local; browser không phát sinh thao tác seed/reset/probe trong đợt kiểm định.

