# Kiểm định Phase 04 — Nhà máy công ty demo

> Checklist dự kiến, chưa có kết quả test. AI đọc lại nguồn hiện tại trước mỗi batch; không gắn tag sẵn hay tự nghiệm thu.

[Rule](../RULES.md) · [Điểm vào](../README.md) · [Mẫu report](../templates/report.md) · [Roadmap](../../master-plan.md) · [Spec V1](../../product-spec.md) · [ADR](../../decisions/0001-v1-foundation.md)

## Nguồn và ranh giới

- Phase: 04
- Dependency từ roadmap: 03
- Yêu cầu liên quan: REQ02
- Gate: Không có gate IG riêng; vẫn kiểm criteria phase và C01–C08
- Contract hash: fa0692d4481c0e1af2db3f0fcad2138740025526cb948f3a6112937dc751b29f

Hash đối chiếu scope/demo/criteria/delivery/limits/evidence/dependency tại thời điểm soạn, không bao gồm status/nhật ký. Nguồn đổi thì cập nhật kế hoạch, không sửa report cũ. Snapshot bên dưới giúp traceability; nguồn hiện tại vẫn ưu tiên.

### Phạm vi phải đọc

- Sinh công ty giả, phòng ban, nhân viên version hóa và event fixture deterministic.
- Tách demo/benchmark/real bằng khóa môi trường, storage paths và thread namespaces; real còn trống.
- Dataset cho idle/running/waiting/failed, approvals, lỗi, retry và usage chưa biết.

### Demo bắt buộc

Reset demo hai lần, đối chiếu dataset ổn định và một bản ghi real thử nghiệm không thay đổi.

### Giới hạn phase

Không thành lập tập đoàn thật của người dùng.

### Evidence bàn giao cần đối chiếu

Seed manifest, kiểm tra reset/isolation và ảnh nhãn demo.

## Mapping nghiệm thu → test

Mỗi AC là gạch đầu dòng nghiệm thu roadmap hiện tại khi soạn. Kiểm thêm C01–C08 theo rule; tiêu chí thay đổi cần remap trong report. Mọi case dưới đây bắt buộc trong phạm vi phase; không gọi inference nếu chưa có grant, mà ghi blocked cho case cần run thật.

| Tiêu chí | Kỳ vọng từ roadmap | Test IDs tối thiểu |
| --- | --- | --- |
| AC1 | Fixture có seed/version; không gọi model khi seed/reset. | P04-01, P04-07 |
| AC2 | Reset không xóa artifacts, ledger hoặc thread của môi trường khác. | P04-02, P04-03, P04-04 |
| AC3 | Dashboard/Inspector/finance không trộn demo vào báo cáo real. | P04-05, P04-06 |

## Ca kiểm định riêng của phase

Mỗi dòng là một test phải có record kết quả riêng. Các biến thể negative/race trong dòng ghi sub-results/evidence để không bỏ sót; nếu một biến thể bắt buộc chưa đạt, cả test không clean. C01–C08 cũng phải có record riêng.

| ID | Test | Bước/điều kiện | Kỳ vọng | Evidence cần lưu | Nguồn bổ sung |
| --- | --- | --- | --- | --- | --- |
| P04-01 | Seed deterministic | Seed cùng version/seed ở môi trường demo test hai lần | Dataset ổn định, manifest seed/version và IDs mapping tái lập | Seed manifests/count/hash | Spec §12 |
| P04-02 | Reset lặp an toàn | Reset demo hai lần trong test scope với quyền đúng | Dataset về baseline; không duplicate/corrupt links | Before/after manifests và reset receipts | Spec §12 |
| P04-03 | Isolation đầy đủ | Đặt canary record/artifact/ledger/thread namespace ngoài demo reset scope | Không ảnh hưởng benchmark/real test; không gateway session cleanup | Scoped counts/hashes/thread metadata | Spec §7/12 |
| P04-04 | Deny reset sai scope | Gửi reset target real/benchmark hoặc scope khác qua backend | Deny trước delete/file action; không chỉ UI confirmation | Negative request/DB/storage diff | Spec §10/12 |
| P04-05 | Nhãn demo/report filters | Mở Dashboard/Inspector/finance với dataset và environment filters | Mọi dữ liệu demo có nhãn; không lẫn KPI real | Ảnh + query/ref mapping | Spec §3/12 |
| P04-06 | States và unknown fixture | Đọc fixture idle/running/waiting/failed/approval/retry/unknown | Đúng contract, không bịa usage=0 hay trạng thái active thật | Fixture manifest và UI assertions | Spec §8/9/11 |
| P04-07 | Không inference/real company | Spy model dispatch khi seed/reset/mở trang | 0 model requests; real company người dùng vẫn chưa tạo | Call counts và scoped DB proof | Spec §2/10/12 |

## Lệnh và điều kiện chạy

Chưa có command runtime được xác minh cho phase này khi soạn. Khi phase được triển khai, đọc manifest/scripts/test source và README hiện tại, chọn lệnh tồn tại, ghi lệnh/exit code vào report; không tự bịa endpoint, cài tool/global hoặc scaffold để chạy checklist.

## Kết luận và lưu kết quả

Tạo `docs/tests/results/phase-04/<test_batch_id>/report.md` và `evidence/`. Ghi C01–C08 + P04-01…P04-07 + case bổ sung; mỗi test có đúng một tag `clean`, `need-change`, `suggestion`, result, expected/actual và evidence. Thống kê đầy đủ, kết luận kỹ thuật theo rule, quyết định Chủ tịch riêng. Tiếp tục remake/retest theo RULES.md khi còn need-change giải quyết được trong Phase 04; không tự chuyển phase. Nếu chỉ được giao test không sửa hoặc gặp blocker thật, lưu kết quả và điều kiện tiếp tục.
