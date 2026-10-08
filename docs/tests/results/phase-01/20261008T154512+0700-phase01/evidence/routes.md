# HTTP và browser — Phase 01

Thời điểm: 08/10/2026, Asia/Ho_Chi_Minh. Chỉ GET, không inference.

- Trước khi khởi động frontend, `127.0.0.1:15500` không có listener và HTTP trả 000; hostname trả 502 do upstream chưa có.
- Vite dev server khởi động thành công ở `127.0.0.1:15500`; lệnh trong [commands.md](commands.md). Server được giữ trong PTY tương tác để còn log.
- Sau khi khởi động: direct web IPv4 HTTP 200; `/api/v1/health/ready` qua Vite HTTP 200 với database ok.
- Hostname `http://agent-corporation.localhost/` HTTP 200, remote IP `127.0.0.1`. Host API `api.agent-corporation.localhost` health/live HTTP 200.
- Browser Chrome mở direct URL, title “Agent Corporation · Tổng quan”. Accessibility tree hiển thị API/PostgreSQL sẵn sàng; demo gắn fixture; inference grant “Chưa được cấp”; copy ghi rõ seed/reset không gọi model. Không bấm reset hoặc mutate dữ liệu.
- Favicon `/favicon.svg` HTTP 200 (`image/svg+xml`); HTML `lang="vi"`.
- IPv6 direct `[::1]:15500` không có listener (curl exit 7/HTTP 000), khớp giới hạn môi trường Chủ tịch ghi trong [AGENTS.md](../../../../../../AGENTS.md#runtime-phase-01). Không claim IPv6 route hoạt động.
- PostgreSQL `127.0.0.1:15510` và API `127.0.0.1:15501` có listener từ trước batch; HTTP readiness đều đạt. Không dừng/restart DB/API vì Phase 04 đang dùng.
