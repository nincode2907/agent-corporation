# Agent Corporation

Nền tảng local-first để Chủ tịch giao mục tiêu, kiểm soát quyền và nghiệm thu bằng chứng. Runtime đã có một lượt inference demo thật; CG01 production vẫn chưa đạt. Development Playground cho thử nghiệm hội thoại theo Session Grant riêng của Owner. Trạng thái chính thức ở master plan.

- [Mở trang theo dõi phase](docs/master-plan.html)
- [Kế hoạch và nguồn trạng thái chính thức](docs/master-plan.md)
- [Đặc tả V1](docs/product-spec.html)
- [Quyết định nền V1](docs/decisions/0001-v1-foundation.html)
- [Bằng chứng Phase 00](docs/evidence/phase-00.md)
- [Bằng chứng Phase 01](docs/evidence/phase-01.md)
- [Bằng chứng Phase 02](docs/evidence/phase-02.md)
- [Bằng chứng Phase 03](docs/evidence/phase-03.md)
- [Bằng chứng Phase 04](docs/evidence/phase-04.md)
- [Employee Chat — thiết kế V1](docs/designs/employee-chat.html) · [Markdown](docs/designs/employee-chat.md)
- [CG01 — kiểm định và quy trình xác minh](docs/reviews/cg01-20261014/report.html) · [Markdown](docs/reviews/cg01-20261014/report.md)
- [Hướng dẫn cho agent](AGENTS.md)
- [Bộ rule và checklist kiểm định từng phase](docs/tests/README.md) · [Bản trực quan](docs/tests/index.html)

## Development Playground (demo)

Mở `http://127.0.0.1:15500/#playground` sau khi chạy app. Owner đăng nhập một lần bằng secret local (không gửi qua chat), chọn nhân viên demo, model và effort. Ở form “Cấp Session Grant”, chọn số request/thời hạn, đọc và tick chấp nhận dữ liệu demo không nhạy cảm, rồi bấm “Cấp quyền và bắt đầu trò chuyện”. Đây là thao tác cấp quyền duy nhất cho phiên; gửi các tin nhắn kế tiếp trong cùng grant không cần xác nhận lại.

Worker Playground tự chạy và dừng cùng API, chỉ xử lý tin nhắn đã được gửi và được grant cho phép. Không cần lệnh worker thủ công. Mở app, login, đọc catalog hoặc tạo grant không tự gọi model. Chuyển nhân viên/model cần tạo phiên mới; lịch sử phiên cũ vẫn đọc được. Model catalog không xác nhận entitlement.

Grant cho 1–100 requests, 1–240 phút, concurrency 1, timeout tối đa 120 giây/request; không retry, fallback, tools, network tools, file/terminal/deploy/company mutation. Hạn mức gợi ý trong form chưa là quyền đã cấp. App không tăng limit, gia hạn hay cấp grant mới. Thời điểm hết hạn thực tế không vượt quá hạn của Owner session gốc; đăng xuất cũng dừng quyền của phiên. `PLAYGROUND_WORKER_ENABLED=false` tắt riêng worker Playground nếu cần vận hành; mặc định bật cùng API.

Stop hủy queued turn trước dispatch; request đang bay được đóng HTTP và có thể giữ `unknown`. Worker crash/restart không phát lại call chưa rõ kết quả. Nếu có unknown, kiểm tra bên gateway đã kết thúc request rồi dùng xác nhận đối chiếu trong UI; outcome/usage vẫn unknown, lượt đã dùng không được hoàn lại. Usage thiếu hiển thị “chưa biết”; chi phí chưa có pricing cũng chưa biết. Context gửi lại tối đa 10 lượt hoàn tất, dưới 48 KB; lịch sử UI vẫn được lưu.

Playground là ngoại lệ demo được Owner chấp nhận, luôn `verified=false`, độc lập với proof/CG01 production và grant Work Order. Không dùng dữ liệu nhạy cảm. PASS Playground không nghiệm thu Phase 06 production hoặc release. [ADR-0003](docs/decisions/0003-development-playground.md) mô tả state, quyền và giới hạn. Seed/reset demo sẽ bị từ chối nếu còn session/call tham chiếu thay vì xóa ngầm evidence.

Kiểm thử tự động trên DB tạm, transport giả (không gọi AI):

```sh
rtk proxy uv run --project apps/api python -X utf8 scripts/test_playground_isolated.py
```

Runner tạo database/role có tên riêng, migrate và chạy grant/expiry/duplicate/Stop/process crash/restart/RLS cùng regression Work Order, rồi dọn đúng tài nguyên đó. Không reset database runtime.

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

Sau lần chuẩn bị đầu tiên, có thể chạy toàn bộ ứng dụng bằng một file: macOS/Linux dùng `./run.sh`; Windows dùng `run.bat`. Script tự tạo `.env` nếu chưa có, bật PostgreSQL, đồng bộ dependency Python, cài dependency web nếu thiếu, chạy migration rồi mở API và web. Trên macOS/Linux, nhấn `Ctrl+C` để dừng API và web; trên Windows, đóng hai cửa sổ API/Web. PostgreSQL tiếp tục chạy nền.

Phase 05 probe Codex server thủ công từ backend bằng `GET /health` và `GET /v1/models`. Mặc định gateway là `http://127.0.0.1:15600`, đã đối chiếu registry/source và GET ngày 09/10/2026 (endpoint khảo sát cũ là4000). Nếu cần cấu hình Bearer, chỉ lưu `CODEX_SERVER_API_KEY` trong `.env` mode `0600`, không đưa vào browser. Probe không gửi prompt hoặc xác minh model entitlement.

`.env` được bootstrap ngẫu nhiên, quyền `0600` và bị Git ignore. Không commit/copy secret; `.env.example` chỉ chứa chỉ dẫn placeholder. Owner session lấy scope được backend cấp; mọi cấu hình profile/run/grant và reset demo cần Owner + CSRF. API vẫn chỉ bind loopback.

## Runtime Phase 06–07

Sau khi kiểm tra migration mới trên môi trường kiểm thử riêng, chạy upgrade cho database local của dự án rồi khởi động lại API theo lệnh ở trên. Tạo secret Owner (giữ secret có sẵn, không tự xoay):

```sh
rtk proxy python3 scripts/bootstrap_owner.py
rtk proxy uv run --project apps/api alembic -c apps/api/alembic.ini upgrade head
```

Mở **Quản trị** hoặc **Văn phòng trực tiếp** để đăng nhập bằng file `.local/owner-secret` (0600; mở local, không gửi qua chat). Session bền vững có expiry/revocation, cookie HttpOnly/SameSite, scope demo do backend xác minh và CSRF cho thao tác ghi. Model profile version hóa; profile/catalog không cấp entitlement hoặc grant. Reset demo từ UI cũng cần session và không thể xóa run đang có liên kết runtime; nếu bị từ chối, giao dịch rollback và giữ dữ liệu.

Runtime mặc định khóa inference. Grant phải được Chủ tịch cấp riêng qua API Owner cho đúng phase/batch/purpose/model/effort/scope, requests gồm retries, concurrency1, timeout≤120s và expiry≤1h. UI chỉ chọn grant đã có, không tạo tự động. Ở chế độ strict, CG01 cần proof do người vận hành kiểm chứng riêng tại `.local/cg01-proof.json`, mode0600, gắn endpoint/source fingerprint/expiry và evidence. Request API không có cờ để tự bỏ gate; repo không tạo proof đạt giả. Gate metadata không thay bằng chứng cách ly thực tế.

### Ngoại lệ kiểm thử demo được Chủ tịch cho phép ngày 14/10/2026

Theo chỉ thị “tạm thời mở gateway để test, khi nào đến phase cuối thì khóa lại mở như hiện tại”, cấu hình local có thể tạm đi qua CG01 bằng `RUNTIME_CG01_DEMO_TEST_OVERRIDE=true`. Mặc định source và `.env.example` là `false` (strict). Ngoại lệ chỉ áp dụng cho đúng scope demo cố định và endpoint HTTP literal loopback đã được adapter cho phép; không mở host.docker.internal/LAN. Đây là quyền thử nghiệm khi CG01 **chưa được xác minh**, không phải proof hoặc nghiệm thu isolation/privacy/cancellation.

```sh
rtk proxy python scripts/cg01_mode.py demo-test
# Khóa lại CG01 theo proof như trước:
rtk proxy python scripts/cg01_mode.py strict
# Bắt buộc trước Phase 23; exit 1 nếu ngoại lệ còn bật hoặc proof chưa đạt:
rtk proxy uv run --project apps/api python scripts/cg01_mode.py release-check
```

Lệnh đổi mode chỉ cập nhật key này trong `.env` đã tồn tại, giữ các giá trị khác và không in secret. Sau khi đổi, khởi động lại API/worker; khi khóa lại, stop/revoke các run đang chạy trước khi dừng worker. Thay đổi file không tự hủy request đang bay. UI hiển thị “Mở tạm cho demo”, API status có `mode=demo-test, verified=false`, policy snapshot của run ghi gate lúc tạo.

Owner/session/CSRF, grant đúng Phase 06/07/batch/model/effort/expiry, hạn mức request/concurrency/timeout, stop và tools-off vẫn bắt buộc. Mode này không tạo grant, không gửi prompt, không khởi động worker/gateway và không cấp quyền sửa gateway dùng chung. Chỉ dùng input giả hoặc văn bản tin cậy không có secret cho các đợt test được cấp riêng.

Trên Windows native, nhánh strict CG01 trả `unsupported_platform` thay vì lỗi thiếu POSIX API. Nhánh demo-test chạy độc lập với POSIX proof. Owner secret dùng protected Windows DACL; kiểm tra local xác nhận ACL và test ACL Windows đạt, nhưng phiên Owner trên trình duyệt và inference qua app chưa được kiểm chứng. Chỉ tiếp tục sau khi Chủ tịch tự đăng nhập trong UI; không gửi secret qua chat. Lượt kiểm định 14/10 đã khởi động PostgreSQL/migration/seed local, API và gateway health/models đều phản hồi; không thay đổi cấu hình gateway dùng chung.

Runtime Phase 06 cho phép Chủ tịch tạo grant test tường minh ngay trong UI sau khi lưu model profile: một request, concurrency 1, timeout 120 giây, không retry, tools tắt, expiry 15 phút. Tạo grant chỉ ghi quyền/audit, không gọi model. Gửi run là thao tác riêng; UI hiện chỉ cho gửi khi CG01 cho phép và grant còn hiệu lực. Tài khoản mới cần chọn/lưu model và reasoning effort trước khi cấp grant. Catalog/models không xác nhận entitlement.

Trước kiểm định/nghiệm thu Phase 23: chuyển strict, stop/restart workers, chạy release-check đạt và xác minh lại CG01 thật. Ngoại lệ không tự tắt theo Markdown roadmap; thao tác khóa lại là checklist bắt buộc và còn được nhắc trong `AGENTS.md`/master plan. Các báo cáo CG01 cũ giữ nguyên giá trị lịch sử, không đổi thành PASS.

Worker Work Order runtime chỉ chạy bằng lệnh tường minh, không từ startup/health/seed hoặc mở trang. Worker Development Playground được app quản lý riêng, xem bên dưới:

```sh
rtk proxy uv run --project apps/api python -c "import sys;sys.path.insert(0,'apps/api/src');from agent_corporation_api.modules.execution.worker import main;main()" --environment <UUID_SCOPE_ĐÃ_CẤP> --company <UUID_SCOPE_ĐÃ_CẤP> --once
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

Các lệnh validation tài liệu chỉ xử lý file local, không gọi model. Đợt test Phase 06 ngày 14/10 đã dùng hết grant một request; không còn grant hợp lệ cho lần gọi tiếp theo. Phase 03 không gọi inference. Mỗi phase sau cần được giao riêng.
