# Đặc tả sản phẩm Agent Corporation V1

> Phiên bản đặc tả: 1.1 · Ngày: 08/10/2026 · Phase: 00.
> Trạng thái: Đã nghiệm thu đặc tả và baseline kiến trúc — Phase 00 Hoàn tất.
> Runtime/inference đã chạy trong Phase 00: **0 lượt**. Hạn mức test được cấp hiện tại: **0 lượt**. Không có công ty thật của người dùng.

[Trang đặc tả trực quan](product-spec.html) · [Theo dõi Phase 00](master-plan.html#phase-00) · [Quyết định nền V1](decisions/0001-v1-foundation.md) · [Bằng chứng Phase 00](evidence/phase-00.md).

## 1. Mục đích và hợp đồng bàn giao

Agent Corporation là nền tảng local-first để một Chủ tịch giao mục tiêu cho tổ chức AI, quản lý quyền/ngân sách, nhìn thấy công việc thực và nghiệm thu bằng chứng. AI là nhân sự có hồ sơ và trách nhiệm; không giả vờ liên tục suy nghĩ khi idle. Thành công đo bằng đầu ra được nghiệm thu và chi phí thực hiện, không bằng số nhân viên hay token đã tiêu.

Phase 00 bàn giao đặc tả màn hình, luồng chính, mô hình dữ liệu logic, state machines, event contract, quyết định kiến trúc, traceability và test/release criteria. Không scaffold ứng dụng, tạo migrations, cài dependency, start worker, reserve port hay thay gateway. Các mã requirement, trạng thái và event là hợp đồng thiết kế để Phase 01–03 triển khai; chưa phải code đã tồn tại.

Nguồn ưu tiên: bản ý tưởng 02 cho build-before-operate và observatory; bản 01 cho domain nhân sự/quyền/finance/memory. Gateway contract lấy từ source hiện có; mọi số mẫu trong hai ý tưởng đều là minh họa, không nhập làm số liệu công ty thật.

## 2. Phạm vi V1 và hai chế độ

### Hai chế độ, cùng một Chủ tịch

| Chế độ | Công việc của người dùng | Đầu ra phải nhìn thấy | Quyền |
| --- | --- | --- | --- |
| Chairman Mode | Giao mục tiêu, đặt giới hạn, duyệt đề xuất, nhận báo cáo | Tiến độ, việc cần quyết định, sản phẩm và bằng chứng nghiệm thu | Owner đã xác thực |
| Operator Mode | Điều tra task/run/tool, xem replay/ledger/benchmark và cấu hình | Bằng chứng nguồn, lỗi, versions và hành động phục hồi được phép | Vẫn là Owner; đổi chế độ không thêm quyền |

V1 có một Owner local, hỗ trợ nhiều hồ sơ công ty trong store nhưng chỉ một công ty/môi trường được chọn tại một thời điểm. Không có tài khoản nhân viên con người hay cộng tác nhiều người. Agent identities là service actors, không có session Owner. Chuyển công ty/môi trường phải hủy stream cũ, đổi scope và load lại dữ liệu theo quyền.

### Phạm vi được giữ

- Công ty/phòng ban/hồ sơ nhân viên version hóa; permanent, on-demand, contractor.
- Work Order, queue, runtime qua gateway HTTP local, tool executor sandbox và giao việc nhiều agent có hạn mức.
- Dashboard, Live Office 2D, Inspector dùng chung, replay read-only, inbox approval.
- Ledger/budgets, benchmark/tournament, proposal tối ưu, context/memory promotion.
- Emergency Stop, incidents/recovery, scheduler, báo cáo ngày/tháng, onboarding và backup/restore.
- Công ty demo/benchmark/real tách biệt; chỉ sau release được nghiệm thu mới tạo công ty thật và một Chief of Staff.

### Ngoài V1

Văn phòng 3D, CEO được bổ nhiệm tự động, Executive Council nhiều agent chuyên sâu, multi-user/remote control, cloud deploy, Kubernetes/microservices, connector không có allowlist, full OpenAI API, token streaming từ gateway và đọc suy nghĩ nội bộ nguyên văn. Không triển khai ngoại lệ bằng cách nới quyền server chung.

## 3. Danh mục màn hình và trạng thái giao diện

| ID | Màn hình | Nội dung/hành động chính | Trạng thái bắt buộc | Phase |
| --- | --- | --- | --- | --- |
| S01 | Tổng quan tập đoàn | Công việc/nhân sự/chi phí/sức khỏe, link task và Inspector | Trống, đang tải, lỗi, demo, offline, số chưa biết | 02, 04, 07, 16 |
| S02 | Văn phòng trực tiếp | Nhóm agent theo phòng; task đang nhận; ai chặn ai | Idle khác offline; waiting model khác executing tools | 08, 12 |
| S03 | Agent Inspector | Plan, tóm tắt quyết định, trace, file diff, tool receipt, messages, model/profile, metrics | Live, historical, interrupted, redacted, missing usage | 08, 11, 13 |
| S04 | Replay run | Timeline/filters/cursor, checkpoint, lỗi và evidence | Read-only; gap dữ liệu rõ; không re-execute | 08 |
| S05 | Công việc | Soạn Work Order, scope, deadline, budget, assignee, queue, pause/cancel/rework | Draft, blocked, chờ duyệt/kiểm tra/nghiệm thu | 09 |
| S06 | Inbox Chủ tịch | Approval action/HR/memory/optimization kèm tác động và evidence | Pending, rejected, approved, expired, stale | 10, 14, 15, 18, 20 |
| S07 | Tổ chức và nhân sự | Org chart, reporting lines, role/capabilities/policy, profile versions | Không có nhân viên, active, probation, draining, offboarded | 13, 14 |
| S08 | Trí nhớ và context | Năm lớp context, nguồn/version/ACL, promotion/revert | Pending, approved, expired, redacted | 15 |
| S09 | Tài chính | Drilldown công ty → phòng → nhân viên → task → model → HTTP call; reservation/usage/pricing | Xác nhận, ước tính, chưa biết, thiếu dữ liệu | 16 |
| S10 | Chất lượng và thí nghiệm | Suite/version/test evidence, so model/profile, A/B proposal | Chưa có mẫu, cỡ mẫu nhỏ, run lỗi, budget blocked | 17, 18 |
| S11 | Sự cố | Loop/timeout/denied tool, Emergency Stop và hướng phục hồi | Stopped bền vững, unknown outcome, reconciling | 19 |
| S12 | Lịch và báo cáo | Scheduled jobs, miss/catch-up, daily/monthly brief, evidence links | Máy ngủ/tắt, skipped, partial usage | 20 |
| S13 | Thiết lập và sức khỏe | Kết nối gateway, catalog/model config, auth refs, policy/budget, backup | Health không chứng minh entitlement; error cụ thể | 05, 10, 22 |
| S14 | Wizard thành lập | Tên/sứ mệnh/mục tiêu, model, autonomy, budget, một Chief of Staff | Real locked đến release; submit idempotent | 21, 23 |

Inspector mở từ S01/S02/S05/S07 mà giữ scope và run đang chọn. Mọi màn hình có nhãn môi trường và thời điểm dữ liệu cập nhật. Metrics `null` hiển thị “Chưa biết”, không thành 0. Empty state chỉ dẫn một hành động phù hợp, không tự seed real. Responsive mục tiêu 390 px, keyboard focus rõ, reduced motion, `lang=vi` và favicon.

## 4. Luồng công việc và demo Phase 00

### Kịch bản đặc tả F01 — Một nhiệm vụ được nghiệm thu

Đây là mô phỏng giấy của nhiệm vụ demo “Tạo báo cáo tổng hợp từ ba tài liệu được cấp”. Không có model/tool chạy, không hiển thị tiến độ giả là runtime thật. Mỗi bước mô tả bằng chứng mà sản phẩm tương lai phải tạo.

| Bước | Người chịu trách nhiệm | Hành động | Trạng thái task sau bước | Bằng chứng dự kiến |
| --- | --- | --- | --- | --- |
| 1 | Chủ tịch | Tạo Work Order có đầu ra, criteria, quyền, deadline và hạn mức | draft | Task revision + acceptance criteria + scope |
| 2 | Hệ thống / Chief of Staff | Kiểm tra grant, enqueue, nhận việc và lập plan | planning | TASK_CREATED, TASK_QUEUED, AGENT_ASSIGNED, TASK_STARTED, PLAN_UPDATED |
| 3 | Chủ tịch | Duyệt plan/action có payload cố định khi ngoài quyền đã cấp | awaiting_approval → executing | APPROVAL_REQUESTED, APPROVAL_DECIDED, policy/version/hash |
| 4 | Worker / executor | Model đề xuất tool, backend validate và executor làm trong sandbox | executing | HTTP call/span, TOOL_CALL_STARTED/COMPLETED, receipt và artifact |
| 5 | Reviewer | So artifact/test với acceptance, chỉ ra sai sót nếu có | reviewing | EVALUATION_COMPLETED, checklist và evidence refs |
| 6 | Chủ tịch | Nhận output đạt kiểm tra để tự đối chiếu điều kiện | awaiting_acceptance | TASK_COMPLETED, delivery manifest, ledger/unknown indicators |
| 7 | Chủ tịch | Chấp nhận kết quả; nếu chưa đạt thì yêu cầu rework | accepted | TASK_ACCEPTED, actor Owner, task revision và evaluation refs |

Bước 3 chỉ xuất hiện khi policy yêu cầu; task nhỏ trong grant không bắt buộc họp hay thêm Architect. Không có inference ở bước 2 khi grant test còn 0. Thao tác submit Work Order không thay cho quyền tăng budget/model. `TASK_COMPLETED` là bàn giao đầu ra, **không** là nghiệm thu `TASK_ACCEPTED`.

### Các nhánh không được che giấu

| ID | Tình huống | Hành vi hợp đồng | Phase kiểm chứng thực |
| --- | --- | --- | --- |
| F02 | Approval bị từ chối/hết hạn | Không dispatch action; giữ bằng chứng, task blocked; Owner có thể sửa scope hoặc cancel | 10, 23 |
| F03 | Reviewer yêu cầu sửa | reviewing → rework; tạo run/attempt mới, giữ run cũ; không tự nới scope/budget | 09, 12, 23 |
| F04 | Timeout/crash lúc gọi gateway | Đánh dấu interrupted/reconciling, không tự gửi lại request chưa biết outcome; không giả usage 0 | 07, 09, 19 |
| F05 | Pause/stop | Chặn bước mới; abort request đang chạy; xác minh cancellation; resume từ boundary đủ bằng chứng | 06, 09, 19 |
| F06 | Đổi model/nhân sự | Proposal + benchmark nếu cần + Owner quyết định; run cũ giữ immutable snapshot | 13, 14, 18 |
| F07 | Máy ngủ qua lịch báo cáo | Không báo đã làm việc; dùng miss policy, dedup job và ghi catch-up thực | 20 |
| F08 | First-run sau release | Wizard thật, budget mặc định 0, Owner cấp scope, chỉ bổ nhiệm một Chief of Staff | 21, 23 |

## 5. Baseline kiến trúc và tổ chức repository

### Quyết định triển khai để nghiệm thu

| Thành phần | Lựa chọn V1 | Lý do / ranh giới |
| --- | --- | --- |
| Giao diện | React + TypeScript + Vite | UI 2D; HTTP actions, SSE chỉ đọc từ backend; không gọi gateway trực tiếp |
| Backend | Python + FastAPI + Pydantic, modular monolith | Một nguồn policy/task/state/event; command handlers tách khỏi views |
| Database | PostgreSQL, migrations qua Alembic/SQLAlchemy | Task state + events + ledger + queue bền vững; transaction/RLS/idempotency |
| Worker/scheduler | Python process riêng, dùng PostgreSQL jobs/leases | Không giữ queue bằng RAM; không cần Redis/Temporal ở V1 |
| Artifacts | File store local theo environment/company/task/run | DB lưu manifest/hash; không dùng path từ client/agent để đọc thẳng |
| Inference | HTTP adapter → codex-server hiện có | Giữ gateway text-only; app sở hữu orchestration/tools và ledger |
| Executor | Sandbox riêng cho tools; capability allowlist | Không chạy terminal trong gateway, không dùng quyền phiên Codex hiện tại |
| Runtime local | Compose cho PostgreSQL; frontend/API/worker trên host lúc dev | Kết nối 127.0.0.1:15600 server-to-server; không thêm host networking của container |

Phiên bản thư viện/image cụ thể được pin từ tooling có thể kiểm chứng ở Phase 01; đây là việc chọn version, không đổi stack. Không tự nâng codex-server hoặc gateway CLI để phù hợp với dự án.

### Sơ đồ sở hữu trách nhiệm

```text
Chủ tịch → Frontend React → Backend FastAPI (auth + policy + commands)
                                  ├→ PostgreSQL (state/events/jobs/ledger/memory)
                                  ├→ Artifact store (manifest + hashes)
                                  ├→ HTTP gateway 127.0.0.1:15600 → Codex CLI → model
                                  └→ Tool executor sandbox (chỉ sau validate + approval)
Backend commit event → SSE → Dashboard / Live Office / Inspector / Replay
Model response → tool proposal → backend kiểm quyền → executor → receipt → lượt model sau
```

Cấu trúc mục tiêu Phase 01 (chưa tạo): `apps/web/`, `apps/api/`, backend modules `companies`, `organization`, `work`, `execution`, `governance`, `observability`, `finance`, `knowledge`, `quality`, `operations`; `infra/`, `scripts/`, `tests/`, `docs/`. Module dùng service/command contract, không tự viết trực tiếp bảng sở hữu của module khác. Workers gọi cùng handlers/policy với API. Public API prefix `/api/v1`; không copy gateway paths thành public proxy.

### Ranh giới phase đầu

Phase 01 chỉ skeleton, health, dev tooling và database baseline; chưa seed nhân sự thật hay gọi model. Phase 02 UI shell theo S01–S14, fixture chưa tính là live. Phase 03 schema/state/events/constraints; Phase 04 mới Demo Factory. Phase 05 probe gateway không inference; Phase 06 mới run thật nếu mọi grant/capability gates đạt. Quyết định này không cấp quyền bắt đầu Phase 01.

## 6. Gateway contract và giới hạn quan sát

Nguồn đã đọc: `codex-server/src/server.ts`, `src/schema.ts`, `src/provider.ts` (hash trong evidence). Package version quan sát: `0.1.0`; CLI ở PATH không nhất thiết là bundled CLI gateway đang dùng. Health GET 200 chỉ chứng minh server trả lời, không chứng minh login/model/quota.

| Contract | Quy định cho adapter V1 |
| --- | --- |
| Endpoint | `http://127.0.0.1:15600`, cấu hình ở backend; chỉ loopback endpoint allowlist; không nhận URL tùy ý từ agent |
| Auth | Nếu gateway yêu cầu Bearer thì backend lấy secret ref; không in `.env`/auth hoặc đưa token vào browser |
| Probe | GET /health và /v1/models; catalog không là entitlement; 401 không tự đọc secret để vượt |
| Request | POST /v1/chat/completions, text messages, model explicit, reasoning_effort explicit, n=1, stream=false; không gửi max_tokens/response_format/metadata/custom IDs |
| Context | App giữ history/checkpoint riêng; gửi đủ tool results và unique tool_call_id trước lượt tiếp; tối đa 512 messages/1 MiB theo gateway, app cap thấp hơn |
| Tools | Function-call proposals, schema draft-07; backend revalidate, policy + approval + sandbox; gateway không thực thi tool của app |
| Correlation | Lưu app request_span_id trước dispatch; nhận X-Codex-Call-Id khi có response; không đoán call ID nếu disconnect trước response |
| Cancellation | Abort HTTP trong worker → gateway close handler abort CLI; Phase 06 phải thử thực tế, không khẳng định kill cả subprocess tree trước test |
| Errors | 400 là invalid contract, 401 auth blocked, 403 boundary blocked, 429 queue/backoff, 502/504 unknown/failed tùy evidence; chỉ retry chắc chắn chưa dispatch |
| Session | V1 mặc định stateless, không dùng gateway session APIs; app giữ context. Session TTL/model lock/invalidation không dùng làm durability của app |
| Metrics | Usage cả Codex turn khi trả final response; null khác 0; không suy internal call counts từ native rollouts |
| Privacy | Chat stateless tại route này vẫn có thể tạo Codex rollout, không phải ephemeral playground; app redaction không xóa transcript nguồn |

Không gửi task secrets hoặc prompt không tin cậy tới gateway shared khi chưa kiểm chứng inference isolation/read boundary và retention. Khả năng này là gate trước Phase 06; nếu không đạt thì dừng run, không sửa gateway chung. V1 app tự lưu Plan/Decision Summary tường minh từ response; không thu thập chain-of-thought. Live chờ model chỉ hiển thị “Đang chờ phản hồi model” và elapsed; không có live token count giả.

Cập nhật cấu hình local ngày 09/10/2026: gateway đã được dự án codex-server đăng ký ở block15600–15699 và đang nghe15600; health/models GET được xác minh không inference. Agent Corporation đồng bộ default endpoint theo registry, không đổi gateway hoặc baseline HTTP. Evidence khảo sát cũ4000 vẫn giữ nguyên trong các batch lịch sử.

### CG01 — Contingency và decision gate cho gateway

Nếu probe/test chỉ ra codex-server không đáp ứng capability bắt buộc, inference isolation hoặc privacy/retention đã quy định, đánh dấu gate **FAIL/Bị chặn** trước inference hoặc trước khi cấp inputs tương ứng. Lưu capability matrix, version/source fingerprint, lỗi đã lọc và requirement/test bị ảnh hưởng; không gửi thêm prompt để thử vượt boundary. Không tự nới quyền, CORS/bind, auth, native tools, logging/retention hoặc sửa/restart gateway dùng chung.

Chủ tịch là người quyết định phương án tiếp theo sau khi nhận gap report:

| Lựa chọn | Phạm vi được phép | Điều kiện trước tiếp tục |
| --- | --- | --- |
| Giữ blocked | Không inference; làm tài liệu/fixture/adapter mock trong scope phase đã giao | Mock có nhãn, không thay bằng chứng run thật, không đạt integration/release gate cần runtime |
| Đợt test thu hẹp | Chỉ inputs tin cậy, capability và privacy boundary đã xác minh, mục đích/hạn mức mới rõ | Chủ tịch cấp grant riêng cho scope thu hẹp; không coi là đạt yêu cầu chưa kiểm chứng |
| Đề xuất instance cô lập hoặc thay đổi cần thiết | Chỉ chuẩn bị phương án: capability/privacy, cấu hình/data/auth tách biệt, chi phí và validation/rollback | Chủ tịch phê duyệt riêng thay đổi/provisioning; nếu đổi baseline/adapter thì có ADR và sửa spec trước implement; không sửa gateway shared |

Mặc định là giữ blocked, không tự chọn fallback provider/adapter/instance. HTTP gateway đã chọn vẫn là baseline; contingency không cấp quyền tạo instance khác. Sau phương án được Chủ tịch chọn, phải kiểm chứng lại capability/isolation/privacy và cấp **grant mới cho đợt test tiếp theo**, không tái dùng grant của đợt đã fail. Gate không đạt thì chưa nghiệm thu năng lực liên quan hoặc bước tích hợp phụ thuộc. Thiếu token streaming/max_tokens đã biết là giới hạn V1, không tự coi là lý do đổi kiến trúc; chỉ thiếu capability bắt buộc mới kích hoạt CG01.

## 7. Mô hình dữ liệu logic và các bất biến

### Thực thể và quyền sở hữu

| Thực thể | Dữ liệu cốt lõi | Bất biến |
| --- | --- | --- |
| Environment / Company | UUID, kind demo/benchmark/real, tên, mission, release lock | environment kind bất biến; real onboarding khóa đến release |
| Department | company/environment IDs, tên, reporting parent | Không reporting cycle hoặc cross-company parent |
| Employee / EmployeeVersion | Loại hợp đồng, lifecycle; persona, model/effort, tools/skills, context/policy refs | Version đã dùng không sửa; offboard không xóa lịch sử |
| WorkOrder / TaskRevision | Goal, output, criteria, scope, deadline, budget/grant, assignee | Criteria/policy version được snapshot; revision thay đổi quyền cần Owner duyệt |
| Run / Step / Checkpoint | Task revision, attempt, employee version, status, planned steps, resume boundary | Một run gắn đúng một revision/profile; completed không suy ra accepted |
| ModelCall | Request span ID, gateway call ID nullable, model/effort, request status, usage | Unknown outcome không auto retry; usage nguồn cả turn, không native/global totals |
| ToolAction / Receipt | Function/schema version, validated args digest, permission/approval refs, receipt | Prepared trước dispatch; idempotency key và outcome, không tự lặp unknown side effect |
| Approval / Decision | Actor, action/payload hash, company/run/policy/expiry, decision | Scoped, one-use, không dùng cho payload đã sửa; chỉ Owner được duyệt owner-only |
| Event / Outbox | Envelope v1, per-company stream sequence, payload đã lọc | Append-only; state + event + outbox cùng transaction |
| Job / Lease | Scope, task/run, next step, ready_at, worker, lease expiry, retry counter | Claim có lock; một active lease/step; expire không suy ra side effect chưa xảy ra |
| Artifact / DeliveryManifest | IDs, relative storage key, hash, MIME/size, source run | API lấy qua authorized manifest; không nhận arbitrary absolute path |
| BudgetGrant / Reservation / Ledger | Owner limit, interval, resource/cost basis, immutable usage/pricing entries | Reserve atomic; one settle per call, missing usage giữ unresolved |
| MemoryVersion / Promotion | Layer, ACL, provenance/evidence, reviewer, expiry | Retrieval không cross-scope; promotion không tự nâng policy |
| Benchmark / Evaluation / Incident / Schedule / Report | Suite/config version, evidence refs, factual aggregates | Environment riêng; report số từ query, không do model bịa |

### Scope và transaction

Mọi dữ liệu công ty có `environment_id` + `company_id`; FK composite và unique keys cùng scope. Backend lấy scope từ Owner session đã xác thực, xác minh selected company; không tin `company_id` client/agent tự gửi. V1 chọn PostgreSQL RLS cho company-scoped tables, application role không owner/superuser/BYPASSRLS; transaction set scope bằng `SET LOCAL`, thiếu scope deny. Migration role tách khỏi app. API/worker/policy/artifact authorization vẫn kiểm tra scope, không dựa riêng vào RLS.

Work Order revision, run profile snapshot, approval decision, pricing snapshot và final ledger entries immutable. Thay đổi bằng phiên bản/sự kiện mới, không sửa run cũ. State transition dùng expected revision/optimistic lock; tạo event/outbox và reservation trong cùng transaction khi tương ứng. Có invariant tests trước Phase 03 được nghiệm thu.

### Work Order contract v1

| Field | Kiểu / yêu cầu | Quy tắc |
| --- | --- | --- |
| schema_version, id, revision | 1, UUID, integer ≥ 1 | Mỗi revision có history |
| environment_id, company_id | UUID bắt buộc | Cross-scope FK bị từ chối |
| goal, expected_outputs | Text, danh sách output | Không submit nếu trống |
| acceptance_criteria | Danh sách id/description/evidence_kind | Có ít nhất 1 tiêu chí có thể kiểm chứng |
| scope | Approved input/artifact/workspace refs, tool capabilities | Không chứa đường dẫn host tùy ý hoặc secrets |
| deadline_at | UTC timestamp hoặc null | Deadline không tự tăng quyền/budget |
| execution_grant_id, budget_limits | Grant ref hoặc null; limits resource/cost basis | Null/0 chặn inference; không dùng budget số mẫu từ ý tưởng |
| stop_conditions | max duration/requests/rework, forbidden actions | Phải có điểm dừng trước dispatch |
| assignee_id, reviewer_id | Employee UUID hoặc null | Assignment kiểm tra lifecycle/capability |
| autonomy | strict/supervised/delegated | Không thay owner-only hay hard constraints |
| created_by, status | Actor ref, task enum | Agent không giả actor Owner |

Ví dụ draft hợp lệ về thiết kế, chưa có grant thực thi:

```json
{
  "schema_version": 1,
  "id": "10000000-0000-4000-8000-000000000001",
  "revision": 1,
  "environment_id": "20000000-0000-4000-8000-000000000001",
  "company_id": "30000000-0000-4000-8000-000000000001",
  "goal": "Tổng hợp ba tài liệu demo đã cấp",
  "expected_outputs": ["Báo cáo có liên kết nguồn"],
  "acceptance_criteria": [{"id": "AC01", "description": "Mỗi kết luận truy ra nguồn đã cấp", "evidence_kind": "source_reference"}],
  "scope": {"input_refs": ["fixture/doc-1", "fixture/doc-2", "fixture/doc-3"], "tool_capabilities": []},
  "deadline_at": null,
  "execution_grant_id": null,
  "budget_limits": {"max_model_requests": 0, "cost_basis": "unknown", "usd_limit_micros": null},
  "stop_conditions": {"max_duration_seconds": 120, "max_rework_rounds": 0},
  "assignee_id": null,
  "reviewer_id": null,
  "autonomy": "strict",
  "created_by": {"kind": "owner", "id": "owner-local"},
  "status": "draft"
}
```

## 8. State machines cho task, run và approval

### Task states và đường chuyển hợp lệ

| Từ | Sang | Điều kiện / actor |
| --- | --- | --- |
| draft | queued | Owner submit revision đủ criteria/scope; grant có thể chưa có, dispatcher vẫn phải gate |
| queued | planning | Lease đã claim; inference gate đạt nếu plan cần model; TASK_STARTED |
| planning | awaiting_approval, executing, blocked | Plan validated; approval khi vượt authority; blocked nêu lý do |
| awaiting_approval | executing, blocked | Approval hợp scope/hash/version/expiry; deny/expired → blocked |
| executing | reviewing, blocked, failed | Output/evidence đủ; unknown outcome → blocked để reconcile, không tự coi failed là chưa chạy |
| reviewing | awaiting_acceptance, rework, blocked | Evaluation có criteria/evidence; không đạt → rework |
| rework | planning, executing, blocked | Run/attempt mới, scope/budget vẫn hợp lệ; sửa criteria/authority phải revision + duyệt lại |
| awaiting_acceptance | accepted, rework | Owner quyết định; agent/reviewer không tự accepted |
| blocked | queued | Owner hoặc handler giải được blocker trong quyền hiện có, đối chiếu checkpoints trước resume |
| queued, planning, awaiting_approval, executing, reviewing, rework, blocked, awaiting_acceptance | paused | Owner pause; lưu resume target, chặn dispatch; request đang chạy abort/reconcile riêng |
| paused | queued | Owner resume, recheck revision/lease/approval/budget; không nhảy giữa token |
| draft, queued, planning, awaiting_approval, executing, reviewing, rework, blocked, awaiting_acceptance, paused | cancelled | Owner cancel; scope cancelled không dispatch bước mới |

`accepted`, `failed`, `cancelled` là terminal task. Retry task failed/cancelled tạo task mới có `retry_of_task_id`, không sửa lịch sử terminal; retry run/step trong task còn hoạt động tạo attempt mới. Parent task hoàn tất khi children/evaluation đủ điều kiện; không tự accepted vì mọi child completed. Trường hợp run failed không bắt buộc terminal task failed: nếu được phép sửa/khôi phục thì task blocked hoặc rework.

### Run states

| State | Ý nghĩa | Bước tiếp theo hợp lệ |
| --- | --- | --- |
| queued | Chưa bắt đầu run | running, cancelled |
| running | Worker có lease đang chọn bước | waiting_model, waiting_tool, waiting_approval, paused, completed, failed, cancelled, reconciling |
| waiting_model | HTTP request đã gửi, chưa final response | running khi kết quả hợp lệ; interrupted/reconciling khi abort/crash; failed khi outcome xác định |
| waiting_tool | Executor đang làm action đã validated | running nếu có receipt; interrupted/reconciling nếu mất kết quả |
| waiting_approval | Chưa dispatch action cần duyệt | running khi approved đúng version; paused/cancelled/failed khi hết điều kiện |
| paused | Không có step đang in-flight, giữ checkpoint | running sau recheck hoặc cancelled |
| interrupted | Request/worker bị ngắt; outcome cần kiểm tra | reconciling; không tự gửi request/tool mới |
| reconciling | Đối chiếu receipts/events/artifacts/call ID và trạng thái thực | completed, failed, cancelled; nếu safe resume thì đóng run cũ cancelled với reason safe_resume và tạo run kế tiếp có resumed_from_run_id |
| completed | Có output/run evidence hợp lệ | Terminal; task còn chờ reviewer/Owner |
| failed | Failure đã xác định | Terminal; parent task chọn rework/blocked/failed theo quyền |
| cancelled | Dừng do Owner, không làm bước mới | Terminal; late usage vẫn reconcile vào call/ledger cũ |

Khi crash mất heartbeat, active run chuyển reconciling. Nếu không có bằng chứng outcome thì giữ reconciling/blocked để Owner xử lý; không claim thành công hoặc an toàn retry. Worker không dùng animation/elapsed làm bằng chứng agent đang suy nghĩ.

### Approval states

`pending → approved | rejected | expired | stale`. `approved → consumed` chỉ một lần khi action dispatch được atomically claim với permission check. Payload/revision/policy/grant thay đổi thì approval chưa dùng trở thành stale. Approval expired/consumed không authorize action khác; kể cả Owner click hai lần cũng không dispatch hai lần. Không đưa secrets vào approval payload hiển thị.

## 9. Event contract v1 và replay

### Envelope

| Field | Quy định |
| --- | --- |
| schema_version, event_id | 1, UUID duy nhất; consumer chấp nhận unknown type bằng generic view |
| type | Enum event bên dưới; thêm type là mở rộng có version/test |
| environment_id, company_id | UUID bắt buộc, authorization + composite FK |
| stream_seq | Integer dương, unique theo environment/company; cursor là seq, không dùng timestamp |
| occurred_at, recorded_at | ISO UTC; occurred_at từ nguồn, recorded_at từ backend; không dùng đồng hồ nguồn để sort commit |
| task_id, run_id, agent_id, employee_version_id | UUID hoặc null; event có run phải có task; active agent run có immutable profile ref |
| correlation_id, parent_event_id | Correlation UUID bắt buộc; parent nullable, cùng scope |
| source, actor | app/gateway_adapter/executor; actor owner/agent/system rõ, không từ model tự khai |
| sensitivity, payload | internal/confidential/public; validated payload đã redacted trước ghi; secrets không được persistence |
| evidence_refs, dedup_key | Authorized artifact/call/checkpoint refs; nguồn fingerprint để dedup trong scope |

`stream_seq` được cấp bằng khóa counter theo company trong transaction ghi state/event/outbox, tránh PG sequence có commit out-of-order làm cursor bỏ mất event. Event metadata append-only; retention/redaction purge nếu được Owner duyệt phải có tombstone/audit, không rewrite trạng thái lịch sử để làm đẹp báo cáo. Nội dung nhạy cảm dùng artifact ref/ACL riêng, không nhúng cả prompt/tool output vào SSE envelope.

### Danh mục event và payload tối thiểu

| Type | Payload tối thiểu / ý nghĩa | Phase tạo khả năng |
| --- | --- | --- |
| TASK_CREATED | task revision, goal ref, criteria ref | 03 |
| TASK_QUEUED | job ref, priority, ready_at | 09 |
| TASK_STARTED | run/assignment refs | 06 |
| AGENT_ASSIGNED | employee/version, task/run | 06 |
| PLAN_UPDATED | plan version/ref, summary tường minh | 06 |
| LLM_CALL_STARTED | request_span_id, model/effort, grant/reservation ref | 06 |
| LLM_CALL_COMPLETED | request_span_id, gateway_call_id nullable, response ref, usage availability | 06 |
| LLM_CALL_FAILED | request_span_id, sanitized error, outcome known/unknown | 06 |
| TOOL_CALL_STARTED | tool action/receipt key, schema/policy/approval refs | 11 |
| TOOL_CALL_COMPLETED | receipt/result/artifact refs, exit code nếu có | 11 |
| TOOL_CALL_FAILED | action ref, sanitized error, outcome known/unknown | 11 |
| TOKEN_USAGE_RECORDED | call ref, input/output/cache nullable, source, measurement status | 06 |
| AGENT_HANDOFF | from/to versions, parent/child task refs, handoff artifact | 12 |
| APPROVAL_REQUESTED | approval ID, action summary, payload hash/version/expiry | 10 |
| APPROVAL_DECIDED | approval ID, Owner decision, bound hash/version | 10 |
| EVALUATION_COMPLETED | evaluator/suite versions, criterion verdicts, evidence refs | 12, 17 |
| TASK_COMPLETED | delivery manifest, evaluation refs; awaiting_acceptance | 09 |
| TASK_ACCEPTED | Owner decision, task revision, evaluation refs | 09 |
| TASK_REWORK_REQUESTED | criteria failed, new attempt/revision refs | 09 |
| TASK_PAUSED | actor/reason/resume target | 09 |
| TASK_RESUMED | rechecked revision/grant/checkpoint refs | 09 |
| TASK_FAILED | final known failure, evidence refs | 06 |
| TASK_CANCELLED | Owner decision and in-flight outcome summary | 09 |
| TASK_STATE_CHANGED | old/new state, expected transition version, actor and reason ref | 03 |
| RUN_STATE_CHANGED | old/new state, checkpoint/reason, expected revision | 06 |
| RUN_CREATED | run text-only đã ghi, grant ref; chưa có dispatch | 06 |
| RUN_STOP_REQUESTED | yêu cầu dừng, in-flight và trạng thái cancellation còn cần xác minh | 06 |
| EXECUTION_GRANT_CREATED | Owner, phase/batch/limits/expiry; không bỏ CG01 | 06 |
| OWNER_MODEL_PROFILE_UPDATED | Owner profile version/model/effort/fallback config; không cấp inference | 06 |
| BUDGET_RESERVED | grant/reservation, limit basis and amount nullable | 06, 16 |
| BUDGET_SETTLED | call/reservation/ledger refs, known/unknown status | 06, 16 |
| INCIDENT_DETECTED | incident ID, run/cause/evidence refs | 19 |
| EMERGENCY_STOP_CHANGED | enabled, Owner/reason, scope and durable epoch | 06, 19 |
| MEMORY_PROMOTED | layer/version/evidence/approval refs | 15 |
| EMPLOYEE_VERSION_CREATED | old/new version, Owner/config refs | 13 |

Schema registry tồn tại từ Phase 03, nhưng không giả lập activity thật của các phase chưa triển khai. Fixtures ở Phase 04 có `fixture=true` và chỉ trong demo. Một event minh họa, không có lượt model:

```json
{
  "schema_version": 1,
  "event_id": "40000000-0000-4000-8000-000000000001",
  "type": "TASK_CREATED",
  "environment_id": "20000000-0000-4000-8000-000000000001",
  "company_id": "30000000-0000-4000-8000-000000000001",
  "stream_seq": 1,
  "occurred_at": "2026-10-08T00:00:00Z",
  "recorded_at": "2026-10-08T00:00:00Z",
  "task_id": "10000000-0000-4000-8000-000000000001",
  "run_id": null,
  "agent_id": null,
  "employee_version_id": null,
  "correlation_id": "50000000-0000-4000-8000-000000000001",
  "parent_event_id": null,
  "source": "app",
  "actor": {"kind": "owner", "id": "owner-local"},
  "sensitivity": "internal",
  "payload": {"task_revision": 1, "fixture": true},
  "evidence_refs": [],
  "dedup_key": "fixture:task-1:revision-1:created"
}
```

### Persistence, live và replay

SSE `/api/v1/events?after_seq=…` là backend → frontend; scope từ session, không proxy raw gateway/CLI logs. Khi reconnect, replay các event `seq > cursor`; UI dedup theo event_id. Heartbeat không là domain event. Cursor vượt retention thì trả reset/gap response rõ và snapshot + valid cursor; không silently skip. Live views là projections từ dữ liệu đã commit, rebuild được từ events/snapshots và không thay execution state. Replay đọc event/checkpoint/artifact đã authorized; không dispatch model/tool.

## 10. Quyền, auth và inference gates

### Owner local và actor agent

V1 dùng một Owner bootstrap credential do máy local tạo khi Phase 01 setup; không có credential mẫu hardcoded. Backend nhận bootstrap credential để mở server session, cookie HttpOnly/SameSite=Strict, Origin/Host allowlist và CSRF protection cho mutation. Secret ref gateway và session signing nằm phía server. Bind trực tiếp loopback; hostname/proxy chỉ bật sau kiểm tra exposure, auth và route. Remote/multi-user không thuộc V1. Trong dev loopback HTTP không claim cookie Secure/TLS; trước remote bắt buộc thiết kế riêng.

Agents dùng scoped internal identity/run grant, không giữ Owner cookie/token. UI Chairman/Operator chỉ là cách nhìn cùng quyền; hidden button không bảo vệ API. Backend luôn đánh giá action/schema/scope/policy/approval/budget; executor kiểm tra capability và boundary trước side effect.

### Ma trận thẩm quyền

| Hành động | Tự động | Trong ủy quyền | Chủ tịch bắt buộc |
| --- | --- | --- | --- |
| Đọc inputs được cấp, phân tích, draft, test trong sandbox | Khi grant/scope cho phép | Giới hạn tool/network/time | Nếu vượt scope hoặc chưa có grant |
| Giao subtask/gọi worker/retry an toàn | Không tự sinh vô hạn | Fan-out/depth/iterations + budget còn | Tăng phạm vi, thêm quyền hay ngân sách |
| Tuyển/offboard nhân viên cố định, đổi model/tools/context policy | Chỉ đề xuất | Không tự áp | Luôn |
| Tăng budget/autonomy, sửa Hiến pháp/Owner config | Chỉ đề xuất | Không tự áp | Luôn |
| External send/deploy production/xóa dữ liệu quan trọng | Chỉ proposal | Không là quyền tự động mặc định | Luôn; V1 không có connector này nếu chưa có allowlist |
| Accepted task, gỡ Emergency Stop, real onboarding sau release | Không | Không | Luôn |
| Ghi memory lesson | Chỉ đề xuất + evidence | Reviewer có grant duyệt memory trong scope | Owner nếu corporate/policy-sensitive; memory không sửa policy |

Approval hash là SHA-256 của canonical action payload: schema-validated JSON, UTF-8, keys sorted, amounts integer micros, không float/nonfinite; gồm action_type, payload, environment/company/task/run/revision, policy/grant version, expiry. Quy tắc canonicalization được contract-test ở Phase 10. Consume approval + reserve budget + claim dispatch trong transaction; policy/stop epoch recheck trước executor. Cancel/expiry trước dispatch không tạo side effect. Dispatch decision và stop epoch được serialize; action đã commit dispatch trước stop là in-flight, có thể kết thúc sau stop. Executor recheck trước tác dụng phụ, run report phân biệt pending/aborted/in-flight/unknown; không hứa dừng hồi tố.

### Quy tắc inference mặc định đóng

Hạn mức được cấp hiện tại = 0. Nút “Chạy thử” chỉ xuất hiện hoạt động sau Owner cấp một grant có environment, model/effort, mục đích, số request tối đa, concurrency, thời gian, expiry và capability profile. Chấp nhận Phase 00/01 hoặc health check không phải cấp grant. Cấu hình grant hết hạn/missing/capability chưa verified/stop active thì deny trước POST. Không mở trang, seed/reset hoặc chạy document validator mà gọi model.

Mỗi inference grant gắn **một đợt test cụ thể**, không phải quyền toàn dự án hay quyền của một phase. Record bắt buộc: grant_id/version, phase_id, test_batch_id, mục đích/test cases, environment/company, model/effort, capability/input scope, max requests (kể cả retry/rework và child calls), concurrency, timeout/resource/cost limits với basis/unknown caveat, expiry, Owner và thời điểm cấp. Worker recheck phase + batch + purpose + scope + hạn mức/expiry/stop trước từng request. Grant thiếu field hoặc không khớp đợt đang chạy thì deny.

Hoàn tất/hủy/fail đợt test, hết hạn, revoke hoặc chuyển phase kết thúc quyền dispatch của grant. Dư hạn mức không chuyển sang đợt/phase khác; không kế thừa grant từ parent task, benchmark, phase trước hoặc nghiệm thu milestone. Đợt tích hợp IG08/IG12/IG16/IG20 có inference cần Chủ tịch cấp grant riêng đúng batch; chỉ có fixture tests thì không cần inference grant. Chạy lại một batch sau khi đã kết thúc là đợt mới với grant mới; usage tới muộn vẫn settle vào call/grant gốc mà không mở quyền gọi thêm.

Candidate test grant trước Phase 06: **1 request text-only**, concurrency 1, client timeout 120 giây, expiry 1 giờ, không tools/fallback và inputs fixture tin cậy. Đây là phương án chờ Chủ tịch cấp riêng, không là authorization hiện tại. Giá/usage chưa biết thì không có USD hard cap; Owner phải thấy rõ hạn mức tài nguyên và chi phí API-equivalent chưa là hóa đơn subscription.

## 11. Ngân sách, đo lường và giới hạn vận hành

### Giá trị mặc định đóng / các trần thiết kế

| Kiểm soát | Baseline V1 | Ý nghĩa |
| --- | --- | --- |
| Inference grant | 0 requests cho mọi demo/benchmark/real khi chưa được cấp | Deny dispatch; không dùng ngân sách mẫu $50 trong ý tưởng |
| Gateway adapter concurrency | Tối đa 1 request từ app, không đổi concurrency server chung | 429 → queued bounded backoff; không giữ lock DB trong HTTP |
| Client request timeout | 120 giây, ≤ timeout đã probe/config của gateway; nếu gateway ngắn hơn thì dùng ngắn hơn | Timeout không chứng minh provider chưa tiêu usage |
| Context envelope app | Tối đa 128 messages và 256 KiB encoded JSON | Compact theo complete tool round-trip units; không bỏ lẻ tool result, không silent truncate criteria/policy |
| Retry 429 chắc chắn chưa dispatch | Tối đa 2 retry, backoff 1 rồi 3 giây, vẫn phải trong grant/expiry | Có attempt event; 502/504/disconnect không auto retry |
| Tool request | Timeout 60 giây, output tối đa 256 KiB; artifact lớn ghi manifest, không nhúng SSE | Phase 11 kiểm chứng isolation trước bật |
| Pause/stop | Chặn bước mới tức thời ở command/dispatch; in-flight cancellation phải xác minh | Không hứa hoàn tác side effect đã gửi ra ngoài |
| Worker lease/heartbeat | 30 giây / 10 giây (mục tiêu cấu hình, Phase 09 đo thực) | Lease mất → reconciling, không tự chạy lại tool |
| Scheduling | Asia/Ho_Chi_Minh; miss policy skip mặc định, catch-up chỉ Owner cấu hình | Job key + occurrence unique, không thực thi khi máy tắt |
| Retention | Không tự purge evidence/real artifacts trong V1 mặc định | Owner policy + preview/backup + audit trước xóa; stream pagination để tránh tải vô hạn |

Đây là trần/mặc định thiết kế, chưa được chứng minh trên máy. Owner grant có thể thấp hơn; tăng trần/resource permissions phải được duyệt, không sửa từ model proposal. Nội dung tool/prompt nhạy cảm mặc định không lưu raw; giữ redacted artifact hoặc hash/provenance theo ACL. Approved context/history được lưu riêng dưới ACL của run để tiếp tục; không đưa toàn bộ history vào log/SSE. Nếu policy không cho lưu nội dung, resume cần Owner cấp lại input, không tái tạo bằng nội dung bịa. Logs/SSE không chứa credentials.

### Ledger contract

Một app `request_span_id` tạo tối đa một final usage entry theo call + source/version; gateway call ID có thể thiếu. Input/output/cache là `integer|null`; total = input + output khi đủ nguồn, cache nằm trong input, reasoning nếu có nằm trong output và không cộng lần hai. Không suy token từ text. Usage tới muộn được reconcile bằng record có source/correction reference, không overwrite snapshot giá lịch sử.

Ledger drilldown dùng HTTP call/turn là mức quan sát hiện tại. Gateway/native/global dashboard không cộng vào app costs; shared gateway requests khác không mang company_id của app. Cost fields gồm basis `actual_api|subscription|api_equivalent|local_compute|unknown`, currency, amount_micros nullable, price_version/source_at, measurement `confirmed|estimated|unknown`. Subscription không có hóa đơn từng call: API-equivalent luôn nhãn “Ước tính tham khảo”, không là chi phí trả thực. Unknown usage không release reservation như 0 usage; giữ unresolved và chặn cấp thêm theo grant cho đến reconcile/Owner xử lý.

Reserve resource/cost atomically trước dispatch, settle/release khi outcome có bằng chứng; concurrency không chia vượt cùng một grant. Không cam kết token hoặc USD hard cap giữa một request vì gateway không nhận max_tokens. Sau final usage, chặn bước tiếp nếu hết hạn mức; báo overshoot của request đang chạy nếu có. Nếu không có upper bound pricing/token đáng tin, chọn resource grant và Owner chấp nhận rủi ro, không quảng cáo USD cap chắc chắn.

## 12. Tách môi trường, lịch và vận hành local

`demo`, `benchmark`, `real` là namespaces bất biến, không chỉ một UI badge. Mọi SQL/query/event/stream/artifact/context và app call mapping cùng scope; reset chỉ nhận demo environment đã authorized, không wildcard theo path. Với gateway shared, app gửi stateless request và không quản lý/xóa sessions/transcripts/native SQLite của gateway; metadata gateway chung không là báo cáo công ty. Trace/privacy warning nêu rõ app redaction không kiểm soát rollout nguồn. Benchmark fixtures/reports không nhập KPI real.

Sơ đồ file tương lai: `storage/<environment_uuid>/<company_uuid>/<task_uuid>/<run_uuid>/<artifact_uuid>` với manifest xác minh root/symlink và hash; demo reset tính phạm vi từ DB và manifest, không nhận absolute path từ UI. Backup bao gồm DB + artifacts + config references; auth secrets backup riêng có kiểm soát, không nhét vào archive chia sẻ. Restore không tự gỡ stop, tạo model request hoặc chạy lại tool; phải reconcile checkpoint/outcome.

Port block chỉ reserve ở Phase 01 sau đọc registry và kiểm tra toàn block/listeners. Không chọn port 3000/8000 tùy ý. Codex gateway giữ 127.0.0.1:15600, là dependency ngoài allocation Agent Corporation, không move/restart để phục vụ phase này. Proxy Dev Hub hiện publish 80 wildcard: không bật route quản trị vào ingress đó khi chưa chứng minh local-only access và auth/Host/Origin behavior. Default usable runtime sẽ là direct loopback sau khởi động thành công; hostname .localhost là lựa chọn dự kiến, không claim đã hoạt động.

Machine sleep/offline không có agent execution thực. Schedules dựa trên durable job occurrence key; skip mặc định, catch-up phải Owner cấp. Báo cáo chỉ dùng task/event/ledger nguồn trong interval và environment; AI summary phải dẫn evidence. Không định kỳ gọi tất cả trưởng phòng khi không có việc.

## 13. Chất lượng, KPI và release gates

### Các chỉ số có định nghĩa trước

| KPI | Tử số / mẫu số và phạm vi | Khi không đủ dữ liệu |
| --- | --- | --- |
| Cost per accepted task | Chọn cohort task có accepted_at trong kỳ, cùng environment/company; tổng chi phí trọn đời của các task trong cohort / số task trong cohort, theo từng cost basis/currency | Cohort rỗng hoặc có unknown usage/cost → chưa tính đầy đủ; hiển thị coverage và as_of |
| Period operating cost | Tổng chi phí mọi call/resource phát sinh trong kỳ theo occurred_at, cùng environment/company và cost basis/currency, bất kể task đã accepted hay chưa | Unknown/late usage → partial/unknown và coverage; không chia cho số task accepted trong kỳ |
| First-pass success | Task đạt evaluation đầu tiên / task có first evaluation cuối cùng trong kỳ | Chưa review không đưa mẫu số; không suy từ model completed |
| Rework cost | Calls gắn attempt rework theo task/run trong kỳ | Missing usage/price → partial/unknown, không 0 |
| P50/P95 latency | Calls đã dispatch có start/end đủ bằng chứng trong kỳ; include known failure, tách status | Báo số mẫu và missing durations; không bịa elapsed sau crash |
| Human intervention | Task có Owner intervention ngoài submission/acceptance thường lệ / task đã bắt đầu trong kỳ | Approval strict thường lệ báo riêng, không lẫn escalation |
| Budget utilization | Confirmed/estimated spend theo cost basis / grant tương ứng; resources usage riêng | Không chia actual với API-equivalent; unknown có nhãn |
| Benchmark score | Verdict theo versioned suite/criteria; cùng constraints và dataset | Cỡ mẫu nhỏ/LLM judge không là chứng minh thắng chắc |
| Idle capacity | Hồ sơ available không có assignment / active employee profiles ở thời điểm đo | Không đồng nghĩa lãng phí, không dùng làm lý do sa thải tự động |

### Chi phí trọn đời và kỳ báo cáo

`Cost per accepted task` lọc cohort bằng `accepted_at`, không lọc call bằng kỳ phát sinh. Lifetime cost của mỗi task gồm mọi model call, attempts/retries, rework, review và child subtasks thuộc task đó từ lúc tạo đến nghiệm thu, kể cả phát sinh ở kỳ trước. Mỗi ledger entry chỉ tính một lần: roll up descendants bằng ownership/task lineage, không cộng cả tổng cha lẫn tổng con. Báo cáo root-task và báo cáo child-task là các cohort riêng, không cộng hai lớp. Task retry độc lập có `retry_of_task_id` vẫn là task khác, không nhập ngầm vào lifetime của task được accepted; chi phí task thất bại ngoài cohort thuộc period operating cost và báo cáo thất bại riêng.

Ví dụ minh họa, không là dữ liệu thật: một task phát sinh 2 USD trong tháng 9 và 3 USD trong tháng 10, được accepted tháng 10. Lifetime cost là 5 USD, cohort tháng 10 gồm đủ 5 USD; period operating cost ghi 2 USD tháng 9 và 3 USD tháng 10. Không đưa 2 USD vào operating cost tháng 10 và không bỏ nó khỏi lifetime cost. Chỉ cộng cùng cost basis/currency; không cộng API-equivalent với actual/subscription thành một số.

Late usage/correction gắn lại call gốc và thời điểm phát sinh, không lấy recorded_at làm kỳ chi phí. Báo cáo cohort đã xuất có `as_of`, ledger/report version và completeness; correction tạo phiên bản báo cáo mới, giữ bản cũ có thể audit. Unknown không bằng 0; không công bố giá trị chính xác khi lifetime chưa đủ nguồn. Grant hết hạn không cản nhận/reconcile usage của các request đã được cấp phép trước đó.

Mọi KPI có interval/timezone/filter/source version và drilldown. Benchmark model/profile so cùng inputs/tools/policy/grant, repeated sample nếu ngân sách cho phép; primary evaluator dùng test xác định, human review cho tiêu chí không tự động. Đổi model/context/HR là proposal + experiment evidence + Owner approval + rollback snapshot.

### Release criteria baseline để nghiệm thu

| Gate | Điều kiện bắt buộc | Cách kiểm chứng ở Phase 23 |
| --- | --- | --- |
| R1 | Ít nhất 3 kịch bản sandbox thật: thành công, reviewer yêu cầu sửa, approval bị từ chối | E2E artifacts/tests/Owner decisions/trace; inference chỉ trong grant được cấp |
| R2 | Inspector/replay từ events đã lưu; reconnect không mất/nhân đôi; p95 commit-confirmed → DOM render ≤ 2 giây | Load fixture 20 hồ sơ agent, 10.000 events, ít nhất 200 phép đo; công bố browser/máy/version và timing instrumentation, không fake 20 agent inference |
| R3 | 0 bypass thành công trong suite owner-only/cross-scope/stale approval/tool escape/secret leak | Negative API/executor/DB tests; approval double-submit race |
| R4 | 0 dispatch mới sau hết grant/reservation; reconcile không trùng; unknown/estimate rõ | Parallel reserve/settle + late usage + failure cases; không hứa hard cap trong request |
| R5 | Stop durable, cancel/restart/worker death/loop/offline xử lý an toàn | Fault injection; kiểm chứng abort gateway, no replay side effect và incidents |
| R6 | Demo reset/benchmark/real isolation đạt; company thật chưa tạo trước release decision | Cross-environment/FK/RLS/artifact/session mapping tests |
| R7 | Restore DB/artifacts/config refs vào môi trường sạch, counts/hash/links đúng | Backup/restore manifest và migration drill; stop giữ nguyên |
| R8 | Cài/chạy theo docs, UX tiếng Việt/mobile 390 px/keyboard; 0 blocker/nghiêm trọng chưa xử lý, Owner chấp nhận V1 | Local install check, rendered UX QA, known limits + release manifest + Owner decision |

Các ngưỡng R2/R8 là baseline đặc tả đã được Chủ tịch nghiệm thu, chưa phải kết quả đo. Performance không hợp lệ nếu browser cache/fixture tránh đường persistence thật; test fixture tải lớn không thay thế run sandbox thật ở R1. Mọi gate chưa kiểm chứng runtime trong Phase 00.

### Integration verification gates trong và giữa các milestone

Các checkpoint sau kiểm chứng **tích hợp những phần đã triển khai**, không thêm feature hoặc thay thứ tự phase. Bắt buộc ghi report PASS/FAIL, môi trường/config/version, test batch/grant nếu có, commands/results và event/artifact/ledger refs. PASS không tự cho phép chạy phase tiếp; FAIL giữ phần liên quan Bị chặn, cần sửa trong scope được giao và kiểm chứng lại. Không dùng mock để đạt tiêu chí yêu cầu run thật. IG03 được kiểm chứng lại cùng Phase 04 batch `20261008T154151+0700-demo-factory` bằng test Phase 03 persistence/transaction/dedup/RLS (xem [report Phase 04 C07](tests/results/phase-04/20261008T154151+0700-demo-factory/report.md)); IG08/12/16/20 vẫn **Chưa thực hiện**. Việc này không tự nghiệm thu phase hoặc cấp quyền inference.

| Gate | Sau phase / trước phase | Luồng tích hợp và bằng chứng bắt buộc | Inference / cách xử lý FAIL |
| --- | --- | --- | --- |
| IG03 | Sau 03 / trước 04 (nền tảng A) | API → PostgreSQL → task revision/state + event/outbox cùng transaction; rollback/restart/dedup/cross-scope deny; fixture test tối thiểu, không triển khai Demo Factory trước 04 | Không inference; sai atomicity/isolation thì blocked trước seed demo |
| IG08 | Sau 08 / trước 09 (quan sát B) | Run text-only sandbox thật → event đã lưu → SSE → Live Office/Inspector → replay; reconnect/filter/error/usage unknown và no replay side effect; đối chiếu IDs, không yêu cầu tools Phase 11 sớm | Grant riêng của đợt IG08 nếu chạy model; CG01/trace gap thì blocked, không dùng fixture để thay run thật |
| IG12 | Sau 12 / trước 13 (tổ chức C) | Work Order → supervisor/worker → permission/approval → sandbox tools → reviewer/rework → manifest; handoff correlation, budget/stop propagation và no duplicate side effect | Grant riêng của đợt IG12; failed handoff/policy/evidence thì blocked trước mở rộng HR/org |
| IG16 | Sau 16 / trước 17 (đo lường D) | Run/call/usage → ledger/reservation/pricing → finance drilldown; parallel reserve/dedup/late usage/unknown; cohort accepted task xuyên kỳ tính đủ lifetime, period operating cost không đổi kỳ | Fixture ledger cho edge cases + run thật với grant IG16 riêng nếu gọi model; mismatch/overcount/unknown bị ghi 0 thì FAIL |
| IG20 | Sau 20 / trước 21 (D → hoàn thiện E) | Task/events/ledger/incident → persistent schedule → daily/monthly report và proposal inbox; sleep/restart/missed job dedup, nguồn số khớp query, stop không tự gỡ | Fixture clock/DB kiểm tra lịch; grant IG20 riêng cho summary inference nếu cần; số báo cáo sai hoặc bỏ gate runtime trước đó thì blocked onboarding |

Report IG phải liên kết các checkpoint trước đã PASS hoặc chỉ rõ phần chưa đạt; IG20 không bù việc thiếu IG08/IG12/IG16. Release Phase 23 kiểm tra evidence của cả IG03/08/12/16/20 bên cạnh R1–R8. Không chạy các gate này trong Phase 00; chỉ định nghĩa cách nghiệm thu tích hợp cho các phase tương ứng.

## 14. Ma trận yêu cầu → phase → tiêu chí kiểm chứng

Nguồn `I1` là ý tưởng tập đoàn; `I2` là xây sản phẩm trước. `P` là diễn giải thiết kế từ master-plan; `G` là source gateway quan sát. Mỗi yêu cầu có một bằng chứng/test cụ thể, không chỉ một màn hình.

| Requirement | Nguồn | Yêu cầu | Phase | Tiêu chí / bằng chứng |
| --- | --- | --- | --- | --- |
| REQ01 | I1/I2 | Chủ tịch quyết định chiến lược và nhịp phase | 00, 10, 23 | Phase00 đã nghiệm thu đặc tả; agent không đổi policy; release Owner decision riêng |
| REQ02 | I2 | Build product trước real onboarding | 04, 21, 23 | Real release lock + demo reset isolation; S14 guarded |
| REQ03 | I1 | Chairman/Operator Mode cùng quyền Owner | 02, 10 | S01/S13 navigation; đổi mode không cấp thêm quyền API |
| REQ04 | I2 | Ba tầng Dashboard/Live Office/Inspector | 02, 07, 08 | S01–S03 correlation tới event/run thật; R2 |
| REQ05 | I2 | Replay đọc bằng chứng, không chạy lại | 03, 08 | S04 cursor/filter/ACL; 0 new POST/tool khi replay; R2 |
| REQ06 | I1 | Nhân viên on-demand, versioned persona/capability/policy | 13, 14 | S07 immutable run snapshot; idle không inference |
| REQ07 | I1 | Work Order có goal/output/criteria/scope/budget/deadline/stop | 03, 09 | Section 7 contract, F01; invalid submit/transition tests |
| REQ08 | I2 | Event store và execution state từ đầu | 03, 07 | Section 9 envelope, state/event/outbox atomic; dedup/reconnect/crash |
| REQ09 | I1/I2/G | Dùng codex-server HTTP local | 05, 06 | Section 6 request contract, health/model probe; authorized live smoke riêng |
| REQ10 | I2/G | Live không bịa tokens/suy nghĩ nội bộ | 06, 08 | S03 waiting model/explicit summary; usage unknown; no raw CoT dependency |
| REQ11 | I1/I2 | Default deny, sandbox và grants trước inference | 06, 10, 11 | Section 10 grants riêng theo phase/test batch, không kế thừa; CG01/R3/R4 |
| REQ12 | I1 | Approval owner-only, hash/version/expiry | 10 | S06 payload tamper/stale/replay/cross-scope/consume race; R3 |
| REQ13 | I1 | Tools file/code/terminal/browser trong sandbox | 11 | S03 receipts/diff/exit code; traversal/symlink/network allowlist tests |
| REQ14 | I1 | Chief of Staff → worker → reviewer, task nhỏ gọn | 12 | F01/F03, handoff DAG/fanout/budget/cancellation tests; R1 |
| REQ15 | I1 | Department/reporting lines và 3 loại hợp đồng | 13 | S07 org cycle/cross-company/lifecycle integrity |
| REQ16 | I1 | HR proposal/probation/offboard có Owner | 14 | F06/S06/S07; không tuyển tự động, stop/drain/offboard evidence |
| REQ17 | I1 | Context 5 lớp, ACL và memory promotion | 15 | S08 provenance/version, cross-scope deny, rollback không sửa history |
| REQ18 | I1/G | Ledger nguồn thật, drilldown, price snapshot | 06, 16 | S09 call mapping/dedup/late usage/unknown, lifetime cohort/period cost; IG16/R4 |
| REQ19 | I1 | Ngân sách cạnh tranh an toàn và cost basis đúng | 06, 16 | Resource reservation races, không sum native/shared cost; R4 |
| REQ20 | I1 | KPI, benchmark, model tournament có suite | 17 | S10 versioned fixtures/evaluator/denominators/sample size |
| REQ21 | I1 | Optimization/experiment, Owner áp và rollback | 18 | F06/S06/S10; rejected proposal không sửa config |
| REQ22 | I1/I2 | Incident/timeout/stop và recovery | 06, 19, 22 | F04/F05/S11, failpoints/stop epoch/reconcile; R5 |
| REQ23 | I1 | Lịch/báo cáo ngày tháng, máy ngủ không bịa hoạt động | 20 | F07/S12, schedule dedup/miss/reports query evidence |
| REQ24 | I1/I2 | Onboarding thật sau V1, chỉ Chief of Staff | 21, 23 | F08/S14 transaction/double-submit/release lock; R6 |
| REQ25 | I2 | Auth/secrets/backup/migration/restore | 01, 10, 22 | Section 10/12 auth boundary + RLS, S13 restore manifest; R3/R7 |
| REQ26 | I2/P | UX Việt, accessible, cài local và release đo được | 01, 02, 23 | S01–S14 lang/favicon/states/390px/keyboard/local install; R8 |

## 15. Quyết định đóng và điểm cần xác minh sau này

Chi tiết/rationale trong [ADR-0001](decisions/0001-v1-foundation.md). D01–D08 đã được Chủ tịch nghiệm thu về đặc tả/baseline sau khi bốn điều chỉnh review hoàn tất và kiểm tra nhất quán. Nghiệm thu không cấp inference grant, model access hoặc quyền bắt đầu Phase 01.

| ID | Quyết định baseline | Người có thẩm quyền / người soạn | Ảnh hưởng |
| --- | --- | --- | --- |
| D01 | Build/test bằng demo trước real; 24 phase không tự chuyển | Chủ tịch / Codex soạn theo yêu cầu | Mọi phase |
| D02 | React/TS/Vite + FastAPI/Pydantic + PostgreSQL/SQLAlchemy/Alembic; modular monolith | Chủ tịch nghiệm thu / Codex chọn baseline | 01–03 |
| D03 | State machine + PG jobs/lease/outbox, app quản lý context, stateless HTTP gateway | Chủ tịch nghiệm thu / Codex | 03, 05–09 |
| D04 | Event envelope v1, stream_seq theo company, state/event atomic; SSE/replay đọc dữ liệu | Chủ tịch nghiệm thu / Codex | 03, 07–08 |
| D05 | Một Owner local, actor agents scoped; loopback/auth, RLS + service/executor checks | Chủ tịch nghiệm thu / Codex | 01, 03, 10 |
| D06 | Inference grant hiện tại 0; owner-only config, stop baseline, tools app sandbox | Chủ tịch cấp grant riêng / Codex thiết kế | 06, 10–11 |
| D07 | Usage final/call, unknown và API-equivalent tách actual; không native/global sum | Chủ tịch nghiệm thu / Codex theo source gateway | 06, 16 |
| D08 | 8 release gates và sample/load target theo Section 13 | Chủ tịch nghiệm thu / Codex | 17, 22–23 |

| Điểm theo dõi | Điều còn phải xác minh | Người quyết định / xử lý | Deadline / hành vi nếu chưa xong |
| --- | --- | --- | --- |
| O01 | Đã đóng: Chủ tịch nghiệm thu đặc tả/baseline bản 1.1 sau bốn điều chỉnh và validation | Chủ tịch | Đã nghiệm thu 08/10/2026; không cấp inference grant/model access/Phase 01 |
| O02 | Block/service mapping/version lock/dev prerequisites thực | Codex thực hiện khi được giao Phase 01 theo registry | Trong 01; không đổi stack để né lỗi, không claim URL chưa chạy |
| O03 | Auth gateway nếu enabled, model/effort entitlement và usage shape | Chủ tịch cung cấp secret ref/grant; Codex probe/test trong 05–06 | Trước inference; missing → deny |
| O04 | Cô lập inference/retention của gateway và tool sandbox thật | Codex kiểm chứng trong 05–06/11; thay environment/quyền do Chủ tịch | Trước task không tin cậy/side effect; fail → blocked, không sửa server shared |
| O05 | Cấp candidate test grant 1 request/120s/1h hoặc hạn mức khác | Chủ tịch | Trước bất kỳ POST inference; hiện 0 |
| O06 | Model pricing/account basis và khả năng USD bound | Chủ tịch xác nhận basis; Codex lấy nguồn có version | 06/16; unknown → resource grant, không quảng cáo hard USD cap |
| O07 | Performance/cancellation/restore đạt trên máy thật | Codex chạy test được cấp; Chủ tịch nghiệm thu | 06/07/22/23; target chưa đạt không báo release |

Không còn lựa chọn kiến trúc thiếu quyết định cho Phase 01–03: stack, auth boundary, scope, state/events và queue đã có baseline cụ thể. O02 là công việc discovery/reservation/version pin được giao cho Phase 01, không gán port trong đặc tả. O03–O07 không cản tạo skeleton/data contract nhưng là hard gates trước runtime/real release. O01 đã đóng theo chỉ dẫn nghiệm thu có điều kiện của Chủ tịch và kết quả kiểm tra đạt; không dùng thời gian chờ hay checkbox cá nhân làm bằng chứng nghiệm thu. O02–O07 vẫn chờ phase/grant riêng đúng phạm vi.

## 16. Cách nghiệm thu Phase 00 và bằng chứng

| Tiêu chí Phase 00 | Bằng chứng đã soạn | Trạng thái hiện tại |
| --- | --- | --- |
| Từng yêu cầu cốt lõi truy ra phase và tiêu chí | 26 requirements tại Section 14; 14 màn hình, F01–F08; R1–R8 | Đã kiểm tra tài liệu và được Chủ tịch nghiệm thu đặc tả |
| Không có điểm mở làm sai thiết kế 01–03 | Baseline D02–D05 + data/state/events; O02 quy trình thực hiện setup | Baseline giữ nguyên, đã được Chủ tịch nghiệm thu |
| Chủ tịch chốt V1 và cơ chế test inference | Sections 2/10/13, ADR-0001, candidate grant chưa cấp | Đã nghiệm thu cơ chế cấp grant riêng từng batch/phase; vẫn chưa có inference authorization |

Demo Phase 00 nằm trong Section 4 và stepper trên HTML; nó trình bày logic, không là run thật. Validation Phase 00 là kiểm tra scope, requirement references, states/events/examples, links, Markdown/HTML synchronization và syntax; không chạy product unit/E2E/inference tests. Kết quả/lệnh/hash nguồn trong [evidence report](evidence/phase-00.md).

Chủ tịch đã chỉ dẫn nghiệm thu sau khi hoàn thành bốn điều chỉnh và kiểm tra nhất quán. Các checks đạt, Phase 00 được ghi Hoàn tất về đặc tả/baseline; integration/release gates chưa chạy. Grant inference vẫn 0, không có model access được cấp và không có yêu cầu bắt đầu Phase 01. Dừng tại đây; phase tiếp chỉ triển khai khi được yêu cầu riêng.

## 17. Nguồn và lịch sử

- [I1 — Ý tưởng tập đoàn](sources/01-y-tuong-tap-doan.txt): nhân sự, authority, Work Order, finance, memory, operations.
- [I2 — Xây sản phẩm trước](sources/02-xay-san-pham-truoc.txt): 24 phase, 3 tầng observatory, durable events/state, demo/real isolation, V1 trước onboarding.
- [Master plan](master-plan.md): nguồn chuẩn trạng thái phase; đặc tả là nguồn chuẩn hợp đồng sản phẩm sau khi nghiệm thu.
- [G — Gateway README](../../codex-server/README.md), [schema](../../codex-server/src/schema.ts), [server](../../codex-server/src/server.ts), [provider](../../codex-server/src/provider.ts): contract hiện có; hash/time/probe trong evidence. Không truy auth/session/native transcripts.
- 08/10/2026: bản 1.0 bàn giao Phase 00; data/state/event/security/limits baseline đã soạn, chưa được Chủ tịch nghiệm thu; 0 inference, chưa bắt đầu Phase 01.

- 08/10/2026: bản 1.1 theo review Chủ tịch: lifetime accepted-task cost tách period operating cost; CG01 contingency; IG03/08/12/16/20; grant riêng theo đợt test/phase. Giữ nguyên baseline kiến trúc; chưa cấp quyền inference hoặc Phase 01.
- 08/10/2026: validation bản 1.1 đạt; ghi nhận nghiệm thu có điều kiện của Chủ tịch đã được đáp ứng. Phase 00 Hoàn tất về đặc tả/baseline; grant = 0, không gọi model, Phase 01 chưa được giao.
