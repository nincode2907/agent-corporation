# Kiểm chứng cô lập Phase 01 — remake r004

Không dùng volume hoặc DB project; credentials là fixture giả, không đọc `.env`. PostgreSQL 18.6 Alpine chạy bằng container `--rm`, image digest khớp Compose, bind Docker cấp ngẫu nhiên trên IPv4 loopback `127.0.0.1:61530`. Source API/web được copy vào `/tmp/ac-p01-r004-copy`; không sửa source của repo ngoài README. Inference = 0.

## Migration baseline (P01-03)

- `uv sync --project /tmp/ac-p01-r004-copy/apps/api --locked` — exit 0.
- Alembic `upgrade 20261008_0001` — lần đầu tạo baseline, exit 0.
- Lặp lại cùng lệnh — exit 0, không áp migration trùng.
- Alembic `current` — `20261008_0001`.
- `psql -c '\dt public.*'` — schema public chỉ có `alembic_version`.

## Health khi DB dừng (P01-02)

- API copy dùng port được OS cấp `127.0.0.1:64268`, trỏ vào DB container riêng.
- Khi DB sẵn: GET `/api/v1/health/live` = 200; `/api/v1/health/ready` = 200, database `ok`.
- Dừng đúng container test `ac-p01-r004-pg`, không tác động PostgreSQL project.
- Khi DB dừng: liveness = 200; readiness = 503 với `{"status":"degraded","checks":{"database":"unavailable"}}`; không lộ connection exception.
- Web copy dùng port OS cấp `127.0.0.1:50658`; Vite proxy tới API copy.
- Browser CUA tại `http://127.0.0.1:50658/#settings` hiển thị: “API nội bộ … Đang hoạt động”, “PostgreSQL … Chưa kết nối”, “API có phản hồi nhưng readiness chưa đạt.” Không bấm probe gateway, không submit POST.
- Vite proxy `/api/v1/health/live` = 200 và `/api/v1/health/ready` = 503.

Sau kiểm tra, gửi Ctrl-C đúng hai tiến trình test, container `--rm` tự xóa, xoá temp copy. Lsof xác nhận chỉ các listener dự án sẵn có còn trên `15500–15510`.
