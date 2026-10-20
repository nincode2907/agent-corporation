# Kiểm định Phase 07 — 20261019T102129+0700-r008-test

## Thông tin batch

- Phase: 07
- Vòng: r008
- Test batch: `20261019T102129+0700-r008-test`
- Bắt đầu / kết thúc: 2026-10-19T10:21:29+07:00 / 2026-10-19T10:53:54+07:00
- Người/AI kiểm định: Codex `/root`; kiểm định độc lập `/root/stabilization03_independent`
- Phạm vi: Phase 07 non-inference dependencies, scoped snapshot recovery, gateway checkpoint/no-replay, regression liên quan.
- Source commit: `6c7f7bd`; working tree dirty. Các thay đổi Docker một-compose đang có và UI Lens artifacts của người dùng được giữ nguyên.
- Evidence source: [source manifest](evidence/source-manifest.json); [commands, runtime facts and screenshots](../../../../../docs/reviews/stabilization-03/evidence/commands.md); [browser result](../../../../../docs/reviews/stabilization-03/evidence/browser-result.json); [independent addendum](independent-addendum.md).
- Inference/grant: không gọi inference, không tạo grant, không dispatch run.
- Dependency: Phase 06 vẫn bị chặn bởi CG01/live acceptance. Phase 07 giữ trạng thái **Bị chặn**.
- Supersedes: [Phase 07 r007](../20261018T232151+0700-r007-test/report.md). Remake nguồn: không có; Sprint 03 thêm code và test theo task được giao.
- Kết luận kỹ thuật: **chưa đủ bằng chứng**. Snapshot recovery, offline/stale UI, lease-expiry crash recovery and fake gateway no-replay đạt; real run and actual worker process restart remain blocked.
- Quyết định Chủ tịch: chưa có.

## Mapping criteria

| Tiêu chí / nguồn | Test IDs | Bắt buộc | Phạm vi |
| --- | --- | --- | --- |
| Roadmap Phase 07 AC1: committed event fetch/reconnect đúng sequence, không trùng | P07-01–03 | có | Isolated PostgreSQL/API và browser fixture recovery |
| Roadmap Phase 07 AC2: heartbeat/offline/unknown state minh bạch | P07-04–05 | có | Stale/offline UI được kiểm; actual worker process restart còn mở |
| Roadmap Phase 07 AC3: crash/session recovery, không replay side effect, gap hiển thị | P07-05–07 | có | Fake gateway/checkpoint + browser snapshot fixture; real run blocked |
| Checklist Phase 07 C01–C08 | C01–C08 | có | Đối chiếu diff, contract, tests, scope, docs/evidence |

## Tổng hợp

| Tag | Số test | Result | Số test |
| --- | ---: | --- | ---: |
| clean | 12 | pass | 12 |
| need-change | 3 | fail | 0 |
| suggestion | 0 | blocked | 3 |
|  |  | not-run | 0 |
|  |  | not-applicable | 0 |

Không có lỗi đã tái hiện; `need-change + blocked` là phần kiểm chứng bắt buộc chưa đủ evidence, không phải lỗi đã xác nhận.

## Kết quả từng test

### C01 — Chỉ xử lý scope giao và giữ dirty work khác

- Nguồn/tiêu chí: [C01–C08 trong RULES.md §5](../../../../tests/RULES.md)
- Bắt buộc: có
- Điều kiện/môi trường: isolated PostgreSQL suite và/hoặc Owner-authenticated browser; không inference, không grant.
- Bước/lệnh: xem [commands/evidence](../../../../../docs/reviews/stabilization-03/evidence/commands.md); kết quả ghi tại [batch evidence](evidence/source-manifest.json).
- Kỳ vọng: Chỉ xử lý scope giao và giữ dirty work khác
- Thực tế: Diff gồm snapshot API/UI, ADR và tests; Docker config và user artifacts giữ nguyên; hashes trong manifest
- Kết quả phản biện: none
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [manifest](evidence/source-manifest.json); không stage/commit
- Xử lý/đề xuất: không stage/commit

### C02 — Contract/roadmap dependency được đọc và nhất quán

- Nguồn/tiêu chí: [C01–C08 trong RULES.md §5](../../../../tests/RULES.md)
- Bắt buộc: có
- Điều kiện/môi trường: isolated PostgreSQL suite và/hoặc Owner-authenticated browser; không inference, không grant.
- Bước/lệnh: xem [commands/evidence](../../../../../docs/reviews/stabilization-03/evidence/commands.md); kết quả ghi tại [batch evidence](evidence/source-manifest.json).
- Kỳ vọng: Contract/roadmap dependency được đọc và nhất quán
- Thực tế: ADR-0004, Spec §9, Phase 07 checklist và Sprint 02 r007 đối chiếu; Phase 06 live/CG01 blocker còn nguyên
- Kết quả phản biện: none
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [ADR-0004](../../../../../docs/decisions/0004-scoped-observability-snapshot.md), [Sprint 02](../../../../../docs/reviews/stabilization-02/report.md)
- Xử lý/đề xuất: Không cần sửa; giữ blocker và status theo báo cáo.

### C03 — Mapping đủ AC và demo đúng loại

- Nguồn/tiêu chí: [C01–C08 trong RULES.md §5](../../../../tests/RULES.md)
- Bắt buộc: có
- Điều kiện/môi trường: isolated PostgreSQL suite và/hoặc Owner-authenticated browser; không inference, không grant.
- Bước/lệnh: xem [commands/evidence](../../../../../docs/reviews/stabilization-03/evidence/commands.md); kết quả ghi tại [batch evidence](evidence/source-manifest.json).
- Kỳ vọng: Mapping đủ AC và demo đúng loại
- Thực tế: Snapshot/UI recovery fixture chạy; Phase 07 demo bắt buộc run thật không được chạy vì chưa có grant
- Kết quả phản biện: none
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Evidence: P07-07; cần Owner grant riêng và authorized live test
- Xử lý/đề xuất: cần Owner grant riêng và authorized live test

### C04 — Read path không tự dispatch model/tool

- Nguồn/tiêu chí: [C01–C08 trong RULES.md §5](../../../../tests/RULES.md)
- Bắt buộc: có
- Điều kiện/môi trường: isolated PostgreSQL suite và/hoặc Owner-authenticated browser; không inference, không grant.
- Bước/lệnh: xem [commands/evidence](../../../../../docs/reviews/stabilization-03/evidence/commands.md); kết quả ghi tại [batch evidence](evidence/source-manifest.json).
- Kỳ vọng: Read path không tự dispatch model/tool
- Thực tế: Read-only DB check trước/sau: không có active model calls/Playground turns; browser POST chỉ Owner login/logout; không có run/grant/tool request
- Kết quả phản biện: none
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [commands](../../../../../docs/reviews/stabilization-03/evidence/commands.md), [browser result](../../../../../docs/reviews/stabilization-03/evidence/browser-result.json)
- Xử lý/đề xuất: Không cần sửa; giữ blocker và status theo báo cáo.

### C05 — Scope/secret/privacy boundary giữ nguyên

- Nguồn/tiêu chí: [C01–C08 trong RULES.md §5](../../../../tests/RULES.md)
- Bắt buộc: có
- Điều kiện/môi trường: isolated PostgreSQL suite và/hoặc Owner-authenticated browser; không inference, không grant.
- Bước/lệnh: xem [commands/evidence](../../../../../docs/reviews/stabilization-03/evidence/commands.md); kết quả ghi tại [batch evidence](evidence/source-manifest.json).
- Kỳ vọng: Scope/secret/privacy boundary giữ nguyên
- Thực tế: Snapshot API RLS/scope tests trong disposable PostgreSQL suite; screenshot blur; browser result loại secret/cookie/CSRF/cursor values
- Kết quả phản biện: none
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: P07-03; [browser result](../../../../../docs/reviews/stabilization-03/evidence/browser-result.json)
- Xử lý/đề xuất: [browser result](../../../../../docs/reviews/stabilization-03/evidence/browser-result.json)

### C06 — Docs/HTML đồng bộ, không đổi status

- Nguồn/tiêu chí: [C01–C08 trong RULES.md §5](../../../../tests/RULES.md)
- Bắt buộc: có
- Điều kiện/môi trường: isolated PostgreSQL suite và/hoặc Owner-authenticated browser; không inference, không grant.
- Bước/lệnh: xem [commands/evidence](../../../../../docs/reviews/stabilization-03/evidence/commands.md); kết quả ghi tại [batch evidence](evidence/source-manifest.json).
- Kỳ vọng: Docs/HTML đồng bộ, không đổi status
- Thực tế: Master plan Markdown cập nhật evidence log, HTML render từ Markdown; Phase 07 vẫn Bị chặn
- Kết quả phản biện: none
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [master plan](../../../../../docs/master-plan.md), [roadmap HTML](../../../../../docs/master-plan.html)
- Xử lý/đề xuất: Không cần sửa; giữ blocker và status theo báo cáo.

### C07 — Regression liên quan chạy

- Nguồn/tiêu chí: [C01–C08 trong RULES.md §5](../../../../tests/RULES.md)
- Bắt buộc: có
- Điều kiện/môi trường: isolated PostgreSQL suite và/hoặc Owner-authenticated browser; không inference, không grant.
- Bước/lệnh: xem [commands/evidence](../../../../../docs/reviews/stabilization-03/evidence/commands.md); kết quả ghi tại [batch evidence](evidence/source-manifest.json).
- Kỳ vọng: Regression liên quan chạy
- Thực tế: Isolated API 244 passed, 3 skipped, 1 warning; web production build và Owner browser recovery pass
- Kết quả phản biện: none
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [commands](../../../../../docs/reviews/stabilization-03/evidence/commands.md)
- Xử lý/đề xuất: Không cần sửa; giữ blocker và status theo báo cáo.

### C08 — Evidence đủ để tái kiểm định

- Nguồn/tiêu chí: [C01–C08 trong RULES.md §5](../../../../tests/RULES.md)
- Bắt buộc: có
- Điều kiện/môi trường: isolated PostgreSQL suite và/hoặc Owner-authenticated browser; không inference, không grant.
- Bước/lệnh: xem [commands/evidence](../../../../../docs/reviews/stabilization-03/evidence/commands.md); kết quả ghi tại [batch evidence](evidence/source-manifest.json).
- Kỳ vọng: Evidence đủ để tái kiểm định
- Thực tế: Source hashes, command outcomes, synthetic browser state, screenshots và independent addendum có link
- Kết quả phản biện: none
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [batch evidence](evidence/source-manifest.json), [browser evidence](../../../../../docs/reviews/stabilization-03/evidence/commands.md)
- Xử lý/đề xuất: Không cần sửa; giữ blocker và status theo báo cáo.

### P07-01 — Event chỉ phát sau commit; rollback không lộ; ID/sequence bền

- Nguồn/tiêu chí: [checklist phase-07.md](../../../phases/phase-07.md)
- Bắt buộc: có
- Điều kiện/môi trường: isolated PostgreSQL suite và/hoặc Owner-authenticated browser; không inference, không grant.
- Bước/lệnh: xem [commands/evidence](../../../../../docs/reviews/stabilization-03/evidence/commands.md); kết quả ghi tại [batch evidence](evidence/source-manifest.json).
- Kỳ vọng: Event chỉ phát sau commit; rollback không lộ; ID/sequence bền
- Thực tế: Existing PostgreSQL/SSE rollback and commit correlation tests pass in full isolated suite; snapshot counter/event read is transactionally consistent
- Kết quả phản biện: none
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [independent addendum](independent-addendum.md); `test_stabilization02_observability.py` and new snapshot integration tests
- Xử lý/đề xuất: `test_stabilization02_observability.py` and new snapshot integration tests

### P07-02 — Ordering/reconnect không mất/trùng event

- Nguồn/tiêu chí: [checklist phase-07.md](../../../phases/phase-07.md)
- Bắt buộc: có
- Điều kiện/môi trường: isolated PostgreSQL suite và/hoặc Owner-authenticated browser; không inference, không grant.
- Bước/lệnh: xem [commands/evidence](../../../../../docs/reviews/stabilization-03/evidence/commands.md); kết quả ghi tại [batch evidence](evidence/source-manifest.json).
- Kỳ vọng: Ordering/reconnect không mất/trùng event
- Thực tế: UI fixture loaded watermark 41, applied concurrent #42 once despite duplicate frame, then replaced projection to watermark 43 after out-of-order #44; API feed/cursor tests also pass
- Kết quả phản biện: none
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [browser result](../../../../../docs/reviews/stabilization-03/evidence/browser-result.json); [Replay after recovery desktop](../../../../../docs/reviews/stabilization-03/evidence/screenshots/replay-after-recovery-1440x900.png)
- Xử lý/đề xuất: [Replay after recovery desktop](../../../../../docs/reviews/stabilization-03/evidence/screenshots/replay-after-recovery-1440x900.png)

### P07-03 — Invalid, stale, retention-gap and other-scope cursor are rejected and gap is surfaced

- Nguồn/tiêu chí: [checklist phase-07.md](../../../phases/phase-07.md)
- Bắt buộc: có
- Điều kiện/môi trường: isolated PostgreSQL suite và/hoặc Owner-authenticated browser; không inference, không grant.
- Bước/lệnh: xem [commands/evidence](../../../../../docs/reviews/stabilization-03/evidence/commands.md); kết quả ghi tại [batch evidence](evidence/source-manifest.json).
- Kỳ vọng: Invalid, stale, retention-gap and other-scope cursor are rejected and gap is surfaced
- Thực tế: Disposable DB tests cover signed cursor binding, retention hole, scope and limits; browser shows irrecoverable prefix before #41
- Kết quả phản biện: none
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: `test_stabilization03_snapshot.py`; [Replay mobile](../../../../../docs/reviews/stabilization-03/evidence/screenshots/replay-after-recovery-390x844.png)
- Xử lý/đề xuất: [Replay mobile](../../../../../docs/reviews/stabilization-03/evidence/screenshots/replay-after-recovery-390x844.png)

### P07-04 — Offline/stale state follows heartbeat during interruption and recovers

- Nguồn/tiêu chí: [checklist phase-07.md](../../../phases/phase-07.md)
- Bắt buộc: có
- Điều kiện/môi trường: isolated PostgreSQL suite và/hoặc Owner-authenticated browser; không inference, không grant.
- Bước/lệnh: xem [commands/evidence](../../../../../docs/reviews/stabilization-03/evidence/commands.md); kết quả ghi tại [batch evidence](evidence/source-manifest.json).
- Kỳ vọng: Offline/stale state follows heartbeat during interruption and recovers
- Thực tế: Owner browser on the real read-only SSE feed displayed offline after the held stream was aborted while the browser was offline; after network return the feed reconnected. With the next SSE held, the 31-second stale timer displayed stale; heartbeat restoration returned it to connected. No business write occurred.
- Kết quả phản biện: none
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [browser result](../../../../../docs/reviews/stabilization-03/evidence/browser-result.json), [Replay offline mobile](../../../../../docs/reviews/stabilization-03/evidence/screenshots/replay-offline-390x844.png), [stale desktop](../../../../../docs/reviews/stabilization-03/evidence/screenshots/replay-stale-1440x900.png), [heartbeat recovered](../../../../../docs/reviews/stabilization-03/evidence/screenshots/replay-heartbeat-recovered-1440x900.png)
- Xử lý/đề xuất: No further UI change indicated; actual worker process restart remains P07-05.

### P07-05 — Worker/server restart reconciles checkpoint; unknown outcome is never replayed

- Nguồn/tiêu chí: [checklist phase-07.md](../../../phases/phase-07.md)
- Bắt buộc: có
- Điều kiện/môi trường: isolated PostgreSQL suite và/hoặc Owner-authenticated browser; không inference, không grant.
- Bước/lệnh: xem [commands/evidence](../../../../../docs/reviews/stabilization-03/evidence/commands.md); kết quả ghi tại [batch evidence](evidence/source-manifest.json).
- Kỳ vọng: Worker/server restart reconciles checkpoint; unknown outcome is never replayed
- Thực tế: Disposable suite includes `test_crash_recovery_is_fenced_unknown_and_no_replay` (expired lease, idempotent recovery, late response cannot overwrite unknown, no reservation bypass) and fake gateway 401/403/disconnect checkpoint tests. The prescribed worker process kill/restart itself was not run.
- Kết quả phản biện: none
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Evidence: New parameterized test in `test_phase06_runtime_persistence.py`; restart portion remains open
- Xử lý/đề xuất: restart portion remains open

### P07-06 — Expired/invalid gateway session recovers from app-owned context without silent resend

- Nguồn/tiêu chí: [checklist phase-07.md](../../../phases/phase-07.md)
- Bắt buộc: có
- Điều kiện/môi trường: isolated PostgreSQL suite và/hoặc Owner-authenticated browser; không inference, không grant.
- Bước/lệnh: xem [commands/evidence](../../../../../docs/reviews/stabilization-03/evidence/commands.md); kết quả ghi tại [batch evidence](evidence/source-manifest.json).
- Kỳ vọng: Expired/invalid gateway session recovers from app-owned context without silent resend
- Thực tế: Fake gateway 401/403 and disconnect cases pass; one attempt only; unresolved outcome remains interrupted/unknown with replay disallowed
- Kết quả phản biện: none
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [independent addendum](independent-addendum.md); isolated API suite
- Xử lý/đề xuất: isolated API suite

### P07-07 — Authorized real run reaches UI with matching persisted IDs

- Nguồn/tiêu chí: [checklist phase-07.md](../../../phases/phase-07.md)
- Bắt buộc: có
- Điều kiện/môi trường: isolated PostgreSQL suite và/hoặc Owner-authenticated browser; không inference, không grant.
- Bước/lệnh: xem [commands/evidence](../../../../../docs/reviews/stabilization-03/evidence/commands.md); kết quả ghi tại [batch evidence](evidence/source-manifest.json).
- Kỳ vọng: Authorized real run reaches UI with matching persisted IDs
- Thực tế: Not run; no fresh Phase 07 grant and task explicitly forbids inference
- Kết quả phản biện: none
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Evidence: Requires Owner decision and new phase/batch-specific grant; Phase 06/CG01 evidence is not inherited
- Xử lý/đề xuất: Phase 06/CG01 evidence is not inherited

## Integration / release gate

| Gate | Verdict | IDs | Evidence |
| --- | --- | --- | --- |
| Phase 07 gates | No dedicated IG gate | P07-01–07 | P07-07 live run and P07-05 actual process restart remain blocked; no phase acceptance claimed |

## Cleanup and handoff

- Disposable database/role were cleaned by the isolated runner. Runtime database remained intact; no model calls or Playground turns exist after the browser run. Owner test session logged out.
- Blocked mandatory tests: C03, P07-05 actual process restart, P07-07.
- No code remake is indicated by a failing test. Remaining work needs new test evidence and, for P07-07, an explicit Owner grant. Phase status is unchanged.
