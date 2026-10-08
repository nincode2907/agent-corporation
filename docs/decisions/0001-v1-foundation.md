# ADR-0001 — Baseline nền tảng V1

> Ngày: 08/10/2026 · Phase 00 · Trạng thái: Được nghiệm thu về đặc tả và baseline kiến trúc (Phase 00 Hoàn tất).
> Người soạn: Codex. Người có thẩm quyền chấp thuận: Chủ tịch. Chưa cấp inference grant hoặc quyền triển khai Phase 01.

[Đặc tả chuẩn](../product-spec.md) · [Bản trực quan](0001-v1-foundation.html) · [Theo dõi phase](../master-plan.html#phase-00).

## Bối cảnh

Hai ý tưởng yêu cầu nền tảng quản trị tập đoàn AI, quan sát bằng chứng và kiểm soát quyền/chi phí. Ý tưởng 02 ưu tiên xây/test toàn nền tảng trước thành lập thật. Gateway codex-server riêng đã có trên host, chỉ text request/response và tools dưới dạng proposals, không streaming/max_tokens. Phase 00 phải chốt đủ để 01–03 không scaffold theo giả định sai.

## Các quyết định và lý do

| ID | Phương án đã chọn để nghiệm thu | Rationale / phương án chưa chọn | Hệ quả cần thực hiện |
| --- | --- | --- | --- |
| D01 | Xây V1 bằng demo; real onboarding sau release; từng phase đợi yêu cầu | Khung 24 phase bản 02 thay roadmap vận hành công ty ngay của bản 01 | Real lock; không seed/thuê nhân viên thật trong development |
| D02 | React/TS/Vite; FastAPI/Pydantic; PostgreSQL/SQLAlchemy/Alembic; modular monolith | Giữ stack gốc, tách domain rõ; không thêm microservices/framework agent khi chưa cần | Phase 01 pin version; API/worker dùng cùng command handlers |
| D03 | PG persistent jobs/leases/outbox + state machine; HTTP gateway stateless; app giữ context | RAM queue mất restart; gateway session TTL/invalidation không đủ làm source of truth | Durable checkpoint, reconcile unknown, no automatic retry 502/504 |
| D04 | Event v1 ngay 03, state/event atomic, counter per-company, SSE từ app + read-only replay | UI state tạm hoặc timestamp cursor dễ mất trace; gateway không có live tokens | Source-backed view, dedup/cursor/gap policy, không bịa CLI events |
| D05 | Một Owner local, actor agent scoped, loopback/Host/Origin/session/CSRF, RLS + service/executor checks | Chủ tịch/Vận hành là mode UI, không hai authority; không chỉ prompt/UI enforcement | App DB role không bypass RLS; chưa bật route qua wildcard ingress |
| D06 | Inference mặc định 0, grant Owner riêng, tools do app sandbox, stop/resource limits trước 06 | Nghiệm thu spec không là consent tiêu usage; gateway read-only không bảo đảm đọc isolation | Phase 06 hard gate grant/capability; không thừa hưởng quyền Codex hiện tại |
| D07 | Usage final theo app HTTP call, provenance/pricing snapshot; unknown/estimate/actual tách | Global/native totals khác scope; giá API-equivalent không là hóa đơn ChatGPT | Ledger map request span/call ID; không hứa token/USD cap giữa request |
| D08 | R1–R8 release criteria và test targets cụ thể | Dashboard fixture đẹp chưa chứng minh runtime/governance/recovery | Thử run thật có grant, negative/race/load/restore tests trước real release |

## Ranh giới quyết định

Stack/data/state/auth/event/queue baseline đã có lựa chọn cụ thể cho 01–03. Chưa chọn service host ports hay exact library versions: Phase 01 phải khám phá registry/tooling thực tế rồi reserve/verify/configure, không là kiến trúc chưa chốt. Không dùng 4000 như allocation của Agent Corporation; nó là endpoint gateway đang có.

Thông tin cần xác minh khi đến gate: auth gateway nếu enabled, model entitlement/usage, inference isolation/retention, tool sandbox, pricing basis, cancellation và performance/restore. Những mục này có owner/deadline/deny behavior tại O01–O07 trong đặc tả. Không nới quyền gateway khi không đạt. Không có vấn đề mở yêu cầu thay stack hoặc event/state model ngay trước 01–03.

## Cơ chế thử inference để nghiệm thu

Grant hiện tại 0. Candidate trước Phase 06 là 1 request text-only, model/effort explicit, concurrency 1, client timeout 120 giây, expiry 1 giờ, fixtures tin cậy, tools/fallback off. Chỉ được chạy sau Chủ tịch cấp riêng và capability/privacy checks đạt. Unknown pricing dùng resource limit có thông báo, không coi đó là hard dollar cap.

## Hệ quả và trade-offs được ghi rõ

- PostgreSQL/RLS/outbox/queue tăng công việc nền Phase 03/09, đổi lại kiểm chứng được scope và restart-safe state.
- Stateless HTTP gửi lại context có thể tốn input tokens; context builder Phase 15 kiểm soát nguồn/kích thước, không dùng gateway sessions như shortcut durability.
- Gateway không streaming: UI chỉ live event của app, cập nhật usage sau response. Native token streaming là capability mở rộng riêng sau V1.
- Read-only gateway shared không là full read sandbox; prompt untrusted/secrets bị chặn cho tới inference isolation đạt.
- Approval payload/version coupling và idempotency receipts khiến retry nghiêm ngặt hơn, tránh lặp tác dụng phụ chưa biết.
- API-equivalent cost chỉ tham khảo; dashboard có coverage/unknown, không hứa chi phí số đẹp nhưng thiếu nguồn.
- Loopback/auth làm remote access ngoài V1; route Dev Hub chỉ bật sau chứng minh local boundary, không broadening binds/CORS.

## Kiểm chứng trước đổi trạng thái ADR

Kiểm tra traceability 26 requirement và screens/flows/state/events/gates; JSON examples, links, renderer và nguồn gateway snapshot. Phase 00 chỉ kiểm chứng tài liệu, không claim runtime tests đã đạt. Evidence tại [Phase 00](../evidence/phase-00.md).

ADR đã chuyển “Được nghiệm thu” theo chỉ dẫn Chủ tịch sau khi bốn điều chỉnh review và kiểm tra nhất quán đạt. Nghiệm thu vẫn không cấp inference grant/model access hoặc quyền chạy Phase 01. Thay baseline sau đó phải có ADR mới/rationale + cập nhật spec/master-plan/HTML, không sửa history giả đã chấp thuận từ trước.

## Làm rõ sau review Chủ tịch — bản đặc tả 1.1

Giữ nguyên D01–D08 và stack/adapter đã chọn. Bốn điều chỉnh là định nghĩa và checkpoint kiểm chứng, không mở rộng tính năng:

- Cost per accepted task: cohort theo accepted_at; tổng chi phí trọn đời của chính các task được nghiệm thu / số task cohort, gồm retries/rework/review/children được roll up không trùng, kể cả kỳ trước. Period operating cost tính riêng theo thời điểm phát sinh của mọi task/call. Coverage, cost basis và late correction/as_of như đặc tả mục 13.
- CG01: capability/isolation/privacy không đạt → blocked + gap report. Chủ tịch quyết định giữ blocked, test scope thu hẹp, hoặc phê duyệt riêng phương án instance cô lập/thay đổi cần thiết. Không tự sửa/nới quyền/restart gateway shared; baseline thay đổi cần ADR và authorization riêng. Gate cần run thật không được pass bằng mock.
- Integration gates IG03/IG08/IG12/IG16/IG20 kiểm chứng các phần đã triển khai trước tiếp bước tương ứng, theo bảng mục 13. Report/evidence PASS cần đủ; FAIL không tự bỏ qua. Hiện chưa chạy gate nào; PASS không cấp quyền triển khai phase kế tiếp.
- Grant chỉ cho một phase/test_batch_id với mục đích/cases, model/effort, môi trường/scope, hạn mức requests kể cả retry/children, concurrency/timeout/basis, expiry và Owner. Không kế thừa giữa các phase/đợt test; batch kết thúc hoặc fail thì đợt mới cần grant mới. Usage muộn chỉ reconcile grant cũ, không mở quyền gọi thêm. Hiện grant = 0.

Chủ tịch đã tuyên bố nghiệm thu Phase 00 về đặc tả/baseline sau khi bốn điều chỉnh được hoàn thành và kiểm tra nhất quán. Việc nghiệm thu không cấp grant/model access hoặc quyền bắt đầu Phase 01.

08/10/2026 — Bốn điều chỉnh đã hoàn tất, validation đạt; nghiệm thu Phase 00 về đặc tả/baseline có hiệu lực. D01–D08 giữ nguyên. Grant = 0; không gọi model, không bắt đầu Phase 01.
