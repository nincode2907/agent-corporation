# Lệnh và quan sát — 20261015T091533+0700-r002-test

Environment: repo root, macOS, Python/uv project `apps/api`. No DB/runtime/dispatch/inference/gateway/network.

| Lệnh | Exit | Quan sát | Cases |
| --- | ---: | --- | --- |
| `rtk proxy uv run --project apps/api pytest apps/api/tests/test_phase12_orchestration_contracts.py apps/api/tests/test_phase13_organization_contracts.py -q` | 0 | `14 passed in 0.08s`. | C07, P12-01, P12-02 |
| `rtk proxy env PYTHONPATH=apps/api/src uv run --project apps/api python docs/tests/results/phase-12/20261015T091533+0700-r002-test/evidence/P12-02-contract-matrix.py` | 0 | Valid refs accepted; empty and malformed refs rejected; bool and float rejected in every DelegationLimits field. | P12-02 |
| `rtk cat apps/api/src/agent_corporation_api/modules/orchestration/contracts.py apps/api/tests/test_phase12_orchestration_contracts.py` | 0 | Source uses minimum 1 evidence ref and full namespace/identifier regex; limit validator requires exact `int` type. Tests cover empty list, invalid namespace token, traversal and boolean limit. | P12-02 |
| `rtk proxy shasum -a 256 apps/api/src/agent_corporation_api/modules/orchestration/contracts.py apps/api/src/agent_corporation_api/modules/orchestration/__init__.py apps/api/tests/test_phase12_orchestration_contracts.py docs/tests/phases/phase-12.md docs/master-plan.md docs/product-spec.md docs/decisions/0001-v1-foundation.md docs/remakes/phase-12/20261015T091254+0700-r001-remake/remake.md` | 0 | Values match [manifest](source-manifest.json). | C01, C08 |
| `rtk git status --short` | 0 | Dirty worktree; current code/docs artifacts remain uncommitted/untracked. | C01 |
| `rtk proxy python3 docs/tests/results/phase-12/20261015T091533+0700-r002-test/evidence/check_report.py` | 0 | `links=39 missing_links=[] cases=15 missing_ids=[] missing_fields=[]`; renderer-visible fields present for every case. | C08 |
| `rtk proxy env PYTHONPATH=scripts python3 -c 'from render_plan import phase_test_report; [(lambda report: print(report["round"], report["verdict"], len(report["cases"]), [item["id"] for item in report["cases"]]))(phase_test_report(phase)) for phase in ("12", "13")]'` | 0 | Both phases parse as `r002`, verdict `chưa đủ bằng chứng`, and 15/15 required cases. | C08 |
