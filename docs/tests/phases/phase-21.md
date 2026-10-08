# Kiểm định Phase 21 — Wizard thành lập tập đoàn

> Checklist dự kiến, chưa có kết quả test. AI đọc lại nguồn hiện tại trước mỗi batch; không gắn tag sẵn hay tự nghiệm thu.

[Rule](../RULES.md) · [Điểm vào](../README.md) · [Mẫu report](../templates/report.md) · [Roadmap](../../master-plan.md) · [Spec V1](../../product-spec.md) · [ADR](../../decisions/0001-v1-foundation.md)

## Nguồn và ranh giới

- Phase: 21
- Dependency từ roadmap: 20
- Yêu cầu liên quan: REQ02, REQ24
- Gate: Không có gate IG riêng; vẫn kiểm criteria phase và C01–C08
- Contract hash: 2c605386701b9d2994277ed155bfe703ef237c3510f28eacc72f3e9d2a751a52

Hash đối chiếu scope/demo/criteria/delivery/limits/evidence/dependency tại thời điểm soạn, không bao gồm status/nhật ký. Nguồn đổi thì cập nhật kế hoạch, không sửa report cũ. Snapshot bên dưới giúp traceability; nguồn hiện tại vẫn ưu tiên.

### Phạm vi phải đọc

- Wizard tên/biểu tượng/sứ mệnh/mục tiêu, autonomy, model connection, budget và policy preview.
- Bổ nhiệm duy nhất Chief of Staff (Ava hoặc tên Chủ tịch chọn); không tự tuyển thêm đội ngũ.
- Transactional onboarding/idempotency, riêng real storage và guarded release activation.

### Demo bắt buộc

Chạy toàn wizard trong môi trường nghiệm thu riêng, retry submit và quay lại sửa bước model.

### Giới hạn phase

Không seed demo vào real; first-run không gọi inference âm thầm.

### Evidence bàn giao cần đối chiếu

Onboarding e2e trong test environment và transactional evidence.

## Mapping nghiệm thu → test

Mỗi AC là gạch đầu dòng nghiệm thu roadmap hiện tại khi soạn. Kiểm thêm C01–C08 theo rule; tiêu chí thay đổi cần remap trong report. Mọi case dưới đây bắt buộc trong phạm vi phase; không gọi inference nếu chưa có grant, mà ghi blocked cho case cần run thật.

| Tiêu chí | Kỳ vọng từ roadmap | Test IDs tối thiểu |
| --- | --- | --- |
| AC1 | Không tạo công ty thật của người dùng trong quá trình phát triển. | P21-02, P21-05 |
| AC2 | Submit trùng không tạo hai công ty/nhân viên; lỗi rollback sạch. | P21-03, P21-04 |
| AC3 | Đường real production onboarding vẫn khóa đến release gate Phase 23. | P21-02, P21-06, P21-07 |

## Ca kiểm định riêng của phase

Mỗi dòng là một test phải có record kết quả riêng. Các biến thể negative/race trong dòng ghi sub-results/evidence để không bỏ sót; nếu một biến thể bắt buộc chưa đạt, cả test không clean. C01–C08 cũng phải có record riêng.

| ID | Test | Bước/điều kiện | Kỳ vọng | Evidence cần lưu | Nguồn bổ sung |
| --- | --- | --- | --- | --- | --- |
| P21-01 | Wizard validation/UX | Tên/icon/mission/goal/autonomy/model/budget/policy preview, back/invalid submit | Vietnamese/focus/mobile, dữ liệu bước giữ, config invalid không submit | E2E ảnh/validation output | Spec §3/10 |
| P21-02 | Release lock | Thử real onboarding khi chưa release, agent bypass qua API | Deny trước create; chỉ môi trường nghiệm thu riêng được test | Negative DB/API counts | Spec §2/10/12 |
| P21-03 | Transactional onboarding | Inject lỗi giữa company/config/Chief of Staff trong DB test | Rollback sạch, không orphan/partial company | Failpoint counts/rollback tests | Spec §7 |
| P21-04 | Double-submit/idempotency | Retry/double-click submit đồng thời cùng onboarding key | Một company và đúng một Chief of Staff, không tuyển thêm | IDs/counts/concurrency tests | Spec §7/10 |
| P21-05 | Real/demo namespaces | Company test mới so demo/reset/artifact/thread scope | Không demo seed vào real, không tạo company người dùng khi phát triển | Environment/storage refs | Spec §12 |
| P21-06 | First-run không inference | Mở wizard, sửa bước model, confirm test env, spy dispatch | Không silent model call; dashboard trống đúng và profile đầu tiên | Request counts/ảnh/DB state | Spec §10 |
| P21-07 | Owner consent/config | Đối chiếu quyền/ngân sách/model preview và snapshot đã submit | Owner quyết định rõ, config/audit đúng input; release chưa là consent vận hành | Snapshot/audit/request refs | Spec §10 |

## Lệnh và điều kiện chạy

Chưa có command runtime được xác minh cho phase này khi soạn. Khi phase được triển khai, đọc manifest/scripts/test source và README hiện tại, chọn lệnh tồn tại, ghi lệnh/exit code vào report; không tự bịa endpoint, cài tool/global hoặc scaffold để chạy checklist.

## Kết luận và lưu kết quả

Tạo `docs/tests/results/phase-21/<test_batch_id>/report.md` và `evidence/`. Ghi C01–C08 + P21-01…P21-07 + case bổ sung; mỗi test có đúng một tag `clean`, `need-change`, `suggestion`, result, expected/actual và evidence. Thống kê đầy đủ, kết luận kỹ thuật theo rule, quyết định Chủ tịch riêng. Dừng tại Phase 21.
