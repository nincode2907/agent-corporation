# Remake Phase 05 — 20261009T110817+0700-r002-remake

## Thông tin vòng sửa

- Phase: 05
- Remake batch: 20261009T110817+0700-r002-remake
- Người/AI remake: Codex `/root`
- Vòng: r002
- Report nguồn: [Phase 05 r002 test](../../../tests/results/phase-05/20261008T165952+0700-r002-test/report.md)
- Bắt đầu / kết thúc: 2026-10-09T11:08:17+07:00 / 2026-10-09T11:10:30+07:00
- Phạm vi/quyền: Chỉ xử lý findings Phase 05 của report r002; không sửa gateway/server hoặc dịch vụ dùng chung, không vượt dependency, không inference.
- Source trước/sau: Worktree có thay đổi sẵn của Chủ tịch và các lượt trước; không thay đổi source sản phẩm trong remake này. Xem [manifest](evidence/source-manifest.json).
- Inference: Không gọi; grant = 0 và không kế thừa grant từ batch trước.
- Kết luận vòng sửa: Bị chặn — findings còn lại cần dependency, capability hoặc quyết định nằm ngoài quyền remake hiện tại; không có sửa source sản phẩm phù hợp trong scope.

## Mapping results → thay đổi

| Test ID / tag-result nguồn | Nguyên nhân | Thay đổi thực tế / file refs | Trạng thái xử lý | Test cần rerun |
| --- | --- | --- | --- | --- |
| [P05-01 — need-change/blocked](../../../tests/results/phase-05/20261008T165952+0700-r002-test/report.md#p05-01--contract-và-live-probe) | Gateway local offline; API process đang chạy chưa nạp route mới; report không có live health/models response. | Không restart API/gateway dùng chung. Điều kiện và evidence hiện có: [bằng chứng Phase 05](../../../../evidence/phase-05.md). | blocked | Khi gateway hoạt động và API build mới được vận hành trong cửa sổ cho phép: GET health/models, xác nhận contract/auth/catalog; giữ probe read-only. |
| [P05-03 — need-change/blocked](../../../tests/results/phase-05/20261008T165952+0700-r002-test/report.md#p05-03--catalog-entitlement-và-profile) | API chưa có authenticated Owner identity; catalog không phải entitlement. | Không tạo Owner/profile giả hoặc quyền từ UI. | blocked | Sau khi identity/authorization được triển khai và dependency được nghiệm thu: test model/effort validation với principal Owner thật và catalog unsupported. |
| [P05-04 — need-change/blocked](../../../tests/results/phase-05/20261008T165952+0700-r002-test/report.md#p05-04--owner-only-profile) | Chưa có auth middleware/principal để chứng minh deny-agent và Owner audit/version. | Không thêm endpoint ghi giả bảo mật. | blocked | Khi có identity/auth backend được duyệt: negative agent access, Owner update/audit/version và secret non-exposure. |
| [P05-05 — need-change/blocked](../../../tests/results/phase-05/20261008T165952+0700-r002-test/report.md#p05-05--429-queue-và-fallback-allowlist) | Chưa có durable queue hoặc Owner-managed fallback allowlist; adapter hiện chỉ trả rate_limited. | Không thêm queue RAM, retry vô hạn hoặc fallback policy giả. | blocked | Khi persistence/orchestration và Owner policy có scope được duyệt: bounded backoff/attempts, allowlist enforcement, restart/resume và side-effect checks. |
| [P05-06 — need-change/blocked](../../../tests/results/phase-05/20261008T165952+0700-r002-test/report.md#p05-06--cg01-isolationprivacy) | Chưa có proof isolation/read boundary và retention; gateway read-only có thể đọc file máy, thread/rollout có thể lưu prompt. | Không gửi prompt/input, không đổi gateway; giữ gate CG01 ở trạng thái blocked. | blocked | Chỉ review/test capability sau proof hoặc quyết định CG01 phù hợp; mọi inference test cần grant mới ghi rõ phase, batch, purpose, limits và expiry. |

## Chi tiết từng finding

### P05-01 — Live gateway probe

- Expected/actual nguồn: Contract matrix kèm health/models live response đã lọc; thực tế gateway `127.0.0.1:4000` offline, app process cũ trả 404 cho route probe.
- Nguyên nhân: Dịch vụ cần kiểm chứng không hoạt động trong môi trường hiện tại; không phải lỗi có thể sửa an toàn bằng thay đổi adapter.
- Trạng thái xử lý: blocked.
- Thay đổi: Không đổi source hoặc cấu hình dịch vụ; lưu lại yêu cầu vận hành theo [report nguồn](../../../tests/results/phase-05/20261008T165952+0700-r002-test/report.md).
- Phản biện: Không có.
- Kiểm tra trong lúc sửa: API 9 tests pass; web lint/build pass; không gọi dịch vụ live hay inference.
- Còn thiếu/blocker: Gateway phải sẵn sàng và route build mới phải được chạy trong cửa sổ được phép; xác minh lại gateway không cần inference.
- Retest cần chạy: P05-01 và P05-02 trên API mới cùng gateway live; không restart process dùng chung nếu chưa được cho phép.

### P05-03/P05-04 — Owner model profile và authorization

- Expected/actual nguồn: Agent bị từ chối; Owner xác thực mới được cấu hình model/profile và có audit/version. API hiện không có authenticated identity.
- Nguyên nhân: Authorization nền tảng chưa tồn tại; tự nhận diện Owner ở UI hoặc thêm route ghi sẽ tạo cảm giác bảo mật sai.
- Trạng thái xử lý: blocked.
- Thay đổi: Không thêm giả lập quyền hoặc endpoint.
- Phản biện: Không có; blocker phù hợp với tiêu chí Owner-only bắt buộc.
- Kiểm tra trong lúc sửa: Đối chiếu report r002, checklist Phase 05 và module/API hiện có; không có source auth/principal đáng tin.
- Còn thiếu/blocker: Dependency/decision về identity và authorization cùng implementation có thể kiểm chứng.
- Retest cần chạy: Kiểm tra deny-agent, Owner update/audit/version và secret redaction khi dependency sẵn sàng.

### P05-05 — Durable queue và fallback

- Expected/actual nguồn: Requeue/backoff bounded, fallback chỉ theo allowlist Owner; hiện adapter chỉ báo rate_limited và không retry.
- Nguyên nhân: Chưa có persistence/orchestration và policy Owner trong source hiện tại.
- Trạng thái xử lý: blocked.
- Thay đổi: Không tạo queue tạm trong RAM hoặc retry side effect chưa xác định.
- Phản biện: Không có.
- Kiểm tra trong lúc sửa: Chạy lại regression backend; không phát sinh model request.
- Còn thiếu/blocker: Durable queue, allowlist và contract retry/resume được giao/duyệt đúng phase.
- Retest cần chạy: Test 429 bounded attempts, fallback allow/deny, restart/resume và idempotency.

### P05-06 — CG01 isolation/privacy

- Expected/actual nguồn: Cần proof isolation, read boundary và retention trước khi gửi input; report r002 xác nhận chưa có proof.
- Nguyên nhân: Gateway chung có thể đọc file trong read-only mode và lưu thread/rollout; chưa có quyết định/capability để vượt gate.
- Trạng thái xử lý: blocked.
- Thay đổi: Không gửi prompt/input, không nới quyền, không đổi gateway hoặc proxy.
- Phản biện: Không có.
- Kiểm tra trong lúc sửa: Chỉ đọc evidence/report đã lọc; không gọi gateway.
- Còn thiếu/blocker: Proof hoặc quyết định CG01. Inference grant phải được cấp riêng cho đúng batch và mục đích nếu một đợt sau cần inference.
- Retest cần chạy: Review proof trước; chỉ thực hiện test phù hợp với grant mới nếu có.

## Cleanup và bước tiếp theo

- Cleanup: Không có process/service restart, DB writes, queue writes, session hoặc inference.
- Evidence: [manifest](evidence/source-manifest.json), [commands](evidence/commands.md), [report nguồn](../../../tests/results/phase-05/20261008T165952+0700-r002-test/report.md).
- Retest tiếp theo: r003 bởi AI độc lập; chưa tạo report retest.
- Blocker/giới hạn: Dependency Phase 04, Owner identity/auth, durable queue/policy và CG01 vẫn mở. Phase 05 vẫn Chờ nghiệm thu; không tự bắt đầu Phase 06.
- Sổ vòng: [Phase 05 rounds](../../../tests/results/phase-05/README.md).
