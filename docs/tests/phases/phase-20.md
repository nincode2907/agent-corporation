# Kiểm định Phase 20 — Lịch làm việc và báo cáo điều hành

> Checklist dự kiến, chưa có kết quả test. AI đọc lại nguồn hiện tại trước mỗi batch; không gắn tag sẵn hay tự nghiệm thu.

[Rule](../RULES.md) · [Điểm vào](../README.md) · [Mẫu report](../templates/report.md) · [Roadmap](../../master-plan.md) · [Spec V1](../../product-spec.md) · [ADR](../../decisions/0001-v1-foundation.md)

## Nguồn và ranh giới

- Phase: 20
- Dependency từ roadmap: 19
- Yêu cầu liên quan: REQ23
- Gate: IG20
- Contract hash: 037c18a4e0ca411d1cbc3f2dca366c85b227a4f721c2802c9645f4c4bbeef0ea

Hash đối chiếu scope/demo/criteria/delivery/limits/evidence/dependency tại thời điểm soạn, không bao gồm status/nhật ký. Nguồn đổi thì cập nhật kế hoạch, không sửa report cũ. Snapshot bên dưới giúp traceability; nguồn hiện tại vẫn ưu tiên.

### Phạm vi phải đọc

- Persistent scheduler, timezone Asia/Ho_Chi_Minh, miss/sleep policy và idempotent job key.
- Morning brief, báo cáo bộ phận, CFO/quality summary và board review theo ledger/events.
- Proposal inbox hợp nhất; report generation theo nhu cầu, không gọi agent idle liên tục.

### Demo bắt buộc

Mô phỏng máy ngủ qua thời điểm báo cáo, mở lại và kiểm tra catch-up policy không chạy trùng.

### Giới hạn phase

Máy local tắt thì không có background execution thực.

### Evidence bàn giao cần đối chiếu

Scheduler resume/dedup tests và report reconciliation.

## Mapping nghiệm thu → test

Mỗi AC là gạch đầu dòng nghiệm thu roadmap hiện tại khi soạn. Kiểm thêm C01–C08 theo rule; tiêu chí thay đổi cần remap trong report. Mọi case dưới đây bắt buộc trong phạm vi phase; không gọi inference nếu chưa có grant, mà ghi blocked cho case cần run thật.

| Tiêu chí | Kỳ vọng từ roadmap | Test IDs tối thiểu |
| --- | --- | --- |
| AC1 | Không báo nhân viên làm xuyên đêm khi server chưa chạy. | P20-01, P20-02 |
| AC2 | Số trong báo cáo tính từ query/version/time window, AI chỉ tóm tắt. | P20-03, P20-05, P20-07 |
| AC3 | Scheduled inference nằm trong hạn mức; không tự sinh vô hạn báo cáo/họp. | P20-04, P20-06 |

## Ca kiểm định riêng của phase

Mỗi dòng là một test phải có record kết quả riêng. Các biến thể negative/race trong dòng ghi sub-results/evidence để không bỏ sót; nếu một biến thể bắt buộc chưa đạt, cả test không clean. C01–C08 cũng phải có record riêng.

| ID | Test | Bước/điều kiện | Kỳ vọng | Evidence cần lưu | Nguồn bổ sung |
| --- | --- | --- | --- | --- | --- |
| P20-01 | Persistent schedule/timezone | Fake clock Asia/Ho_Chi_Minh qua occurrence/day/month/restart | Job key+occurrence unique, timezone/kỳ đúng | Clock config/DB occurrence tests | Spec §11/12 |
| P20-02 | Sleep/missed policy | Máy ngủ qua lịch rồi restart scheduler test, skip default/catch-up Owner | Không bịa hoạt động lúc tắt, không job/report trùng | Resume/dedup counts/logs | Spec §12 |
| P20-03 | Numbers source-backed | Daily/monthly CFO/quality report từ query/version/window/scopes | Totals khớp events/ledger/incident, coverage/cost basis đúng; AI chỉ summary | Report query reconciliation | Spec §13 |
| P20-04 | Bounded summary inference | Grant thiếu/expired, scheduler parallel; live chỉ grant report batch riêng | Không meetings/report loop idle; 0 unauthorized inference | Dispatch counts/grant refs | Spec §10/11 |
| P20-05 | Inbox/source links | Morning brief/proposals link task/ledger/incident/evaluation | Đúng report version/nguồn, không lẫn môi trường | Ảnh inbox và link/query checks | Spec §3/12 |
| P20-06 | Stop khi schedule due | Stop active qua restart/catch-up với fake clock | Scheduler không tự gỡ stop/dispatch, scheduled state đúng | Epoch/job/call counts | Spec §10 |
| P20-07 | IG20 | Task/events/ledger/incident→schedule→report/inbox; audit IG03/08/12/16 | Sleep/dedup/source totals đạt; không thay upstream gate thiếu, grant IG20 riêng nếu inference | IG20 report + upstream verdicts | Spec §13 |

## Lệnh và điều kiện chạy

Chưa có command runtime được xác minh cho phase này khi soạn. Khi phase được triển khai, đọc manifest/scripts/test source và README hiện tại, chọn lệnh tồn tại, ghi lệnh/exit code vào report; không tự bịa endpoint, cài tool/global hoặc scaffold để chạy checklist.

## Kết luận và lưu kết quả

Gate IG20 phải có verdict riêng và links evidence theo spec §13. Không PASS từ mock nếu nguồn yêu cầu runtime thật. IG03 chưa có public API thì ghi lớp đã kiểm, mismatch/blocked cho proof API còn thiếu; không thêm feature để né gate.

Tạo `docs/tests/results/phase-20/<test_batch_id>/report.md` và `evidence/`. Ghi C01–C08 + P20-01…P20-07 + case bổ sung; mỗi test có đúng một tag `clean`, `need-change`, `suggestion`, result, expected/actual và evidence. Thống kê đầy đủ, kết luận kỹ thuật theo rule, quyết định Chủ tịch riêng. Tiếp tục remake/retest theo RULES.md khi còn need-change giải quyết được trong Phase 20; không tự chuyển phase. Nếu chỉ được giao test không sửa hoặc gặp blocker thật, lưu kết quả và điều kiện tiếp tục.
