# Bằng chứng Phase 06 — triển khai lại ngày 09/10/2026

## Phạm vi và quyền

Theo chỉ thị “fix bị chặn, thực hiện lại phase 6, 7”, đã triển khai các prerequisite Owner auth/profile và code Phase 06–07. Không tự nghiệm thu các dependency hoặc phase. Không triển khai Phase 08, không tạo công ty thật, không gọi inference và không chỉnh/restart shared gateway hoặc DB/runtime đang dùng.

## Phần đã có trong source

Owner session bền vững/CSRF/Host/Origin, profile có version; runtime PG grant/reservation, một call toàn app, text-only một turn, checkpoint/correlation/artifact, stop/unknown và late usage correction bất biến.

- Migration 0004 Owner scopes/sessions/profile; 0005 runtime/grants/calls/global guard; 0006 late usage corrections. App role không bypass RLS; transaction scope backend từ session.
- Default grant thật 0, CG01 proof thiếu/hết hạn/sai fingerprint/endpoint/symlink/FIFO/JSON lỗi đều deny. HTTP input không có cờ bypass gate; grant cần Owner và CSRF, gắn phase/batch/purpose/model/effort/limits/expiry.
- Gateway default hiện 15600 theo registry/src/config.ts và listener/GET health/models thật ngày 09/10. Cổng 4000 là cấu hình khảo sát cũ. Chỉ đổi client app; catalog không chứng minh entitlement.
- 429 requeue theo grant, backoff 1/3s và attempt count bounded. Không fallback tự động. Timeout/disconnect/unknown/recovery giữ fence, không phát lại POST.
- Completed run đưa task sang reviewing, không accepted. Thiếu usage giữ unresolved; correction không sửa outcome gốc, không giảm requests đã tiêu, không gia hạn/tái cấp grant. Không endpoint nhập usage tùy ý.
- API error validation không echo input/secret; lỗi SQLAlchemy được xử lý bằng503 chung và worker CLI dừng bằng thông báo không chứa SQL parameters. SSE chỉ metadata, không raw prompt/output/history/host path. Cursor bảo vệ signature+session+scope+expiry; heartbeat SSE chỉ báo kết nối.
- UI tiếng Việt ở Quản trị/Văn phòng: đăng nhập/profile, gate/grant, text-only run/stop, event list, heartbeat worker riêng, cache local có nhãn chưa đối chiếu. Mở trang không dispatch model.

## Kiểm thử và vòng sửa

- [AI test r002](../tests/results/phase-06/20261009T121142+0700-r002-test/report.md) đã phát hiện lỗi readonly GET/counter FK, malformed proof, missing usage reservation và task lifecycle.
- [Remake r002](../remakes/phase-06/20261009T145834+0700-r002-remake/remake.md) lưu thay đổi/source hashes và mọi finding của report nguồn.
- [Retest độc lập r003](../tests/results/phase-06/20261009T145600+0700-r003-test/report.md): API 73/73 pass trên PostgreSQL disposable head 0006; 5 kiểm tra độc lập actual Owner/auth/CSRF/CAS, usage-unresolved, proof deny, HTTP/SSE reconnect/logout và SIGKILL worker riêng đều pass. Không dùng mock để PASS run model thật.
- Bổ sung cuối: [xử lý lỗi DB](../remakes/phase-06/20261009T145834+0700-r002-remake/evidence/privacy-error-addendum.md), 34 focused unit tests đạt; AI độc lập kiểm tra source cuối riêng, không coi đây là chạy lại PostgreSQL suite.
- Report r003 đã chốt: 10 ca clean/pass, 6 ca need-change/blocked, không có ca fail. Sau bổ sung xử lý lỗi DB, AI độc lập chạy lại 53/53 unit tests đạt; không chạy lại PostgreSQL suite đã cleanup.
- Web lint/build đạt. Framework issue lifecycle14 tests đạt, gồm sort theo vòng khi thời gian chuẩn bị batch chồng nhau.
- Browser preview riêng: login/profile/reload/committed events, mobile 390px, stale worker dù SSE vẫn kết nối và ngắt preview không còn báo worker active. Đây là môi trường QA có nhãn, không là demo inference thật.

## Gate còn mở

CG01 của gateway shared vẫn thiếu proof isolation/read boundary/privacy-retention/cancellation phù hợp; không tạo proof đạt giả. Inference grant thật hiện 0. Các case cần request model/provider cancellation/run thật→UI chưa chạy; grant phải cấp mới theo đúng batch/mục đích/hạn mức/expiry. Nghiệm thu dependency và phase do Chủ tịch quyết định.

Code và các bản remake không đánh dấu Hoàn tất. Xem [sổ vòng](../tests/results/phase-06/README.md) và [master plan](../master-plan.html).
