# Lệnh và quan sát — 20261015T085217+0700-r003-test

Môi trường: repository root, macOS, Python 3.14.8, pytest 9.0.2, uv project `apps/api`. Canary giả; không dùng secret thật. Không DB/runtime/inference/gateway/external network.

| Lệnh | Exit | Quan sát | IDs |
| --- | ---: | --- | --- |
| `rtk proxy env PYTHONPATH=apps/api/src uv run --project apps/api python docs/tests/results/phase-11/20261015T085217+0700-r003-test/evidence/P11-06-canary-check.py` | 0 | `leaking_cases=["json_escaped_token"]`; hash present and matches filtered output; byte count matches; output 451 bytes. | C05, P11-06 |
| `rtk proxy uv run --project apps/api pytest apps/api/tests/test_phase11_tools.py apps/api/tests/test_sensitive_validation.py -q` | 0 | 25 passed, 1 StarletteDeprecationWarning about `httpx`/`starlette.testclient`, 0.99s. | C07, P11-01, P11-02, P11-06 |
| `rtk rg -n 'validate_proposal|execute_read_file|WorkspaceReader|list_tools' apps/api/src apps/api/tests/test_phase11_tools.py` | 0 | No production executor/API integration call site; tool references confined to the new module/tests. | C04, P11-01, P11-04, P11-05, P11-07 |
| `rtk proxy shasum -a 256 apps/api/src/agent_corporation_api/modules/observability/redaction.py apps/api/src/agent_corporation_api/modules/tools/__init__.py apps/api/src/agent_corporation_api/modules/tools/registry.py apps/api/src/agent_corporation_api/modules/tools/workspace.py apps/api/tests/test_phase11_tools.py apps/api/tests/test_sensitive_validation.py` | 0 | All hashes match [source-manifest.json](source-manifest.json). | C01, C08 |
| `rtk proxy python3 -c '<relative-link and case-count check over report.md>'` | 0 | Report has 65 relative links, none missing, and all 15 C01–C08/P11 cases. | C08 |

The probe script prints only the leaked case label and hash/size assertions. The exact escaped JSON fixture is stored in [P11-06-canary-check.py](P11-06-canary-check.py); values are synthetic.
