# Kiểm định Phase 15 — Context và trí nhớ có kiểm chứng

> Checklist dự kiến, chưa có kết quả test. AI đọc lại nguồn hiện tại trước mỗi batch; không gắn tag sẵn hay tự nghiệm thu.

[Rule](../RULES.md) · [Điểm vào](../README.md) · [Mẫu report](../templates/report.md) · [Roadmap](../../master-plan.md) · [Spec V1](../../product-spec.md) · [ADR](../../decisions/0001-v1-foundation.md)

## Nguồn và ranh giới

- Phase: 15
- Dependency từ roadmap: 14
- Yêu cầu liên quan: REQ17
- Gate: Không có gate IG riêng; vẫn kiểm criteria phase và C01–C08
- Contract hash: f09980a3cca619b21090942cf10161e97e491f9186a67d836f600d57f26f2e1d

Hash đối chiếu scope/demo/criteria/delivery/limits/evidence/dependency tại thời điểm soạn, không bao gồm status/nhật ký. Nguồn đổi thì cập nhật kế hoạch, không sửa report cũ. Snapshot bên dưới giúp traceability; nguồn hiện tại vẫn ưu tiên.

### Phạm vi phải đọc

- Năm lớp corporate/department/employee/task/working; ACL và context budget, provenance, redaction/retention.
- Promotion: bài học → evidence → đề xuất → reviewer/Chủ tịch duyệt → version; rollback/expiry.
- Task context selection và chống đưa tài liệu không tin cậy thành policy.

### Demo bắt buộc

Một worker đề xuất bài học, reviewer duyệt, run kế tiếp dùng đúng version; agent phòng khác bị từ chối.

### Giới hạn phase

Không tự coi lời agent nói là fact đã được xác minh.

### Evidence bàn giao cần đối chiếu

Context manifest, promotion/rollback/isolation tests.

## Mapping nghiệm thu → test

Mỗi AC là gạch đầu dòng nghiệm thu roadmap hiện tại khi soạn. Kiểm thêm C01–C08 theo rule; tiêu chí thay đổi cần remap trong report. Mọi case dưới đây bắt buộc trong phạm vi phase; không gọi inference nếu chưa có grant, mà ghi blocked cho case cần run thật.

| Tiêu chí | Kỳ vọng từ roadmap | Test IDs tối thiểu |
| --- | --- | --- |
| AC1 | Retrieval và promotion cùng kiểm tra company/environment/ACL ở backend. | P15-01, P15-02 |
| AC2 | Run snapshot truy được nguồn/version; rollback không sửa lịch sử. | P15-03, P15-04 |
| AC3 | Không nhồi toàn bộ chat lịch sử; dữ liệu không tin cậy không ghi đè quyền. | P15-01, P15-05, P15-06 |

## Ca kiểm định riêng của phase

Mỗi dòng là một test phải có record kết quả riêng. Các biến thể negative/race trong dòng ghi sub-results/evidence để không bỏ sót; nếu một biến thể bắt buộc chưa đạt, cả test không clean. C01–C08 cũng phải có record riêng.

| ID | Test | Bước/điều kiện | Kỳ vọng | Evidence cần lưu | Nguồn bổ sung |
| --- | --- | --- | --- | --- | --- |
| P15-01 | Context năm lớp | Build context corporate/department/employee/task/working theo task test | Đúng nguồn/ACL/budget; không nhồi toàn bộ chat, giữ criteria/policy cần thiết | Context manifest/source hashes | Spec §7/11 |
| P15-02 | Retrieval/promotion scope | Company/environment khác và actor không ACL ở query/promote | Deny tại backend cho cả read/write, không chỉ UI | Negative ACL/DB tests | Spec §10/12 |
| P15-03 | Promotion có proof | Lesson → evidence → đề xuất → reviewer/Owner theo grant → version | Không lời agent tự thành fact/policy; authority đúng | Promotion/audit/evidence refs | Spec §10 |
| P15-04 | Version/rollback/expiry | Promote rồi rollback/expire, so run cũ/run kế tiếp | Run snapshot giữ nguồn cũ, rollback không mutate history | Memory/run versions + asserts | Spec §7 |
| P15-05 | Untrusted context | Chèn prompt injection trong tài liệu fixture, đề xuất mở quyền | Nội dung không trở thành policy, không nâng quyền model/tool | Context/policy diff and deny counts | Spec §10 |
| P15-06 | Redaction/retention/resume | Canary ở history/context; policy không lưu raw, thử resume thiếu input | Không leak; hash/provenance đủ, input thiếu yêu cầu cấp lại không bịa | Redacted manifests/resume state | Spec §10/11 |

## Lệnh và điều kiện chạy

Chưa có command runtime được xác minh cho phase này khi soạn. Khi phase được triển khai, đọc manifest/scripts/test source và README hiện tại, chọn lệnh tồn tại, ghi lệnh/exit code vào report; không tự bịa endpoint, cài tool/global hoặc scaffold để chạy checklist.

## Kết luận và lưu kết quả

Tạo `docs/tests/results/phase-15/<test_batch_id>/report.md` và `evidence/`. Ghi C01–C08 + P15-01…P15-06 + case bổ sung; mỗi test có đúng một tag `clean`, `need-change`, `suggestion`, result, expected/actual và evidence. Thống kê đầy đủ, kết luận kỹ thuật theo rule, quyết định Chủ tịch riêng. Dừng tại Phase 15.
