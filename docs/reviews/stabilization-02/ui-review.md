# UI review — Stabilization Sprint 02

## Phạm vi capture

Owner-authenticated local UI, desktop **1440×900**, mobile **390×844**. Đã chụp Overview, Playground, Office, Work, Inspector, Replay, Organization, Approvals, Settings; thêm state ảnh cursor gap, offline, stale. Toàn bộ screenshots và manifest nằm trong [contact sheet](evidence/authenticated-fresh/contact-sheet.html), [inventory](evidence/authenticated-fresh/inventory.md) và [ZIP sanitized](evidence/authenticated-ui-review.zip).

Phiên chỉ điều hướng/đọc dữ liệu. POST duy nhất là Owner login/logout; không gửi message, cấp grant, sửa profile, quyết định approval hay dispatch run. Nội dung Playground lịch sử và opaque IDs được làm mờ ở ảnh review. Manifest không chứa token, cookie, CSRF hay response body.

## Findings theo mức độ

### P1 — Recovery sau retention gap chưa hoàn chỉnh

- UI nhận diện gap và hiển thị rõ “Kết nối event store: Có khoảng trống dữ liệu”. Điều này giúp người dùng biết feed không đầy đủ.
- API trả 409 cho cursor vượt retention, nhưng chưa có snapshot endpoint/contract để dựng lại state với cursor hợp lệ. Reload không thể khôi phục gap lịch sử khi retention thực sự đã loại event.
- **Khuyến nghị:** quyết định snapshot contract trước khi triển khai. Kiểm tra gap thật có thể dùng fixture/API test; không cần inference.
- Evidence: `screenshots/states/cursor-gap/1440x900.png`; test mới `test_stabilization02_observability.py`.

### P2 — Trạng thái offline và stale có thể phân biệt

- Khi network offline, UI hiện “Mất kết nối”. Khi stream vẫn mở nhưng không có heartbeat hơn 31 giây, UI hiện “Dữ liệu đã cũ”. Hai nhãn khác nhau và đều hồi phục sau khi online/stream trở lại rồi reload.
- Recovery trong capture có thao tác reload feed; đây không phải bằng chứng auto-reconnect hoạt động sau khi thiết bị mạng thực sự mất kết nối. Active `idle`/`waiting_model` chưa được kiểm tra vì không chạy run.
- Evidence: `screenshots/states/offline/1440x900.png`, `screenshots/states/stale/1440x900.png`, manifest `stateChecks`.

### P2 — Organization chỉ quan sát danh sách nhân viên

- Màn Organization cho phép xem danh sách, nhưng review không thấy employee detail flow. Đây là khoảng trống sản phẩm cần đánh giá riêng, không thuộc scope sửa trong Sprint 02.
- Không thao tác thay đổi nhân viên.
- Evidence: `screenshots/organization/1440x900.png`, `screenshots/organization/390x844.png`.

### P2 — Approval và Work chỉ kiểm tra ở trạng thái đọc

- Đã mở Work và Approvals ở hai viewport. Không gửi quyết định approval do action này có side effect và không có yêu cầu thực hiện.
- Capture chứng minh bố cục/nhãn trong trạng thái hiện có, không chứng minh authorization hay persisted decision.
- Evidence: `screenshots/work/1440x900.png`, `screenshots/approvals/1440x900.png`.

### P2 — Replay read-only journey có evidence tốt hơn

- Lọc/seek/reload thành công; slider hiện diện, 2 GET event reads được quan sát; reload phục hồi. DB snapshots read-only trước/sau so sánh 13 bảng, không thấy khác biệt.
- Request log cho toàn phiên có login/logout POST; manifest ghi riêng `businessWrites: []` cho replay flow. Không truy xuất riêng một artifact endpoint vì không xác định được route tương ứng trong scope hiện tại.
- Evidence: `screenshots/replay/1440x900.png`, `screenshots/replay/390x844.png`, `replay-db-before.json`, `replay-db-after.json`.

## Inventory màn hình

Mỗi màn có desktop và mobile; xem contact sheet để mở ảnh đầy đủ. Capture thấy không có browser page error. Kết luận responsive chỉ áp dụng cho 18 screenshot đã chụp, không thay cho accessibility audit.

| Màn | Nội dung kiểm tra |
| --- | --- |
| Overview | Dashboard và đường điều hướng tới các khu vực. |
| Playground | Profile, grant/history hiển thị; không dùng grant, không gửi message. |
| Office | Trạng thái persisted; không có live run mới. |
| Work | Danh sách/trạng thái công việc, chỉ đọc. |
| Inspector | Chi tiết run/event có sẵn, không tạo run. |
| Replay | Lọc, seek, reload; quan sát event feed. |
| Organization | Danh sách employee; không mở/sửa employee detail. |
| Approvals | Queue hiện tại; không approve/reject. |
| Settings | Owner/session và trạng thái grant; không đổi cấu hình. |

## Kết luận UI

Không có P0 hoặc lỗi P1 về bố cục được xác nhận. P1 duy nhất là giới hạn khôi phục dữ liệu sau retention gap, thuộc API/UI contract. Findings P2 là coverage hoặc product gap; chưa sửa trong sprint. Chi tiết sanitization và từng request xem manifest/inventory.
