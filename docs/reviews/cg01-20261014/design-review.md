# Kiểm định độc lập thiết kế Employee Chat

Ngày 14/10/2026 · Phạm vi: review tài liệu thiết kế/đặc tả/roadmap/ADR, không test sản phẩm, không inference, không tạo proof hoặc grant. Tester là agent khác với agent sửa tài liệu. Báo cáo CG01 riêng: [report.md](report.md).

**Verdict tài liệu: không còn finding giải quyết được chưa xử lý trong phạm vi review.** Hai finding ban đầu đã được agent soạn tài liệu sửa và tester đọc lại xác minh. Đây không phải nghiệm thu sản phẩm: Employee Chat **NOT RUN**, CG01 **BLOCKED**, mọi live qualification/inference chưa được cấp quyền trong task này.

## Finding và vòng xác minh

| ID | Mức độ / tag ban đầu | Finding ban đầu | Sửa và bằng chứng đọc lại | Trạng thái cuối |
| --- | --- | --- | --- | --- |
| EC-DOC-01 | P1 · `need-change` | IGCHAT trước20 đòi EC01–11 trong khi EC11 backup/restore ở22; 22 phụ thuộc21/20 tạo vòng phụ thuộc. | [Thiết kế:137](../../designs/employee-chat.md:137) tách EC01–10 baseline + EC12 live ở IGCHAT; EC11/hardening22 chỉ là điều kiện release23. [Roadmap:1055](../../master-plan.md:1055), [IGCHAT:1293](../../master-plan.md:1293), [spec:501](../../product-spec.md:501) khớp. Dependency metadata [Phase13:773](../../master-plan.md:773) không tham chiếu phase19; [Phase19:1046](../../master-plan.md:1046) chỉ cần phase trước; [Phase20:1092](../../master-plan.md:1092) chờ19+IGCHAT, [Phase22:1180](../../master-plan.md:1180) sau21. Không còn đường22 → IGCHAT. | `clean` — fixed qua review tài liệu |
| EC-DOC-02 | P2 · `need-change` | General send khóa đến IGCHAT PASS nhưng gate cần liveEC12; chưa phân biệt qualification batch với mở dùng thường. | [Thiết kế:116](../../designs/employee-chat.md:116) nêu rõ chỉ isolated Owner-authorized test batch chạy livequalification trướcPASS; mỗi call vẫn cần CG01/grant/budget/stop. General send chỉ mở sauPASS, realusage chờrelease. [Roadmap IGCHAT:1293](../../master-plan.md:1293) đồng bộ. Không exemption, grant hoặc inference được tạo bởi tài liệu này. | `clean` — fixed qua review tài liệu |

## Bao phủ yêu cầu đã đối chiếu

- Ba lối vào profile/org chart/Inspector, mobile/keyboard và trạng thái blocked/unknown có trong thiết kế S15; prototype là tài liệu minh họa, không được mô tả là chat đã chạy.
- Private history đúng environment/company/employee/conversation; không tự đưa transcript vào nhân viên khác/search/memory/reports. Approved profile/model/context/policy pins, ACL/lifecycle recheck và explicit branch khi đổi version được định nghĩa.
- Chat tách Work Order, no tools/config mutations; migration subject chat/RLS/FK/events/grant được ghi là việc tương lai, không giả current runtime task-bound đã tương thích.
- Durable app history/stateless gateway; unknown không tự resend, usage/cost thiếu không thành0; sharedreservation/budget/stop và call trace có nguồn.
- Chọn excerpt → review → draft/proposal → submit/approval riêng; không hiểu lời model/Owner trong chat là permission change hoặc authorization ngầm.
- [ADR-0002](../../decisions/0002-employee-chat.md) là thiết kế đề xuất chưa triển khai/nghiệm thu; spec1.2 giữ lịch sử nghiệm thu baseline1.1. Các doc không tuyên bố CG01 hoặc chat product đã đạt.

Giới hạn: review này kiểm sự đầy đủ và nhất quán thiết kế hiện có bằng đọc source Markdown; không chứng minh runtime, migration, authorization enforcement, privacy hay browser accessibility đã đạt. EC01–EC12 vẫn NOT RUN; CG01 còn thiếu evidence như report riêng. Không có product tests hoặc model calls trong lượt review tài liệu.

## Snapshot tài liệu đã đọc lại

SHA-256 giúp nhận diện phiên bản Markdown của lần kiểm định; không là gateway proof.

| File | SHA-256 |
| --- | --- |
| `docs/designs/employee-chat.md` | `5cc27104953d7399e508e36866faa570266d90765446a058622899ea2b043a89` |
| `docs/product-spec.md` | `45aecbd42d59c330ed138687d09babf18adf5c936991d50136fb4e3d5e04d483` |
| `docs/master-plan.md` | `b7b7abb662eb55b86287bf168a80c096db5ee419e728422322bebe1e37d8eba5` |
| `docs/decisions/0002-employee-chat.md` | `3ac682a4fcd0b7d00b58c744fbbcdd1b3f1c16baebf87f6cfaf82579f72566e4` |
