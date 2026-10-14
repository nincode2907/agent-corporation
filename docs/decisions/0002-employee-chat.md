# ADR-0002 — Employee Chat riêng trong V1

> Trạng thái: Chủ tịch đồng ý kiến trúc tổng thể ngày 14/10/2026; thiết kế chi tiết đang chỉnh sau review, chưa chốt/triển khai/nghiệm thu. Không cấp inference hoặc grant; CG01 vẫn BLOCKED.

## Bối cảnh

Baseline ADR-0001 ưu tiên Work Order và execution trace; chưa có hợp đồng trò chuyện trực tiếp một-một giữa Chủ tịch và nhân viên. Dùng task giả cho chat sẽ làm sai lifetime cost, approval semantics và riêng tư. Gateway session không thể là nguồn bền vững của lịch sử app.

## Quyết định thiết kế đề xuất

Thêm S15 Employee Chat ở V1, truy cập từ employee profile/org chart/Agent Inspector. Conversation thuộc environment/company/employee và Owner, pin approved employee/model/context/policy versions. Dùng app-owned history và stateless HTTP; text-only, không tools/config mutations; mọi turn đi qua CG01, grant dành cho chat, reservation/budget và Emergency Stop.

Thêm conversation/message/turn và cost subject chat bằng migration có RLS/FK/idempotency, không tạo task/run giả. Context và transcript riêng không được tự đưa sang memory, nhân viên khác hoặc báo cáo. Chỉ Owner-selected excerpts được chuyển qua review thành draft Work Order/proposal; submit/approval là bước riêng.

## Điều chỉnh sau review Chủ tịch

Chat-first với Inspector đóng mặc định; context/policy/provenance nằm sau disclosure. Usage/cost drilldown từ conversation và message về unique call/nguồn, không phân bổ giả cho từng tin. Owner review trước khi tạo bất kỳ draft/task; submit/approval vẫn riêng. [TDG-CG01](../designs/cg01-technical-decision.md) OPEN phải chốt target trước inference06 và chat backend13; không chờ Phase23 và không tự bỏ gate.

## Hệ quả và giới hạn

- Privacy tại app không có nghĩa gateway/provider không lưu prompt; CG01 phải xác minh riêng read boundaries/persistence/retention/cancel.
- Phải mở rộng event/model-call subject và ledger, không thể chỉ thêm chat textarea vào UI hiện có.
- Phiên bản mới/ACL bị thu hồi cần Owner xem xét nhánh mới; resume không phụ thuộc memory gateway và không tự gửi lại unknown call.
- Chi phí chat thuộc period operating cost và drilldown conversation; không nhập hồi tố vào accepted-task KPI.
- Foundation triển khai ở Phase 13; context ở 15, finance ở 16, stop ở 19; IGCHAT sau 19 trước 20 mới kiểm tích hợp live. Không tạo dependency ngược 13 → 19 hoặc mở send khi chưa đủ gates.
- Windows cần trusted proof/ACL tương đương trước inference, ngoài phạm vi sửa code lần này.

## Tài liệu và kiểm chứng

[Thiết kế + EC01–EC12](../designs/employee-chat.md), [đặc tả 1.2](../product-spec.md), [master plan](../master-plan.md), [CG01 verification](../reviews/cg01-20261014/report.md). Tất cả kiểm thử chat sản phẩm chưa chạy. Baseline ADR-0001 và lịch sử nghiệm thu Phase 00 giữ nguyên; bản này không ghi giả một quyết định đã được nghiệm thu.
