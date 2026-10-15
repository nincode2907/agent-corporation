# Remake Phase 11 — 20261015T085118+0700-r002-remake

## Thông tin vòng sửa

- Phase: 11
- Remake batch: `20261015T085118+0700-r002-remake`
- Người/AI remake: `/root`
- Vòng: r002
- Report nguồn: [test r002](../../../tests/results/phase-11/20261015T084733+0700-r002-test/report.md)
- Bắt đầu: 2026-10-15 08:51:18 +07:00 (Asia/Ho_Chi_Minh)
- Phạm vi/quyền: Khắc phục finding redaction trong Phase 11; không nối dispatch, không chạy runtime/DB/gateway, không gọi inference.
- Source trước/sau: Worktree dirty, chưa có commit; hash sau sửa trong [manifest](evidence/source-manifest.json).
- Inference: Không gọi; không dùng grant.
- Kết luận vòng sửa: Đã thay đổi và cần retest độc lập.

## Mapping results → thay đổi

| Test ID / tag-result nguồn | Nguyên nhân | Thay đổi thực tế / file refs | Trạng thái xử lý | Test cần rerun |
| --- | --- | --- | --- | --- |
| [C05 — fail](../../../tests/results/phase-11/20261015T084733+0700-r002-test/report.md#c05--scope-và-dữ-liệu-nhạy-cảm) | Quoted JSON secret matcher còn thiếu key phổ biến `token` và `authorization`; text assignment cũng thiếu các nhãn này. | Mở rộng [redaction.py](../../../../apps/api/src/agent_corporation_api/modules/observability/redaction.py) để xử lý quoted/unquoted token, authorization, proxy-authorization, cookie, set-cookie; thêm canary JSON token/authorization qua reader. | changed | Canary variants, metadata hash/byte_count, redaction regression. |
| [P11-06 — fail](../../../tests/results/phase-11/20261015T084733+0700-r002-test/report.md#p11-06--redactioncorrelation) | Hai giá trị JSON vẫn xuất hiện dù các header/cookie, JSON password/api_key/credential/token khác và PEM đã được che. | Thêm JSON `{token, authorization}` fixtures; redaction được áp dụng trước hash/byte_count, test đảm bảo hai giá trị không còn trong output. | changed | Chạy lại toàn bộ canary r002 và kiểm correlation metadata. |
| C03/C04, P11-01…05, P11-07 — blocked | Phase 10 approval chưa tích hợp executor; Phase 09 lease/retry/recovery chưa đạt; chưa có sandbox/terminal/network/write/artifact/replay runtime hay grant. | Không thay đổi: các điều kiện này cần dependency/quyền ngoài phần sửa redaction. | blocked | Chạy lại khi dependency, sandbox và quyền tương ứng có evidence. |

## Chi tiết từng finding

### C05 / P11-06 — JSON token và authorization

- Expected/actual nguồn: r002 cho thấy các canary JSON field `token` và `authorization` vẫn có mặt; hash/kích thước trước đó đã khớp output lọc một phần. Xem [report r002](../../../tests/results/phase-11/20261015T084733+0700-r002-test/report.md) và [canary evidence](../../../tests/results/phase-11/20261015T084733+0700-r002-test/evidence/P11-06-canary-check.py).
- Nguyên nhân: regex cho quoted JSON fields không bao gồm key `token`/`authorization`; assignment text matcher cũng thiếu labels này.
- Trạng thái xử lý: changed.
- Thay đổi: Bổ sung các labels vào quoted JSON và text assignment patterns trong `redact_text`; thêm test qua `WorkspaceReader`/`execute_read_file` cho JSON token/authorization.
- Phản biện: Không có.
- Kiểm tra trong lúc sửa: `rtk proxy uv run --project apps/api pytest apps/api/tests/test_phase11_tools.py apps/api/tests/test_sensitive_validation.py -q` — 25 passed, 1 deprecation warning; compileall và `rtk git diff --check` exit 0. Xem [commands](evidence/commands.md). Chưa phải independent retest.
- Còn thiếu/blocker: Kết quả live Inspector/log/artifact chưa kiểm chứng vì executor chưa được tích hợp.
- Retest cần chạy: Retest độc lập toàn bộ canary matrix, bảo đảm `token`/`authorization` không rò; hash và byte count phải phản ánh output đã redacted.

## Cleanup và bước tiếp theo

- Cleanup: Chỉ pytest `tmp_path` fixtures, tự dọn sau test.
- Evidence: [source manifest](evidence/source-manifest.json), [commands](evidence/commands.md).
- Retest tiếp theo: r003; tạo batch report mới cho source sau remake.
- Blocker/giới hạn: Approval/worker/sandbox/runtime/grant gaps vẫn mở; không tự mở phase khác.
- Sổ vòng: [phase 11 results README](../../../tests/results/phase-11/README.md).
