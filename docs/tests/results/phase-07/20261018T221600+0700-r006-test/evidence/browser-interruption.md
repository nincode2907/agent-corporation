# P07-02 — Browser stream interruption/reconnect

- **URL:** `http://127.0.0.1:15500/#settings`
- **Browser:** Chromium `156.0.8078.4`; viewport `1440×900`.
- **Setup:** Owner login bằng secret local có sẵn; chuyển khỏi runtime để stream hiện hành đóng; dùng Playwright route interception để chặn `/api/v1/events/stream` khi Settings remount RuntimePanel. Không chặn `/api/v1/events`, không tạo event/model call.
- **Expected:** Stream lỗi chuyển UI sang reconnecting; retry dùng cursor; khi chặn được gỡ stream nhận lại 200; danh sách lịch sử giữ cùng event ID/thứ tự.
- **Observed:** UI hiện `Đang kết nối lại`; trong lúc route interception ghi nhận 4 request stream bị chặn/retry. Request `/api/v1/events` và reconnect EventSource có `cursor` query. Sau gỡ route, EventSource nhận HTTP 200, UI trở lại `Đã kết nối`.
- **Event list:** 40 event ID trước và sau giống hệt nhau theo thứ tự; 0 ID bị thêm/mất/nhân đôi trong cửa sổ kiểm tra.
- **Network methods:** GET only trong reconnect; phần auth riêng có POST login và logout. Không gọi `/runtime/runs`, `/playground/.../send`, grant, gateway hoặc model dispatch.
- **Tag:** `clean`; đây là bằng chứng reconnect trên events đã persisted, không phải run inference mới.
- **Artifact đầy đủ:** [`authenticated/manifest.json`](../../../../../reviews/stabilization-01/evidence/authenticated/manifest.json) (chứa `networkInterruption`, request metadata, viewports và screenshots).

## Giới hạn chạy

- Cursor expired/gap được kiểm trong API suite nhưng không inject vào browser UI ở batch này.
- `context.setOffline(true)` không làm EventSource đổi state trong timeout 10 giây; phương thức này không được dùng làm bằng chứng offline. Test cuối dùng route interception chặn SSE và chỉ kết luận `reconnecting`, không khẳng định thiết bị ở trạng thái offline.
- Không restart API/worker dùng chung trong lúc kiểm tra; worker lifecycle/crash checks được chạy qua isolated fake tests.
