# Bằng chứng Phase 01 — Nền phát triển local

Ngày triển khai: 08/10/2026 · Trạng thái: **Hoàn tất — Chủ tịch đã duyệt Phase 01 để sang Phase 02**.

## Dependency và lựa chọn runtime

- Dependency phase: Phase 00 đã Hoàn tất và baseline V1.1 được Chủ tịch nghiệm thu. Phase 01 không dùng domain model/schema của phase tương lai.
- Toolchain đã quan sát: Node.js 24.21.0/npm 11.19.0, Python 3.14.8, `uv`, Docker Compose 2.15.1.
- Web versions khóa trong `apps/web/package-lock.json`: React 19.3.0, Vite 8.3.3, TypeScript 6.0.2.
- API versions khóa trong `apps/api/uv.lock`: FastAPI 0.142.4, Pydantic 2.13.5, Pydantic Settings 2.11.0, SQLAlchemy 2.1.4, Alembic 1.20.0, psycopg 3.3.6, Uvicorn 0.38.0.
- PostgreSQL image `postgres:18.6-alpine`, digest `sha256:77f585114c32fbca283dc835b0596f4e52b51b4c6662d7810b2f4084f60a1873`; đã pull thành công trên Docker Desktop 4.17.0.
- `compose.yml` chỉ chạy PostgreSQL; database được publish trên `127.0.0.1:15510 → 5432`. Gateway codex-server vẫn là process host độc lập tại `127.0.0.1:4000`, không bị đổi cấu hình.
- Dependency check đã GET `http://127.0.0.1:4000/health` và nhận HTTP 200. Không gọi chat/session/model; Phase 01 chưa cần một request inference hay adapter.

## Dev Hub và network scope

- Trước reserve, registry có các block tới `15400–15499`; Dev Hub `discover` lúc `2026-10-08T06:33:32.069Z` và recheck lúc `06:33:56.754Z` báo candidate kế tiếp `[15500, 15599]`, `conflicts: []`, `warnings: []`.
- Discovery đã kiểm listener/Docker publication và TCP cả `127.0.0.1`/`::1`; recheck `lsof -nP -iTCP:15500-15599 -sTCP:LISTEN` không thấy listener trước reserve. Block không chồng lấn registry.
- `npm run allocate` chỉ preview và từ chối vì discovery nhận diện path Git chưa đăng ký cần review identity/service. Đã đối chiếu repo path, mục tiêu phase và 3 service slots trước khi reserve.
- Registry entry `agent-corporation`: web 15500, API 15501, PostgreSQL 15510; block 100 ports. Proxy route `proxy_enabled: false` do Dev Hub Caddy Docker publication là `80:80` wildcard.
- Chỉ dùng URL IPv4 loopback nếu health/browser đã trả đúng; không quảng bá `.localhost` là route hoạt động. PostgreSQL được bind IPv4 loopback để giới hạn quyền truy cập local.

## Secret và migration

- `python3 scripts/bootstrap_local.py` sinh `.env` bằng entropy hệ điều hành; terminal chỉ báo tạo thành công, không in secret. Quan sát file mode `0600`; `git check-ignore .env` xác nhận bị ignore. `.env.example` chỉ có placeholders.
- Alembic baseline `20261008_0001` không tạo domain tables; Phase 03 sở hữu schema task/state/event. Lịch sử migration đã apply vào PostgreSQL local.
- API hiện chỉ expose liveness và readiness. Liveness không phụ thuộc database; readiness chạy `SELECT 1`, trả 503 với thông báo đã lọc khi database down.

## Lệnh và kết quả

```text
python3 scripts/bootstrap_local.py                         PASS — tạo .env local mode 0600; secret không hiển thị
docker compose up -d postgres                             PASS — PostgreSQL healthy; 127.0.0.1:15510->5432
uv sync --project apps/api --locked                       PASS — cài từ lock, Python 3.14.8
uv run --project apps/api pytest apps/api/tests -q        PASS — 3 health tests, 3 passed
npm ci --prefix apps/web                                  PASS — cài từ lock, npm audit 0 vulnerabilities
npm run --prefix apps/web build                           PASS — tsc + Vite production build
npm run --prefix apps/web lint                            PASS — 0 finding
uv run --project apps/api alembic -c apps/api/alembic.ini upgrade head  PASS — applied 20261008_0001
uv run --project apps/api alembic -c apps/api/alembic.ini current       PASS — 20261008_0001 (head)
python3 scripts/validate_phase00.py                       PASS — docs/references/examples/3 HTML đồng bộ và syntax
```

Lần migration đầu chưa nạp `apps/api/src` vào `sys.path` vì prepend path tương đối theo working directory; đổi thành `%(here)s/src`, chạy lại trên PostgreSQL thật và migration thành công.

HTTP thực tế: web `127.0.0.1:15500/` HTTP 200, favicon HTTP 200, frontend proxy `/api/v1/health/ready` HTTP 200; API liveness/readiness trực tiếp HTTP 200, ready trả `database: ok`. Kiểm tra IPv6 `::1:15500` và `::1:15501` không có listener (URLError); runtime chủ ý chỉ bind IPv4 loopback, nên chỉ công bố URL `127.0.0.1`. Browser Chrome mở trang tại `http://127.0.0.1:15500/`, đọc được ba dịch vụ hoạt động và không có console error. Proxy `.localhost` không được bật/claim.

Kiểm chứng database-down theo demo: `docker compose stop postgres` → readiness HTTP 503 `{"status":"degraded","checks":{"database":"unavailable"}}`; liveness vẫn HTTP 200; UI báo không kết nối PostgreSQL. `docker compose start postgres` → container healthy, readiness HTTP 200 trở lại. Database hiện được giữ chạy.

Startup log: Uvicorn `Started server process`, `Application startup complete`, `Uvicorn running on http://127.0.0.1:15501`; Vite `v8.3.3 ready`, `http://127.0.0.1:15500/`. Hai server giữ trong PTY tương tác để theo dõi log.

`npm ci` phát cảnh báo npm 11 yêu cầu review install script tùy chọn của `fsevents`; clean install, typecheck/build và lint đều thành công. Không có dependency audit finding.

## Files bàn giao

- `apps/web/`: Vite/React/TypeScript health page tiếng Việt, lang `vi`, favicon, responsive và same-origin `/api` proxy.
- `apps/api/`: FastAPI/Pydantic settings, SQLAlchemy connectivity probe, health routes, Alembic baseline và tests.
- `compose.yml`, `.env.example`, `.gitignore`, `.nvmrc`, `.python-version`, `scripts/bootstrap_local.py`.
- `README.md`, `AGENTS.md`, Dev Hub `projects.yml`, `docs/master-plan.md` và bản HTML sinh từ đó.

## Giới hạn bàn giao

Phase 01 chưa tạo bảng domain, công ty/fixture, Owner auth endpoint, worker/scheduler, inference adapter hoặc agent runtime. Secret Owner/session chỉ được tạo cục bộ để không commit credential mẫu; hiện chưa được dùng bởi API. Proxy `.localhost` vẫn tắt. Inference grant = 0; không có request model nào.
