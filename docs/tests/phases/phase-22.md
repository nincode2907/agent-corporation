# Kiểm định Phase 22 — Bảo vệ dữ liệu và khôi phục

> Checklist dự kiến, chưa có kết quả test. AI đọc lại nguồn hiện tại trước mỗi batch; không gắn tag sẵn hay tự nghiệm thu.

[Rule](../RULES.md) · [Điểm vào](../README.md) · [Mẫu report](../templates/report.md) · [Roadmap](../../master-plan.md) · [Spec V1](../../product-spec.md) · [ADR](../../decisions/0001-v1-foundation.md)

## Nguồn và ranh giới

- Phase: 22
- Dependency từ roadmap: 21
- Yêu cầu liên quan: REQ22, REQ25
- Gate: Không có gate IG riêng; vẫn kiểm criteria phase và C01–C08
- Contract hash: 589304b9ae140df8580974ad062952b0c686494fb379f880b2f6f33d71252ddc

Hash đối chiếu scope/demo/criteria/delivery/limits/evidence/dependency tại thời điểm soạn, không bao gồm status/nhật ký. Nguồn đổi thì cập nhật kế hoạch, không sửa report cũ. Snapshot bên dưới giúp traceability; nguồn hiện tại vẫn ưu tiên.

### Phạm vi phải đọc

- Audit auth/owner-only, local exposure/CORS, permission/tool escape, secret/log/prompt handling và retention.
- Backup/restore database + artifacts + config refs; secrets xử lý riêng; version-compatible migration/recovery.
- Crash recovery và restore drill có checkpoint/thread reconciliation, không tự replay side effects.

### Demo bắt buộc

Backup môi trường test, làm hỏng dữ liệu, restore vào môi trường sạch và kiểm tra history/ledger/artifacts.

### Giới hạn phase

Không tuyên bố backup tốt chỉ vì tạo được file; không đổi proxy/system service ngoài scope.

### Evidence bàn giao cần đối chiếu

Restore manifest, permission audit và crash/migration drill.

## Mapping nghiệm thu → test

Mỗi AC là gạch đầu dòng nghiệm thu roadmap hiện tại khi soạn. Kiểm thêm C01–C08 theo rule; tiêu chí thay đổi cần remap trong report. Mọi case dưới đây bắt buộc trong phạm vi phase; không gọi inference nếu chưa có grant, mà ghi blocked cho case cần run thật.

| Tiêu chí | Kỳ vọng từ roadmap | Test IDs tối thiểu |
| --- | --- | --- |
| AC1 | Restore drill chứng minh task/evidence/profile/policy còn liên kết; counts/checksums khớp. | P22-03, P22-04, P22-06 |
| AC2 | Bypass quyền và secret test không có lỗi nghiêm trọng chưa xử lý. | P22-01, P22-02, P22-07 |
| AC3 | Migration được kiểm tra trên snapshot phiên bản trước; rollback/recovery constraints ghi rõ. | P22-05 |

## Ca kiểm định riêng của phase

Mỗi dòng là một test phải có record kết quả riêng. Các biến thể negative/race trong dòng ghi sub-results/evidence để không bỏ sót; nếu một biến thể bắt buộc chưa đạt, cả test không clean. C01–C08 cũng phải có record riêng.

| ID | Test | Bước/điều kiện | Kỳ vọng | Evidence cần lưu | Nguồn bổ sung |
| --- | --- | --- | --- | --- | --- |
| P22-01 | Defensive permission suite | Auth/Owner/CORS/Host/Origin/CSRF/tool escape/cross-scope tests trong môi trường test | Không bypass/leak nghiêm trọng chưa xử lý, không nới proxy để pass | Negative API/executor/DB audit | Spec §10/13 |
| P22-02 | Secret/retention boundary | Canary trong prompt/log/artifact/backup và policy deletion preview | Redaction/ACL trước lưu; secrets backup riêng, no silent purge | Redacted audit/manifest assertions | Spec §10/12 |
| P22-03 | Backup manifest | Backup DB/artifacts/config refs test với consistent snapshot/version | Manifest counts/hash/links đủ; file tồn tại chưa đủ proof restore | Backup metadata/manifests | Spec §12 |
| P22-04 | Restore clean environment | Restore sang DB/storage test sạch được cấp, kiểm task/event/profile/policy/ledger/artifact | Counts/checksums/relations khớp, không phụ thuộc nguồn cũ | Restore drill + before/after hashes | Spec §12/13 |
| P22-05 | Migration compatibility | Snapshot phiên bản trước → upgrade → verify, drill recovery theo documented constraints | Không mất evidence/scope, recovery constraints rõ và đã test | Migration/drill reports | Spec §7/12 |
| P22-06 | Stop/checkpoint sau restore | Restore stop-active và unknown model/tool outcomes | Stop giữ, reconcile không replay side effect/inference tự phát | Epoch/checkpoint/call counts | Spec §8/10 |
| P22-07 | Local exposure audit | Đối chiếu listeners/container publishes/proxy/auth với registry hiện tại | Loopback theo quyền, không sửa shared service ngoài scope | Listener/publication/audit metadata | Spec §12 |

## Lệnh và điều kiện chạy

Chưa có command runtime được xác minh cho phase này khi soạn. Khi phase được triển khai, đọc manifest/scripts/test source và README hiện tại, chọn lệnh tồn tại, ghi lệnh/exit code vào report; không tự bịa endpoint, cài tool/global hoặc scaffold để chạy checklist.

## Kết luận và lưu kết quả

Tạo `docs/tests/results/phase-22/<test_batch_id>/report.md` và `evidence/`. Ghi C01–C08 + P22-01…P22-07 + case bổ sung; mỗi test có đúng một tag `clean`, `need-change`, `suggestion`, result, expected/actual và evidence. Thống kê đầy đủ, kết luận kỹ thuật theo rule, quyết định Chủ tịch riêng. Dừng tại Phase 22.
