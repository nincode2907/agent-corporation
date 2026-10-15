# Lệnh và kết quả — 20261015T084733+0700-r002-test

Môi trường: repository root, macOS, Python 3.14.8, pytest 9.0.2, `uv` project `apps/api`. Chỉ canary tổng hợp; không đọc secret thật. Không có DB, runtime, dispatch, inference, gateway, network hay side effect bên ngoài.

| Lệnh | Exit | Quan sát | Case |
| --- | ---: | --- | --- |
| `rtk proxy uv run --project apps/api pytest apps/api/tests/test_phase11_tools.py apps/api/tests/test_sensitive_validation.py -q` | 0 | `24 passed, 1 warning in 1.01s`; warning StarletteDeprecationWarning về `httpx`/`starlette.testclient`, không phải test failure. | C07, P11-01, P11-02, P11-06 |
| `rtk proxy env PYTHONPATH=apps/api/src uv run --project apps/api python docs/tests/results/phase-11/20261015T084733+0700-r002-test/evidence/P11-06-canary-check.py` | 0 | JSON report: `leaking_cases=["json_token","json_authorization"]`; `sha256_present=true`; `sha256_matches_redacted_output=true`; `byte_count_matches_redacted_output=true`; filtered output length 379 bytes. | C05, P11-06 |
| `rtk rg -n 'validate_proposal|execute_read_file|WorkspaceReader|list_tools' apps/api/src apps/api/tests/test_phase11_tools.py` | 0 | Production references remain confined to the new tools module; no executor/API integration call site. | C04, P11-01, P11-04, P11-05, P11-07 |
| `rtk proxy shasum -a 256 apps/api/src/agent_corporation_api/modules/observability/redaction.py apps/api/src/agent_corporation_api/modules/tools/__init__.py apps/api/src/agent_corporation_api/modules/tools/registry.py apps/api/src/agent_corporation_api/modules/tools/workspace.py apps/api/tests/test_phase11_tools.py apps/api/tests/test_sensitive_validation.py` | 0 | All values match [source-manifest.json](source-manifest.json). | C01, C08 |
| `rtk proxy python3 -c '<relative link and case-count check over report.md>'` | 0 | 67 relative links, none missing; all 15 C01–C08/P11 cases are present. | C08 |

Canary details and assertions are in [P11-06-canary-check.py](P11-06-canary-check.py). Output deliberately includes only field names with leaked synthetic values and metadata checks, not credential values.
