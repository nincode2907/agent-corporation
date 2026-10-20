# Integration Fix 05.1 — Runtime reconciliation contract

## Mục tiêu

Cho Owner xem bằng chứng của Run đã interrupted/unknown và ghi nhận quyết định kiểm tra mà không sửa lịch sử call. Với evidence không đủ kết luận, outcome giữ `unknown`, usage/cost giữ `unknown`, request grant đã tiêu thụ không được hoàn lại và global dispatch guard vẫn giữ nguyên.

## API và quyền

- `GET /api/v1/runtime/runs/{run_id}/reconciliation`: `require_owner`; mọi truy vấn gắn `environment_id` + `company_id` từ Owner session, không nhận scope từ client.
- `POST /api/v1/runtime/runs/{run_id}/reconciliation`: `require_owner_write` (Owner session, local Host/Origin, CSRF), body strict `decision="unresolved_retained"` và lý do tối đa 500 ký tự; bắt buộc header `Idempotency-Key` UUID.
- Backend kiểm tra Run/call thuộc scope hiện tại, call mới nhất còn `unknown`, và guard vẫn trỏ đúng request span. Giao dịch khóa hàng guard; decision receipt và event được ghi cùng transaction.
- Cùng idempotency key + payload trả lại receipt cũ. Cùng key với payload khác bị từ chối. Các lần ghi đều append; role ứng dụng chỉ có `SELECT, INSERT` trên `runtime_reconciliation_decisions`.
- Không có endpoint xác nhận completion/cancellation từ một khẳng định Owner tự nhập. Read view chỉ gán completion cho final response đã lưu; cancellation cho Run bị hủy trước khi có model call; known pre-dispatch failure cho trường hợp có receipt cục bộ/không có model call. Gateway cancellation không có receipt tin cậy thì tiếp tục là `unresolved`.

## Dữ liệu được hiển thị

View trả Run/task/employee version/timestamp/outcome, các model-call span và gateway call ID nếu đã được lưu, checkpoint metadata đã lọc (không trả prompt history), trạng thái lease/heartbeat, grant và usage provenance, cost status luôn `unknown`, trạng thái guard, event IDs liên quan và Owner decisions trước đó. Không hiển thị prompt/output trong view này.

## State transitions

| Evidence trong ledger | Classification | Guard |
|---|---|---|
| Final response được lưu | `confirmed_completion` | Đã nhả bởi normal finish |
| Run bị Owner hủy khi chưa dispatch | `confirmed_cancellation` | Không có request span |
| Không có span và Run failed/cancelled | `confirmed_pre_dispatch_failure` / `confirmed_cancellation` | Không có span |
| Span failed với reason thuộc allowlist pre-HTTP | `confirmed_pre_dispatch_failure` | Đã nhả bởi normal finish |
| Call `unknown`, guard vẫn giữ span đó | `unresolved`; chỉ cho phép ghi `unresolved_retained` | Giữ nguyên |
| Dữ liệu khác hoặc thiếu | `unresolved` | Không tự thay đổi |

Không có “force unlock”. Ghi decision không gọi worker/gateway, không tạo Run mới, không đổi status/checkpoint/usage/ledger, không tăng lại grant, không vượt Emergency Stop và không xác nhận rằng Run cũ đã được reconcile.

## Gateway evidence và giới hạn

Gateway source `src/server.ts` phát `X-Codex-Call-Id` khi nhận HTTP request, hủy provider khi client disconnect và trả `/health` với số active request. Gateway cũng có call metrics/read routes, nhưng app Runtime hiện gọi stateless `/v1/chat/completions`, không có giao thức callback/status/cancellation receipt bền vững được nối với Runtime span. API health `active_requests=0` là snapshot toàn gateway, không chứng minh một call cụ thể đã hoàn tất hay usage/cost bằng 0. Khi transport bị hủy trước final response, adapter có thể không nhận được call ID header; gateway call ID vì vậy chỉ là `if available`.

Không đủ evidence để an toàn nhả guard của call unknown. Tiếp tục giữ guard cho đến khi có final response/correlation evidence tin cậy được xác minh theo cùng call ID. Nếu cần chạy demo trong lúc call cũ vẫn unresolved, dùng một runtime demo cô lập riêng với database/artifacts/Owner/config tách biệt, concurrency 1 và một grant mới được Chủ tịch cấp cho đúng batch; không dùng risk-ack để coi call cũ đã xong hoặc tái sử dụng guard/Run cũ. Owner có thể chọn chờ evidence hoặc phê duyệt môi trường demo cô lập; bước cấp grant/deploy/inference là quyết định riêng.
