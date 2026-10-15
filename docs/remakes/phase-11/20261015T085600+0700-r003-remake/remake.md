# Remake Phase 11 — 20261015T085600+0700-r003-remake

## Thông tin vòng sửa

- Phase: 11
- Remake batch: `20261015T085600+0700-r003-remake`
- Người/AI remake: `/root`
- Vòng: r003
- Report nguồn: [test r003](../../../tests/results/phase-11/20261015T085217+0700-r003-test/report.md)
- Bắt đầu: 2026-10-15 08:56:00 +07:00 (Asia/Ho_Chi_Minh)
- Phạm vi/quyền: Sửa redaction JSON escape trong Phase 11; không nối dispatch, không chạy runtime/DB/gateway, không gọi inference.
- Source trước/sau: Worktree dirty; source sau sửa và hash tại [manifest](evidence/source-manifest.json).
- Inference: Không gọi; không dùng grant.
- Kết luận vòng sửa: Đã thay đổi và cần retest độc lập.

## Mapping results → thay đổi

| Test ID / tag-result nguồn | Nguyên nhân | Thay đổi thực tế / file refs | Trạng thái xử lý | Test cần rerun |
| --- | --- | --- | --- | --- |
| [C05 — fail](../../../tests/results/phase-11/20261015T085217+0700-r003-test/report.md#c05--scope-và-dữ-liệu-nhạy-cảm) | Matcher JSON cắt string tại escaped quote, làm sót suffix canary. | Mở rộng quoted-value pattern trong [redaction.py](../../../../apps/api/src/agent_corporation_api/modules/observability/redaction.py) để nhận JSON escapes hoàn chỉnh. | changed | Canary escaped quote/backslash, output JSON validity, redaction regression. |
| [P11-06 — fail](../../../tests/results/phase-11/20261015T085217+0700-r003-test/report.md#p11-06--redactioncorrelation) | Test không có chuỗi JSON credential chứa quote/backslash escape. | Thêm test adapter cho token value `before "quoted" backslash \\ ...`; xác nhận toàn bộ value được che và serialized JSON vẫn hợp lệ. | changed | Độc lập chạy matrix r003, hash/byte_count trên nội dung redacted. |
| C03/C04, P11-01…05, P11-07 — blocked | Phase 10 approval chưa tích hợp executor; Phase 09 lease/retry/recovery chưa đạt; chưa có sandbox/terminal/network/write/artifact/replay runtime hay grant. | Không thay đổi: blocker ngoài phần sửa redaction; registry vẫn chỉ công bố tool read-only. | blocked | Chạy lại sau khi dependency, sandbox và quyền có evidence. |

## Chi tiết từng finding

### C05 / P11-06 — Escaped JSON credential value

- Expected/actual nguồn: r003 ghi nhận `json-escaped-token` suffix còn trong output sau escaped quote; xem [canary evidence](../../../tests/results/phase-11/20261015T085217+0700-r003-test/evidence/P11-06-canary-check.py).
- Nguyên nhân: Regex JSON quoted value dừng tại dấu `"` đã escape.
- Trạng thái xử lý: changed.
- Thay đổi: Pattern nay đọc chuỗi quoted theo cặp escape; thay thế nguyên giá trị bằng JSON string `"[REDACTED]"` để giữ đầu ra JSON hợp lệ. Thêm regression case cho quote/backslash.
- Phản biện: Không có.
- Kiểm tra trong lúc sửa: Lần chạy đầu bắt được lỗi mới: substitution dùng dấu quote escape sai khiến output JSON không hợp lệ; đã sửa replacement và xác nhận lại. `rtk proxy uv run --project apps/api pytest apps/api/tests/test_phase11_tools.py apps/api/tests/test_sensitive_validation.py -q` — 26 passed, 1 deprecation warning; compileall và `rtk git diff --check` exit 0. Xem [commands](evidence/commands.md).
- Còn thiếu/blocker: Chưa có Inspector/log/artifact persistence path để xác minh redaction end-to-end; runtime correlation vẫn blocked.
- Retest cần chạy: Rerun full canary including escaped values, assert canary absent, JSON remains valid, hash and byte_count match redacted output.

## Cleanup và bước tiếp theo

- Cleanup: Chỉ pytest `tmp_path` fixtures; tự dọn sau test.
- Evidence: [source manifest](evidence/source-manifest.json), [commands](evidence/commands.md).
- Retest tiếp theo: r004; tạo report mới trước khi kiểm định source sau sửa.
- Blocker/giới hạn: Approval/worker/sandbox/runtime/grant gaps vẫn mở.
- Sổ vòng: [phase 11 results README](../../../tests/results/phase-11/README.md).
