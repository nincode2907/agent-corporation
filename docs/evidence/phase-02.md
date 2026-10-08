# Bằng chứng Phase 02 — Khung giao diện Chủ tịch

Ngày triển khai: 08/10/2026 · Trạng thái: **Hoàn tất theo chỉ thị chuyển tiếp sang Phase 03**.

## Dependency và giới hạn

- Phase 00 đã được nghiệm thu; Phase 01 đã được Chủ tịch duyệt khi giao Phase 02. Khi giao Phase 03 trực tiếp, Phase 02 được tiếp nhận làm dependency; không xem đó là xác minh viewport 390 px.
- Runtime được kiểm tra trước và sau thay đổi: `http://127.0.0.1:15500/` trả HTTP 200; `GET /api/v1/health/live` trả 200; `GET /api/v1/health/ready` trả `{"status":"ok","checks":{"database":"ok"}}`; favicon trả HTTP 200.
- Không gọi codex-server, model, chat/session hay inference. Grant vẫn bằng 0. S13 nói rõ capability probe thuộc Phase 05.
- Không tạo domain schema, company, employee, task, event hay dữ liệu fixture. S14 vẫn khóa thao tác thành lập công ty thật tới sau release V1.

## Thay đổi đã triển khai

- Thay health-only landing page bằng dashboard điều hành tiếng Việt, thanh điều hướng đủ 14 khu vực S01–S14, URL hash có thể bookmark/back, tiêu đề trang cập nhật theo khu vực, skip link và trạng thái mục hiện hành.
- Hai mode Chủ tịch/Vận hành chỉ đổi góc nhìn. Cả hai hiển thị cùng vai trò Owner; không đổi quyền API.
- S01 dashboard phân biệt dữ liệu nghiệp vụ chưa tồn tại với health hệ thống lấy trực tiếp từ API. S13 có health view và retry thủ công; không có poll/model call tự động.
- S02–S12 hiển thị khung theo phạm vi phase tương ứng cùng thông báo chưa có dữ liệu; S14 hiển thị trạng thái khóa. Không dựng agent, hoạt cảnh live hoặc metric giả.
- Khi API không sẵn sàng, cả health row, nhãn trạng thái tổng hợp và thông báo phục hồi phản ánh lỗi; retry thực hiện lại đúng hai health GET. CSS có reflow tại 760 px và 430 px, cuộn ngang riêng cho điều hướng trên màn hình nhỏ, focus-visible và reduced-motion.
- Giữ React/Vite hiện hữu, không thêm dependency hoặc đổi kiến trúc/runtime.

## Kiểm tra và kết quả

```text
npm run --prefix apps/web lint   PASS — oxlint, không báo lỗi
npm run --prefix apps/web build  PASS — tsc -b và Vite production build
GET http://127.0.0.1:15500/      PASS — HTTP 200
GET /favicon.svg                 PASS — HTTP 200
GET API health/live              PASS — HTTP 200
GET API health/ready             PASS — database ok
git diff --check                 PASS — không có whitespace error
```

Kiểm tra Chrome desktop: thấy đủ 14 link điều hướng; mở S05 Công việc giữ empty state không fixture; S13 chỉ trình bày API/PostgreSQL readiness thật, nêu gateway chưa probe; S14 khóa rõ wizard. Chuyển mode Vận hành đổi trạng thái lựa chọn và nội dung góc nhìn, vẫn nói cùng quyền Owner. Tiêu đề tab theo route.

Đã dừng API trong một lượt kiểm tra có kiểm soát: sau reload dashboard hiển thị API/PostgreSQL “Chưa kết nối” và hướng khôi phục. Khởi động lại API trong PTY; direct readiness và Vite proxy cùng trả 200, database `ok`. Sau đó sửa nhãn tổng hợp để phân biệt rõ “Sẵn sàng / Đang kiểm tra / Không kết nối”, tránh hàm ý đang stream liên tục. Không thao tác Chrome thêm sau khi trình duyệt báo người dùng lấy lại quyền điều khiển, nên thay đổi nhãn cuối chưa được quan sát lại trên browser.

Rà soát thiết kế: giữ layout điều hành tiết chế, palette xanh rêu/đá, chữ serif cho tiêu đề và biểu tượng quỹ đạo tĩnh làm dấu nhận diện; không dùng chuyển động hay số màn hình kiểu tiến trình để tránh gợi ý có agent đang hoạt động.

## Giới hạn kiểm chứng còn lại

- CSS responsive breakpoint cho chiều rộng 390 px đã được triển khai, nhưng không đo overflow/screenshot tại viewport cố định 390 px: browser control bị người dùng lấy lại trước khi hoàn tất công cụ thiết bị. Cần xác minh ở lượt nghiệm thu hoặc trình duyệt có viewport override.
- Semantic navigation, skip link, focus-visible, `lang="vi"`, reduced motion và favicon đã được kiểm tra trong source/build; chưa chạy audit accessibility chuyên biệt hoặc keyboard-only sweep đầy đủ.
- Ảnh Chrome desktop đã được quan sát trong phiên kiểm tra nhưng chưa lưu thành artifact ảnh trong repository.
- Tại thời điểm bàn giao Phase 02, S02–S12 là preview shell; chức năng domain chưa được triển khai trong phase đó.

## Bàn giao

Các thay đổi UI nằm tại `apps/web/src/App.tsx`, `apps/web/src/App.css` và `apps/web/index.html`; cập nhật trạng thái/evidence ở `docs/master-plan.md`, `docs/evidence/phase-01.md`, README và hướng dẫn project. Phase 02 được tiếp nhận ngày 08/10/2026 theo chỉ thị trực tiếp bắt đầu Phase 03. Giới hạn viewport 390 px vẫn cần xác minh nếu trở thành tiêu chí phát hành.
