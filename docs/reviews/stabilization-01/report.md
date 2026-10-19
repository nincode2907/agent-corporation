# Stabilization Sprint 01 — Báo cáo tổng kết

- **Ngày:** 18/10/2026 (Asia/Ho_Chi_Minh)
- **Phạm vi:** ổn định UI và bằng chứng cho Phase 06–08; kiểm tra reconnect, Playground bằng fake transport, Inspector/Replay và kiến trúc runtime hiện có.
- **Kết luận:** các sửa lỗi UI và một số kiểm tra hồi quy đã đạt. Phase 06–08 vẫn giữ trạng thái chính thức hiện hành; sprint không nghiệm thu phase, không mở Phase 11, không tạo grant và không gọi inference.
- **Báo cáo liên quan:** [UI/UX review](ui-ux-review.md) · [Next actions](next-actions.md) · [gói chuẩn bị Gemini](gemini-review-package.md).

## 1. Tóm tắt điều hành

Sprint xác nhận UI Lens có thể chụp các màn hình trọng yếu ở desktop và mobile sau khi sửa selector Settings. Browser có Owner session được dùng để mở read-only các route cần bảo vệ, chụp đủ 9 màn hình × 2 viewport, xác nhận không có page horizontal overflow, và kiểm tra hành vi SSE reconnect. Browser logout cuối lượt. Không sửa profile, cấp Session Grant, gửi tin nhắn, tạo run, thực hiện approval hoặc gọi codex-server.

Đã sửa ba điểm giao diện có thể tái hiện: skip link keyboard thiếu main focus target; hàng nút điều hướng phiên Playground bị ép rộng bởi rule nút toàn cục; Inspector/Observatory tràn chiều ngang ở desktop/mobile. Build web đạt. Isolated API suite dùng PostgreSQL tạm và fake transport đạt 143 passed, 11 skipped, 1 warning. Các case cần true offline, cursor gap trên UI, gateway session invalid, run live, cross-scope browser actor, replay DB before/after và IG08 vẫn chưa có đầy đủ bằng chứng.

## 2. Những phần đã làm

### UI Lens và browser evidence

- Đã đăng ký project UI Lens theo `.ui-review.json` ở root: 9 targets (`overview`, `playground`, `office`, `work`, `inspector`, `replay`, `organization`, `approvals`, `settings`) × desktop 1440×900 và mobile 390×844, settle 1200 ms.
- Tái hiện lỗi selector Settings: `a[href="#settings"]` trùng nav link với profile link; locator strict mode không chọn được duy nhất. Selector được giới hạn vào nav (`a.nav-link[href="#settings"]`) và các target điều hướng khác dùng selector tương tự.
- Final capture: [UI Lens manifest](../../../artifacts/ui-review/2026-10-18T15-28-04-437Z_c80b5d46-9af9-4eb2-8155-e3d97c33cd0d/manifest.json), [diagnostics](../../../artifacts/ui-review/2026-10-18T15-28-04-437Z_c80b5d46-9af9-4eb2-8155-e3d97c33cd0d/diagnostics.json). Kết quả 18/18 capture success, không có page error. UI Lens ghi nhận probe `/api/v1/owner/session` trả 401 khi capture anonymous và một số GET health/dashboard bị `net::ERR_ABORTED` lúc điều hướng/chụp; các chi tiết này được giữ trong diagnostics thay vì diễn giải thành lỗi sản phẩm.
- Authenticated browser đã chụp đủ [18 màn hình](evidence/authenticated/manifest.json). Mỗi viewport có `documentWidth` bằng viewport width. Requests được ghi dưới dạng method/path, không chứa request body, session cookie, CSRF token, cursor hay nội dung bí mật.

### Sửa giao diện

- [App.tsx](../../../apps/web/src/App.tsx): thêm `id="main-content"` và `tabIndex={-1}` cho main content để skip link đưa focus bàn phím đúng đích.
- [PlaygroundPanel.css](../../../apps/web/src/PlaygroundPanel.css): đặt width phù hợp cho nút điều hướng phiên để không bị rule `.quiet-button` áp `width: 100%` làm tràn hàng flex trên desktop.
- [RuntimePanel.css](../../../apps/web/src/RuntimePanel.css): cho Inspector heading/action co giãn đúng; giới hạn min/max width của panel; cho grid Observatory có cột `minmax(0, 1fr)`; cho control/label/select co lại; cho nội dung section wrap chuỗi dài.
- Browser keyboard audit xác nhận tab đầu tiên đến “Bỏ qua điều hướng”; Enter chuyển focus vào main. 9 mobile screens có `documentWidth=390`. Nav mobile là vùng cuộn ngang có chủ ý, không phải page overflow.

### Runtime và test

- Web build: `rtk proxy npm run --prefix apps/web build` — thành công, gồm TypeScript build và Vite build.
- API: `rtk proxy uv run --project apps/api python scripts/test_playground_isolated.py` — **143 passed, 11 skipped, 1 warning**. Runner tạo/migrate rồi xóa database và role PostgreSQL tạm. Fake transport; không inference; runtime database không đổi.
- Fake API/persistence regression bao gồm expiry/limit, idempotent duplicate send/concurrency, worker crash/restart, unknown outcome, chặn replay side effect và tools denied. Đây là test isolated, không phải CG01/live proof.
- Controlled SSE interruption: browser điều hướng ra khỏi stream, route `/api/v1/events/stream` bị chặn có chủ đích; UI hiện “Đang kết nối lại”; sau khi bỏ chặn EventSource nhận HTTP 200. 40 event IDs trước/sau giống hệt và cùng thứ tự; request reconnect có cursor. Đây là recovery của event đã lưu, không phải inference/run mới. [Chi tiết gián đoạn](../../tests/results/phase-07/20261018T221600+0700-r006-test/evidence/browser-interruption.md).

## 3. Kiến trúc và luồng code hiện tại

Đây là mô tả source/runtime được sprint quan sát, không phải tuyên bố mọi phase đã nghiệm thu.

```text
Browser — React + TypeScript + Vite
  ├─ Demo UI → API demo routes → PostgreSQL fixture
  ├─ Owner UI → session + CSRF → authenticated API routes
  └─ Runtime/Office/Inspector/Replay → REST reads + SSE event feed
                         ↓
FastAPI modular monolith — apps/api
  ├─ Owner/session, profile và grant boundary
  ├─ Playground sessions/turns, bounded request/usage guards
  ├─ Work Orders, approvals, runtime, event store/feed
  └─ Worker/dispatch orchestration
                         ↓
PostgreSQL — SQLAlchemy/Alembic, durable records/events/outbox
                         ↓ (chỉ khi được cấp grant và worker dispatch)
Codex server gateway → provider/model
```

### Luồng UI

1. Vite serve SPA; `/api` được proxy cùng origin tới FastAPI. Desktop/mobile dùng chung các component; nav mobile tự cuộn ngang.
2. Trang demo đọc fixture và health/readiness qua API. Health phản ánh liveness/readiness, không khởi chạy inference.
3. Owner routes yêu cầu session; các thao tác thay đổi dùng CSRF và backend authorization. Anonymous capture có session probe 401 mặc định-deny.
4. Runtime/Office/Inspector/Replay đọc status, run đã lưu và event feed. SSE cung cấp event của ứng dụng; không đồng nghĩa gateway stream token. Reconnect dùng cursor để tiếp tục từ event store.
5. Replay tái dựng lịch sử đọc được. Sprint chỉ quan sát mở/capture màn; chưa chạy seek/reload có DB before/after nên chưa chứng minh đầy đủ tính bất biến của replay.

### Luồng Playground và giới hạn chứng cứ

1. Owner tạo session/grant theo profile và các hạn mức đã được phê duyệt; backend lưu session, turn, trạng thái request và usage.
2. Worker của app lấy lượt đủ điều kiện, dispatch tới gateway, lưu kết quả và events. Không tự dispatch chỉ vì mở trang.
3. Dữ liệu persistence/fencing/unknown-result được test với fake transport và DB biệt lập. Trong sprint không được cấp grant mới; grant lịch sử Phase 06 đã dùng hết ngày 14/10/2026.
4. Vì vậy ảnh Playground phản ánh session/run lịch sử và trạng thái grant hết hạn; nó không phải bằng chứng cho run mới hay quyền inference hiện hành.

## 4. Kết quả phase có liên quan

| Phase | Batch | Đạt | Còn blocked | Kết luận |
| --- | --- | ---: | ---: | --- |
| 07 | [r006](../../tests/results/phase-07/20261018T221600+0700-r006-test/report.md) | 9/15 criteria | 6/15 | P07-02 reconnect browser clean; P07-05 fake worker restart/unknown clean; P07-01,03,04,06,07 chưa đủ evidence. |
| 08 | [r005](../../tests/results/phase-08/20261018T221600+0700-r005-test/report.md) | 6/15 criteria | 9/15 | UI/read-only route checks và explicit-missing-data copy đạt; live Office, ACL-negative, replay side-effect proof, reload/gap và IG08 còn blocked. |

Không có `fail` trong hai batch; `blocked` nghĩa là thiếu evidence bắt buộc, không chứng minh chức năng đó hỏng. Phase 06 vẫn phụ thuộc CG01/live acceptance. Sprint không sửa trạng thái các phase.

## 5. Kiến trúc chất lượng và rủi ro còn mở

- **Reconnect:** browser chứng minh stream tạm ngắt rồi hồi phục với event đã lưu; chưa đối chiếu DB commit timestamp với event SSE nhận để kết luận P07-01.
- **Offline/stale:** route interruption chứng minh “reconnecting”, không giả lập thiết bị offline thật hoặc heartbeat stale timeout. Không dùng thử `context.setOffline()` bị timeout làm evidence.
- **Cursor boundaries:** API tests kiểm tra tamper/expiry/scope/gap; chưa inject các response này vào browser để xác minh copy và hành động reload.
- **Gateway session:** chưa test session invalid/expired trên fake gateway có liên kết call ledger và context recovery.
- **Office/Inspector:** browser mở được các màn trong Owner scope và thấy run Phase 06 lịch sử; chưa có live run thuộc Phase 08.
- **Replay:** mở route chỉ tạo GET trong browser log; chưa chạy seek/reload với spy write và DB snapshot trước/sau.
- **ACL:** isolated tests đạt phần liên quan; chưa tạo actor/environment thứ hai và chạy browser HTTP/SSE negative test cross-scope.
- **CG01/IG08:** chưa verified; không có inference hoặc grant trong sprint.

## 6. Gemini review

Không thực hiện review bằng Gemini: CLI `gemini` không có trong PATH và session không có Gemini tool/API tích hợp cho task. Không dùng trình duyệt đăng nhập hoặc browser impersonation để lách giới hạn. [Gói review đã chuẩn bị](gemini-review-package.md) có vision, giới hạn, screenshot links và câu hỏi; chưa có `gemini-review.md` vì chưa có review thật.

## 7. Evidence index

- [Authenticated browser manifest và 18 screenshot links](evidence/authenticated/manifest.json)
- [Browser audit trước/sau](evidence/browser-audit-after.json)
- [Script audit responsive/keyboard](evidence/browser_audit.mjs)
- [Script review authenticated và SSE](evidence/authenticated_review.mjs)
- [Phase 07 r006 report](../../tests/results/phase-07/20261018T221600+0700-r006-test/report.md) · [commands](../../tests/results/phase-07/20261018T221600+0700-r006-test/evidence/commands.md)
- [Phase 08 r005 report](../../tests/results/phase-08/20261018T221600+0700-r005-test/report.md) · [commands](../../tests/results/phase-08/20261018T221600+0700-r005-test/evidence/commands.md)
- [UI Lens capture root](../../../artifacts/ui-review/2026-10-18T15-28-04-437Z_c80b5d46-9af9-4eb2-8155-e3d97c33cd0d/)

