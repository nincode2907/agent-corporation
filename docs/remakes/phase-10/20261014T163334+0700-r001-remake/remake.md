# Remake Phase 10 — evaluator binds approval to action and revision

- Vòng: `r001`
- Report nguồn: [Phase 10 r001](../../../tests/results/phase-10/20261014T162815+0700-r001-test/report.md)
- Trạng thái xử lý: `changed`

## Issue đã xử lý

- `P10-01`: evaluator chấp nhận approval/delegation khi `payload_hash` và scope còn khớp nhưng không đối chiếu `action_type` được yêu cầu với `action_type` đã duyệt, cũng không đối chiếu `task_revision` hiện tại với revision đã duyệt. Tester độc lập ghi nhận bypass trước khi sửa; không còn transcript thô của probe ban đầu, vì vậy source manifest r001 là mốc phiên bản và r002 mới là bằng chứng trực tiếp về fix.

## Thay đổi

- `permission.evaluate_action()` hiện nhận `task_revision` tường minh; approval và delegation phải khớp cả `action_type` cùng `task_revision`.
- Bổ sung negative tests cho action type khác và revision cũ ở cả approval lẫn delegation, ngoài các kiểm tra scope/hash/policy/expiry/consume hiện có.
- Không có action được dispatch; đây là evaluator fail-closed và kiểm định unit.

## Bằng chứng thay đổi

- [Source/test snapshot và lệnh kiểm tra](evidence/commands.md)
- Ghi nhận P10-01 và source manifest ban đầu: [report r001](../../../tests/results/phase-10/20261014T162815+0700-r001-test/report.md) và [manifest](../../../tests/results/phase-10/20261014T162815+0700-r001-test/evidence/source-manifest.json). Matrix trong r001 đã được tạo sau bản sửa, nên không dùng làm bằng chứng pre-fix.

## Trạng thái chờ

Chờ AI test độc lập chạy Phase 10 r002 trên source sau remake. Dù r002 xác nhận fix, lifecycle PostgreSQL/API, cross-scope RLS, concurrent consume, executor bypass, Emergency Stop/epoch và audit evidence vẫn cần kết quả riêng; không suy ra từ unit/build/migration.
