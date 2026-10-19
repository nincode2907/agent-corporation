# Kiểm định Phase 16 — 20261015T102032+0700-r003-test

## Thông tin batch

- Phase: 16; vòng r003.
- Test batch: 20261015T102032+0700-r003-test.
- Bắt đầu / kết thúc: 2026-10-15T10:21:55+07:00 / 2026-10-15T10:22:45+07:00 (Asia/Ho_Chi_Minh; batch ID được giao cố định).
- Người/AI kiểm định: `/root/phase11_independent_test`; độc lập với AI remake.
- Yêu cầu/phạm vi: retest Phase 16 remake r002, regressions and blockers; không sửa source, DB/migration/runtime/inference.
- Source: dirty worktree; hashes and tracked roadmap diff hash in [manifest](evidence/manifest.txt), [git state](evidence/git-status.txt).
- Môi trường: Python 3.14.8 / pytest 9.0.2; synthetic fixtures, no secrets.
- Inference: không gọi; grant = 0.
- Dependency: Phase 15 chưa nghiệm thu; Phase 16 `Đang triển khai`. Owner acceptance: chưa có.
- Supersedes: [Phase 16 r002](../20261015T101533+0700-r002-test/report.md).
- Remake nguồn: [Phase 16 r002 remake](../../../../remakes/phase-16/20261015T102032+0700-r002-remake/remake.md).
- Kết luận kỹ thuật: chưa đủ bằng chứng. Local reservation/reference, unknown-empty, scope, usage, pricing/currency, lifetime/period/chat regressions pass; persistent finance and atomicity remain blocked.
- Quyết định Chủ tịch: Chưa có.

## Mapping và tổng hợp

| Tiêu chí / nguồn | Test IDs | Bằng chứng |
| --- | --- | --- |
| RULES C01–C08 | C01–C08 | Scope, dependency, boundaries, HTML, regression and report integrity. |
| AC1 usage dedup/pricing/reservation | P16-01, P16-02, P16-03 | Contract fixtures pass; source reconciliation and concurrent DB proof absent. |
| AC2 cost basis, lifetime/period | P16-02, P16-04, P16-05, P16-06 | Synthetic value checks pass; persistent query/view absent. |
| AC3 resource limits and IG16 | P16-03, P16-07, P16-08 | No live adapter, approved cap enforcement or gate evidence. |

| Tag | Count |
| --- | ---: |
| clean | 7 |
| need-change | 9 |
| suggestion | 0 |

| Result | Count |
| --- | ---: |
| pass | 7 |
| fail | 0 |
| blocked | 9 |
| not-run | 0 |
| not-applicable | 0 |

## Kết quả từng test

### C01 — Scope and source snapshot

- Nguồn/tiêu chí: [RULES §1](../../../RULES.md); [Phase 16 checklist](../../../phases/phase-16.md).
- Bắt buộc: có.
- Điều kiện/môi trường: worktree dirty; retest source after r002 remake.
- Bước/lệnh: `rtk git status --short`; source/doc `rtk shasum -a 256` — exit 0.
- Kỳ vọng: source, tests, docs and dirty state captured.
- Thực tế: all relevant current hashes and tracked docs diff hash saved; no tester source edits.
- Kết quả phản biện: none.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [manifest](evidence/manifest.txt), [git status](evidence/git-status.txt).
- Xử lý/đề xuất: use this snapshot for next review.

### C02 — Dependency and roadmap status

- Nguồn/tiêu chí: [Phase 16 roadmap](../../../../master-plan.md); dependency 15.
- Bắt buộc: có.
- Điều kiện/môi trường: current Markdown/HTML status.
- Bước/lệnh: inspect Phase 15/16 blocks.
- Kỳ vọng: current state and upstream dependency shown; no acceptance inferred.
- Thực tế: Phase 16 `Đang triển khai`, depends on Phase 15; Phase 15 is not accepted.
- Kết quả phản biện: none.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [master-plan.md](../../../../master-plan.md), [Phase 16 checklist](../../../phases/phase-16.md).
- Xử lý/đề xuất: keep dependency gate visible.

### C03 — Finance demo and view

- Nguồn/tiêu chí: Phase 16 demo/delivery in [roadmap](../../../../master-plan.md); P16-01/P16-06.
- Bắt buộc: có.
- Điều kiện/môi trường: demo requires runtime; grant=0.
- Bước/lệnh: not run by scope.
- Kỳ vọng: two demo tasks + retry reconciled to usage source; environment-filtered finance view.
- Thực tế: no demo, persistent ledger/source reconciliation or dashboard exercised.
- Kết quả phản biện: none.
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Evidence: [checklist](../../../phases/phase-16.md); [manifest](evidence/manifest.txt).
- Xử lý/đề xuất: requires isolated demo runtime and evidence-backed finance view.

### C04 — No unapproved dispatch or side effect

- Nguồn/tiêu chí: [RULES §2](../../../RULES.md); spec §11.
- Bắt buộc: có.
- Điều kiện/môi trường: fixture tests and local pure functions only.
- Bước/lệnh: focused pytest and direct canaries.
- Kỳ vọng: no inference/tool dispatch or DB writes; no new grant.
- Thực tế: none occurred; grant remains 0.
- Kết quả phản biện: none.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [focused output](evidence/focused-pytest.txt), [canaries](evidence/boundary-canaries.txt).
- Xử lý/đề xuất: no execution permission inferred.

### C05 — Aggregate company/environment scope

- Nguồn/tiêu chí: spec §§11–12; P16-06.
- Bắt buộc: có.
- Điều kiện/môi trường: synthetic mixed-company and mixed-environment tuples.
- Bước/lệnh: run period/lifetime aggregators on cross-scope rows.
- Kỳ vọng: reject mixed company/environment aggregation.
- Thực tế: both cross-company and cross-environment canaries raise `aggregate_scope_mismatch`.
- Kết quả phản biện: none.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [boundary canaries](evidence/boundary-canaries.txt).
- Xử lý/đề xuất: persistent query isolation remains part of P16-06.

### C06 — Markdown and rendered HTML

- Nguồn/tiêu chí: [RULES §1](../../../RULES.md); master-plan is source of truth.
- Bắt buộc: có.
- Điều kiện/môi trường: read-only comparison after remake renderer; no render command by tester.
- Bước/lệnh: extract phase status/journal from Markdown and HTML.
- Kỳ vọng: Phase 16 history and status synchronize.
- Thực tế: status `Đang triển khai`, one journal, HTML status/history matches Markdown. Phase 17 journal also matches after correction.
- Kết quả phản biện: none.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [roadmap comparison](evidence/roadmap-consistency.txt).
- Xử lý/đề xuất: no status change.

### C07 — Focused regressions

- Nguồn/tiêu chí: P16-01…08 plus dependency Phase 15 regression.
- Bắt buộc: có.
- Điều kiện/môi trường: Python 3.14.8, pytest 9.0.2.
- Bước/lệnh: `rtk proxy uv run --project apps/api pytest apps/api/tests/test_phase16_finance_contracts.py apps/api/tests/test_phase17_quality_contracts.py apps/api/tests/test_phase15_memory_contracts.py` — exit 0.
- Kỳ vọng: 24 tests pass with local negative boundaries.
- Thực tế: 24 passed. Bool/float/malformed ref and dispatched-release boundaries, empty unknown, cross-scope, usage dedup, pricing/basis/currency, lifetime/period/chat exclusion fixtures pass.
- Kết quả phản biện: none.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [pytest output](evidence/focused-pytest.txt), [boundary canaries](evidence/boundary-canaries.txt).
- Xử lý/đề xuất: fixture pass does not close unrun integration cases.

### C08 — Report and evidence integrity

- Nguồn/tiêu chí: [RULES §§3.2, 4, 7](../../../RULES.md), [template](../../../templates/report.md).
- Bắt buộc: có.
- Điều kiện/môi trường: r003 report snapshot.
- Bước/lệnh: verify IDs, tags/results, evidence, links, hashes.
- Kỳ vọng: all C01–C08/P16-01…08 present once, each one tag/result.
- Thực tế: report contains all cases and evidence; no acceptance claim.
- Kết quả phản biện: none.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: report and [manifest](evidence/manifest.txt).
- Xử lý/đề xuất: retain immutable snapshot.

### P16-01 — Usage/source dedup

- Nguồn/tiêu chí: [checklist P16-01](../../../phases/phase-16.md), spec §11.
- Bắt buộc: có.
- Điều kiện/môi trường: cumulative usage fixtures; no source adapter/ledger DB.
- Bước/lệnh: focused tests for cumulative sequence and conflicts.
- Kỳ vọng: one final entry per call/source/version with cache/reasoning not double-counted; real source reconciles.
- Thực tế: local snapshot selector and dedup regressions pass; source-to-ledger/retry/late persistence not integrated.
- Kết quả phản biện: none.
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Evidence: [pytest output](evidence/focused-pytest.txt); [checklist](../../../phases/phase-16.md).
- Xử lý/đề xuất: implement and verify source reconciliation.

### P16-02 — Pricing/basis immutability

- Nguồn/tiêu chí: [checklist P16-02](../../../phases/phase-16.md), spec §11.
- Bắt buộc: có.
- Điều kiện/môi trường: synthetic immutable pricing/cost fact fixtures.
- Bước/lệnh: focused suite.
- Kỳ vọng: historical price stable; actual/subscription/API-equivalent/currency distinct.
- Thực tế: contract regressions pass; persistence and dashboard assertions absent.
- Kết quả phản biện: none.
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Evidence: [pytest output](evidence/focused-pytest.txt); [manifest](evidence/manifest.txt).
- Xử lý/đề xuất: integrate persistence and source-backed reporting.

### P16-03 — Reservation transitions and release boundary

- Nguồn/tiêu chí: [checklist P16-03](../../../phases/phase-16.md), spec §§10–11.
- Bắt buộc: có.
- Điều kiện/môi trường: in-memory reservation state transitions only.
- Bước/lệnh: focused fixture tests and invalid-type/ref/release canaries.
- Kỳ vọng: reject bool revision, float settlement, malformed `../bad` ref, release after dispatch; no double settle, atomic reserve under concurrency.
- Thực tế: all local negative cases reject as required; unresolved/terminal guards pass. No database concurrency/atomicity, grant/period limit enforcement or in-flight settlement run.
- Kết quả phản biện: none.
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Evidence: [boundary canaries](evidence/boundary-canaries.txt), [pytest output](evidence/focused-pytest.txt).
- Xử lý/đề xuất: persistence CAS/race tests and budget enforcement remain necessary.

### P16-04 — Accepted-task lifetime cohort

- Nguồn/tiêu chí: [checklist P16-04](../../../phases/phase-16.md), spec §13.
- Bắt buộc: có.
- Điều kiện/môi trường: synthetic period/lifetime/chat cohort fixtures.
- Bước/lệnh: focused `period_cost_and_accepted_task_lifetime...` regression.
- Kỳ vọng: lifetime across periods includes accepted cohort once; chat excluded.
- Thực tế: fixture totals and chat exclusion pass; no persistent acceptance cohort query/descendant lineage.
- Kết quả phản biện: none.
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Evidence: [pytest output](evidence/focused-pytest.txt), [checklist](../../../phases/phase-16.md).
- Xử lý/đề xuất: add persistent query proof for accepted cohort/retry/children.

### P16-05 — Empty period and late corrections

- Nguồn/tiêu chí: [checklist P16-05](../../../phases/phase-16.md), spec §13.
- Bắt buộc: có.
- Điều kiện/môi trường: empty, unknown and reporting fixtures.
- Bước/lệnh: focused empty/mixed unknown tests.
- Kỳ vọng: empty period is unknown, not confirmed zero; late corrections create immutable report versions/as_of.
- Thực tế: empty result is `(None, unknown, 0)` and mixed unknown not partial-zero; no correction report version integration.
- Kết quả phản biện: none.
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Evidence: [boundary canaries](evidence/boundary-canaries.txt), [pytest output](evidence/focused-pytest.txt).
- Xử lý/đề xuất: integrate correction ledger and as-of report snapshots.

### P16-06 — Finance drilldown and scope isolation

- Nguồn/tiêu chí: [checklist P16-06](../../../phases/phase-16.md), spec §§11–12.
- Bắt buộc: có.
- Điều kiện/môi trường: local synthetic mixed scope only.
- Bước/lệnh: mixed company/environment aggregate canaries.
- Kỳ vọng: reject cross-scope aggregation; UI drilldown maps totals to source calls and filters shared gateway/native cost.
- Thực tế: cross-scope rejects; no DB query, dashboard, source-call drilldown or real gateway exclusion proof.
- Kết quả phản biện: none.
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Evidence: [boundary canaries](evidence/boundary-canaries.txt), [checklist](../../../phases/phase-16.md).
- Xử lý/đề xuất: integrated scoped query and drilldown required.

### P16-07 — Hard cap/resource enforcement

- Nguồn/tiêu chí: [checklist P16-07](../../../phases/phase-16.md), spec §11.
- Bắt buộc: có.
- Điều kiện/môi trường: no runtime adapter or Owner-approved limits.
- Bước/lệnh: not run by scope.
- Kỳ vọng: no unsupported hard USD/token cap; approved resource budget enforced and overshoot surfaced.
- Thực tế: cost contract separates unknown/estimate; enforcement/UI not tested.
- Kết quả phản biện: none.
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Evidence: [checklist](../../../phases/phase-16.md), spec §11.
- Xử lý/đề xuất: verify approved cap and in-flight behavior with authorized fake/runtime adapter.

### P16-08 — IG16

- Nguồn/tiêu chí: [IG16](../../../phases/phase-16.md), spec §13.
- Bắt buộc: có.
- Điều kiện/môi trường: no DB/runtime; grant=0; no upstream gate revalidation.
- Bước/lệnh: not run by scope.
- Kỳ vọng: run/source usage → ledger/budget/pricing → finance; race, late correction, unknown and accepted cohort proven.
- Thực tế: only local fixtures available; no persistence, calls or dashboard.
- Kết quả phản biện: none.
- Tag: need-change
- Kết quả: blocked
- Mức độ: critical
- Evidence: [checklist](../../../phases/phase-16.md), [test output](evidence/focused-pytest.txt).
- Xử lý/đề xuất: integrated authorized IG16 run required; grant currently absent.

## Integration / release gates

| Gate | Verdict | Test IDs | Evidence / blocker |
| --- | --- | --- | --- |
| IG16 | BLOCKED | P16-08 | No DB/persistent ledger, source run, dashboard, atomic reservation evidence or dedicated grant. |

## Cleanup, giới hạn và bàn giao

- Cleanup: no DB/runtime resources; synthetic values only.
- Chưa kiểm chứng: persistent source reconciliation, atomic budgets, pricing history/dashboard, correction versions, task cohort query, drilldown, hard caps, IG16.
- Cần sửa: no remaining local source defect found. All 9 need-change cases are blocked integration/proof gaps.
- Đề xuất tùy chọn: none.
- Bước tiếp theo: continue only after required dependencies/grants/integration are available; no phase acceptance inferred.
- Bàn giao: report/evidence r003 saved; status remains `Đang triển khai`.
