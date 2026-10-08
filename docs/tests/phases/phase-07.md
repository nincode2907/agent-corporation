# Kiểm định Phase 07 — Luồng event và khôi phục kết nối

> Checklist dự kiến, chưa có kết quả test. AI đọc lại nguồn hiện tại trước mỗi batch; không gắn tag sẵn hay tự nghiệm thu.

[Rule](../RULES.md) · [Điểm vào](../README.md) · [Mẫu report](../templates/report.md) · [Roadmap](../../master-plan.md) · [Spec V1](../../product-spec.md) · [ADR](../../decisions/0001-v1-foundation.md)

## Nguồn và ranh giới

- Phase: 07
- Dependency từ roadmap: 06
- Yêu cầu liên quan: REQ04, REQ08
- Gate: Không có gate IG riêng; vẫn kiểm criteria phase và C01–C08
- Contract hash: bd561cd3b1361e87ac5cf82ea8210fc37e4037d84d35d2f912036b4be846ea6d

Hash đối chiếu scope/demo/criteria/delivery/limits/evidence/dependency tại thời điểm soạn, không bao gồm status/nhật ký. Nguồn đổi thì cập nhật kế hoạch, không sửa report cũ. Snapshot bên dưới giúp traceability; nguồn hiện tại vẫn ưu tiên.

### Phạm vi phải đọc

- HTTP request/response + tool/orchestration events của app → domain events, lưu trước phát; SSE backend → UI theo cursor.
- Ordering/dedup/reconnect, heartbeat và dấu thời điểm dữ liệu cập nhật.
- Checkpoint reconciliation khi worker/server chết; lease và idempotency tránh chạy lại side effect chưa biết kết quả.

### Demo bắt buộc

Chạy task thật, ngắt UI stream, reconnect rồi đối chiếu cùng event count; restart worker ở giữa run.

### Giới hạn phase

Replay UI ở Phase 08; không hứa exactly-once cho hệ thống ngoài.

### Evidence bàn giao cần đối chiếu

Log reconnect/crash, event IDs và state sau phục hồi.

## Mapping nghiệm thu → test

Mỗi AC là gạch đầu dòng nghiệm thu roadmap hiện tại khi soạn. Kiểm thêm C01–C08 theo rule; tiêu chí thay đổi cần remap trong report. Mọi case dưới đây bắt buộc trong phạm vi phase; không gọi inference nếu chưa có grant, mà ghi blocked cho case cần run thật.

| Tiêu chí | Kỳ vọng từ roadmap | Test IDs tối thiểu |
| --- | --- | --- |
| AC1 | Event đã lưu có thể fetch lại đúng sequence, không nhân đôi sau reconnect. | P07-01, P07-02, P07-03 |
| AC2 | Không báo đang hoạt động sau mất heartbeat; model đang chờ chỉ có trạng thái waiting, không bịa tiến độ/token nội bộ; unknown outcome cần reconciliation. | P07-04, P07-05 |
| AC3 | Crash không tạo model request/tool mới trùng; session invalidated/expired cần khôi phục từ context app; gap nguồn được hiển thị rõ. | P07-05, P07-06, P07-07 |

## Ca kiểm định riêng của phase

Mỗi dòng là một test phải có record kết quả riêng. Các biến thể negative/race trong dòng ghi sub-results/evidence để không bỏ sót; nếu một biến thể bắt buộc chưa đạt, cả test không clean. C01–C08 cũng phải có record riêng.

| ID | Test | Bước/điều kiện | Kỳ vọng | Evidence cần lưu | Nguồn bổ sung |
| --- | --- | --- | --- | --- | --- |
| P07-01 | Lưu trước phát | Observe event commit rồi SSE, inject transaction fail | Chỉ emit event committed, state/event/outbox còn durable | Commit/SSE IDs and timestamps | Spec §9 |
| P07-02 | Ordering/reconnect | Ngắt SSE, thêm events, reconnect cursor/Last-Event-ID rồi reload | Không mất/nhân đôi; ordering theo stream_seq | Before/after event ID lists | Spec §9 |
| P07-03 | Gap/cursor boundary | Dùng cursor invalid/expired/gap/scope khác | Gap có thông báo/handling rõ, không giả tiến độ | HTTP/SSE error và UI evidence | Spec §9 |
| P07-04 | Heartbeat/offline | Ngắt stream/worker heartbeat trong test runtime | UI stale/offline theo nguồn, không tiếp tục báo hoạt động | Clock/config + ảnh/state events | Spec §3/9 |
| P07-05 | Crash và unknown outcome | Kill riêng worker test ở các checkpoint model/step, restart | Reconcile lease/outcome; không request/tool trùng hay retry side effect unknown | Checkpoint/attempt/call counts | Spec §8/9 |
| P07-06 | Session/context recovery | Fake gateway expired/invalidated khi đang recover | Dùng history/checkpoint app, không resume failed session ngầm | Context/source refs và adapter trace | Spec §6/8 |
| P07-07 | Run thật đến UI | Grant mới đúng batch nếu cần chạy text-only rồi disconnect/reconnect | Run IDs/event IDs/UI khớp; waiting model không bịa tokens | Live trace + filtered SSE + ảnh | Spec §6/9 |

## Lệnh và điều kiện chạy

Chưa có command runtime được xác minh cho phase này khi soạn. Khi phase được triển khai, đọc manifest/scripts/test source và README hiện tại, chọn lệnh tồn tại, ghi lệnh/exit code vào report; không tự bịa endpoint, cài tool/global hoặc scaffold để chạy checklist.

## Kết luận và lưu kết quả

Tạo `docs/tests/results/phase-07/<test_batch_id>/report.md` và `evidence/`. Ghi C01–C08 + P07-01…P07-07 + case bổ sung; mỗi test có đúng một tag `clean`, `need-change`, `suggestion`, result, expected/actual và evidence. Thống kê đầy đủ, kết luận kỹ thuật theo rule, quyết định Chủ tịch riêng. Tiếp tục remake/retest theo RULES.md khi còn need-change giải quyết được trong Phase 07; không tự chuyển phase. Nếu chỉ được giao test không sửa hoặc gặp blocker thật, lưu kết quả và điều kiện tiếp tục.
