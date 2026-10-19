# Lệnh và quan sát — 20261015T091102+0700-r001-test

Environment: repository root, macOS, Python/uv project `apps/api`. Không DB/runtime/dispatch/inference/gateway/network. Pytest dùng UUID và model fixtures thuần.

| Lệnh | Exit | Quan sát | Cases |
| --- | ---: | --- | --- |
| `rtk proxy uv run --project apps/api pytest apps/api/tests/test_phase12_orchestration_contracts.py apps/api/tests/test_phase13_organization_contracts.py -q` | 0 | `14 passed in 0.08s` | C07, P12-01, P12-02, P13-01…03 |
| `rtk git status --short` | 0 | Dirty worktree: Phase 12/13 contract modules and tests untracked; Phase 11 redaction and docs also dirty. No commit identified. | C01 |
| `rtk proxy shasum -a 256 apps/api/src/agent_corporation_api/modules/orchestration/contracts.py apps/api/src/agent_corporation_api/modules/orchestration/__init__.py apps/api/tests/test_phase12_orchestration_contracts.py docs/tests/phases/phase-12.md docs/master-plan.md docs/product-spec.md docs/decisions/0001-v1-foundation.md` | 0 | Hashes recorded in [manifest](source-manifest.json). | C01, C08 |
| `rtk rg -n 'route_task|validate_delegation_plan|class Handoff' apps/api/src apps/api/tests/test_phase12_orchestration_contracts.py` | 0 | Source refs found only in contract module and unit tests; inspected module functions validate/route but do not dispatch. | C04, P12-01…07 |
| `rtk proxy python3 docs/tests/results/phase-12/20261015T091102+0700-r001-test/evidence/check_report.py` | 0 | `relative_links=3 missing_links=[] missing_ids=[]`; 15 required case IDs are present. | C08 |

Source observation for P12-02: `Handoff.evidence_refs` defaults to `[]`; `refs_are_opaque` iterates values but does not reject an empty list. Thus a handoff may be constructed without evidence despite the checklist's complete-evidence criterion. Existing test only tests valid nonempty refs and rejects path traversal; it does not cover empty refs.
