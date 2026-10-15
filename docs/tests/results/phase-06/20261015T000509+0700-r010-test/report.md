# Kiểm định Phase 06 — Playground r010

## Thông tin batch

- Phase: 06; vòng r010; test batch `20261015T000509+0700-r010-test`.
- Thời điểm bắt đầu: 15/10/2026, 00:05:09 Asia/Saigon.
- Supersedes: [r009](../20261014T233046+0700-r009-test/report.md).
- Remake nguồn: [remake r007](../../../remakes/phase-06/20261014T231406+0700-r007-remake/remake.md); r010 retest thêm Playground theo ADR-0003.
- Phạm vi: kiểm định độc lập Development Playground DPG01–DPG10; regression API trên PostgreSQL disposable; web lint/build; đọc source và UI state.
- Quyền: không đọc Owner secret/cookie; không tạo grant trên runtime DB; không migration runtime DB; transport test là fake; không gọi inference.
- Kết luận Playground: **chưa đủ bằng chứng cho DPG10 UI end-to-end**; 9 case DPG đã được kiểm tra bằng source/API/DB tests. Không có lỗi implementation được xác nhận trong scope đã chạy.
- Kết luận Phase 06 production: **Bị chặn**. Demo Playground không chứng minh CG01/isolation production; không thay đổi trạng thái chính thức hoặc nghiệm thu phase.

## Bản đồ thay đổi và phiên bản nguồn

Đọc ADR-0003, checklist Phase 06, service/router/worker, lifespan/settings, migration 0009, Playground UI, isolated runner và test suite. Bản đồ hash có trong [source manifest](evidence/source-manifest.json). Các rủi ro được tập trung vào Owner/CSRF và consent, demo boundary/RLS, cắt riêng Work Orders, reservation/shared dispatch guard, hạn mức và idempotency, tools-off, Stop/unknown/crash recovery, và UI recovery.

## Kết quả kiểm thử

### C01 — Phạm vi và diff

- Nguồn/tiêu chí: AGENTS.md, docs/tests/RULES.md §5, ADR-0003.
- Điều kiện: dirty workspace hiện tại; không sửa implementation.
- Thực tế: source mới/đang thay đổi liên quan Playground, migration 0009, test runner, tests, UI và docs Phase 06. Không chạy hoặc sửa phase khác. Hash và file nguồn trong manifest.
- Kết quả: pass
- Tag: clean
- Mức độ: info
- Evidence: [manifest](evidence/source-manifest.json), [commands](evidence/commands.md).
- Xử lý/đề xuất: Không có.

### C02 — Dependency và nguồn quyết định

- Nguồn/tiêu chí: docs/master-plan.md, phase-06.md, ADR-0003, r009.
- Thực tế: roadmap vẫn ghi Phase 06 bị chặn; ADR-0003 xác định Playground demo độc lập Work Orders nhưng `verified=false`; r009 là một lượt runtime test khác scope, không phải DPG proof.
- Kết quả: pass
- Tag: clean
- Mức độ: info
- Evidence: [commands](evidence/commands.md), [r009](../20261014T233046+0700-r009-test/report.md).
- Xử lý/đề xuất: Giữ nguyên production gate CG01.

### C03 — Đủ criteria và demo

- Thực tế: mapping đầy đủ DPG01–DPG10 dưới đây. API/DB suite có fixture fake transport; live browser chỉ được quan sát ở trạng thái form consent chưa chọn, nút tạo grant disabled, profile đã tải. Không tạo grant hay gửi inference trong r010.
- Kết quả: blocked
- Tag: need-change
- Mức độ: major
- Evidence: DPG01–DPG10 và [runtime checks](evidence/runtime-checks.md).
- Xử lý/đề xuất: Cần kiểm tra UI tạo grant, chat, Stop/expiry và unknown recovery trong một batch được Chủ tịch cấp quyền riêng; UI chưa đủ bằng chứng để kết luận end-to-end.

### C04 — Không thực thi âm thầm

- Thực tế: mở Playground không tự tạo grant; runtime UI quan sát cho thấy consent chưa được chọn và nút tạo grant đang disabled. Các kiểm tra API dùng test client, DB cách ly và fake transport. Không có model/inference request trong batch này.
- Kết quả: pass
- Tag: clean
- Mức độ: info
- Evidence: [runtime checks](evidence/runtime-checks.md), [commands](evidence/commands.md), test DPG01/DPG08.
- Xử lý/đề xuất: Không có.

### C05 — Scope và dữ liệu nhạy cảm

- Thực tế: session/turn lưu ở bảng riêng, RLS bật và FORCE; API kiểm demo scope; session tạo mới kiểm tra Owner session khớp owner/scope và grant expiry không vượt Owner session expiry. Tests xác minh scope khác đọc 0 rows. Playground không ghi Work Order/model_calls; input/output không được đưa vào event payload theo source. Không đọc secret/cookie và không lưu transcript thật.
- Kết quả: pass
- Tag: clean
- Mức độ: info
- Evidence: DPG01/DPG02/DPG09, [manifest](evidence/source-manifest.json).
- Xử lý/đề xuất: Cần giữ `verified=false`; đây không phải chứng minh isolation của gateway/provider.

### C06 — Tài liệu và bản nhìn

- Thực tế: chạy `render_phase00.py` với UTF-8 exit 0, đồng bộ product spec và roadmap HTML; kiểm tra thủ công xác nhận master-plan HTML chứa r010 và test batch ID. `validate_phase00.py` exit 1 vì tự gọi renderer con không truyền cờ UTF-8, gặp lỗi decode Windows cp1252 trước khi validator báo PASS contract.
- Kết quả: pass
- Tag: suggestion
- Mức độ: minor
- Evidence: [commands](evidence/commands.md), source manifest chứa hash HTML đã render.
- Xử lý/đề xuất: Phase 06 artifacts đã render; nếu validator Phase 00 được chạy sau này, cần truyền UTF-8 cho subprocess renderer hoặc sửa script ngoài scope r010.

### C07 — Regression liên quan

- Thực tế: isolated runner nâng migration 0009 trên DB tạm rồi chạy toàn bộ API tests: 142 passed, 11 skipped, 1 cảnh báo deprecation. Web lint và production build đều exit 0. Runner báo DB/role disposable đã được xóa; không thay đổi runtime data.
- Kết quả: pass
- Tag: clean
- Mức độ: info
- Evidence: [commands](evidence/commands.md).
- Xử lý/đề xuất: Không có lỗi test fail trong lượt này.

### C08 — Có thể tái kiểm định

- Thực tế: lệnh, exit code, kết quả, source hashes, cleanup và giới hạn được ghi trong evidence. Chạy script bằng Python mặc định ban đầu dừng trước DB setup do thiếu SQLAlchemy; chạy lại bằng `uv run --project apps/api` dùng dependency lock và hoàn tất. Không có resource nào được tạo bởi lần chạy lỗi.
- Kết quả: pass
- Tag: clean
- Mức độ: info
- Evidence: [commands](evidence/commands.md), [manifest](evidence/source-manifest.json).
- Xử lý/đề xuất: Tái chạy runner qua uv như ghi trong commands.

### DPG01 — Owner, CSRF, consent và demo-only

- Nguồn/tiêu chí: docs/tests/phases/phase-06.md DPG01; ADR-0003.
- Thực tế: anonymous list trả 401; grant POST thiếu CSRF trả 403; `accept_demo_policy=false`, scope ngoài demo và input có trường quyền không hợp lệ bị từ chối. Mở UI không tạo grant. Test client dùng dependency override fixture.
- Kết quả: pass
- Tag: clean
- Mức độ: info
- Evidence: `test_playground.py::test_anonymous_and_extra_tool_configuration_denied`, `test_csrf_required_for_playground_grant`; DPG01.
- Xử lý/đề xuất: Không có.

### DPG02 — Multi-turn, profile snapshot và Work Order separation

- Thực tế: disposable PostgreSQL test xác minh turn thứ hai mang history lượt đã hoàn tất, giữ profile/model snapshot cũ sau khi global profile đổi, event liên kết session/turn, không thêm Work Order hay `model_calls`.
- Kết quả: pass
- Tag: clean
- Mức độ: info
- Evidence: `test_playground_persistence.py::test_multi_turn_history_snapshots_usage_unknown_and_work_order_isolation`.
- Xử lý/đề xuất: Không có.

### DPG03 — App-owned worker lifecycle và recovery

- Thực tế: lifespan bật worker theo setting và dừng lúc app shutdown; Supervisor tiếp tục vòng sau exception; worker xử lý queue trong isolated process test; không cần CLI worker để reserve/dispatch fixture job. Không tạo grant tự động.
- Kết quả: pass
- Tag: clean
- Mức độ: info
- Evidence: `test_playground.py::test_managed_worker_starts_and_stops_with_api`, `test_supervisor_restarts_loop_after_fault_without_creating_grants`, `test_playground_persistence.py::test_real_worker_process_crash_and_new_process_recovery_never_replays`.
- Xử lý/đề xuất: Không có.

### DPG04 — Expiry, request limit, reserve và concurrency

- Thực tế: hết hạn trước send bị deny; hết hạn trước dispatch hủy queue, không transport call và không tiêu request. Grant expiry được chặn bởi expiry Owner session. Nhiều reserve đồng thời chỉ một request được reserve; limit sử dụng tại reserve, không refund sau unknown.
- Kết quả: pass
- Tag: clean
- Mức độ: info
- Evidence: `test_expired_grant_before_send_and_before_dispatch_never_calls`, `test_limit_exceeded_and_replay_same_key_does_not_spend_again`, `test_session_and_send_idempotency_concurrent_duplicate_and_concurrency`, `test_grant_effective_expiry_is_bounded_by_owner_session`.
- Xử lý/đề xuất: Không có.

### DPG05 — Duplicate send và payload mismatch

- Thực tế: nhiều submit đồng thời cùng idempotency key/nội dung cho một turn; nội dung khác cùng key bị deny; một pending/unknown chưa reconcile chặn turn khác.
- Kết quả: pass
- Tag: clean
- Mức độ: info
- Evidence: `test_session_and_send_idempotency_concurrent_duplicate_and_concurrency`, `test_worker_crash_restart_fences_late_completion_keeps_unknown_guard_and_consumed_request`.
- Xử lý/đề xuất: Không có.

### DPG06 — Stop, expiry, revoke và Owner logout

- Thực tế: queued Stop hủy không gọi transport và không tiêu request. Với request in-flight, Stop/expiry/revoke Owner session cancel transport, ghi unknown, giữ request đã dùng và không retry. Owner session hết hạn giới hạn grant hiệu lực.
- Kết quả: pass
- Tag: clean
- Mức độ: info
- Evidence: `test_stop_queued_and_revoke_are_durable_without_dispatch`, `test_in_flight_stop_expiry_logout_close_transport_unknown_and_no_retry`, `test_grant_effective_expiry_is_bounded_by_owner_session`.
- Xử lý/đề xuất: UI thao tác Stop chưa được kiểm thử live trong batch này.

### DPG07 — Crash/restart, unknown và fencing

- Thực tế: subprocess chết sau reserve; process mới thu hồi lease thành unknown, không gửi lại; request vẫn đã tiêu, late completion bị fence; shared dispatch guard giữ đến Owner resolve.
- Kết quả: pass
- Tag: clean
- Mức độ: info
- Evidence: `test_real_worker_process_crash_and_new_process_recovery_never_replays`, `test_worker_crash_restart_fences_late_completion_keeps_unknown_guard_and_consumed_request`.
- Xử lý/đề xuất: Chưa thử thao tác resolve trong browser UI.

### DPG08 — Tools và capability bị từ chối

- Thực tế: schema từ chối tools/network/fallback/concurrency/file/terminal/deploy/config fields; worker tự dựng payload tools rỗng, `tool_choice=none`, `parallel_tool_calls=false`, không chuyển fallback fields; response có provider tool call thành unknown, không execute.
- Kết quả: pass
- Tag: clean
- Mức độ: info
- Evidence: `test_anonymous_and_extra_tool_configuration_denied`, `test_worker_payload_never_adopts_tools_and_missing_usage_stays_unknown`, `test_unauthorized_provider_tool_output_is_unknown`.
- Xử lý/đề xuất: Đây là test/source evidence trong fake transport; không tuyên bố provider isolation đã xác minh.

### DPG09 — Usage, events và RLS

- Thực tế: RLS/FORCE và scope sai fail closed; event lưu session/turn/profile version và trạng thái. Test Work Order + Playground dùng chung dispatch capacity nhưng mỗi worker không dispatch hàng đợi của lane còn lại. Khi transport thiếu usage, DB giữ `usage=null`, provenance `unknown`, không đổi thành 0. Usage do fake adapter cung cấp được lưu khi có.
- Kết quả: pass
- Tag: clean
- Mức độ: info
- Evidence: `test_rls_fail_closed_scope_and_profile_policy_acceptance`, `test_multi_turn_history_snapshots_usage_unknown_and_work_order_isolation`, `test_work_order_runtime_and_playground_share_capacity_without_dispatching_each_others_jobs`.
- Xử lý/đề xuất: Không suy ra chi phí.

### DPG10 — UI và recovery end-to-end

- Thực tế: web lint/build thành công; parent quan sát route Playground sau khi Owner đã đăng nhập sẵn: profile/employee list tải, consent chưa chọn và Create Grant disabled. Không thao tác login; không tạo grant; không gửi chat; không kiểm thử UI Stop/expiry/remaining/recovery trên browser.
- Kết quả: blocked
- Tag: need-change
- Mức độ: major
- Evidence: [runtime checks](evidence/runtime-checks.md), [commands](evidence/commands.md).
- Xử lý/đề xuất: UI chưa được nghiệm thu end-to-end. Chỉ tiếp tục browser workflow khi có Owner chủ động cấp grant riêng cho batch/mục đích và hạn mức cụ thể.

## Thử bypass và kiểm tra biên

| Tấn công/biên | Expected | Actual | Kết quả |
| --- | --- | --- | --- |
| Anonymous GET session | 401 | 401 | pass |
| POST không CSRF | deny | 403 | pass |
| Tắt consent hoặc cấp ngoài demo scope | deny | 422 / `RuntimeDenied` | pass |
| Thêm tool/fallback/network/concurrency vào request | reject | schema 422 | pass |
| Duplicate submit cạnh tranh cùng key | một turn duy nhất | một turn duy nhất | pass |
| Expiry/Stop/logout trong lúc transport đang chờ | cancel, unknown, không retry/refund | fake transport bị cancel; unknown và request tiêu | pass |
| Crash rồi late response | unknown giữ guard, không overwrite/replay | fenced; process mới không gọi transport | pass |
| Grant/session scope DB khác | fail closed | RLS trả 0 rows | pass |

Không dùng production credentials, inference, grant thật hay prompt/runtime data để thực hiện các bypass.

## Findings và độ nghiêm trọng

- Không có lỗi implementation được xác nhận trong source/test scope đã chạy.
- **Major — DPG10 blocked, thiếu evidence UI end-to-end.** Không khẳng định UI flow đạt từ build hoặc test fixture; chưa tạo grant nên không thể quan sát chat, Stop, expiry hoặc unknown resolution trực tiếp.
- **Major — Production Phase 06 vẫn blocked ngoài Playground.** CG01 proof/isolation và các gate production không được kiểm thử hoặc miễn trừ bởi batch này. `RUNTIME_CG01_DEMO_TEST_OVERRIDE` và lượt r009 không chứng minh release strict.
- Sự cố an toàn trước batch: parent báo lần chạy full API suite trước khi fixture guard được thêm đã bị FK ngăn reset; transaction rollback, dữ liệu runtime và run `100bc3c8` còn nguyên theo kiểm tra read-only của parent. Fixture hiện chỉ cho phép reset nếu `PLAYGROUND_TEST_ISOLATED=1` và DB tên `ac_pgtest_*`; r010 chỉ chạy isolated runner.

## Giới hạn

- 11 API tests skipped theo marker/điều kiện môi trường; xem pytest output trong [commands](evidence/commands.md).
- Disposable DB kiểm tra migration và semantics PostgreSQL nhưng không chứng minh isolation của gateway/provider hoặc entitlement model.
- Không thực hiện live UI grant/chat/inference; không dùng DB runtime để kiểm tra write/migration.
- UI browser state được ghi nhận bởi parent, không kèm screenshot; không xem hoặc lưu cookie/session data.

## Kết luận

Playground source và DB/API paths đã đạt các kiểm tra DPG01–DPG09 trong môi trường fake/disposable; lint/build đều đạt. DPG10 còn blocked vì không thực hiện workflow UI có grant. Không có finding implementation cần remake được xác nhận trong lượt này. Production Phase 06 tiếp tục **Bị chặn**, không đổi trạng thái roadmap.
