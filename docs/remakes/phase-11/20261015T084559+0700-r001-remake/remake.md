# Remake Phase 11 — 20261015T084559+0700-r001-remake

## Thông tin vòng sửa

- Phase: 11
- Remake batch: `20261015T084559+0700-r001-remake`
- Người/AI remake: `/root`
- Vòng: r001
- Report nguồn: [test r001](../../../tests/results/phase-11/20261015T084213+0700-r001-test/report.md)
- Bắt đầu / kết thúc: 2026-10-15 08:45:45–08:45:59 +07:00 (Asia/Ho_Chi_Minh)
- Phạm vi/quyền: Khắc phục các finding Phase 11 có thể sửa trong code hiện tại; không thêm dispatch, không chạy runtime/DB/gateway, không gọi inference.
- Source trước/sau: Worktree dirty, chưa có commit; sau sửa có hash trong [manifest](evidence/source-manifest.json).
- Inference: Không gọi; không dùng grant.
- Kết luận vòng sửa: Đã thay đổi và cần retest độc lập.

## Mapping results → thay đổi

| Test ID / tag-result nguồn | Nguyên nhân | Thay đổi thực tế / file refs | Trạng thái xử lý | Test cần rerun |
| --- | --- | --- | --- | --- |
| [C05 — fail](../../../tests/results/phase-11/20261015T084213+0700-r001-test/report.md#c05--scope-và-dữ-liệu-nhạy-cảm) | Bộ lọc text không che Authorization/cookie; phạm vi module reader dùng `redact_text` trực tiếp. | Mở rộng [redaction.py](../../../../apps/api/src/agent_corporation_api/modules/observability/redaction.py) cho authorization headers, cookie headers/assignments, credential fields dạng JSON và private-key blocks. | changed | Canary variants, output adapter, full redaction regression. |
| [P11-06 — fail](../../../tests/results/phase-11/20261015T084213+0700-r001-test/report.md#p11-06--redactioncorrelation) | Chưa bao phủ credential labels/format variants và nhiều dòng. | Thêm test đọc file qua tool adapter cho Basic/Bearer Authorization, Cookie/Set-Cookie, JSON credentials và PEM private key; xác nhận canary bị che, hash/kích thước vẫn được tạo trên output đã lọc. | changed | P11-06 toàn bộ biến thể và kiểm correlation metadata. |
| C02/C03/C04, P11-01…05, P11-07 — blocked | Phase 10 approval chưa tích hợp executor; Phase 09 lease/retry/recovery chưa đạt; chưa có sandbox/terminal/network/write/artifact/replay runtime hay grant. | Không thay đổi: dependency/quyền ngoài lát code độc lập này; giữ tool registry chỉ có reader read-only. | blocked | Chạy lại khi dependency, sandbox và quyền tương ứng có bằng chứng. |

## Chi tiết từng finding

### C05 / P11-06 — Redaction canary

- Expected/actual nguồn: Canary `Authorization: Basic ...` và `cookie=...` còn nguyên trong output; xem [P11-06 evidence](../../../tests/results/phase-11/20261015T084213+0700-r001-test/evidence/P11-06-redaction.md).
- Nguyên nhân: `redact_text` chỉ nhận một số bearer/password/token labels và không xử lý authorization/cookie headers hoặc quoted JSON values/private key blocks.
- Trạng thái xử lý: changed.
- Thay đổi: Redaction giờ xử lý `Authorization`, `Proxy-Authorization`, `Cookie`, `Set-Cookie`, JSON credential assignments và private-key PEM blocks trước regex secret assignment hiện có. Test mở rộng qua `WorkspaceReader`/`execute_read_file` với canary giả.
- Phản biện: Không có.
- Kiểm tra trong lúc sửa: `rtk proxy uv run --project apps/api pytest apps/api/tests/test_phase11_tools.py apps/api/tests/test_sensitive_validation.py -q` — 24 passed, 1 deprecation warning; compileall và `rtk git diff --check` exit 0. Chi tiết ở [commands](evidence/commands.md). Đây chưa phải kết luận independent retest.
- Còn thiếu/blocker: Chưa có log/Inspector/artifact path để xác minh mọi lớp persistence; P11-06 correlation end-to-end vẫn blocked.
- Retest cần chạy: Independent test trên các canary được bổ sung, bảo đảm hash/kích thước tính từ output đã redacted; chạy regression redaction.

## Cleanup và bước tiếp theo

- Cleanup: Chỉ pytest `tmp_path` fixtures; đã tự dọn khi pytest kết thúc.
- Evidence: [source manifest](evidence/source-manifest.json), [commands](evidence/commands.md), diff hiện hành.
- Retest tiếp theo: r002; tạo report batch mới trước khi kiểm định source mới.
- Blocker/giới hạn: Approval/worker/sandbox/runtime/grant gaps nêu trong report nguồn vẫn mở; không tự mở phase khác.
- Sổ vòng: [phase 11 results README](../../../tests/results/phase-11/README.md).
