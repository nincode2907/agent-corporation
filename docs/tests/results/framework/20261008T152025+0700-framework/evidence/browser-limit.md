# Giới hạn kiểm tra giao diện

Đã thử mở `docs/tests/index.html` trong Chrome để kiểm tra trực quan. Browser policy từ chối protocol `file://` và chỉ cho phép `http:`/`https:`. Thông báo yêu cầu không thử lại qua server/proxy/alternate browser surface; nên không có screenshot hoặc kiểm tra layout trực tiếp. Kiểm tra HTML tĩnh, đồng bộ nguồn, lang, favicon, phase anchors và links đã chạy bằng validator. Trình duyệt trực tiếp không dùng cho kiểm định này.
