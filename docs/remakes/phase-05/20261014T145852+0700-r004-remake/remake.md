# Remake Phase 05 — 20261014T145852+0700-r004-remake

## Thông tin vòng sửa

- Phase: 05
- Remake batch: 20261014T145852+0700-r004-remake
- Người/AI remake: /root
- Vòng: r004
- Report nguồn: [report độc lập r004](../../../tests/results/phase-05/20261014T144929+0700-r004-test/report.md)
- Bắt đầu / kết thúc: 2026-10-14T14:58:52+07:00 / 2026-10-14T15:01:18+07:00
- Phạm vi/quyền: Check Phase 05 theo AGENTS/RULES, được remake lỗi trong phase; không tự nghiệm thu hoặc mở phase khác.
- Source trước/sau: [source-manifest](evidence/source-manifest.json); source bắt đầu clean ở f74320e2ff20516ec93fbfe3413cfb953695b51d, sau sửa5files.
- Inference: Không gọi; grant thật0. GET metadata không cấp inference.
- Kết luận vòng sửa: Đã thay đổi và cần retest; CG01 vẫn bị chặn bởi proof thiếu.

## Mapping results → thay đổi

| Test ID / tag-result nguồn | Nguyên nhân | Thay đổi thực tế / file refs | Trạng thái xử lý | Test cần rerun |
| --- | --- | --- | --- | --- |
| P05-02 need-change/fail | json.loads(bytes) có thể ném UnicodeDecodeError; endpoint500 | [adapter](../../../../apps/api/src/agent_corporation_api/modules/codex_gateway/adapter.py) normalize parse ValueError/RecursionError thành contract_mismatch; regression UTF8/JSON/nesting | changed | P05-02 + UI error/recovery |
| P05-03 need-change/fail | Profile chỉ regex, thiếu catalog model/effort validation; UI effort thiếu max/ultra/persistent | [profile](../../../../apps/api/src/agent_corporation_api/modules/governance/profile.py) kiểm intersection GET v1/models và GET api/models; primary/fallback phải support effort; offline503 không ghi; [UI](../../../../apps/web/src/RuntimePanel.tsx) đủ effort schema8 và label kiểm catalog | changed | P05-03/04/07: known/unknown model, per-model effort, fallback, offline, stale version/audit |
| P05-06 need-change/blocked | Trusted proof CG01 thiếu hoặc không hợp lệ; chưa đủ evidence isolation/privacy/retention/cancellation | Không tạo proof hoặc mở gate từ metadata giả; giữ missing_or_invalid_proof | blocked | Kiểm gate thật khi có evidence/decision hợp lệ |

## Chi tiết từng finding

### P05-02 — Response encoding và schema

- Expected/actual nguồn: R004 tái hiện probe HTTP500 với UTF8 invalid; expected normalized error không crash.
- Nguyên nhân: Ngoại lệ decoding nằm ngoài catch JSONDecodeError cũ.
- Trạng thái xử lý: changed
- Thay đổi: Chỉ catch ValueError/RecursionError ngay tại json.loads, giữ HTTP status và payload None để map contract_mismatch; lỗi transport vẫn offline. Không trả raw body/error.
- Phản biện: Không có.
- Kiểm tra trong lúc sửa: [37tests](evidence/commands.md), gồm API actual path cho UTF8 invalid, JSON sai và nesting sâu.
- Còn thiếu/blocker: Cần independent retest.
- Retest cần chạy: Original UTF8 repro, normal probe/error mapping, API không500.

### P05-03 — Profile model/effort thực

- Expected/actual nguồn: R004 lưu model ngoài catalog thành công và readback persisted; effort valid gateway bị app từ chối hoặc effort không đúng model vẫn nhận.
- Nguyên nhân: Profile chỉ kiểm cú pháp, effort Literal/UI chưa đồng bộ gateway contract.
- Trạng thái xử lý: changed
- Thay đổi: Explicit profile save đọc metadata gateway qua loopback/no proxy/no redirect/bodylimit hiện có, không inference. Chỉ dùng model trong live catalog có chat_supported và effort tương ứng trong capability snapshot. Cả fallback cùng effort phải hợp lệ. Unknown422, catalog unavailable/malformed503 trước transaction. Không tự probe startup/profile read; entitlement và grant vẫn độc lập. UI schema đủ8efforts; backend quyết định từng model/effort.
- Phản biện: Không có.
- Kiểm tra trong lúc sửa: [commands](evidence/commands.md), [source hashes](evidence/source-manifest.json).
- Còn thiếu/blocker: Independent retest persistence/audit/version trên DB cô lập.
- Retest cần chạy: Knownmodel/max, unsupported model/effort/fallback, offline preservation, CSRF/Owner/staleversion,0POST.

### P05-06 — CG01 evidence

- Expected/actual nguồn: Gate actual allowed=false / missing_or_invalid_proof ở r004; không kết luận source gateway bị exploit.
- Nguyên nhân: Chưa có trusted evidence cho isolation/privacy-retention/cancellation theo contract.
- Trạng thái xử lý: blocked
- Thay đổi: Không sửa proof/gateway/grants; source/runtime guard tiếp tục default deny.
- Phản biện: Không có.
- Kiểm tra trong lúc sửa: Dùng kết quả gate hiện tại ở [r004](../../../tests/results/phase-05/20261014T144929+0700-r004-test/evidence/P05-01-contract-and-gaps.md), không claim rerun hoặc live inference.
- Còn thiếu/blocker: Evidence và quyết định CG01 hợp lệ, đúng fingerprint/endpoint/expiry; inference test nếu có cần grant riêng.
- Retest cần chạy: Gate verification khi điều kiện thật thay đổi.

## Cleanup và bước tiếp theo

- Cleanup: Unit tests chỉ temporary/fake transport, không DB writes; UI QA servers vẫn được điều phối để test tiếp rồi cleanup theo scope.
- Evidence: [commands](evidence/commands.md), [manifest](evidence/source-manifest.json).
- Retest tiếp theo: r005 do AI test độc lập thực hiện sau chốt remake.
- Blocker/giới hạn: Không tự mở CG01 hoặc cấp inference grant; Phase05 vẫn Chờ nghiệm thu.
- Sổ vòng: [Phase05](../../../tests/results/phase-05/README.md).
