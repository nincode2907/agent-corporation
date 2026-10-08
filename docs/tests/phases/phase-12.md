# Kiểm định Phase 12 — Điều phối nhiều nhân viên

> Checklist dự kiến, chưa có kết quả test. AI đọc lại nguồn hiện tại trước mỗi batch; không gắn tag sẵn hay tự nghiệm thu.

[Rule](../RULES.md) · [Điểm vào](../README.md) · [Mẫu report](../templates/report.md) · [Roadmap](../../master-plan.md) · [Spec V1](../../product-spec.md) · [ADR](../../decisions/0001-v1-foundation.md)

## Nguồn và ranh giới

- Phase: 12
- Dependency từ roadmap: 11
- Yêu cầu liên quan: REQ14
- Gate: IG12
- Contract hash: d62a667bc58612dabb134099594a06a2aa54f4a4d4460caa2b7b0203568bdca1

Hash đối chiếu scope/demo/criteria/delivery/limits/evidence/dependency tại thời điểm soạn, không bao gồm status/nhật ký. Nguồn đổi thì cập nhật kế hoạch, không sửa report cũ. Snapshot bên dưới giúp traceability; nguồn hiện tại vẫn ưu tiên.

### Phạm vi phải đọc

- Supervisor/Chief of Staff, worker, reviewer; routing deterministic cho việc nhỏ.
- Subtasks/DAG, handoff contract, messages và parent/correlation IDs; giới hạn fan-out/depth/iterations.
- Shared budget reservation và hủy propagation; review/rework có bằng chứng trước human acceptance.

### Demo bắt buộc

Công ty demo có Chief of Staff → worker → reviewer sửa một app nhỏ; reviewer yêu cầu sửa một lần.

### Giới hạn phase

Agent chỉ thực thi trong scope; thêm nhân viên thử nghiệm không phải tuyển chính thức.

### Evidence bàn giao cần đối chiếu

Trace DAG, quality/rework evidence và cancellation/budget race tests.

## Mapping nghiệm thu → test

Mỗi AC là gạch đầu dòng nghiệm thu roadmap hiện tại khi soạn. Kiểm thêm C01–C08 theo rule; tiêu chí thay đổi cần remap trong report. Mọi case dưới đây bắt buộc trong phạm vi phase; không gọi inference nếu chưa có grant, mà ghi blocked cho case cần run thật.

| Tiêu chí | Kỳ vọng từ roadmap | Test IDs tối thiểu |
| --- | --- | --- |
| AC1 | Task nhỏ không tự triệu tập cả phòng; không loop delegation vô hạn. | P12-01, P12-02 |
| AC2 | Ngân sách tổng không bị vượt do các worker reserve đồng thời; dừng cha chặn bước mới của con. | P12-03, P12-04, P12-06 |
| AC3 | Chủ tịch thấy đủ evidence của từng handoff và quyết định nghiệm thu. | P12-05, P12-07 |

## Ca kiểm định riêng của phase

Mỗi dòng là một test phải có record kết quả riêng. Các biến thể negative/race trong dòng ghi sub-results/evidence để không bỏ sót; nếu một biến thể bắt buộc chưa đạt, cả test không clean. C01–C08 cũng phải có record riêng.

| ID | Test | Bước/điều kiện | Kỳ vọng | Evidence cần lưu | Nguồn bổ sung |
| --- | --- | --- | --- | --- | --- |
| P12-01 | Routing bounded | Task nhỏ và task cần supervisor/worker/reviewer trong fixture | Không gọi cả phòng cho task nhỏ; fanout/depth/iterations caps | DAG/routing output | Spec §4/11 |
| P12-02 | Handoff contract/DAG | Thử cyclic/missing-parent/cross-scope/invalid output handoff | Deny invalid; parent/correlation/evidence đầy đủ | DAG validation + messages refs | Spec §7/9 |
| P12-03 | Budget reservation race | Workers reserve đồng thời cùng parent grant | Không double-spend, tính retry/rework/child calls; hết grant chặn dispatch | Parallel reservations/call counts | Spec §10/11 |
| P12-04 | Cancel propagation | Stop/cancel parent khi con queued/running/unknown | Chặn bước mới ở children, abort/reconcile in-flight | Epoch/child states/action counts | Spec §8/10 |
| P12-05 | Review và sửa thật | Grant batch riêng chạy Chief of Staff → worker → reviewer yêu cầu sửa một lần | Manifest có artifact/test/review/rework, Owner acceptance riêng | Live trace/DAG/quality artifacts | Spec §4/13 |
| P12-06 | No duplicate side effect | Crash ở handoff/tool checkpoint rồi restart riêng worker test | Không lặp tool unknown; dispatch theo receipt/idempotency | Crash logs và action receipts | Spec §8/9 |
| P12-07 | IG12 | WorkOrder → delegation → permission/approval/tools → reviewer/rework/manifest; audit IG08 | Luồng thật đạt, budget/stop/evidence đầy đủ, grant IG12 riêng | IG12 report + upstream refs/IDs | Spec §13 |

## Lệnh và điều kiện chạy

Chưa có command runtime được xác minh cho phase này khi soạn. Khi phase được triển khai, đọc manifest/scripts/test source và README hiện tại, chọn lệnh tồn tại, ghi lệnh/exit code vào report; không tự bịa endpoint, cài tool/global hoặc scaffold để chạy checklist.

## Kết luận và lưu kết quả

Gate IG12 phải có verdict riêng và links evidence theo spec §13. Không PASS từ mock nếu nguồn yêu cầu runtime thật. IG03 chưa có public API thì ghi lớp đã kiểm, mismatch/blocked cho proof API còn thiếu; không thêm feature để né gate.

Tạo `docs/tests/results/phase-12/<test_batch_id>/report.md` và `evidence/`. Ghi C01–C08 + P12-01…P12-07 + case bổ sung; mỗi test có đúng một tag `clean`, `need-change`, `suggestion`, result, expected/actual và evidence. Thống kê đầy đủ, kết luận kỹ thuật theo rule, quyết định Chủ tịch riêng. Tiếp tục remake/retest theo RULES.md khi còn need-change giải quyết được trong Phase 12; không tự chuyển phase. Nếu chỉ được giao test không sửa hoặc gặp blocker thật, lưu kết quả và điều kiện tiếp tục.
