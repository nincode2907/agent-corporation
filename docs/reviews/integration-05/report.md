# Agent Corporation — Integration Fix 05 report

**Kết quả:** functional synthetic vertical slice đã thực hiện trong stack local cô lập. Chưa phải nghiệm thu Phase 06–08 hoặc bằng chứng CG01 thật.

## Thay đổi

- Runtime Run nay gắn đúng demo employee và immutable EmployeeVersion. Service xác nhận company/environment, lifecycle active/probation, version hiện hành, Owner grant và policy. Run/profile snapshot, system context và event đều giữ employee/version; historical Run không assignment hiện “Chưa phân công nhân viên”. Không migration mới.
- Thêm Owner-only `GET /api/v1/runtime/employees`; tạo Run yêu cầu employee/version. UI hiển thị employee, model/effort, grant/limit, CG01, task/run state, usage/cost provenance và synthetic label.
- Compose Runtime worker chạy được nền dưới PostgreSQL advisory-lock singleton, giữ lock trên cùng connection, phục hồi lease hết hạn thành `unknown` không replay, và tách biệt khỏi Playground queue.
- Office hiển thị Run cùng employee/task/state; Inspector/Replay deep links theo `run_id`. Replay chỉ đọc và giữ event filter khi reload.
- Pre-HTTP shutdown là known failure và giải phóng dispatch guard. Request đã gọi nhưng không có final response vẫn là `unknown`, không retry.
- Đã sửa mapping Phase 07 r009 theo criterion ID; r009 đổi phạm vi P07-03 và có aggregate lệch. [Bản đính chính](evidence/phase-07-r009-classification-correction.md) ghi cumulative latest evidence **13 clean/2 blocked/0 fail**; Phase 07 vẫn Bị chặn.

### File liên quan Fix 05

- API/runtime: `apps/api/src/agent_corporation_api/modules/execution/{router.py,service.py,worker.py}`; `apps/api/src/agent_corporation_api/modules/observability/{events.py,feed.py}`.
- UI: `apps/web/src/{App.tsx,RuntimePanel.tsx,RuntimePanel.css}`.
- Worker deployment/test: `compose.yml`; `apps/api/tests/{test_phase06_runtime.py,test_phase06_runtime_persistence.py,test_cg01_demo_mode.py,test_sensitive_validation.py}`; `scripts/test_playground_isolated.py`; `scripts/test_integration05_stack.py`; `scripts/integration05_fake_api.py`; `scripts/integration05_fake_worker.py`.
- Docs/evidence: `docs/master-plan.md`, generated `docs/master-plan.html`, and all deliverables/evidence under this directory.
- Không có migration schema.

## Kiểm định

| Hạng mục | Kết quả |
|---|---|
| Toàn API suite trong DB/role PostgreSQL disposable | **250 passed, 3 skipped, 1 Starlette deprecation warning**, 26.48 giây. DB/role disposable đã bị xóa bởi runner; runtime data không đổi. |
| Web production build | `rtk npm run --prefix apps/web build` — đạt (`tsc -b`, Vite build). |
| Desktop browser | Chrome, viewport capture 1440×900: Run waiting, Office, employee → Inspector đúng Run, Replay đúng Run. |
| Mobile browser | Chrome, 390×844: Office, Inspector, Replay. `html.clientWidth=390`; ảnh evidence đúng 390×844. Không tràn ngang. |
| Fake transport vertical slice | 3 Run hoàn tất; mỗi Run 1 model_call, đúng một EmployeeVersion, 10 event correlation cùng Run/task/employee/version, deterministic response và usage. |
| Replay read-only | Seek + reload; trước/sau giống nhau: 3 Run, 3 model_call, 54 event, 8 Work Order, 4 artifact, 9 checkpoint, 3 grant request. |
| Shared demo readiness | API/Nginx health 200; demo dashboard API/Nginx/hostname HTTP 200, `available=true`; UI fixture nạp thành công. Không reset dữ liệu dùng chung. |

Lệnh API: `rtk uv run --project apps/api python scripts/test_playground_isolated.py`. Lệnh web: `rtk npm run --prefix apps/web build`. Stack trình duyệt được tạo bằng `scripts/test_integration05_stack.py`, với database/volumes riêng, credential Owner giả, catalog giả, fake gate adapter và fake worker transport. Không gọi gateway; env `RUNTIME_CG01_DEMO_TEST_OVERRIDE=false`. [JSON evidence](evidence/browser-vertical-slice.json) và ảnh nằm trong `evidence/`.

## Rà soát kiến trúc và coverage

- Employee assignment negative coverage: cross-company, offboarded, stale version, duplicate idempotency và immutable historical version. Worker coverage: CG01 deny, grant exhausted, singleton lock contender/reacquire, shutdown trước HTTP, stop trong fake in-flight, process restart/recovery/no replay.
- Rà soát độc lập trước remake tìm link Inspector/Replay không cập nhật Run đang chọn và advisory-lock connection không được pin. Cả hai đã được sửa; worker lock contention/reacquire có PostgreSQL test. Chưa có vòng independent reviewer retest riêng sau sửa.
- Work Order queue chưa được nối vào Runtime Run. [Khuyến nghị Phase 09](phase09-bridge-plan.md) dùng adapter/receipt tới cùng Runtime service, không tạo inference engine thứ hai.

## Blocker và trạng thái

**P1 — in-flight `unknown` giữ global dispatch guard và chưa có Owner reconciliation route.** Đây là lựa chọn an toàn chống replay khi không biết gateway đã xử lý request hay chưa, nhưng có thể chặn mọi Runtime dispatch tiếp theo trong scope. Cần quyết định/thiết kế reconciliation dựa trên bằng chứng gateway trước khi real-model demonstration.

Harness fake gate hiển thị `demo-test`, `verified=false`, chỉ để chạy UI/API trong stack riêng; không cấp CG01 proof. Không tạo grant thật, không gọi model thật, không bật demo override, không migration DB live. Roadmap Markdown/HTML chỉ ghi evidence và giữ nguyên trạng thái Phase 06–08; không phase nào được đánh dấu Hoàn tất.

## Tài liệu bàn giao

- [Vertical slice](vertical-slice.md)
- [Kế hoạch bridge Phase 09](phase09-bridge-plan.md)
- [Hướng dẫn kiểm tra deployment hiện có](live-test-readiness.md)
- [Browser/DB evidence](evidence/browser-vertical-slice.json)
- [P07 r009 classification correction](evidence/phase-07-r009-classification-correction.md)
