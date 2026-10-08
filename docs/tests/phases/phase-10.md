# Kiểm định Phase 10 — Quyền hạn và hộp phê duyệt

> Checklist dự kiến, chưa có kết quả test. AI đọc lại nguồn hiện tại trước mỗi batch; không gắn tag sẵn hay tự nghiệm thu.

[Rule](../RULES.md) · [Điểm vào](../README.md) · [Mẫu report](../templates/report.md) · [Roadmap](../../master-plan.md) · [Spec V1](../../product-spec.md) · [ADR](../../decisions/0001-v1-foundation.md)

## Nguồn và ranh giới

- Phase: 10
- Dependency từ roadmap: 09; baseline đã có ở 06
- Yêu cầu liên quan: REQ01, REQ03, REQ11, REQ12, REQ25
- Gate: Không có gate IG riêng; vẫn kiểm criteria phase và C01–C08
- Contract hash: 0e5653536aad9abd585c1b03fa396a13565f947a54be2b3c8551d10388dea62d

Hash đối chiếu scope/demo/criteria/delivery/limits/evidence/dependency tại thời điểm soạn, không bao gồm status/nhật ký. Nguồn đổi thì cập nhật kế hoạch, không sửa report cũ. Snapshot bên dưới giúp traceability; nguồn hiện tại vẫn ưu tiên.

### Phạm vi phải đọc

- Ba cấp: tự động trong scope, ủy quyền có hạn, Chủ tịch duyệt; backend và executor cùng cưỡng chế.
- Approval gắn action/payload hash/company/run, policy version, expiry, budget; deny stale/replay/cross-scope.
- Secrets references, audit owner-only configuration; policy không cho agent tự cấp quyền.

### Demo bắt buộc

Agent đề xuất tăng quyền, duyệt một payload rồi thay payload để chứng minh approval cũ không dùng lại.

### Giới hạn phase

Không mở quyền mới trước gate này; external send/deploy/destructive vẫn cần Chủ tịch duyệt.

### Evidence bàn giao cần đối chiếu

Bypass/replay/stale tests và audit trail.

## Mapping nghiệm thu → test

Mỗi AC là gạch đầu dòng nghiệm thu roadmap hiện tại khi soạn. Kiểm thêm C01–C08 theo rule; tiêu chí thay đổi cần remap trong report. Mọi case dưới đây bắt buộc trong phạm vi phase; không gọi inference nếu chưa có grant, mà ghi blocked cho case cần run thật.

| Tiêu chí | Kỳ vọng từ roadmap | Test IDs tối thiểu |
| --- | --- | --- |
| AC1 | Bypass API/tool vẫn bị chặn; agent không tự đổi policy/model/budget. | P10-01, P10-06 |
| AC2 | Approval khác run/company hoặc hết hạn bị từ chối; deny không tạo side effect. | P10-02, P10-03, P10-04, P10-05 |
| AC3 | Owner-only config và secret redaction đã được kiểm tra ở lớp thực thi. | P10-06, P10-07 |

## Ca kiểm định riêng của phase

Mỗi dòng là một test phải có record kết quả riêng. Các biến thể negative/race trong dòng ghi sub-results/evidence để không bỏ sót; nếu một biến thể bắt buộc chưa đạt, cả test không clean. C01–C08 cũng phải có record riêng.

| ID | Test | Bước/điều kiện | Kỳ vọng | Evidence cần lưu | Nguồn bổ sung |
| --- | --- | --- | --- | --- | --- |
| P10-01 | Authority bypass | Agent gọi backend/executor trực tiếp đổi policy/model/budget/autonomy/Owner actions | Deny tại lớp thật; Owner quyết định được audit | Negative API/executor/audit suite | Spec §10 |
| P10-02 | Canonical payload hash | JSON reordered/schema valid, tamper scope/action/amount/revision/version | Hash canonical ổn định; integer micros, reject nonfinite; tamper invalidates approval | Contract vectors + assertions | Spec §10 |
| P10-03 | Stale/replay/cross-scope | Approve rồi đổi policy/payload/run/company hoặc expiry, dùng lại token | Deny stale/replayed/wrong-scope trước side effect | Request/receipt/DB before/after | Spec §10 |
| P10-04 | Consume/reserve race | Double-submit approval đồng thời với reserve và dispatch | Consume một lần atomic; không duplicate side effect | Parallel test + receipt/reservation IDs | Spec §10/11 |
| P10-05 | Stop/policy epoch race | Stop/cancel/revoke ngay trước executor action trong test | Recheck epoch; phân biệt in-flight/unknown, không hồi tố giả | Timeline/epoch/action evidence | Spec §10 |
| P10-06 | Local Owner auth boundary | Test Host/Origin/CSRF/cookie/session mutation và actor scoped theo implementation | Cross-origin/unauthorized deny; không chỉ hidden button; không claim Secure trên HTTP | Auth negative tests + config metadata | Spec §10 |
| P10-07 | Inbox/audit/secrets | Owner approve/reject có impact/evidence; canary secret test | Deny không side effect; audit actor/hash/version; secrets ref/redaction | Ảnh inbox + audit/log assertions | Spec §3/10 |

## Lệnh và điều kiện chạy

Chưa có command runtime được xác minh cho phase này khi soạn. Khi phase được triển khai, đọc manifest/scripts/test source và README hiện tại, chọn lệnh tồn tại, ghi lệnh/exit code vào report; không tự bịa endpoint, cài tool/global hoặc scaffold để chạy checklist.

## Kết luận và lưu kết quả

Tạo `docs/tests/results/phase-10/<test_batch_id>/report.md` và `evidence/`. Ghi C01–C08 + P10-01…P10-07 + case bổ sung; mỗi test có đúng một tag `clean`, `need-change`, `suggestion`, result, expected/actual và evidence. Thống kê đầy đủ, kết luận kỹ thuật theo rule, quyết định Chủ tịch riêng. Tiếp tục remake/retest theo RULES.md khi còn need-change giải quyết được trong Phase 10; không tự chuyển phase. Nếu chỉ được giao test không sửa hoặc gặp blocker thật, lưu kết quả và điều kiện tiếp tục.
