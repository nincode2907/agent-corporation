# Báo cáo hiện trạng Agent Corporation

> Ngày chốt: 18/10/2026 (Asia/Saigon). Báo cáo tổng hợp mã nguồn, roadmap, đặc tả và các report kiểm định đã lưu trong repository tại thời điểm soạn. Không chạy test mới trong lượt tạo báo cáo này.

## 1. Tóm tắt điều hành

Agent Corporation là sản phẩm local-first để một Chủ tịch quản lý tổ chức AI, giao Work Order, kiểm soát quyền/ngân sách, theo dõi sự kiện và nghiệm thu artifact. V1 được xây qua 24 phase, trước tiên dùng fixture/demo; chỉ mở vận hành thật sau khi hoàn tất các release gate và có quyết định của Chủ tịch.

Tình trạng chính thức theo [`master-plan.md`](master-plan.md):

| Trạng thái | Phase | Ý nghĩa hiện tại |
|---|---|---|
| Hoàn tất | 00 | Hoàn tất baseline đặc tả và quyết định kiến trúc; không đồng nghĩa runtime hoàn tất. |
| Chờ nghiệm thu | 01–05 | Có implementation và evidence kiểm định ở các mức khác nhau; chưa có quyết định nghiệm thu mới để đổi trạng thái. |
| Bị chặn | 06–08 | Các gate/runtime/UI evidence còn thiếu, đặc biệt CG01/isolation, grant riêng, reconnect và IG08. |
| Đang triển khai | 09–10 | Queue/Work Order và governance approvals đang được xây; còn issue kỹ thuật và evidence tích hợp. |
| Chưa triển khai | 11–23 | Các phase sau chưa bắt đầu theo trạng thái roadmap. |

Chỉ **1/24 phase** được ghi Hoàn tất. Một lượt inference demo ở Phase 06 đã chạy thành công ngày 14/10; grant một request đó đã dùng hết. Tài liệu hiện ghi grant hợp lệ còn lại là **0**. CG01 vẫn `verified=false`; cấu hình ngoại lệ demo chỉ cho phép thử trong scope demo cố định và không thay thế kiểm chứng isolation hoặc nghiệm thu production.

Các mốc test dưới đây là snapshot từ report đã lưu, không phải kết quả được chạy lại trên source hiện thời khi tạo tài liệu này. Report kỹ thuật đạt cũng không tự đổi trạng thái phase hay thay quyết định nghiệm thu của Chủ tịch.

## 2. Lịch sử phase và phần đã làm

### Phase 00 — Chốt đặc tả V1

**Trạng thái: Hoàn tất.** Đã chuyển hai tài liệu ý tưởng thành hợp đồng sản phẩm: phạm vi V1, Chairman/Operator modes, 14 màn hình, yêu cầu có trace tới phase, luồng chính, dữ liệu logic, state machine, event contract, ngân sách/quyền và tiêu chí release. Stack nền được chọn là React/TypeScript/Vite, FastAPI/Pydantic, PostgreSQL/SQLAlchemy/Alembic và modular monolith. Chủ tịch nghiệm thu baseline đặc tả; việc này không cấp quyền inference hoặc tự cho phép bắt đầu phase khác. Employee Chat được bổ sung sau đó trong spec 1.2 nhưng vẫn là thiết kế, chưa được nghiệm thu hoặc triển khai.

### Phase 01 — Dựng nền phát triển local

**Trạng thái: Chờ nghiệm thu.** Repository có app web/API, cấu hình Compose và dependency pins, hướng dẫn bootstrap local/secret, migration baseline và health/readiness. Các port trong tài liệu: web `127.0.0.1:15500`, API `127.0.0.1:15501`, PostgreSQL `127.0.0.1:15510`; Vite proxy `/api` cùng origin. Report độc lập r005 ghi 15/15 case clean, gồm cài từ bản sao sạch, DB up/down, migration idempotent, binds/hostname và browser/favicon. Chưa có quyết định nghiệm thu mới của Chủ tịch.

### Phase 02 — Khung giao diện Chủ tịch

**Trạng thái: Chờ nghiệm thu.** Web SPA tiếng Việt có điều hướng hash và khung điều hành cho Tổng quan, Văn phòng, Công việc, approvals, Inspector/Replay, Tổ chức, Tài chính, Cấu hình/Sức khỏe, Playground và các màn hình đang khóa/đợi phase sau. Giao diện có trạng thái fixture/unknown thay vì giả dữ liệu thật. Report r002 có 11 case clean và 3 case blocked; còn thiếu bằng chứng UI/network được nêu trong roadmap. Vì vậy UI tồn tại không có nghĩa mọi flow đã được nghiệm thu.

### Phase 03 — Dữ liệu và bằng chứng bền vững

**Trạng thái: Chờ nghiệm thu.** Migration `0002` bổ sung mô hình domain bền vững gồm environment/company, organization, employee versions, policy, Work Order revisions, task/run state, checkpoints, approvals, artifacts, event counters, events và outbox. Event/state được thiết kế để lưu bằng PostgreSQL và gắn scope/correlation; redaction và API scope bắt đầu từ nền này. Report r002 ghi 17 case clean, không còn issue trong batch và **IG03 đạt về kỹ thuật**. Phase vẫn chờ quyết định nghiệm thu chính thức.

### Phase 04 — Nhà máy công ty demo

**Trạng thái: Chờ nghiệm thu.** Có factory tạo/reset fixture công ty demo, UI đọc dashboard demo và các guard để không trộn dữ liệu demo với công ty thật. Seed/reset phải tường minh. Report demo-factory lưu trong repository ghi 12 clean, 4 need-change và 3 blocked; không thấy report retest mới hơn trong bộ results hiện tại. Vì vậy không coi các issue cũ đã được đóng chỉ vì code tiếp tục thay đổi.

### Phase 05 — Kết nối Codex server local

**Trạng thái: Chờ nghiệm thu.** Backend có gateway adapter, health/catalog probe, profile model có version và chỗ lưu credential reference phía server; UI nhắc catalog không chứng minh entitlement. Gateway là HTTP local độc lập; browser không gọi thẳng gateway. Report r005 ngày 14/10 có 14 clean, 1 blocked, không gọi inference và không dùng grant thật. Case còn thiếu liên quan bằng chứng capability/CG01 và integration đủ điều kiện. Gateway không cung cấp token streaming hoặc hard `max_tokens`; Agent Corporation không được suy diễn các khả năng đó.

### Phase 06 — Agent đầu tiên chạy trong sandbox / Development Playground

**Trạng thái: Bị chặn về runtime production và nghiệm thu.** Có Owner session/CSRF, model profile, grant runtime, gate CG01, runtime call persistence, adapter, worker Work Order text-only và Development Playground tách biệt. Playground theo ADR-0003 có Session Grant riêng do Owner tạo; worker ứng dụng tự quản lý chỉ nhận queue Playground được cấp. Tin nhắn Playground không tạo Work Order, không có tools và không tự cấp/gia hạn grant.

Ngày 14/10 có một lượt demo runtime được gửi tường minh: model trả `final_response`, usage gateway ghi 10,354 prompt + 81 completion = 10,435 tokens; chi phí không biết. Grant một request được dùng hết. Đây là evidence lịch sử của lượt demo, không phải grant còn hiệu lực.

Report r010 ngày 15/10 kiểm Playground bằng source/API/DB fixture và fake transport: 9 case DPG được kiểm; API suite disposable có 142 passed, 11 skipped, web lint/build đạt. DPG10 — luồng UI grant/chat/Stop/recovery end-to-end — còn thiếu evidence. Report không gọi inference thật. CG01/isolation, cancellation và integration/runtime evidence production vẫn chặn Phase 06. Ngoại lệ `RUNTIME_CG01_DEMO_TEST_OVERRIDE=true` là chế độ demo có giới hạn, không phải proof; trước Phase 23 phải quay lại strict, dừng/khởi động lại workers và đạt release-check theo README.

### Phase 07 — Luồng event và khôi phục kết nối

**Trạng thái: Bị chặn.** Có event feed/SSE từ app, cursor có chữ ký/scope, redaction, gap handling và UI reconnect. Report r005 ghi 6 clean, 9 blocked. Regression route xác nhận `Last-Event-ID` mới được ưu tiên hơn query cursor cũ; chưa có browser network-drop evidence. Các case transaction failpoint, heartbeat/offline, crash/unknown, context recovery và run thật đến UI vẫn blocked; IG07 không phải gate riêng nhưng dependency Phase 06 chưa được giải quyết.

### Phase 08 — Live Office và Agent Inspector

**Trạng thái: Bị chặn.** Có các màn hình Office/Inspector/Replay đọc run và persisted events. Report r004 ngày 15/10 có 6 clean, 9 blocked, không có fail được xác nhận trong scope đã chạy. Reviewer đọc lại run Phase 06 đã lưu, xem 10 persisted events, seek/reload, kiểm copy cho summary thiếu và usage unknown/cost unknown. Chưa có run được cấp riêng cho Phase 08, Live Office active-run evidence, ACL âm/cross-scope, replay side-effect instrumentation, browser network-drop/reconnect và **IG08**. Grant/run Phase 06 không chuyển sang Phase 08.

### Phase 09 — Bảng nhiệm vụ và hàng đợi

**Trạng thái: Đang triển khai.** Có Work Order API/board, state transitions, revisions, priority, idempotency receipts, event ghi cùng thao tác và bảng queue/lease trong PostgreSQL. Report r002 ngày 14/10 có 5 clean, 10 need-change; trong đó 3 fail và 7 blocked. Các vấn đề chính được ghi là worker claim/recovery còn thiếu, retry/checkpoint chưa đạt và review/rework/accept chưa được chứng minh đầy đủ. Roadmap tóm tắt Phase 09 còn thiếu lease/recovery/retry. Phase phụ thuộc Phase 08, hiện chưa được nghiệm thu.

### Phase 10 — Quyền hạn và hộp phê duyệt

**Trạng thái: Đang triển khai.** Có permission evaluator, API approval requests/decisions, binding payload hash, expiry/staleness checks, Owner audit events, idempotency receipts và consume đơn lần. Phần quyết định/consume hiện trả `dispatch_status=not_dispatched`; executor được duyệt chưa tích hợp để chạy hành động thật. Report r002 có 6 clean và 9 blocked, không fail; evaluator/unit và schema/RLS được kiểm ở mức đã nêu, nhưng demo approve→tamper→reject, persisted lifecycle/race, executor và browser flows còn thiếu. Phase phụ thuộc Phase 09.

## 3. Roadmap các phase tiếp theo

Các trạng thái và dependency dưới đây lấy từ roadmap tại ngày chốt; phần mô tả là mục tiêu kế hoạch, không phải tính năng đã có.

| Phase | Trạng thái | Phụ thuộc | Mục tiêu bàn giao |
|---|---|---|---|
| 11 — Hệ thống công cụ thực thi | Chưa triển khai | 10 | Tool registry, policy/approval gates, sandbox executor, receipts/idempotency và bằng chứng side-effect an toàn trong workspace được cấp. |
| 12 — Điều phối nhiều nhân viên | Chưa triển khai | 11 | Luồng planner → worker → reviewer, handoff rõ ràng, quyền/budget/stop propagation; gate IG12 trước Phase 13. |
| 13 — Tổ chức và hồ sơ nhân viên | Chưa triển khai | 12; target CG01 cần Owner chốt trước chat backend | Organization/employee profile versions và nền tảng Employee Chat riêng, không dùng task giả; cần các foundation phase 03/06/07/08/10. |
| 14 — Tuyển dụng và thử việc | Chưa triển khai | 13 | AI đề xuất nhân sự/role, Chủ tịch quyết định; vòng onboarding/thử việc và đánh giá có bằng chứng. |
| 15 — Context và trí nhớ có kiểm chứng | Chưa triển khai | 14 | Context snapshot và memory có nguồn/provenance, ACL/retention, đúng nhân viên và scope; nền context cho chat và công việc. |
| 16 — Tài chính và ngân sách | Chưa triển khai | 15; usage/limits nền từ 06 | Ledger, reservation, usage provenance, cost basis/unknown, ngân sách và reconciliation; gate IG16. |
| 17 — Benchmark và chất lượng | Chưa triển khai | 16 | Bộ benchmark có cùng tiêu chí/fixture, so sánh nhân viên/model và kết quả truy vết được. |
| 18 — Đề xuất tối ưu có thử nghiệm | Chưa triển khai | 17 | AI đề xuất tối ưu tổ chức dựa trên số liệu, thử nghiệm có kiểm soát và Chủ tịch duyệt thay đổi. |
| 19 — Sự cố và dừng khẩn cấp | Chưa triển khai | 18; chat foundation 13–16; stop tối thiểu đã có ở 06 | Incident workflow, cô lập run, emergency stop và phục hồi theo checkpoint có bằng chứng; không replay side effects mơ hồ. |
| 20 — Lịch làm việc và báo cáo điều hành | Chưa triển khai | 19; cần IGCHAT trước mốc vận hành | Scheduler bền vững theo timezone, catch-up/dedup và báo cáo ngày/tháng từ dữ liệu nguồn; IG20. |
| 21 — Wizard thành lập tập đoàn | Chưa triển khai | 20 | Onboarding công ty thật sau release: policy/model/budget preview, bổ nhiệm một Chief of Staff, transaction/idempotency và real lock. |
| 22 — Bảo vệ dữ liệu và khôi phục | Chưa triển khai | 21 | Security/access audit, backup/restore DB + artifacts/config refs, migration/recovery drills; giữ ACL/evidence và không replay call. |
| 23 — Nghiệm thu và phát hành V1 | Chưa triển khai | 22; nghiệm thu toàn bộ 00–22 và IGCHAT đạt | E2E sandbox, polish, release manifest và R1–R8/IG evidence. Chỉ sau nghiệm thu V1 mới mở onboarding thật. |

### Trình tự phụ thuộc cần lưu ý

Roadmap hiện còn đồng thời Phase 06–08 bị chặn trong khi Phase 09–10 đang triển khai. Phase 09 phụ thuộc 08; Phase 10 phụ thuộc 09; Phase 11 phụ thuộc 10. Việc một phần source tồn tại hoặc một test suite pass không gỡ dependency/gate. Các gate tích hợp IG03/08/12/16/20 và IGCHAT phải có report/config/batch/evidence đúng scope; PASS không tự cấp quyền bắt đầu phase kế tiếp.

## 4. Kiến trúc đã chọn và kiến trúc đang có

### Baseline kiến trúc

```text
Browser (React/TypeScript/Vite, loopback)
    │ same-origin HTTP; Vite proxy /api
    ▼
FastAPI modular monolith (loopback)
    ├── Governance: Owner auth/session, profile, permissions, approvals
    ├── Work: Work Orders, transitions, queue commands
    ├── Execution: grant/gate, runtime calls, worker, gateway adapter
    ├── Observability: durable events, redaction, feed/SSE, replay reads
    ├── Demo: fixed-scope fixture factory/reset
    └── Playground: session/turn service and isolated background worker
    │
    ├── SQLAlchemy/Alembic → PostgreSQL (loopback, durable state/events)
    └── HTTP → local codex-server → provider/model
```

Gateway chỉ là transport/inference adapter, không phải authority của sản phẩm và không thực thi tools. Gateway hiện được mô tả là text chat completions `stream=false`, trả usage sau response, function call là proposal; Agent Corporation phải enforce quyền, sandbox và execution riêng. Không được suy entitlement, chi phí, privacy/isolation hoặc cancellation thật từ việc catalog/health phản hồi.

### Cấu trúc code hiện tại

- **Frontend:** `apps/web/src/App.tsx` là SPA điều hướng hash; `RuntimePanel.tsx` hiển thị health, runtime, event feed, Inspector/Replay và các lối điều hành; `PlaygroundPanel.tsx` giữ riêng UI Playground. CSS và favicon nằm trong `apps/web/src/` và `apps/web/public/`.
- **API bootstrap:** `apps/api/src/agent_corporation_api/main.py` gắn routers, thiết lập lifecycle worker Playground, trả liveness/readiness và làm sạch validation/database errors.
- **Governance:** `modules/governance/` có Owner auth/session, Windows ACL, profiles, permission evaluator và approvals.
- **Demo/domain:** `modules/demo/` có fixture factory/router; `modules/work/` có Work Order commands, state transitions, queue logic; `modules/companies/`/`organization/` đang là các package nền.
- **Execution/gateway:** `modules/execution/` gồm gates, service/router, worker và adapter path; `modules/codex_gateway/` probe catalog/health và HTTP adapter. Grant/gate và profile là điều kiện phía backend, không chỉ trạng thái UI.
- **Observability:** `modules/observability/` có events, scope, redaction, feed/router; events được lưu và cấp qua API/SSE. UI không được tuyên bố token streaming từ gateway.
- **Persistence:** migration Alembic từ `20261008_0001` tới `20261014_0009`. Các mốc chính: durable domain (`0002`), demo reset (`0003`), Owner (`0004`), runtime/grants/model calls (`0005`), usage corrections (`0006`), task queue (`0007`), queue leases và governance approvals ở hai nhánh `0008`, sau đó merge cùng Playground sessions/turns tại `0009`.
- **Tests:** `apps/api/tests/` có health/auth/gateway, persistence/domain demo, runtime/gates, event feed, queue/lease, approval và Playground tests. Web có lint/build qua package scripts. `docs/tests/` giữ checklist, report/evidence và remake history theo phase.

### Stack và dependency pins trong manifest

| Lớp | Pin/phiên bản khai báo |
|---|---|
| Frontend | Node 24 theo tài liệu runtime; React/React DOM 19.3.0; Vite 8.3.3; TypeScript 6.0.2; Oxlint 1.81.0. |
| API | Python `>=3.14,<3.15`; FastAPI 0.142.4; SQLAlchemy 2.1.4; Alembic 1.20.0; psycopg 3.3.6; Uvicorn 0.38.0. |
| Database | PostgreSQL 18.6 Alpine image, pin theo digest trong `compose.yml`. |
| Lockfiles | `apps/web/package-lock.json`, `apps/api/uv.lock`; source of truth cho toàn bộ transitive dependency. |

Đây là pin trong repository, không phải khẳng định các service hiện đang chạy. Các report test ghi riêng OS/tool version của từng batch.

### Các ranh giới thiết kế quan trọng

1. Một Owner local; Chairman/Operator là mode giao diện, không phải hai cấp quyền.
2. Scope company/environment được enforce ở API/database; một prompt hoặc nút UI không thay permission engine.
3. State, event, checkpoint, queue, receipt và usage cần bền vững; không dùng UI state hoặc gateway session làm nguồn chuẩn.
4. `completed` không đồng nghĩa task đã `accepted`; acceptance cần artifact/review/human decision.
5. Usage không có thì ghi unknown; cost unknown không được hiển thị như 0. Một request đang chạy có thể có outcome unknown sau stop/crash.
6. Side effect chưa rõ outcome không được retry nếu không có idempotency/receipt đủ tin cậy.
7. Demo/Playground, benchmark và real phải tách scope/data/artifacts/secrets. Playground worker chỉ xử lý Playground queue đã được grant.

## 5. Luồng code chính

### 5.1 Work Order / runtime dự kiến và phần đã hiện thực

```text
Owner UI
  → API Owner session + CSRF + company/environment scope
  → tạo/sửa Work Order revision, lưu state/event/receipt trong transaction
  → queue command (enqueue/pause/resume/cancel/accept/rework)
  → worker claim lease (đang hoàn thiện ở Phase 09)
  → kiểm grant + CG01 + policy/resource limits
  → gửi HTTP request qua adapter tới codex-server
  → lưu call result/usage hoặc unknown + events/checkpoint
  → feed/SSE → Office/Inspector/Replay
  → review/approval/rework/acceptance
```

Hiện có API/UI và các thành phần DB/queue/lease cùng phần execution nền, nhưng Phase 09 report nêu claim/recovery/retry còn thiếu; Phase 06–08 gates chưa đạt. Do đó sơ đồ mô tả luồng mục tiêu và các điểm code hiện có, không khẳng định luồng Work Order end-to-end đã được nghiệm thu.

### 5.2 Approval

API evaluator kiểm payload hash, expiry, task revision, policy version và trạng thái hiện hành; quyết định gắn Owner, idempotency key, reason/audit event. Consume khóa bản ghi và chỉ cho một lần dùng. Code hiện trả `not_dispatched`: approval không tự thực hiện hành động. Tích hợp executor thuộc Phase 11 và cần giữ kiểm tra hash/scope/side-effect tại thời điểm dispatch.

### 5.3 Development Playground

Owner đăng nhập → chọn profile/model/effort/employee demo và chấp nhận policy → bấm cấp Session Grant tường minh → session/turn ghi vào bảng Playground riêng → worker trong lifecycle FastAPI reserve request rồi gọi gateway stateless → lưu output/usage/event metadata. Tools/fallback bị tắt; hạn mức và expiry được enforce; Stop/crash có thể tạo unknown, không tự phát lại. Cơ chế này phục vụ demo Phase 06, không thay Employee Chat production ở Phase 13–20.

### 5.4 Giao tiếp web/API

Vite chỉ bind `127.0.0.1:15500`, proxy `/api` tới `127.0.0.1:15501`; API và PostgreSQL cũng chỉ bind loopback theo cấu hình dự án. Web gọi health/dashboard lúc mở để hiển thị trạng thái; theo contract, health/open/replay không được dispatch inference. Mở trang Playground cũng không cấp grant hoặc gửi message.

Trong working tree hiện có thêm file `.ui-review.json` để UI Lens capture tổng quan, Playground, Tổ chức và Cấu hình/Sức khỏe ở desktop/mobile; registry UI Lens bên ngoài repo đã trỏ ID `agent-corporation` về đường dẫn Windows hiện tại. Capture chưa chạy và file này không phải evidence/acceptance cho phase.

## 6. Kiểm thử và evidence hiện có

| Phase | Batch mới nhất đã lưu | Kết quả report | Tình trạng/giới hạn chính |
|---|---|---|---|
| 00 | Evidence Phase 00 | Validation tài liệu/baseline đạt và được Chủ tịch nghiệm thu | Đây không phải product unit/E2E/runtime test. |
| 01 | [r005](tests/results/phase-01/20261009T092254+0700-r005-test/report.md) | 15 clean, 0 need-change; kỹ thuật đạt | Đã retest setup/local DB/browser; chờ nghiệm thu chính thức. |
| 02 | [r002](tests/results/phase-02/20261009T094432+0700-r002-test/report.md) | 11 clean, 3 blocked | Thiếu UI/network evidence; chờ nghiệm thu. |
| 03 | [r002](tests/results/phase-03/20261009T094432+0700-r002-test/report.md) | 17 clean; IG03 kỹ thuật đạt | Chưa có quyết định nghiệm thu mới. |
| 04 | [demo-factory](tests/results/phase-04/20261008T162050+0700-demo-factory/report.md) | 12 clean, 4 need-change, 3 blocked | Report lịch sử; chưa thấy retest mới đóng các điểm còn lại. |
| 05 | [r005](tests/results/phase-05/20261014T150201+0700-r005-test/report.md) | 14 clean, 1 blocked | Không inference; capability/CG01 evidence còn mở. |
| 06 | [Playground r010](tests/results/phase-06/20261015T000509+0700-r010-test/report.md) | 142 API passed, 11 skipped; lint/build đạt; DPG10 blocked | Test dùng DB disposable/fake transport; không chứng minh CG01 hoặc live Playground UI. Production phase vẫn blocked. |
| 07 | [r005](tests/results/phase-07/20261015T071306+0700-r005-test/report.md) | 6 clean, 9 blocked; focused API 54 passed/9 skipped; full isolated API 143 passed/11 skipped; lint/build đạt | Thiếu browser network-drop, worker crash/recovery và run thật; P07-02 route regression đã kiểm. |
| 08 | [r004](tests/results/phase-08/20261015T073129+0700-r004-test/report.md) | 6 clean, 9 blocked; isolated API 143 passed/11 skipped; lint/build đạt | Quan sát saved Phase 06 run; ACL-negative, side-effect instrumentation, live Office, reconnect và IG08 còn blocked. |
| 09 | [r002](tests/results/phase-09/20261014T162815+0700-r002-test/report.md) | 5 clean, 10 need-change; 3 fail, 7 blocked | Worker claim/recovery/retry và acceptance evidence chưa đạt. |
| 10 | [r002](tests/results/phase-10/20261014T163443+0700-r002-test/report.md) | 6 clean, 9 blocked; 0 fail | Evaluator/schema checks có evidence; executor/browser/lifecycle/tamper demo chưa chạy. |

Các con số này thuộc những môi trường/batch khác nhau; không cộng thành một “tổng test pass” duy nhất. `skipped`/`blocked` không được tính như pass. Chi tiết commands, versions, source hash và cleanup nằm trong report/evidence được liên kết.

### Cách chạy bộ kiểm tra theo tài liệu dự án

Các lệnh dưới đây được chép từ README và AGENTS.md, không được chạy trong lượt lập báo cáo này:

```sh
uv run --project apps/api pytest apps/api/tests
npm run --prefix apps/web build
uv run --project apps/api alembic -c apps/api/alembic.ini upgrade head
```

Đối với pipeline một phase, cần đọc `docs/tests/RULES.md` và `docs/tests/phases/phase-NN.md`, dùng batch `rNNN`, lưu report/evidence và tiếp tục remake/retest nếu còn need-change có thể giải quyết. Kết quả test không tự nghiệm thu phase.

## 7. Blocker và giới hạn còn đáng chú ý

- **CG01/isolation:** strict proof cần evidence thật về isolation, privacy/retention và cancellation. Demo override không biến `verified=false` thành true.
- **Inference grant:** grant là theo phase/batch/mục đích/scope/hạn mức/expiry; lượt demo đã dùng hết grant cũ. Không mặc định có quyền chạy lượt mới.
- **Phase 07–08:** thiếu UI/browser fault evidence và IG08 live integration; test route/unit không thay thế network-drop hoặc run có grant phù hợp.
- **Phase 09–10:** queue/lease recovery và approval lifecycle/executor còn chưa khép kín; approval hiện chưa dispatch action.
- **Employee Chat:** ADR/spec và prototype/design tồn tại, nhưng production backend/UI, privacy gates, finance, stop/recovery và IGCHAT chưa triển khai/nghiệm thu.
- **Release:** backup/restore, full security audit, R1–R8 và toàn bộ IG còn phía trước. Chưa có công ty thật; wizard thật vẫn khóa đến release V1.

## 8. Tài liệu nguồn và cách đọc tiếp

- Trạng thái, dependency, phạm vi và tiêu chí: [`master-plan.md`](master-plan.md).
- Hợp đồng sản phẩm: [`product-spec.md`](product-spec.md).
- Quyết định nền: [`ADR-0001`](decisions/0001-v1-foundation.md), [`ADR-0002 Employee Chat`](decisions/0002-employee-chat.md), [`ADR-0003 Development Playground`](decisions/0003-development-playground.md).
- Checklist/pipeline test: [`docs/tests/README.md`](tests/README.md), [`RULES.md`](tests/RULES.md), từng phase trong [`tests/phases/`](tests/phases/).
- Report kiểm thử và remake: [`docs/tests/results/`](tests/results/) và [`docs/remakes/`](remakes/).
- Runtime/setup và giới hạn bảo mật: [`README.md`](../README.md), [`AGENTS.md`](../AGENTS.md).

**Nguyên tắc đọc trạng thái:** master plan là nguồn chính thức cho phase. Report mô tả kiểm định kỹ thuật ở một snapshot; remake mô tả thay đổi; chỉ quyết định của Chủ tịch mới chuyển trạng thái sang nghiệm thu/hoàn tất. Không suy quyền từ code tồn tại, test mock, catalog model hoặc lượt inference lịch sử.
