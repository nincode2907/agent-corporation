# Khởi động Agent Corporation trên Windows và macOS

## Yêu cầu

Cài và mở Docker Desktop, chờ Docker báo đang chạy. Không cần cài Python, `uv` hoặc Node.js trên máy.

## Khởi động lần đầu

Mở terminal tại thư mục dự án rồi chạy các bước setup riêng:

**Windows PowerShell**

```powershell
rtk proxy docker compose --profile setup run --build --rm --no-deps bootstrap
rtk proxy docker compose up -d --wait postgres
rtk proxy docker compose --profile setup run --build --rm --no-deps migrate
rtk proxy docker compose up --build -d api web
```

**macOS Terminal**

```sh
rtk proxy docker compose --profile setup run --build --rm --no-deps bootstrap
rtk proxy docker compose up -d --wait postgres
rtk proxy docker compose --profile setup run --build --rm --no-deps migrate
rtk proxy docker compose up --build -d api web
```

Bootstrap tạo config/Owner một lần, PostgreSQL mở volume hiện có hoặc tạo volume mới, rồi migration được gọi riêng trước API/web. API không tự migrate hoặc bootstrap khi khởi động. Thiếu hay lệch schema làm readiness báo lỗi rõ ràng. Để các dịch vụ tiếp tục chạy, dùng `rtk proxy docker compose up -d api web`.

## Mở ứng dụng

Truy cập <http://127.0.0.1:15500>.

## Dừng và khởi động lại

Nhấn `Ctrl+C` trong terminal để dừng. Lần sau, mở Docker Desktop rồi chạy tại thư mục dự án:

```sh
rtk proxy docker compose up -d api web
```

Lệnh `docker compose down` dừng các container. Không dùng `docker compose down -v` nếu muốn giữ dữ liệu local.
