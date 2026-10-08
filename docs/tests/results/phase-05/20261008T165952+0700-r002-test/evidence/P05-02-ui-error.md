# P05-02 — HTTP contract error sau remake r001

- Môi trường: Chrome QA tab `http://127.0.0.1:15500/#settings`; API `127.0.0.1:15501` đang chạy process cũ.
- Tương tác: reload Settings, bấm `Probe gateway`; GET `/api/v1/codex/probe` nhận HTTP 404.
- Quan sát accessibility tree sau click: `Contract/cấu hình cần kiểm tra`; `API probe không khả dụng (HTTP 404). Cập nhật API local rồi thử lại.`; nút Probe gateway, Settings, Health, Model profile và Capability vẫn có trong tree.
- Quan sát ảnh màn hình: Settings được render đầy đủ, thông báo lỗi nằm trong card gateway; ảnh hiện trên phiên QA nhưng không có API CUA ghi screenshot vào filesystem.
- Console log API trả về vẫn có các exception cũ từ lần test trước remediation (09:53:32Z và 09:55:32Z); không phát sinh log mới sau reload/click retest (09:59Z). Không kết luận từ log lịch sử như lỗi còn tồn tại.
- Kết luận: non-2xx hiện thành contract error và không làm unmount trang; đây là GET, không prompt/inference.
