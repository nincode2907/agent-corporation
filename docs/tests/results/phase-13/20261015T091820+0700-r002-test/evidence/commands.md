# Lệnh và quan sát — 20261015T091820+0700-r002-test

Environment: repository root, macOS, Python/uv project `apps/api`; no DB/runtime/inference/chat/gateway.

| Lệnh | Exit | Quan sát | Cases |
| --- | ---: | --- | --- |
| `rtk proxy uv run --project apps/api pytest apps/api/tests/test_phase12_orchestration_contracts.py apps/api/tests/test_phase13_organization_contracts.py -q` | 0 | `14 passed in 0.08s`. | C07, P13-01…03 |
| `rtk proxy shasum -a 256 apps/api/src/agent_corporation_api/modules/organization/contracts.py apps/api/src/agent_corporation_api/modules/organization/__init__.py apps/api/tests/test_phase13_organization_contracts.py docs/tests/phases/phase-13.md docs/master-plan.md docs/product-spec.md docs/decisions/0001-v1-foundation.md` | 0 | Values match [manifest](source-manifest.json). | C01, C08 |
| `rtk git status --short` | 0 | Dirty worktree; Phase 13 contract/test untracked, no commit; other project docs and phase artifacts also dirty. | C01 |
| `rtk rg -n -C 3 'class EmployeeProfileVersion|frozen|test_profile_revision_is_append_only' apps/api/src/agent_corporation_api/modules/organization/contracts.py apps/api/tests/test_phase13_organization_contracts.py` | 0 | `frozen=True`; negative mutation assertion expects `ValidationError`. | P13-03 |
| `rtk rg -n 'EmployeeProfileVersion|OrganizationSnapshot|next_profile_version' apps/api/src` | 0 | Only pure contract definitions and internal validator refs; no persistence/CRUD API caller found. | C04, P13-01…07 |
| `rtk rg -n -i 'create.{0,30}(employee|department|company)|\\bceo\\b|\\bhire|staffing|employee_version' apps/api/src` | 0 | Matches demo-scoped seed/read paths and employee version references; no CEO/real staffing endpoint found in source search. | P13-07 |
| `rtk proxy python3 docs/tests/results/phase-13/20261015T091820+0700-r002-test/evidence/check_report.py` | 0 | `links=36 missing_links=[] cases=15 missing_ids=[] missing_fields=[]`; canonical renderer fields present. | C08 |
| `rtk proxy env PYTHONPATH=scripts python3 -c 'from render_plan import phase_test_report; [(lambda report: print(report["round"], report["verdict"], len(report["cases"]), [item["id"] for item in report["cases"]]))(phase_test_report(phase)) for phase in ("12", "13")]'` | 0 | Both phases parse as `r002`, verdict `chưa đủ bằng chứng`, and 15/15 required cases. | C08 |
