# Bằng chứng triển khai Phase 09 — 09/10/2026

## Phạm vi đã triển khai

- Work Order API dưới Owner session: đọc bảng và assignee trong scope hiện tại, tạo task với Idempotency-Key, kiểm tra assignee/reviewer active hoặc probation.
- Migration `20261009_0007` thêm queue entries và command receipts có composite scope key, foreign key, RLS, index ưu tiên/thời gian sẵn sàng và payload hash cho replay idempotent.
- Queue actions có optimistic `transition_version`: enqueue với priority `-100..100`, pause/resume tại ranh giới queued, hủy chỉ khi draft/queued/paused, Owner acceptance chỉ khi awaiting_acceptance và có linked completed run, rework cần lý do. Event và state/queue receipt được ghi trong cùng transaction.
- Cùng task được serialize trước khi đọc command receipt để concurrent replay cùng Idempotency-Key không cùng vượt qua bước kiểm receipt.
- Web S05 đã nối runtime panel thay cho demo fixture: tạo nháp, lọc/tìm, chọn assignee/reviewer, nhập ưu tiên enqueue, xem queue/state, pause/resume/hủy và yêu cầu nghiệm thu/rework. UI thể hiện rõ model request cap = 0, không có tools/dispatch và dữ liệu chỉ trong Owner scope.
- Work Order input giới hạn reference thành opaque refs, từ chối đường dẫn/traversal, khóa autonomy vào enum đã định nghĩa và khóa inference request ở 0.

## Kiểm tra đã chạy

- `rtk proxy uv run --project apps/api pytest apps/api/tests/test_phase09_work_orders.py` — **12 passed**. Bao gồm contract hợp lệ, blank/invalid fields, reference path/traversal, cấm tool capabilities và request budget, deadline timezone/future, action/version/priority bounds, route từ chối khi thiếu Owner session.
- Regression unit/API an toàn, không ghi DB: `rtk proxy uv run --project apps/api pytest apps/api/tests/test_phase09_work_orders.py apps/api/tests/test_phase06_runtime.py apps/api/tests/test_phase07_feed.py apps/api/tests/test_owner_auth.py apps/api/tests/test_health.py apps/api/tests/test_sensitive_validation.py` — **59 passed**.
- `rtk proxy npm run --prefix apps/web lint` — exit 0.
- `rtk proxy npm run --prefix apps/web build` — exit 0 (TypeScript + Vite production build).
- `rtk proxy python3 -m compileall apps/api/src/agent_corporation_api/modules/work apps/api/migrations/versions/20261009_0007_task_queue.py` — exit 0.
- `rtk proxy uv run --project apps/api alembic -c apps/api/alembic.ini history` — exit 0; revision 0007 nối tiếp 0006 tới head. Đây chỉ xác minh migration graph, không chạy migration lên database.

## Chưa được chứng minh

- Không chạy migration hay test ghi dữ liệu lên PostgreSQL dùng chung. Trong môi trường hiện tại chỉ thấy container DB dự án đang bind `127.0.0.1:15510`; không có disposable database dành cho Phase 09. Vì vậy RLS/rollback/index và migration từ 0006→0007 chưa được kiểm chứng trực tiếp.
- Chưa có worker lease/heartbeat, atomic claim, concurrency cap, crash/expired-lease reconciliation, queue dispatch hoặc liên kết để người dùng tạo Work Order chạy qua runtime. Không tự nối dispatcher vì Phase 08 chưa được nghiệm thu và queue worker có thể mở đường dispatch thực thi.
- Chưa chạy browser demo hai task, chưa thử restart/resume/retry hoặc acceptance/rework end-to-end. Source không tự tạo checkpoint/attempt mới khi resume.
- Chưa có AI kiểm định độc lập. 12 unit checks là kiểm tra code của đợt triển khai, không phải report nghiệm thu Phase 09.
- Không gọi codex-server/inference; không có inference grant.

## Dependency và quyết định trạng thái

Phase 08 vẫn `Bị chặn` theo master-plan; source Owner/session/event của Phase 06–07 hiện diện nhưng chưa có nghiệm thu dependency. Phần Work Order CRUD và queue commands độc lập đã được triển khai. Phase 09 tiếp tục `Đang triển khai`, chưa đủ bằng chứng để chuyển `Chờ nghiệm thu` hoặc `Hoàn tất`. Cần kiểm định độc lập và môi trường PostgreSQL disposable trước khi chạy test tích hợp; lease/worker/concurrency/recovery và demo là phần bắt buộc còn thiếu theo checklist P09-02…P09-05.

## Source

- API: `apps/api/src/agent_corporation_api/modules/work/router.py`, `queue.py`, `commands.py`.
- Migration: `apps/api/migrations/versions/20261009_0007_task_queue.py`.
- UI: `apps/web/src/App.tsx`, `apps/web/src/RuntimePanel.tsx`, `apps/web/src/RuntimePanel.css`.
- Unit checks: `apps/api/tests/test_phase09_work_orders.py`.
