# Remake Phase 16 — 20261015T100829+0700-r001-remake

- Trạng thái xử lý: changed
- Report nguồn: [Phase 16 r001](../../../tests/results/phase-16/20261015T100829+0700-r001-test/report.md)
- Source trước: hash theo manifest report r001.
- Source sau: finance contracts/tests đã sửa; xem git diff và test r002.

## Findings xử lý

- P16-03: `expected_revision` phải là integer thực, không nhận bool; settlement amount phải là integer thực, không để `model_copy` bỏ qua validation; settlement bị giới hạn bởi reservation; dispatched reservation không được release; unresolved cần call ref.
- P16-05: period rỗng trả unknown (`amount_micros=None`) thay vì xác nhận 0.
- C05/P16-06: period và accepted-task aggregates từ chối rows trộn environment/company scope.
- Regression: giữ unknown cost khác 0, currency/basis không gộp, duplicate call bị từ chối.

## Kiểm tra và giới hạn

- Đã thêm fixture boundaries cho findings và sẽ retest riêng ở r002.
- Chưa sửa được trong pure contract: DB atomicity/concurrency, grant-level budget enforcement, pricing persistence, correction report versioning, dashboard, source reconciliation/demo và IG16 run thật. Không gọi DB/runtime/inference; grant = 0.
