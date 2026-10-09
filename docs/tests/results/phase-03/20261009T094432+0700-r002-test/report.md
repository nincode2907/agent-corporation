# Kiểm định Phase 03 — 20261009T094432+0700-r002-test

## Thông tin batch

- Phase: 03
- Test batch: 20261009T094432+0700-r002-test
- Vòng: r002
- Bắt đầu / kết thúc: 2026-10-09 09:44:32–09:53 +07:00 (Asia/Ho_Chi_Minh; timestamp batch là lúc bắt đầu)
- Người/AI kiểm định: AI độc lập `/root/independent_phase02_03_retest`; khác AI remake `/root`
- Yêu cầu/phạm vi được giao: retest Phase03 sau [remake r001](../../../../remakes/phase-03/20261009T094205+0700-r001-remake/remake.md); không sửa product source, không inference, không restart shared DB/API
- Source: HEAD `e44bc19783e15b29311f467a2be86943b76d847f`, dirty worktree; [manifest/hash](evidence/source-manifest.json)
- Môi trường/config/tool versions: PostgreSQL local fixtures + disposable Postgres 18.6 clean DB, loopback-only Uvicorn test process; no secrets in report
- Inference: không gọi; grant=0
- Dependency/quyết định nghiệm thu: Phase01/02 dependencies; status sources match, formal status remains `Chờ nghiệm thu`
- Supersedes: [legacy report](../20261008T161241+0700-phase-03/report.md)
- Remake nguồn: [r001](../../../../remakes/phase-03/20261009T094205+0700-r001-remake/remake.md)
- Kết luận kỹ thuật: đạt
- Tóm tắt kết luận: toàn bộ test bắt buộc pass, IG03 PASS theo nội dung Phase03 hiện có; không tự nghiệm thu phase
- Quyết định Chủ tịch: Chưa có

## Mapping criteria

| Tiêu chí / nguồn | Test IDs | Bắt buộc | Ghi chú |
| --- | --- | --- | --- |
| AC1 deny invalid transitions, atomic rollback | P03-03, P03-04 | có | History snapshots and direct absence assertions. |
| AC2 no cross-company/environment access | P03-01, P03-05 | có | Composite FK and RLS/scope/pool tests. |
| AC3 dedup/event envelope/redaction | P03-06, P03-07 | có | Concurrent envelope, dedup and canary assertions. |
| Demo persistence task/run/checkpoint/event after backend restart | P03-08 | có | Real Uvicorn process restart on disposable stack. |
| IG03 API/internal command → PostgreSQL integration | P03-01…08 | có | No public domain API claimed; use internal command layer present. |
| C01–C08 | C01–C08 | có | Full checks and evidence links included. |

## Tổng hợp

| Tag | Số test |
| --- | ---: |
| clean | 17 |
| need-change | 0 |
| suggestion | 0 |

| Result | Số test |
| --- | ---: |
| pass | 17 |
| fail | 0 |
| blocked | 0 |
| not-run | 0 |
| not-applicable | 0 |

## Kết quả từng test

### C01 — Scope và diff

- Nguồn/tiêu chí: Yêu cầu remake Phase03; [manifest](evidence/source-manifest.json)
- Bắt buộc: có
- Điều kiện/môi trường: Dirty shared worktree; test code/source only.
- Bước/lệnh: Đối chiếu file list/hash và source phase.
- Kỳ vọng: Chỉ đúng Phase03; không dừng shared DB/API hoặc sửa product source.
- Thực tế: Chỉ test/source đọc và QA artifacts; suite fixtures dùng UUID scope-owned; test containers/process được riêng tạo và cleanup.
- Kết quả phản biện: none
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [manifest](evidence/source-manifest.json), [commands](evidence/commands.md)
- Xử lý/đề xuất: Không cần sửa.

### C02 — Dependency và nguồn quyết định

- Nguồn/tiêu chí: [Master plan](../../../../master-plan.md) Phase03; [AGENTS](../../../../../AGENTS.md)
- Bắt buộc: có
- Điều kiện/môi trường: Phase03 dependency 01,02; status phase ở master plan.
- Bước/lệnh: So status summary/detail, dependency, baseline spec và nhật ký reopen.
- Kỳ vọng: Không mismatch; status không được nâng bởi tester.
- Thực tế: AGENTS/master-plan cùng ghi Phase01–05 Chờ nghiệm thu; phase03 log kể acceptance 08/10 là historical, sau đó reopen có evidence 09/10.
- Kết quả phản biện: none
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [manifest](evidence/source-manifest.json)
- Xử lý/đề xuất: Giữ phase Chờ nghiệm thu.

### C03 — Criteria và demo evidence

- Nguồn/tiêu chí: [Checklist](../../../phases/phase-03.md); [master plan](../../../../master-plan.md) AC Phase03
- Bắt buộc: có
- Điều kiện/môi trường: Fresh disposable Postgres + task/run/checkpoint/events scoped fixture.
- Bước/lệnh: Map AC1→P03-03/04; AC2→P03-01/05; AC3→P03-06/07; seed domain fixture and restart process.
- Kỳ vọng: Mọi AC có test; task/run/checkpoint/event rows persist after backend restart.
- Thực tế: All criteria mapped. Task/event created through internal command; run/checkpoint use fixture SQL; same 1/1/1/2 counts remain after process restart.
- Kết quả phản biện: none
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [P03-08 restart evidence](evidence/P03-08-restart-observation.md)
- Xử lý/đề xuất: No public domain API claimed.

### C04 — Không gọi inference âm thầm

- Nguồn/tiêu chí: [RULES](../../../RULES.md) §5; [main.py](../../../../../apps/api/src/agent_corporation_api/main.py)
- Bắt buộc: có
- Điều kiện/môi trường: Grant=0; disposable PostgreSQL and health API only.
- Bước/lệnh: Read suite/source, create internal task with `max_model_requests=0`; start/restart health-only API.
- Kỳ vọng: No model/tool dispatch.
- Thực tế: No codex-server/model calls; API exposed only health during restart; payload/fixture had no model request budget.
- Kết quả phản biện: none
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [commands](evidence/commands.md), [restart evidence](evidence/P03-08-restart-observation.md)
- Xử lý/đề xuất: Không cần sửa.

### C05 — Isolation và dữ liệu nhạy cảm

- Nguồn/tiêu chí: [RULES](../../../RULES.md) §5; Spec §§7/9/10
- Bắt buộc: có
- Điều kiện/môi trường: UUID-owned fixtures; fake canaries only.
- Bước/lệnh: App-role RLS/missing-scope/pool tests and redaction assertions.
- Kỳ vọng: No cross-scope read/write or secret persistence/log leaks.
- Thực tế: Target suite pass; test source asserts other company/environment invisibility, no-scope read/write deny, pool reset, canary absent from revision/event/log capture.
- Kết quả phản biện: none
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [commands](evidence/commands.md), [manifest](evidence/source-manifest.json)
- Xử lý/đề xuất: Không cần sửa.

### C06 — Tài liệu/HTML và trạng thái

- Nguồn/tiêu chí: [Master plan](../../../../master-plan.md); [renderer](../../../../../scripts/render_plan.py)
- Bắt buộc: có
- Điều kiện/môi trường: After results/README write.
- Bước/lệnh: Render plan, validate reports/links/checklists, inspect phase status.
- Kỳ vọng: HTML mirrors Markdown; no phase status promotion.
- Thực tế: Renderer and validator passed after batch files were written; Phase03 remains Chờ nghiệm thu.
- Kết quả phản biện: none
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [commands](evidence/commands.md)
- Xử lý/đề xuất: Không đổi trạng thái.

### C07 — Regression liên quan

- Nguồn/tiêu chí: [Checklist](../../../phases/phase-03.md)
- Bắt buộc: có
- Điều kiện/môi trường: Target changes are Phase03 persistence test coverage.
- Bước/lệnh: Run target suite on existing local PG and separate clean disposable PG; web build/lint.
- Kỳ vọng: Persistence suite and affected web regression pass.
- Thực tế: 8 passed on shared local database and 8 passed on fresh migrated disposable DB; build and lint pass.
- Kết quả phản biện: none
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [commands](evidence/commands.md)
- Xử lý/đề xuất: Không cần sửa.

### C08 — Report tái kiểm định được

- Nguồn/tiêu chí: [RULES](../../../RULES.md) §5 C08/§7
- Bắt buộc: có
- Điều kiện/môi trường: Dirty revision plus evidence files; test environment disposable.
- Bước/lệnh: Validate ID counts/tags, link targets, manifests and cleanup record.
- Kỳ vọng: Full required IDs and non-sensitive evidence; teardown documented.
- Thực tế: C01–C08 and P03-01…09 present; source hashes, command logs, restart IDs/counts retained; credentials redact; isolated container destroyed.
- Kết quả phản biện: none
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [manifest](evidence/source-manifest.json), [commands](evidence/commands.md), [restart evidence](evidence/P03-08-restart-observation.md)
- Xử lý/đề xuất: Không cần sửa.

### P03-01 — Schema and composite scoped FK

- Nguồn/tiêu chí: [Checklist](../../../phases/phase-03.md) P03-01; Spec §7
- Bắt buộc: có
- Điều kiện/môi trường: PostgreSQL 18.6 migration schema; integration suite on shared and clean disposable DB.
- Bước/lệnh: Run `test_composite_scope_foreign_key_rejects_mismatched_company`.
- Kỳ vọng: Cross-company task/revision composite FK insert denied and transaction rolled back.
- Thực tế: Test passed on both DBs; assertion expects `IntegrityError` from scope mismatch.
- Kết quả phản biện: none
- Tag: clean
- Kết quả: pass
- Mức độ: major
- Evidence: [commands](evidence/commands.md); [test source](../../../../../apps/api/tests/test_phase03_persistence.py)
- Xử lý/đề xuất: Không cần sửa.

### P03-02 — Clean migration durability

- Nguồn/tiêu chí: [Checklist](../../../phases/phase-03.md) P03-02; Spec §7
- Bắt buộc: có
- Điều kiện/môi trường: Fresh disposable database; no shared migrations.
- Bước/lệnh: Alembic upgrade head from empty DB; `current`; app-role persistence tests and independent process after backend restart.
- Kỳ vọng: Migrations reach head cleanly; state remains readable after restart.
- Thực tế: Fresh upgrade ran 0001→0002→0003, current `20261008_0003 (head)`; persistence rows were readable after Uvicorn restart.
- Kết quả phản biện: none
- Tag: clean
- Kết quả: pass
- Mức độ: major
- Evidence: [commands](evidence/commands.md), [restart evidence](evidence/P03-08-restart-observation.md)
- Xử lý/đề xuất: Không cần sửa.

### P03-03 — State/revision invariants

- Nguồn/tiêu chí: [Checklist](../../../phases/phase-03.md) P03-03; Spec §§7/8
- Bắt buộc: có
- Điều kiện/môi trường: Suite uses generated scope-owned fixture.
- Bước/lệnh: Run valid queued transition, invalid transition and stale expected version; compare full history snapshots.
- Kỳ vọng: Invalid/stale transitions deny and leave state/revision/event/outbox histories unchanged.
- Thực tế: Target tests passed; current source snapshots state, revisions, events, outbox and compares unchanged after both denials.
- Kết quả phản biện: none
- Tag: clean
- Kết quả: pass
- Mức độ: major
- Evidence: [commands](evidence/commands.md); [test source](../../../../../apps/api/tests/test_phase03_persistence.py)
- Xử lý/đề xuất: Không cần sửa.

### P03-04 — Atomic rollback state/event/outbox

- Nguồn/tiêu chí: [Checklist](../../../phases/phase-03.md) P03-04; Spec §§7/9
- Bắt buộc: có
- Điều kiện/môi trường: PostgreSQL test-only failure monkeypatch after state write.
- Bước/lệnh: Run injected failure then direct scoped row/count assertions.
- Kỳ vọng: No work order, execution state, revision, event, outbox or sequence-counter row remains.
- Thực tế: Test passed and directly asserts empty results for all six affected row groups.
- Kết quả phản biện: none
- Tag: clean
- Kết quả: pass
- Mức độ: major
- Evidence: [commands](evidence/commands.md); [test source](../../../../../apps/api/tests/test_phase03_persistence.py)
- Xử lý/đề xuất: Không cần sửa.

### P03-05 — RLS/missing scope/pool leakage

- Nguồn/tiêu chí: [Checklist](../../../phases/phase-03.md) P03-05; Spec §§7/10
- Bắt buộc: có
- Điều kiện/môi trường: App role on shared and disposable DBs.
- Bước/lệnh: Check role flags, other company/environment reads, absent-scope write/read, same-connection transaction-local scope reset.
- Kỳ vọng: App role is nonprivileged; reads filter; writes without scope denied; pool has no prior scope leakage.
- Thực tế: Target suite passed twice; explicit query/assertions cover all listed cases.
- Kết quả phản biện: none
- Tag: clean
- Kết quả: pass
- Mức độ: critical
- Evidence: [commands](evidence/commands.md); [test source](../../../../../apps/api/tests/test_phase03_persistence.py)
- Xử lý/đề xuất: Không cần sửa.

### P03-06 — Envelope/dedup/sequence/concurrency

- Nguồn/tiêu chí: [Checklist](../../../phases/phase-03.md) P03-06; Spec §9
- Bắt buộc: có
- Điều kiện/môi trường: Six concurrent writers on fixture company.
- Bước/lệnh: Run concurrent creates and query ordered event stream fields; duplicate key tested in target suite.
- Kỳ vọng: Sequence is contiguous; envelope fields complete; duplicate event does not multiply.
- Thực tế: Test passed on both DBs; asserts 6 unique sequence numbers + schema/type/times/task/run/correlation/source/actor/sensitivity/payload/evidence/dedup metadata. Duplicate command returns same task/event.
- Kết quả phản biện: none
- Tag: clean
- Kết quả: pass
- Mức độ: major
- Evidence: [commands](evidence/commands.md); [test source](../../../../../apps/api/tests/test_phase03_persistence.py)
- Xử lý/đề xuất: Không cần sửa.

### P03-07 — Redaction trước persistence

- Nguồn/tiêu chí: [Checklist](../../../phases/phase-03.md) P03-07; Spec §§9/10
- Bắt buộc: có
- Điều kiện/môi trường: Only synthetic password/API key/Bearer canaries.
- Bước/lệnh: Persist task; query revision/event/outbox and inspect captured logs/redaction helper.
- Kỳ vọng: Canaries absent from durable payloads/logs; no real secrets.
- Thực tế: Test passed; source assertions search three fake canaries through revision/event/outbox projection and logs; fake password is redacted by helper.
- Kết quả phản biện: none
- Tag: clean
- Kết quả: pass
- Mức độ: critical
- Evidence: [commands](evidence/commands.md); [test source](../../../../../apps/api/tests/test_phase03_persistence.py)
- Xử lý/đề xuất: Không cần sửa.

### P03-08 — Restart fixture task/run/checkpoint/events

- Nguồn/tiêu chí: [Checklist](../../../phases/phase-03.md) P03-08; Spec §§7/9
- Bắt buộc: có
- Điều kiện/môi trường: Fresh disposable PG; loopback Uvicorn test process, app-role query after restart.
- Bước/lệnh: Seed task through `create_work_order`; run/state/checkpoint through fixture SQL; append event; start→ready→stop→restart→ready; read scoped IDs.
- Kỳ vọng: Task/run/checkpoint/events persist after an actual backend process restart.
- Thực tế: Readiness healthy before/after; new process returned same counts tasks=1, runs=1, checkpoints=1, events=2 for same fixture IDs. Run/checkpoint rows were seeded directly by migration role because no run creation command exists.
- Kết quả phản biện: none
- Tag: clean
- Kết quả: pass
- Mức độ: major
- Evidence: [restart evidence](evidence/P03-08-restart-observation.md), [commands](evidence/commands.md)
- Xử lý/đề xuất: Pass persistence contract; do not infer public domain HTTP route or run creation path.

### P03-09 — IG03

- Nguồn/tiêu chí: [Checklist](../../../phases/phase-03.md) P03-09; [Product spec](../../../../product-spec.md) §13; ADR §13
- Bắt buộc: có
- Điều kiện/môi trường: grant=0; clean disposable PG; internal work command, target tests and real API process restart; no public domain route assumed.
- Bước/lệnh: Combine P03-01…08: command→PostgreSQL; rollback, restart, dedup, cross-scope deny.
- Kỳ vọng: Gate PASS only with real DB and restart evidence; no mock/inference.
- Thực tế: All required database invariants passed twice; internal `create_work_order` created task/revision/state/event/outbox; backend process restarted and rows persisted; scope deny and dedup tests passed. This satisfies current internal-command/PG gate without claiming a public API.
- Kết quả phản biện: none
- Tag: clean
- Kết quả: pass
- Mức độ: major
- Evidence: [commands](evidence/commands.md), [restart evidence](evidence/P03-08-restart-observation.md)
- Xử lý/đề xuất: IG03 PASS for Phase03 baseline; Phase status remains Chờ nghiệm thu pending Chủ tịch.

## Integration / release gates

| Gate | Verdict | Test IDs | Batch/config/evidence |
| --- | --- | --- | --- |
| IG03 | PASS | C04–C07, P03-01…08 | Batch r002; PostgreSQL 18.6 disposable clean DB; grant=0; real Uvicorn process restart and scoped DB verification; [restart evidence](evidence/P03-08-restart-observation.md). |

## Cleanup, giới hạn và bàn giao

- Cleanup: Uvicorn process dừng; hai disposable PostgreSQL containers `--rm` đã dừng/xóa; không để lại volumes. Shared PG/API không bị stop/restart.
- Chưa kiểm chứng: Không có public domain HTTP route/run creator trong Phase03; test chỉ xác nhận internal command + schema và restart persistence. Không coi health route là domain API.
- Cần sửa: không có finding bắt buộc còn mở trong Phase03 checklist; run/checkpoint fixture setup dùng migration role do không có command phù hợp.
- Đề xuất tùy chọn: Không có.
- Bước tiếp theo: bàn giao report kỹ thuật đạt để Chủ tịch nghiệm thu; **không cập nhật trạng thái phase**.
- Bàn giao: [commands](evidence/commands.md), [restart observation](evidence/P03-08-restart-observation.md), [manifest](evidence/source-manifest.json).
