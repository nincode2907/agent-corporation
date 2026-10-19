# Lệnh và kết quả — 20261015T085652+0700-r004-test

Môi trường: repository root, macOS, Python 3.14.8, pytest 9.0.2, uv project `apps/api`. Canary values đều giả. Không DB/runtime/dispatch/inference/gateway/network/external side effect.

| Lệnh | Exit | Quan sát | IDs |
| --- | ---: | --- | --- |
| `rtk proxy env PYTHONPATH=apps/api/src uv run --project apps/api python docs/tests/results/phase-11/20261015T085652+0700-r004-test/evidence/P11-06-json-matrix.py` | 0 | `leaking_cases=[]`; `output_json_valid=true`; escaped token value replaced entirely; all JSON credential values replaced; SHA-256 present/matches redacted bytes; byte_count matches redacted bytes; output 443 bytes. | C05, P11-06 |
| `rtk proxy uv run --project apps/api pytest apps/api/tests/test_phase11_tools.py apps/api/tests/test_sensitive_validation.py -q` | 0 | 26 passed, 1 StarletteDeprecationWarning about `httpx`/`starlette.testclient`, 1.28s. | C07, P11-01, P11-02, P11-06 |
| `rtk rg -n 'validate_proposal|execute_read_file|WorkspaceReader|list_tools' apps/api/src apps/api/tests/test_phase11_tools.py` | 0 | References remain in tools module/tests; no production executor/API call site. | C04, P11-01, P11-04, P11-05, P11-07 |
| `rtk git status --short` | 0 | `redaction.py` modified; Phase 11 tools/tests and remake/results artifacts untracked; no commit identified. | C01 |
| `rtk proxy shasum -a 256 apps/api/src/agent_corporation_api/modules/observability/redaction.py apps/api/src/agent_corporation_api/modules/tools/__init__.py apps/api/src/agent_corporation_api/modules/tools/registry.py apps/api/src/agent_corporation_api/modules/tools/workspace.py apps/api/tests/test_phase11_tools.py apps/api/tests/test_sensitive_validation.py` | 0 | Values match [source-manifest.json](source-manifest.json). | C01, C08 |
| `rtk proxy python3 docs/tests/results/phase-11/20261015T085652+0700-r004-test/evidence/check_report.py` | 0 | `relative_links=65 missing=[] cases=15`; all 65 relative links resolve and all 15 C01–C08/P11 records are present. | C08 |

Probe inputs and assertions are in [P11-06-json-matrix.py](P11-06-json-matrix.py). Script emits no canary values.
