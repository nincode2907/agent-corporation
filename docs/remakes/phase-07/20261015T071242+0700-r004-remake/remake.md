# Remake Phase 07 — 20261015T071242+0700-r004-remake

- Phase: 07; Vòng: r004; AI remake: `/root`.
- Bắt đầu: 2026-10-15T07:12:42+07:00, Asia/Saigon.
- Report nguồn: [r004](../../../tests/results/phase-07/20261014T161904+0700-r004-test/report.md).
- Phạm vi: sửa hai lỗi reconnect P07-02/P07-03 được r004 tái hiện; không gọi inference, không thay CG01 hoặc đổi trạng thái phase.

## Thay đổi

- P07-02: `Last-Event-ID` được ưu tiên hơn query cursor cũ. EventSource giữ URL ban đầu khi tự reconnect nhưng gửi ID tiến lên ở header; cả hai cursor vẫn được xác minh bằng luồng feed có chữ ký/scope hiện có.
- P07-03: khi SSE báo lỗi, UI kiểm tra read-only event page bằng cursor hiện tại. HTTP 400/409/410/422 hoặc sequence cache vượt event store đóng stream, đánh dấu `gap` và hướng dẫn tải lại; lỗi mạng/5xx tạm thời giữ trạng thái reconnecting để EventSource thử lại.
- Thêm regression test route kiểm tra cursor header được chọn khi reconnect và cursor query được dùng cho kết nối đầu.

## Kiểm tra trước retest độc lập

- `pytest apps/api/tests/test_phase07_feed.py -q`: 5 passed.
- `npm run --prefix apps/web lint`: exit 0.
- `npm run --prefix apps/web build`: exit 0.
- `uv run --project apps/api python -X utf8 scripts/test_playground_isolated.py`: 143 passed, 11 skipped; disposable DB/role đã được dọn.
- `git diff --check` các file liên quan: exit 0.
- Browser Work: sáu task và phần chi tiết render; không còn lỗi `TaskCard.join` với fixture đang thiếu `input_refs`. Browser QA chưa mô phỏng network drop/real reconnect.

## Giới hạn và bàn giao

- Không dùng shared runtime DB, không tạo inference grant và không gọi model.
- P07-01, P07-04–P07-07 và các blocker dependency/run thật chưa được đóng bởi remake này.
- Chờ AI test độc lập retest P07-02/P07-03 và regression liên quan. Không đánh dấu Phase 07 hoàn tất.

