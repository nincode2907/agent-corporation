# Kế hoạch Agent Corporation

> Phiên bản kế hoạch: 1.0 · Ngày lập: 08/10/2026 · Ngôn ngữ: tiếng Việt.
> Trạng thái: **Phase 00–03 Hoàn tất; Phase 04–05 Chờ nghiệm thu; Phase 06 Bị chặn; 4/24 phase hoàn tất**. Chưa có runtime agent, chưa gọi inference.

## 1. Hướng đi đã chọn

Xây nền tảng hoàn chỉnh trước, kiểm thử bằng công ty demo và agent thử nghiệm, đạt V1 rồi Chủ tịch mới chính thức thành lập tập đoàn. Bản ý tưởng thứ hai ưu tiên cho thứ tự delivery; giữ business logic cốt lõi của bản thứ nhất. 24 phase là các lát triển khai có thể nghiệm thu, không phải cam kết thời gian hay số lượng bất biến. Mỗi phase chỉ bắt đầu khi người dùng giao tiếp; kết thúc phase báo cáo, đợi yêu cầu tiếp.

### Tầm nhìn V1

- Chủ tịch sở hữu chiến lược, ngân sách và quyền. AI thực hiện trong giới hạn; hệ thống giữ bằng chứng và lịch sử.
- Chairman Mode: giao mục tiêu, duyệt đề xuất, nhận báo cáo. Operator Mode: xem task/run/agent/tools/metrics/config.
- Dashboard → Live Office 2D → Agent Inspector dùng chung; replay từ dữ liệu đã lưu.
- Work Order → lập kế hoạch → thực hiện → kiểm tra → sửa nếu cần → Chủ tịch nghiệm thu.
- Nhân viên là hồ sơ version hóa, không phải tiến trình suy nghĩ liên tục. Chỉ kích hoạt khi có việc.
- Chief of Staff đầu tiên; CEO, hội đồng nhiều agent và văn phòng 3D để sau V1 khi có nhu cầu.

### Hai chặng

| Chặng | Phạm vi | Điểm kết thúc |
| --- | --- | --- |
| A — Xây sản phẩm | Phase 00–23; fixtures và công ty demo; agent thật có sandbox và hạn mức test được cấp | Chủ tịch nghiệm thu V1 |
| B — Vận hành thật | Sau V1; mở wizard → đặt công ty → chọn mục tiêu/model/quyền/ngân sách → bổ nhiệm Chief of Staff → giao việc | Đo chất lượng/chi phí và cải tiến từ dữ liệu thực |

## 2. Các mốc bàn giao

| Mốc | Phase | Giá trị mới cuối mốc |
| --- | --- | --- |
| A | 00–04 | Nền local, khung giao diện, dữ liệu bền vững và demo tách biệt |
| B | 05–10 | Agent thật sandbox, live trace, Inspector/replay, task queue và phê duyệt |
| C | 11–15 | Tools, giao việc nhiều agent, phòng ban, HR và memory có kiểm chứng |
| D | 16–20 | Tài chính, benchmark, tối ưu, sự cố và báo cáo điều hành |
| E | 21–23 | Onboarding, bảo vệ/khôi phục dữ liệu và release V1 |

## 3. Quy tắc không được trì hoãn

1. Demo/benchmark/real tách dữ liệu, artifacts, threads, secrets và báo cáo; development không tạo tập đoàn thật của người dùng.
2. Event store, execution state, correlation và redaction có từ Phase 03. Phase 07 làm streaming/recovery; không tạo trace bằng state UI tạm.
3. Default deny, sandbox, resource limits, owner-only model/policy và stop tối thiểu có trước turn thật Phase 06. Phase 10/16/19 mở rộng quyền/tài chính/sự cố; không trì hoãn kiểm soát cốt lõi tới đó.
4. Agent không tự tuyển/sa thải cố định, đổi model, tăng ngân sách, mở quyền, sửa Hiến pháp, deploy production, gửi dữ liệu ngoài hoặc xóa dữ liệu quan trọng. Đề xuất phải tới Chủ tịch.
5. Giá/usage đều có nguồn và phiên bản. Unknown khác 0; live estimate khác final usage. Subscription/API/local compute tách riêng.
6. Plan và Decision Summary là nội dung tường minh; không phụ thuộc suy nghĩ nội bộ nguyên văn. Prompt/tool/output lưu theo ACL, retention và redaction policy.
7. Run completed khác task accepted. Nghiệm thu cần artifact/test/review/human decision. Replay chỉ đọc, không gọi lại tool.
8. Pause/resume theo bước/checkpoint; không hứa tiếp tục từ giữa token. Retry side effect phải biết outcome hoặc có idempotency receipt.
9. Không có inference tự động khi mở trang, seed demo hay chạy health check. Test thật cần grant riêng gắn phase/test_batch_id/mục đích/phạm vi/hạn mức/expiry; không kế thừa qua đợt test hoặc phase. Model fallback phải được Chủ tịch cho phép trước.
10. Mọi màn hình người dùng tiếng Việt, `lang=vi`, favicon; trạng thái idle/offline dựa trên runtime thật.

## 4. Kiến trúc đề xuất và Codex local

Baseline đã chọn trong đặc tả Phase 00, đã được Chủ tịch nghiệm thu, chưa có code: React + TypeScript + Vite frontend; Python + FastAPI + Pydantic modular monolith; PostgreSQL + SQLAlchemy/Alembic; queue/scheduler bền vững trong nền backend. Compose cho hạ tầng local. Tránh thêm Redis/LangGraph/Temporal/Langfuse/LiteLLM trước khi có nhu cầu và evidence; không dùng thêm framework để lặp lại orchestration của Codex.

```text
Chủ tịch / giao diện React
            ↓ HTTP + SSE (đề xuất)
Backend: công ty / Work Order / policy / approvals / orchestration
       ├── PostgreSQL: execution state + events + ledger + memory
       ├── Kho artifacts tách môi trường
       └── Adapter HTTP local → codex-server → Codex CLI → model/provider
                                  └── trả tool proposals; app thực thi trong sandbox riêng
Event đã lưu → Live Office / Inspector / Replay / Finance / Benchmark / Reports
```

### Tích hợp codex-server hiện có

Sử dụng project có thật tại `/Users/buivannin/Desktop/workspace/personal/codex-server`, đang nghe `127.0.0.1:4000`. `GET /health` trả HTTP 200, `{ok:true, provider:codex, active_requests:0}` lúc khảo sát. Đây là HTTP gateway riêng, không phải Codex App Server. Agent Corporation backend kết nối server-to-server; browser chỉ gọi backend của mình. Không sửa CORS, bind, quyền hay storage gateway để làm kết nối hoạt động.

Nguồn hợp đồng: [README gateway](../../codex-server/README.md), `codex-server/src/server.ts`, `src/schema.ts`, `src/provider.ts`; source ưu tiên khi docs lệch. Routes hiện có: `GET /health`, `GET /v1/models`, `POST /v1/chat/completions`, tùy chọn session APIs. `/v1/models` hiện gồm configured model + catalog hỗ trợ chat theo source, không chứng minh account entitlement. Model `gpt-6.1-sol` và effort `high` là lựa chọn mong muốn trong ý tưởng, phải thử có hạn mức trước khi khẳng định dùng được. Không in `.env`, auth hoặc session transcripts.

| Khả năng gateway hiện tại | Cách Agent Corporation xử lý |
| --- | --- |
| Text Chat Completions, `stream=false`, usage khi trả kết quả | Ghi request-start/waiting/response; không bịa stream token hay event nội bộ CLI |
| Function calling là structured proposals; gateway không thực thi tools | Backend kiểm tra JSON schema + policy + approval, sandbox executor chạy tool, lưu receipt rồi gửi `role=tool` lượt sau |
| `X-Codex-Call-Id`, usage của cả Codex turn | Map HTTP call ID → company/task/run/agent; app ledger chỉ tính call của mình, không cộng toàn bộ native/gateway totals |
| Timeout và cancellation theo disconnect; 429 concurrency, 409 session busy | App queue/retry có backoff, abort HTTP khi dừng; kiểm tra gateway đã hủy thực, không coi đóng UI là dừng inference |
| Sessions có TTL, model/effort cố định, lỗi/timeout vô hiệu hóa session | Mặc định chat stateless + history/checkpoints bền vững do app giữ; nếu dùng session thì xử lý expired/invalidated, không tự resume failed history |
| Không có `max_tokens`, full Responses API hay native tools | Token hard cap giữa request chưa được hỗ trợ; dùng giới hạn số lượt/thời gian/concurrency và reservation; chặn bước mới sau final usage, ghi rõ overshoot có thể của lượt đang chạy |

Live Observatory V1 quan sát các bước do ứng dụng quản lý: task, request model, plan tường minh khi nhận response, tool calls thật của app, handoff, review, approvals, usage cuối lượt và lỗi. Phase 07 dùng SSE từ event store của Agent Corporation tới UI; không có nghĩa gateway hỗ trợ SSE/token streaming. Replay chỉ tái dựng events đã ghi. Nếu cần token stream/native Codex execution events, đó là thay đổi capability riêng của codex-server hoặc adapter khác, không âm thầm áp trong V1.

Read-only của gateway không đủ cô lập quyền đọc dữ liệu. Trước inference từ task không tin cậy, kiểm chứng isolation user/container và context/secret boundary; nếu không đạt thì chặn run và báo blocker, không nới quyền server chung. Tool executor của Agent Corporation tách biệt với inference gateway, phải enforce sandbox/policy thật.

Có `codex-cli 0.162.0-alpha.2` trong PATH và có lệnh `codex app-server`; đây chỉ là quan sát bổ sung, không phải adapter mặc định. [Tài liệu App Server chính thức](https://learn.chatgpt.com/docs/app-server) là nguồn cho khả năng tùy chọn sau này. Chưa gọi inference, chưa xác minh entitlement/usage thực; không khẳng định server local miễn phí hay model chạy offline.

## 5. Khảo sát bootstrap và runtime

Khảo sát tại `/Users/buivannin/Desktop/workspace/personal/agent-corporation`, ngày 08/10/2026, trước thay đổi:

| Khu vực | Bằng chứng / kết luận | Hướng xử lý |
| --- | --- | --- |
| Repository | Thư mục trống; `git status` báo không phải Git repository; không manifest/source/test | Chỉ tạo tài liệu và hướng dẫn; scaffold/Git thuộc Phase 01 |
| Agent instructions | Không có AGENTS.md root/nested/ancestor trên đường dẫn khảo sát; user cung cấp RTK.md | Tạo root AGENTS.md nhỏ, giữ rule rtk; không có nội dung cần migrate/xóa |
| Knowledge | Hai file ý tưởng được cung cấp, bản 02 điều chỉnh roadmap bản 01 | Lưu nguyên bản ở docs/sources; master-plan là nguồn chuẩn của phạm vi/trạng thái |
| Chất lượng instruction | Chưa có rule project cũ để phát hiện duplicate/obsolete; thiếu rule phase delivery/isolation/evidence/runtime | Bổ sung các invariant vào AGENTS.md; không sao chép toàn bộ skill global |
| Skill global | project-ai-bootstrap, openai-docs, frontend-design có sẵn và đã dùng ở bước này | Route on demand; feature-builder/ui-page-builder/task-qa-review dùng khi phase phù hợp |
| Dev Hub registry | `/Users/buivannin/Desktop/workspace/personal/dev-hub/projects.yml`, version 1; không entry trùng path/ID của dự án | Chưa reserve vì chỉ lập kế hoạch; đọc lại registry/listeners ở Phase 01 |
| Port hiện tại | Dự án chưa có allocation; gateway riêng đã nghe 127.0.0.1:4000, Docker port 80 wildcard | Không gán port, không dừng service khác; kiểm tra toàn block trước khi reserve |
| Proxy | Dev Hub Caddyfile có 5 route khác, không route Agent Corporation; compose.proxy.yml publish `80:80`, DEV_HUB_BIND=0.0.0.0 | Proxy hiện tại không loopback-only; không thay system/proxy trong bước này |
| Hostname | Chưa có hostname/HTTP route của dự án được kiểm chứng | `agent-corporation.localhost` chỉ là tên dự kiến, chưa hoạt động; Phase 01 chốt theo registry |
| Lệnh hiện hữu | Kiểm tra CLI, GET /health gateway 200 và Python dựng tài liệu | Không ghi npm/compose/dev commands như đã chạy thành công |

### Thay đổi trong bước lập kế hoạch

- Tạo `AGENTS.md`: operating manual và route đọc đúng ngữ cảnh; từ chưa tồn tại thành 34 dòng. Không tạo project skill vì chưa có workflow thực cần tách.
- Tạo `docs/master-plan.md` và `docs/master-plan.html`: nguồn chuẩn và trang trực quan cùng ý nghĩa.
- Tạo `docs/assets/roadmap-template.html`, `scripts/render_plan.py`: chỉ phục vụ tài liệu, không là product frontend/backend.
- Lưu `docs/sources/01-y-tuong-tap-doan.txt`, `02-xay-san-pham-truoc.txt` nguyên bản; `README.md` hướng dẫn mở và render.
- Không init Git, install dependency, reserve port, start product server, sửa Dev Hub, gọi inference, commit hoặc push.

### Quyết định còn mở

Stack/auth boundary/data/state/event/queue đã có baseline để nghiệm thu tại `docs/product-spec.md`; D01–D08 và O01–O07 có owner/deadline/deny behavior. Phase 00 được nghiệm thu về đặc tả/baseline; Phase 01 đã được Chủ tịch duyệt ngày 08/10/2026. Các quyết định nghiệm thu không tự cấp quyền runtime hay inference. Profile/model entitlement, auth gateway nếu enabled, sandbox/isolation và grant test phải được xác minh/cấp riêng trước lượt chạy thật (hiện grant = 0). Service-to-port mapping, binding/proxy access và route được kiểm tra theo Phase 01. Ngưỡng hiệu năng/retention/backup đặt mục tiêu đề xuất ở release gate, chốt trong spec và đo bằng môi trường máy thật; không có lịch/ngân sách dollar ước đoán.

## 6. Cách theo dõi và yêu cầu triển khai

Mở `master-plan.html` trực tiếp trong trình duyệt; không cần server/port. Mỗi phase có phần mới, dependency, phạm vi, demo, checklist và evidence. Search/lọc mốc để tìm phần cần xem; chọn phase rồi sao chép yêu cầu triển khai và gửi trong cuộc trò chuyện.

Trạng thái chính thức trong Markdown: **Chưa triển khai → Đang triển khai → Chờ nghiệm thu → Hoàn tất**; **Bị chặn** phải nêu blocker. HTML đọc trạng thái này, không tự chốt DONE. Phase 00–03 đã hoàn tất; Phase 04–05 chờ nghiệm thu; Phase 06 bị chặn tại dependency Phase 05 và CG01; Phase 07–23 Chưa triển khai. Inference grant = 0.

Checklist/ghi chú cá nhân trên HTML lưu trong localStorage nếu browser cho phép; không sửa Markdown, không giao task cho Codex và không gọi backend. Có thể xuất JSON để giữ ghi chú rồi gửi cùng phản hồi nghiệm thu. File HTML khác path/browser có thể có bộ ghi chú khác; xuất trước khi đổi nơi lưu. Nếu storage bị chặn, UI báo chưa lưu bền vững; nội dung vẫn xuất được trong phiên hiện tại. Khi kế hoạch/checklist đổi phiên bản, xuất ghi chú cũ trước và kiểm tra lại tiêu chí.

Mẫu yêu cầu: “Triển khai Phase 00 của Agent Corporation theo docs/master-plan.md. Chỉ làm phase này; cập nhật evidence và HTML, báo cáo để tôi nghiệm thu rồi dừng, chưa sang phase tiếp.” Nếu dependency chưa xong, agent trình bày điều còn thiếu và chờ quyết định, không âm thầm vượt phase.

Sau mỗi phase: cập nhật trạng thái, ngày, phạm vi thực tế, phần mới, files/commit nếu có, demo URL đã kiểm chứng, lệnh test + kết quả, evidence/artifacts, blocker/known limits và quyết định của Chủ tịch trong Markdown; render HTML cùng thay đổi. Không ghi phase Hoàn tất khi chỉ có giao diện hoặc checklist cá nhân.

## 7. Danh sách phase chi tiết

### Phase 00 — Chốt đặc tả V1

- Mốc: A
- Trạng thái: Hoàn tất
- Phụ thuộc: Không có
- Mục tiêu: Biến hai bản ý tưởng thành hợp đồng sản phẩm có thể nghiệm thu.

#### Phạm vi

- Chốt Chairman Mode, Operator Mode, 3 tầng quan sát và các luồng chính.
- Chốt ranh giới V1, stack đề xuất, trạng thái Work Order/run và hợp đồng event.
- Chốt các điểm còn mở: codex-server contract/version, authentication, ngân sách demo và môi trường sandbox.

#### Có gì mới

- Đã bàn giao đặc tả V1: 14 màn hình, 26 yêu cầu truy ra phase, 8 luồng và hợp đồng Work Order/task/run/30 event types; bản 1.1 làm rõ lifetime accepted-task cost và period operating cost.
- Đã soạn ADR D01–D08 và O01–O07 có owner/deadline; HTML mô phỏng 7 bước, CG01 contingency, IG03/08/12/16/20; grant riêng theo đợt/phase, hiện vẫn 0.

#### Demo

Mở docs/product-spec.html, chọn từng bước trong demo đặc tả F01: Work Order → plan → approval → worker/tools → review → bàn giao → Chủ tịch nghiệm thu. Đây là mô phỏng logic bằng dữ liệu đặc tả, chưa gọi model/tool.

#### Nghiệm thu

- Từng yêu cầu cốt lõi truy ra phase và tiêu chí nghiệm thu.
- Không còn điểm mở có thể làm sai thiết kế Phase 01–03; ghi rõ giả định được chấp nhận.
- Chủ tịch chốt phạm vi V1 và cơ chế chạy thử có inference.

#### Bàn giao

Đã bàn giao docs/product-spec.md + .html, docs/decisions/0001-v1-foundation.md + .html, docs/evidence/phase-00.md; scripts/render_phase00.py và scripts/validate_phase00.py chỉ phục vụ tài liệu.

#### Giới hạn

Không tạo UI sản phẩm, không gọi inference.

#### Bằng chứng cần có

Evidence tại docs/evidence/phase-00.md: dependency Không có; 26 requirements/14 screens/8 flows/30 events/R1–R8; gateway source hashes + GET health 200; checks tài liệu/links/examples/MD–HTML/syntax/phạm vi. Không có runtime/E2E tests hay inference.

#### Nhật ký triển khai

08/10/2026 — Bản 1.1 đã đáp ứng bốn điều chỉnh review: lifetime cost theo cohort accepted tách period cost; CG01 decision gate; IG03/08/12/16/20; grants riêng từng phase/test batch không kế thừa. Validation tài liệu/định nghĩa/references/JSON/links/MD–HTML/syntax/phạm vi đạt. Theo chỉ dẫn Chủ tịch, Phase 00 Hoàn tất về đặc tả/baseline. Không cấp grant, không gọi model, không bắt đầu Phase 01.

Lịch sử bàn giao bản 1.0 (trước nghiệm thu): 08/10/2026 — Đã triển khai phần đặc tả của Phase 00. Chọn baseline React/TS/Vite + FastAPI/Pydantic + PostgreSQL/SQLAlchemy/Alembic; PG jobs/state/events/outbox; gateway HTTP stateless; Owner local, scope/RLS và grants mặc định đóng. Bản bàn giao có phạm vi/screens/flows/state/events/authority/resource limits/traceability/release criteria. Validation tài liệu được ghi trong evidence. Trạng thái Chờ nghiệm thu; chưa có quyết định của Chủ tịch, chưa cấp grant test, chưa triển khai Phase 01. Không commit/push hoặc thay gateway/Dev Hub. Review Chủ tịch yêu cầu bốn làm rõ trong bản 1.1; kiểm tra nhất quán trước chốt nghiệm thu, không đổi baseline hoặc triển khai phase tiếp.

#### Tài liệu liên quan

- [Đặc tả V1 trực quan](product-spec.html)
- [Nguồn đặc tả Markdown](product-spec.md)
- [Quyết định kiến trúc](decisions/0001-v1-foundation.html)
- [Bằng chứng Phase 00](evidence/phase-00.md)

### Phase 01 — Dựng nền phát triển local

- Mốc: A
- Trạng thái: Hoàn tất
- Phụ thuộc: 00
- Mục tiêu: Có một môi trường phát triển khởi động và kiểm tra được.

#### Phạm vi

- Tạo repo và cấu trúc frontend/backend sau khi được yêu cầu triển khai.
- Cấu hình React + TypeScript, FastAPI + Pydantic, PostgreSQL; Compose cho hạ tầng, codex-server hiện có chạy độc lập trên host, kết nối server-to-server.
- Đọc lại Dev Hub, reserve và kiểm tra port block; env mẫu, health check, migration baseline, lệnh vận hành.

#### Có gì mới

- Trang kiểm tra sức khỏe frontend/backend/database.
- Mở ứng dụng local qua URL đã xác minh và xem lỗi kết nối rõ ràng.

#### Demo

Khởi động từ hướng dẫn trên môi trường sạch; tắt database và xem health báo lỗi đúng.

#### Nghiệm thu

- Lệnh cài/chạy/check hoạt động thực tế, không cần secret trong Git.
- Service mapping khớp registry; toàn block đã kiểm tra trước khi reserve.
- URL loopback/proxy chỉ báo hoạt động sau kiểm tra HTTP IPv4/IPv6 và browser.

#### Bàn giao

Ứng dụng skeleton, cấu hình local, README vận hành; chưa có runtime agent.

#### Giới hạn

Không triển khai production, không tự cài global/system service.

#### Bằng chứng cần có

Log khởi động, health responses, lệnh kiểm tra và registry diff.

#### Nhật ký triển khai

08/10/2026 — Đã tạo Vite/React/TypeScript frontend, FastAPI/Pydantic API, Compose PostgreSQL 18.6, secret local mode 0600, liveness/readiness, health page tiếng Việt và migration Alembic baseline không có domain tables. Dev Hub reserve `agent-corporation`, block `15500–15599`: web `127.0.0.1:15500`, API `127.0.0.1:15501`, PostgreSQL `127.0.0.1:15510 → 5432`; proxy route tắt vì ingress chung publish wildcard. Dependency pins ở package-lock/uv.lock/image digest. Log, migration, API tests, build, HTTP/browser và database-down evidence tại [Phase 01](evidence/phase-01.md). Chủ tịch duyệt Phase 01 ngày 08/10/2026; chưa seed dữ liệu, worker/agent, domain schema hoặc inference; grant = 0.

#### Tài liệu liên quan

- [Hướng dẫn chạy local](../README.md)
- [Bằng chứng Phase 01](evidence/phase-01.md)
Runtime local sau khi khởi động: web `127.0.0.1:15500`, API `127.0.0.1:15501`.

### Phase 02 — Khung giao diện Chủ tịch

- Mốc: A
- Trạng thái: Hoàn tất
- Phụ thuộc: 01
- Mục tiêu: Có không gian điều hành 2D nhất quán và dễ dùng.

#### Phạm vi

- Design system, navigation, trang dashboard và hai chế độ Chủ tịch/Vận hành.
- Empty/loading/error states, layout responsive, bàn phím và focus.
- Phác khung Live Office, Inspector, task, phê duyệt, tài chính, tổ chức.

#### Có gì mới

- Điều hướng các khu vực sản phẩm bằng giao diện tiếng Việt.
- Nhìn thấy trạng thái trống đúng; mọi preview ghi rõ chưa có dữ liệu và không tạo fixture.

#### Demo

Đi từ dashboard vào task và inspector shell ở desktop/mobile; xem khi API lỗi. Dùng CSS breakpoint 390 px để xác minh không tràn ngang.

#### Nghiệm thu

- Không có số giả trình bày như dữ liệu thật.
- Luồng điều hướng chính dùng được bằng bàn phím, lang vi và favicon đúng.
- Không tràn ngang ở 390 px; desktop giữ thứ bậc nội dung rõ.

#### Bàn giao

Design tokens, component cơ bản, các màn hình khung.

#### Giới hạn

Chưa có agent đang hoạt động; không dựng hoạt cảnh giả.

#### Bằng chứng cần có

Ảnh desktop/mobile, kiểm tra accessibility và các trạng thái.

#### Nhật ký triển khai

08/10/2026 — Phase 02 được hoàn tất khi Chủ tịch trực tiếp yêu cầu tiếp tục sang Phase 03; đây là chỉ thị chuyển tiếp được dùng để tiếp nhận dependency. Web build/lint, desktop navigation, mode Owner, trạng thái API lỗi/phục hồi, S13 và S14 đã được kiểm tra trong lượt trước. CSS breakpoint 390 px vẫn là giới hạn chưa xác minh trực tiếp viewport; xem [bằng chứng Phase 02](evidence/phase-02.md). Không có model request; inference grant = 0.

#### Tài liệu liên quan

- [Bằng chứng Phase 02](evidence/phase-02.md)
- Runtime local đã kiểm tra: `http://127.0.0.1:15500/`.

### Phase 03 — Dữ liệu và bằng chứng bền vững

- Mốc: A
- Trạng thái: Hoàn tất
- Phụ thuộc: 01, 02
- Mục tiêu: Dữ liệu công ty, công việc và event sống qua restart.

#### Phạm vi

- Schema company/environment, department, employee_version, Work Order, run, approval, policy và artifacts.
- Event store ngay từ đầu: company/task/run/agent IDs, occurred/received time, correlation/parent, sequence, sensitivity và dedup key.
- Execution state độc lập event; transaction/outbox, checkpoints, migration, isolation và chỉ mục theo đường truy vấn.

#### Có gì mới

- Schema PostgreSQL cho environment/company, departments/employees/version, policies, Work Orders/revisions/state, runs/checkpoints/approvals, artifacts, events và transactional outbox.
- Task command ghi revision + state + event + outbox nguyên tử; state machine kiểm tra chuyển trạng thái/version, dedup theo company stream; app role bị giới hạn và RLS lọc chéo company.
- Giao diện có dark mode lưu lựa chọn local và mặc định theo system preference; hostname `agent-corporation.localhost` được proxy loopback IPv4 tới web.

#### Demo

Tạo task demo bằng fixture, restart backend, đối chiếu task, run và event vẫn còn.

#### Nghiệm thu

- Chuyển trạng thái sai bị từ chối; event và state không lệch do transaction thất bại.
- Query khác company/environment không đọc được dữ liệu ngoài phạm vi.
- Event trùng không nhân đôi; secret thử nghiệm được lọc trước persistence.

#### Bàn giao

Schema/migrations, hợp đồng event và state machine v1.

#### Giới hạn

Chưa streaming live; không đợi Phase 07 mới tạo event store.

#### Bằng chứng cần có

Schema diagram, migration test, isolation/state/outbox test.

#### Nhật ký triển khai

08/10/2026 — Phase 03 được Chủ tịch nghiệm thu ngày 08/10/2026 (“ok duyệt” trước chỉ thị Phase 04). Migration `20261008_0002` áp dụng; 17 bảng domain/evidence, app login role không privileged + forced RLS, Work Order/state/event/outbox command và redaction đã được kiểm tra bằng PostgreSQL integration tests (8/8). API restart/readiness đạt; web lint/build Node 24.21.0 đạt. Dark mode hoạt động theo lựa chọn local/system preference. Proxy `agent-corporation.localhost` trả 200 qua IPv4 loopback; IPv6 Docker bind bị từ chối, không mở rộng wildcard. Chi tiết lệnh/test/giới hạn ở [evidence Phase 03](evidence/phase-03.md). Không gọi codex-server/inference, grant = 0.

#### Tài liệu liên quan

- [Bằng chứng Phase 03](evidence/phase-03.md)

### Phase 04 — Nhà máy công ty demo

- Mốc: A
- Trạng thái: Chờ nghiệm thu
- Phụ thuộc: 03
- Mục tiêu: Có môi trường mẫu có thể tạo và reset an toàn.

#### Phạm vi

- Sinh công ty giả, phòng ban, nhân viên version hóa và event fixture deterministic.
- Tách demo/benchmark/real bằng khóa môi trường, storage paths và thread namespaces; real còn trống.
- Dataset cho idle/running/waiting/failed, approvals, lỗi, retry và usage chưa biết.

#### Có gì mới

- Dashboard, công việc, approval, Inspector và finance đọc cùng fixture demo có nhãn; usage/chi phí unknown vẫn hiện là chưa biết.
- Reset chỉ nhận xác nhận, không nhận environment/company từ client và chỉ tác động UUID demo cố định.
- Seed v1 tạo phòng ban, hồ sơ nhân sự version hóa, state/run/approval/artifact metadata và event fixture deterministic; không mở runtime agent.

#### Demo

Reset demo hai lần, đối chiếu dataset ổn định và một bản ghi real thử nghiệm không thay đổi.

#### Nghiệm thu

- Fixture có seed/version; không gọi model khi seed/reset.
- Reset không xóa artifacts, ledger hoặc thread của môi trường khác.
- Dashboard/Inspector/finance không trộn demo vào báo cáo real.

#### Bàn giao

Demo factory, fixtures và quy trình reset.

#### Giới hạn

Không thành lập tập đoàn thật của người dùng.

#### Bằng chứng cần có

Seed manifest, kiểm tra reset/isolation và ảnh nhãn demo.

#### Nhật ký triển khai

08/10/2026 — Triển khai và bàn giao Phase 04 chờ Chủ tịch nghiệm thu. Migration `20261008_0003` thêm hàm reset SECURITY DEFINER chỉ cho app role và scope demo cố định; seed tường minh tạo 2 phòng ban, 3 hồ sơ nhân sự v1, 5 Work Order ở các trạng thái fixture, approval, artifact metadata và 20 events; reset lặp cho cùng manifest hash. API `GET /api/v1/demo/dashboard` và `POST /api/v1/demo/reset` không nhận target scope; UI gắn nhãn demo xuyên các màn hình, yêu cầu xác nhận reset và không biến usage unknown thành 0. Alembic 0003, 7 API integration tests, web lint/build và API HTTP reset 2 lần đạt; không có inference request/grant. Checklist Phase 04 ghi blocker bằng chứng cho ledger/thread/file storage vì các domain này chưa tồn tại trong dependency hiện tại; xem [bằng chứng Phase 04](evidence/phase-04.md) và [report batch](tests/results/phase-04/20261008T154151+0700-demo-factory/report.md). Phase 04 chưa đánh dấu Hoàn tất; tại thời điểm bàn giao này Phase 05 chưa bắt đầu.

#### Tài liệu liên quan

- [Bằng chứng Phase 04](evidence/phase-04.md)
- [Report kiểm định Phase 04](tests/results/phase-04/20261008T154151+0700-demo-factory/report.md)

### Phase 05 — Kết nối Codex server local

- Mốc: B
- Trạng thái: Chờ nghiệm thu
- Phụ thuộc: 03, 04
- Mục tiêu: Sản phẩm nhận biết Codex khả dụng và model được chọn.

#### Phạm vi

- Adapter HTTP tới codex-server hiện có; base URL cấu hình, contract/capability probe, auth ref và secret redaction.
- Tách role/persona, model/tools/skills, policy; xác thực lựa chọn model thực thay vì hardcode nhãn GPT-6.1 Sol High.
- Health/auth status, profile config tối thiểu, owner-only model config; adapter giả cho lỗi và test miễn phí.

#### Có gì mới

- Màn hình kết nối server local, trạng thái và model/profile được cấu hình.
- Hiển thị lỗi version/auth/model không hỗ trợ và hành động khắc phục.

#### Demo

GET health/models không inference; mô phỏng server offline, 401 và schema/capability mismatch.

#### Nghiệm thu

- Health/models API hoạt động; contract từ source gateway được xác nhận, không log token hay đưa secret ra UI.
- Catalog model không chứng minh entitlement; lượt chạy thật kiểm tra ở Phase 06.
- Không đổi cấu hình server chung; fallback chỉ trong danh sách đã được Chủ tịch duyệt; 429 được đưa lại queue.

#### Bàn giao

HTTP gateway adapter, probe và capability matrix theo source/API hiện có.

#### Giới hạn

Chưa bắt đầu turn có inference; nếu dùng gateway khác phải chốt adapter riêng.

#### Bằng chứng cần có

Contract/schema, health/models responses đã lọc, lỗi probe và profile snapshot.

#### Nhật ký triển khai

08/10/2026 — Theo chỉ thị Chủ tịch sau remediation report Phase 01, triển khai adapter probe read-only và màn hình Settings để probe thủ công. Adapter chỉ cho HTTP literal loopback, chỉ GET `/health` + `/v1/models`, chặn redirect/proxy môi trường, timeout và response quá lớn; API chỉ trả trạng thái/model ID đã lọc, không trả secret hoặc khẳng định entitlement. Startup/health/profile không tự probe; không có POST chat/session hoặc inference. Codex server ở `127.0.0.1:4000` không nghe tại thời điểm kiểm chứng, nên live probe trả offline; API tests (9), web lint/build đều pass. Phần owner-authenticated model profile bị chặn vì API hiện chưa có identity/auth đáng tin; durable 429 queue/fallback allowlist chưa có persistence/Owner policy và thuộc capability chưa có ở phase này. CG01 bị chặn: source gateway xác nhận sandbox read-only không cô lập quyền đọc file máy, stateless chat vẫn tạo Codex thread/rollout có thể lưu prompt; không gửi input và không sửa server chung. Phase 04 vẫn Chờ nghiệm thu với khoảng trống isolation ledger/thread/file store và screenshot; Chủ tịch đã chỉ thị tiếp tục Phase 05, không thay trạng thái Phase 04. Xem [bằng chứng Phase 05](evidence/phase-05.md) và [report kiểm định](tests/results/phase-05/20261008T161028+0700-phase05-probe/report.md). Grant = 0; Phase 06 chưa bắt đầu.

#### Tài liệu liên quan

- [Bằng chứng Phase 05](evidence/phase-05.md)
- [Report kiểm định Phase 05](tests/results/phase-05/20261008T161028+0700-phase05-probe/report.md)

### Phase 06 — Agent đầu tiên chạy trong sandbox

- Mốc: B
- Trạng thái: Bị chặn
- Phụ thuộc: 05; nền event/state của 03
- Mục tiêu: Một agent thử nghiệm thực hiện nhiệm vụ thật có giới hạn.

#### Phạm vi

- Runtime do app quản lý vòng request/response; map X-Codex-Call-Id tới run, history/checkpoint, profile/policy snapshot và kết quả có cấu trúc.
- Trước request đầu: default deny, inference isolation được kiểm chứng, hạn mức lượt/thời gian/concurrency, quan sát usage cuối lượt và abort tối thiểu; tools chưa bật.
- Ghi event + usage nguồn gốc; xin hạn mức test được Chủ tịch cấp, không tự chạy inference từ UI mở trang.

#### Có gì mới

- Nút chạy nhiệm vụ demo, trạng thái thực thi và kết quả từ agent thật.
- Giới hạn chạy và nút dừng; không tạo nhân viên/công ty thật.

#### Demo

Agent demo xử lý một nhiệm vụ phân tích văn bản nhỏ; thử timeout, từ chối thao tác ngoài scope và dừng đang chạy.

#### Nghiệm thu

- Có request model thật hoàn tất với evidence; lỗi/aborted không hiển thị thành công.
- Sandbox/policy kiểm tra hành vi thực; không thừa hưởng quyền unrestricted của phiên Codex hiện tại.
- Hết hạn mức thì chặn request mới; thiếu usage/cost ghi chưa biết; không cam kết chặn token giữa request khi gateway chưa hỗ trợ.

#### Bàn giao

Single-agent runtime, baseline policy/budget/stop và một run demo thật.

#### Giới hạn

Không tool mở rộng hay đa agent; USD hard cap chỉ cam kết khi biết pricing và có reservation bảo thủ.

#### Bằng chứng cần có

Trace thật đã lọc, artifact, timeout/deny/abort test, usage provenance.

#### Nhật ký triển khai

08/10/2026 — Theo yêu cầu Chủ tịch tiếp Phase 06 sau khi làm lại test Phase 05, đã kiểm dependency trước khi triển khai. Phase 05 chưa được nghiệm thu: report r002 kết luận chưa đủ bằng chứng, live gateway offline, Owner auth/profile, durable queue/fallback và CG01 còn blocked; Phase 04 cũng Chờ nghiệm thu. CG01 chưa chứng minh isolation/read boundary và retention, inference grant = 0; backend hiện có run/checkpoint/events nền nhưng chưa có authenticated Owner grant/reservation hoặc ModelCall ledger/dispatcher. Vì vậy dừng trước khi thêm dispatcher/migration/API và trước khi gửi input; không gọi model, không restart shared gateway/API, không tự chọn instance thay thế. API health/gateway unit tests (9) pass; đây không thay bằng chứng Phase 06. Xem [report preflight Phase 06](tests/results/phase-06/20261008T170343+0700-r001-test/report.md). Điều kiện tiếp tục: dependency/gates được xử lý theo quyết định Chủ tịch, CG01 được chứng minh, và inference chỉ khi có grant riêng đúng test batch/mục đích/hạn mức/expiry.

### Phase 07 — Luồng event và khôi phục kết nối

- Mốc: B
- Trạng thái: Chưa triển khai
- Phụ thuộc: 06
- Mục tiêu: Tiến độ thực được stream từ dữ liệu đã lưu.

#### Phạm vi

- HTTP request/response + tool/orchestration events của app → domain events, lưu trước phát; SSE backend → UI theo cursor.
- Ordering/dedup/reconnect, heartbeat và dấu thời điểm dữ liệu cập nhật.
- Checkpoint reconciliation khi worker/server chết; lease và idempotency tránh chạy lại side effect chưa biết kết quả.

#### Có gì mới

- Task/agent cập nhật live, phân biệt đang chạy và đã mất kết nối.
- Reload trang không mất lịch sử tiến độ.

#### Demo

Chạy task thật, ngắt UI stream, reconnect rồi đối chiếu cùng event count; restart worker ở giữa run.

#### Nghiệm thu

- Event đã lưu có thể fetch lại đúng sequence, không nhân đôi sau reconnect.
- Không báo đang hoạt động sau mất heartbeat; model đang chờ chỉ có trạng thái waiting, không bịa tiến độ/token nội bộ; unknown outcome cần reconciliation.
- Crash không tạo model request/tool mới trùng; session invalidated/expired cần khôi phục từ context app; gap nguồn được hiển thị rõ.

#### Bàn giao

Durable stream và cơ chế reconcile trạng thái.

#### Giới hạn

Replay UI ở Phase 08; không hứa exactly-once cho hệ thống ngoài.

#### Bằng chứng cần có

Log reconnect/crash, event IDs và state sau phục hồi.

#### Nhật ký triển khai

Chưa có triển khai, kết quả kiểm thử hay quyết định nghiệm thu.

### Phase 08 — Live Office và Agent Inspector

- Mốc: B
- Trạng thái: Chưa triển khai
- Phụ thuộc: 07
- Mục tiêu: Nhìn được agent đang làm gì và xem lại run đã chạy.

#### Phạm vi

- Live Office 2D theo phòng ban; trạng thái idle/running/waiting/failed dựa vào event.
- Inspector mở từ dashboard/agent/task/org: Plan, tóm tắt quyết định, tools, file diff, messages, lỗi, model/profile và metrics.
- Replay timeline theo event/checkpoint đã ghi; filter task/agent/run và redaction theo quyền.

#### Có gì mới

- Click agent để theo dõi trực tiếp nhiệm vụ và bằng chứng.
- Kéo timeline xem lại từng bước, lỗi và chuyển giao; usage xác nhận/ước tính/chưa biết rõ.

#### Demo

Mở run thật Phase 06–07, lọc task, xem lỗi, kéo replay và reload; đối chiếu với event store.

#### Nghiệm thu

- Luồng trên UI đến từ run thật; fixture chỉ dùng test UI và có nhãn.
- Replay không gọi model/tool, không sửa trạng thái và không tạo tác dụng phụ.
- Không hiển thị tóm tắt quyết định như suy nghĩ nội bộ nguyên văn; prompt lưu theo policy.

#### Bàn giao

Observatory, Inspector và Replay v1.

#### Giới hạn

Chưa có văn phòng 3D; timeline không bịa dữ liệu thiếu.

#### Bằng chứng cần có

Video/ảnh demo thật, event correlation và kiểm tra replay/redaction.

#### Nhật ký triển khai

Chưa có triển khai, kết quả kiểm thử hay quyết định nghiệm thu.

### Phase 09 — Bảng nhiệm vụ và hàng đợi

- Mốc: B
- Trạng thái: Chưa triển khai
- Phụ thuộc: 08
- Mục tiêu: Quản lý toàn bộ vòng đời công việc có thể tiếp tục an toàn.

#### Phạm vi

- Work Order gồm mục tiêu, đầu ra, acceptance, quyền, deadline, budget, điểm dừng và assignee.
- Queue bền vững, ưu tiên, concurrency/lease, states blocked/awaiting approval/quality/rework/accepted.
- Pause ngăn bước mới; abort HTTP request đang chạy khi cần; resume từ checkpoint xác minh, retry có attempt mới và idempotency.

#### Có gì mới

- Tạo/giao/lọc task, nhìn queue và biết ai đang chặn ai.
- Tạm dừng, tiếp tục, thử lại, hủy và yêu cầu sửa với lịch sử rõ.

#### Demo

Đưa hai task vào queue, pause một task, restart worker, resume rồi retry lỗi an toàn.

#### Nghiệm thu

- Hai worker không nhận cùng lease; quá concurrency không tạo run thêm.
- UI không hứa resume giữa suy luận/token; trạng thái pause/interrupted/checkpoint thể hiện đúng.
- Accepted do nghiệm thu, không suy ra từ turn completed; rework giữ evidence cũ.

#### Bàn giao

Task board, queue và lifecycle đầy đủ.

#### Giới hạn

Không áp đặt gọi đủ Architect/QA cho mọi task nhỏ.

#### Bằng chứng cần có

Queue/lease/crash tests và state transition evidence.

#### Nhật ký triển khai

Chưa có triển khai, kết quả kiểm thử hay quyết định nghiệm thu.

### Phase 10 — Quyền hạn và hộp phê duyệt

- Mốc: B
- Trạng thái: Chưa triển khai
- Phụ thuộc: 09; baseline đã có ở 06
- Mục tiêu: Chủ tịch kiểm soát hành động vượt thẩm quyền.

#### Phạm vi

- Ba cấp: tự động trong scope, ủy quyền có hạn, Chủ tịch duyệt; backend và executor cùng cưỡng chế.
- Approval gắn action/payload hash/company/run, policy version, expiry, budget; deny stale/replay/cross-scope.
- Secrets references, audit owner-only configuration; policy không cho agent tự cấp quyền.

#### Có gì mới

- Inbox phê duyệt có tác động, lý do, bằng chứng; duyệt/từ chối đúng hành động.
- Xem lịch sử thay đổi quyền/model/ngân sách và các lần bị chặn.

#### Demo

Agent đề xuất tăng quyền, duyệt một payload rồi thay payload để chứng minh approval cũ không dùng lại.

#### Nghiệm thu

- Bypass API/tool vẫn bị chặn; agent không tự đổi policy/model/budget.
- Approval khác run/company hoặc hết hạn bị từ chối; deny không tạo side effect.
- Owner-only config và secret redaction đã được kiểm tra ở lớp thực thi.

#### Bàn giao

Permission engine, approval inbox và audit log.

#### Giới hạn

Không mở quyền mới trước gate này; external send/deploy/destructive vẫn cần Chủ tịch duyệt.

#### Bằng chứng cần có

Bypass/replay/stale tests và audit trail.

#### Nhật ký triển khai

Chưa có triển khai, kết quả kiểm thử hay quyết định nghiệm thu.

### Phase 11 — Hệ thống công cụ thực thi

- Mốc: C
- Trạng thái: Chưa triển khai
- Phụ thuộc: 10
- Mục tiêu: Agent có thể làm việc thật trong workspace đã cấp.

#### Phạm vi

- Tool registry/schema/version cho files, code, terminal, browser; adapter và capability allowlist.
- Workspace/container sandbox theo task, network egress allowlist, timeout/output caps, artifact/file diff capture.
- Approval trước side effects; receipt/idempotency cho hành động bên ngoài và kết quả chưa xác định.

#### Có gì mới

- Theo dõi lệnh, tool input/output đã lọc, file thay đổi và kết quả test trong Inspector.
- Nhận artifact mở được từ một nhiệm vụ lập trình nhỏ.

#### Demo

Agent sửa file trong sandbox, chạy test, đọc trang được cho phép; thử path traversal và command ngoài scope.

#### Nghiệm thu

- Không truy file/secret ngoài workspace; network/tool ngoài allowlist bị chặn ở executor.
- Run thật có diff, test exit code và artifact; redaction không làm mất correlation.
- Retry không lặp hành động có side effect khi chưa có kết quả xác định.

#### Bàn giao

Tool adapters v1 và sandbox execution.

#### Giới hạn

Không gửi email/deploy production tự động; không tắt sandbox để vượt test.

#### Bằng chứng cần có

Tool receipts, diff/test log, negative tests về file/network.

#### Nhật ký triển khai

Chưa có triển khai, kết quả kiểm thử hay quyết định nghiệm thu.

### Phase 12 — Điều phối nhiều nhân viên

- Mốc: C
- Trạng thái: Chưa triển khai
- Phụ thuộc: 11
- Mục tiêu: Một mục tiêu đi qua người lập kế hoạch, thực hiện và kiểm tra.

#### Phạm vi

- Supervisor/Chief of Staff, worker, reviewer; routing deterministic cho việc nhỏ.
- Subtasks/DAG, handoff contract, messages và parent/correlation IDs; giới hạn fan-out/depth/iterations.
- Shared budget reservation và hủy propagation; review/rework có bằng chứng trước human acceptance.

#### Có gì mới

- Sơ đồ giao việc, phụ thuộc và chuyển giao hiển thị trên task/Live Office.
- Báo cáo tổng hợp liên kết kết quả của từng nhân viên.

#### Demo

Công ty demo có Chief of Staff → worker → reviewer sửa một app nhỏ; reviewer yêu cầu sửa một lần.

#### Nghiệm thu

- Task nhỏ không tự triệu tập cả phòng; không loop delegation vô hạn.
- Ngân sách tổng không bị vượt do các worker reserve đồng thời; dừng cha chặn bước mới của con.
- Chủ tịch thấy đủ evidence của từng handoff và quyết định nghiệm thu.

#### Bàn giao

Orchestrator và quy trình demo đa agent end-to-end.

#### Giới hạn

Agent chỉ thực thi trong scope; thêm nhân viên thử nghiệm không phải tuyển chính thức.

#### Bằng chứng cần có

Trace DAG, quality/rework evidence và cancellation/budget race tests.

#### Nhật ký triển khai

Chưa có triển khai, kết quả kiểm thử hay quyết định nghiệm thu.

### Phase 13 — Tổ chức và hồ sơ nhân viên

- Mốc: C
- Trạng thái: Chưa triển khai
- Phụ thuộc: 12
- Mục tiêu: Quản lý tập đoàn như một tổ chức có trách nhiệm.

#### Phạm vi

- Organization chart, department, reporting line; permanent/on-demand/contractor với trạng thái thật.
- Employee version lưu role/persona, model + reasoning, tools/skills, context và policy refs.
- Inspector dùng chung mọi nơi; xem workload và hiệu suất gắn đúng profile version.

#### Có gì mới

- Sơ đồ phòng ban, danh sách nhân viên và hồ sơ có lịch sử phiên bản.
- Xem ai chịu trách nhiệm, đang nhận task nào và profile nào đã chạy.

#### Demo

Đổi profile demo bằng quyền Chủ tịch; run cũ vẫn hiển thị version cũ, run mới dùng version mới.

#### Nghiệm thu

- Hồ sơ idle không tạo tiến trình/inference liên tục.
- Model/profile thay đổi qua owner-only; không mutate snapshot của run đang chạy; gateway session cố định model/effort phải đổi session nếu dùng.
- Org chart không có chu kỳ; xóa/chuyển phòng vẫn giữ lịch sử và evidence.

#### Bàn giao

Organization UI và versioned employee profiles.

#### Giới hạn

Không tự bổ nhiệm CEO; Chief of Staff là vị trí đầu tiên khi vận hành thật.

#### Bằng chứng cần có

Version comparison, run snapshots và org integrity tests.

#### Nhật ký triển khai

Chưa có triển khai, kết quả kiểm thử hay quyết định nghiệm thu.

### Phase 14 — Tuyển dụng và thử việc

- Mốc: C
- Trạng thái: Chưa triển khai
- Phụ thuộc: 13
- Mục tiêu: AI đề xuất nhân sự, Chủ tịch quyết định.

#### Phạm vi

- HR proposal: nhu cầu, loại hợp đồng, model/tools, dự toán, probation và tiêu chí giữ lại.
- Approve/reject/offboard; thu hồi quyền và stop/drain các run trước chuyển trạng thái.
- Lưu assessment thử việc; benchmark tự động nâng cấp ở Phase 17, giai đoạn này dùng evidence suite cố định.

#### Có gì mới

- Inbox tuyển dụng, thử việc, thay đổi hình thức nhân sự và nghỉ việc.
- Xem lý do, tác động chi phí và kết quả kiểm tra trước quyết định.

#### Demo

Đề xuất QA on-demand, từ chối một lần rồi duyệt proposal mới; offboard khi còn task đang chạy.

#### Nghiệm thu

- Agent không tự tuyển/sa thải nhân viên cố định hoặc mở quyền.
- Offboard chặn run mới, xử lý run hiện tại và không mất lịch sử.
- Đánh giá theo chất lượng/nhu cầu/chi phí biên, không xem token tiêu thụ là năng suất.

#### Bàn giao

HR lifecycle, proposal và probation v1.

#### Giới hạn

Không tự kết luận specialist vô ích vì tháng này idle.

#### Bằng chứng cần có

Proposal audit, probation evidence và offboard test.

#### Nhật ký triển khai

Chưa có triển khai, kết quả kiểm thử hay quyết định nghiệm thu.

### Phase 15 — Context và trí nhớ có kiểm chứng

- Mốc: C
- Trạng thái: Chưa triển khai
- Phụ thuộc: 14
- Mục tiêu: Tổ chức tích lũy bài học đúng người, đúng phạm vi.

#### Phạm vi

- Năm lớp corporate/department/employee/task/working; ACL và context budget, provenance, redaction/retention.
- Promotion: bài học → evidence → đề xuất → reviewer/Chủ tịch duyệt → version; rollback/expiry.
- Task context selection và chống đưa tài liệu không tin cậy thành policy.

#### Có gì mới

- Xem context được cấp, nguồn kiến thức và lịch sử memory.
- Duyệt bài học có bằng chứng để run sau tái sử dụng.

#### Demo

Một worker đề xuất bài học, reviewer duyệt, run kế tiếp dùng đúng version; agent phòng khác bị từ chối.

#### Nghiệm thu

- Retrieval và promotion cùng kiểm tra company/environment/ACL ở backend.
- Run snapshot truy được nguồn/version; rollback không sửa lịch sử.
- Không nhồi toàn bộ chat lịch sử; dữ liệu không tin cậy không ghi đè quyền.

#### Bàn giao

Memory store, context builder và promotion inbox.

#### Giới hạn

Không tự coi lời agent nói là fact đã được xác minh.

#### Bằng chứng cần có

Context manifest, promotion/rollback/isolation tests.

#### Nhật ký triển khai

Chưa có triển khai, kết quả kiểm thử hay quyết định nghiệm thu.

### Phase 16 — Tài chính và ngân sách

- Mốc: D
- Trạng thái: Chưa triển khai
- Phụ thuộc: 15; usage + limits có từ 06
- Mục tiêu: Biết đã tiêu gì, cho ai và với độ chính xác nào.

#### Phạm vi

- Ledger Company → Department → Employee → Task → Model → call/span quan sát được; reconcile và dedup usage cumulative.
- Pricing versions tại thời điểm gọi; reserve/settle/release concurrent budgets theo task/day/month.
- API trả thực, subscription, local compute và ước tính điện tách riêng; thiếu usage/giá ghi unknown.

#### Có gì mới

- Dashboard tài chính và truy từ số tổng đến bằng chứng nguồn.
- Xem chi phí/task được nghiệm thu, rework, ngân sách còn lại và cảnh báo vượt hạn mức.

#### Demo

Chạy hai task demo, một retry; so ledger với usage nguồn và bật filter môi trường.

#### Nghiệm thu

- Không đếm trùng cumulative usage sau reconnect/retry; pricing snapshot không bị giá mới sửa.
- Không lấy token × giá API để gọi đó là hóa đơn subscription; ước tính có nhãn.
- Chỉ hard cap USD khi dữ liệu/pricing cho phép; nếu thiếu dùng giới hạn tài nguyên đã duyệt và báo rõ.

#### Bàn giao

Cost ledger, budgets và finance dashboard.

#### Giới hạn

HTTP call/turn usage là mức đo hiện có; không bịa internal LLM call. Cost API-equivalent gateway chỉ tham khảo, không là hóa đơn ChatGPT.

#### Bằng chứng cần có

Reconciliation report, pricing/budget race tests và unknown cases.

#### Nhật ký triển khai

Chưa có triển khai, kết quả kiểm thử hay quyết định nghiệm thu.

### Phase 17 — Benchmark và chất lượng

- Mốc: D
- Trạng thái: Chưa triển khai
- Phụ thuộc: 16
- Mục tiêu: So sánh nhân viên/model trên cùng bài kiểm tra.

#### Phạm vi

- Versioned suite/dataset, evaluator deterministic ưu tiên; human review khi cần, blind evaluation.
- First-pass success, accepted-task cost, rework, P50/P95, human intervention; denominator/time window rõ.
- Model Tournament, cố định tools/context/budget, repeated runs và CI/regression; benchmark environment riêng.

#### Có gì mới

- Bảng so model/profile theo chất lượng, latency và chi phí.
- Chạy benchmark có hạn mức và xem artifact/test evidence từng bài.

#### Demo

So hai profile trên cùng suite; mở bài thất bại và đối chiếu điểm với test, không chỉ LLM judge.

#### Nghiệm thu

- Không trộn benchmark/demo vào KPI vận hành thật.
- Không công bố model thắng từ một sample thiếu cơ sở; ghi cỡ mẫu và uncertainty.
- Evaluator/fixtures có version, môi trường và constraints tái lập được.

#### Bàn giao

Benchmark harness, evaluator và quality dashboard.

#### Giới hạn

Không đổi model tự động sau tournament.

#### Bằng chứng cần có

Suite manifest, run/evaluation artifacts và regression comparisons.

#### Nhật ký triển khai

Chưa có triển khai, kết quả kiểm thử hay quyết định nghiệm thu.

### Phase 18 — Đề xuất tối ưu có thử nghiệm

- Mốc: D
- Trạng thái: Chưa triển khai
- Phụ thuộc: 17
- Mục tiêu: Cải thiện tổ chức bằng số liệu, có Chủ tịch kiểm soát.

#### Phạm vi

- Đề xuất routing/model/context/nhân sự từ ledger + benchmark; expected benefit và rủi ro.
- Shadow/A-B experiment trong môi trường riêng, hạn mức và acceptance rule trước thử.
- Owner approval, config version rollout/rollback; tránh thay đổi nhiều biến rồi gán nguyên nhân.

#### Có gì mới

- Inbox tối ưu có phương án hiện tại, đề xuất mới và evidence so sánh.
- Duyệt thử nghiệm, xem kết quả rồi chọn áp dụng hoặc giữ nguyên.

#### Demo

Đề xuất đổi model worker, chạy suite hiện tại/mới, Chủ tịch từ chối rồi kiểm tra cấu hình vẫn như cũ.

#### Nghiệm thu

- LLM không tự phát minh KPI hay tự áp cấu hình.
- Experiment không gọi external side effect thật và không trộn ledger real.
- Có snapshot trước/sau và rollback đã thử.

#### Bàn giao

Optimization proposals và experiment lab v1.

#### Giới hạn

Hội đồng điều hành nhiều agent chuyên sâu là mở rộng sau V1.

#### Bằng chứng cần có

Experiment report, approval audit và rollback evidence.

#### Nhật ký triển khai

Chưa có triển khai, kết quả kiểm thử hay quyết định nghiệm thu.

### Phase 19 — Sự cố và dừng khẩn cấp

- Mốc: D
- Trạng thái: Chưa triển khai
- Phụ thuộc: 18; stop tối thiểu đã có ở 06
- Mục tiêu: Cô lập run bất thường và phục hồi có bằng chứng.

#### Phạm vi

- Incident detection: loop, timeout, token burst, tool deny, stalled lease, server disconnect.
- Global Emergency Stop durable: chặn dispatch/request/tool mới, abort request và worker app đang chạy; không dừng codex-server chung hoặc run ứng dụng khác.
- Incident timeline, reconciliation, safe retry/manual intervention và recovery drill.

#### Có gì mới

- Trung tâm sự cố, cảnh báo và nút dừng toàn hệ thống.
- Xem hành động nào dừng được, đang chờ hoặc đã gửi ra ngoài.

#### Demo

Tạo loop demo và kill worker, bấm stop; restart hệ thống vẫn giữ stop cho tới Chủ tịch mở lại.

#### Nghiệm thu

- Stop không tự được gỡ sau restart; race dispatch/abort đã kiểm tra và gateway cancellation được xác minh.
- Không hứa hoàn tác hành động bên ngoài; unknown outcome được cô lập trước retry.
- Có incident report liên kết cause/evidence/recovery và run bị ảnh hưởng.

#### Bàn giao

Incident Command Center và recovery playbook.

#### Giới hạn

Không đợi phase này mới có timeout/stop; đây là mở rộng toàn hệ thống.

#### Bằng chứng cần có

Fault injection, stop race và recovery drill artifacts.

#### Nhật ký triển khai

Chưa có triển khai, kết quả kiểm thử hay quyết định nghiệm thu.

### Phase 20 — Lịch làm việc và báo cáo điều hành

- Mốc: D
- Trạng thái: Chưa triển khai
- Phụ thuộc: 19
- Mục tiêu: Có báo cáo ngày/tháng dựa trên việc đã chạy.

#### Phạm vi

- Persistent scheduler, timezone Asia/Ho_Chi_Minh, miss/sleep policy và idempotent job key.
- Morning brief, báo cáo bộ phận, CFO/quality summary và board review theo ledger/events.
- Proposal inbox hợp nhất; report generation theo nhu cầu, không gọi agent idle liên tục.

#### Có gì mới

- Lịch công việc, bản tin Chủ tịch và báo cáo tháng có liên kết bằng chứng.
- Phân biệt lịch dự kiến, lần chạy thực và việc bị lỡ khi máy ngủ.

#### Demo

Mô phỏng máy ngủ qua thời điểm báo cáo, mở lại và kiểm tra catch-up policy không chạy trùng.

#### Nghiệm thu

- Không báo nhân viên làm xuyên đêm khi server chưa chạy.
- Số trong báo cáo tính từ query/version/time window, AI chỉ tóm tắt.
- Scheduled inference nằm trong hạn mức; không tự sinh vô hạn báo cáo/họp.

#### Bàn giao

Scheduler và executive reports/inbox.

#### Giới hạn

Máy local tắt thì không có background execution thực.

#### Bằng chứng cần có

Scheduler resume/dedup tests và report reconciliation.

#### Nhật ký triển khai

Chưa có triển khai, kết quả kiểm thử hay quyết định nghiệm thu.

### Phase 21 — Wizard thành lập tập đoàn

- Mốc: E
- Trạng thái: Chưa triển khai
- Phụ thuộc: 20
- Mục tiêu: Chuẩn bị trải nghiệm tạo công ty thật sau release.

#### Phạm vi

- Wizard tên/biểu tượng/sứ mệnh/mục tiêu, autonomy, model connection, budget và policy preview.
- Bổ nhiệm duy nhất Chief of Staff (Ava hoặc tên Chủ tịch chọn); không tự tuyển thêm đội ngũ.
- Transactional onboarding/idempotency, riêng real storage và guarded release activation.

#### Có gì mới

- Trải nghiệm first-run tiếng Việt, kiểm tra cấu hình và xem quyền trước khi xác nhận.
- Sau xác nhận có dashboard trống đúng với một Chief of Staff.

#### Demo

Chạy toàn wizard trong môi trường nghiệm thu riêng, retry submit và quay lại sửa bước model.

#### Nghiệm thu

- Không tạo công ty thật của người dùng trong quá trình phát triển.
- Submit trùng không tạo hai công ty/nhân viên; lỗi rollback sạch.
- Đường real production onboarding vẫn khóa đến release gate Phase 23.

#### Bàn giao

Onboarding wizard hoàn chỉnh, chưa kích hoạt real vận hành.

#### Giới hạn

Không seed demo vào real; first-run không gọi inference âm thầm.

#### Bằng chứng cần có

Onboarding e2e trong test environment và transactional evidence.

#### Nhật ký triển khai

Chưa có triển khai, kết quả kiểm thử hay quyết định nghiệm thu.

### Phase 22 — Bảo vệ dữ liệu và khôi phục

- Mốc: E
- Trạng thái: Chưa triển khai
- Phụ thuộc: 21
- Mục tiêu: Đổi phiên bản hoặc lỗi máy vẫn giữ quyền và bằng chứng.

#### Phạm vi

- Audit auth/owner-only, local exposure/CORS, permission/tool escape, secret/log/prompt handling và retention.
- Backup/restore database + artifacts + config refs; secrets xử lý riêng; version-compatible migration/recovery.
- Crash recovery và restore drill có checkpoint/thread reconciliation, không tự replay side effects.

#### Có gì mới

- Trang backup/restore và tình trạng hệ thống, hướng dẫn khôi phục có kiểm tra.
- Biết bản sao nào dùng được và phạm vi dữ liệu đã bảo vệ.

#### Demo

Backup môi trường test, làm hỏng dữ liệu, restore vào môi trường sạch và kiểm tra history/ledger/artifacts.

#### Nghiệm thu

- Restore drill chứng minh task/evidence/profile/policy còn liên kết; counts/checksums khớp.
- Bypass quyền và secret test không có lỗi nghiêm trọng chưa xử lý.
- Migration được kiểm tra trên snapshot phiên bản trước; rollback/recovery constraints ghi rõ.

#### Bàn giao

Security audit, backup tooling và recovery/migration docs.

#### Giới hạn

Không tuyên bố backup tốt chỉ vì tạo được file; không đổi proxy/system service ngoài scope.

#### Bằng chứng cần có

Restore manifest, permission audit và crash/migration drill.

#### Nhật ký triển khai

Chưa có triển khai, kết quả kiểm thử hay quyết định nghiệm thu.

### Phase 23 — Nghiệm thu và phát hành V1

- Mốc: E
- Trạng thái: Chưa triển khai
- Phụ thuộc: 22; toàn bộ phase 00–22 được nghiệm thu
- Mục tiêu: Nền tảng sẵn sàng để Chủ tịch bắt đầu vận hành thật.

#### Phạm vi

- E2E nhiệm vụ thật sandbox: goal → plan → worker tools → reviewer → approval → acceptance → ledger/report.
- Polish UI, error handling, pagination/virtualization/retention, hiệu năng, cài local và tài liệu vận hành.
- Release checklist định lượng, bằng chứng tất cả gates, known limits; Chủ tịch nghiệm thu V1 rồi mới mở real onboarding.

#### Có gì mới

- Bản V1 local hoàn chỉnh và gói hướng dẫn cài/chạy/backup.
- Mở wizard thật để Chủ tịch thành lập tập đoàn và bổ nhiệm nhân viên đầu tiên.

#### Demo

Cài từ hướng dẫn, chạy nhiệm vụ sandbox end-to-end, gây lỗi/restart, restore rồi đối chiếu UI/ledger; Chủ tịch xem gói evidence.

#### Nghiệm thu

- Tất cả release gates R1–R8 đạt; không có lỗi blocker/nghiêm trọng chưa xử lý.
- Có bằng chứng thật cho observability, policy, budgets và recovery, không chỉ UI fixture.
- Chủ tịch chấp nhận release; không tự tạo công ty thật hoặc chạy task thật trước quyết định này.

#### Bàn giao

V1 release notes, acceptance report, installer/local scripts và docs.

#### Giới hạn

Không tự deploy cloud, không 3D office trong V1; dừng trước chặng vận hành thật.

#### Bằng chứng cần có

E2E report, release manifest, screenshots và quyết định nghiệm thu V1.

#### Nhật ký triển khai

Chưa có triển khai, kết quả kiểm thử hay quyết định nghiệm thu.

## 8. Release gate V1

Các ngưỡng dưới đây là baseline đặc tả Phase 00 đã được Chủ tịch nghiệm thu; hiện chưa đo và chưa đạt. Chi tiết tải test/denominator/ràng buộc tại docs/product-spec.md, mục 13.

| Gate | Điều kiện đo / nghiệm thu |
| --- | --- |
| R1 — Công việc thật | Ít nhất 3 kịch bản sandbox: thành công, reviewer yêu cầu sửa, approval bị từ chối; goal → artifact → review → human acceptance có trace đầy đủ |
| R2 — Quan sát | Inspector/replay dùng event thật; reconnect không mất/nhân đôi event đã lưu; p95 commit-confirmed → DOM render ≤ 2 giây với fixture 20 hồ sơ/10.000 events, ≥200 phép đo và môi trường ghi rõ |
| R3 — Quyền | 0 bypass thành công trong suite owner-only/cross-company/stale approval/tool escape/secret leak; approval gắn đúng payload/version |
| R4 — Ngân sách | Ledger reconciliation không đếm trùng; unknown/estimate rõ; 0 lượt dispatch mới sau hết reservation/hạn mức; không cam kết USD hard cap khi thiếu pricing |
| R5 — Sự cố | Kill worker/restart/offline/loop/interrupt thử thực tế; checkpoint hồi phục, không lặp side effect chưa xác định; stop giữ qua restart |
| R6 — Tách môi trường | Reset/demo/benchmark/real isolation suite đạt; real chưa có công ty người dùng cho tới quyết định release |
| R7 — Khôi phục | Restore database + artifacts + config refs vào môi trường sạch; counts/checksums/liên kết history khớp; có migration drill |
| R8 — Trải nghiệm và bàn giao | Cài/chạy theo docs trên môi trường kiểm tra; UI tiếng Việt/focus/mobile 390 px; mục tiêu 20 agent hiển thị + 10.000 event replay có pagination; 0 blocker/nghiêm trọng chưa xử lý; Chủ tịch chấp nhận |

### Checkpoint tích hợp trước tiếp bước

Chi tiết tại Product Spec V1 mục 13; đây là điều kiện kiểm chứng các phần đã triển khai, không thêm feature. Gate có report/config/version/batch/grant/evidence và PASS/FAIL; FAIL giữ Bị chặn, không thay run thật bằng mock. PASS không cấp quyền bắt đầu phase tiếp. Hiện mọi IG **Chưa thực hiện**; Phase 00 chỉ nghiệm thu định nghĩa.

| Gate | Sau / trước phase | Luồng kiểm chứng |
| --- | --- | --- |
| IG03 | 03 / 04 | API/DB/state/events/outbox atomic, restart/dedup và isolation; không inference |
| IG08 | 08 / 09 | Run thật text-only → events/SSE → Live Office/Inspector/replay; reconnect/error/usage, grant IG08 riêng nếu inference |
| IG12 | 12 / 13 | Work Order → delegation → quyền/approval/tools → review/rework/evidence; budget/stop propagation, grant IG12 riêng |
| IG16 | 16 / 17 | Calls/usage → ledger/budget/finance; dedup/late/unknown và lifetime cohort xuyên kỳ tách period cost; grant IG16 riêng nếu inference |
| IG20 | 20 / 21 | Task/events/ledger/incident → lịch/report/inbox; sleep/restart/dedup, nguồn số khớp query; grant IG20 riêng nếu inference |

R1–R8 tại release Phase 23 cần kèm evidence IG03/08/12/16/20. Gateway capability/isolation/privacy không đạt thì CG01: blocked + gap report cho Chủ tịch, không tự nới quyền/sửa/restart gateway shared hoặc tự đổi adapter. Phương án tiếp theo cần quyết định riêng; mock/đợt test thu hẹp không đạt thay tiêu chí runtime chưa kiểm chứng.

Cost per accepted task chọn cohort bằng accepted_at rồi tính toàn bộ lifetime cost của chính task cohort, gồm retry/rework/review/children không trùng, kể cả kỳ trước. Period operating cost tính riêng theo occurred_at mọi call/resource phát sinh trong kỳ. Giữ cost basis/currency/coverage/as_of/corrections và unknown khác 0, như đặc tả mục 13.

## 9. Chặng vận hành sau V1

Sau Phase 23 và quyết định nghiệm thu: Chủ tịch mở wizard thật → đặt tên/sứ mệnh → chọn model đã kiểm tra → cấp quyền và ngân sách → bổ nhiệm một Chief of Staff → giao nhiệm vụ đầu tiên → xem Inspector/ledger → nghiệm thu. Không tự mở chặng này khi Codex vừa báo test pass.

Nâng cấp sau V1 dựa trên evidence: 3D office, Executive Council, connector chuyên môn, remote/multi-user, provider adapter khác và tối ưu chuyên sâu. Không tự thêm vô hạn tính năng; mỗi mở rộng có phạm vi, ngân sách, quyền và điều kiện nghiệm thu riêng.

## 10. Nguồn và lịch sử kế hoạch

- [Ý tưởng tập đoàn ban đầu](sources/01-y-tuong-tap-doan.txt): domain, nhân sự, quyền, finance, memory; roadmap ban đầu chỉ là tham khảo.
- [Xây sản phẩm trước](sources/02-xay-san-pham-truoc.txt): nguồn chính của khung 00–23, observatory sớm, demo/real isolation và release gate.
- [README codex-server hiện có](../../codex-server/README.md) và source server/schema/provider: nguồn chính cho gateway HTTP.
- [Codex App Server chính thức](https://learn.chatgpt.com/docs/app-server): tham khảo tùy chọn mở rộng, không phải runtime mặc định của V1.
- 08/10/2026 — Kế hoạch 1.0: giữ 24 phase; chuyển event/state foundation lên 03 và baseline quyền/budget/stop trước 06. Chưa có triển khai sản phẩm hay nghiệm thu phase. Đã tìm thấy gateway codex-server riêng ở 127.0.0.1:4000 và điều chỉnh tích hợp theo source của gateway.

### Kiểm tra bàn giao tài liệu

Đã kiểm tra cấu trúc đủ 24 phase, trạng thái nguồn/HTML, các đường dẫn tương đối, JavaScript syntax và render lại từ Markdown. AGENTS.md có 34 dòng, nguồn ý tưởng được lưu nguyên bản. Chưa chạy test sản phẩm hay inference.

Kiểm tra trực quan trong trình duyệt tự động chưa thực hiện được: công cụ chặn navigation tới `file://`, chỉ chấp nhận HTTP/HTTPS. Trang vẫn được thiết kế để người dùng mở trực tiếp bằng trình duyệt; chưa khẳng định đã xác minh responsive qua ảnh render. Không start thêm server hay đổi port/proxy để thực hiện bước kiểm tra này.

### Bàn giao Phase 00

08/10/2026: cập nhật đặc tả/ADR/evidence và tài liệu trực quan. Phase 00 Chờ nghiệm thu; 01–23 giữ nguyên. 0 inference; 0 grant được cấp; chưa tạo runtime/công ty thật hoặc bắt đầu phase tiếp. Đầu lượt quan sát root có Git branch master và các file tài liệu untracked; giữ nguyên các thay đổi Git bên ngoài, không stage/commit. [Đặc tả V1](product-spec.html) · [Evidence](evidence/phase-00.md).

### Nghiệm thu sau review Phase 00 — bản 1.1

08/10/2026 — Chủ tịch yêu cầu bốn điều chỉnh nhỏ và nghiệm thu sau khi hoàn thành/kiểm tra nhất quán. Bốn điều chỉnh đã cập nhật vào đặc tả/ADR/roadmap; validation đạt, Phase 00 Hoàn tất. D01–D08/stack/adapter không đổi. IG03/08/12/16/20 và R1–R8 chỉ được định nghĩa, chưa kiểm chứng runtime. 0 inference, grant = 0, không quyền gọi model hoặc bắt đầu Phase 01; 01–23 giữ nguyên.
