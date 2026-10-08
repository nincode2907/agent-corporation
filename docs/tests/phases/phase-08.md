# Kiểm định Phase 08 — Live Office và Agent Inspector

> Checklist dự kiến, chưa có kết quả test. AI đọc lại nguồn hiện tại trước mỗi batch; không gắn tag sẵn hay tự nghiệm thu.

[Rule](../RULES.md) · [Điểm vào](../README.md) · [Mẫu report](../templates/report.md) · [Roadmap](../../master-plan.md) · [Spec V1](../../product-spec.md) · [ADR](../../decisions/0001-v1-foundation.md)

## Nguồn và ranh giới

- Phase: 08
- Dependency từ roadmap: 07
- Yêu cầu liên quan: REQ04, REQ05, REQ10
- Gate: IG08
- Contract hash: bb5fdee096221011e90ce1d80d08f76c0dbcaecfc70c14d0b807234adf2c033f

Hash đối chiếu scope/demo/criteria/delivery/limits/evidence/dependency tại thời điểm soạn, không bao gồm status/nhật ký. Nguồn đổi thì cập nhật kế hoạch, không sửa report cũ. Snapshot bên dưới giúp traceability; nguồn hiện tại vẫn ưu tiên.

### Phạm vi phải đọc

- Live Office 2D theo phòng ban; trạng thái idle/running/waiting/failed dựa vào event.
- Inspector mở từ dashboard/agent/task/org: Plan, tóm tắt quyết định, tools, file diff, messages, lỗi, model/profile và metrics.
- Replay timeline theo event/checkpoint đã ghi; filter task/agent/run và redaction theo quyền.

### Demo bắt buộc

Mở run thật Phase 06–07, lọc task, xem lỗi, kéo replay và reload; đối chiếu với event store.

### Giới hạn phase

Chưa có văn phòng 3D; timeline không bịa dữ liệu thiếu.

### Evidence bàn giao cần đối chiếu

Video/ảnh demo thật, event correlation và kiểm tra replay/redaction.

## Mapping nghiệm thu → test

Mỗi AC là gạch đầu dòng nghiệm thu roadmap hiện tại khi soạn. Kiểm thêm C01–C08 theo rule; tiêu chí thay đổi cần remap trong report. Mọi case dưới đây bắt buộc trong phạm vi phase; không gọi inference nếu chưa có grant, mà ghi blocked cho case cần run thật.

| Tiêu chí | Kỳ vọng từ roadmap | Test IDs tối thiểu |
| --- | --- | --- |
| AC1 | Luồng trên UI đến từ run thật; fixture chỉ dùng test UI và có nhãn. | P08-01, P08-02, P08-06 |
| AC2 | Replay không gọi model/tool, không sửa trạng thái và không tạo tác dụng phụ. | P08-03, P08-04 |
| AC3 | Không hiển thị tóm tắt quyết định như suy nghĩ nội bộ nguyên văn; prompt lưu theo policy. | P08-05 |

## Ca kiểm định riêng của phase

Mỗi dòng là một test phải có record kết quả riêng. Các biến thể negative/race trong dòng ghi sub-results/evidence để không bỏ sót; nếu một biến thể bắt buộc chưa đạt, cả test không clean. C01–C08 cũng phải có record riêng.

| ID | Test | Bước/điều kiện | Kỳ vọng | Evidence cần lưu | Nguồn bổ sung |
| --- | --- | --- | --- | --- | --- |
| P08-01 | Live Office theo event | Mở run text-only thật đã authorized và agent status view | Idle/running/waiting/failed từ events; fixture luôn nhãn | Ảnh + run/event correlations | Spec §3/9 |
| P08-02 | Inspector dùng chung | Mở cùng agent/run từ dashboard/task/org, kiểm tabs/errors/profile/metrics | Cùng IDs/source; tools chưa có không bịa diff; unknown rõ | Ảnh/tab assertions + query IDs | Spec §3 |
| P08-03 | Replay chỉ đọc | Replay cursor/filter/seek/reload, spy mutation/model/tool endpoints | 0 side effect, không state change; timeline từ persistence | Request counts và DB before/after | Spec §9 |
| P08-04 | ACL/redaction | Thử khác company/environment và nhạy cảm bằng actors test | Deny/filtered ở backend, không raw prompt/secret lộ UI | Negative API/SSE/UI evidence | Spec §9/10 |
| P08-05 | Explicit summary | Đối chiếu Plan/Decision Summary và source payload | Không claim suy nghĩ nội bộ nguyên văn hay giả dữ liệu thiếu | Source comparison + ảnh | Spec §3/9 |
| P08-06 | Reconnect/error/usage | Offline/reconnect/filter missing events/unknown usage trên cùng run | Không fake active/progress, giá trị rõ confirmed/estimated/unknown | IDs/counts/state screenshots | Spec §9/11 |
| P08-07 | IG08 | Run thật text-only → saved events → SSE → Office/Inspector/replay; audit IG03 | Gate yêu cầu run thật, no tools Phase11 sớm; grant IG08 riêng nếu gọi model | IG08 report + upstream refs/config/IDs | Spec §13 |

## Lệnh và điều kiện chạy

Chưa có command runtime được xác minh cho phase này khi soạn. Khi phase được triển khai, đọc manifest/scripts/test source và README hiện tại, chọn lệnh tồn tại, ghi lệnh/exit code vào report; không tự bịa endpoint, cài tool/global hoặc scaffold để chạy checklist.

## Kết luận và lưu kết quả

Gate IG08 phải có verdict riêng và links evidence theo spec §13. Không PASS từ mock nếu nguồn yêu cầu runtime thật. IG03 chưa có public API thì ghi lớp đã kiểm, mismatch/blocked cho proof API còn thiếu; không thêm feature để né gate.

Tạo `docs/tests/results/phase-08/<test_batch_id>/report.md` và `evidence/`. Ghi C01–C08 + P08-01…P08-07 + case bổ sung; mỗi test có đúng một tag `clean`, `need-change`, `suggestion`, result, expected/actual và evidence. Thống kê đầy đủ, kết luận kỹ thuật theo rule, quyết định Chủ tịch riêng. Dừng tại Phase 08.
