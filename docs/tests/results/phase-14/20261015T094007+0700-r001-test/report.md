# Kiểm định Phase 14 — 20261015T094007+0700-r001-test

## Thông tin batch

- Phase: 14
- Test batch: 20261015T094007+0700-r001-test
- Vòng: r001
- Bắt đầu / kết thúc: 2026-10-15 09:40:07–09:40:30 +07:00 (Asia/Ho_Chi_Minh)
- Người/AI kiểm định: `/root/phase11_independent_test`
- Độc lập với AI triển khai/remake: kiểm định độc lập theo giao việc của `/root`; không có thông tin agent triển khai cụ thể.
- Yêu cầu/phạm vi được giao: kiểm định Phase 14–15 hiện trạng; snapshot Phase 14 trước, không sửa source, không chạy DB/migration/runtime/inference.
- Source: worktree dirty, không có commit snapshot; source hashes tại [source manifest](evidence/source-manifest.sha256), lệnh kiểm tra [evidence](evidence/test-output.txt).
- Môi trường/config/tool versions: macOS workspace; Python project `apps/api`; pytest qua `uv run`; không đọc `.env`/secret; chỉ unit/contract fixture và gọi hàm thuần.
- Inference: không gọi; grant = 0.
- Dependency/quyết định nghiệm thu: phụ thuộc Phase 13, chưa nghiệm thu; roadmap Phase 14 vẫn `Chưa triển khai`. Không có quyết định Owner/Chủ tịch cấp quyền chạy hay nghiệm thu.
- Supersedes: không có, vòng đầu.
- Remake nguồn: không có, vòng đầu.
- Kết luận kỹ thuật: **cần sửa**.
- Quyết định Chủ tịch: Chưa có.

## Mapping và phạm vi kiểm định

| Tiêu chí hiện tại / nguồn | Test IDs | Bắt buộc / tùy điều kiện | Ghi chú |
| --- | --- | --- | --- |
| C01–C08 theo [RULES §5](../../../RULES.md) | C01–C08 | Bắt buộc | Phạm vi, dependency, demo, dispatch, dữ liệu, docs, regression, tái kiểm định. |
| AC1: Agent không tự tuyển/sa thải cố định hoặc mở quyền | P14-01, P14-02 | Bắt buộc | Contract có proposal/Owner decision; API auth/persistence chưa tích hợp. |
| AC2: Offboard chặn run mới, xử lý run hiện tại, giữ lịch sử | P14-04, P14-05 | Bắt buộc | Contract chỉ lập kế hoạch; có lỗi bool/int ở revision guard. |
| AC3: đánh giá quality/need/marginal cost, không dùng token làm năng suất | P14-03, P14-06 | Bắt buộc | Contract fields có; suite/history thật chưa có. |
| HR proposal audit, fixed probation evidence, offboard run demo | P14-01…P14-06 | Bắt buộc | Chưa có end-to-end demo/evidence store. |

## Tổng hợp

| Tag | Số test |
| --- | ---: |
| clean | 6 |
| need-change | 8 |
| suggestion | 0 |

| Result | Số test |
| --- | ---: |
| pass | 6 |
| fail | 1 |
| blocked | 7 |
| not-run | 0 |
| not-applicable | 0 |

## Kết quả từng test

### C01 — Phạm vi và diff

- Nguồn/tiêu chí: [RULES C01](../../../RULES.md); Phase 14 source/test files trong manifest.
- Bắt buộc: có.
- Điều kiện/môi trường: worktree dirty; không thay đổi source.
- Bước/lệnh: `rtk git status --short`; đọc source, test và manifest.
- Kỳ vọng: chỉ đánh giá Phase 14 hiện tại, không làm phase khác/không đụng thay đổi người dùng.
- Thực tế: review giới hạn ở HR contract và test; không sửa source. Worktree có thay đổi của các phase khác, ghi nhận trong snapshot.
- Kết quả phản biện: none.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [manifest](evidence/source-manifest.sha256); worktree status đã xem trong phiên.
- Xử lý/đề xuất: không có.

### C02 — Dependency và nguồn quyết định

- Nguồn/tiêu chí: [Phase 14 roadmap](../../../../master-plan.md#phase-14--tuyển-dụng-và-thử-việc), Phase 14 checklist, Spec REQ16.
- Bắt buộc: có.
- Điều kiện/môi trường: đối chiếu roadmap/detail/spec; không suy diễn nghiệm thu.
- Bước/lệnh: đọc checklist, block roadmap Phase 14, requirement matrix và ADR.
- Kỳ vọng: dependency Phase 13 và trạng thái Owner/grant được nêu đúng.
- Thực tế: phụ thuộc Phase 13; roadmap hiện `Chưa triển khai`; không có quyết định nghiệm thu hay inference grant.
- Kết quả phản biện: none.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [checklist](../../../phases/phase-14.md); source manifest.
- Xử lý/đề xuất: giữ blocker Phase 13 và Owner authorization trong report.

### C03 — Đủ criteria và demo

- Nguồn/tiêu chí: [Phase 14 AC/demo](../../../../master-plan.md#phase-14--tuyển-dụng-và-thử-việc), checklist P14-01…06.
- Bắt buộc: có.
- Điều kiện/môi trường: chỉ unit/contract, không có Owner auth, persistence hoặc runtime.
- Bước/lệnh: focused pytest; đối chiếu checklist/evidence yêu cầu.
- Kỳ vọng: proposal audit, từ chối rồi duyệt proposal mới, probation evidence và offboard đang có run.
- Thực tế: 14 contract tests pass; không có audit persistence, UI/demo artifact, fixed suite output hay execution stop/drain receipt.
- Kết quả phản biện: none.
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Evidence: [test output](evidence/test-output.txt); [checklist](../../../phases/phase-14.md).
- Xử lý/đề xuất: sau dependency/authorization phù hợp, nối persistence/demo và lưu đúng bằng chứng checklist yêu cầu.

### C04 — Không thực thi âm thầm

- Nguồn/tiêu chí: [RULES C04](../../../RULES.md); HR contract docstring.
- Bắt buộc: có.
- Điều kiện/môi trường: source review và pure functions; không dispatch runtime/model/tool.
- Bước/lệnh: đọc `contracts.py`, chạy contract pytest và hai hàm pure được ghi trong evidence.
- Kỳ vọng: contract không tự tạo nhân viên, sửa grants hoặc thực thi stop.
- Thực tế: `decide_hr_proposal` trả kết quả `employee_created=False`, `grants_changed=False`; `begin_offboard` chỉ tạo plan; không có network/dispatch path trong module đã review.
- Kết quả phản biện: none.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [source](../../../../../apps/api/src/agent_corporation_api/modules/hr/contracts.py); [test output](evidence/test-output.txt).
- Xử lý/đề xuất: runtime integration vẫn blocked riêng trong P14-02/P14-04.

### C05 — Scope và dữ liệu nhạy cảm

- Nguồn/tiêu chí: [RULES C05](../../../RULES.md); HR proposal company/environment IDs and opaque refs.
- Bắt buộc: có.
- Điều kiện/môi trường: source/fixture review; không dùng dữ liệu thật.
- Bước/lệnh: đọc validators/decision scope checks; focused tests.
- Kỳ vọng: scope refs được ràng buộc, không đưa secret thật vào evidence.
- Thực tế: proposal/decision mang company/environment IDs; refs opaque; không đọc secret, test chỉ dùng UUID/fixture giả. Chưa có cross-tenant API/storage boundary để xác minh.
- Kết quả phản biện: none.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [source](../../../../../apps/api/src/agent_corporation_api/modules/hr/contracts.py); [test output](evidence/test-output.txt).
- Xử lý/đề xuất: API/storage scope enforcement chưa chứng minh; thuộc blocker tích hợp, không phải kết luận pass cho boundary đó.

### C06 — Tài liệu và bản nhìn

- Nguồn/tiêu chí: [RULES C06](../../../RULES.md); roadmap Markdown/HTML policy.
- Bắt buộc: có.
- Điều kiện/môi trường: đọc Markdown; không render roadmap vì không đổi trạng thái/roadmap.
- Bước/lệnh: đối chiếu roadmap Markdown với report scope.
- Kỳ vọng: không nâng trạng thái; tài liệu/bản nhìn nhất quán.
- Thực tế: không sửa Markdown/master-plan/HTML và không chạy renderer; worktree HTML/Markdown vốn dirty. Chưa xác minh nhất quán bản nhìn ở snapshot này.
- Kết quả phản biện: none.
- Tag: need-change
- Kết quả: blocked
- Mức độ: minor
- Evidence: [checklist](../../../phases/phase-14.md); `git status` trong phiên cho thấy master-plan HTML/Markdown dirty.
- Xử lý/đề xuất: đối chiếu/render ở bước documentation pipeline sau khi các báo cáo/remakes cần thiết cập nhật; không thay roadmap status.

### C07 — Regression liên quan

- Nguồn/tiêu chí: [RULES C07](../../../RULES.md); Phase 14 focused tests.
- Bắt buộc: có.
- Điều kiện/môi trường: focused contract suite Phase 14 + Phase 15, không DB/runtime.
- Bước/lệnh: `rtk proxy uv run --project apps/api pytest apps/api/tests/test_phase14_hr_contracts.py apps/api/tests/test_phase15_memory_contracts.py -q`.
- Kỳ vọng: regression focused xanh; ghi giới hạn.
- Thực tế: 14 passed, exit 0. Suite không kiểm Owner API authorization, persistence, run stop/drain hoặc race thật.
- Kết quả phản biện: none.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [test output](evidence/test-output.txt).
- Xử lý/đề xuất: rerun sau remake source revision mới.

### C08 — Có thể tái kiểm định

- Nguồn/tiêu chí: [RULES C08](../../../RULES.md); [report template](../../../templates/report.md).
- Bắt buộc: có.
- Điều kiện/môi trường: report, manifest, command evidence và link tương đối.
- Bước/lệnh: kiểm IDs/tags/report/evidence bằng đọc lại; source hashes ở manifest.
- Kỳ vọng: từng C/P case có đúng một tag/result và evidence/expected/actual.
- Thực tế: report có 14 case blocks, manifest băm source/docs và log command/repro; chưa có link checker automation.
- Kết quả phản biện: none.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: report hiện tại và [manifest](evidence/source-manifest.sha256).
- Xử lý/đề xuất: xác minh link checker ở bước tài liệu nếu có.

### P14-01 — HR proposal đủ căn cứ

- Nguồn/tiêu chí: [checklist P14-01](../../../phases/phase-14.md); roadmap AC1.
- Bắt buộc: có.
- Điều kiện/môi trường: pure model fixture; không có audit store/UI.
- Bước/lệnh: focused pytest `test_proposal_requires_need_evidence_probation_criteria_and_cost_provenance`.
- Kỳ vọng: proposal cần nhu cầu/evidence, contract/model/tools, cost status/provenance, probation/criteria; không tự thành hire.
- Thực tế: validator test pass; proposal fields có các dữ liệu cần thiết. Proposal audit/persistence và demo tạo proposal chưa được tích hợp.
- Kết quả phản biện: none.
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Evidence: [test output](evidence/test-output.txt); [source](../../../../../apps/api/src/agent_corporation_api/modules/hr/contracts.py).
- Xử lý/đề xuất: nối contract với lưu audit/evidence và UI flow trong phase sau khi dependency được chấp nhận.

### P14-02 — Owner approve/reject

- Nguồn/tiêu chí: [checklist P14-02](../../../phases/phase-14.md); Spec §10/REQ16.
- Bắt buộc: có.
- Điều kiện/môi trường: pure function tests; chưa có API auth/session/CSRF/persistence.
- Bước/lệnh: focused pytest `test_owner_decision_only_records_proposal_outcome_and_never_creates_employee_or_grants` và `test_rejection_is_auditable_but_does_not_change_employee_state`.
- Kỳ vọng: agent bị deny; Owner decision auditable; reject không đổi employee/grants; approve không tự dispatch.
- Thực tế: contract chặn `actor_role != owner`; output thuần không tạo employee/grant; tests pass. Không chứng minh Owner auth tại API, persistence/audit hoặc bypass các endpoint thật.
- Kết quả phản biện: none.
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Evidence: [test output](evidence/test-output.txt); [source](../../../../../apps/api/src/agent_corporation_api/modules/hr/contracts.py).
- Xử lý/đề xuất: tích hợp với verified Owner auth + durable audit; kiểm negative API bypass sau khi dependency được chấp nhận.

### P14-03 — Probation assessment

- Nguồn/tiêu chí: [checklist P14-03](../../../phases/phase-14.md); roadmap AC3.
- Bắt buộc: có.
- Điều kiện/môi trường: fixed suite chưa có; chỉ schema/fixtures.
- Bước/lệnh: focused pytest `test_probation_assessment_uses_criteria_evidence_and_keeps_unknown_cost_explicit`.
- Kỳ vọng: outcome theo criterion/evidence và marginal cost; token không là năng suất.
- Thực tế: assessment contract giữ outcome unknown, evidence refs và `CostBasis(status="unknown")`; không có suite outputs hoặc persisted assessment.
- Kết quả phản biện: none.
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Evidence: [test output](evidence/test-output.txt); [source](../../../../../apps/api/src/agent_corporation_api/modules/hr/contracts.py).
- Xử lý/đề xuất: cung cấp fixed suite và assessment evidence lưu được; không tự suy hiệu suất từ token.

### P14-04 — Offboard trong run

- Nguồn/tiêu chí: [checklist P14-04](../../../phases/phase-14.md); roadmap AC2.
- Bắt buộc: có.
- Điều kiện/môi trường: chỉ plan contract; không active worker/runtime/stop grant.
- Bước/lệnh: focused pytest `test_offboard_plan_blocks_new_assignments_and_partitions_active_run_outcomes`.
- Kỳ vọng: ngăn assignment mới, queued cancel, running stop, unknown reconcile, giữ history trước khi chuyển lifecycle.
- Thực tế: plan partition IDs và đánh dấu deny/preserve; không thực hiện stop/drain/revoke hay xác nhận task kết thúc.
- Kết quả phản biện: none.
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Evidence: [test output](evidence/test-output.txt); [source](../../../../../apps/api/src/agent_corporation_api/modules/hr/contracts.py).
- Xử lý/đề xuất: blocker tích hợp execution/approval/stop lifecycle; cần receipt thật và durable history.

### P14-05 — Offboard race/idempotency và revision type

- Nguồn/tiêu chí: [checklist P14-05](../../../phases/phase-14.md); optimistic revision contract.
- Bắt buộc: có.
- Điều kiện/môi trường: synthetic pure-call negative checks; không có DB/concurrency runtime.
- Bước/lệnh: synthetic calls trong [evidence](evidence/test-output.txt), cùng focused pytest.
- Kỳ vọng: bool không được nhận là integer revision tại begin/complete; stale revision bị reject; mutation concurrent idempotent.
- Thực tế: `begin_offboard(current_revision=1, expected_revision=True, ...)` tạo plan; `complete_offboard(plan.expected_revision=1, current_revision=True, ...)` trả revision 2. Python bool/int equality vượt guard ở cả hai transition. Race/idempotency thật chưa được kiểm chứng.
- Kết quả phản biện: none.
- Tag: need-change
- Kết quả: fail
- Mức độ: major
- Evidence: [reproduction output](evidence/test-output.txt); [source lines/function](../../../../../apps/api/src/agent_corporation_api/modules/hr/contracts.py).
- Xử lý/đề xuất: xác nhận `type(expected_revision) is int` ở begin boundary và `type(current_revision) is int` ở completion boundary trước equality; thêm negative regression tests cho hai canary, sau đó kiểm concurrency/idempotency qua integration.

### P14-06 — Idle và history

- Nguồn/tiêu chí: [checklist P14-06](../../../phases/phase-14.md); roadmap giới hạn idle.
- Bắt buộc: có.
- Điều kiện/môi trường: source contract review; không profile/history store.
- Bước/lệnh: đọc schema `ProbationAssessment`, `OffboardPlan`, focused tests.
- Kỳ vọng: không tự sa thải do idle; assessment/history version có thể truy lại.
- Thực tế: contract không có auto-offboard theo usage/token; `preserve_history=True`; không có profile/version persistence hoặc retrieval proof.
- Kết quả phản biện: none.
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Evidence: [source](../../../../../apps/api/src/agent_corporation_api/modules/hr/contracts.py); [checklist](../../../phases/phase-14.md).
- Xử lý/đề xuất: hoàn thiện versioned profile/history persistence và truy xuất evidence; không kết luận từ idle.

## Integration / release gates

| Gate áp dụng | PASS / FAIL / BLOCKED | Test IDs | Batch/grant/config/evidence và gate trước |
| --- | --- | --- | --- |
| Phase 14: không có IG riêng | BLOCKED | C03, P14-01…P14-06 | Contract foundation only; Phase 13 chưa được chấp nhận; Owner auth/persistence/run stop integration/evidence thiếu; inference grant 0. |

## Cleanup, giới hạn và bàn giao

- Cleanup: không tạo DB/runtime data; fixture là dữ liệu giả; không cleanup cần thiết.
- Chưa kiểm chứng: C03, C06, P14-01…04, P14-06 do demo, Owner auth/persistence, fixed-suite evidence, runtime stop/drain/revoke, race/idempotency và versioned history chưa có.
- Cần sửa: P14-05 major — bool revision bypass tại `begin_offboard` và `complete_offboard`; direct repro đã lưu.
- Đề xuất tùy chọn: không có.
- Blocker summary: Phase 13 chưa nghiệm thu; không có tích hợp Owner authorization/audit persistence; không có execution stop/drain/revoke; không có race/idempotency proof; inference grant = 0. Các blocker không biến contract proof thành end-to-end pass.
- Bước tiếp theo: remake P14-05 và thêm negative tests; retest trên source freeze mới. Chỉ sau đó tiếp tục phần bị chặn khi dependency/quyền phù hợp được cấp.
- Bàn giao: snapshot độc lập lưu tại batch này; kỹ thuật `cần sửa`, không phải Owner acceptance hay phase status change.
