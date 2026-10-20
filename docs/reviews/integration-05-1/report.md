# Agent Corporation — Integration Fix 05.1

**Ngày:** 20/10/2026 · **Phạm vi:** Owner reconciliation cho unknown Runtime outcome, independent regression, shared deployment preflight, demo plan. **Kết luận hiện tại:** đã có cơ chế ghi nhận unresolved an toàn; không nhả guard khi thiếu gateway evidence. Shared deployment chưa cập nhật. Phase 06–08 vẫn giữ trạng thái hiện hành.

## Thay đổi đã làm

- Thêm `GET /api/v1/runtime/runs/{run_id}/reconciliation` và `POST` cùng path trong `apps/api/src/agent_corporation_api/modules/execution/router.py`.
- Thêm read model ở `execution/service.py`: Run/employee version, call span/gateway ID, checkpoint metadata đã lọc, lease/heartbeat, grant/usage, guard và event refs. Không trả prompt history ở reconciliation view.
- POST chỉ chấp nhận `unresolved_retained`; bắt buộc Owner write dependency (session + Host/Origin + CSRF) và `Idempotency-Key`. Backend xác minh scope, span mới nhất là unknown và guard còn trỏ span này. Tạo receipt append-only + event cùng transaction; không thay outcome/checkpoint/usage, không reset grant và không nhả guard. Lý do được redaction trước khi lưu.
- Thêm migration `20261020_0010` cho receipt scoped + RLS, FK/unique key; app role chỉ SELECT/INSERT.
- Thêm entry trong Runtime UI cho Run interrupted: xem evidence, classification, grant/usage/cost/lease/guard và ghi quyết định Owner giữ guard. Không có force unlock hoặc nút tạo Run mới trong luồng này.
- Thêm regression test cho API boundary/idempotency schema, PG reconciliation concurrency/double submit, Owner audit, scope dữ liệu, guard retention và pre-dispatch cancellation classification.

## Gateway và deadlock decision

Gateway source có `X-Codex-Call-Id`, cancellation khi client disconnect và global health counters. Runtime gọi stateless `/v1/chat/completions`, không có API receipt đã nối chứng minh final state/cancel/usage cho từng span. `active_requests=0` là snapshot, không chứng minh completion/cancellation hay zero usage/cost. Không đủ evidence để nhả unknown guard. Không thêm force unlock hoặc risk-ack. Nếu Owner cần live demo khi unknown còn giữ guard, lựa chọn là chờ evidence hoặc dùng environment demo cô lập riêng với data/artifact/Owner/config/worker/concurrency/grant tách biệt; run cũ không replay.

## Kiểm định

| Hạng mục | Bằng chứng |
|---|---|
| API regression | `rtk uv run --project apps/api python scripts/test_playground_isolated.py` — **252 passed, 3 skipped, 1 warning in 27.67s**; disposable PostgreSQL/role được tạo và xóa, fake transport, không inference. Skips: Windows-only Owner ACL test trên macOS và hai Phase 09 queue tests opt-in; warning là Starlette/httpx deprecation. |
| Web | `rtk npm run --prefix apps/web build` — TypeScript + Vite build đạt. |
| UI smoke | Chrome trên stack cô lập: Demo overview và Owner-gated Office render đúng; sau synthetic Owner sign-in, các nhóm Run hiển thị trạng thái/count rỗng có nhãn. Chưa tạo synthetic interrupted Run nên panel reconciliation chưa được kiểm tra trực quan; xem [browser-smoke.md](evidence/browser-smoke.md). |
| Compose | `rtk proxy docker compose config --quiet` — exit 0. |
| Runtime integration | Report độc lập và source manifest tại [evidence](evidence/independent-test.md) sau khi hoàn thành. |
| Deployment | Read-only: shared API/PostgreSQL/web healthy, migration 0009, fixed Demo Corporation khớp một lần và có 3 employee, 0 Runtime Runs, 0 model calls, 0 valid unexhausted grants, guard empty, không có worker active. Compose source định nghĩa đúng một worker. |
| CG01/model | Shared scope `strict`, blocked `missing_or_invalid_proof`; gateway health/models GET 200; `gpt-6-luna` catalogued, medium có trong snapshot capability (checked 02/10), entitlement chưa được xác minh. |

Full command/observation list: [verification-commands.md](evidence/verification-commands.md). Deployment preflight: [deployment-preflight.md](deployment-preflight.md).

## Còn thiếu / quyết định Owner

- Duyệt hoặc từ chối build/restart riêng project Agent Corporation để áp dụng migration/API/UI và bật đúng một worker. Không chạy trong Fix 05.1.
- Strict CG01 hiện không pass. Nếu muốn demo bằng ngoại lệ, cần Owner phê duyệt riêng đúng scope/batch; không tự đổi config.
- Sau duyệt deploy/gate, Owner mới quyết định environment và cấp grant đúng lần test. Chưa tạo grant và chưa gọi model.
- Reconciliation của completion/cancellation in-flight cần gateway evidence bền vững/đối chiếu call ID. Hiện unresolved vẫn giữ guard; unknown usage/cost không thành zero.

Không có commit/push, shared restart/migration, reset/seed, gateway edit, grant, inference, hoặc phase status transition trong batch này.
