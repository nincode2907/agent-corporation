# Đối chiếu source Phase 01 — r004

- `apps/api/src/agent_corporation_api/main.py`: startup chỉ dựng FastAPI/router; `/health/live` không chạm DB; `/health/ready` chỉ gọi connectivity probe và lọc lỗi SQLAlchemy.
- `apps/api/tests/test_health.py`: ba test dùng ASGI transport; readiness fail được mô phỏng bằng monkeypatch `OperationalError`, không kết nối DB thật.
- `apps/web/src/App.tsx`: khi mở trang gọi health liveness/readiness và `GET /api/v1/demo/dashboard`; gateway probe chỉ chạy từ nút bấm; reset fixture chỉ qua thao tác xác nhận và `POST /api/v1/demo/reset`.
- `apps/api/src/agent_corporation_api/modules/demo/router.py`: dashboard gọi `read_demo_dashboard`, còn reset là route POST tách biệt; không có seed trong GET route.
- `apps/api/src/agent_corporation_api/modules/codex_gateway/adapter.py`: probe là GET `/health` + `/v1/models`; không dispatch chat/session. Không chạy probe trong batch này.
- `apps/web/index.html`: `lang="vi"`; favicon tồn tại và trả HTTP 200.
- `README.md` dòng lệnh cài frontend dùng `npm ci --prefix apps/web` từ root. Bản sao sạch tái hiện fail; `npm ci` từ thư mục `apps/web` thành công. Chi tiết [finding P01-01](finding-p01-01.md).
- Compose/Vite/README/listener khớp block trong Dev Hub registry: web 15500, API 15501, PostgreSQL 15510; listener chỉ `127.0.0.1` IPv4. Registry ghi hostname app `proxy_enabled: true`, API hostname false.

Không phát hiện Phase 01 product source thay đổi so với manifest r002; hash các file runtime, lockfile, README và checklist trùng. `docs/master-plan.md` đã thay đổi sau r002 để ghi lịch sử/pipeline chờ review độc lập. Hash chi tiết nằm trong [source manifest](source-manifest.json); `.env` không được đọc hoặc hash.
