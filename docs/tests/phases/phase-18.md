# Kiểm định Phase 18 — Đề xuất tối ưu có thử nghiệm

> Checklist dự kiến, chưa có kết quả test. AI đọc lại nguồn hiện tại trước mỗi batch; không gắn tag sẵn hay tự nghiệm thu.

[Rule](../RULES.md) · [Điểm vào](../README.md) · [Mẫu report](../templates/report.md) · [Roadmap](../../master-plan.md) · [Spec V1](../../product-spec.md) · [ADR](../../decisions/0001-v1-foundation.md)

## Nguồn và ranh giới

- Phase: 18
- Dependency từ roadmap: 17
- Yêu cầu liên quan: REQ21
- Gate: Không có gate IG riêng; vẫn kiểm criteria phase và C01–C08
- Contract hash: a0e98142327f89aa1ec21acd7113009ff87383efa39eb2c132d67ceeb7161823

Hash đối chiếu scope/demo/criteria/delivery/limits/evidence/dependency tại thời điểm soạn, không bao gồm status/nhật ký. Nguồn đổi thì cập nhật kế hoạch, không sửa report cũ. Snapshot bên dưới giúp traceability; nguồn hiện tại vẫn ưu tiên.

### Phạm vi phải đọc

- Đề xuất routing/model/context/nhân sự từ ledger + benchmark; expected benefit và rủi ro.
- Shadow/A-B experiment trong môi trường riêng, hạn mức và acceptance rule trước thử.
- Owner approval, config version rollout/rollback; tránh thay đổi nhiều biến rồi gán nguyên nhân.

### Demo bắt buộc

Đề xuất đổi model worker, chạy suite hiện tại/mới, Chủ tịch từ chối rồi kiểm tra cấu hình vẫn như cũ.

### Giới hạn phase

Hội đồng điều hành nhiều agent chuyên sâu là mở rộng sau V1.

### Evidence bàn giao cần đối chiếu

Experiment report, approval audit và rollback evidence.

## Mapping nghiệm thu → test

Mỗi AC là gạch đầu dòng nghiệm thu roadmap hiện tại khi soạn. Kiểm thêm C01–C08 theo rule; tiêu chí thay đổi cần remap trong report. Mọi case dưới đây bắt buộc trong phạm vi phase; không gọi inference nếu chưa có grant, mà ghi blocked cho case cần run thật.

| Tiêu chí | Kỳ vọng từ roadmap | Test IDs tối thiểu |
| --- | --- | --- |
| AC1 | LLM không tự phát minh KPI hay tự áp cấu hình. | P18-01, P18-02, P18-06 |
| AC2 | Experiment không gọi external side effect thật và không trộn ledger real. | P18-02, P18-03 |
| AC3 | Có snapshot trước/sau và rollback đã thử. | P18-04, P18-05 |

## Ca kiểm định riêng của phase

Mỗi dòng là một test phải có record kết quả riêng. Các biến thể negative/race trong dòng ghi sub-results/evidence để không bỏ sót; nếu một biến thể bắt buộc chưa đạt, cả test không clean. C01–C08 cũng phải có record riêng.

| ID | Test | Bước/điều kiện | Kỳ vọng | Evidence cần lưu | Nguồn bổ sung |
| --- | --- | --- | --- | --- | --- |
| P18-01 | Proposal factual | Ledger/benchmark evidence → routing/model/context/HR proposal | KPI từ queries, expected benefit/risk có nguồn, không LLM tự bịa | Proposal/evidence refs | Spec §13 |
| P18-02 | Experiment preconditions | Versioned control/candidate, acceptance rule trước test, bounded grant nếu inference | Biến/constraints rõ, thử trong môi trường riêng đúng hạn mức | Experiment plan/grant/config | Spec §10/13 |
| P18-03 | Shadow side effects | Replay/simulate candidate external actions bằng executor stub | Không send/deploy tác động ngoài thật; ledger không real | Receipt/action counters + scope proof | Spec §10/12 |
| P18-04 | Reject/approval gate | Owner từ chối đổi model worker, thử agent tự apply và stale proposal | Không config change trước approval đúng payload/version | Before/after snapshot và negative tests | Spec §10 |
| P18-05 | Rollout/rollback | Approve test config, rollout rồi rollback trong scope cô lập | Phiên bản trước/sau audit, restore đúng, run cũ immutable | Config hashes/audit/rollback log | Spec §7/13 |
| P18-06 | Comparison honest | So current/new suite có missing data/uncertainty | Không gán causality khi đổi nhiều biến, no unknown=0 | Experiment report/query/evaluator | Spec §13 |

## Lệnh và điều kiện chạy

Chưa có command runtime được xác minh cho phase này khi soạn. Khi phase được triển khai, đọc manifest/scripts/test source và README hiện tại, chọn lệnh tồn tại, ghi lệnh/exit code vào report; không tự bịa endpoint, cài tool/global hoặc scaffold để chạy checklist.

## Kết luận và lưu kết quả

Tạo `docs/tests/results/phase-18/<test_batch_id>/report.md` và `evidence/`. Ghi C01–C08 + P18-01…P18-06 + case bổ sung; mỗi test có đúng một tag `clean`, `need-change`, `suggestion`, result, expected/actual và evidence. Thống kê đầy đủ, kết luận kỹ thuật theo rule, quyết định Chủ tịch riêng. Tiếp tục remake/retest theo RULES.md khi còn need-change giải quyết được trong Phase 18; không tự chuyển phase. Nếu chỉ được giao test không sửa hoặc gặp blocker thật, lưu kết quả và điều kiện tiếp tục.
