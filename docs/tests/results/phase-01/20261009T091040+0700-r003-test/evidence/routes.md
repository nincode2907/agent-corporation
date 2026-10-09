# Route, registry và scope — Phase 01 r003

- Đối chiếu `dev-hub/projects.yml`: Agent Corporation chiếm block `15500–15599`; web `15500` → `agent-corporation.localhost`; API `15501`; PostgreSQL `15510`. Proxy chỉ bật cho web. Ghi chú registry nói proxy publish IPv4 loopback vì Docker host từ chối IPv6 loopback.
- `lsof -nP -iTCP:15500-15599 -sTCP:LISTEN`: Vite `127.0.0.1:15500`, API `127.0.0.1:15501`, Docker/PostgreSQL `127.0.0.1:15510`; không listener khác trong block.
- GET `http://127.0.0.1:15500/` và `http://agent-corporation.localhost/` → HTTP 200.
- GET `/api/v1/health/live` trực tiếp → HTTP 200, `{"status":"ok","service":"api"}`.
- GET `/api/v1/health/ready` trực tiếp và qua hostname proxy → HTTP 200, `{"status":"ok","checks":{"database":"ok"}}`.
- `/favicon.svg` trực tiếp và qua proxy → HTTP 200 `image/svg+xml`; HTML gốc khai báo `lang="vi"` và liên kết `/favicon.svg`. `/favicon.ico` trả 404 nhưng không được HTML yêu cầu.
- Không thử IPv6 route: registry/AGENTS hiện ghi khả năng host không bind IPv6 loopback; URL được xác minh chỉ là IPv4 loopback và hostname proxy.

