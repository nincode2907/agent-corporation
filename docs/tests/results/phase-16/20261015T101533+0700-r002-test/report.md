# Kiểm định Phase 16 — 20261015T101533+0700-r002-test

## Thông tin batch

- Phase: 16; vòng r002.
- Test batch: 20261015T101533+0700-r002-test.
- Bắt đầu / kết thúc: 2026-10-15T10:15:44+07:00 / 2026-10-15T10:17:19+07:00, Asia/Ho_Chi_Minh. ID batch được Chủ tịch giao cố định.
- Người/AI kiểm định: `/root/phase11_independent_test`; độc lập với AI remake.
- Yêu cầu/phạm vi: retest remake Phase 16; no product edits, DB/migrations/runtime/inference.
- Source: dirty worktree; source/test/doc/remake hashes and tracked Markdown/HTML diff hash: [manifest](evidence/manifest.txt); [dirty state](evidence/git-status.txt).
- Môi trường: Python 3.14.8, pytest 9.0.2, project uv env; synthetic-only canaries.
- Inference: không gọi; grant = 0.
- Dependency: Phase 15 chưa nghiệm thu; Phase 16 đang triển khai. Owner acceptance: chưa có.
- Supersedes: [Phase 16 r001](../20261015T100829+0700-r001-test/report.md).
- Remake nguồn: [Phase 16 r001 remake](../../../../remakes/phase-16/20261015T100829+0700-r001-remake/remake.md).
- Kết luận kỹ thuật: cần sửa. R001 fixes pass in focused fixtures, but settlement still accepts malformed call reference `../bad`. Persistent finance integration and IG16 remain blocked.
- Quyết định Chủ tịch: Chưa có.

## Mapping và tổng hợp

| Tiêu chí / nguồn | Test IDs | Kết quả kiểm |
| --- | --- | --- |
| RULES C01–C08 | C01–C08 | Đủ source, dependency, scope, permission, isolation, docs, regressions and report integrity. |
| AC1 dedup/pricing/reservation | P16-01, P16-02, P16-03 | Fixture regressions pass; source reconciliation, persistence and race remain unproven. |
| AC2 cost basis and cohort/period | P16-02, P16-04, P16-05, P16-06 | Local values checked; reporting integration absent. |
| AC3 justified limits and IG16 | P16-03, P16-07, P16-08 | No live dispatch or gate evidence. |

| Tag | Count |
| --- | ---: |
| clean | 7 |
| need-change | 9 |
| suggestion | 0 |

| Result | Count |
| --- | ---: |
| pass | 7 |
| fail | 1 |
| blocked | 8 |
| not-run | 0 |
| not-applicable | 0 |

## Kết quả từng test

### C01 — Source snapshot and scope

- Nguồn/tiêu chí: [RULES §1](../../../RULES.md); [Phase 16 checklist](../../../phases/phase-16.md).
- Bắt buộc: có.
- Điều kiện/môi trường: dirty worktree; no source edits by tester.
- Bước/lệnh: `rtk git status --short`; `rtk shasum -a 256 ...` — exit 0.
- Kỳ vọng: retest đúng Phase 16, snapshot hashes traceable.
- Thực tế: finance/quality source and tests are untracked, master plan/HTML modified; exact hashes and diff hash captured.
- Kết quả phản biện: none.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [manifest](evidence/manifest.txt), [git state](evidence/git-status.txt).
- Xử lý/đề xuất: use these hashes for next remake/retest.

### C02 — Roadmap dependency and status

- Nguồn/tiêu chí: [Phase 16 roadmap](../../../../master-plan.md); dependency 15.
- Bắt buộc: có.
- Điều kiện/môi trường: current Markdown source.
- Bước/lệnh: inspect Phase 15/16 status and dependency.
- Kỳ vọng: status/dependency are explicit; no inferred acceptance.
- Thực tế: Phase 16 `Đang triển khai`, dependency 15; Phase 15 remains unaccepted.
- Kết quả phản biện: none.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [master-plan.md](../../../../master-plan.md), [checklist](../../../phases/phase-16.md).
- Xử lý/đề xuất: preserve dependency blocker.

### C03 — Required demo and finance view

- Nguồn/tiêu chí: Phase 16 demo/delivery in [roadmap](../../../../master-plan.md); P16-01/P16-06.
- Bắt buộc: có.
- Điều kiện/môi trường: no runtime/worker/inference; grant 0.
- Bước/lệnh: not run by scope.
- Kỳ vọng: two task demo + retry, source reconciliation and environment-filtered view.
- Thực tế: no persistence/dashboard and no demo was run.
- Kết quả phản biện: none.
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Evidence: [checklist](../../../phases/phase-16.md), [manifest](evidence/manifest.txt).
- Xử lý/đề xuất: requires integrated isolated demo and source ledger.

### C04 — No silent dispatch/permission expansion

- Nguồn/tiêu chí: [RULES §2](../../../RULES.md); spec §11.
- Bắt buộc: có.
- Điều kiện/môi trường: test run uses local fixtures only.
- Bước/lệnh: focused pytest; direct pure-function canaries.
- Kỳ vọng: no model/tool dispatch, database writes, or new grant.
- Thực tế: none occurred; inference grant remains 0.
- Kết quả phản biện: none.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [focused pytest output](evidence/focused-pytest.txt), [negative canaries](evidence/negative-canaries.txt).
- Xử lý/đề xuất: no expanded permission inferred.

### C05 — Company/environment aggregation boundary

- Nguồn/tiêu chí: spec §§11–12; P16-06.
- Bắt buộc: có.
- Điều kiện/môi trường: synthetic mixed-scope rows.
- Bước/lệnh: call both period and lifetime aggregates across company and environment pairs.
- Kỳ vọng: reject mixed company/environment scope.
- Thực tế: company and environment mixtures raise `aggregate_scope_mismatch`; no persistent query/UI was exercised.
- Kết quả phản biện: none.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [scope canaries](evidence/negative-canaries.txt).
- Xử lý/đề xuất: P16-06 integration view remains blocked separately.

### C06 — Rendered roadmap consistency

- Nguồn/tiêu chí: [RULES §1](../../../RULES.md); Markdown source and generated HTML.
- Bắt buộc: có.
- Điều kiện/môi trường: current Markdown and existing rendered HTML; no rerender by tester.
- Bước/lệnh: extraction/compare of Phase 16 status/history from MD and HTML.
- Kỳ vọng: status/history synchronized and no contradictory journal.
- Thực tế: Phase 16 Markdown has one journal, status `Đang triển khai`; HTML phase object has same status and journal text.
- Kết quả phản biện: none.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [roadmap comparison](evidence/roadmap-consistency.txt); doc hashes in [manifest](evidence/manifest.txt).
- Xử lý/đề xuất: no status/render change needed in this report.

### C07 — Focused finance/quality/memory regressions

- Nguồn/tiêu chí: P16-01…08 and affected Phase 15 regression.
- Bắt buộc: có.
- Điều kiện/môi trường: safe fixture tests and in-memory negative canaries.
- Bước/lệnh: `rtk proxy uv run --project apps/api pytest apps/api/tests/test_phase16_finance_contracts.py apps/api/tests/test_phase17_quality_contracts.py apps/api/tests/test_phase15_memory_contracts.py` — exit 0.
- Kỳ vọng: focused suite and specified negative/regression boundaries pass.
- Thực tế: 23 passed. Bool/float rejection, dispatched release rejection, empty unknown, cross-scope, usage/pricing/currency, lifetime/period/chat fixtures pass; malformed settlement ref canary still succeeds.
- Kết quả phản biện: none.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [focused output](evidence/focused-pytest.txt), [canaries](evidence/negative-canaries.txt).
- Xử lý/đề xuất: P16-03 remains open despite green suite.

### C08 — Report/evidence integrity

- Nguồn/tiêu chí: [RULES §3.2/§4/§7](../../../RULES.md), [template](../../../templates/report.md).
- Bắt buộc: có.
- Điều kiện/môi trường: r002 snapshot.
- Bước/lệnh: check required IDs/tags/results/local links/hashes.
- Kỳ vọng: C01–C08/P16-01…08 each present once; evidence links resolve.
- Thực tế: report includes all cases and one tag/result per case, current hashes, command output and blockers.
- Kết quả phản biện: none.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: report and [evidence directory](evidence/manifest.txt).
- Xử lý/đề xuất: preserve snapshot immutable.

### P16-01 — Usage/source dedup

- Nguồn/tiêu chí: [checklist P16-01](../../../phases/phase-16.md), spec §11.
- Bắt buộc: có.
- Điều kiện/môi trường: cumulative/retry fixtures only.
- Bước/lệnh: focused suite, `test_usage_dedup_selects_highest_cumulative_sequence...`.
- Kỳ vọng: latest cumulative snapshot selected once; conflicts rejected; source reconciliation persists.
- Thực tế: local selection/dedup and conflict tests pass; no source adapter/ledger persistence or retry reconciliation run.
- Kết quả phản biện: none.
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Evidence: [pytest output](evidence/focused-pytest.txt); [checklist](../../../phases/phase-16.md).
- Xử lý/đề xuất: implement and verify source-to-ledger reconciliation.

### P16-02 — Pricing and cost basis

- Nguồn/tiêu chí: [checklist P16-02](../../../phases/phase-16.md), spec §11.
- Bắt buộc: có.
- Điều kiện/môi trường: immutable value fixtures, subscription/API-equivalent negatives.
- Bước/lệnh: focused suite.
- Kỳ vọng: basis/currency remain distinct; historical snapshot cannot be changed by new pricing; no subscription invoice inference.
- Thực tế: contract regression passes for versioned pricing and basis rejection; no persisted pricing lookup/dashboard report is exercised.
- Kết quả phản biện: none.
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Evidence: [pytest output](evidence/focused-pytest.txt); [source manifest](evidence/manifest.txt).
- Xử lý/đề xuất: persistence and historical report verification remain necessary.

### P16-03 — Revision, settlement, release and dispatched refs

- Nguồn/tiêu chí: [checklist P16-03](../../../phases/phase-16.md), spec §§10–11.
- Bắt buộc: có.
- Điều kiện/môi trường: synthetic reservation contract.
- Bước/lệnh: focused regression plus settle with `call_ref='../bad'`; release a dispatched reservation.
- Kỳ vọng: bool revision/float amount rejected; dispatched release rejected; settlement refs obey opaque-ref syntax; terminal/repeated transitions are rejected.
- Thực tế: bool revision and float amount rejected; dispatched release rejected. However settlement accepts `../bad` and returns it in settled reservation. Concurrent DB/CAS semantics not tested.
- Kết quả phản biện: none.
- Tag: need-change
- Kết quả: fail
- Mức độ: major
- Evidence: [negative canaries](evidence/negative-canaries.txt), [source hash](evidence/manifest.txt).
- Xử lý/đề xuất: validate call_ref against opaque-reference contract at transition boundary and revalidate result; add malformed-reference tests. Atomicity remains blocked.

### P16-04 — Accepted-task lifetime cohort

- Nguồn/tiêu chí: [checklist P16-04](../../../phases/phase-16.md), spec §13.
- Bắt buộc: có.
- Điều kiện/môi trường: synthetic old/current/child/retry/chat rows.
- Bước/lệnh: focused suite lifetime/period/chat test.
- Kỳ vọng: lifetime includes accepted cohort across periods once; chat excluded; currency/basis not blended.
- Thực tế: fixture verifies old + current + child totals and chat exclusion; no persistence/query selection or descendant lineage integration.
- Kết quả phản biện: none.
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Evidence: [pytest output](evidence/focused-pytest.txt), [checklist](../../../phases/phase-16.md).
- Xử lý/đề xuất: prove cohort selection and lineage through persistent ledger query.

### P16-05 — Empty period and late corrections

- Nguồn/tiêu chí: [checklist P16-05](../../../phases/phase-16.md), spec §13.
- Bắt buộc: có.
- Điều kiện/môi trường: empty and unknown-period fixtures.
- Bước/lệnh: focused suite `test_empty_period_is_unknown...` and mixed known/unknown test.
- Kỳ vọng: empty/unknown coverage is not zero; correction versions preserve previous as-of report.
- Thực tế: empty period now returns unknown; late correction `as_of`/version persistence remains absent.
- Kết quả phản biện: none.
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Evidence: [pytest output](evidence/focused-pytest.txt); [checklist](../../../phases/phase-16.md).
- Xử lý/đề xuất: add versioned correction/report integration and compare prior/new as-of outputs.

### P16-06 — Finance drilldown and scope

- Nguồn/tiêu chí: [checklist P16-06](../../../phases/phase-16.md), spec §§11–12.
- Bắt buộc: có.
- Điều kiện/môi trường: synthetic mixed company/environment values only.
- Bước/lệnh: in-memory aggregate negative checks.
- Kỳ vọng: cross-scope sums rejected; full Company→call drilldown links source and environment filters.
- Thực tế: mixed environment/company aggregates reject; no ledger query, dashboard, source call ID drilldown or shared gateway/native exclusion is integrated.
- Kết quả phản biện: none.
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Evidence: [negative canaries](evidence/negative-canaries.txt), [checklist](../../../phases/phase-16.md).
- Xử lý/đề xuất: implement persistent scoped drilldown and verify source IDs.

### P16-07 — Hard cap and approved resource limits

- Nguồn/tiêu chí: [checklist P16-07](../../../phases/phase-16.md), spec §11.
- Bắt buộc: có.
- Điều kiện/môi trường: no runtime adapter/config UI.
- Bước/lệnh: not run; source review only.
- Kỳ vọng: unknown cost not presented as hard USD cap; approved resource caps enforced after in-flight overshoot.
- Thực tế: contracts distinguish unknown/estimate; no enforcement or Owner-approved limit flow tested.
- Kết quả phản biện: none.
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Evidence: [checklist](../../../phases/phase-16.md), [manifest](evidence/manifest.txt).
- Xử lý/đề xuất: requires approved limit integration and adapter boundary proof.

### P16-08 — IG16

- Nguồn/tiêu chí: [IG16 checklist](../../../phases/phase-16.md), spec §13.
- Bắt buộc: có.
- Điều kiện/môi trường: no DB/runtime; no upstream IG12 revalidation; grant=0.
- Bước/lệnh: not run by scope.
- Kỳ vọng: end-to-end run/source usage, ledger/reservation/pricing/finance, dedup/late/unknown/race and accepted cohort all pass with correct evidence.
- Thực tế: only fixture contracts; no atomic persistence, run refs or dashboard.
- Kết quả phản biện: none.
- Tag: need-change
- Kết quả: blocked
- Mức độ: critical
- Evidence: [checklist](../../../phases/phase-16.md), [pytest output](evidence/focused-pytest.txt).
- Xử lý/đề xuất: integrate and run dedicated authorized gate after dependencies; no grant currently.

## Integration / release gates

| Gate | Verdict | Test IDs | Evidence / blocker |
| --- | --- | --- | --- |
| IG16 | BLOCKED | P16-08 | No persistent ledger/reservation, source run reconciliation, finance dashboard or dedicated grant; P16-03 has remaining fail. |

## Cleanup, giới hạn và bàn giao

- Cleanup: no DB/runtime artifacts; synthetic in-memory values only.
- Chưa kiểm chứng: source reconciliation, persistence, atomic reservation, late correction versions, drilldown/dashboard, approved limits, IG16.
- Cần sửa: P16-03 malformed settlement call ref (major). R001 bool/float, release, empty unknown and scope findings retested successfully.
- Đề xuất tùy chọn: none.
- Bước tiếp theo: remake P16-03 boundary finding, then independent r003; keep integration blockers visible.
- Bàn giao: r002 snapshot and evidence saved; no Owner acceptance or phase status change.
