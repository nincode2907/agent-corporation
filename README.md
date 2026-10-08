# Agent Corporation

Nền tảng local-first để Chủ tịch giao mục tiêu, kiểm soát quyền và nghiệm thu bằng chứng. Phase 00–03 đã hoàn tất; Phase 04 chờ nghiệm thu. Chưa có runtime agent hoặc inference.

- [Mở trang theo dõi phase](docs/master-plan.html)
- [Kế hoạch và nguồn trạng thái chính thức](docs/master-plan.md)
- [Đặc tả V1](docs/product-spec.html)
- [Quyết định nền V1](docs/decisions/0001-v1-foundation.html)
- [Bằng chứng Phase 00](docs/evidence/phase-00.md)
- [Bằng chứng Phase 01](docs/evidence/phase-01.md)
- [Bằng chứng Phase 02](docs/evidence/phase-02.md)
- [Bằng chứng Phase 03](docs/evidence/phase-03.md)
- [Bằng chứng Phase 04](docs/evidence/phase-04.md)
- [Hướng dẫn cho agent](AGENTS.md)
- [Bộ rule và checklist kiểm định từng phase](docs/tests/README.md) · [Bản trực quan](docs/tests/index.html)

## Khởi động local

Prerequisites đã kiểm chứng trên máy phát triển: Node.js 24, Python 3.14, `uv` và Docker Compose v2. Xem các version pin trong `.nvmrc`, `.python-version`, `apps/web/package-lock.json`, `apps/api/uv.lock` và `compose.yml`.

Từ root repo, tạo secret riêng local, dựng PostgreSQL và cài dependency:

```sh
python3 scripts/bootstrap_local.py
docker compose up -d postgres
uv sync --project apps/api --locked
npm ci --prefix apps/web
uv run --project apps/api alembic -c apps/api/alembic.ini upgrade head
```

Chạy API và web trong hai terminal nhìn thấy log:

```sh
uv run --project apps/api uvicorn agent_corporation_api.main:app --app-dir apps/api/src --host 127.0.0.1 --port 15501
npm run --prefix apps/web dev
```

Mở `http://agent-corporation.localhost` (hoặc `http://127.0.0.1:15500`). Vite forward `/api` tới API loopback. Kiểm tra readiness trực tiếp bằng `curl -i http://127.0.0.1:15501/api/v1/health/ready`. Dừng PostgreSQL bằng `docker compose stop postgres`; lệnh này giữ nguyên dữ liệu local. Chạy lại bằng `docker compose start postgres`.

Block `15500–15599` đã được reserve tại Dev Hub; mapping cụ thể ở registry trung tâm. Hostname `agent-corporation.localhost` dùng proxy Dev Hub chỉ publish trên IPv4/IPv6 loopback.

`.env` được bootstrap ngẫu nhiên, quyền `0600` và bị Git ignore. Không commit/copy secret; `.env.example` chỉ chứa chỉ dẫn placeholder. Health routes không thực hiện authentication, nên API chỉ bind loopback và chỉ có liveness/readiness trong phase này.

## Kiểm tra và tài liệu

```sh
uv run --project apps/api pytest apps/api/tests
uv run --project apps/api alembic -c apps/api/alembic.ini current
npm run --prefix apps/web build
rtk proxy python3 scripts/render_plan.py
rtk proxy python3 scripts/validate_phase00.py
```

Các lệnh tài liệu chỉ xử lý file local, không gọi model. Inference grant hiện là 0; Phase 03 không gọi inference. Mỗi phase sau cần được giao riêng.
