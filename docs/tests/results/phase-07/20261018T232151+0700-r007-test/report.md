# Kiểm định Phase 07 — 20261018T232151+0700-r007-test

## Thông tin batch

- Phase: 07
- Test batch: 20261018T232151+0700-r007-test
- Vòng: r007
- Bắt đầu / kết thúc: 2026-10-18 23:21:51–23:37:56 +07:00 (Asia/Ho_Chi_Minh)
- Người/AI kiểm định: Codex `/root`; không có AI test độc lập khác trong môi trường này.
- Độc lập với AI triển khai/remake: không độc lập; đây là lượt kiểm định do cùng agent thực hiện. Không dùng kết quả này làm nghiệm thu.
- Yêu cầu/phạm vi: Agent Corporation Stabilization Sprint 02; Phase 07 evidence closure không inference.
- Source: `main`, worktree dirty; source hashes ở [manifest](evidence/source-manifest.json).
- Môi trường: local Phase 01 runtime, Owner test session, isolated disposable PostgreSQL cho API tests; Chromium 156.0.8078.4.
- Inference: không gọi; không grant/run/worker dispatch.
- Dependency/quyết định: retention snapshot contract và gateway-session recovery còn mở.
- Supersedes: [r006](../20261018T221600+0700-r006-test/report.md).
- Remake nguồn: không có remake sản phẩm trong Sprint 02; chỉ sửa test/evidence harness.
- Kết luận kỹ thuật: chưa đủ bằng chứng.
- Quyết định Chủ tịch: chưa có; AI không nghiệm thu phase.

## Mapping và tổng hợp

| Criteria | Test IDs | Ghi chú |
| --- | --- | --- |
| AC1 committed ordering, reconnect, gap | P07-01, P07-02, P07-03 | P07-02 evidence carried forward; gap lacks snapshot recovery. |
| AC2 heartbeat/offline/unknown | P07-04, P07-05 | Offline/stale observed; live idle/waiting run not exercised. |
| AC3 crash/context/session/replay safety | P07-05, P07-06, P07-07 | Fake crash covered; expired gateway session and live run remain open. |
| Test governance and evidence | C01–C08 | Scope, source, cleanup, proof traceability. |

| Tag | Số test |
| --- | ---: |
| clean | 10 |
| need-change | 5 |
| suggestion | 0 |

| Result | Số test |
| --- | ---: |
| pass | 10 |
| fail | 0 |
| blocked | 5 |
| not-run | 0 |
| not-applicable | 0 |

## Kết quả từng test

### C01 — Scope và worktree

- Nguồn/tiêu chí: Sprint 02 brief; `docs/tests/RULES.md`.
- Bắt buộc: có.
- Điều kiện/môi trường: worktree hiện có dirty changes từ Sprint01.
- Bước/lệnh: kiểm tra git status, source diff và evidence mới; không commit/push.
- Kỳ vọng: bảo toàn thay đổi có trước, không sửa code sản phẩm/phase ngoài scope.
- Thực tế: Sprint02 thêm test/evidence/docs; không chỉnh runtime sản phẩm. Thay đổi trước đó được giữ.
- Kết quả phản biện: none.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [Sprint02 report](../../../../reviews/stabilization-02/report.md), source manifest.
- Xử lý/đề xuất: không cần.

### C02 — Dependencies và phase boundary

- Nguồn/tiêu chí: `docs/master-plan.md`, `docs/tests/phases/phase-07.md`.
- Bắt buộc: có.
- Điều kiện/môi trường: đối chiếu r006 và spec; không inference.
- Bước/lệnh: đọc dependency/CG01/grant state; không đổi phase status.
- Kỳ vọng: không mở Phase 08/11 bằng suy luận hoặc Phase 00 acceptance.
- Thực tế: P07 live run vẫn phụ thuộc Owner grant/CG01; status không đổi.
- Kết quả phản biện: none.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [master plan](../../../../master-plan.md), [r006](../20261018T221600+0700-r006-test/report.md).
- Xử lý/đề xuất: giữ gate.

### C03 — Criteria mapping

- Nguồn/tiêu chí: Phase 07 AC1–3; checklist `phase-07.md`.
- Bắt buộc: có.
- Điều kiện/môi trường: r007 test/evidence.
- Bước/lệnh: ánh xạ C01–C08 và P07-01…07.
- Kỳ vọng: không bỏ case bắt buộc.
- Thực tế: toàn bộ AC và 7 test IDs được liệt kê; P07-03/06/07 thiếu evidence bắt buộc.
- Kết quả phản biện: none.
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Evidence: batch report và Sprint02 report.
- Xử lý/đề xuất: hoàn tất blocker tại P07-03/06/07 trước khi xin nghiệm thu.

### C04 — No silent execution

- Nguồn/tiêu chí: `phase-07.md`, V1 runtime boundary.
- Bắt buộc: có.
- Điều kiện/môi trường: browser Owner session; API tests dùng fixture.
- Bước/lệnh: đọc manifest HTTP method/path; replay/test feed chỉ đọc; kiểm tra isolated suite.
- Kỳ vọng: không gọi model/tool, tạo run hoặc grant.
- Thực tế: browser POST chỉ login/logout; không có request gateway/run/grant/send; không inference.
- Kết quả phản biện: none.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: `../../../../reviews/stabilization-02/evidence/authenticated-fresh/manifest.json`.
- Xử lý/đề xuất: không cần.

### C05 — Scope, redaction, cursor authorization

- Nguồn/tiêu chí: Phase 07 AC3; API feed scope contract.
- Bắt buộc: có.
- Điều kiện/môi trường: disposable DB; Owner test principal; company fixtures tổng hợp.
- Bước/lệnh: test HTTP GET scoped feed; cursor hợp lệ/tamper/expiry/cross-scope.
- Kỳ vọng: không rò event ngoài scope; cursor sai bị từ chối.
- Thực tế: GET chỉ trả scope Owner; cursor tamper/expired/khác scope HTTP 400; no inference.
- Kết quả phản biện: none.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: `apps/api/tests/test_stabilization02_observability.py`, command evidence.
- Xử lý/đề xuất: browser second-actor negative remains Phase08 coverage.

### C06 — Traceable evidence

- Nguồn/tiêu chí: `docs/tests/RULES.md`.
- Bắt buộc: có.
- Điều kiện/môi trường: sanitized evidence package.
- Bước/lệnh: manifest, screenshots, contact sheet, zip packaging.
- Kỳ vọng: reproducible paths, no secrets/request bodies.
- Thực tế: 18 viewport screenshots + 3 state screenshots; method/path only; Owner logout observed.
- Kết quả phản biện: none.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: `../../../reviews/stabilization-02/evidence/authenticated-fresh/inventory.md`, ZIP.
- Xử lý/đề xuất: Gemini consultation not performed.

### C07 — Regression suite

- Nguồn/tiêu chí: Phase 07; test rules.
- Bắt buộc: có.
- Điều kiện/môi trường: isolated PostgreSQL via test runner.
- Bước/lệnh: `rtk proxy uv run --project apps/api python -X utf8 scripts/test_playground_isolated.py`.
- Kỳ vọng: suite hoàn tất; disposable DB/role được dọn.
- Thực tế: 145 passed, 11 skipped, 1 warning; exit 0; cleanup runner hoàn tất.
- Kết quả phản biện: none.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [commands](evidence/commands.md).
- Xử lý/đề xuất: warning deprecation được ghi nhận.

### C08 — Phase/status/report integrity

- Nguồn/tiêu chí: master-plan source of truth; Rules.
- Bắt buộc: có.
- Điều kiện/môi trường: Markdown source.
- Bước/lệnh: ghi batch mới, không tự nghiệm thu; render plan sau khi cập nhật master.
- Kỳ vọng: giữ statuses và lịch sử trước.
- Thực tế: status vẫn giữ nguyên; r001–r006 được giữ.
- Kết quả phản biện: none.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: master plan, phase README.
- Xử lý/đề xuất: render HTML sau master update.

### P07-01 — Commit trước khi phát SSE

- Nguồn/tiêu chí: Phase 07 P07-01; Product Spec §9.
- Bắt buộc: có.
- Điều kiện/môi trường: isolated PostgreSQL, actual application event page/SSE frame.
- Bước/lệnh: targeted test `test_committed_event_id_and_sequence_match_sse_and_rollback_is_never_emitted` in `test_stabilization02_observability.py`; full isolated suite.
- Kỳ vọng: committed DB `event_id`/`stream_seq` match SSE event ID/payload; rollback absent from DB/page/SSE.
- Thực tế: assertions pass for committed and rolled-back events.
- Kết quả phản biện: none.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: test file and [commands](evidence/commands.md).
- Xử lý/đề xuất: browser live stream correlation not required for this API invariant.

### P07-02 — Ordering và reconnect cursor

- Nguồn/tiêu chí: Phase 07 P07-02; Product Spec §9.
- Bắt buộc: có.
- Điều kiện/môi trường: event store browser reconnect scenario from r006; Sprint02 API source has no reconnect change.
- Bước/lệnh: **bằng chứng r006 được giữ nguyên, không rerun** theo yêu cầu tránh test trùng khi source tương ứng không đổi.
- Kỳ vọng: reconnect giữ event ID/order.
- Thực tế: r006 đã chứng minh 40 IDs trước/sau khớp theo thứ tự; API persistence/cursor tests tiếp tục pass trong r007 suite.
- Kết quả phản biện: accepted; source scope unchanged.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [r006 browser interruption](../20261018T221600+0700-r006-test/evidence/browser-interruption.md).
- Xử lý/đề xuất: live run vẫn được tách riêng tại P07-07.

### P07-03 — Cursor boundary và retention gap

- Nguồn/tiêu chí: Phase 07 P07-03; Product Spec §9.
- Bắt buộc: có.
- Điều kiện/môi trường: synthetic cursor tests; deterministic browser 409 route injection.
- Bước/lệnh: `test_stabilization02_observability.py`; authenticated state capture.
- Kỳ vọng: tamper/expiry/scope reject; gap có recovery snapshot/cursor.
- Thực tế: invalid cursor returns 400; retention gap/no cursor returns 409; UI shows gap label and recovers after temporary route error is removed. No snapshot endpoint/contract exists for actual retention recovery.
- Kết quả phản biện: none; API behavior alone does not satisfy product-spec snapshot recovery.
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Evidence: [gap screenshot](../../../../reviews/stabilization-02/evidence/authenticated-fresh/screenshots/states/cursor-gap/1440x900.png), test file.
- Xử lý/đề xuất: Owner/product decision on snapshot contract required before implementation.

### P07-04 — Offline, stale, heartbeat và trạng thái run

- Nguồn/tiêu chí: Phase 07 P07-04; Product Spec §3/9.
- Bắt buộc: có.
- Điều kiện/môi trường: Chromium offline network mode + EventSource abort; stalled feed with 31s browser clock advance.
- Bước/lệnh: authenticated review state checks.
- Kỳ vọng: phân biệt offline/stale và recovery; distinguish active idle/waiting_model.
- Thực tế: offline label/recovery, stale label/recovery verified; no active run, so idle/waiting_model distinction and real-device network loss not observed.
- Kết quả phản biện: none.
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Evidence: state screenshots and manifest under `../../../../reviews/stabilization-02/evidence/authenticated-fresh/`.
- Xử lý/đề xuất: live-state case remains blocked pending authorized run.

### P07-05 — Crash/unknown outcome

- Nguồn/tiêu chí: Phase 07 P07-05; Product Spec §8/9.
- Bắt buộc: có.
- Điều kiện/môi trường: fake transport, disposable PostgreSQL.
- Bước/lệnh: full isolated suite includes worker crash/restart/unknown outcome tests; not a live gateway call.
- Kỳ vọng: no replay of uncertain side effect; consumed guard remains.
- Thực tế: related tests pass in isolated suite; zero inference.
- Kết quả phản biện: accepted for fake transport contract only.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [commands](evidence/commands.md), test names in r006 and test suite.
- Xử lý/đề xuất: gateway live proof is outside authorized scope.

### P07-06 — Gateway session/context recovery

- Nguồn/tiêu chí: Phase 07 P07-06; Product Spec §8/9.
- Bắt buộc: có.
- Điều kiện/môi trường: isolated tests; no gateway access.
- Bước/lệnh: run regression suite; inspect browser evidence.
- Kỳ vọng: expired/invalid gateway session recovers without replay/duplicate side effects.
- Thực tế: bounded application context and unknown outcome regression are covered; no focused expired/revoked fake gateway-session test in this batch.
- Kết quả phản biện: none.
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Evidence: [commands](evidence/commands.md), [Sprint02 report](../../../../reviews/stabilization-02/report.md).
- Xử lý/đề xuất: add focused fake gateway session expiration/invalidation case in Phase 07.

### P07-07 — Authorized run tới UI

- Nguồn/tiêu chí: Phase 07 P07-07; V1 grant policy.
- Bắt buộc: có.
- Điều kiện/môi trường: no authorized grant available; inference explicitly out of scope.
- Bước/lệnh: not run.
- Kỳ vọng: authorized bounded run and event/UI correlation.
- Thực tế: no live run or model request; no grant created.
- Kết quả phản biện: none.
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Evidence: [IG08 proposal](../../../../reviews/stabilization-02/ig08-live-test-proposal.md).
- Xử lý/đề xuất: await explicit Owner decision and scoped grant.

## Integration / release gates

| Gate | Verdict | Test IDs | Evidence |
| --- | --- | --- | --- |
| Phase 07 / IG | No separate gate | P07-01–07 | Technical closure incomplete; no acceptance. |

## Cleanup, limits, handoff

- Cleanup: disposable DB/role cleaned by runner; browser Owner session logged out; no grant/run created; no persistent runtime mutation from Replay snapshots.
- Not verified: retention snapshot recovery, expired gateway session, authorized live run and active-state correlation.
- Required changes: snapshot recovery contract and focused session-expiry case; both require Phase 07 follow-up.
- Next: see [Sprint02 next actions](../../../../reviews/stabilization-02/next-actions.md). AI does not move to another phase.
