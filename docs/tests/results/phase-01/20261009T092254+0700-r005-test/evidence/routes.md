# Registry, routes và scope — Phase 01 r005

- Dev Hub registry: block `15500–15599`; web `15500` → `agent-corporation.localhost` (proxy bật), API `15501` và PostgreSQL `15510` (proxy tắt). Compose/Vite/README khớp mapping. Registry xác nhận proxy IPv4 loopback-only.
- `lsof -nP -iTCP:15500-15599 -sTCP:LISTEN`: Vite `127.0.0.1:15500`, API `127.0.0.1:15501`, Docker/PostgreSQL `127.0.0.1:15510`; không listener khác trong block.
- Checkout hiện tại GET web direct và hostname `/` → 200; direct API liveness/readiness và readiness qua hostname → 200; `/favicon.svg` qua hostname → 200 `image/svg+xml`.
- Bản sao sạch: Vite/API cùng bind IPv4 loopback port ephemeral 56118/56117. Khi chỉ dừng PostgreSQL test container, direct và Vite-proxy liveness → 200; readiness → 503 với body chỉ nêu DB unavailable; dashboard → 503 với thông báo tổng quát. Không có connection string/stack trace trong response.
- UI lỗi được xác minh qua accessibility tree sau reload: API còn hoạt động, PostgreSQL “Chưa kết nối”; hiển thị lỗi readiness và demo unavailable. UI khỏe được xác minh trước khi dừng DB.
- Không thử route IPv6; không được công bố IPv6. `api.agent-corporation.localhost`/database hostname không proxy theo registry.

