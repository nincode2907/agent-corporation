# Kiểm định Phase 23 — Nghiệm thu và phát hành V1

> Checklist dự kiến, chưa có kết quả test. AI đọc lại nguồn hiện tại trước mỗi batch; không gắn tag sẵn hay tự nghiệm thu.

[Rule](../RULES.md) · [Điểm vào](../README.md) · [Mẫu report](../templates/report.md) · [Roadmap](../../master-plan.md) · [Spec V1](../../product-spec.md) · [ADR](../../decisions/0001-v1-foundation.md)

## Nguồn và ranh giới

- Phase: 23
- Dependency từ roadmap: 22; toàn bộ phase 00–22 được nghiệm thu
- Yêu cầu liên quan: REQ01, REQ02, REQ24, REQ26
- Gate: R1–R8 + IG03/08/12/16/20
- Contract hash: 767ba55882e62a1f91ad5c96d4690a52ca66156fcb87ce3d67e1526a384f40bb

Hash đối chiếu scope/demo/criteria/delivery/limits/evidence/dependency tại thời điểm soạn, không bao gồm status/nhật ký. Nguồn đổi thì cập nhật kế hoạch, không sửa report cũ. Snapshot bên dưới giúp traceability; nguồn hiện tại vẫn ưu tiên.

### Phạm vi phải đọc

- E2E nhiệm vụ thật sandbox: goal → plan → worker tools → reviewer → approval → acceptance → ledger/report.
- Polish UI, error handling, pagination/virtualization/retention, hiệu năng, cài local và tài liệu vận hành.
- Release checklist định lượng, bằng chứng tất cả gates, known limits; Chủ tịch nghiệm thu V1 rồi mới mở real onboarding.

### Demo bắt buộc

Cài từ hướng dẫn, chạy nhiệm vụ sandbox end-to-end, gây lỗi/restart, restore rồi đối chiếu UI/ledger; Chủ tịch xem gói evidence.

### Giới hạn phase

Không tự deploy cloud, không 3D office trong V1; dừng trước chặng vận hành thật.

### Evidence bàn giao cần đối chiếu

E2E report, release manifest, screenshots và quyết định nghiệm thu V1.

## Mapping nghiệm thu → test

Mỗi AC là gạch đầu dòng nghiệm thu roadmap hiện tại khi soạn. Kiểm thêm C01–C08 theo rule; tiêu chí thay đổi cần remap trong report. Mọi case dưới đây bắt buộc trong phạm vi phase; không gọi inference nếu chưa có grant, mà ghi blocked cho case cần run thật.

| Tiêu chí | Kỳ vọng từ roadmap | Test IDs tối thiểu |
| --- | --- | --- |
| AC1 | Tất cả release gates R1–R8 đạt; không có lỗi blocker/nghiêm trọng chưa xử lý. | P23-01, P23-02, P23-03, P23-04, P23-05, P23-06, P23-07, P23-08, P23-09 |
| AC2 | Có bằng chứng thật cho observability, policy, budgets và recovery, không chỉ UI fixture. | P23-01, P23-02, P23-03, P23-04, P23-05, P23-06, P23-07 |
| AC3 | Chủ tịch chấp nhận release; không tự tạo công ty thật hoặc chạy task thật trước quyết định này. | P23-08, P23-10 |

## Ca kiểm định riêng của phase

Mỗi dòng là một test phải có record kết quả riêng. Các biến thể negative/race trong dòng ghi sub-results/evidence để không bỏ sót; nếu một biến thể bắt buộc chưa đạt, cả test không clean. C01–C08 cũng phải có record riêng.

| ID | Test | Bước/điều kiện | Kỳ vọng | Evidence cần lưu | Nguồn bổ sung |
| --- | --- | --- | --- | --- | --- |
| P23-01 | R1 công việc thật | Grant batch riêng, 3 sandbox scenarios: success, rework, approval denied | Goal→artifact→review→Owner acceptance có trace; rejected action không side effect | E2E artifacts/tests/decisions | Spec §13 |
| P23-02 | R2 observability/performance | Run/event thật cho trace; load 20 profiles/10000 events, ít nhất 200 commit-confirmed→DOM measurements | No gaps/duplicates, p95 ≤2s; công bố browser/máy/version/instrumentation | Load timings/IDs/plots/report | Spec §13 |
| P23-03 | R3 quyền | Negative owner-only/cross-scope/stale approval/tool escape/secret leak + double-submit race | 0 bypass thành công tại API/executor/DB | Negative suite/receipts | Spec §13 |
| P23-04 | R4 ngân sách | Parallel reserve/settle/late usage/unknown/revoke/expiry | 0 dispatch mới sau hết grant/reservation, no duplicate costs, labels/basis đúng | Resource/ledger reconciliation | Spec §13 |
| P23-05 | R5 sự cố | Stop/kill worker/restart/loop/offline/interrupt/cancel recovery trong test | Stop durable, gateway abort verified; no replay/unknown side-effect retry | Fault/recovery logs và receipts | Spec §13 |
| P23-06 | R6 isolation | Demo reset/benchmark/real, FK/RLS/artifact/thread/session namespace | Không mix/xóa cross-env, company người dùng chưa tạo trước release decision | Scope suite/manifests | Spec §13 |
| P23-07 | R7 restore | Restore DB/artifacts/config refs test sạch và migration drill | Counts/hash/links/history/stop khớp, không inference tự bật | Restore/migration manifests | Spec §13 |
| P23-08 | R8 cài/UX/bàn giao | Cài/chạy từ docs, 390px/desktop/keyboard, pagination/replay tải lớn, known limits | 0 blocker/nghiêm trọng chưa xử lý; Owner chấp nhận V1 là quyết định riêng | Install/UX reports + release manifest + decision ref | Spec §13 |
| P23-09 | Audit toàn bộ IG | Đọc reports IG03/08/12/16/20 và source/config relevance hiện tại | Đủ PASS có proof; thay đổi ảnh hưởng cần retest grant mới, IG20 không bù gate thiếu | Gate matrix và refs/batch versions | Spec §13 |
| P23-10 | Release lock/chặng B | Trước/sau Owner release decision trong test, spy real create/deploy | Không tự công ty thật/deploy cloud/vận hành sau V1; dừng bàn giao | Release decision/audit/state evidence | Spec §2/10/13 |

## Lệnh và điều kiện chạy

Chưa có command runtime được xác minh cho phase này khi soạn. Khi phase được triển khai, đọc manifest/scripts/test source và README hiện tại, chọn lệnh tồn tại, ghi lệnh/exit code vào report; không tự bịa endpoint, cài tool/global hoặc scaffold để chạy checklist.

## Kết luận và lưu kết quả

Gate R1–R8 + IG03/08/12/16/20 phải có verdict riêng và links evidence theo spec §13. Không PASS từ mock nếu nguồn yêu cầu runtime thật. IG03 chưa có public API thì ghi lớp đã kiểm, mismatch/blocked cho proof API còn thiếu; không thêm feature để né gate.

Tạo `docs/tests/results/phase-23/<test_batch_id>/report.md` và `evidence/`. Ghi C01–C08 + P23-01…P23-10 + case bổ sung; mỗi test có đúng một tag `clean`, `need-change`, `suggestion`, result, expected/actual và evidence. Thống kê đầy đủ, kết luận kỹ thuật theo rule, quyết định Chủ tịch riêng. Dừng tại Phase 23.
