# ADR-0004 — Scoped Snapshot với Watermark Cursor

> Ngày: 19/10/2026 · Scope: phục hồi projection event/Office/Inspector/Replay · Quyết định được Chủ tịch giao trong Stabilization Sprint 03. Quyết định này không nghiệm thu Phase 07/08, không cấp inference/grant và không cho phép mở Phase 11.

## Bối cảnh

Owner event feed dùng `stream_seq` tăng theo company và cursor HMAC gắn environment/company/session. Khi event trước cursor đã bị retention xóa, API trả 409. Frontend giữ metadata trong `sessionStorage` nhưng không có cách tải lại state và bắt đầu cursor hợp lệ. Reload không thể dựng event đã mất. Gọi các endpoint projection riêng lẻ cũng không tạo được một watermark nhất quán với run state.

## Quyết định

Thêm `GET /api/v1/events/snapshot-v1` làm một lần đọc projection có phiên bản và watermark, dùng chung event store/cursor hiện tại.

- Yêu cầu Owner session hiện hành; scope chỉ lấy từ `OwnerPrincipal`, không từ query/body. PostgreSQL RLS và filter đều gắn environment/company.
- Một transaction `REPEATABLE READ, READ ONLY` đọc run projection và event high-watermark. Cursor HMAC ràng buộc phiên/scope, gắn watermark và anchor retained-event hiện tại.
- Snapshot trả tối đa 200 event mới nhất, tối đa 20 run, tối đa 512 KiB. Chỉ public/redacted event envelope và các trường run đang được Runtime UI dùng; không có prompt, artifact content, gateway transcript, host path hay admin data.
- `history_gap` phân biệt phần lịch sử đã mất/chuỗi sequence rỗng bên trong; `replay_window_start_seq` cho biết giới hạn cửa sổ 200 event. Snapshot không tái tạo event đã mất. Replay giữ cảnh báo gap không thể phục hồi; cửa sổ cũ hơn chỉ được nêu là ngoài trang hiện tại khi nguồn vẫn liên tục.
- Snapshot không ghi DB, append event, dispatch queue, gọi gateway, inference hoặc tool. Không thay execution state và không tạo source of truth mới; chỉ chiếu event store và runtime projection hiện có.
- Client thay event/run projection sau khi xác thực response rồi mở SSE bằng cursor watermark. Commit xảy ra sau snapshot có sequence lớn hơn watermark và được stream phát khi mở SSE. Trùng ID/sequence bị dedup; sequence nhảy kích hoạt snapshot thay vì tiếp tục với tiến độ thiếu.
- Gap lặp khi retention đổi giữa snapshot và SSE chỉ được thử lại hữu hạn; nếu chưa đồng bộ được, UI giữ trạng thái gap và yêu cầu người dùng thử lại. HTTP 401 tiếp tục theo Owner session flow; snapshot quá giới hạn trả 413 và báo rõ.

## Lý do và đánh đổi

Đọc các projection riêng bằng nhiều request có thể trộn trạng thái trước/sau một commit; lấy cursor sau khi đọc event cũng có thể bỏ qua commit chen giữa. Một transaction lặp lại được cùng watermark cùng run state, còn event stream counter được khóa theo transaction ghi nên commit sau watermark nhận sequence lớn hơn. Snapshot không tuyên bố lịch sử đầy đủ: retention gap là sự thật hiển thị, không được che bằng tổng hợp trạng thái giả.

Giới hạn 200 event/20 run giữ response và UI bounded. 512 KiB là hard ceiling; nếu vượt, endpoint từ chối toàn bộ response thay vì cắt payload không thông báo. Người dùng có thể thử lại sau; chưa có pagination lịch sử tùy ý trong contract này.

## Failure modes / invariants

| Trường hợp | Hành vi |
|---|---|
| Owner hết hạn/thu hồi hoặc cursor cũ/hỏng/sai scope | API từ chối; không cấp quyền mới hoặc mở scope. 400/401/409 được UI xử lý theo loại. |
| Commit đồng thời với snapshot | Commit không thuộc snapshot có `stream_seq > watermark`; SSE sau cursor trả event đó. |
| Retention xóa prefix hoặc dữ liệu sequence có lỗ | Snapshot có thể phục hồi projection hiện tại; `history_gap=true`; Replay báo vùng không thể dựng lại. Không bịa event/state lịch sử. |
| Retention thay đổi sau khi trả snapshot, trước khi SSE đọc cursor | SSE trả gap; UI thử snapshot hữu hạn rồi hiển thị lỗi nếu lặp lại. |
| Duplicate/out-of-order SSE | Event đã thấy bị bỏ; sequence mới không liền kề kích hoạt snapshot. |
| Payload quá lớn | HTTP413; không cắt im lặng, không cập nhật UI một phần. |
| Request snapshot khi có queue/run | Chỉ đọc; không tăng call/request count, không thay run/checkpoint, không phát event. |

## Nghiệm thu và rollout

PostgreSQL disposable tests bao phủ scope, cursor, concurrent commit, retention gap, bounds, read-only/no-dispatch. Browser regression kiểm tra recovery, Replay gap, duplicate/order và session navigation ở desktop/mobile. Migration không cần thiết: quyết định không thêm bảng/column. Implementation có thể rollout cùng API/UI; khi API cũ chưa có endpoint, browser 404 để offline/error an toàn và không tự dựng state.

Kiểm định độc lập và runtime findings được ghi tại [Stabilization Sprint 03](../reviews/stabilization-03/report.md). Kết quả không thay trạng thái Phase 07/08 hoặc gate IG08.
