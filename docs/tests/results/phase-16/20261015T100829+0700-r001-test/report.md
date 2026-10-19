# Kiểm định Phase 16 — 20261015T100829+0700-r001-test

## Thông tin batch

- Phase: 16
- Test batch: 20261015T100829+0700-r001-test
- Vòng: r001
- Bắt đầu / kết thúc: 2026-10-15T10:08:29+07:00 / 2026-10-15T10:11:23+07:00 (Asia/Ho_Chi_Minh; batch ID được giao trước khi bắt đầu)
- Người/AI kiểm định: `/root/phase11_independent_test`
- Độc lập với AI triển khai/remake: Được giao độc lập từ `/root`; hiện chưa có remake cho batch này.
- Yêu cầu/phạm vi được giao: kiểm định độc lập contracts/tests Phase 16–17; chỉ fixture/safe source checks; không sửa implementation, không DB/migration/runtime/inference.
- Source: worktree dirty, không dùng commit làm định danh. Hashes và `git status --short` tại [manifest](evidence/manifest.txt) và [dirty-state capture](evidence/git-status.txt).
- Môi trường/config/tool versions: macOS workspace; Python project environment qua `rtk proxy uv`; chỉ synthetic in-memory fixtures. Không đọc secrets.
- Inference: không gọi; inference grant = 0.
- Dependency/quyết định nghiệm thu: roadmap Phase 16 phụ thuộc Phase 15; Phase 15 đang triển khai/chưa nghiệm thu. Không có Owner acceptance Phase 16.
- Supersedes: Không có; r001.
- Remake nguồn: Không có ở vòng đầu.
- Kết luận kỹ thuật: cần sửa; các fixture pass chỉ chứng minh contracts cục bộ. Finance source có lỗi loại dữ liệu và cô lập scope; atomicity, persistence, dashboard, reconciliation và gate còn blocked.
- Quyết định Chủ tịch: Chưa có.

## Mapping và phạm vi kiểm định

| Tiêu chí hiện tại / nguồn | Test IDs | Bắt buộc / tùy điều kiện | Ghi chú |
| --- | --- | --- | --- |
| C01–C08 theo [RULES](../../../RULES.md) | C01–C08 | Bắt buộc | Source, scope, dependency, permissions, privacy, integration, test evidence, report integrity. |
| AC1: cumulative usage dedup; immutable pricing | P16-01, P16-02, P16-03 | Bắt buộc | Pure fixtures only; source reconciliation and race/persistence not present. |
| AC2: cost basis and accepted-task/lifetime/period accounting | P16-02, P16-04, P16-05, P16-06 | Bắt buộc | Contract behavior reviewed; reports/query/dashboard not integrated. |
| AC3: justified hard caps and resource limits | P16-03, P16-07, P16-08 | Bắt buộc | IG16 requires run evidence and separate grant if a real run is performed. |

## Tổng hợp

| Tag | Số test |
| --- | ---: |
| clean | 5 |
| need-change | 11 |
| suggestion | 0 |

| Result | Số test |
| --- | ---: |
| pass | 5 |
| fail | 4 |
| blocked | 7 |
| not-run | 0 |
| not-applicable | 0 |

## Kết quả từng test

### C01 — Đúng phase và source snapshot

- Nguồn/tiêu chí: [RULES §1](../../../RULES.md); [Phase 16 checklist](../../../phases/phase-16.md).
- Bắt buộc: có.
- Điều kiện/môi trường: đọc source, checklist, spec/ADR; worktree dirty.
- Bước/lệnh: `rtk git status --short`; `rtk shasum -a 256 ...` — exit 0.
- Kỳ vọng: test đúng scope, source dirty được hash đầy đủ.
- Thực tế: source/tests mới là untracked, master-plan và HTML modified; manifest ghi hashes hiện tại.
- Kết quả phản biện: none.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [manifest](evidence/manifest.txt), [git status](evidence/git-status.txt).
- Xử lý/đề xuất: dùng đúng snapshot hashes cho remake/retest.

### C02 — Roadmap, dependency và tiêu chí nghiệm thu

- Nguồn/tiêu chí: [Phase 16 roadmap](../../../../master-plan.md); dependency 15; [checklist](../../../phases/phase-16.md).
- Bắt buộc: có.
- Điều kiện/môi trường: kiểm tra Markdown; không thay đổi status.
- Bước/lệnh: đọc Phase 15–16 roadmap blocks — exit 0.
- Kỳ vọng: dependency và status được ghi rõ; không tuyên bố nghiệm thu.
- Thực tế: Phase 16 `Đang triển khai`, phụ thuộc Phase 15; roadmap không ghi Owner acceptance.
- Kết quả phản biện: none.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [master-plan.md](../../../../master-plan.md), [Phase 16 checklist](../../../phases/phase-16.md).
- Xử lý/đề xuất: giữ nguyên blocker dependency trong các vòng sau.

### C03 — Demo reconciliation và finance view

- Nguồn/tiêu chí: Phase 16 demo/bàn giao trong [roadmap](../../../../master-plan.md); checklist P16-01/P16-06.
- Bắt buộc: có.
- Điều kiện/môi trường: không chạy worker, runtime hoặc inference; grant = 0.
- Bước/lệnh: source review.
- Kỳ vọng: hai task demo, retry, ledger khớp usage source và filter môi trường.
- Thực tế: không có finance dashboard/persistent run reconciliation trong scope source hiện có; demo không chạy theo ranh giới được giao.
- Kết quả phản biện: none.
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Evidence: [checklist P16-01/P16-06](../../../phases/phase-16.md); [manifest](evidence/manifest.txt).
- Xử lý/đề xuất: cần integration/UI và dữ liệu demo cô lập; không suy ra từ fixture.

### C04 — Permission, inference và side-effect boundary

- Nguồn/tiêu chí: [RULES §2](../../../RULES.md); Phase 16 limits; ADR foundation.
- Bắt buộc: có.
- Điều kiện/môi trường: chỉ đọc contracts/tests.
- Bước/lệnh: source review; focused pytest — exit 0.
- Kỳ vọng: test không dispatch, không cấp quyền mới, không giả làm gate thật.
- Thực tế: chỉ Pydantic/value contract tests và pure functions; không gọi inference/runtime/DB.
- Kết quả phản biện: none.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [focused pytest](evidence/focused-pytest.txt).
- Xử lý/đề xuất: không mở rộng quyền; real-run proof cần grant riêng theo batch.

### C05 — Finance scope isolation

- Nguồn/tiêu chí: spec §§11–13; Phase 16 P16-04/P16-06.
- Bắt buộc: có.
- Điều kiện/môi trường: synthetic rows từ hai company scopes.
- Bước/lệnh: in-memory `aggregate_period` và `aggregate_accepted_task_lifetime` canaries.
- Kỳ vọng: helper từ chối scope pha trộn hoặc lọc theo company/environment.
- Thực tế: helper không nhận scope selector/không xác minh homogeneity; hai công ty bị cộng chung (40, 2), kể cả cùng accepted_task_ref.
- Kết quả phản biện: none.
- Tag: need-change
- Kết quả: fail
- Mức độ: major
- Evidence: [negative canaries](evidence/negative-canaries.txt); source hash trong [manifest](evidence/manifest.txt).
- Xử lý/đề xuất: bắt buộc scope-bound query/aggregation và negative test cross-company/environment.

### C06 — HTML/roadmap consistency

- Nguồn/tiêu chí: [RULES §1](../../../RULES.md); Markdown là nguồn chuẩn, HTML là bản nhìn.
- Bắt buộc: có.
- Điều kiện/môi trường: HTML hiện có được hash; không render lại theo chỉ thị.
- Bước/lệnh: `rtk shasum -a 256 docs/master-plan.md docs/master-plan.html` — exit 0.
- Kỳ vọng: generated HTML phản ánh roadmap hiện tại.
- Thực tế: Markdown/HTML đều modified; không chạy renderer hoặc kiểm tra parsed Phase 16 payload độc lập trong lượt này.
- Kết quả phản biện: none.
- Tag: need-change
- Kết quả: blocked
- Mức độ: minor
- Evidence: [manifest](evidence/manifest.txt).
- Xử lý/đề xuất: xác minh render đồng bộ khi bước tài liệu được giao; không sửa status ở report này.

### C07 — Focused fixture tests và negative boundaries

- Nguồn/tiêu chí: Phase 16 checklist P16-01…08.
- Bắt buộc: có.
- Điều kiện/môi trường: project Python environment, synthetic-only.
- Bước/lệnh: `rtk proxy uv run --project apps/api pytest apps/api/tests/test_phase16_finance_contracts.py apps/api/tests/test_phase17_quality_contracts.py -q` — exit 0.
- Kỳ vọng: focused tests chạy; negative boundaries được kiểm tra độc lập.
- Thực tế: 13 passed; thêm canaries phát hiện bool revision, float settlement, empty aggregate và cross-company aggregation defects.
- Kết quả phản biện: none.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [pytest output](evidence/focused-pytest.txt), [canaries](evidence/negative-canaries.txt).
- Xử lý/đề xuất: pass suite không đóng các issue của case P16.

### C08 — Report/evidence integrity

- Nguồn/tiêu chí: [RULES §3.2/§4](../../../RULES.md), [template](../../../templates/report.md).
- Bắt buộc: có.
- Điều kiện/môi trường: report snapshot r001.
- Bước/lệnh: đối chiếu case IDs, evidence links, hashes và dirty state.
- Kỳ vọng: đủ C01–C08/P16-01…08, mỗi case có một tag/result/evidence.
- Thực tế: report dùng block riêng; manifest chứa source/doc hashes; không có Owner acceptance.
- Kết quả phản biện: none.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: report và các files trong `evidence/`.
- Xử lý/đề xuất: giữ report immutable sau snapshot.

### P16-01 — Usage/source dedup

- Nguồn/tiêu chí: [checklist P16-01](../../../phases/phase-16.md), spec §11.
- Bắt buộc: có.
- Điều kiện/môi trường: fixtures cover snapshots; không có live source ledger.
- Bước/lệnh: focused pytest; xem [output](evidence/focused-pytest.txt).
- Kỳ vọng: cumulative/reconnect/retry/late correction reconciliation ra một final entry per call/source/version.
- Thực tế: value contract validates cumulative token relations; source→ledger ingestion, dedup persistence và late correction reporting chưa tích hợp.
- Kết quả phản biện: none.
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Evidence: focused tests và [checklist](../../../phases/phase-16.md).
- Xử lý/đề xuất: cần source reconciliation report và persistent idempotency tests.

### P16-02 — Pricing/basis immutability

- Nguồn/tiêu chí: [checklist P16-02](../../../phases/phase-16.md), spec §11.
- Bắt buộc: có.
- Điều kiện/môi trường: immutable pricing value contract fixtures.
- Bước/lệnh: focused pytest.
- Kỳ vọng: old pricing snapshot unchanged; actual/subscription/API-equivalent/local estimates distinguishable.
- Thực tế: contract types separate basis/measurement and frozen snapshot; no pricing history/dashboard query test, so end-to-end claim unverified.
- Kết quả phản biện: none.
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Evidence: [finance source](../../../../../apps/api/src/agent_corporation_api/modules/finance/contracts.py); pytest output.
- Xử lý/đề xuất: integrate versioned pricing persistence and verify old call report remains immutable.

### P16-03 — Budget concurrent settle

- Nguồn/tiêu chí: [checklist P16-03](../../../phases/phase-16.md), spec §§10–11.
- Bắt buộc: có.
- Điều kiện/môi trường: pure reservation transition only; no concurrent storage.
- Bước/lệnh: focused pytest plus synthetic negative call `transition_reservation(... expected_revision=True ...)` and `settled_amount=0.5`.
- Kỳ vọng: revision requires exact integer; amount obeys strict integer bounds; stale/duplicate concurrent transition is rejected atomically.
- Thực tế: `True` accepted against current revision 1 and settled to revision 2; float 0.5 remains in returned model because `model_copy(update=...)` bypasses validation. Atomic race not tested.
- Kết quả phản biện: none.
- Tag: need-change
- Kết quả: fail
- Mức độ: major
- Evidence: [negative canaries](evidence/negative-canaries.txt), [source hash](evidence/manifest.txt).
- Xử lý/đề xuất: exact-type revision/amount validation and validate returned model; then add transactional race/idempotency tests.

### P16-04 — Lifetime accepted cohort

- Nguồn/tiêu chí: [checklist P16-04](../../../phases/phase-16.md), spec §13.
- Bắt buộc: có.
- Điều kiện/môi trường: helper-level synthetic input only.
- Bước/lệnh: focused pytest; source review.
- Kỳ vọng: accepted cohort sums only authorized accepted task/descendant scope exactly once; independent retry excluded.
- Thực tế: helper aggregates supplied entries but has no query, persisted acceptance cohort, or descendant dedup integration. Mixed company rows are accepted (C05/P16-06).
- Kết quả phản biện: none.
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Evidence: [source/test manifest](evidence/manifest.txt), [checklist](../../../phases/phase-16.md).
- Xử lý/đề xuất: implement persistent cohort selection and prove retry/descendant behavior.

### P16-05 — Period and late corrections

- Nguồn/tiêu chí: [checklist P16-05](../../../phases/phase-16.md), spec §13.
- Bắt buộc: có.
- Điều kiện/môi trường: synthetic empty period canary.
- Bước/lệnh: call `aggregate_period(())`.
- Kỳ vọng: no rows/unknown coverage must not be asserted as confirmed zero; later corrections preserve prior as-of report.
- Thực tế: empty period returns amount 0, `measurement=confirmed`, entry_count 0. No correction ledger/report version path exists.
- Kết quả phản biện: none.
- Tag: need-change
- Kết quả: fail
- Mức độ: major
- Evidence: [negative canaries](evidence/negative-canaries.txt).
- Xử lý/đề xuất: represent empty/unobserved coverage as unknown; add versioned `as_of` correction records and regression.

### P16-06 — Finance drilldown and isolation

- Nguồn/tiêu chí: [checklist P16-06](../../../phases/phase-16.md), spec §§11–12.
- Bắt buộc: có.
- Điều kiện/môi trường: synthetic mixed-company entries; no dashboard/runtime.
- Bước/lệnh: `aggregate_period(mixed_rows)` and `aggregate_accepted_task_lifetime(mixed_rows, ref)`.
- Kỳ vọng: each query is bound to company/environment; totals drill to matching source IDs and exclude global gateway/native usage.
- Thực tế: helper sums cross-company rows without rejection/filter; each yielded amount 40 and count 2. No drilldown UI/source-link proof.
- Kết quả phản biện: none.
- Tag: need-change
- Kết quả: fail
- Mức độ: major
- Evidence: [negative canaries](evidence/negative-canaries.txt).
- Xử lý/đề xuất: scope aggregation at query/API boundary; add tenant/environment negative tests and source drilldown.

### P16-07 — Hard cap claims and resource limits

- Nguồn/tiêu chí: [checklist P16-07](../../../phases/phase-16.md), spec §11.
- Bắt buộc: có.
- Điều kiện/môi trường: no runtime adapter, config UI, or grants.
- Bước/lệnh: source review only.
- Kỳ vọng: no unsupported USD/token hard-cap claim; approved resource limit remains enforceable.
- Thực tế: cost basis values distinguish unknown/estimate, but no runtime limit enforcement or Owner-visible controls exercised.
- Kết quả phản biện: none.
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Evidence: [finance source manifest](evidence/manifest.txt), [checklist](../../../phases/phase-16.md).
- Xử lý/đề xuất: require approved limit path and fake-adapter overshoot proof before claiming cap behavior.

### P16-08 — IG16 integration gate

- Nguồn/tiêu chí: [checklist IG16](../../../phases/phase-16.md), spec §13.
- Bắt buộc: có.
- Điều kiện/môi trường: no DB/runtime, upstream IG12 not revalidated; grant = 0.
- Bước/lệnh: not run by scope.
- Kỳ vọng: source usage→ledger/budgets/pricing→finance, retries/late/unknown/cohort, gate dependencies and evidence IDs pass.
- Thực tế: only fixture tests exist; no atomic storage, source calls, dashboard, or qualifying run evidence.
- Kết quả phản biện: none.
- Tag: need-change
- Kết quả: blocked
- Mức độ: critical
- Evidence: [checklist](../../../phases/phase-16.md), [focused tests](evidence/focused-pytest.txt).
- Xử lý/đề xuất: implement integration and run dedicated authorized batch after upstream gates; no inference grant currently.

## Integration / release gates

| Gate áp dụng | Verdict | Test IDs | Evidence / blockers |
| --- | --- | --- | --- |
| IG16 | BLOCKED | P16-08 | No DB/runtime/ledger reconciliation or approved grant; P16-03/P16-05/P16-06 fail. No Owner acceptance. |

## Cleanup, giới hạn và bàn giao

- Cleanup: không tạo DB/runtime resources; synthetic-only canaries, không cleanup cần thiết.
- Chưa kiểm chứng: source ingestion, pricing dashboard, transaction atomicity, late correction/as-of versioning, approved resource cap, drilldown, IG16.
- Cần sửa: P16-03 (major type/validation bypass), P16-05 (major unknown reported as confirmed zero), P16-06/C05 (major cross-company aggregation). Also address missing integrations listed as blocked.
- Đề xuất tùy chọn: none.
- Bước tiếp theo: remake fixable source findings, then independent r002 retest against new hashes; do not infer phase acceptance.
- Bàn giao: report/evidence snapshot saved; Phase 16 remains `Đang triển khai`; Owner acceptance not asserted.
