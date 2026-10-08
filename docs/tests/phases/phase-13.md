# Kiểm định Phase 13 — Tổ chức và hồ sơ nhân viên

> Checklist dự kiến, chưa có kết quả test. AI đọc lại nguồn hiện tại trước mỗi batch; không gắn tag sẵn hay tự nghiệm thu.

[Rule](../RULES.md) · [Điểm vào](../README.md) · [Mẫu report](../templates/report.md) · [Roadmap](../../master-plan.md) · [Spec V1](../../product-spec.md) · [ADR](../../decisions/0001-v1-foundation.md)

## Nguồn và ranh giới

- Phase: 13
- Dependency từ roadmap: 12
- Yêu cầu liên quan: REQ06, REQ15
- Gate: Không có gate IG riêng; vẫn kiểm criteria phase và C01–C08
- Contract hash: 30b065c3b5430617786f4e615230d903ecebe572fd79ce453da3991775a2bd1a

Hash đối chiếu scope/demo/criteria/delivery/limits/evidence/dependency tại thời điểm soạn, không bao gồm status/nhật ký. Nguồn đổi thì cập nhật kế hoạch, không sửa report cũ. Snapshot bên dưới giúp traceability; nguồn hiện tại vẫn ưu tiên.

### Phạm vi phải đọc

- Organization chart, department, reporting line; permanent/on-demand/contractor với trạng thái thật.
- Employee version lưu role/persona, model + reasoning, tools/skills, context và policy refs.
- Inspector dùng chung mọi nơi; xem workload và hiệu suất gắn đúng profile version.

### Demo bắt buộc

Đổi profile demo bằng quyền Chủ tịch; run cũ vẫn hiển thị version cũ, run mới dùng version mới.

### Giới hạn phase

Không tự bổ nhiệm CEO; Chief of Staff là vị trí đầu tiên khi vận hành thật.

### Evidence bàn giao cần đối chiếu

Version comparison, run snapshots và org integrity tests.

## Mapping nghiệm thu → test

Mỗi AC là gạch đầu dòng nghiệm thu roadmap hiện tại khi soạn. Kiểm thêm C01–C08 theo rule; tiêu chí thay đổi cần remap trong report. Mọi case dưới đây bắt buộc trong phạm vi phase; không gọi inference nếu chưa có grant, mà ghi blocked cho case cần run thật.

| Tiêu chí | Kỳ vọng từ roadmap | Test IDs tối thiểu |
| --- | --- | --- |
| AC1 | Hồ sơ idle không tạo tiến trình/inference liên tục. | P13-02, P13-05 |
| AC2 | Model/profile thay đổi qua owner-only; không mutate snapshot của run đang chạy; gateway session cố định model/effort phải đổi session nếu dùng. | P13-03, P13-04 |
| AC3 | Org chart không có chu kỳ; xóa/chuyển phòng vẫn giữ lịch sử và evidence. | P13-01, P13-06, P13-07 |

## Ca kiểm định riêng của phase

Mỗi dòng là một test phải có record kết quả riêng. Các biến thể negative/race trong dòng ghi sub-results/evidence để không bỏ sót; nếu một biến thể bắt buộc chưa đạt, cả test không clean. C01–C08 cũng phải có record riêng.

| ID | Test | Bước/điều kiện | Kỳ vọng | Evidence cần lưu | Nguồn bổ sung |
| --- | --- | --- | --- | --- | --- |
| P13-01 | Org integrity | Tạo/chuyển phòng/reporting parent, thử cycle/cross-company | Deny cycle/cross-scope, không đứt history khi đổi tổ chức | Org/FK tests và graph | Spec §7 |
| P13-02 | Contract/lifecycle | Permanent/on-demand/contractor và các status workload bằng fixtures | Đúng semantics, không suy idle thành terminated | UI/DB status assertions | Spec §3/7 |
| P13-03 | Immutable profiles | Owner tạo version mới, thử agent đổi model/tools/policy và sửa version đã dùng | Owner-only, version dùng rồi immutable | Version diff/audit/negative tests | Spec §7/10 |
| P13-04 | Run snapshots | Run cũ/đang chạy/new sau profile change, session reuse fake nếu có | Run cũ giữ version, new dùng version mới; session model/effort cố định đúng | Run/version IDs và adapter trace | Spec §6/7 |
| P13-05 | Idle không inference | Mở hồ sơ idle/workload, quan sát dispatch scheduler | Không background thinking/inference khi không assignment | Call counters + source review | Spec §2/10 |
| P13-06 | Inspector/org metrics | Mở Inspector từ chart/profile/task, so workload/evaluation đúng version | Metrics/drilldown gắn đúng run/profile; không bịa hiệu suất | Ảnh + query/ID correlation | Spec §3/13 |
| P13-07 | Không CEO/real hire tự phát | Đối chiếu init/org create/proposal với authority | Không tự bổ nhiệm CEO hay tạo real staffing; Owner decisions riêng | Source/DB/audit evidence | Spec §2/10 |

## Lệnh và điều kiện chạy

Chưa có command runtime được xác minh cho phase này khi soạn. Khi phase được triển khai, đọc manifest/scripts/test source và README hiện tại, chọn lệnh tồn tại, ghi lệnh/exit code vào report; không tự bịa endpoint, cài tool/global hoặc scaffold để chạy checklist.

## Kết luận và lưu kết quả

Tạo `docs/tests/results/phase-13/<test_batch_id>/report.md` và `evidence/`. Ghi C01–C08 + P13-01…P13-07 + case bổ sung; mỗi test có đúng một tag `clean`, `need-change`, `suggestion`, result, expected/actual và evidence. Thống kê đầy đủ, kết luận kỹ thuật theo rule, quyết định Chủ tịch riêng. Tiếp tục remake/retest theo RULES.md khi còn need-change giải quyết được trong Phase 13; không tự chuyển phase. Nếu chỉ được giao test không sửa hoặc gặp blocker thật, lưu kết quả và điều kiện tiếp tục.
