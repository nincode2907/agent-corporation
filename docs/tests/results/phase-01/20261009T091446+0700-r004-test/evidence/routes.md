# Bằng chứng HTTP và trình duyệt — Phase 01 r004

Mọi request chủ động là HTTP GET. Không thay đổi runtime, cấu hình proxy hoặc dữ liệu.

| URL | Kết quả quan sát |
| --- | --- |
| `http://127.0.0.1:15500/` | HTTP 200, `text/html`. |
| `http://127.0.0.1:15500/favicon.svg` | HTTP 200, `image/svg+xml`. |
| `http://127.0.0.1:15501/api/v1/health/live` | HTTP 200, `{"status":"ok","service":"api"}`. |
| `http://127.0.0.1:15501/api/v1/health/ready` | HTTP 200, `{"status":"ok","checks":{"database":"ok"}}`. |
| `http://127.0.0.1:15500/api/v1/health/ready` | HTTP 200 qua Vite same-origin proxy; DB `ok`. |
| `http://agent-corporation.localhost/` | HTTP 200, `text/html`. |
| `http://agent-corporation.localhost/api/v1/health/ready` | HTTP 200, DB `ok`, qua Dev Hub/Caddy hostname IPv4. |

Chrome tab mới do AI test mở tới `http://agent-corporation.localhost/#settings`; accessibility tree hiển thị tiêu đề “Cấu hình & sức khỏe”, API nội bộ và PostgreSQL đều “Đang hoạt động”, inference grant `0`, Gateway “Chưa chạy probe trong phiên này”. Không bấm “Probe gateway”, “Đặt lại demo” hoặc thao tác ghi nào. Trang cho biết demo fixture hiện có; fixture này thuộc Phase 04, không thể dùng lượt đọc này để kết luận thời điểm nó được tạo.

Không kiểm tra IPv6 bằng cách đổi bind/proxy; Dev Hub registry và AGENTS hiện hành ghi proxy chỉ publish IPv4 loopback do Docker từ chối IPv6 loopback. `api.agent-corporation.localhost` có `proxy_enabled: false` trong registry nên không phải URL Phase 01 được công bố.
