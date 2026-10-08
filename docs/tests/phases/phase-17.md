# Kiểm định Phase 17 — Benchmark và chất lượng

> Checklist dự kiến, chưa có kết quả test. AI đọc lại nguồn hiện tại trước mỗi batch; không gắn tag sẵn hay tự nghiệm thu.

[Rule](../RULES.md) · [Điểm vào](../README.md) · [Mẫu report](../templates/report.md) · [Roadmap](../../master-plan.md) · [Spec V1](../../product-spec.md) · [ADR](../../decisions/0001-v1-foundation.md)

## Nguồn và ranh giới

- Phase: 17
- Dependency từ roadmap: 16
- Yêu cầu liên quan: REQ20
- Gate: Không có gate IG riêng; vẫn kiểm criteria phase và C01–C08
- Contract hash: dd853a3c81d828cef1ac701792c97ed4775d52fc408015ca78e6dd98b4475fab

Hash đối chiếu scope/demo/criteria/delivery/limits/evidence/dependency tại thời điểm soạn, không bao gồm status/nhật ký. Nguồn đổi thì cập nhật kế hoạch, không sửa report cũ. Snapshot bên dưới giúp traceability; nguồn hiện tại vẫn ưu tiên.

### Phạm vi phải đọc

- Versioned suite/dataset, evaluator deterministic ưu tiên; human review khi cần, blind evaluation.
- First-pass success, accepted-task cost, rework, P50/P95, human intervention; denominator/time window rõ.
- Model Tournament, cố định tools/context/budget, repeated runs và CI/regression; benchmark environment riêng.

### Demo bắt buộc

So hai profile trên cùng suite; mở bài thất bại và đối chiếu điểm với test, không chỉ LLM judge.

### Giới hạn phase

Không đổi model tự động sau tournament.

### Evidence bàn giao cần đối chiếu

Suite manifest, run/evaluation artifacts và regression comparisons.

## Mapping nghiệm thu → test

Mỗi AC là gạch đầu dòng nghiệm thu roadmap hiện tại khi soạn. Kiểm thêm C01–C08 theo rule; tiêu chí thay đổi cần remap trong report. Mọi case dưới đây bắt buộc trong phạm vi phase; không gọi inference nếu chưa có grant, mà ghi blocked cho case cần run thật.

| Tiêu chí | Kỳ vọng từ roadmap | Test IDs tối thiểu |
| --- | --- | --- |
| AC1 | Không trộn benchmark/demo vào KPI vận hành thật. | P17-03 |
| AC2 | Không công bố model thắng từ một sample thiếu cơ sở; ghi cỡ mẫu và uncertainty. | P17-02, P17-04, P17-05 |
| AC3 | Evaluator/fixtures có version, môi trường và constraints tái lập được. | P17-01, P17-02, P17-06 |

## Ca kiểm định riêng của phase

Mỗi dòng là một test phải có record kết quả riêng. Các biến thể negative/race trong dòng ghi sub-results/evidence để không bỏ sót; nếu một biến thể bắt buộc chưa đạt, cả test không clean. C01–C08 cũng phải có record riêng.

| ID | Test | Bước/điều kiện | Kỳ vọng | Evidence cần lưu | Nguồn bổ sung |
| --- | --- | --- | --- | --- | --- |
| P17-01 | Suite/evaluator version | Chạy deterministic fixture suite pass/fail cùng manifest/version/config | Score từ criteria/test/artifact; LLM judge không là proof duy nhất | Suite/evaluator manifest | Spec §13 |
| P17-02 | Model tournament fairness | Cùng input/context/tools/policy/budget, repeated samples trong grant benchmark riêng | Constraints cố định, sample size/uncertainty, không chọn thắng từ sample không đủ | Per-run eval artifacts/config | Spec §10/13 |
| P17-03 | Environment isolation | Benchmark dataset/artifacts/calls và finance/KPI real filters | Không trộn benchmark/demo vào real, namespace riêng | Query counts/hashes và filters | Spec §12/13 |
| P17-04 | KPI denominators | Fixtures chưa review/failed/accepted/rework/missing latency/Owner intervention | Định nghĩa first-pass/P50/P95/cost/intervention có mẫu số/kỳ/timezone/coverage đúng | Expected KPI table + query evidence | Spec §13 |
| P17-05 | Failure drilldown/regression | Mở case thất bại, so baseline suite version và changed profile | Truy test/artifact/evaluation, regression không so sai fixtures | Comparison report + source refs | Spec §13 |
| P17-06 | Owner model config | Tournament đề xuất winner rồi spy config mutations | Không auto đổi model/tools/policy; Owner approval riêng | Config diff và audit/deny tests | Spec §10/13 |

## Lệnh và điều kiện chạy

Chưa có command runtime được xác minh cho phase này khi soạn. Khi phase được triển khai, đọc manifest/scripts/test source và README hiện tại, chọn lệnh tồn tại, ghi lệnh/exit code vào report; không tự bịa endpoint, cài tool/global hoặc scaffold để chạy checklist.

## Kết luận và lưu kết quả

Tạo `docs/tests/results/phase-17/<test_batch_id>/report.md` và `evidence/`. Ghi C01–C08 + P17-01…P17-06 + case bổ sung; mỗi test có đúng một tag `clean`, `need-change`, `suggestion`, result, expected/actual và evidence. Thống kê đầy đủ, kết luận kỹ thuật theo rule, quyết định Chủ tịch riêng. Tiếp tục remake/retest theo RULES.md khi còn need-change giải quyết được trong Phase 17; không tự chuyển phase. Nếu chỉ được giao test không sửa hoặc gặp blocker thật, lưu kết quả và điều kiện tiếp tục.
