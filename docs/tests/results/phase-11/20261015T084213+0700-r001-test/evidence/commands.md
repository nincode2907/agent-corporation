# Lệnh và quan sát — 20261015T084213+0700-r001-test

Thư mục làm việc: repository root. Platform/config: macOS, Python 3.14.8, pytest 9.0.2, uv project `apps/api`. Không đọc `.env`, token hoặc secret thật.

| Lệnh | Exit | Quan sát | Liên quan |
| --- | ---: | --- | --- |
| `rtk proxy uv run --project apps/api pytest apps/api/tests/test_phase11_tools.py` | 0 | 15 passed in 0.20s; chạy lại sau hardening path: 15 passed in 0.10s | C07, P11-01, P11-02, P11-06 |
| `rtk proxy env PYTHONPATH=apps/api/src uv run --project apps/api python -c 'from agent_corporation_api.modules.observability.redaction import redact_text; print(repr(redact_text("Authorization: Basic test-canary-123\\ncookie=test-cookie-456\\napi_key=masked-canary-789")))'` | 0 | Kết quả giữ nguyên `Authorization: Basic test-canary-123` và `cookie=test-cookie-456`; `api_key` thành `[REDACTED]`. Unit test redaction cũng xác nhận `api_key=...` bị che. | C05, P11-06 |
| `rtk proxy shasum -a 256 apps/api/src/agent_corporation_api/modules/tools/__init__.py apps/api/src/agent_corporation_api/modules/tools/registry.py apps/api/src/agent_corporation_api/modules/tools/workspace.py apps/api/tests/test_phase11_tools.py` | 0 | Hashes khớp [source-manifest.json](source-manifest.json). | C01, C08 |
| `rtk rg -n 'validate_proposal|execute_read_file|WorkspaceReader|list_tools' apps/api/src apps/api/tests/test_phase11_tools.py` | 0 | Mọi reference production nằm trong module mới; không có API/executor integration call site được tìm thấy trong `apps/api/src`. | C04, P11-01, P11-04, P11-05, P11-07 |
| `rtk proxy python3 -c '<relative link and case-count check over report.md>'` | 0 | 71 relative links, none missing; all 15 C01–C08/P11 cases are present. | C08 |

Không chạy API suite đầy đủ, DB/migration, worker, server, tool dispatch, network probe, inference, gateway hoặc lệnh có side effect.
