# Kiểm định Phase 11 — Hệ thống công cụ thực thi

> Checklist dự kiến, chưa có kết quả test. AI đọc lại nguồn hiện tại trước mỗi batch; không gắn tag sẵn hay tự nghiệm thu.

[Rule](../RULES.md) · [Điểm vào](../README.md) · [Mẫu report](../templates/report.md) · [Roadmap](../../master-plan.md) · [Spec V1](../../product-spec.md) · [ADR](../../decisions/0001-v1-foundation.md)

## Nguồn và ranh giới

- Phase: 11
- Dependency từ roadmap: 10
- Yêu cầu liên quan: REQ11, REQ13
- Gate: Không có gate IG riêng; vẫn kiểm criteria phase và C01–C08
- Contract hash: cf302a335981079bece7d91eaf985da6108ac4a1b11ed06fd6d20635087c8aa7

Hash đối chiếu scope/demo/criteria/delivery/limits/evidence/dependency tại thời điểm soạn, không bao gồm status/nhật ký. Nguồn đổi thì cập nhật kế hoạch, không sửa report cũ. Snapshot bên dưới giúp traceability; nguồn hiện tại vẫn ưu tiên.

### Phạm vi phải đọc

- Tool registry/schema/version cho files, code, terminal, browser; adapter và capability allowlist.
- Workspace/container sandbox theo task, network egress allowlist, timeout/output caps, artifact/file diff capture.
- Approval trước side effects; receipt/idempotency cho hành động bên ngoài và kết quả chưa xác định.

### Demo bắt buộc

Agent sửa file trong sandbox, chạy test, đọc trang được cho phép; thử path traversal và command ngoài scope.

### Giới hạn phase

Không gửi email/deploy production tự động; không tắt sandbox để vượt test.

### Evidence bàn giao cần đối chiếu

Tool receipts, diff/test log, negative tests về file/network.

## Mapping nghiệm thu → test

Mỗi AC là gạch đầu dòng nghiệm thu roadmap hiện tại khi soạn. Kiểm thêm C01–C08 theo rule; tiêu chí thay đổi cần remap trong report. Mọi case dưới đây bắt buộc trong phạm vi phase; không gọi inference nếu chưa có grant, mà ghi blocked cho case cần run thật.

| Tiêu chí | Kỳ vọng từ roadmap | Test IDs tối thiểu |
| --- | --- | --- |
| AC1 | Không truy file/secret ngoài workspace; network/tool ngoài allowlist bị chặn ở executor. | P11-01, P11-02, P11-03 |
| AC2 | Run thật có diff, test exit code và artifact; redaction không làm mất correlation. | P11-05, P11-06 |
| AC3 | Retry không lặp hành động có side effect khi chưa có kết quả xác định. | P11-04, P11-07 |

## Ca kiểm định riêng của phase

Mỗi dòng là một test phải có record kết quả riêng. Các biến thể negative/race trong dòng ghi sub-results/evidence để không bỏ sót; nếu một biến thể bắt buộc chưa đạt, cả test không clean. C01–C08 cũng phải có record riêng.

| ID | Test | Bước/điều kiện | Kỳ vọng | Evidence cần lưu | Nguồn bổ sung |
| --- | --- | --- | --- | --- | --- |
| P11-01 | Tool schema/capability | Sai args/schema/version, tool chưa allowlist hoặc actor ngoài scope | Deny trước executor; proposals không trực tiếp chạy | Tool contract tests/counters | Spec §6/10 |
| P11-02 | File escape | Traversal/absolute path/symlink root/secret canary trên sandbox test | Không đọc/ghi ngoài root ở executor và artifact access | Negative file tests + hashes | Spec §7/10/12 |
| P11-03 | Network/terminal boundary | Ngoài egress allowlist/command scope; timeout và output cap | Chặn mạng/tool ngoài quyền, limits đúng, sandbox không tắt | Executor/network/exit evidence | Spec §10/11 |
| P11-04 | Approval/receipt/idempotency | Action có approval, unknown/disconnect rồi retry cùng key | Prepared trước dispatch; có receipt, unknown không auto repeat | Action/approval/receipt IDs | Spec §10 |
| P11-05 | Run code thật trong sandbox | Grant mới đúng tools/input scope; sửa file nhỏ, test, đọc trang allowlist | Artifact/diff/test exit thật, trace liên kết run | Diff/log/artifact manifest đã lọc | Spec §3/13 |
| P11-06 | Redaction/correlation | Canary ở args/stdout/stderr/file diff/prompt | Không leak logs/Inspector; IDs/correlation còn đủ | Redaction assertions + ảnh | Spec §9/10 |
| P11-07 | Replay và external denial | Xem lại tool trace; thử external send/deploy không quyền | Replay không chạy lại; send/deploy deny, không thực hiện ngoài môi trường test | Dispatch counts và negative proof | Spec §9/10 |

## Lệnh và điều kiện chạy

Chưa có command runtime được xác minh cho phase này khi soạn. Khi phase được triển khai, đọc manifest/scripts/test source và README hiện tại, chọn lệnh tồn tại, ghi lệnh/exit code vào report; không tự bịa endpoint, cài tool/global hoặc scaffold để chạy checklist.

## Kết luận và lưu kết quả

Tạo `docs/tests/results/phase-11/<test_batch_id>/report.md` và `evidence/`. Ghi C01–C08 + P11-01…P11-07 + case bổ sung; mỗi test có đúng một tag `clean`, `need-change`, `suggestion`, result, expected/actual và evidence. Thống kê đầy đủ, kết luận kỹ thuật theo rule, quyết định Chủ tịch riêng. Dừng tại Phase 11.
