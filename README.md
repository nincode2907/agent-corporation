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
npm --prefix apps/web ci
uv run --project apps/api alembic -c apps/api/alembic.ini upgrade head
```

Chạy API và web trong hai terminal nhìn thấy log:

```sh
uv run --project apps/api uvicorn agent_corporation_api.main:app --app-dir apps/api/src --host 127.0.0.1 --port 15501
npm run --prefix apps/web dev
```

Mở `http://agent-corporation.localhost` (hoặc `http://127.0.0.1:15500`). Vite forward `/api` tới API loopback. Kiểm tra readiness trực tiếp bằng `curl -i http://127.0.0.1:15501/api/v1/health/ready`. Dừng PostgreSQL bằng `docker compose stop postgres`; lệnh này giữ nguyên dữ liệu local. Chạy lại bằng `docker compose start postgres`.

Block `15500–15599` đã được reserve tại Dev Hub; mapping cụ thể ở registry trung tâm. Hostname `agent-corporation.localhost` dùng proxy Dev Hub chỉ publish trên IPv4 loopback; môi trường hiện tại không bind IPv6 loopback.

Phase 05 probe Codex server thủ công từ backend bằng `GET /health` và `GET /v1/models`. Mặc định gateway là `http://127.0.0.1:15600`, đã đối chiếu registry/source và GET ngày 09/10/2026 (endpoint khảo sát cũ là4000). Nếu cần cấu hình Bearer, chỉ lưu `CODEX_SERVER_API_KEY` trong `.env` mode `0600`, không đưa vào browser. Probe không gửi prompt hoặc xác minh model entitlement.

`.env` được bootstrap ngẫu nhiên, quyền `0600` và bị Git ignore. Không commit/copy secret; `.env.example` chỉ chứa chỉ dẫn placeholder. Owner session lấy scope được backend cấp; mọi cấu hình profile/run/grant và reset demo cần Owner + CSRF. API vẫn chỉ bind loopback.

## Runtime Phase 06–07

Sau khi kiểm tra migration mới trên môi trường kiểm thử riêng, chạy upgrade cho database local của dự án rồi khởi động lại API theo lệnh ở trên. Tạo secret Owner (giữ secret có sẵn, không tự xoay):

```sh
rtk proxy python3 scripts/bootstrap_owner.py
rtk proxy uv run --project apps/api alembic -c apps/api/alembic.ini upgrade head
```

Mở **Quản trị** hoặc **Văn phòng trực tiếp** để đăng nhập bằng file `.local/owner-secret` (0600; mở local, không gửi qua chat). Session bền vững có expiry/revocation, cookie HttpOnly/SameSite, scope demo do backend xác minh và CSRF cho thao tác ghi. Model profile version hóa; profile/catalog không cấp entitlement hoặc grant. Reset demo từ UI cũng cần session và không thể xóa run đang có liên kết runtime; nếu bị từ chối, giao dịch rollback và giữ dữ liệu.

Runtime mặc định khóa inference. Grant phải được Chủ tịch cấp riêng qua API Owner cho đúng phase/batch/purpose/model/effort/scope, requests gồm retries, concurrency1, timeout≤120s và expiry≤1h. UI chỉ chọn grant đã có, không tạo tự động. CG01 cần proof do người vận hành kiểm chứng riêng tại `.local/cg01-proof.json`, mode0600, gắn endpoint/source fingerprint/expiry và evidence. API không có cờ để tự bỏ gate; repo không tạo proof đạt giả. Gate metadata không thay bằng chứng cách ly thực tế.

Worker chỉ chạy bằng lệnh tường minh, không từ startup/health/seed hoặc mở trang:

```sh
rtk proxy uv run --project apps/api python -m agent_corporation_api.modules.execution.worker --environment <UUID_SCOPE_ĐÃ_CẤP> --company <UUID_SCOPE_ĐÃ_CẤP> --once
```

Lệnh worker có thể gọi model nếu gate và grant đều hợp lệ; chưa được chạy trong đợt triển khai này. Mỗi run tối đa một turn text-only, tools/fallback tắt. PG guard giới hạn một call toàn app; 429 requeue có giới hạn theo grant (backoff1/3s), timeout/disconnect/crash/stop giữ unknown và không retry. Thiếu usage giữ unresolved; giá/cost vẫn chưa biết. Run completed không tự nghiệm thu task.

Event list và SSE chỉ đọc event đã commit trong scope session. Cursor có chữ ký, gắn session/scope; reconnect dùng Last-Event-ID, không tạo model/tool request. Gặp gap/reset nguồn cần tải lại tường minh. Heartbeat SSE phản ánh kết nối event store; heartbeat worker được hiển thị riêng. Prompt, output thô và đường dẫn host không nằm trong SSE; kết quả đã lọc được đọc qua API run theo Owner scope. Office 2D/Inspector/replay đầy đủ vẫn thuộc Phase08.

## Kiểm tra và tài liệu

```sh
uv run --project apps/api pytest apps/api/tests
uv run --project apps/api alembic -c apps/api/alembic.ini current
npm run --prefix apps/web build
rtk proxy python3 scripts/render_plan.py
rtk proxy python3 scripts/validate_phase00.py
```

Các lệnh tài liệu chỉ xử lý file local, không gọi model. Inference grant hiện là 0; Phase 03 không gọi inference. Mỗi phase sau cần được giao riêng.
