# Kiểm định Phase 19 — Sự cố và dừng khẩn cấp

> Checklist dự kiến, chưa có kết quả test. AI đọc lại nguồn hiện tại trước mỗi batch; không gắn tag sẵn hay tự nghiệm thu.

[Rule](../RULES.md) · [Điểm vào](../README.md) · [Mẫu report](../templates/report.md) · [Roadmap](../../master-plan.md) · [Spec V1](../../product-spec.md) · [ADR](../../decisions/0001-v1-foundation.md)

## Nguồn và ranh giới

- Phase: 19
- Dependency từ roadmap: 18; stop tối thiểu đã có ở 06
- Yêu cầu liên quan: REQ22
- Gate: Không có gate IG riêng; vẫn kiểm criteria phase và C01–C08
- Contract hash: 9a4977e69619bdece03e2b0756421c92483c3c6201e0cfe151ff60ee0849a68d

Hash đối chiếu scope/demo/criteria/delivery/limits/evidence/dependency tại thời điểm soạn, không bao gồm status/nhật ký. Nguồn đổi thì cập nhật kế hoạch, không sửa report cũ. Snapshot bên dưới giúp traceability; nguồn hiện tại vẫn ưu tiên.

### Phạm vi phải đọc

- Incident detection: loop, timeout, token burst, tool deny, stalled lease, server disconnect.
- Global Emergency Stop durable: chặn dispatch/request/tool mới, abort request và worker app đang chạy; không dừng codex-server chung hoặc run ứng dụng khác.
- Incident timeline, reconciliation, safe retry/manual intervention và recovery drill.

### Demo bắt buộc

Tạo loop demo và kill worker, bấm stop; restart hệ thống vẫn giữ stop cho tới Chủ tịch mở lại.

### Giới hạn phase

Không đợi phase này mới có timeout/stop; đây là mở rộng toàn hệ thống.

### Evidence bàn giao cần đối chiếu

Fault injection, stop race và recovery drill artifacts.

## Mapping nghiệm thu → test

Mỗi AC là gạch đầu dòng nghiệm thu roadmap hiện tại khi soạn. Kiểm thêm C01–C08 theo rule; tiêu chí thay đổi cần remap trong report. Mọi case dưới đây bắt buộc trong phạm vi phase; không gọi inference nếu chưa có grant, mà ghi blocked cho case cần run thật.

| Tiêu chí | Kỳ vọng từ roadmap | Test IDs tối thiểu |
| --- | --- | --- |
| AC1 | Stop không tự được gỡ sau restart; race dispatch/abort đã kiểm tra và gateway cancellation được xác minh. | P19-02, P19-03, P19-04 |
| AC2 | Không hứa hoàn tác hành động bên ngoài; unknown outcome được cô lập trước retry. | P19-04, P19-05 |
| AC3 | Có incident report liên kết cause/evidence/recovery và run bị ảnh hưởng. | P19-01, P19-06, P19-07 |

## Ca kiểm định riêng của phase

Mỗi dòng là một test phải có record kết quả riêng. Các biến thể negative/race trong dòng ghi sub-results/evidence để không bỏ sót; nếu một biến thể bắt buộc chưa đạt, cả test không clean. C01–C08 cũng phải có record riêng.

| ID | Test | Bước/điều kiện | Kỳ vọng | Evidence cần lưu | Nguồn bổ sung |
| --- | --- | --- | --- | --- | --- |
| P19-01 | Incident detection | Inject loop/timeout/token burst/tool deny/stalled lease/disconnect trong test | Threshold nguồn rõ, incident đúng IDs, không bịa usage burst thiếu số | Fault config + incident/event refs | Spec §8/11 |
| P19-02 | Stop durable | Stop riêng app test rồi restart API/workers | Stop vẫn active, chỉ Owner mở lại; không dừng gateway/shared apps | Epoch/state/restart evidence | Spec §10 |
| P19-03 | Dispatch/stop race | Concurrent stop với request/tool preparation/dispatch | 0 dispatch mới sau stop decision; in-flight/unknown được phân biệt | Serialized timeline/receipts | Spec §10 |
| P19-04 | Abort thực | Fake và live cancellation chỉ đúng grant; đối chiếu gateway outcome | Không coi UI close là abort, không claim undo external action | App/gateway filtered call evidence | Spec §6/10 |
| P19-05 | Unknown reconciliation | Timeout/crash sau external test action rồi recover/retry | Cô lập outcome unknown, receipt/checkpoint đối chiếu trước retry | Incident/receipt/attempt counts | Spec §8 |
| P19-06 | Recovery drill/Owner | Phục hồi loop/crash sau canary fault, Owner quyết định gỡ stop | Cause/evidence/recovery audit đầy đủ, stop không tự gỡ | Drill report và decisions | Spec §10/13 |
| P19-07 | Incident UI scope | Xem pending/aborted/in-flight/unknown và run bị ảnh hưởng | Liên kết chính xác, không báo dừng hết khi còn pending | Ảnh/state/action counts | Spec §3/8 |

## Lệnh và điều kiện chạy

Chưa có command runtime được xác minh cho phase này khi soạn. Khi phase được triển khai, đọc manifest/scripts/test source và README hiện tại, chọn lệnh tồn tại, ghi lệnh/exit code vào report; không tự bịa endpoint, cài tool/global hoặc scaffold để chạy checklist.

## Kết luận và lưu kết quả

Tạo `docs/tests/results/phase-19/<test_batch_id>/report.md` và `evidence/`. Ghi C01–C08 + P19-01…P19-07 + case bổ sung; mỗi test có đúng một tag `clean`, `need-change`, `suggestion`, result, expected/actual và evidence. Thống kê đầy đủ, kết luận kỹ thuật theo rule, quyết định Chủ tịch riêng. Dừng tại Phase 19.
