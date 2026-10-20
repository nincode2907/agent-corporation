# Deployment verification

## Trước triển khai

- Worktree có nhiều thay đổi staged/unstaged từ các công việc trước; không dọn, checkout hay ghi đè chúng. Cấu hình Compose hợp lệ. Preflight 05.1 ghi nhận API/PostgreSQL/web healthy, chưa có worker, revision `20261014_0009`, Demo Corporation tồn tại với 3 employee, 0 Runtime runs/calls, 0 grant còn hiệu lực và dispatch guard trống.
- `RUNTIME_CG01_DEMO_TEST_OVERRIDE=false`. CG01 release check trả blocked `missing_or_invalid_proof`; không thay đổi policy.
- Bản dump PostgreSQL riêng tư ở `/Users/buivannin/.local/share/agent-corporation/backups/deployment-06-20261020/agent-corporation-postgres.dump` (ngoài repository). Thư mục mode `0700`, dump mode `0600`, dung lượng 135,681 byte, SHA-256 `25c6bcd8a8fd1765282a6ce4ddae99a63574978dff23ff2c15a8cab8188b851d`.
- `pg_restore --list` đọc được 238 mục. Đã restore đầy đủ vào PostgreSQL tạm riêng, xác nhận Demo Corporation/3 employee/0 Run, rồi thử migration `20261020_0010` trên DB đã restore. Kết quả 0009 → 0010 thành công; bảng receipt mới tồn tại. Container, network và volume kiểm định đã được xóa. Bản restore đầu tiên thiếu role app trong môi trường tạm; role đã được tạo trong DB tạm và restore đầy đủ thành công. DB dùng chung không bị ảnh hưởng.
- Đã lưu image cũ để rollback: `agent-corporation-api:deployment06-rollback` (image ID `sha256:4556a4c1bca29f9ca55cd547b8f1dd03ecd50cf0ce116825e3304f28b55dd88a`) và `agent-corporation-web:deployment06-rollback` (`sha256:d436b84e81e14e3f4c7c4167c37a715ec57b48c5d4292640a51edce59723db3a`).

## Triển khai và sau triển khai

- Chạy `docker compose up --build` ở foreground. Giữ terminal runtime hoạt động để thấy log. Bootstrap xác nhận Owner/config hiện có được giữ lại; không ghi credential ra terminal hay báo cáo.
- Cùng PostgreSQL volume được gắn lại; log PostgreSQL xác nhận data directory hiện có được dùng. Migration `20261020_0010` hoàn tất.
- `docker compose ps`: đúng một API, PostgreSQL, web và một Runtime worker trong project `agent-corporation`; API/PostgreSQL/web healthy, worker running (service không khai báo healthcheck riêng).
- API `http://127.0.0.1:15501/api/v1/health/ready`: `{"status":"ok","checks":{"database":"ok"}}`; web `http://127.0.0.1:15500/healthz`: `ok`.
- Revision `20261020_0010`; tổng dữ liệu hiện tại: 1 company, 3 employee, 0 Runtime runs, 0 model calls, 0 grant còn hiệu lực/chưa dùng hết, dispatch guard không giữ, 0 Playground sessions/turns.
- Worker singleton: lock PostgreSQL có đúng một lock giữ; probe phụ trên cùng lock key nhận `false`, xác nhận instance thứ hai không thể giữ lock.
- CG01 vẫn strict; release check vẫn blocked `missing_or_invalid_proof`. Không có yêu cầu đến inference gateway trong các bước triển khai/kiểm định.
- Volume giữ nguyên: `agent-corporation_agent_corporation_postgres`, `agent-corporation_database_secrets`, `agent-corporation_runtime_secrets`, `agent-corporation_artifacts`.

## Rollback đã chuẩn bị

Migration chỉ thêm bảng receipt quyết định với policy RLS, FK và unique idempotency; migration thử trên bản restore đã thành công. Không chạy `alembic downgrade`, vì downgrade sẽ xóa bảng mới. Không phục hồi dump lên DB dùng chung để xử lý lỗi ứng dụng thông thường.

Nếu sau này cần rollback ứng dụng, dùng image tag rollback đã lưu để khôi phục tag local, rồi cập nhật riêng `api`, `web`, `worker` bằng Compose và bỏ qua dependency/migration đã hoàn thành (không chạy lại service `migrate`). Giữ schema 0010 và mọi dữ liệu hiện có. Xác minh readiness/health, worker singleton và CG01 sau rollback. Nếu bản ứng dụng cũ không tương thích với schema 0010, dừng và giữ nguyên DB để điều tra; không downgrade hoặc restore dữ liệu khi chưa đối chiếu toàn bộ ghi phát sinh sau backup và có quyết định riêng của Chủ tịch.

Backup private nêu trên chỉ dành cho phục hồi thảm họa có quyết định riêng. Không chạy `docker compose down --volumes` trên runtime.
