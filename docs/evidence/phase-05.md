# Bằng chứng Phase 05 — Kết nối Codex server local

Ngày: 08/10/2026 · Bàn giao: **Chờ Chủ tịch nghiệm thu** · Inference grant: **0**.

## Dependency và quyền

- Phase 03 đã được nghiệm thu. Phase 04 vẫn **Chờ nghiệm thu**: report ghi thiếu bằng chứng isolation cho ledger/thread/file store chưa tồn tại và screenshot UI chưa lưu. Chủ tịch đã yêu cầu tiếp tục Phase 05 sau khi sửa finding Phase 01; trạng thái Phase 04 giữ nguyên. Phase 05 triển khai probe độc lập, nhưng không coi dependency 04 đã nghiệm thu.
- Runtime codex-server hiện có theo baseline là `127.0.0.1:4000`; GET probe trả kết nối offline. Không start/restart gateway, không sửa config dùng chung, không đọc token/session/transcript.
- Không có inference grant. Chỉ phát triển và kiểm tra GET/fixture; không gọi chat, session, model hoặc tool.

## Tích hợp đã làm

- API `GET /api/v1/codex/probe` dùng cấu hình backend `CODEX_SERVER_BASE_URL` (mặc định `http://127.0.0.1:4000`) và `CODEX_SERVER_API_KEY` tùy chọn. Secret chỉ làm Bearer header từ backend; không xuất trong payload/UI/log.
- Adapter chấp nhận HTTP trên literal loopback IP, từ chối DNS/arbitrary host, URL credentials/path/query/fragment, chặn redirect, timeout 2 giây, giới hạn body 256 KiB. Chỉ GET `/health` và `/v1/models`; response được chuẩn hóa và danh sách chỉ giữ model ID.
- Settings UI chỉ probe khi bấm nút. Không có probe khi startup, health check hay mở profile. UI phân biệt offline/auth/rate-limit/contract mismatch; model catalog luôn ghi entitlement chưa xác minh.
- Profile chưa thể ghi/sửa owner-only: chưa có identity/auth được xác minh ở API hiện tại. UI nêu rõ chưa cấu hình và không nhận actor tự khai báo.
- Không có queue bền vững hoặc allowlist fallback do Owner quản lý; adapter không tự retry 429 hoặc fallback. Đưa request model trở lại queue cần orchestration/persistence và policy ở phase có phạm vi đó.

## Contract/capability matrix

Nguồn: codex-server README, `src/server.ts`, `src/schema.ts`, `src/provider.ts`, `src/config.ts`, `docs/TECHNICAL.md`; hashes và trạng thái runtime nằm trong [manifest test](../tests/results/phase-05/20261008T161028+0700-phase05-probe/evidence/source-manifest.json).

| Capability | Bằng chứng source | Kết quả Phase 05 |
| --- | --- | --- |
| `GET /health` | `{ok, provider, active_requests}` | Contract đã đối chiếu; live **blocked/offline** |
| `GET /v1/models` | `{object:"list", data:[{id,...}]}` gồm configured model + catalog chat-supported | Contract đã đối chiếu; live **blocked/offline**; catalog không chứng minh entitlement |
| Auth | `LOCAL_API_KEY` optional; Bearer bảo vệ các data endpoints, dashboard asset là ngoại lệ | Secret ref backend hỗ trợ; live auth chưa kiểm được vì server offline |
| Chat request | `POST /v1/chat/completions`, text; request có model/reasoning, `stream:false`; schema không hỗ trợ max_tokens | Không gọi; không claim runtime behavior ở batch này |
| Streaming / max_tokens | Không được hỗ trợ theo README/schema | Không hỗ trợ; không giả lập như capability |
| Native tools | Function calls là proposal; app gọi function, gateway không thực thi native app tool | Không dispatch; adapter probe chỉ GET |
| Session | Session API tạo/lưu transcript; Phase 05 không dùng | Không dùng |
| Read isolation | Provider sandbox `read-only`, shell/network/tools hạn chế; source kỹ thuật ghi sandbox không ngăn đọc dữ liệu user trên máy | **CG01 BLOCKED** trước khi gửi input |
| Privacy/retention | Gateway `sessions.json` lưu messages; chat stateless vẫn tạo Codex thread/rollout | **CG01 BLOCKED**; không gửi prompt thử nghiệm |
| Fallback/429 | Gateway có concurrency 429; Agent Corporation chưa có durable queue/Owner allowlist | Không retry/fallback; queue integration **BLOCKED** |

## Kết quả kiểm thử

- API unit/integration cho health và adapter: 9 passed, gồm kiểm proxy môi trường không được chuyển tiếp request hoặc Bearer header.
- Web lint và TypeScript/Vite production build: pass.
- Fake cases: available contract, offline, 401, 429, schema mismatch, external-host rejection; spy chứng minh chỉ gọi 2 GET allowlist, secret canary không xuất hiện trong output.
- Live gateway: offline. Không chạy fresh install/migration/DB-writing suite; đây không thuộc phạm vi Phase 05.
- Chi tiết từng case, tag, command và giới hạn ở [report batch](../tests/results/phase-05/20261008T161028+0700-phase05-probe/report.md).

## Kết luận

Có bản tích hợp probe read-only và UI để review, nhưng Phase 05 **chưa đủ bằng chứng** cho live health/models/auth, owner-only profile, durable 429 queue/fallback, và CG01. Không gửi input để vượt privacy gap, không thay gateway/proxy, không đánh dấu Phase 04 complete và không bắt đầu Phase 06. Chờ quyết định của Chủ tịch sau nghiệm thu đặc tả/kết quả.
