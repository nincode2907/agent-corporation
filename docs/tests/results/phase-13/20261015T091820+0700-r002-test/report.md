# Kiểm định Phase 13 — 20261015T091820+0700-r002-test

## Thông tin batch

- Phase: 13
- Test batch: 20261015T091820+0700-r002-test
- Vòng: r002
- Bắt đầu / kết thúc: 2026-10-15 09:18:20–09:18:30 +07:00 (Asia/Ho_Chi_Minh)
- Người/AI kiểm định: `/root/phase11_independent_test`, độc lập với implementation/remake agent.
- Yêu cầu/phạm vi: Canonical-format follow-up to r001 so renderer can read case data; rerun focused suite and inspect the current frozen profile contract. No source change/remake in this batch.
- Source: dirty worktree, no commit snapshot; current hashes in [manifest](evidence/source-manifest.json).
- Environment: macOS, Python/uv project `apps/api`; tests are local contracts/fixtures.
- Inference/grant: no inference; grant = 0.
- Dependencies/decisions: Phase 13 depends on Phase 12, not accepted. TDG-CG01 awaits Owner decision; chat foundation 03/06/07/08/10 and Employee Chat send remain gated.
- Supersedes: [Phase 13 r001 report](../20261015T091314+0700-r001-test/report.md) (format follow-up; r001 remains immutable).
- Remake nguồn: No source remake; this batch corrects report structure only.
- Kết luận kỹ thuật: **chưa đủ bằng chứng** — pure profile/organization contracts pass locally; all full app/runtime acceptance remains blocked.
- Quyết định Chủ tịch: Chưa có.

## Mapping tiêu chí

| Criteria hiện tại | Test IDs | Bắt buộc | Coverage |
| --- | --- | --- | --- |
| RULES §5 common checks | C01–C08 | Có | Scope, dependencies, demo, execution/data boundary, docs, regression, reproducibility. |
| AC1: idle profile does not create process/inference | P13-02, P13-05 | Có | Contract lifecycle only; no workload scheduler/runtime. |
| AC2: Owner-only profile change, immutable version/run snapshot and fixed gateway session behavior | P13-03, P13-04 | Có | Frozen Pydantic model/stale version helper tested; no Owner CRUD, run snapshot or session adapter. |
| AC3: acyclic org graph, preserved history/evidence, correct Inspector metrics and no real self-hire | P13-01, P13-06, P13-07 | Có | Graph contract tests pass; history, Inspector, metrics and actual staffing audit absent. |
| Employee Chat EC01–07/10 design added to Phase 13 | P13-03…06 | Có | No conversation/RLS/pins/send/resume implementation; CG01/grant/foundation gates open. |

## Tổng hợp

| Tag | Số |
| --- | ---: |
| clean | 5 |
| need-change | 10 |
| suggestion | 0 |

| Result | Số |
| --- | ---: |
| pass | 5 |
| fail | 0 |
| blocked | 10 |
| not-run | 0 |
| not-applicable | 0 |

## Kết quả từng test

### C01 — Phạm vi và diff

- Nguồn/tiêu chí: RULES §5 C01.
- Bắt buộc: Có.
- Điều kiện/môi trường: Dirty worktree; no commit snapshot.
- Bước/lệnh: `rtk git status --short`; compare [manifest](evidence/source-manifest.json).
- Kỳ vọng: Scope and changed paths identified; no extra phase edits by reviewer.
- Thực tế: Phase 13 contract/test remain untracked; other phase artifacts/docs dirty; reviewer did not edit product source/master-plan.
- Kết quả phản biện: none.
- Tag: clean.
- Kết quả: pass.
- Mức độ: info.
- Evidence: [manifest](evidence/source-manifest.json), [commands](evidence/commands.md).
- Xử lý/đề xuất: None.

### C02 — Dependency và quyết định

- Nguồn/tiêu chí: Phase 13 roadmap/checklist; product spec REQ06/REQ15/REQ27–32; ADR-0001.
- Bắt buộc: Có.
- Điều kiện/môi trường: Current docs/source review.
- Bước/lệnh: Dependency and gate comparison.
- Kỳ vọng: Preserve Phase 12, CG01 and Employee Chat gates; no inferred Owner acceptance.
- Thực tế: Phase 12 is not accepted; TDG-CG01 awaits Owner decision; chat foundation and grant remain gated.
- Kết quả phản biện: none.
- Tag: clean.
- Kết quả: pass.
- Mức độ: info.
- Evidence: [Phase 13 checklist](../../../phases/phase-13.md), [manifest](evidence/source-manifest.json).
- Xử lý/đề xuất: Keep dependencies visible.

### C03 — Đủ tiêu chí và demo

- Nguồn/tiêu chí: RULES §5 C03; Phase 13 demo/acceptance.
- Bắt buộc: Có.
- Điều kiện/môi trường: No profile UI, run snapshot path, or grant.
- Bước/lệnh: Map AC1–3 to P13-01…07.
- Kỳ vọng: Owner changes demo profile; old/new run versions and comparison evidence visible.
- Thực tế: Only pure contracts and unit fixtures; no application demo or run snapshots exist in inspected scope.
- Kết quả phản biện: none.
- Tag: need-change.
- Kết quả: blocked.
- Mức độ: major.
- Evidence: [checklist](../../../phases/phase-13.md), [commands](evidence/commands.md).
- Xử lý/đề xuất: Requires profile/run integration and demo evidence.

### C04 — Không thực thi âm thầm

- Nguồn/tiêu chí: RULES §5 C04.
- Bắt buộc: Có.
- Điều kiện/môi trường: Source trace; no runtime/service.
- Bước/lệnh: Search for organization contract call sites (see [commands](evidence/commands.md)).
- Kỳ vọng: Opening idle profile cannot dispatch inference/tool; counters/network proof when an app path exists.
- Thực tế: Search finds the contract module but no profile CRUD/API caller; no runtime/counter to observe.
- Kết quả phản biện: none.
- Tag: need-change.
- Kết quả: blocked.
- Mức độ: major.
- Evidence: [commands](evidence/commands.md).
- Xử lý/đề xuất: Verify idle view and dispatch counters after integration.

### C05 — Scope và dữ liệu nhạy cảm

- Nguồn/tiêu chí: RULES §5 C05; spec §7/§9 and employee context ACL.
- Bắt buộc: Có.
- Điều kiện/môi trường: No DB/event/log/Inspector surface.
- Bước/lệnh: Inspect scope/ref validators and storage call sites.
- Kỳ vọng: Cross-company/private profile/context data is denied and sensitive content is filtered before persistence/log.
- Thực tế: Contract validates graph scope and opaque refs locally; persistence and event/log surfaces do not exist here, so no canary/ACL proof.
- Kết quả phản biện: none.
- Tag: need-change.
- Kết quả: blocked.
- Mức độ: major.
- Evidence: [manifest](evidence/source-manifest.json), [commands](evidence/commands.md).
- Xử lý/đề xuất: Verify scoped storage and redacted event/log behavior when integrated.

### C06 — Tài liệu và bản nhìn

- Nguồn/tiêu chí: RULES §5 C06; Phase 13 master-plan/checklist.
- Bắt buộc: Có.
- Điều kiện/môi trường: Docs-only source check; no phase status update requested.
- Bước/lệnh: Compare docs and current report status.
- Kỳ vọng: No phase status change; report does not claim acceptance.
- Thực tế: Roadmap status is unchanged; no HTML render is required because no phase status changed.
- Kết quả phản biện: none.
- Tag: clean.
- Kết quả: pass.
- Mức độ: info.
- Evidence: [Phase 13 checklist](../../../phases/phase-13.md), [commands](evidence/commands.md).
- Xử lý/đề xuất: None.

### C07 — Regression liên quan

- Nguồn/tiêu chí: RULES §5 C07; changed organization contract and frozen profile assertion.
- Bắt buộc: Có.
- Điều kiện/môi trường: Local fixture/unit tests only.
- Bước/lệnh: Focused pytest command in [commands](evidence/commands.md).
- Kỳ vọng: Focused Phase 12/13 regressions pass; no DB/runtime.
- Thực tế: 14 passed in 0.08s.
- Kết quả phản biện: none.
- Tag: clean.
- Kết quả: pass.
- Mức độ: info.
- Evidence: [commands](evidence/commands.md).
- Xử lý/đề xuất: No focused test failure.

### C08 — Tái kiểm định và report format

- Nguồn/tiêu chí: RULES §5 C08/§7 and renderer case parser.
- Bắt buộc: Có.
- Điều kiện/môi trường: Canonical report structure for the current renderer.
- Bước/lệnh: Check source hashes, case IDs/fields/links.
- Kỳ vọng: All 15 cases appear as headings with explicit Tag/Result fields and valid evidence links.
- Thực tế: Checker result is recorded in [commands](evidence/commands.md); all case records use canonical fields.
- Kết quả phản biện: none.
- Tag: clean.
- Kết quả: pass.
- Mức độ: info.
- Evidence: [manifest](evidence/source-manifest.json), [commands](evidence/commands.md).
- Xử lý/đề xuất: r001 kept immutable; this follow-up corrects report structure.

### P13-01 — Org integrity

- Nguồn/tiêu chí: Phase 13 checklist P13-01; spec §7.
- Bắt buộc: Có.
- Điều kiện/môi trường: OrganizationSnapshot unit fixtures.
- Bước/lệnh: Focused tests cover department/reporting cycles, dangling references, cross-scope members.
- Kỳ vọng: Deny cycles/cross-company; preserve history when changing/deleting department or reporting lines.
- Thực tế: Graph negatives pass; no DB constraints or history-preserving move/delete implementation to verify.
- Kết quả phản biện: none.
- Tag: need-change.
- Kết quả: blocked.
- Mức độ: major.
- Evidence: [commands](evidence/commands.md), [checklist](../../../phases/phase-13.md).
- Xử lý/đề xuất: Verify persistence/FK/history once organization operations exist.

### P13-02 — Contract/lifecycle

- Nguồn/tiêu chí: Phase 13 checklist P13-02; REQ06/REQ15.
- Bắt buộc: Có.
- Điều kiện/môi trường: Local profile/EmployeeNode contract.
- Bước/lệnh: Focused unit tests.
- Kỳ vọng: Permanent/on-demand/contractor/status semantics; idle is not terminated.
- Thực tế: Contract types and lifecycle enum validate; transitions/workload semantics and UI/DB status assertions absent.
- Kết quả phản biện: none.
- Tag: need-change.
- Kết quả: blocked.
- Mức độ: major.
- Evidence: [commands](evidence/commands.md), [manifest](evidence/source-manifest.json).
- Xử lý/đề xuất: Add lifecycle transitions/persistence assertions in integrated path.

### P13-03 — Immutable profiles

- Nguồn/tiêu chí: Phase 13 checklist P13-03; spec §7/§10.
- Bắt buộc: Có.
- Điều kiện/môi trường: Current frozen Pydantic profile contract and stale version helper.
- Bước/lệnh: Focused pytest plus source check in [commands](evidence/commands.md).
- Kỳ vọng: Used profile cannot mutate; new versions append; only Owner can authorize change.
- Thực tế: `frozen=True` is present and field mutation raises ValidationError; stale version conflicts pass. No Owner-only persistence/API audit exists.
- Kết quả phản biện: none.
- Tag: need-change.
- Kết quả: blocked.
- Mức độ: major.
- Evidence: [commands](evidence/commands.md), [manifest](evidence/source-manifest.json).
- Xử lý/đề xuất: Local immutability is clean; verify Owner authorization and append-only storage after integration.

### P13-04 — Run snapshots

- Nguồn/tiêu chí: Phase 13 checklist P13-04; spec §6/§7.
- Bắt buộc: Có.
- Điều kiện/môi trường: No run/session adapter path.
- Bước/lệnh: Source inventory; no runtime called.
- Kỳ vọng: Old run preserves profile; new run pins latest approved profile; fixed session model/effort causes new session.
- Thực tế: Organization contract is not wired into run snapshot or gateway session adapter.
- Kết quả phản biện: none.
- Tag: need-change.
- Kết quả: blocked.
- Mức độ: major.
- Evidence: [manifest](evidence/source-manifest.json), [checklist](../../../phases/phase-13.md).
- Xử lý/đề xuất: Implement and verify run/profile/session IDs after dependencies.

### P13-05 — Idle không inference

- Nguồn/tiêu chí: Phase 13 checklist P13-05; REQ06.
- Bắt buộc: Có.
- Điều kiện/môi trường: No idle profile UI/scheduler runtime.
- Bước/lệnh: Source review; inference not invoked.
- Kỳ vọng: Idle profile/workload view produces zero background inference.
- Thực tế: No profile workload/scheduler caller exists in this slice; no runtime call counter evidence.
- Kết quả phản biện: none.
- Tag: need-change.
- Kết quả: blocked.
- Mức độ: major.
- Evidence: [commands](evidence/commands.md), [manifest](evidence/source-manifest.json).
- Xử lý/đề xuất: Verify zero-dispatch when idle app path exists, with authorized grant only if required.

### P13-06 — Inspector/org metrics

- Nguồn/tiêu chí: Phase 13 checklist P13-06; spec S03/S07.
- Bắt buộc: Có.
- Điều kiện/môi trường: No Inspector/org metrics UI/query in this contract slice.
- Bước/lệnh: Static source review.
- Kỳ vọng: Workload/evaluation drilldowns correlate to correct profile version; unknown metrics are not invented.
- Thực tế: No Phase 13 Inspector/org metrics view or query path to compare.
- Kết quả phản biện: none.
- Tag: need-change.
- Kết quả: blocked.
- Mức độ: major.
- Evidence: [checklist](../../../phases/phase-13.md), [manifest](evidence/source-manifest.json).
- Xử lý/đề xuất: Needs Inspector queries and profile/run correlation.

### P13-07 — Không CEO/real hire tự phát

- Nguồn/tiêu chí: Phase 13 checklist P13-07; authority boundary in spec §2/§10.
- Bắt buộc: Có.
- Điều kiện/môi trường: Source review only; no DB/create action.
- Bước/lệnh: Search organization contract/call sites; current source findings in [commands](evidence/commands.md).
- Kỳ vọng: No automatic CEO/real staffing; Owner retains decision authority.
- Thực tế: Demo factory is demo-scoped and labels Chief of Staff, but this contract slice has no staffing API/audit surface for full authority verification.
- Kết quả phản biện: none.
- Tag: need-change.
- Kết quả: blocked.
- Mức độ: major.
- Evidence: [commands](evidence/commands.md), [checklist](../../../phases/phase-13.md).
- Xử lý/đề xuất: Verify scope and Owner decision on the actual create/appointment path; do not create real staff.

## Integration / release gates

| Gate | Verdict | Test IDs | Batch/grant/dependency/evidence |
| --- | --- | --- | --- |
| Phase 13 dedicated IG | Không áp dụng | C01–C08, P13-01…07 | No dedicated phase gate; Phase 12 and TDG-CG01/chat foundation gates remain separate and blocked. |

## Cleanup, giới hạn và bàn giao

- Cleanup: Local fixture tests only; no runtime or persisted data.
- Chưa kiểm chứng: C03–C05, P13-01…07; integration paths and dependencies absent.
- Cần sửa: No current source finding in inspected profile contract; r001 mutable-model concern was already fixed before r001 current source snapshot and is not a finding here.
- Đề xuất tùy chọn: None.
- Bước tiếp theo: Wait for Phase 12 acceptance and CG01/foundation decisions; then verify Owner writes, history, snapshots, Inspector and chat gates.
- Bàn giao: r002 is the renderer-compatible report follow-up; source/master-plan status unchanged and Owner acceptance remains absent.
