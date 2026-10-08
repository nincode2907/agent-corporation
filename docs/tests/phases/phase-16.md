# Kiểm định Phase 16 — Tài chính và ngân sách

> Checklist dự kiến, chưa có kết quả test. AI đọc lại nguồn hiện tại trước mỗi batch; không gắn tag sẵn hay tự nghiệm thu.

[Rule](../RULES.md) · [Điểm vào](../README.md) · [Mẫu report](../templates/report.md) · [Roadmap](../../master-plan.md) · [Spec V1](../../product-spec.md) · [ADR](../../decisions/0001-v1-foundation.md)

## Nguồn và ranh giới

- Phase: 16
- Dependency từ roadmap: 15; usage + limits có từ 06
- Yêu cầu liên quan: REQ18, REQ19
- Gate: IG16
- Contract hash: ddf770933cb1de77b2dfbf9b6f767c0b48456f6a55b2a6c0b71194d2b2b79fe1

Hash đối chiếu scope/demo/criteria/delivery/limits/evidence/dependency tại thời điểm soạn, không bao gồm status/nhật ký. Nguồn đổi thì cập nhật kế hoạch, không sửa report cũ. Snapshot bên dưới giúp traceability; nguồn hiện tại vẫn ưu tiên.

### Phạm vi phải đọc

- Ledger Company → Department → Employee → Task → Model → call/span quan sát được; reconcile và dedup usage cumulative.
- Pricing versions tại thời điểm gọi; reserve/settle/release concurrent budgets theo task/day/month.
- API trả thực, subscription, local compute và ước tính điện tách riêng; thiếu usage/giá ghi unknown.

### Demo bắt buộc

Chạy hai task demo, một retry; so ledger với usage nguồn và bật filter môi trường.

### Giới hạn phase

HTTP call/turn usage là mức đo hiện có; không bịa internal LLM call. Cost API-equivalent gateway chỉ tham khảo, không là hóa đơn ChatGPT.

### Evidence bàn giao cần đối chiếu

Reconciliation report, pricing/budget race tests và unknown cases.

## Mapping nghiệm thu → test

Mỗi AC là gạch đầu dòng nghiệm thu roadmap hiện tại khi soạn. Kiểm thêm C01–C08 theo rule; tiêu chí thay đổi cần remap trong report. Mọi case dưới đây bắt buộc trong phạm vi phase; không gọi inference nếu chưa có grant, mà ghi blocked cho case cần run thật.

| Tiêu chí | Kỳ vọng từ roadmap | Test IDs tối thiểu |
| --- | --- | --- |
| AC1 | Không đếm trùng cumulative usage sau reconnect/retry; pricing snapshot không bị giá mới sửa. | P16-01, P16-02, P16-03 |
| AC2 | Không lấy token × giá API để gọi đó là hóa đơn subscription; ước tính có nhãn. | P16-02, P16-04, P16-05, P16-06 |
| AC3 | Chỉ hard cap USD khi dữ liệu/pricing cho phép; nếu thiếu dùng giới hạn tài nguyên đã duyệt và báo rõ. | P16-03, P16-07, P16-08 |

## Ca kiểm định riêng của phase

Mỗi dòng là một test phải có record kết quả riêng. Các biến thể negative/race trong dòng ghi sub-results/evidence để không bỏ sót; nếu một biến thể bắt buộc chưa đạt, cả test không clean. C01–C08 cũng phải có record riêng.

| ID | Test | Bước/điều kiện | Kỳ vọng | Evidence cần lưu | Nguồn bổ sung |
| --- | --- | --- | --- | --- | --- |
| P16-01 | Usage/source dedup | Fixtures input/output/cache/reasoning/null/cumulative/late corrections theo call | Một final entry/call+source/version, cache/reasoning không cộng đôi, unknown khác 0 | Source→ledger reconciliation | Spec §11 |
| P16-02 | Pricing/basis immutable | Thay giá sau call; actual/subscription/API-equivalent/local compute/currency | Snapshot cũ không đổi; basis/currency riêng, estimate nhãn đúng | Pricing versions/dashboard assertions | Spec §11 |
| P16-03 | Budget concurrent settle | Reserve/settle/release parallel/repeated/failure/unknown theo task/day/month | Không double-spend/settle; unknown unresolved; hết grant 0 new dispatch | Race/call/reservation refs | Spec §10/11 |
| P16-04 | Lifetime accepted cohort | Task 2 USD kỳ trước + 3 USD kỳ accepted, retry/review/children | Cohort lifetime=5 cùng basis, descendant rollup một lần; retry task độc lập không nhập ngầm | Fixture/query expected totals | Spec §13 |
| P16-05 | Period/late corrections | Cùng fixture, late usage recorded kỳ sau, report as_of/version | Operating cost 2 rồi 3 theo occurred_at; correction giữ report cũ, coverage rõ | Versioned report/query comparison | Spec §13 |
| P16-06 | Finance drilldown/isolation | Company→department→employee→task→model→HTTP call, environment filter | Tổng đến nguồn khớp; không cộng gateway global/native vào công ty | Query/ledger IDs và ảnh | Spec §11/12 |
| P16-07 | Không hứa hard cap giả | Thiếu pricing/usage và overshoot lượt in-flight với fake adapter | Resource limits được duyệt, cost unknown/estimate, không hard token/USD cap vô căn cứ | UI/source and limit tests | Spec §11 |
| P16-08 | IG16 | Calls/usage→ledger/budgets/pricing→finance; audit IG12 và cases xuyên kỳ | Dedup/late/unknown/race/cohort pass; grant IG16 riêng nếu tạo run thật | IG16 report + upstream/call IDs | Spec §13 |

## Lệnh và điều kiện chạy

Chưa có command runtime được xác minh cho phase này khi soạn. Khi phase được triển khai, đọc manifest/scripts/test source và README hiện tại, chọn lệnh tồn tại, ghi lệnh/exit code vào report; không tự bịa endpoint, cài tool/global hoặc scaffold để chạy checklist.

## Kết luận và lưu kết quả

Gate IG16 phải có verdict riêng và links evidence theo spec §13. Không PASS từ mock nếu nguồn yêu cầu runtime thật. IG03 chưa có public API thì ghi lớp đã kiểm, mismatch/blocked cho proof API còn thiếu; không thêm feature để né gate.

Tạo `docs/tests/results/phase-16/<test_batch_id>/report.md` và `evidence/`. Ghi C01–C08 + P16-01…P16-08 + case bổ sung; mỗi test có đúng một tag `clean`, `need-change`, `suggestion`, result, expected/actual và evidence. Thống kê đầy đủ, kết luận kỹ thuật theo rule, quyết định Chủ tịch riêng. Dừng tại Phase 16.
