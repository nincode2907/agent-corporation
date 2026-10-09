# Bằng chứng triển khai Phase 08 — 09/10/2026

## Phạm vi

Đã bổ sung ba màn hình Observatory vào shell web hiện tại: Văn phòng trực tiếp (S02), Agent Inspector (S03), Phát lại (S04). Các view dùng Owner session, status API và event feed Phase 07 hiện có. Không thêm endpoint, migration, dependency, quyền hoặc gọi inference.

## Hành vi đã triển khai

- **Văn phòng:** các lane đang xử lý, đang chờ, thất bại và chưa biết kết quả lấy từ run đã lưu. Phòng ban nếu có chỉ đến từ Demo Factory và luôn được ghi nhãn fixture. Không gán run cho nhân viên/phòng ban vì source hiện không có quan hệ đó; không có heartbeat worker thì không suy agent active.
- **Inspector:** chọn một run đã lưu; hiển thị trạng thái, model/effort, usage/outcome và event cùng run. Chỉ các trường scalar thuộc allowlist được trình bày. Plan/tóm tắt quyết định, tools/file diff/messages và profile chi tiết hiện ghi rõ chưa có nguồn trong projection; không dựng nội dung thay thế.
- **Replay:** lọc event theo run, chọn mốc bằng slider hoặc timeline và tải lại từ event store. Luồng chỉ đọc; cursor/gap vẫn do API Phase 07 xác thực. Mốc chỉ đại diện cửa sổ đã tải, không tuyên bố chứa toàn bộ lịch sử.
- Metadata cache trong sessionStorage tiếp tục loại payload; payload projection chỉ giữ trong bộ nhớ sau khi nhận từ API/SSE. Đăng xuất đóng SSE và xóa cache theo cơ chế Phase 07.
- Bố cục hỗ trợ desktop/mobile và giao diện tối hiện có; các điều khiển dùng label/focus semantics.

## Kiểm tra source sau khi code

- `rtk proxy npm run --prefix apps/web lint` — exit 0.
- `rtk proxy npm run --prefix apps/web build` — exit 0; TypeScript 6.0.2 và Vite 8.3.3 build.
- `rtk proxy python3 scripts/render_plan.py` — đồng bộ master plan HTML, 24 phase.
- Chưa chạy test suite Phase 08, UI browser hoặc IG08 run thật; chưa có inference grant.

## Điều kiện còn thiếu

Phase 07 và Phase 06 còn Bị chặn tại CG01, grant/test run thật và nghiệm thu dependency. Không có run thật để demo end-to-end; Phase 08 chưa đạt IG08. Sơ đồ phòng ban fixture không phải bằng chứng hoạt động của agent thật. Cần test/review Phase 08 riêng và run/evidence được phép trước khi đánh giá gate.

## Source

- Web: `apps/web/src/App.tsx`, `apps/web/src/RuntimePanel.tsx`, `apps/web/src/RuntimePanel.css`.
- API read contract hiện hữu: `GET /api/v1/runtime/status`, `GET /api/v1/events`, `GET /api/v1/events/stream`.
