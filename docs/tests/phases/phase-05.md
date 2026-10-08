# Kiểm định Phase 05 — Kết nối Codex server local

> Checklist dự kiến, chưa có kết quả test. AI đọc lại nguồn hiện tại trước mỗi batch; không gắn tag sẵn hay tự nghiệm thu.

[Rule](../RULES.md) · [Điểm vào](../README.md) · [Mẫu report](../templates/report.md) · [Roadmap](../../master-plan.md) · [Spec V1](../../product-spec.md) · [ADR](../../decisions/0001-v1-foundation.md)

## Nguồn và ranh giới

- Phase: 05
- Dependency từ roadmap: 03, 04
- Yêu cầu liên quan: REQ09
- Gate: Không có gate IG riêng; vẫn kiểm criteria phase và C01–C08
- Contract hash: 656bd9aaafb8d5dc876c07be155da25173d53b2c7101287b88dff4809156c80e

Hash đối chiếu scope/demo/criteria/delivery/limits/evidence/dependency tại thời điểm soạn, không bao gồm status/nhật ký. Nguồn đổi thì cập nhật kế hoạch, không sửa report cũ. Snapshot bên dưới giúp traceability; nguồn hiện tại vẫn ưu tiên.

### Phạm vi phải đọc

- Adapter HTTP tới codex-server hiện có; base URL cấu hình, contract/capability probe, auth ref và secret redaction.
- Tách role/persona, model/tools/skills, policy; xác thực lựa chọn model thực thay vì hardcode nhãn GPT-6.1 Sol High.
- Health/auth status, profile config tối thiểu, owner-only model config; adapter giả cho lỗi và test miễn phí.

### Demo bắt buộc

GET health/models không inference; mô phỏng server offline, 401 và schema/capability mismatch.

### Giới hạn phase

Chưa bắt đầu turn có inference; nếu dùng gateway khác phải chốt adapter riêng.

### Evidence bàn giao cần đối chiếu

Contract/schema, health/models responses đã lọc, lỗi probe và profile snapshot.

## Mapping nghiệm thu → test

Mỗi AC là gạch đầu dòng nghiệm thu roadmap hiện tại khi soạn. Kiểm thêm C01–C08 theo rule; tiêu chí thay đổi cần remap trong report. Mọi case dưới đây bắt buộc trong phạm vi phase; không gọi inference nếu chưa có grant, mà ghi blocked cho case cần run thật.

| Tiêu chí | Kỳ vọng từ roadmap | Test IDs tối thiểu |
| --- | --- | --- |
| AC1 | Health/models API hoạt động; contract từ source gateway được xác nhận, không log token hay đưa secret ra UI. | P05-01, P05-02, P05-04 |
| AC2 | Catalog model không chứng minh entitlement; lượt chạy thật kiểm tra ở Phase 06. | P05-03, P05-07 |
| AC3 | Không đổi cấu hình server chung; fallback chỉ trong danh sách đã được Chủ tịch duyệt; 429 được đưa lại queue. | P05-05, P05-06 |

## Ca kiểm định riêng của phase

Mỗi dòng là một test phải có record kết quả riêng. Các biến thể negative/race trong dòng ghi sub-results/evidence để không bỏ sót; nếu một biến thể bắt buộc chưa đạt, cả test không clean. C01–C08 cũng phải có record riêng.

| ID | Test | Bước/điều kiện | Kỳ vọng | Evidence cần lưu | Nguồn bổ sung |
| --- | --- | --- | --- | --- | --- |
| P05-01 | Source contract/probe | Đọc gateway README/server/schema/provider và GET health/models đã lọc | Capability matrix theo source/hash/time; không streaming/max_tokens giả | Source hashes + HTTP probe | Spec §6 |
| P05-02 | Offline/auth/schema mismatch | Fake adapter timeout/offline/401/schema mismatch | Trạng thái và cách khắc phục đúng; không log token | Contract tests và UI error evidence | Spec §6/10 |
| P05-03 | Model catalog/entitlement | Cấu hình supported/unsupported model và effort theo Owner | Catalog không chứng minh entitlement; không live POST ở phase này | Profile snapshot + validation cases | Spec §6/10 |
| P05-04 | Owner-only profile | Thử đổi model/config bằng actor agent và Owner test identity | Agent bị deny, Owner audit/version; frontend không giữ gateway secret | API/service deny và audit | Spec §10 |
| P05-05 | 429/fallback | Fake 429/session conflict/timeout với adapter theo contract | Queue/backoff có giới hạn, fallback chỉ allowlist Owner; unknown không auto retry | Fake transport trace/attempt counts | Spec §6/11 |
| P05-06 | CG01 capability/privacy | Review isolation/retention/input boundary được yêu cầu | Thiếu capability bắt buộc → blocked + gap report, không sửa gateway shared | Capability/gap report, decision refs | Spec §6 |
| P05-07 | Không inference từ probe | Spy startup/health/models/profile view | 0 POST inference, không tạo session/run thật tự động | Request log đã lọc/counters | Spec §6/10 |

## Lệnh và điều kiện chạy

Chưa có command runtime được xác minh cho phase này khi soạn. Khi phase được triển khai, đọc manifest/scripts/test source và README hiện tại, chọn lệnh tồn tại, ghi lệnh/exit code vào report; không tự bịa endpoint, cài tool/global hoặc scaffold để chạy checklist.

## Kết luận và lưu kết quả

Tạo `docs/tests/results/phase-05/<test_batch_id>/report.md` và `evidence/`. Ghi C01–C08 + P05-01…P05-07 + case bổ sung; mỗi test có đúng một tag `clean`, `need-change`, `suggestion`, result, expected/actual và evidence. Thống kê đầy đủ, kết luận kỹ thuật theo rule, quyết định Chủ tịch riêng. Dừng tại Phase 05.
