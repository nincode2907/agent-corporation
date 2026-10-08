# Remake Phase 05 — 20261008T165817+0700-r001-remake

## Thông tin vòng sửa

- Phase: 05
- Remake batch: 20261008T165817+0700-r001-remake
- Vòng: r001
- Report nguồn: [r001 test](../../../tests/results/phase-05/20261008T165432+0700-r001-test/report.md)
- Bắt đầu / kết thúc: 2026-10-08T16:58:17+07:00 / 2026-10-08T17:01:20+07:00
- Phạm vi/quyền: Chỉ remediation finding Phase 05 theo yêu cầu “làm lại test rồi tiếp phase 6”; không restart shared services, không thay gateway, không inference.
- Source trước/sau: Worktree dirty, giữ nguyên các thay đổi Chủ tịch; [manifest trước remake](evidence/source-manifest.json).
- Inference: Không gọi; grant Phase 05 = 0, không kế thừa grant.
- Kết luận vòng sửa: Đã thay đổi hai finding có thể sửa trong scope; blockers cần runtime/identity/queue/isolation giữ nguyên và chuyển sang retest với trạng thái blocked.

## Mapping results → thay đổi

| Test ID / tag-result nguồn | Nguyên nhân | Thay đổi thực tế / file refs | Trạng thái xử lý | Test cần rerun |
| --- | --- | --- | --- | --- |
| [C02 — need-change/fail](../../../tests/results/phase-05/20261008T165432+0700-r001-test/report.md#c02--dependency-và-nguồn-trạng-thái) | Root AGENTS nói Phase 04 đang triển khai, khác trạng thái chuẩn Chờ nghiệm thu trong master-plan. | Đồng bộ đúng một câu trạng thái trong [AGENTS.md](../../../../AGENTS.md); không đổi roadmap/status. | changed | C02 và C06 |
| [C03 — need-change/fail](../../../tests/results/phase-05/20261008T165432+0700-r001-test/report.md#c03--tiêu-chí-và-demo) | UI ép kiểu JSON không kiểm tra HTTP status/schema rồi render `.models.length`. | [App.tsx](../../../../apps/web/src/App.tsx) kiểm `response.ok`, schema từng field, malformed JSON và fallback contract error. | changed | C03, C06, P05-02, build/lint |
| [C06 — need-change/fail](../../../tests/results/phase-05/20261008T165432+0700-r001-test/report.md#c06--tài-liệu-và-bản-nhìn) | Exception render làm trắng toàn trang khi API 404. | Cùng thay đổi UI như C03; retest browser trên API process hiện có, không restart. | changed | C06, P05-02, console/error state |
| [P05-01 — need-change/blocked](../../../tests/results/phase-05/20261008T165432+0700-r001-test/report.md#p05-01--contract-và-live-probe) | Gateway 4000 offline; API process chưa nạp route mới. | Không restart gateway/API dùng chung trong phạm vi này. | blocked | P05-01 khi có cửa sổ vận hành được phép |
| [P05-02 — need-change/fail](../../../tests/results/phase-05/20261008T165432+0700-r001-test/report.md#p05-02--offlineauthschema-mismatch) | HTTP non-2xx không được phân biệt với GatewayProbe hợp lệ. | Sửa status/schema guard và thông báo an toàn trong App.tsx. | changed | P05-02 với HTTP 404 thực và fake schema tests |
| [P05-03 — need-change/blocked](../../../tests/results/phase-05/20261008T165432+0700-r001-test/report.md#p05-03--catalog-entitlement-và-profile), [P05-04 — need-change/blocked](../../../tests/results/phase-05/20261008T165432+0700-r001-test/report.md#p05-04--owner-only-profile) | Không có danh tính Owner xác thực, nên không thể chứng minh quyền ghi profile. | Không dựng quyền giả hoặc endpoint ghi không xác thực. | blocked | Sau khi có identity/authorization được duyệt |
| [P05-05 — need-change/blocked](../../../tests/results/phase-05/20261008T165432+0700-r001-test/report.md#p05-05--429-queue-và-fallback-allowlist) | Durable queue và Owner fallback allowlist chưa có. | Không thêm retry/fallback RAM hoặc policy giả. | blocked | Khi capability/persistence thuộc phase được giao |
| [P05-06 — need-change/blocked](../../../tests/results/phase-05/20261008T165432+0700-r001-test/report.md#p05-06--cg01-isolationprivacy) | `read-only` không chứng minh read isolation; retention prompt gateway chưa được xác nhận. | Không gửi input và không thay đổi codex-server dùng chung. | blocked | Chỉ sau proof CG01/decision gate và grant độc lập nếu có inference |

## Chi tiết từng finding

### C02 — Nguồn trạng thái dependency

- Expected/actual nguồn: AGENTS phải nhất quán với nguồn chuẩn; report r001 ghi mismatch Phase 04.
- Nguyên nhân: Một câu chỉ thị cũ không được đồng bộ sau khi master-plan chuyển Phase 04 sang Chờ nghiệm thu.
- Thay đổi: Chỉ đồng bộ status sentence trong AGENTS; các nội dung mới khác của Chủ tịch không bị thay.
- Kiểm tra trong lúc sửa: `rtk proxy git diff --check` pass; C02 được đối chiếu lại ở report r002.
- Còn thiếu/blocker: Phase 04 vẫn chờ nghiệm thu; đây là trạng thái dependency, không phải lỗi nội dung.
- Retest cần chạy: So sánh AGENTS/master-plan summary và phase detail.

### C03/C06/P05-02 — Contract error không làm hỏng Settings

- Expected/actual nguồn: HTTP 404 và malformed/non-contract JSON phải hiện lỗi có thể hiểu được, không crash.
- Nguyên nhân: `response.json()` được ép kiểu compile-time; không có kiểm tra HTTP status hoặc payload runtime.
- Thay đổi: `isGatewayProbe` xác thực enum/status, string fields, models, booleans và invariant `entitlement_verified === false`; API non-2xx và JSON lỗi trở thành contract error an toàn; network failure vẫn hiển thị offline.
- Kiểm tra trong lúc sửa: Web lint/build và diff check pass. Browser click Probe gateway trước API HTTP 404 hiển thị “Contract/cấu hình cần kiểm tra” và “API probe không khả dụng (HTTP 404)”; cây accessibility vẫn có Settings và không có runtime error được quan sát.
- Còn thiếu/blocker: Không có API process đã nạp route mới để thử happy-path live; adapter fake tests cover backend contract.
- Retest cần chạy: HTTP 404 thực sau sửa, fake adapter errors, build/lint.

### P05-01/P05-03/P05-04/P05-05/P05-06 — Blockers ngoài scope/quyền

- Expected/actual nguồn: Live gateway, Owner-only profile, queue/fallback và CG01 đều chưa đủ bằng chứng.
- Nguyên nhân: Dịch vụ/identity/capability hoặc dependency không tồn tại trong trạng thái hiện tại.
- Thay đổi: Không có; không restart server dùng chung, không tạo auth giả, không tự thêm queue/policy hoặc gửi dữ liệu.
- Kiểm tra trong lúc sửa: Read-only probe trước đó ghi gateway offline; test mới chỉ xác minh phần UI/error contract.
- Còn thiếu/blocker: Gateway/API được vận hành trong cửa sổ phù hợp; Owner auth/queue; isolation/read boundary/retention proof và quyết định/gate. Inference grant mới phải chỉ rõ phase, batch, mục đích, hạn mức, expiry.
- Retest cần chạy: Khi điều kiện bên ngoài được đáp ứng; grant không kế thừa.

## Cleanup và bước tiếp theo

- Cleanup: Không có DB writes, session hay process restart; không có inference.
- Evidence: [manifest](evidence/source-manifest.json), [commands](evidence/commands.md), report nguồn r001.
- Retest tiếp theo: [sổ Phase 05](../../../tests/results/phase-05/README.md) sẽ liên kết r002 khi report tồn tại.
- Blocker/giới hạn: Các finding blocked ở trên không được coi là đóng chỉ vì code UI pass.
- Sổ vòng: [Phase 05 rounds](../../../tests/results/phase-05/README.md).
