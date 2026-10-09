# Quan sát UI thực trên preview cô lập

Bước CUA: mở new QA tab ở own preview64520/#settings; nhập fake canary Owner secret, login; profile fixture-model savev1; reload xác minh profilev1/cachedmetadata được gắn nhãn; SSE lại kết nối. Không bấm probe gateway, không tạo grant hay submit model qua UI.

Fullsuite Phase04 đồng thời reset fixed demo dataset trong cùng QA DB (không sharedDB). Browser cursor21 vượt latest20 hiển thị Có khoảng trống dữ liệu; bấm Tải lại từ dữ liệu đã lưu lấy20events từ committed store, trở về Đã kết nối. Đây là gap recovery thực, không lỗi source.

Sau fullsuite, tạo fake durable run trạng thái waiting_model bằng service và reservation trong ownDB nhưng không gọi transport. Heartbeat riêng được đặt30s cũ: UI tự refresh run từ event, hiện Worker mất heartbeat/dữ liệu đã cũ và cảnh báo trạng thái lưu không chứng minh hoạt động; SSE vẫn live. Screenshot P07-04-worker-stale.png. Own preview bị dừng: Kết nối event store Đang kết nối lại; run Không đối chiếu được worker/dữ liệu có thể đã cũ. Screenshot P07-04-disconnected.png.

Mobile390x844: scrollWidth375<=viewport390, label/focus/form controls trong flow dùng được, run disabled thiếu CG01/grant. Screenshot P07-04-mobile-390.png. Restore viewport và close only QA-created tab. Keyboard heading press attempt không focus được (h3 không interactive), không dùng làm bằng chứng accessibilityfail; thao tác native AX/controls vẫn đúng.

Ảnh và run fixture không chứng minh model/gateway live hoặc Phase08 replay.
