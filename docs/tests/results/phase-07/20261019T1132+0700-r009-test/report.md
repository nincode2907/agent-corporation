# Kiểm định Phase 07 — 20261019T1132+0700-r009-test

## Batch

- Phase: 07
- Vòng: r009
- Supersedes: [Phase 07 r008](../20261019T102129+0700-r008-test/report.md) for targeted worker process recovery evidence.
- Remake nguồn: Không có; targeted integration follow-up, no product issue was reproduced.
- Scope: non-inference worker process recovery and related regression.
- Source commit: `6c7f7bd`, dirty tree; unrelated pre-existing Docker/UI Lens changes preserved.
- Inference/grant/live run: none. Unique disposable PostgreSQL database/role only.
- Commands: see [batch commands](evidence/commands.md); source hashes: [manifest](evidence/source-manifest.json).
- Technical conclusion: **incomplete evidence**. The real subprocess fake-transport restart path now passes; live authorized Run and network-drop UI remain blocked. Phase status remains **Bị chặn**; no Owner acceptance decision.

## Summary

| Tag | Count | Result |
|---|---:|---|
| clean | 11 | pass |
| need-change | 4 | blocked |
| suggestion | 0 | — |
| fail | 0 | — |

## Cases

| ID | Expected | Actual / evidence | Tag | Result |
|---|---|---|---|---|
| C01 | Stay in assigned scope and preserve dirty work | Only Runtime recovery test, Owner label and Sprint 04 evidence changed; other dirty work retained. `git status` and evidence manifest. | clean | pass |
| C02 | Contract/dependency matches current plan | Phase 07 depends on Phase 06; no acceptance or phase transition. ADR/spec/roadmap and prior batch read. | clean | pass |
| C03 | Required demo is a real authorized Run | No current Owner session/profile and strict CG01 denies; no live Run was authorized. | need-change | blocked |
| C04 | Read paths do not dispatch or replay model/tool actions | Snapshot/recovery tests are read-only; subprocess uses fake coroutine and proves one call row/no second reservation. | clean | pass |
| C05 | Owner scope and sensitive data remain protected | Disposable scoped tests; no credential/prompt saved. | clean | pass |
| C06 | Implementation respects phase boundaries | Only restart evidence and neutral UI label added; no Phase 09/10/11 implementation. | clean | pass |
| C07 | Regression checks pass | Isolated suite 245 passed, 3 skipped, 1 existing warning; web build passed. | clean | pass |
| C08 | Evidence is reproducible and explicit | Synthetic Run/task/request span/event IDs and event order are recorded in `synthetic-runtime-restart.json`. | clean | pass |
| P07-01 | Stored event IDs/sequences remain continuous | Disposable test asserts exact event-type order and sequence 1..counter; API suite passed. | clean | pass |
| P07-02 | Reconnect/cursor recovery does not duplicate or lose state | Snapshot recovery and sequence tests re-ran; live reconnect in this batch was not repeated. Existing Sprint 03 authenticated fixture evidence is linked as regression context. | clean | pass |
| P07-03 | Browser network drop/reconnect recovers the same stream | No authenticated Owner session was available to repeat browser network-drop against a Run. | need-change | blocked |
| P07-04 | Worker heartbeat/stale state is evidenced | Real child worker heartbeat advanced while fake transport was pending; test waited for persisted timestamp. | clean | pass |
| P07-05 | Process crash reconciles without resending unknown call | Child process killed after fake transport entry; fresh worker process recovered expired lease to unknown/interrupted; one call row and no second reservation. | clean | pass |
| P07-06 | Checkpoint/recovery preserves no-replay decision | `before_dispatch` + `dispatch_reserved`, ordered correlated events, unknown usage null, and recovery checkpoint checked. Existing gateway 401/403/disconnect tests re-ran. | clean | pass |
| P07-07 | Real Run traverses saved event/SSE/UI | Strict CG01 currently denies and no Owner grant exists. Mock/process evidence cannot pass this test. | need-change | blocked |

## Remake / retest handoff

No product defect was reproduced. The only code issue found during authoring was a test assertion that expected an incomplete checkpoint list; corrected to assert both checkpoints. An independent reviewer then recommended process cleanup and ordered event assertions; both were added. The final isolated suite and web build passed in implementation and independent verification. Current remaining issues are blocked evidence/Owner dependencies, not code remediation. Phase 07 remains blocked.

## Test records for roadmap renderer

### C01 — Giữ đúng scope và dirty work
- Kỳ vọng: Chỉ sửa scope được giao; không mất thay đổi khác.
- Thực tế: Chỉ thêm Runtime recovery test, nhãn Owner trung tính và Sprint 04 evidence; dirty work khác còn nguyên.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Xử lý/đề xuất: Không stage hoặc commit.

### C02 — Contract và dependency
- Kỳ vọng: Tuân thủ Phase 07 dependency và hợp đồng hiện tại.
- Thực tế: Đối chiếu roadmap, ADR-0003/0004, product spec và batch trước; không đổi phase state.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Xử lý/đề xuất: Giữ phase blocked.

### C03 — Run thật được cấp quyền
- Kỳ vọng: Có Run thật qua UI và event store.
- Thực tế: Runtime hiện strict/blocked; không Owner session/profile hoặc grant mới.
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Xử lý/đề xuất: Chờ quyết định Owner và live test.

### C04 — Read path không dispatch
- Kỳ vọng: Snapshot/Replay read không tạo model/tool action.
- Thực tế: Snapshot tests read-only; subprocess chỉ dùng fake coroutine, một call row và không có reservation thứ hai.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Xử lý/đề xuất: Không cần sửa.

### C05 — Owner scope và dữ liệu nhạy cảm
- Kỳ vọng: Scope cách ly; không lưu credential/prompt ngoài DB test.
- Thực tế: Disposable scoped tests; evidence chỉ chứa synthetic IDs, trạng thái và metadata.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Xử lý/đề xuất: Không cần sửa.

### C06 — Ranh giới phase
- Kỳ vọng: Không tự triển khai phase kế tiếp.
- Thực tế: Không sửa Phase 09/10/11 hoặc CG01; chỉ thêm process evidence trong Phase 07.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Xử lý/đề xuất: Không cần sửa.

### C07 — Regression
- Kỳ vọng: API và web build pass.
- Thực tế: 245 passed, 3 skipped, 1 warning; web build passed.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Xử lý/đề xuất: Warning Starlette deprecation remains existing.

### C08 — Evidence
- Kỳ vọng: IDs and results reproducible and labeled.
- Thực tế: Run/task/request-span/event IDs recorded as synthetic test data.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Xử lý/đề xuất: Keep JSON evidence with batch.

### P07-01 — Event sequence continuity
- Kỳ vọng: Sequence continuous and event order stable.
- Thực tế: Isolated test asserts ordered run events and company sequence 1..counter.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Xử lý/đề xuất: None.

### P07-02 — Cursor/snapshot recovery
- Kỳ vọng: Snapshot recovery preserves sequence and avoids duplicate event replay.
- Thực tế: Isolated snapshot/API suite passed; prior Sprint 03 browser recovery is linked as historical regression evidence.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Xử lý/đề xuất: Fresh live reconnect remains separate.

### P07-03 — Browser stream network drop
- Kỳ vọng: Authenticated UI reconnects to same event history after network loss.
- Thực tế: No authenticated Owner session available to repeat browser network-drop against a Run.
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Xử lý/đề xuất: Repeat after Owner session and Run are available.

### P07-04 — Worker heartbeat
- Kỳ vọng: Pending worker heartbeat is durable.
- Thực tế: Real subprocess heartbeat advanced during pending fake transport.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Xử lý/đề xuất: None.

### P07-05 — Worker process crash/restart
- Kỳ vọng: Unknown outcome is recovered without automatic dispatch.
- Thực tế: Killed process recovered in fresh worker process; one model-call row, unknown usage, interrupted Run and no second reservation.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Xử lý/đề xuất: None for the synthetic path.

### P07-06 — Checkpoint and no replay
- Kỳ vọng: Checkpoint and event correlation make request boundary explicit.
- Thực tế: before_dispatch, dispatch_reserved and interrupted_unknown checkpoints plus ordered events and no-replay policy verified.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Xử lý/đề xuất: Live gateway cancellation remains unproven.

### P07-07 — Live Run event UI
- Kỳ vọng: Real authorized Run appears through committed event feed and UI.
- Thực tế: No grant or live Run; mock cannot pass this criterion.
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Xử lý/đề xuất: Await explicit Owner decision.
