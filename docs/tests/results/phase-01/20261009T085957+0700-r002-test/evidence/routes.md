# Bằng chứng HTTP và trình duyệt — retest Phase 01

- Thời gian: 2026-10-09 09:00 +07:00.
- Không restart/chỉnh cấu hình runtime dùng chung; chỉ GET các đường health/page.
- `http://127.0.0.1:15500/`: HTTP 200, remote `127.0.0.1`.
- `http://127.0.0.1:15501/api/v1/health/live`: HTTP 200.
- `http://127.0.0.1:15501/api/v1/health/ready`: HTTP 200, `{"status":"ok","checks":{"database":"ok"}}`.
- `http://127.0.0.1:15500/api/v1/health/ready`: HTTP 200 cùng-origin qua Vite proxy, DB `ok`.
- `http://127.0.0.1:15500/favicon.svg`: HTTP 200.
- `http://agent-corporation.localhost/`: HTTP 200, remote `127.0.0.1`.
- Chrome accessibility tree: title `Agent Corporation · Tổng quan`, URL đúng loopback, nội dung `Không gian local`, `Chưa có công ty thật`, `Inference grant — Chưa được cấp`. Trang render được; fixture demo chưa seed nên hiển thị trạng thái chưa có dữ liệu. Không bấm seed, không POST.
- Giới hạn mạng: Dev Hub/AGENTS hiện ghi proxy publish IPv4 loopback; không yêu cầu hay cấu hình IPv6.
