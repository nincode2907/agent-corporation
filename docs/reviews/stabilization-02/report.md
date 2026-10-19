# Agent Corporation — Stabilization Sprint 02

**Mục tiêu:** đóng evidence cho Phase 07/08 bằng kiểm định không inference; sửa harness/evidence nếu cần; tổng hợp UI và chuẩn bị đề xuất IG08 để Chủ tịch quyết định sau.  
**Kết luận:** chưa đủ bằng chứng để nghiệm thu Phase 07/08. Không thay đổi mã sản phẩm trong Sprint 02; bổ sung test hồi quy và công cụ/evidence. Phase status giữ nguyên. Không chạy inference, tạo grant, dispatch worker, gọi gateway, thay CG01 hay mở Phase 11.

## VERIFIED PASS

- Isolated API suite: **145 passed, 11 skipped, 1 warning**, exit 0. Lệnh: `rtk proxy uv run --project apps/api python -X utf8 scripts/test_playground_isolated.py`. Runner dùng PostgreSQL/database-role tạm và dọn sau khi chạy. Warning là deprecation của `httpx` qua Starlette TestClient; xem batch commands.
- Bổ sung kiểm định Phase 07 cho event đã commit: so sánh `event_id` và `stream_seq` trong PostgreSQL với SSE `id`/payload; event bị rollback không còn trong DB, API page hoặc SSE. GET event feed qua Owner test principal không đọc event thuộc company scope thứ hai.
- Cursor ký hợp lệ được chấp nhận; cursor bị sửa, hết hạn, khác scope bị từ chối HTTP 400. Cursor vượt retention và thiếu cursor trả HTTP 409. API không cung cấp snapshot recovery.
- Browser Owner-authenticated: 9 màn hình × desktop 1440×900 và mobile 390×844 (18 ảnh), cộng 3 ảnh state (gap, offline, stale). Không page error. Replay filter/seek/reload quan sát được 2 event reads, slider và reload recovery. Hành trình không tạo grant/run/message/approval/profile change.
- Browser kiểm tra state: gap UI hiện “Kết nối event store: Có khoảng trống dữ liệu”, reload sau bỏ lỗi phục hồi kết nối; offline hiện “Mất kết nối” rồi hồi phục sau online + reload; stream stalled quá 31 giây hiện “Dữ liệu đã cũ” rồi hồi phục khi stream được khôi phục.
- Replay DB snapshot trước/sau có **13 bảng** metadata-only; khác biệt số hàng/fingerprint: **không có**. Snapshot chạy read-only. Request log toàn phiên chỉ có POST Owner login/logout; replay flow không có business writes. Có 2 lần đọc event.
- UI evidence được đóng gói tại [authenticated-ui-review.zip](../stabilization-02/evidence/authenticated-ui-review.zip), contact sheet [contact-sheet.html](../stabilization-02/evidence/authenticated-fresh/contact-sheet.html), inventory [inventory.md](../stabilization-02/evidence/authenticated-fresh/inventory.md), manifest [manifest.json](../stabilization-02/evidence/authenticated-fresh/manifest.json). Ảnh làm mờ nội dung Playground lịch sử và opaque IDs.

## REPRODUCED AND FIXED

- Không phát hiện lỗi sản phẩm cần sửa trong phạm vi kiểm định này; không có thay đổi runtime/UI sản phẩm trong Sprint 02.
- Sửa test harness/evidence: fixture event dùng source hợp lệ; bộ phân tích frame SSE nhận diện frame `event: domain`; cleanup route/offline state được khôi phục; package generator đọc được cả flow có metadata thay vì chỉ flow có `actions`; manifest replay ghi `businessWrites: []` (POST login/logout được báo riêng ở cấp phiên). Những lần chạy harness lỗi trước khi sửa không được tính là pass và không thay đổi dữ liệu runtime.

## STILL BLOCKED

- **Phase 07:** retention gap hiện trả HTTP 409 nhưng không có endpoint/contract snapshot để UI lấy snapshot + cursor mới. UI hiển thị gap và reload phục hồi khi lỗi tạm được bỏ, nhưng không thể chứng minh recovery cho gap retention thật. Cần quyết định contract snapshot trước khi sửa.
- Không có kiểm tra fake gateway session hết hạn/thu hồi trong test scope mới; recovery của context gateway hết hạn vẫn mở.
- Không có authorized live run, grant hoặc model call; run thật tới Office/Inspector/UI và IG08 đều blocked. Không tự cấp grant.
- **Phase 08:** isolation API được kiểm tra với dữ liệu tổng hợp ở database tạm, nhưng không có browser Inspector/artifact retrieval negative test cho actor thứ hai. Chưa có active run chung để chứng minh Office→Inspector→Replay end-to-end.
- Kết quả các batch mới: Phase 07 r007 **10 clean / 5 blocked / 0 fail**; Phase 08 r006 **8 clean / 7 blocked / 0 fail**. Đây là kết quả kỹ thuật từng case, không phải quyết định nghiệm thu phase.

## NOT TESTED

- Inference, worker dispatch, model entitlement, usage/price, gateway cancellation semantics, grant/CG01 behavior, concurrent live run, active-state `idle`/`waiting_model` trên cùng run.
- Approval decision, sửa hồ sơ, employee detail (không có luồng detail trong UI được rà), replay artifact fetch endpoint độc lập; không có mutation thao tác nào được thực hiện.
- Gemini consultation: **không thực hiện**; không có reviewer Gemini khả dụng. Package giữ sẵn để gửi review sau nếu cần.
- Không chạy lại UI build/Playwright suite tổng thể vì Sprint 02 không sửa source sản phẩm; các chỉ số build/browser trước đó được dẫn chiếu ở r006/r005. Browser audit mới chạy riêng cho journeys/state đã nêu.

## REQUIRES OWNER DECISION

IG08 chỉ có thể mở sau quyết định của Chủ tịch về một test grant riêng: chọn profile/model cụ thể; chốt scope demo cô lập; ghi rõ phase, batch, mục đích, **1 request, concurrency 1, tối đa 120 giây**, expiry cụ thể; chốt CG01 ở chế độ strict hay ngoại lệ demo đang được phép. Đề xuất chưa cấp grant và chưa chạy. Xem [IG08 live-test proposal](ig08-live-test-proposal.md).

## Thay đổi và evidence

- Test mới: `apps/api/tests/test_stabilization02_observability.py`.
- Evidence runner và ảnh: `docs/reviews/stabilization-02/evidence/`.
- Batches: [Phase 07 r007](../../tests/results/phase-07/20261018T232151+0700-r007-test/report.md), [Phase 08 r006](../../tests/results/phase-08/20261018T232151+0700-r006-test/report.md).
- UI findings: [ui-review.md](ui-review.md). Kế hoạch tiếp theo: [next-actions.md](next-actions.md).

## Giới hạn báo cáo

Số 145/11/1 là lần isolated suite hoàn tất thành công. Các lần harness/browser lỗi trước khi hoàn thiện được ghi trong command evidence để không nhầm thành kết quả pass. Snapshot DB loại bỏ session table vì chính login/logout tạo/revoke session. Test feed/assertion dùng fixtures tổng hợp và không chứng minh quyền truy cập production. Không có phase nào được AI nghiệm thu.
