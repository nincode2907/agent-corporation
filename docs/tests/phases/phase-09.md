# Kiểm định Phase 09 — Bảng nhiệm vụ và hàng đợi

> Checklist dự kiến, chưa có kết quả test. AI đọc lại nguồn hiện tại trước mỗi batch; không gắn tag sẵn hay tự nghiệm thu.

[Rule](../RULES.md) · [Điểm vào](../README.md) · [Mẫu report](../templates/report.md) · [Roadmap](../../master-plan.md) · [Spec V1](../../product-spec.md) · [ADR](../../decisions/0001-v1-foundation.md)

## Nguồn và ranh giới

- Phase: 09
- Dependency từ roadmap: 08
- Yêu cầu liên quan: REQ07
- Gate: Không có gate IG riêng; vẫn kiểm criteria phase và C01–C08
- Contract hash: f930693e3be08dc318c6eae2da6719fe8f2426b0a34e370f40ea815ed14e53d4

Hash đối chiếu scope/demo/criteria/delivery/limits/evidence/dependency tại thời điểm soạn, không bao gồm status/nhật ký. Nguồn đổi thì cập nhật kế hoạch, không sửa report cũ. Snapshot bên dưới giúp traceability; nguồn hiện tại vẫn ưu tiên.

### Phạm vi phải đọc

- Work Order gồm mục tiêu, đầu ra, acceptance, quyền, deadline, budget, điểm dừng và assignee.
- Queue bền vững, ưu tiên, concurrency/lease, states blocked/awaiting approval/quality/rework/accepted.
- Pause ngăn bước mới; abort HTTP request đang chạy khi cần; resume từ checkpoint xác minh, retry có attempt mới và idempotency.

### Demo bắt buộc

Đưa hai task vào queue, pause một task, restart worker, resume rồi retry lỗi an toàn.

### Giới hạn phase

Không áp đặt gọi đủ Architect/QA cho mọi task nhỏ.

### Evidence bàn giao cần đối chiếu

Queue/lease/crash tests và state transition evidence.

## Mapping nghiệm thu → test

Mỗi AC là gạch đầu dòng nghiệm thu roadmap hiện tại khi soạn. Kiểm thêm C01–C08 theo rule; tiêu chí thay đổi cần remap trong report. Mọi case dưới đây bắt buộc trong phạm vi phase; không gọi inference nếu chưa có grant, mà ghi blocked cho case cần run thật.

| Tiêu chí | Kỳ vọng từ roadmap | Test IDs tối thiểu |
| --- | --- | --- |
| AC1 | Hai worker không nhận cùng lease; quá concurrency không tạo run thêm. | P09-02, P09-03 |
| AC2 | UI không hứa resume giữa suy luận/token; trạng thái pause/interrupted/checkpoint thể hiện đúng. | P09-04, P09-05 |
| AC3 | Accepted do nghiệm thu, không suy ra từ turn completed; rework giữ evidence cũ. | P09-06, P09-07 |

## Ca kiểm định riêng của phase

Mỗi dòng là một test phải có record kết quả riêng. Các biến thể negative/race trong dòng ghi sub-results/evidence để không bỏ sót; nếu một biến thể bắt buộc chưa đạt, cả test không clean. C01–C08 cũng phải có record riêng.

| ID | Test | Bước/điều kiện | Kỳ vọng | Evidence cần lưu | Nguồn bổ sung |
| --- | --- | --- | --- | --- | --- |
| P09-01 | WorkOrder validation | Submit thiếu goal/output/criteria/scope/budget/deadline/stop/assignee constraints | Invalid deny trước queue, revision/snapshot đúng | Validation output + DB state | Spec §7 |
| P09-02 | Lease/concurrency race | Hai workers claim một job/step và quá concurrency | Một active lease; không run/dispatch trùng | Parallel test + lease/call counts | Spec §7/8 |
| P09-03 | Durable queue/crash | Queue hai tasks khác priority, restart worker test/expire lease | Không mất job, reconcile trước retry, đúng ordering/caps | Queue/lease before/after | Spec §8 |
| P09-04 | Pause/resume checkpoint | Pause đang queued/waiting, resume sau recheck quyền/budget/approval | Không dispatch mới khi pause, không resume giữa token | State transitions + checkpoint IDs | Spec §8/10 |
| P09-05 | Retry/idempotency | Known safe retry tạo attempt mới; unknown side effect bị chặn | History giữ, receipt/outcome check; failed terminal task tạo retry task mới | Attempt/task lineage và receipts | Spec §8 |
| P09-06 | Review/rework/acceptance | Model completed → review → rework → Owner acceptance, thử agent accepted | Completed khác accepted; agent không tự accepted, evidence cũ giữ | State/actor/evaluation logs | Spec §8/10 |
| P09-07 | Task board filters/actions | Tạo/giao/lọc/blocked/cancel trong UI test không inference | Đúng blocker/assignee/history; hủy chặn bước mới | Ảnh + API state comparison | Spec §3/8 |

## Lệnh và điều kiện chạy

Chưa có command runtime được xác minh cho phase này khi soạn. Khi phase được triển khai, đọc manifest/scripts/test source và README hiện tại, chọn lệnh tồn tại, ghi lệnh/exit code vào report; không tự bịa endpoint, cài tool/global hoặc scaffold để chạy checklist.

## Kết luận và lưu kết quả

Tạo `docs/tests/results/phase-09/<test_batch_id>/report.md` và `evidence/`. Ghi C01–C08 + P09-01…P09-07 + case bổ sung; mỗi test có đúng một tag `clean`, `need-change`, `suggestion`, result, expected/actual và evidence. Thống kê đầy đủ, kết luận kỹ thuật theo rule, quyết định Chủ tịch riêng. Dừng tại Phase 09.
