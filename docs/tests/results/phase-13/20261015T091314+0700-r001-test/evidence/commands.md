# Lệnh và quan sát — 20261015T091314+0700-r001-test

Environment: repository root, macOS, Python/uv project `apps/api`. No DB/runtime/inference/chat/gateway/network.

| Lệnh | Exit | Quan sát | Cases |
| --- | ---: | --- | --- |
| `rtk proxy uv run --project apps/api pytest apps/api/tests/test_phase12_orchestration_contracts.py apps/api/tests/test_phase13_organization_contracts.py -q` | 0 | `14 passed in 0.08s`; run after `EmployeeProfileVersion` frozen config and mutation-negative assertion were present. | C07, P13-01…03 |
| `rtk proxy shasum -a 256 apps/api/src/agent_corporation_api/modules/organization/contracts.py apps/api/src/agent_corporation_api/modules/organization/__init__.py apps/api/tests/test_phase13_organization_contracts.py docs/tests/phases/phase-13.md docs/master-plan.md docs/product-spec.md docs/decisions/0001-v1-foundation.md` | 0 | Hashes recorded in [manifest](source-manifest.json). | C01, C08 |
| `rtk git status --short` | 0 | Dirty worktree; Phase 13 contract/test untracked, no commit; master-plan/HTML and Phase 11 artifacts are also dirty. | C01 |
| `rtk rg -n -C 3 'class EmployeeProfileVersion|frozen|test_profile_revision_is_append_only' apps/api/src/agent_corporation_api/modules/organization/contracts.py apps/api/tests/test_phase13_organization_contracts.py` | 0 | Current model has `frozen=True`; test asserts assignment raises `ValidationError`. | P13-03 |
| `rtk rg -n 'EmployeeProfileVersion|OrganizationSnapshot|next_profile_version' apps/api/src` | 0 | References only the pure organization contract module; no persistence/CRUD/API call sites found. | C04, P13-01…07 |
| `rtk rg -n -i 'create.{0,30}(employee|department|company)|\\bceo\\b|\\bhire|staffing|employee_version' apps/api/src` | 0 | Matching write path is deterministic demo fixture seeding; source shows demo scope and Chief of Staff, not CEO. No real staffing path identified in search. | P13-07 |
| `rtk proxy python3 docs/tests/results/phase-13/20261015T091314+0700-r001-test/evidence/check_report.py` | 0 | `relative_links=4 missing_links=[] missing_ids=[]`; all 15 required case IDs are present. | C08 |

No runtime cases were invoked. The regression command is fixture/unit-only.
