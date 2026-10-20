# Agent Corporation

## Hướng dẫn áp dụng
- Đọc và tuân thủ `/Users/buivannin/.codex/RTK.md`; mọi lệnh shell dùng tiền tố `rtk`.
- Dự án local-first để Chủ tịch giao mục tiêu, quản lý nhân viên AI, quan sát thực thi và nghiệm thu bằng chứng.
- Trạng thái phase theo `docs/master-plan.md`: Phase 00 Hoàn tất; Phase 01–05 Chờ nghiệm thu; Phase 06–08 Bị chặn. Mỗi lượt chỉ triển khai phase được giao; không tự chuyển sang phase tiếp.
- Chỉ triển khai phase người dùng yêu cầu; hết phase thì báo cáo và dừng. Không tự chuyển phase, tạo công ty thật, gọi inference hoặc thay cấu hình toàn máy.

## Đọc đúng ngữ cảnh
- Trước khi triển khai: đọc `docs/master-plan.md`, phase được yêu cầu, dependency và các quy tắc V1.
- Đặc tả V1: đọc `docs/product-spec.md` và `docs/decisions/0001-v1-foundation.md` trước scaffold/data/runtime; baseline đã được Chủ tịch nghiệm thu Phase 00.
- Đối chiếu ý tưởng khi cần: `docs/sources/`; bản 02 ưu tiên cho thứ tự xây sản phẩm trước, vận hành sau.
- Setup/runtime: dùng skill global `project-ai-bootstrap`; gateway: đọc README/source của codex-server; OpenAI native protocol dùng `openai-docs` khi cần.
- UI dùng `ui-page-builder` hoặc `frontend-design`; feature dùng `feature-builder`; QA sau phase dùng `task-qa-review` khi phù hợp. Không nạp toàn bộ skill cùng lúc.
- Flow mặc định trong phase được giao: code → test ghi `docs/tests/results/` → remake theo report ghi `docs/remakes/` → retest ghi batch results mới; còn `need-change` giải quyết được thì tiếp tục. Đọc `docs/tests/RULES.md` và `docs/tests/phases/phase-NN.md`, dùng số vòng `rNNN` và tên file theo rule. “Chỉ test/không sửa” thì chỉ kiểm định; blocker thật cần quyền/dependency ngoài scope thì ghi rõ rồi dừng. Mỗi test có tag `clean`, `need-change` hoặc `suggestion`; thiếu evidence không được `clean`. AI không tự nghiệm thu hoặc sang phase khác.
- Pipeline do AI điều phối tự động: AI code/remake và AI test độc lập là agent khác nhau, dùng công cụ cộng tác để bàn giao tuần tự khi có. AI test ghi issue; AI remake ghi sửa hoặc phản biện; AI test lại xác minh đến OK hoặc blocker thật. Chủ tịch chỉ theo dõi tab Kiểm thử, không phải tick/duyệt giữa các vòng. Dấu tick tự suy từ results/remakes theo RULES; render roadmap sau mỗi bước.

## Ranh giới quan trọng
- Runtime dùng HTTP gateway `/Users/buivannin/Desktop/workspace/personal/codex-server`, host `127.0.0.1:15600`. Theo phương án Docker được Chủ tịch duyệt 15/10/2026, container dùng mode `docker-host`, chỉ endpoint `http://host.docker.internal:15600` và HTTP Host `127.0.0.1:15600`; native mode giữ literal loopback. Đọc contract/source; không đổi server chung, không giả định streaming hay model entitlement.
- Demo, benchmark và công ty thật phải tách dữ liệu, artifacts, threads, secrets và báo cáo.
- Model/policy/ngân sách/quyền do Chủ tịch quyết định. Agent chỉ đề xuất, backend kiểm tra quyền; prompt không phải permission engine.
- Event store và execution state bền vững từ đầu; ghi bằng chứng, tóm tắt quyết định tường minh, không hứa hiển thị suy nghĩ nội bộ.
- Grant inference cấp riêng cho đúng phase/test batch/mục đích/hạn mức/expiry; không kế thừa giữa phase/đợt test. Nghiệm thu Phase 00 không cấp grant/model access hoặc quyền bắt đầu Phase 01.
- Development Playground demo Phase 06 theo ADR-0003 có Session Grant riêng do Owner tạo trong UI: quyền một lần cho nhiều tin nhắn trong limit/expiry/profile đã chốt; không hỏi lại từng message. Worker Playground tự chạy cùng API, chỉ dispatch queue Playground đã được cấp. Không tạo Work Order hay tự cấp/gia hạn grant. Policy Development Playground không phải CG01 verified/production acceptance; test mock không cấp inference thật.
- Ngoại lệ Chủ tịch ngày 14/10/2026: cho phép tạm qua CG01 để test scope demo bằng `RUNTIME_CG01_DEMO_TEST_OVERRIDE=true`, theo [README](README.md#ngoại-lệ-kiểm-thử-demo-được-chủ-tịch-cho-phép-ngày-14102026). Không coi CG01 đã xác minh; giữ Owner/CSRF/grant/limits/stop/tools-off. Trước Phase 23 phải chuyển `strict`, stop/restart worker, chạy `rtk proxy docker compose exec api python scripts/cg01_mode.py release-check` đạt rồi mới kiểm định release; không giữ ngoại lệ cho nghiệm thu/vận hành thật.
- Không đoán usage/giá; phân biệt xác nhận, ước tính, chưa biết. Giới hạn run và dừng khẩn cấp trước agent thật.
- Không retry tool có side effect khi chưa biết kết quả; resume phải kiểm tra checkpoint và idempotency.
- Tiếng Việt cho giao diện/tài liệu người dùng, `lang="vi"`, favicon, responsive và accessibility.

## Tài liệu và nghiệm thu
- `docs/master-plan.md` là nguồn chuẩn cho phạm vi, trạng thái và bằng chứng phase; HTML là bản nhìn trực quan.
- Sửa Markdown trước, đồng bộ HTML bằng `rtk proxy python3 scripts/render_plan.py` từ root. Template tại `docs/assets/roadmap-template.html`.
- Tài liệu Phase 00: `rtk proxy python3 scripts/render_phase00.py` đồng bộ spec/ADR/roadmap; `rtk proxy python3 scripts/validate_phase00.py` chỉ kiểm tra tài liệu local, không inference.
- Ghi chú/checklist trong trình duyệt chỉ là ghi chú cá nhân; không thay trạng thái chính thức.
- Chỉ hoàn tất phase khi có demo, kiểm thử phù hợp, evidence và người dùng nghiệm thu; cập nhật Markdown rồi render HTML cùng lần.
- Không commit/push hoặc cài global tool khi chưa được yêu cầu.

## Runtime Phase 01
- Stack và dependency pins: `apps/web/package-lock.json`, `apps/api/uv.lock`, `compose.yml`; setup từ [README.md](README.md).
- Chỉ dùng `docker compose up --build` (sau đó `docker compose up`): một compose.yml tự bootstrap config/Owner → PG → migration → API/web; không cần wrapper, `.env` trước hoặc Python/Node trên host. `.env` cũ chỉ nhập readonly nếu có, credential mới tạo một lần trong volumes. API/worker UID1000, Owner/config mode0600; API không mount volume credential admin. Không in secret; không dùng `down --volumes` trên runtime. Operator tự xem Owner secret bằng `docker compose exec api cat /runtime-secrets/owner-secret` tại máy khi cần đăng nhập.
- PostgreSQL chỉ bind `127.0.0.1:15510`; API `127.0.0.1:15501`; Nginx web `127.0.0.1:15500` proxy `/api` cùng origin, SSE không buffer. Vite chỉ dùng khi phát triển native và đã dừng Docker web/API.
- Giữ volume `agent-corporation_agent_corporation_postgres`; không dùng `down --volumes` trên runtime. Migration credential chỉ có trong service migrate, không đưa vào API. Không mount native Codex auth/session; chỉ năm source files phục vụ fingerprint. Strict proof phải gắn endpoint + `gateway_transport: docker-host` cho Docker.
- Dev Hub mapping ở registry trung tâm, block `15500–15599`; `agent-corporation.localhost` đi qua Caddy chỉ publish trên IPv4 loopback (Docker host từ chối bind IPv6 loopback).
- Smoke/API: `uv run --project apps/api pytest apps/api/tests`; web: `npm run --prefix apps/web build`; migration: `uv run --project apps/api alembic -c apps/api/alembic.ini upgrade head`.
- Health chỉ kiểm tra liveness/readiness. Phase 06–07 đã bổ sung Owner session/CSRF/profile, worker text-only có gate/grant và event feed/SSE; worker không tự chạy khi mở trang. Phase 06 đã có một grant test một request được dùng hết ngày 14/10/2026; không còn grant hợp lệ. Các phase vẫn chờ kiểm định/nghiệm thu phù hợp.

## Runtime tương lai
- Trước quyết định host port đọc `/Users/buivannin/Desktop/workspace/personal/dev-hub/projects.yml`, kiểm tra toàn block và listener rồi reserve → verify → configure.
- Allocation/hostname hoạt động đã được xác minh ở Phase 01/03. Không dùng port dự đoán; thay đổi shared proxy chỉ trong phạm vi route local đã được yêu cầu và có evidence.
- Khi triển khai runtime, giữ server trong terminal tương tác nhìn được log; chỉ công bố URL đã xác minh.
