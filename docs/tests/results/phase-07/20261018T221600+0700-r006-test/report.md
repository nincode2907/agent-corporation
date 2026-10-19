# Phase 07 — test batch r006

- **Batch:** `20261018T221600+0700-r006-test`
- **Thời gian:** 18/10/2026, Asia/Ho_Chi_Minh
- **Yêu cầu:** Stabilization Sprint 01; retest reconnect/event continuity, Playground fake transport, các tiêu chí Phase 07 còn liên quan.
- **Vòng trước:** [r005](../20261015T071306+0700-r005-test/report.md)
- **Remake nguồn:** Không có. Sprint này nhận các fix UI/Lens đã triển khai rồi kiểm tra lại; không có remake phase độc lập.
- **Revision:** `39321b177a60a20ecf327cfccaa9e6b865fe4db0` trên `main`, worktree dirty; source manifest lưu trong `evidence/source-manifest.json`.
- **Kết luận kỹ thuật:** **chưa đủ bằng chứng**. P07-02 và kiểm tra fake worker crash/unknown outcome đạt ở lớp browser/API. P07-01, P07-03, P07-04, P07-06 và P07-07 còn thiếu bằng chứng end-to-end cụ thể.
- **Gate:** Không có IG riêng. CG01 vẫn `verified=false`; không có inference hoặc grant trong batch này.
- **Quyết định Chủ tịch:** Chưa có.

## Tóm tắt kết quả

| Nhóm | clean/pass | need-change/blocked | fail | Tổng |
| --- | ---: | ---: | ---: | ---: |
| C01–C08 | 7 | 1 | 0 | 8 |
| P07-01–P07-07 | 2 | 5 | 0 | 7 |
| **Tổng** | **9** | **6** | **0** | **15** |

`need-change + blocked` dưới đây là thiếu loại bằng chứng bắt buộc, không khẳng định đã tìm thấy lỗi ở các chức năng đó.

## Ánh xạ acceptance criteria

| Criteria | Test | Kết quả |
| --- | --- | --- |
| AC1: event đã lưu lấy lại đúng thứ tự, không mất/nhân đôi khi reconnect | P07-01, P07-02, P07-03 | P07-02 browser route recovery đạt với cùng 40 event ID theo đúng thứ tự; P07-01 SSE-after-commit và P07-03 gap UI còn thiếu. |
| AC2: heartbeat/offline/unknown outcome không báo sai trạng thái | P07-04, P07-05 | Fake crash/unknown guard đạt ở API; browser thấy `Đang kết nối lại` khi stream bị chặn. Trạng thái thiết bị offline/stale/idle so với waiting chưa được chứng minh đủ. |
| AC3: crash/context/session recovery không replay tác dụng phụ; gap hiển thị rõ | P07-05, P07-06, P07-07 | Fake worker restart/unknown không replay đạt; context recovery với phiên gateway invalid và run thật tới UI còn blocked. |

## Kiểm tra chung

### C01 — Phạm vi và diff

- **Kỳ vọng:** Chỉ làm Sprint 01; không mở Phase 11/Employee Chat production; giữ thay đổi người dùng ngoài scope.
- **Thực tế:** Sửa keyboard skip link và responsive overflow trong UI hiện hữu; chỉnh cấu hình capture `.ui-review.json`; thêm report/evidence. Không sửa API/gateway/migration, không commit/push. `docs/current-project-report.md` và các artifacts trước sprint được giữ.
- Tag: `clean`
- Kết quả: `pass`
- Mức độ: `info`
- **Evidence:** `evidence/source-manifest.json`, [report sprint](../../../../reviews/stabilization-01/report.md).

### C02 — Dependency và nguồn quyết định

- **Kỳ vọng:** Đối chiếu dependency Phase 06, Phase 07 r005, CG01 và checklist hiện hành.
- **Thực tế:** Phase 06 vẫn bị chặn bởi CG01/live acceptance; Phase 07 r005 ghi P07-02 route fix đã pass nhưng browser network-drop và run/live criteria còn mở. Sprint này kiểm browser recovery bằng route chặn EventSource; không làm thay CG01 hoặc grant/run thật.
- Tag: `clean`
- Kết quả: `pass`
- Mức độ: `info`
- **Evidence:** [master plan](../../../../master-plan.md), [checklist Phase 07](../../../phases/phase-07.md), [r005](../20261015T071306+0700-r005-test/report.md).

### C03 — Criteria và demo

- **Kỳ vọng:** Ánh xạ mọi AC/P07 case; demo phù hợp từng test.
- **Thực tế:** Đã ánh xạ AC1–3 và P07-01…07. Reconnect browser dùng event store đã lưu; không tạo task/run/model call mới. Các case yêu cầu live/expired gateway session chưa chạy.
- Tag: `need-change`
- Kết quả: `blocked`
- Mức độ: `major`
- **Evidence:** `evidence/browser-interruption.md`, `evidence/authenticated/manifest.json`.
- **Còn thiếu:** P07-01, P07-03, P07-04, P07-06, P07-07 như bảng dưới.

### C04 — Không thực thi âm thầm

- **Kỳ vọng:** Mở trang/health/replay không dispatch model/tool.
- **Thực tế:** Browser chỉ ghi POST `/api/v1/owner/login` và `/api/v1/owner/logout`; các route còn lại chỉ GET, gồm feed/status. Không có POST profile/grant/send/run, không thấy request tới Codex gateway. Full API suite dùng fake transport; không có inference.
- Tag: `clean`
- Kết quả: `pass`
- Mức độ: `info`
- **Evidence:** `evidence/authenticated/manifest.json`, `evidence/commands.md`.

### C05 — Scope và dữ liệu nhạy cảm

- **Kỳ vọng:** Không để lộ secret/raw prompt hoặc mở cross-scope.
- **Thực tế:** Secret Owner đọc trực tiếp từ file local, không ghi vào manifest, console output hay screenshot; browser context đăng xuất cuối lượt. Feed/cursor GET dùng session scope. Bộ API test đầy đủ đạt; cross-scope browser negative không chạy trong batch này.
- Tag: `clean`
- Kết quả: `pass` cho luồng đã thực hiện
- Mức độ: `info`
- **Evidence:** `evidence/authenticated/manifest.json`, test `test_phase07_feed.py` và `test_phase07_feed_persistence.py` trong full suite.

### C06 — Tài liệu và bản nhìn

- **Kỳ vọng:** Bằng chứng đúng với UI hiện tại, không nâng trạng thái phase.
- **Thực tế:** UI Lens hoàn tất 18/18 captures; browser authenticated chụp 9 màn hình ở hai kích thước. Phase status không thay đổi; bản HTML chỉ render sau khi ghi lịch sử có links và kết luận giữ nguyên.
- Tag: `clean`
- Kết quả: `pass`
- Mức độ: `info`
- **Evidence:** [UI Lens manifest](../../../../../artifacts/ui-review/2026-10-18T15-28-04-437Z_c80b5d46-9af9-4eb2-8155-e3d97c33cd0d/manifest.json), `evidence/authenticated/manifest.json`.

### C07 — Regression liên quan

- **Kỳ vọng:** Kiểm feed/cursor, durable state, crash/restart và UI change.
- **Thực tế:** `rtk proxy uv run --project apps/api python scripts/test_playground_isolated.py` chạy migration trên PostgreSQL disposable và toàn API suite: **143 passed, 11 skipped, 1 warning**; DB/role tạm được runner xóa. `rtk proxy npm run --prefix apps/web build` exit 0. Không lặp API suite sau CSS/TSX-only fixes vì API source không đổi.
- Tag: `clean`
- Kết quả: `pass`
- Mức độ: `info`
- **Evidence:** `evidence/commands.md`.

### C08 — Tái kiểm định được

- **Kỳ vọng:** Có command, version, ảnh, manifest, actual/expected và cleanup.
- **Thực tế:** Batch có manifest hashes, Playwright 156.0.8078.4, UI Lens 0.1.0, URL/viewport, event-ID comparison và log method/path đã loại nội dung nhạy cảm. Runner xác nhận xóa disposable DB/role.
- Tag: `clean`
- Kết quả: `pass`
- Mức độ: `info`
- **Evidence:** `evidence/source-manifest.json`, `evidence/commands.md`, `evidence/authenticated/manifest.json`.

## Ca Phase 07

### P07-01 — Lưu trước phát

- **Nguồn:** Checklist P07-01 / Product Spec §9.
- **Kỳ vọng:** Chỉ phát SSE sau commit; transaction fail không phát event.
- **Thực tế:** API suite có test committed pages, no uncommitted events và rollback state/event/outbox; chưa có browser/network observation gắn cùng event ID để chứng minh thứ tự commit→SSE trong runtime này.
- Tag: `need-change`
- Kết quả: `blocked`
- Mức độ: `major`
- **Evidence:** `evidence/commands.md`; tests `test_committed_pages_reconnect_no_mutations_or_uncommitted_events`, `test_event_failure_rolls_back_work_order_revision_state_and_counter`.
- **Còn thiếu:** Correlate DB commit timestamp/ID với event SSE nhận trong browser.

### P07-02 — Ordering và reconnect cursor

- **Nguồn:** Checklist P07-02 / Product Spec §9.
- **Kỳ vọng:** Ngắt stream rồi reconnect bằng cursor; không mất/nhân đôi event.
- **Thực tế:** Chặn có chủ đích `/api/v1/events/stream`, browser thấy `Đang kết nối lại`; sau bỏ chặn EventSource nhận HTTP 200. Danh sách **40 event ID** trước/sau giống hệt, cùng thứ tự. Request reconnect có query cursor; API cursor/persistence tests trong suite cũng đạt.
- Tag: `clean`
- Kết quả: `pass`
- Mức độ: `info`
- **Evidence:** `evidence/browser-interruption.md`, `evidence/authenticated/manifest.json`, `evidence/commands.md`.
- **Giới hạn:** Đây là browser test trên event đã lưu, không phải run inference mới.

### P07-03 — Gap và cursor boundary

- **Nguồn:** Checklist P07-03 / Product Spec §9.
- **Kỳ vọng:** Cursor sai/hết hạn/gap/khác scope có handling rõ trên UI.
- **Thực tế:** API tests cursor tamper/expiry/scope và gap sequence đạt; browser route test lần này không inject cursor hết hạn/gap để xác minh nhãn UI.
- Tag: `need-change`
- Kết quả: `blocked`
- Mức độ: `major`
- **Evidence:** `evidence/commands.md`; `test_cursor_rejects_tamper_expiry_different_scope_and_session`, `test_missing_sequence_reports_gap_and_wrong_scope_is_empty`.
- **Còn thiếu:** Browser test cho từng lỗi cursor/gap và hành động reload.

### P07-04 — Heartbeat/offline

- **Nguồn:** Checklist P07-04 / Product Spec §3/9.
- **Kỳ vọng:** Phân biệt live, reconnecting, stale và offline theo tín hiệu thật; không nhầm worker heartbeat.
- **Thực tế:** Thử nghiệm browser thấy reconnecting khi stream bị chặn; trạng thái stale do heartbeat hết hạn và `navigator.onLine=false` chưa được kiểm tra bằng một thiết bị offline thật. UI copy phân biệt heartbeat event store với worker heartbeat.
- Tag: `need-change`
- Kết quả: `blocked`
- Mức độ: `major`
- **Evidence:** `evidence/browser-interruption.md`, [ảnh Office](../../../../reviews/stabilization-01/evidence/authenticated/screenshots/office/1440x900.png).
- **Còn thiếu:** Offline thực, stale timeout và kiểm chứng trạng thái idle/waiting trên cùng run.

### P07-05 — Crash và unknown outcome

- **Nguồn:** Checklist P07-05 / Product Spec §8/9.
- **Kỳ vọng:** Worker restart không gọi lại side effect chưa biết kết quả; unknown giữ request đã tiêu thụ.
- **Thực tế:** Fake transport + disposable PostgreSQL tests xác nhận worker crash/restart bị fence, late completion không ghi đè unknown, request không được replay và guard giữ concurrency/usage. Không gọi model thật.
- Tag: `clean`
- Kết quả: `pass`
- Mức độ: `info`
- **Evidence:** `evidence/commands.md`; tests `test_worker_crash_restart_fences_late_completion_keeps_unknown_guard_and_consumed_request`, `test_real_worker_process_crash_and_new_process_recovery_never_replays`.
- **Giới hạn:** Bằng chứng fake transport trong DB tạm, không là CG01/live proof.

### P07-06 — Session/context recovery

- **Nguồn:** Checklist P07-06 / Product Spec §6/8.
- **Kỳ vọng:** Session gateway expired/invalidated không resume ngầm; context app được dựng từ history/checkpoint.
- **Thực tế:** Kiểm history bounded và test fake worker recovery; chưa inject gateway session expired/invalidated trên luồng browser/runtime hiện tại.
- Tag: `need-change`
- Kết quả: `blocked`
- Mức độ: `major`
- **Evidence:** `evidence/commands.md`; `test_history_keeps_only_bounded_explicit_completed_context`.
- **Còn thiếu:** Fake gateway session-invalidated test gắn recovery context/call ledger.

### P07-07 — Run thật đến UI

- **Nguồn:** Checklist P07-07 / Product Spec §6/9.
- **Kỳ vọng:** Run text-only được cấp riêng, UI disconnect/reconnect, cùng run/event ID.
- **Thực tế:** Không có grant hợp lệ được tạo trong sprint; chỉ dùng event của run lịch sử và fake transport. Không thể dùng ảnh fixture/run cũ thay live evidence.
- Tag: `need-change`
- Kết quả: `blocked`
- Mức độ: `major`
- **Evidence:** `evidence/authenticated/manifest.json`; `evidence/commands.md`.
- **Điều kiện tiếp tục:** Owner cấp grant cho đúng phase/test batch nếu muốn thực hiện run thật; CG01 chưa verified.

## Bypass matrix

| Đường bypass | Kỳ vọng | Quan sát | Trạng thái |
| --- | --- | --- | --- |
| Mở trang Inspector/Replay khi chưa auth | Không đọc dữ liệu Owner | UI Lens thấy 401 session probe; trang auth gate | Quan sát được; 401 là default-deny mong đợi |
| Mở trang/replay khi đã auth | GET dữ liệu, không dispatch | Request log chỉ GET ngoài login/logout | Pass cho route đã duyệt |
| Reconnect stream với event đã lưu | Không nhân đôi | 40 IDs giữ nguyên thứ tự | Pass |
| Cursor invalid/gap được render UI | Thông báo gap/reload | Chưa inject trong browser | Blocked |
| Worker restart với unknown model result | Không retry call | Fake + PostgreSQL tests pass | Pass trong isolated test scope |

## Kết luận

P07-02 browser reconnect đã có bằng chứng mới và không làm thay đổi dữ liệu event. P07-05 có regression fake/persistence pass. Các phần còn lại chưa đạt đủ loại evidence; Phase 07 không được coi hoàn tất và vẫn chờ dependency/acceptance hiện hành.
