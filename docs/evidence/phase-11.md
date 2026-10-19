# Bằng chứng triển khai Phase 11 — 15/10/2026

> Trạng thái: đang triển khai, chưa nghiệm thu. Phase 10 chưa tích hợp approval với executor; Phase 09 còn thiếu lease/recovery/retry. Không có sandbox runtime hoặc inference grant.

## Đã thêm

- `modules/tools/registry.py`: tool contract có tên, schema version, capability và side-effect metadata. Registry hiện chỉ công bố `workspace.read_file` v1; unknown tool, sai version/schema và capability không có đều deny. Validator không dispatch và không tự quyết định quyền.
- `modules/tools/workspace.py`: reader read-only nhận root từ caller tin cậy, dùng `dir_fd` + `O_NOFOLLOW`, chặn absolute/traversal/symlink và special file; giới hạn output 64 KiB mặc định, chỉ nhận UTF-8, không lộ host path/error. Reader không phải OS sandbox và không chạy lệnh.
- `observability/redaction.py`: lọc Authorization/Proxy-Authorization, Cookie/Set-Cookie, các credential fields dạng JSON/text, private-key PEM và string JSON có escape trước khi trả output.
- `test_phase11_tools.py`: coverage cho registry/version/capability, traversal, absolute path, symlink escape/parent, size cap, binary/special file, redaction canaries và metadata.

## Kiểm tra và pipeline độc lập

- `rtk proxy uv run --project apps/api pytest apps/api/tests/test_phase11_tools.py apps/api/tests/test_sensitive_validation.py -q` — 26 passed; một warning deprecation Starlette/httpx.
- `rtk proxy python3 -m compileall -q apps/api/src/agent_corporation_api/modules/tools apps/api/src/agent_corporation_api/modules/observability/redaction.py apps/api/tests/test_phase11_tools.py` — pass.
- `rtk git diff --check` — pass.
- AI tester độc lập r004: 6 clean, 9 blocked, không fail. Full credential canary matrix, gồm JSON escaped quote/backslash, không còn leak trong reader; JSON output hợp lệ; SHA-256 và byte_count khớp output đã redacted. [Report và evidence](../tests/results/phase-11/20261015T085652+0700-r004-test/report.md).
- Ba remake và lịch sử các report trước được lưu tại [results Phase 11](../tests/results/phase-11/README.md) và [remakes Phase 11](../remakes/phase-11/).

## Còn thiếu / blocker

- Chưa có OS/container sandbox per task, egress allowlist, terminal/browser/write adapter, timeout/output caps cho process, file diff/test exit/artifact capture hoặc Inspector integration.
- Chưa gọi `evaluate_action` + `consume_approval` trước side effect; Phase 10 approval API hiện chỉ ghi audit. Phase 09 chưa đạt worker lease/recovery/retry.
- Chưa có receipt/idempotency/reconcile path cho external side effects, replay trace, persistence hay run thật. Không có inference grant; không chạy runtime/gateway.
- Vì vậy P11-01…05/P11-07 và P11-06 end-to-end vẫn blocked. Phần này không chứng minh sandbox hoặc executor an toàn và không đủ điều kiện nghiệm thu Phase 11.

## Source

- `apps/api/src/agent_corporation_api/modules/tools/registry.py`
- `apps/api/src/agent_corporation_api/modules/tools/workspace.py`
- `apps/api/src/agent_corporation_api/modules/observability/redaction.py`
- `apps/api/tests/test_phase11_tools.py`
