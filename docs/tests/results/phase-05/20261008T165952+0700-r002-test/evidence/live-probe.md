# Live probe Phase 05 r002

- Gateway: `GET http://127.0.0.1:4000/health`, timeout 3s → connection refused, HTTP 000.
- Application API: `GET http://127.0.0.1:15501/api/v1/codex/probe`, timeout 4s → HTTP 404 `{detail: "Not Found"}`. Đây là process đang phục vụ Phase 04; không restart trong lượt này.
- Không gửi input, không gọi `POST /v1/chat/completions`, không tạo session, inference grant = 0.
- Source gateway đã có ở manifest r001/Phase 05 evidence. Kết luận: live contract/runtime chưa kiểm chứng được trong batch này.
