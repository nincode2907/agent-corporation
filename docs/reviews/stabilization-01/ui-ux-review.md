# UI/UX review — Stabilization Sprint 01

Review dựa trên UI Lens capture, authenticated Chromium browser và source CSS/TSX. Viewports: desktop 1440×900 và mobile 390×844. Đây là review có scope stabilization, không đề xuất đổi IA hoặc redesign toàn sản phẩm.

## Tóm tắt

- 18/18 UI Lens captures thành công; 18/18 authenticated screen states không làm document rộng hơn viewport.
- Mobile nav là vùng cuộn ngang có chủ ý. Welcome ornament/label có phần tử con vượt bounds hoặc text bị cắt bên trong container, nhưng document không tràn; không nên nhầm các điểm này thành page overflow.
- Đã sửa keyboard skip target và hai cụm layout responsive (Playground session nav, Inspector/Observatory).
- Các `401` anonymous session probe trong UI Lens là default-deny; `net::ERR_ABORTED` ở health/dashboard được ghi khi capture chuyển route. Không có page errors. Xem [diagnostics](../../../artifacts/ui-review/2026-10-18T15-28-04-437Z_c80b5d46-9af9-4eb2-8155-e3d97c33cd0d/diagnostics.json).

## Phát hiện và xử lý

| Ưu tiên | Màn hình / vấn đề | Bằng chứng | Xử lý / trạng thái |
| --- | --- | --- | --- |
| P1 | Keyboard skip link trước đây trỏ `#main-content` nhưng main chưa focusable, khiến keyboard user không thể chuyển focus vào nội dung | [Browser audit](evidence/browser-audit-after.json) | Đã thêm `id` + `tabIndex=-1` cho main. Tab đầu tiên focus “Bỏ qua điều hướng”; Enter focus main: pass. |
| P1 | Inspector heading/action và Observatory controls có min-width/column sizing làm panel tràn trên viewport nhỏ; desktop cũng có thể bị action sizing | [Inspector desktop](evidence/authenticated/screenshots/inspector/1440x900.png), [Inspector mobile](evidence/authenticated/screenshots/inspector/390x844.png) | Đã giới hạn flex/control width, grid dùng `minmax(0, 1fr)`, text dài wrap. Sau sửa document width bằng viewport. |
| P1 | Playground session navigation buttons nhận `width:100%` từ `.quiet-button`, khiến hàng ngang rộng hơn cần thiết | [Playground desktop](evidence/authenticated/screenshots/playground/1440x900.png), [Playground mobile](evidence/authenticated/screenshots/playground/390x844.png) | Đã override width trong session nav; build và capture sau sửa pass. |
| P2 | UI Lens Settings target match cả nav Settings lẫn Owner profile `href="#settings"` | [Phase 07 commands](../../tests/results/phase-07/20261018T221600+0700-r006-test/evidence/commands.md) | Đổi sang nav-scoped selector; final capture Settings desktop/mobile thành công. |
| P2 | Một số route khi anonymous tạo 401 console/HTTP do probe Owner session; mỗi capture cũng có thể abort GET khi điều hướng | [UI Lens diagnostics](../../../artifacts/ui-review/2026-10-18T15-28-04-437Z_c80b5d46-9af9-4eb2-8155-e3d97c33cd0d/diagnostics.json) | Chưa cần đổi hành vi bảo mật: authenticated browser xác nhận route hoạt động; không có JS page error. Theo dõi riêng nếu diagnostics tiếp tục gây nhiễu review tự động. |

## Ảnh màn hình

Các ảnh dưới đây lấy từ authenticated browser sau khi đăng nhập Owner, ở mode read-only. Manifest có đầy đủ 18 đường dẫn và metadata: [manifest.json](evidence/authenticated/manifest.json).

| Khu vực | Desktop | Mobile |
| --- | --- | --- |
| Tổng quan | [1440×900](evidence/authenticated/screenshots/overview/1440x900.png) | [390×844](evidence/authenticated/screenshots/overview/390x844.png) |
| Playground | [1440×900](evidence/authenticated/screenshots/playground/1440x900.png) | [390×844](evidence/authenticated/screenshots/playground/390x844.png) |
| Văn phòng | [1440×900](evidence/authenticated/screenshots/office/1440x900.png) | [390×844](evidence/authenticated/screenshots/office/390x844.png) |
| Work Orders | [1440×900](evidence/authenticated/screenshots/work/1440x900.png) | [390×844](evidence/authenticated/screenshots/work/390x844.png) |
| Inspector | [1440×900](evidence/authenticated/screenshots/inspector/1440x900.png) | [390×844](evidence/authenticated/screenshots/inspector/390x844.png) |
| Replay | [1440×900](evidence/authenticated/screenshots/replay/1440x900.png) | [390×844](evidence/authenticated/screenshots/replay/390x844.png) |
| Tổ chức | [1440×900](evidence/authenticated/screenshots/organization/1440x900.png) | [390×844](evidence/authenticated/screenshots/organization/390x844.png) |
| Approval Inbox | [1440×900](evidence/authenticated/screenshots/approvals/1440x900.png) | [390×844](evidence/authenticated/screenshots/approvals/390x844.png) |
| Cấu hình | [1440×900](evidence/authenticated/screenshots/settings/1440x900.png) | [390×844](evidence/authenticated/screenshots/settings/390x844.png) |

## Tiếp tục review

1. Thêm browser states cho loading/error/empty trên Inspector và Office; hiện ảnh chủ yếu là populated historical data.
2. Inject cursor expiry/gap/invalid scope vào browser và xác nhận message, recovery/reload path.
3. Chạy Replay seek/reload với read-only network assertion và DB before/after snapshot.
4. Khi có grant/IG riêng được cấp đúng scope, kiểm tra run live tới Office/Inspector/SSE. Không dùng run Phase 06 thay bằng chứng Phase 08.

