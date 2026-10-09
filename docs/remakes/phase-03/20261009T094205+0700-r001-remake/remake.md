# Remake Phase 03 — 20261009T094205+0700-r001-remake

## Thông tin vòng sửa

- Phase: 03 — Dữ liệu và bằng chứng bền vững
- Vòng: r001 (report nguồn legacy)
- Report nguồn: [kiểm định Phase 03 legacy](../../../tests/results/phase-03/20261008T161241+0700-phase-03/report.md)
- Người/AI remake: Codex implementer trong phiên Chủ tịch giao remake
- Thời gian: 2026-10-09 +07:00
- Phạm vi/quyền: chỉ Phase 03; test dùng UUID fixture theo test hiện hữu; không restart DB/API dùng chung; không gọi inference.
- Source trước/sau: dirty worktree; xem [manifest](evidence/source-manifest.json).
- Inference: không gọi; grant = 0.
- Kết luận vòng sửa: đã bổ sung kiểm thử negative/race/redaction; clean migration/restart còn cần kiểm chứng độc lập trên môi trường cô lập.

## Mapping results → thay đổi

| Test ID / kết quả nguồn | Nguyên nhân | Thay đổi thực tế | Trạng thái xử lý | Retest |
| --- | --- | --- | --- | --- |
| C02 — need-change / mismatch | Dòng hướng dẫn trạng thái phase đã cũ. | Đồng bộ `AGENTS.md` với nguồn trạng thái Markdown. | changed | C02 và kiểm tra HTML/source status |
| P03-01 — blocked | Chưa chạy negative composite FK insert. | Thêm test revision có company khác với task; kỳ vọng DB từ chối và transaction rollback. | changed | Chạy integration test trên PostgreSQL và xem evidence |
| P03-02 — blocked | Report chưa có clean DB migration/restart evidence. | Chưa đổi migration; yêu cầu AI test chạy clean upgrade/restart trên PostgreSQL cô lập. | blocked | Alembic upgrade từ DB rỗng tới head; kiểm tra current và dữ liệu sau restart cô lập |
| P03-03 — blocked | Chỉ so state/version, không snapshot revision/event/outbox. | Snapshot toàn history trước negative/stale transitions và so sánh nguyên trạng sau đó. | changed | Chạy negative/stale transition test |
| P03-04 — blocked | Rollback assertion chưa kiểm tra trực tiếp revision/event/outbox. | Bổ sung truy vấn xác nhận không còn các row cùng task/event sau rollback. | changed | Chạy fault-injection test trong transaction fixture |
| P03-05 — blocked | Thiếu-scope write/read và pooled-connection leakage chưa test. | Thêm thiếu scope, write denial, transaction-local scope và connection reuse assertions. | changed | Chạy RLS/pool isolation test trên app role |
| P03-06 — blocked | Chưa có writers đồng thời và event envelope completeness. | Thêm 6 concurrent create calls, kiểm sequence liên tục, event metadata và dedup keys. | changed | Chạy concurrency test lặp trong PostgreSQL |
| P03-07 — blocked | Canary chưa được dò outbox/log sink. | Query outbox + `caplog` để bảo đảm password/key/Bearer canary không xuất hiện. | changed | Chạy redaction canary test, xem dữ liệu đã lọc |
| P03-08 — blocked | Chưa kiểm run/checkpoint/event sau restart backend. | Không restart DB/API dùng chung; chờ AI độc lập kiểm chứng bằng stack disposable. | blocked | Khởi tạo run/checkpoint/event trong scope fixture, restart process backend cô lập và đọc lại |
| P03-09 — blocked | IG03 phụ thuộc restart persistence còn thiếu. | Gate giữ BLOCKED; không đổi tiêu chí hoặc dùng inference/mock. | blocked | Chỉ retest IG03 sau P03-02/P03-08 có evidence thật |

## Chi tiết và kiểm tra

- Thay đổi duy nhất trong code là bổ sung coverage vào `apps/api/tests/test_phase03_persistence.py`; không thay schema, migration, API contract, kiến trúc hay authority.
- Target test chạy: `rtk proxy uv run --project apps/api pytest apps/api/tests/test_phase03_persistence.py -q` — exit 0, **8 passed in 1.59s** trên PostgreSQL local hiện hữu. Dữ liệu fixture thuộc các UUID mới do fixture tạo và dọn; không dừng/restart shared services.
- Lệnh/source hashes: [commands](evidence/commands.md), [manifest](evidence/source-manifest.json).
- P03-02/P03-08 và IG03 chưa đạt/đóng; phải được AI test khác đánh giá trong môi trường cô lập trước nghiệm thu.

## Cleanup và bước tiếp theo

- Cleanup: pytest fixture xóa các rows của hai environment UUID vừa tạo; test không ghi ngoài phạm vi đó.
- Retest tiếp theo: AI độc lập chạy r002; cần bổ sung evidence clean migration/restart, restart backend persistence và IG03.
- Trạng thái phase: Chờ nghiệm thu; chưa được đánh dấu Hoàn tất.
- Sổ vòng: [Phase 03](../../../tests/results/phase-03/README.md).
