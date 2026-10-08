# Kiểm định Phase 14 — Tuyển dụng và thử việc

> Checklist dự kiến, chưa có kết quả test. AI đọc lại nguồn hiện tại trước mỗi batch; không gắn tag sẵn hay tự nghiệm thu.

[Rule](../RULES.md) · [Điểm vào](../README.md) · [Mẫu report](../templates/report.md) · [Roadmap](../../master-plan.md) · [Spec V1](../../product-spec.md) · [ADR](../../decisions/0001-v1-foundation.md)

## Nguồn và ranh giới

- Phase: 14
- Dependency từ roadmap: 13
- Yêu cầu liên quan: REQ06, REQ16
- Gate: Không có gate IG riêng; vẫn kiểm criteria phase và C01–C08
- Contract hash: ad5effb61d09c87639f6e45d43b22872fed6946c29e5dca1b44daa2ff7744d4c

Hash đối chiếu scope/demo/criteria/delivery/limits/evidence/dependency tại thời điểm soạn, không bao gồm status/nhật ký. Nguồn đổi thì cập nhật kế hoạch, không sửa report cũ. Snapshot bên dưới giúp traceability; nguồn hiện tại vẫn ưu tiên.

### Phạm vi phải đọc

- HR proposal: nhu cầu, loại hợp đồng, model/tools, dự toán, probation và tiêu chí giữ lại.
- Approve/reject/offboard; thu hồi quyền và stop/drain các run trước chuyển trạng thái.
- Lưu assessment thử việc; benchmark tự động nâng cấp ở Phase 17, giai đoạn này dùng evidence suite cố định.

### Demo bắt buộc

Đề xuất QA on-demand, từ chối một lần rồi duyệt proposal mới; offboard khi còn task đang chạy.

### Giới hạn phase

Không tự kết luận specialist vô ích vì tháng này idle.

### Evidence bàn giao cần đối chiếu

Proposal audit, probation evidence và offboard test.

## Mapping nghiệm thu → test

Mỗi AC là gạch đầu dòng nghiệm thu roadmap hiện tại khi soạn. Kiểm thêm C01–C08 theo rule; tiêu chí thay đổi cần remap trong report. Mọi case dưới đây bắt buộc trong phạm vi phase; không gọi inference nếu chưa có grant, mà ghi blocked cho case cần run thật.

| Tiêu chí | Kỳ vọng từ roadmap | Test IDs tối thiểu |
| --- | --- | --- |
| AC1 | Agent không tự tuyển/sa thải nhân viên cố định hoặc mở quyền. | P14-01, P14-02 |
| AC2 | Offboard chặn run mới, xử lý run hiện tại và không mất lịch sử. | P14-04, P14-05 |
| AC3 | Đánh giá theo chất lượng/nhu cầu/chi phí biên, không xem token tiêu thụ là năng suất. | P14-03, P14-06 |

## Ca kiểm định riêng của phase

Mỗi dòng là một test phải có record kết quả riêng. Các biến thể negative/race trong dòng ghi sub-results/evidence để không bỏ sót; nếu một biến thể bắt buộc chưa đạt, cả test không clean. C01–C08 cũng phải có record riêng.

| ID | Test | Bước/điều kiện | Kỳ vọng | Evidence cần lưu | Nguồn bổ sung |
| --- | --- | --- | --- | --- | --- |
| P14-01 | HR proposal đủ căn cứ | Tạo proposal có nhu cầu/contract/model/tools/cost basis/probation/criteria | Có sources/evidence, unknown cost có nhãn, không tự thành hire | Proposal manifest/UI | Spec §3/11/13 |
| P14-02 | Owner approve/reject | Agent hire/fire/permanent grant API bypass; Owner reject rồi approve proposal mới | Agent deny; reject không đổi nhân sự/quyền, audit quyết định | Negative tests/audit/DB diff | Spec §10 |
| P14-03 | Probation assessment | Suite cố định pass/fail/unknown; kiểm criteria và assessment refs | Chất lượng/nhu cầu/chi phí biên từ evidence, token không là năng suất | Suite/evaluation outputs | Spec §13 |
| P14-04 | Offboard trong run | Offboard employee test đang queued/running; stop/drain/revoke | Chặn run mới; run hiện tại xử lý theo outcome, không mất history | Lifecycle/receipt/stop timeline | Spec §7/8/10 |
| P14-05 | Offboard race/idempotency | Offboard double-submit đồng thời assignment | Không run mới lọt sau revoke, không duplicate mutation | Race/DB/action counts | Spec §10 |
| P14-06 | Idle và history | Hồ sơ specialist idle, chuyển contract và xem run cũ | Không auto sa thải vì idle, evidence/version vẫn truy được | Source/ảnh/profile/history refs | Spec §7/13 |

## Lệnh và điều kiện chạy

Chưa có command runtime được xác minh cho phase này khi soạn. Khi phase được triển khai, đọc manifest/scripts/test source và README hiện tại, chọn lệnh tồn tại, ghi lệnh/exit code vào report; không tự bịa endpoint, cài tool/global hoặc scaffold để chạy checklist.

## Kết luận và lưu kết quả

Tạo `docs/tests/results/phase-14/<test_batch_id>/report.md` và `evidence/`. Ghi C01–C08 + P14-01…P14-06 + case bổ sung; mỗi test có đúng một tag `clean`, `need-change`, `suggestion`, result, expected/actual và evidence. Thống kê đầy đủ, kết luận kỹ thuật theo rule, quyết định Chủ tịch riêng. Dừng tại Phase 14.
