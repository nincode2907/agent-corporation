# Stabilization Sprint 01 — Việc tiếp theo

Danh sách này sắp theo dependency và evidence gap. Đây là gợi ý thực hiện khi Chủ tịch giao phase/batch tương ứng; không tự chuyển phase, cấp quyền, grant hay inference.

## P0 — Giữ ranh giới hiện tại

- Không mở Phase 11/production Employee Chat trong stabilization.
- Không coi Phase 06 historical run `100bc3c8…` là live Phase 07/08 evidence.
- Không mở CG01 hoặc tạo grant. `CG01 verified=false`; Phase 06 grant một request cũ đã dùng hết.
- Giữ Phase 06–08 ở trạng thái nguồn hiện tại tới khi có batch evidence phù hợp và quyết định nghiệm thu của Chủ tịch.

## P1 — Phase 07 evidence gaps

1. **P07-01 save-before-publish:** gắn transaction commit/event ID với quan sát SSE cùng ID, kể cả rollback case.
2. **P07-03 cursor UI:** browser inject cursor tamper/expiry/scope/gap; xác minh trạng thái, hướng dẫn reload và không mất/nhân đôi event.
3. **P07-04 offline/stale:** kiểm tra true browser offline, heartbeat timeout, worker idle/waiting/stale; không suy ra offline từ việc abort stream.
4. **P07-06 context recovery:** fake gateway trả session invalid/expired; correlate app history/checkpoint, call ledger và đảm bảo không resume ngầm.
5. **P07-07 run tới UI:** chỉ sau khi Owner quyết định batch/phase/purpose/limit/expiry và cấp grant riêng, làm run text-only có thể đối chiếu run/event ID end-to-end. CG01 vẫn phải theo gate riêng.

## P2 — Phase 08 evidence gaps

1. **P08-01/02 Live Office:** cần một run được cho phép và event đã lưu; kiểm tra các entry point cùng run ID, trạng thái reconnect và reload.
2. **P08-03 Replay read-only:** thêm spy cho API/write/model/tool; lưu database snapshot trước/sau seek/reload và đối chiếu cursor/event nguồn.
3. **P08-04 ACL:** tạo actor/scope test thứ hai trong dữ liệu disposable; negative test HTTP/SSE/Inspector, không lộ payload.
4. **P08-06 state/error:** kiểm thử empty/loading/error/recovery state của Office/Inspector với nguồn dữ liệu xác định.
5. **IG08:** hoàn tất checklist và evidence riêng; historical Phase 06 screenshot không thay nghiệm thu.

## P3 — Theo dõi chất lượng UI

- Giữ bộ UI Lens 9 targets × 2 viewport; xem 401 session probe và `ERR_ABORTED` riêng trong diagnostics, tránh tự động quy thành page failure khi page error count bằng 0.
- Có thể bổ sung test component/browser để ngăn regression ở skip link, session nav width và Inspector controls.
- Chụp lại visual baseline nếu UI/API content thay đổi; không lưu secret, session token hoặc transcript không cần thiết vào artifacts.

## Phụ thuộc quyết định Owner

- Có cấp batch riêng cho run/inference Phase 07 hoặc IG08 không? Nếu có: phase, purpose, model/profile đã quyết, số lượt/concurrency/timeout, expiry và stop owner phải được ghi rõ.
- Có cho phép tạo dữ liệu/actor disposable thứ hai để test ACL và replay DB before/after không?
- Ai nghiệm thu các phase còn pending sau khi evidence gap được lấp? Agent chỉ báo cáo kết quả, không tự tick nghiệm thu.

## Đề xuất thứ tự

Tiếp tục từ phase đang được giao theo dependency chính thức: P07-01/03/04/06 bằng test không inference trước; sau đó hoàn thiện P08 read-only/ACL/replay. Chỉ chạy P07-07/IG08 nếu có grant/gate quyết định riêng. Khi batch test hoàn tất, chạy remediation/retest theo `docs/tests/RULES.md`, ghi batch mới và dừng ở phase được giao.

