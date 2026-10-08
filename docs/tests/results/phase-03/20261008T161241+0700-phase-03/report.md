# Kiểm định Phase 03 — 20261008T161241+0700-phase-03

## Thông tin batch

- Phase: 03
- Test batch: 20261008T161241+0700-phase-03
- Bắt đầu / kết thúc: 2026-10-08T16:12:41+07:00 / 2026-10-08T16:12:41+07:00 (Asia/Ho_Chi_Minh)
- Người/AI kiểm định: Codex
- Yêu cầu/phạm vi được giao: User yêu cầu “test phase 2 + 3”; batch này chỉ kiểm định Phase 03.
- Source: commit `edb550c`; worktree dirty, các thay đổi owner được giữ nguyên; [manifest/hash/file list](evidence/source-manifest.json).
- Môi trường/config/tool versions: Web `127.0.0.1:15500`; API `127.0.0.1:15501`; PostgreSQL `127.0.0.1:15510`; readiness ok; migration head `20261008_0003`; [commands](evidence/commands.md).
- Inference: Không gọi; grant=0. Không probe gateway, reset fixture hoặc tạo task/run qua UI.
- Dependency/quyết định nghiệm thu: Phase 00–03 ghi Hoàn tất trong master plan; AGENTS.md hướng dẫn Phase 04 đang triển khai nhưng master-plan ghi Chờ nghiệm thu — được ghi ở C02. Không cập nhật trạng thái.
- Supersedes: Không có.
- Kết luận kỹ thuật: cần sửa
- Quyết định Chủ tịch: Chưa có.

## Mapping và phạm vi kiểm định

| Tiêu chí hiện tại / nguồn | Test IDs | Bắt buộc / tùy điều kiện | Ghi chú |
| --- | --- | --- | --- |
| AC1 | Chuyển trạng thái sai bị từ chối; event và state không lệch do transaction thất bại. | P03-03, P03-04 | Bắt buộc |
| AC2 | Query khác company/environment không đọc được dữ liệu ngoài phạm vi. | P03-01, P03-05 | Bắt buộc |
| AC3 | Event trùng không nhân đôi; secret thử nghiệm được lọc trước persistence. | P03-06, P03-07 | Bắt buộc |
| Kiểm tra chung theo RULES.md §§5–7 | C01–C08 | Bắt buộc | Từng record bên dưới. |

## Tổng hợp

| Tag | Số test |
| --- | --- |
| clean | 6 |
| need-change | 11 |
| suggestion | 0 |

| Result | Số test |
| --- | --- |
| pass | 6 |
| fail | 1 |
| blocked | 10 |
| not-run | 0 |
| not-applicable | 0 |

## Kết quả từng test

### C01 — Phạm vi và diff

- Nguồn/tiêu chí: Chỉ thị kiểm định Phase 02 + 03; root AGENTS.md § phase
- Bắt buộc: có
- Điều kiện/môi trường: Runtime local read-only; Phase 03 persistence test dùng UUID fixture/teardown riêng khi có liên quan.
- Bước/lệnh: Đối chiếu git status/diff; không sửa source hoặc chuyển phase.
- Kỳ vọng: Chỉ kiểm tra phase được giao; preserve owner changes.
- Thực tế: Worktree dirty tại App/UI/API/Phase 04 và docs/remakes; không chỉnh sửa trong batch. Commit nền edb550c.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [evidence](evidence/commands.md)
- Xử lý/đề xuất: Không cần xử lý.
### C02 — Dependency và nguồn quyết định

- Nguồn/tiêu chí: docs/master-plan.md §6; AGENTS.md Phase/owner guidance
- Bắt buộc: có
- Điều kiện/môi trường: Runtime local read-only; Phase 03 persistence test dùng UUID fixture/teardown riêng khi có liên quan.
- Bước/lệnh: So sánh trạng thái roadmap với hướng dẫn vận hành được cung cấp.
- Kỳ vọng: Phase 00–03 complete và nguồn Phase 04 đồng nhất.
- Thực tế: Phase 00–03 complete. AGENTS.md ghi Phase 04 đang triển khai; master-plan.md ghi Phase 04 chờ nghiệm thu. Master plan là nguồn trạng thái chuẩn; mismatch được ghi nhận.
- Tag: need-change
- Kết quả: fail
- Mức độ: minor
- Evidence: [evidence](evidence/commands.md)
- Xử lý/đề xuất: Chủ tịch đồng bộ trạng thái giữa nguồn hướng dẫn và roadmap; không chỉnh nguồn chính thức trong batch này.
### C03 — Đủ criteria và demo

- Nguồn/tiêu chí: phase-03.md Mapping/AC1–3; master-plan Phase 03
- Bắt buộc: có
- Điều kiện/môi trường: Runtime local read-only; Phase 03 persistence test dùng UUID fixture/teardown riêng khi có liên quan.
- Bước/lệnh: Map AC1→P03-03/04, AC2→P03-01/05, AC3→P03-06/07; đối chiếu demo task/run/events với restart case.
- Kỳ vọng: AC có test; demo task/run/event tồn tại sau restart backend.
- Thực tế: Mapping đầy đủ; test DB thực hiện được một phần. Không restart backend đang dùng và test file không tạo run/checkpoint; phần demo bắt buộc chưa được chứng minh.
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Evidence: [evidence](evidence/commands.md)
- Xử lý/đề xuất: Chạy test restart/data fixture trên backend test cô lập và đưa run/checkpoint vào fixture.
### C04 — Không thực thi âm thầm

- Nguồn/tiêu chí: RULES.md C04; test_phase03_persistence.py; App.tsx
- Bắt buộc: có
- Điều kiện/môi trường: Runtime local read-only; Phase 03 persistence test dùng UUID fixture/teardown riêng khi có liên quan.
- Bước/lệnh: Review test calls/source; kiểm tra UI mở không gọi probe/reset/model.
- Kỳ vọng: Không có inference/tool dispatch khi chạy test Phase 03 hoặc mở UI.
- Thực tế: Pytest chỉ gọi internal commands/DB; UI không bấm probe/reset; inference grant 0.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [evidence](evidence/commands.md)
- Xử lý/đề xuất: Không cần xử lý.
### C05 — Scope và dữ liệu nhạy cảm

- Nguồn/tiêu chí: RULES.md C05; test_phase03_persistence.py teardown
- Bắt buộc: có
- Điều kiện/môi trường: Runtime local read-only; Phase 03 persistence test dùng UUID fixture/teardown riêng khi có liên quan.
- Bước/lệnh: Review setup/teardown và canary; xác nhận health DB trước khi test.
- Kỳ vọng: Không tiết lộ secret thật; ghi/xóa fixture chỉ trong UUID environment mới.
- Thực tế: Teardown lọc theo hai environment UUID tạo trong fixture; canary giả được assert redacted ở revision/event. Readiness ok trước test, không đọc .env.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [evidence](evidence/commands.md)
- Xử lý/đề xuất: Không cần xử lý.
### C06 — Tài liệu và bản nhìn

- Nguồn/tiêu chí: RULES.md C06; phase-03.md; migration
- Bắt buộc: có
- Điều kiện/môi trường: Runtime local read-only; Phase 03 persistence test dùng UUID fixture/teardown riêng khi có liên quan.
- Bước/lệnh: Chạy alembic current (read-only), build web; validate docs/report sau khi lưu.
- Kỳ vọng: Không nâng cấp schema trong test; tài liệu refs hợp lệ; không nâng trạng thái phase.
- Thực tế: Alembic current=20261008_0003 (head); web build pass. Chỉ đọc current, không chạy upgrade/downgrade. Validator theo batch kiểm cấu trúc và links, không proof sản phẩm; toàn repo hiện fail ở report Phase 04 ngoài scope vì verdict bọc markdown.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [evidence](evidence/commands.md)
- Xử lý/đề xuất: Không cần xử lý.
### C07 — Regression liên quan

- Nguồn/tiêu chí: RULES.md C07; Phase 03 dependencies 01/02
- Bắt buộc: có
- Điều kiện/môi trường: Runtime local read-only; Phase 03 persistence test dùng UUID fixture/teardown riêng khi có liên quan.
- Bước/lệnh: Chạy test_phase03_persistence.py và web build; không chạy full suite.
- Kỳ vọng: Persistence/scope/redaction regression không ảnh hưởng runtime khác.
- Thực tế: 5/5 persistence tests pass; web build pass; full API suite không chạy để tránh Phase 04 fixture/test scope chưa audit.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [evidence](evidence/commands.md)
- Xử lý/đề xuất: Không cần xử lý.
### C08 — Có thể tái kiểm định

- Nguồn/tiêu chí: RULES.md C08; fixture source and report
- Bắt buộc: có
- Điều kiện/môi trường: Runtime local read-only; Phase 03 persistence test dùng UUID fixture/teardown riêng khi có liên quan.
- Bước/lệnh: Lưu exact commands, test output, migration current, hash manifest, fixture cleanup description.
- Kỳ vọng: Evidence có scope, no secrets, tags/results and links validate.
- Thực tế: Test output `5 passed in 1.38s`; environment-specific rows cleanup in fixture teardown; manifest filtered.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [evidence](evidence/commands.md)
- Xử lý/đề xuất: Không cần xử lý.
### P03-01 — Schema và scoped FK

- Nguồn/tiêu chí: phase-03.md P03-01; product-spec §7; migration 0002
- Bắt buộc: có
- Điều kiện/môi trường: Runtime local read-only; Phase 03 persistence test dùng UUID fixture/teardown riêng khi có liên quan.
- Bước/lệnh: Review migration entities/FKs and run scoped RLS read tests; no deliberately invalid insert.
- Kỳ vọng: Composite scoped constraints and negative cross-scope insert denial verified.
- Thực tế: Test verifies cross-company/environment reads return empty; migration review only. Negative INSERT/FK constraint assertion not executed.
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Evidence: [evidence](evidence/phase03-test-observations.md)
- Xử lý/đề xuất: Add/run negative composite-FK inserts in disposable DB fixture; retain catalog evidence.
### P03-02 — Migration bền vững

- Nguồn/tiêu chí: phase-03.md P03-02; product-spec §7
- Bắt buộc: có
- Điều kiện/môi trường: Runtime local read-only; Phase 03 persistence test dùng UUID fixture/teardown riêng khi có liên quan.
- Bước/lệnh: Run read-only alembic current; no clean DB upgrade or backend restart.
- Kỳ vọng: Clean upgrade reaches expected head and baseline data/history persist across restart.
- Thực tế: Current DB is 20261008_0003 head. No clean database, migration upgrade, baseline count/hash, or backend restart test was run.
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Evidence: [evidence](evidence/phase03-test-observations.md)
- Xử lý/đề xuất: Use isolated disposable PostgreSQL for upgrade and restart persistence test.
### P03-03 — State/revision

- Nguồn/tiêu chí: phase-03.md P03-03; product-spec §7/8
- Bắt buộc: có
- Điều kiện/môi trường: Runtime local read-only; Phase 03 persistence test dùng UUID fixture/teardown riêng khi có liên quan.
- Bước/lệnh: Run target pytest valid transition, invalid transition and stale version; inspect final state.
- Kỳ vọng: Invalid/stale transition denied without mutating state, revision, or event history.
- Thực tế: Test passes: draft→queued version 2; InvalidTaskTransition and StaleTaskState raised; final state remains queued/version 2. Revision/event history before/after invalid attempts is not asserted.
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Evidence: [evidence](evidence/phase03-test-observations.md)
- Xử lý/đề xuất: Extend assertions to compare revision/event counts and run negative cases.
### P03-04 — Atomic state/event/outbox

- Nguồn/tiêu chí: phase-03.md P03-04; product-spec §7/9
- Bắt buộc: có
- Điều kiện/môi trường: Runtime local read-only; Phase 03 persistence test dùng UUID fixture/teardown riêng khi có liên quan.
- Bước/lệnh: Run injected append_event exception after state write; inspect assertions in test.
- Kỳ vọng: Rollback removes work order, revision, execution state, event, outbox row and sequence counter.
- Thực tế: Injected error test passes and asserts no work_order, task state, or counter. It does not assert revision/event/outbox rows directly.
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Evidence: [evidence](evidence/phase03-test-observations.md)
- Xử lý/đề xuất: Add direct absence assertions for task_revisions/events/outbox_events, then rerun on scoped fixture.
### P03-05 — RLS và scope

- Nguồn/tiêu chí: phase-03.md P03-05; product-spec §7/10
- Bắt buộc: có
- Điều kiện/môi trường: Runtime local read-only; Phase 03 persistence test dùng UUID fixture/teardown riêng khi có liên quan.
- Bước/lệnh: Run tests under app role for rol flags and cross-company/environment SELECT.
- Kỳ vọng: No-scope and cross-scope read/write denied; connection pool does not leak scope.
- Thực tế: Test confirms app role non-super/non-bypass and cross-company/environment reads filtered. Missing-scope writes/query and reused-connection scope leakage were not exercised.
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Evidence: [evidence](evidence/phase03-test-observations.md)
- Xử lý/đề xuất: Add missing-scope read/write and connection-reuse isolation cases.
### P03-06 — Envelope/dedup/sequence

- Nguồn/tiêu chí: phase-03.md P03-06; product-spec §9
- Bắt buộc: có
- Điều kiện/môi trường: Runtime local read-only; Phase 03 persistence test dùng UUID fixture/teardown riêng khi có liên quan.
- Bước/lệnh: Run duplicate create and read state/event/outbox over fresh connection; no concurrency load.
- Kỳ vọng: Dedup stable, sequence order correct under concurrent writers, envelope metadata complete.
- Thực tế: Duplicate resolves same work_order/event; first stream_seq=1; fresh connection sees committed state/event/outbox. No concurrent writers or complete envelope field assertions.
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Evidence: [evidence](evidence/phase03-test-observations.md)
- Xử lý/đề xuất: Add concurrent same-company writers and assert IDs/timestamps/correlation/parent/sensitivity/ordered sequence.
### P03-07 — Redaction trước lưu

- Nguồn/tiêu chí: phase-03.md P03-07; product-spec §9/10
- Bắt buộc: có
- Điều kiện/môi trường: Runtime local read-only; Phase 03 persistence test dùng UUID fixture/teardown riêng khi có liên quan.
- Bước/lệnh: Run fake password/API-key/Bearer canary and inspect revision/event assertions.
- Kỳ vọng: Secret canaries absent from revision, event, outbox and logs.
- Thực tế: Test confirms fake password/key/Bearer absent from revision and event plus redaction helper. Outbox and log sinks are not asserted.
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Evidence: [evidence](evidence/phase03-test-observations.md)
- Xử lý/đề xuất: Extend canary assertions to outbox and captured logs.
### P03-08 — Restart demo fixture

- Nguồn/tiêu chí: phase-03.md P03-08; product-spec §7/9
- Bắt buộc: có
- Điều kiện/môi trường: Runtime local read-only; Phase 03 persistence test dùng UUID fixture/teardown riêng khi có liên quan.
- Bước/lệnh: Check readiness and test scope; no stop/restart of shared API/DB.
- Kỳ vọng: Task, run, checkpoint and events remain after backend restart.
- Thực tế: No isolated backend available for this batch; live API was left running. Target fixture creates a work order but not run/checkpoint and no restart occurred.
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Evidence: [evidence](evidence/phase03-test-observations.md)
- Xử lý/đề xuất: Run restart test with separate backend process and disposable fixture; do not restart shared service.
### P03-09 — IG03

- Nguồn/tiêu chí: phase-03.md IG03; product-spec §13
- Bắt buộc: có
- Điều kiện/môi trường: Runtime local read-only; Phase 03 persistence test dùng UUID fixture/teardown riêng khi có liên quan.
- Bước/lệnh: Assess real DB test evidence for internal command layer and required rollback/restart/dedup/cross-scope.
- Kỳ vọng: Gate PASS only with DB evidence including restart/recovery requirements.
- Thực tế: Real PostgreSQL integration test passed dedup/rollback/cross-scope/state/redaction cases; restart persistence is missing, so IG03 cannot pass.
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Evidence: [evidence](evidence/phase03-test-observations.md)
- Xử lý/đề xuất: Complete P03-08 in isolated runtime and link new evidence; no inference required.
## Integration / release gates

| Gate áp dụng | Kết quả | Test IDs | Batch/grant/config/evidence và gate trước |
| --- | --- | --- | --- |
| IG03 | BLOCKED | P03-01, P03-02, P03-04, P03-05, P03-06, P03-07, P03-08 | [Evidence/commands](evidence/commands.md); DB thật và grant=0; restart backend test còn thiếu. |

## Cleanup, giới hạn và bàn giao

- Cleanup: Pytest teardown đã xóa domain rows/environment chỉ thuộc hai UUID fixture mới; giữ evidence. Không restart/stop DB/API.
- Chưa kiểm chứng: P03-01…P03-09 đều còn một hoặc nhiều assertion/runtime requirement thiếu như từng record; IG03 BLOCKED. C02 có mismatch trạng thái roadmap/hướng dẫn.
- Cần sửa: C02 cần đồng bộ Phase 04 giữa hướng dẫn và roadmap. Các P03 `blocked` là thiếu coverage/evidence, chưa xác nhận lỗi implementation.
- Đề xuất tùy chọn: Không có.
- Bàn giao: [test commands/output](evidence/commands.md), [fixture boundary](evidence/fixture-cleanup.md), [source manifest](evidence/source-manifest.json). Không nghiệm thu thay Chủ tịch.
