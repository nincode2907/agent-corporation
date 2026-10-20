# Kiểm định Phase 08 — 20261019T1132+0700-r008-test

## Batch

- Phase: 08
- Vòng: r008
- Supersedes: [Phase 08 r007](../20261019T102129+0700-r007-test/report.md) for the targeted scope/read-only and IG08 readiness retest.
- Remake nguồn: No product remake; the neutral Owner access-label follow-up is recorded in this report.
- Scope: non-inference scope/replay checks, UI access-label follow-up and current IG08 blockers.
- Source commit: `6c7f7bd`, dirty tree; unrelated work preserved.
- Inference/grant/live run: none. Owner UI was unauthenticated; user Runtime DB was not used for test writes.
- Commands: see [batch commands](evidence/commands.md); source hashes: [manifest](evidence/source-manifest.json).
- Technical conclusion: **incomplete evidence**. Read-only and scope behavior are verified at API/source level; full authenticated browser side-effect comparison and IG08 remain blocked. Phase status remains **Bị chặn**.

## Summary

| Tag | Count | Result |
|---|---:|---|
| clean | 8 | pass |
| need-change | 7 | blocked |
| suggestion | 0 | — |
| fail | 0 | — |

## Cases

| ID | Expected | Actual / evidence | Tag | Result |
|---|---|---|---|---|
| C01 | Preserve scope and existing changes | Only neutral shell label, Runtime process test and Sprint 04 documents added. | clean | pass |
| C02 | Match Phase 07 dependency and current contract | ADR-0003 keeps Playground separate; ADR-0004 snapshot remains read-only; roadmap dependency unchanged. | clean | pass |
| C03 | Demo uses a real Run, not a fixture | No authenticated active Run; Playground turn cannot substitute. | need-change | blocked |
| C04 | Readiness and Replay never dispatch | Snapshot and event APIs are reads; disposable Runtime test has no network and no tool route. | clean | pass |
| C05 | Cross-company scope/redaction denies data | API scope/RLS tests for events/snapshot pass. No artifact-content route exists. Browser negative actor checks remain unverified. | need-change | blocked |
| C06 | Correctly report implementation and blockers | Traceability report separates Playground, Runtime Run and Work Order queue. | clean | pass |
| C07 | Focused regression/build succeeds | 245 passed, 3 skipped, 1 warning; web production build passed. | clean | pass |
| C08 | Evidence and phase state match findings | IDs labeled synthetic; no phase was accepted or transitioned. | clean | pass |
| P08-01 | Office state comes from an authorized live Run | No live Run; employee-to-Run relation is absent. | need-change | blocked |
| P08-02 | Inspector shows same Run and profile/employee identity | Run event correlation exists; employee/profile-version identity is not stored/projected. | need-change | blocked |
| P08-03 | Replay filter/seek/reload is read-only with DB before/after comparison | Source and snapshot read-only tests pass, but no authenticated UI spy or full DB comparison was run this batch. | need-change | blocked |
| P08-04 | Cross-scope API/SSE/artifact/UI denial is proven | Event snapshot scope tests pass; no artifact-content route exists; authenticated browser negative checks unavailable. | need-change | blocked |
| P08-05 | Explicit outputs do not claim hidden reasoning or missing history | Event projections are redacted/explicit and Replay labels history gaps; no claim of a successful inference output. | clean | pass |
| P08-06 | Offline/stale/unknown usage remains explicit | Runtime recovery verifies unknown usage remains null; prior Sprint 03 Owner-authenticated stale/offline screenshots are historical regression evidence, not a fresh active-Run check. | clean | pass |
| P08-07 | IG08 real text-only Run correlates through event UI | Blocked by strict CG01, no grant, no authenticated session, missing employee projection, and no Work Order executor bridge. | need-change | blocked |

## UI finding and remake

Changed `apps/web/src/App.tsx` to display `Yêu cầu quyền Owner` instead of static `Cần session Owner`. This is a neutral access requirement label and does not reflect session state. Owner session/CSRF/authz behavior was not weakened. Production build passed; current Docker UI was not rebuilt, so rendered Sprint 04 wording is not claimed as runtime-verified.

## Test records for roadmap renderer

### C01 — Giữ scope và thay đổi khác
- Kỳ vọng: Không sửa/xóa dirty work ngoài scope.
- Thực tế: Chỉ neutral label, Runtime process test và Sprint 04 docs thêm mới.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Xử lý/đề xuất: Không stage/commit.

### C02 — Dependency/contract
- Kỳ vọng: Phase 08 giữ dependency Phase 07 và đọc đúng ADR/spec.
- Thực tế: ADR-0003 giữ Playground riêng; ADR-0004 snapshot vẫn read-only; status không đổi.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Xử lý/đề xuất: Không cần sửa.

### C03 — Run thật, không thay bằng fixture
- Kỳ vọng: Run thật làm nguồn Office/Inspector/Replay.
- Thực tế: Không Owner session/Run; Playground turn không có Run ID.
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Xử lý/đề xuất: Chờ live test được Owner duyệt.

### C04 — Read-only
- Kỳ vọng: Load/Replay không dispatch model hoặc tools.
- Thực tế: Snapshot/event APIs đọc; isolated fake worker không có network/tools.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Xử lý/đề xuất: Không cần sửa.

### C05 — Cross-company/sensitive scope
- Kỳ vọng: API/UI chặn scope khác công ty và nội dung nhạy cảm.
- Thực tế: Event/snapshot scope tests pass; không có artifact-content route; browser negative actor checks chưa chạy.
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Xử lý/đề xuất: Cần authenticated browser run cho routes hiện có.

### C06 — Blocker clarity
- Kỳ vọng: Mô tả đúng đường thực thi và phần thiếu.
- Thực tế: Traceability tách Playground, direct Runtime Run và Work Order queue; employee profile link/queue bridge ghi rõ.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Xử lý/đề xuất: Không cần sửa.

### C07 — Regression/build
- Kỳ vọng: Suite/build pass.
- Thực tế: 245 passed, 3 skipped, 1 warning; web build passed.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Xử lý/đề xuất: Warning Starlette deprecation remains existing.

### C08 — Evidence and phase state
- Kỳ vọng: Evidence reflects test data; no automatic acceptance.
- Thực tế: Run IDs labeled synthetic; Phase 08 remains blocked.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Xử lý/đề xuất: Await Owner decision.

### P08-01 — Office event state
- Kỳ vọng: Office shows active employee and accurate state from an authorized Run.
- Thực tế: No authorized Run; Runtime has no employee relation/projection.
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Xử lý/đề xuất: Requires approved employee-to-Run contract and live test.

### P08-02 — Inspector correlation/profile
- Kỳ vọng: Same Run and employee/profile-version identity across entry points.
- Thực tế: Run/event IDs correlate; employee/profile version identity is not exposed in the Run projection.
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Xử lý/đề xuất: Requires model/read projection decision; no fixture substitution.

### P08-03 — Replay side effects
- Kỳ vọng: Filters/seek/reload leave DB unchanged and call counts at zero.
- Thực tế: Snapshot reads are covered; no authenticated UI request spy plus DB before/after was run in r008.
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Xử lý/đề xuất: Run full authenticated read-only browser comparison.

### P08-04 — Scope-negative routes
- Kỳ vọng: Other-company requests are denied/redacted on implemented API/SSE/artifact/UI paths.
- Thực tế: API event/snapshot scope tests pass; no artifact-content route; browser checks unavailable.
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Xử lý/đề xuất: Test current routes with authenticated actors; do not invent artifact endpoint.

### P08-05 — Explicit summary and history gaps
- Kỳ vọng: No hidden reasoning claims or fabricated missing history.
- Thực tế: Public event projection redacts fields; Replay displays history gaps; no live output is claimed.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Xử lý/đề xuất: None.

### P08-06 — Offline/unknown usage
- Kỳ vọng: Unknown values remain explicit during recovery.
- Thực tế: Runtime restart test retains unknown usage as null; prior authenticated Sprint 03 evidence covers offline/stale UI states.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Xử lý/đề xuất: Fresh active-Run UI evidence remains open.

### P08-07 — IG08
- Kỳ vọng: Live text-only Run through saved events/SSE/Office/Inspector/Replay.
- Thực tế: Strict CG01 denies; no grant; no current Owner session; employee projection and Work Order executor bridge absent.
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Xử lý/đề xuất: Separate Owner decision and scoped grant proposal is prepared; no grant or prompt sent.
