# Bằng chứng triển khai Phase 10 — Quyền hạn và hộp phê duyệt

> Ngày: 14/10/2026 · Trạng thái: đang triển khai; chưa nghiệm thu. Phase 09 chưa đạt lease/recovery/retry và Phase 06–08 còn gate, vì vậy Phase 10 chưa được coi là tích hợp hoặc hoàn tất.

## Đã thêm

- Migration `20261014_0008`: mở rộng `approvals` với task revision, action payload, budget snapshot, expiry, decision provenance và hash; thêm request/decision idempotency receipts có RLS theo company/environment.
- Governance API `/api/v1/approvals`: Owner-scoped inbox, tạo yêu cầu review có expiry 1 phút–7 ngày, hash canonical gắn company/task revision/run/action/payload/policy/budget/expiry, và quyết định một lần theo đúng hash.
- `permission.py`: evaluator fail-closed với ba mức `automatic_in_scope`, `bounded_delegation`, `chairman_approval`. Hành động thay permission/model/profile/budget, gửi ngoài, deploy, destructive và promotion chat luôn cần Owner approval. Delegation yêu cầu khớp scope/action/payload/policy, chưa hết hạn và có reservation.
- `consume_approval`: khóa và tiêu thụ approval atomically một lần trước khi executor tương lai dispatch; thay đổi task/policy/run hoặc hết hạn chuyển approval sang stale/expired. Helper chỉ ghi trạng thái, không dispatch.
- S06 Inbox hiện payload/hash, task/run, policy, budget snapshot và expiry; quyết định cần Owner session + CSRF. Legacy fixture thiếu snapshot bị khóa quyết định.
- Profile/model changes hiện đã đi qua Owner API và ghi event `OWNER_MODEL_PROFILE_UPDATED`; endpoint agent không có quyền sửa profile, policy hoặc grant.

## Ranh giới và điều còn thiếu

- Hiện chưa có worker lease/recovery, tool executor hoặc nguồn agent proposal; decision API vì vậy chỉ lưu approval audit, không thực hiện action. Executor Phase 11 phải gọi `evaluate_action` + `consume_approval` trong đường thực thi, kiểm tra policy/stop/epoch và xử lý unknown outcome trước side effect.
- Các test integration migration/API/RLS/replay/stale/expiry/consume trên PostgreSQL disposable và browser runtime chưa chạy trong batch này; không chạy migration lên DB runtime hiện tại.
- Không gọi inference, không tạo/cấp inference grant, không sửa gateway. CG01 và grant hiện tại giữ nguyên.

## Kiểm tra đã chạy

- `uv run --project apps/api pytest apps/api/tests -q` — 102 passed, 10 skipped; có một cảnh báo deprecation từ Starlette/httpx.
- Permission evaluator độc lập: exact binding, mismatched action/revision/scope/hash/policy, expired/consumed, default-deny và unknown action — đều đạt; chi tiết tại [Phase 10 r001](../tests/results/phase-10/20261014T162815+0700-r001-test/).
- `npm run --prefix apps/web lint` — pass.
- `npm run --prefix apps/web build` — pass.
- `uv run --project apps/api python -m compileall -q apps/api/src/agent_corporation_api` — pass.
- `uv run --project apps/api alembic -c apps/api/alembic.ini history` — migration chain kết thúc ở `20261014_0008`.
- PostgreSQL 18.6 disposable: toàn bộ migration lên `20261014_0008` thành công; catalog xác nhận RLS + FORCE RLS và quyền app role trên approval/receipt tables. Xem [evidence migration cô lập](../tests/results/phase-10/20261014T162815+0700-r001-test/evidence/postgres-disposable-check.md).
- `rtk proxy python3 scripts/render_plan.py` — đồng bộ roadmap HTML thành công với 24 phase; renderer đọc được cả report đầy đủ và report độc lập dạng rút gọn.
- `git diff --check` — pass.

AI tester độc lập r002 xác nhận P10-01 đã sửa ở lớp evaluator (71 focused tests + matrix), nhưng kết luận Phase 10 **chưa đủ bằng chứng**: lifecycle/replay/concurrency, populated-row RLS, executor/stop race và browser audit UI vẫn blocked. Xem [report r002](../tests/results/phase-10/20261014T163443+0700-r002-test/report.md). Kết quả chưa thay thế Owner nghiệm thu; không chạy inference, không cấp grant và không tác động database runtime.
