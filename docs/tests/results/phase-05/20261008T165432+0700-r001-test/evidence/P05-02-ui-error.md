# P05-02 — Lỗi UI khi API trả HTTP non-2xx

- Môi trường: Chrome tab QA riêng, Vite `127.0.0.1:15500`; API Phase 04 đang chạy ở `127.0.0.1:15501` nhưng chưa nạp route Phase 05.
- Tương tác: Mở Settings, bấm `Probe gateway`; browser gửi GET `/api/v1/codex/probe`, nhận HTTP 404 `{detail:"Not Found"}`.
- Quan sát: UI trắng/unmounted; console: `TypeError: Cannot read properties of undefined (reading 'length') at App (App.tsx:1388:34)`.
- Nguyên nhân trực tiếp: frontend tin HTTP response luôn là GatewayProbe hợp lệ, không kiểm tra `response.ok`/shape; sau đó đọc `gatewayProbe.models.length`.
- Không có prompt/inference; request chỉ là GET. Screenshot tại thời điểm lỗi trắng không cung cấp thêm thông tin nên evidence giữ console/response đã lọc.
