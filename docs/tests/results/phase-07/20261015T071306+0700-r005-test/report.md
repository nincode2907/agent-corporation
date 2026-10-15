# Kiểm định Phase 07 — Retest r005

## Thông tin batch

- Phase: 07; vòng r005; test batch `20261015T071306+0700-r005-test`.
- Thời điểm bắt đầu: 15/10/2026 07:13:06 Asia/Saigon.
- Tester: `/root/phase06_independent_review`, độc lập với remake r004.
- Yêu cầu: retest P07-02/P07-03 sau [remake r004](../../../../remakes/phase-07/20261015T071242+0700-r004-remake/remake.md), C01–C08 và regression liên quan.
- Supersedes: [r004](../20261014T161904+0700-r004-test/report.md).
- Remake nguồn: [remake r004](../../../../remakes/phase-07/20261015T071242+0700-r004-remake/remake.md).
- Source: worktree dirty; không sửa product code. Hashes/config snapshot trong [source manifest](evidence/source-manifest.json).
- Grant/inference/gateway: không tạo hoặc dùng grant; không gọi inference/gateway; không đọc Owner secret/cookie.
- Kết luận kỹ thuật: **chưa đủ bằng chứng**. P07-02 route cursor fix được retest; P07-03 UI gap/reconnect chưa được kiểm tra qua browser network-drop; P07-01/P07-04–07 vẫn blocked.
- Trạng thái chính thức Phase 07: không thay đổi; Phase 07 vẫn bị chặn bởi dependency Phase 06/CG01/run thật và các case còn thiếu.

## Mapping

| Tiêu chí | Case | Kết quả r005 |
| --- | --- | --- |
| AC1 ordering/reconnect | P07-01, P07-02, P07-03 | P07-02 route ưu tiên advanced `Last-Event-ID`; no browser network-drop/event-list proof. P07-01/P07-03 blocked |
| AC2 heartbeat/offline/unknown | P07-04, P07-05 | blocked |
| AC3 crash/recovery/gap | P07-05, P07-06, P07-07 | blocked; browser gap evidence thiếu |
| C01–C08 | C01–C08 | 5 pass, 3 blocked |

## Tổng hợp

| Tag | Số case |
| --- | ---: |
| clean | 6 |
| need-change | 9 |
| suggestion | 0 |

| Result | Số case |
| --- | ---: |
| pass | 6 |
| blocked | 9 |
| fail | 0 |
| not-run | 0 |

Tổng 15 cases: 6 pass, 9 blocked, 0 fail. Không có bug mới được xác nhận; các blocked là tiêu chí bắt buộc chưa có loại evidence phù hợp.

## Kết quả từng case

### C01 — Phạm vi và diff

- Nguồn: [RULES §5](../../../RULES.md), task bàn giao r005.
- Kỳ vọng: retest r004 remake và ghi evidence; không thay product source hoặc phase ngoài scope.
- Thực tế: đọc report r004/remake r004, checklist, source diff/manifest; chỉ thêm report/evidence/sổ vòng Phase 07. Không có product-code edit.
- Kết quả phản biện: none.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [source manifest](evidence/source-manifest.json), [commands](evidence/commands.md).
- Xử lý/đề xuất: Không có.

### C02 — Dependency và nguồn quyết định

- Nguồn: [phase checklist](../../../phases/phase-07.md), [master plan](../../../../master-plan.md), Phase 06 dependency.
- Kỳ vọng: phase dependency và status phải được giữ đúng; không suy nghiệm thu từ remake.
- Thực tế: Phase 07 phụ thuộc Phase 06; Phase 06/CG01 và run thật vẫn chưa được nghiệm thu. Remake r004 chỉ xử lý reconnect cursor/gap UI.
- Kết quả phản biện: none.
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Evidence: [r004 report](../20261014T161904+0700-r004-test/report.md), [remake r004](../../../../remakes/phase-07/20261015T071242+0700-r004-remake/remake.md), checklist.
- Xử lý/đề xuất: Giữ dependency blocker và không nâng trạng thái Phase 07.

### C03 — Criteria và demo

- Nguồn: Phase 07 AC1–AC3 và demo bắt buộc trong checklist.
- Kỳ vọng: đối chiếu sequence trước/sau reconnect, gap/error UI, heartbeat/crash recovery và run/UI evidence theo checklist.
- Thực tế: API route/unit and full isolated regression ran. Không thực hiện browser network drop, worker crash/failpoint hay run thật; nên chưa đủ evidence cho demo Phase 07.
- Kết quả phản biện: none.
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Evidence: [commands](evidence/commands.md), P07-01–P07-07.
- Xử lý/đề xuất: Bổ sung browser disconnect/reconnect + before/after event IDs khi có test tool phù hợp; run/crash cases theo quyền/dependency riêng.

### C04 — Không thực thi âm thầm

- Nguồn: [RULES §5](../../../RULES.md), ADR V1.
- Kỳ vọng: kiểm tra route/idle/reconnect không tự phát inference/tool.
- Thực tế: regression dùng unit/TestClient và PostgreSQL disposable; web lint/build; không gọi gateway, inference hay tool. Reconnect probe chỉ cung cấp cursor fixture.
- Kết quả phản biện: none.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [commands](evidence/commands.md), source `observability/router.py` và `RuntimePanel.tsx`.
- Xử lý/đề xuất: Không có.

### C05 — Scope và dữ liệu nhạy cảm

- Nguồn: Phase 07 event cursor/feed contract; [RULES §5](../../../RULES.md).
- Kỳ vọng: cursor gắn scope/session, invalid/tamper/expired cursor từ chối; public events không lộ private payload.
- Thực tế: focused tests pass cursor tamper, khác company/session, expiry và event payload redaction. Disposable full suite không tạo run/grant thật.
- Kết quả phản biện: none.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: `test_phase07_feed.py::test_cursor_rejects_tamper_expiry_different_scope_and_session`, `test_event_envelope_omits_raw_context_and_confidential_payloads`.
- Xử lý/đề xuất: Không tuyên bố cross-scope DB/RLS UI e2e từ các unit checks này.

### C06 — Tài liệu và bản nhìn

- Nguồn: [RULES §5](../../../RULES.md).
- Kỳ vọng: report/remake/README links hợp lệ; trạng thái không bị nâng; roadmap HTML được cập nhật sau report bởi parent.
- Thực tế: r005 report và README record tạo sau; Phase 07 master-plan Markdown/HTML không sửa trong batch theo yêu cầu, parent sẽ thêm summary và render.
- Kết quả phản biện: none.
- Tag: need-change
- Kết quả: blocked
- Mức độ: minor
- Evidence: [README](../README.md), [commands](evidence/commands.md).
- Xử lý/đề xuất: Parent cập nhật Markdown trước, render HTML sau khi r005 report link được thêm.

### C07 — Regression liên quan

- Nguồn: Phase 07 SSE, event feed, Owner auth, runtime/work-order dependency.
- Kỳ vọng: API subset, full isolated API suite, web lint/build.
- Thực tế: focused API: 54 passed, 9 skipped; full isolated suite: 143 passed, 11 skipped; web lint/build đều exit 0. Runner upgrade migration 0009 trên DB tạm rồi xóa đúng DB/role.
- Kết quả phản biện: none.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [commands](evidence/commands.md).
- Xử lý/đề xuất: Các test pass không thay evidence browser/runtime bắt buộc.

### C08 — Tái kiểm định được

- Nguồn: [RULES §5](../../../RULES.md).
- Kỳ vọng: lệnh/exit, hashes, environment, cleanup và giới hạn có thể kiểm tra lại.
- Thực tế: commands, versioned source hashes, pytest counts và cleanup runner được lưu; report phân biệt unit, disposable DB, source review và UI checks chưa chạy.
- Kết quả phản biện: none.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [commands](evidence/commands.md), [source manifest](evidence/source-manifest.json).
- Xử lý/đề xuất: Không có.

### P07-01 — Lưu trước phát

- Nguồn: checklist P07-01 / Spec §9.
- Kỳ vọng: chỉ event đã commit mới phát; inject transaction fail và chứng minh state/event/outbox durable.
- Thực tế: không chạy transaction failpoint hoặc DB event/SSE consistency test trong r005; full suite không thay cho case failpoint.
- Kết quả phản biện: none.
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Evidence: [commands](evidence/commands.md).
- Xử lý/đề xuất: Chạy failpoint/integration test trên fixture DB disposable.

### P07-02 — Ordering và reconnect cursor

- Nguồn: checklist P07-02 / Spec §9; issue r004 `Last-Event-ID` advanced cursor.
- Kỳ vọng: EventSource reconnect giữ URL query cursor cũ nhưng server phải tiếp tục từ `Last-Event-ID` mới, trả 200 và không replay event đã nhận.
- Thực tế: test mới gọi route với query `signed-cursor-from-original-url` và header `signed-cursor-from-last-event-id`; monkeypatch xác nhận `page()` nhận header cursor và route trả 200. Helper chọn `last_event_id or query_cursor`; client lưu cursor khi nhận event/heartbeat và bỏ event có sequence không vượt sequence hiện tại. R004 lỗi 400 do mismatch không còn tái hiện trong route regression.
- Kết quả phản biện: none.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: `test_phase07_feed.py::test_stream_uses_advanced_last_event_id_on_eventsource_reconnect`, `test_sse_frame_has_opaque_cursor_and_single_json_data`, [commands](evidence/commands.md).
- Xử lý/đề xuất: Pass cho route/cursor precedence regression. Trình duyệt chưa bị ngắt mạng nên chưa có before/after delivered event list thực tế.

### P07-03 — Gap và cursor boundary

- Nguồn: checklist P07-03 / Spec §9; issue r004 UI chỉ báo reconnecting khi stream lỗi.
- Kỳ vọng: invalid/expired/scope/gap cursor phân biệt với lỗi mạng; gap được thông báo kèm hành động reload, không mô tả stream như live.
- Thực tế: tests xác minh tamper, expiry, scope/session mismatch; backend ánh xạ EventGap thành HTTP 409 và stream event `gap` cho lỗi cursor/gap; UI `onerror` thăm dò read-only event page, phân loại 400/409/410/422 thành trạng thái `gap` và hiển thị hướng dẫn tải lại, còn network/5xx giữ trạng thái reconnect. Lint/build đạt. Không mô phỏng network drop hoặc quan sát thông báo trên browser.
- Kết quả phản biện: none.
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Evidence: `test_phase07_feed.py::test_cursor_rejects_tamper_expiry_different_scope_and_session`, source `observability/router.py` và `RuntimePanel.tsx`, [commands](evidence/commands.md).
- Xử lý/đề xuất: Logic source/route không cho thấy lỗi r004; cần browser/network-drop QA để chứng minh UI thông báo và reload flow.

### P07-04 — Heartbeat/offline

- Nguồn: checklist P07-04 / Spec §3/9.
- Kỳ vọng: sau mất heartbeat UI stale/offline; không báo agent active dựa vào heartbeat stream.
- Thực tế: browser disconnect và worker heartbeat timeout không được thực hiện trong r005.
- Kết quả phản biện: none.
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Evidence: [commands](evidence/commands.md).
- Xử lý/đề xuất: Cần browser/runtime QA với worker fixture; không dùng inference.

### P07-05 — Crash và unknown outcome

- Nguồn: checklist P07-05 / Spec §8/9.
- Kỳ vọng: worker restart/reconciliation không replay side effect chưa rõ.
- Thực tế: không kill worker hoặc chạy checkpoint fixture Phase 07 trong r005; disposable runner không được dùng làm bằng chứng cho case crash này.
- Kết quả phản biện: none.
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Evidence: [commands](evidence/commands.md).
- Xử lý/đề xuất: Worker lifecycle/fault injection riêng trên DB disposable, fake transport.

### P07-06 — Session/context recovery

- Nguồn: checklist P07-06 / Spec §6/8.
- Kỳ vọng: gateway session invalidation được khôi phục từ app history/checkpoint, không resume session lỗi ngầm.
- Thực tế: không chạy fake gateway invalidation/recovery trace trong r005.
- Kết quả phản biện: none.
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Evidence: [commands](evidence/commands.md).
- Xử lý/đề xuất: Adapter recovery tests trong scope Phase 07; live provider run vẫn theo grant/dependency riêng.

### P07-07 — Run thật đến UI

- Nguồn: checklist P07-07 / Spec §6/9.
- Kỳ vọng: authorized run/event IDs khớp UI qua disconnect/reconnect; waiting model không bịa token/progress.
- Thực tế: không có grant mới hoặc run trong r005; Phase 06/CG01 dependency chưa được gỡ.
- Kết quả phản biện: none.
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Evidence: [commands](evidence/commands.md), [dependency](../../../../master-plan.md).
- Xử lý/đề xuất: Chờ CG01/dependency và grant riêng đúng batch; không suy ra từ test fake.

## Bypass và boundary checks

| Boundary | Expected | Evidence/result |
| --- | --- | --- |
| EventSource URL có cursor cũ + advanced Last-Event-ID | Header cursor được dùng, không 400 mismatch | Route test trả 200 và page nhận advanced cursor; pass |
| Tampered/expired/different session/scope cursor | Từ chối cursor | focused cursor test; pass |
| EventGap/sequence inconsistency | Gap + yêu cầu reload, không báo live | Backend/UI source review; chưa browser-run, P07-03 blocked |
| Network/5xx failure | Giữ reconnecting/offline, không nhầm thành cursor gap | UI source phân nhánh; không network-drop E2E |
| Open page/health/reconnect | Không dispatch inference/tool | Read-only routes/tests; không gateway access |

## Findings, limits, handoff

- Không có lỗi implementation mới được xác nhận trong P07-02/P07-03 source/route checks.
- P07-02 regression fix được xác minh ở route level: advanced `Last-Event-ID` thắng query cursor cũ.
- P07-03 giữ blocked vì checklist cần UI evidence; browser network-drop không được mô phỏng trong batch này. P07-01/P07-04/P07-05/P07-06/P07-07 cũng blocked theo evidence còn thiếu/dependency.
- Không thay đổi Phase 07 status hoặc Phase 06 CG01/dependency. Không có inference/grant/gateway access/runtime DB changes.
- Parent sẽ cập nhật master-plan Markdown rồi render sau khi nhận report r005.
