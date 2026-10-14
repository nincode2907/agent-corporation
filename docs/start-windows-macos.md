# Khởi động Agent Corporation trên Windows và macOS

## Yêu cầu

Cài và mở Docker Desktop, chờ Docker báo đang chạy. Không cần cài Python, `uv` hoặc Node.js trên máy.

## Khởi động lần đầu

Mở terminal tại thư mục dự án. Tạo file `.env` local một lần bằng Python chạy trong Docker:

**Windows PowerShell**

```powershell
docker run --rm -v "${PWD}:/workspace" -w /workspace python:3.12-slim python scripts/bootstrap_local.py
docker compose up --build -d
docker compose exec api uv run --project apps/api alembic -c apps/api/alembic.ini upgrade head
docker compose up
```

**macOS Terminal**

```sh
docker run --rm -v "$PWD:/workspace" -w /workspace python:3.12-slim python scripts/bootstrap_local.py
docker compose up --build -d
docker compose exec api uv run --project apps/api alembic -c apps/api/alembic.ini upgrade head
docker compose up
```

Lần đầu Docker tải image và build các dịch vụ nên sẽ mất thêm thời gian. Để các dịch vụ tiếp tục chạy, giữ terminal mở.

## Mở ứng dụng

Truy cập <http://127.0.0.1:15500>.

## Dừng và khởi động lại

Nhấn `Ctrl+C` trong terminal để dừng. Lần sau, mở Docker Desktop rồi chạy tại thư mục dự án:

```sh
docker compose up
```

Lệnh `docker compose down` dừng các container. Không dùng `docker compose down -v` nếu muốn giữ dữ liệu local.
