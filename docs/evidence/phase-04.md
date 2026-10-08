# Bằng chứng Phase 04 — Nhà máy công ty demo

Ngày: 08/10/2026 · Trạng thái bàn giao: **Chờ Chủ tịch nghiệm thu** · Inference grant: **0**.

## Dependency và phạm vi

- Phase 03 đã được Chủ tịch duyệt bằng “ok duyệt”; migration 0002 có mặt. PostgreSQL local healthy, API readiness trả `database: ok`, web và hostname local đã được đăng ký ở các phase trước. Phase 03 evidence có lịch sử nghiệm thu được cập nhật cùng lượt này.
- Đã đối chiếu IG03 trong Product Spec: suite integration Phase 03 chạy lại trong batch Phase 04 và xác minh scoped DB writes, fresh connection/persistence, event/outbox transaction, dedup, rollback và cross-scope RLS. Không có Phase 04-specific integration gate trong checklist.
- Không dùng codex-server, model, browser gateway hay inference. Không tạo user company. Chỉ thêm fixed demo company có `kind=demo`, `release_locked=true`; kiểm thử tạo synthetic canary `kind=real` tạm thời rồi dọn trong cùng test.
- Phase 05 không bắt đầu. Không sửa codex-server, shared proxy, hostname hay port.

## Phần được triển khai

- Alembic `20261008_0003` tạo `reset_agent_corporation_demo()` SECURITY DEFINER. Hàm chỉ cho đúng `session_user` app role thực thi, chỉ chạy khi UUID environment/company cố định vẫn là demo + release-locked; xóa theo whitelist bảng và điều kiện cả environment/company, không nhận scope/path từ client. PUBLIC bị revoke, quyền execute chỉ cấp cho app role.
- `scripts/seed_demo.py --seed` là thao tác tường minh. Provision environment/company dùng migration role; reset/seed dùng app role. App startup và GET dashboard không tự seed.
- Seed v1 deterministic: 2 phòng ban, 3 hồ sơ nhân viên version 1, 5 Work Order (draft/idle, executing + running, awaiting approval, failed + artifact metadata, rework + attempt 1 failed/attempt 2 queued) và 20 event fixture. Task budget khóa `max_model_requests=0`; usage/cost là `unknown`/`null`.
- API `GET /api/v1/demo/dashboard` đọc duy nhất UUID demo cố định. `POST /api/v1/demo/reset` chỉ nhận `{confirmed: true}`; body đóng từ chối `environment_id`/`company_id` và không có đường xóa storage arbitrary.
- UI có banner DEMO + seed version + reset confirmation xuyên màn hình; Work/Approvals/Inspector/Organization/Finance hiển thị fixture phù hợp. Finance ghi “Chưa biết”; onboarding real giữ khóa. Không thực hiện model/gateway requests.

## Manifest và isolation

- Seed name: `agent-corporation-phase-04-v1`; seed version: `1`.
- Environment UUID: `b93f752e-7b69-5e8b-8f74-1498a15a5609`; company UUID: `b4375333-b12b-5fca-b984-87864032d3a8`.
- Manifest API SHA-256 sau reset lặp: `03e1126cafadf2b400f51ebde367459565278634453e4b01fdcbf28a6242753a`.
- Canary benchmark và synthetic-real (artifact metadata + Work Order riêng) giữ nguyên SHA/storage key qua reset; test đã cleanup toàn bộ canary. Sau cleanup không còn environment `kind=real`.
- Reset whitelist hiện bao phủ bảng có trong Phase 03. Chưa có ledger schema, app thread namespace hoặc file artifact store. Vì vậy test chưa thể đặt canary tương ứng hoặc chứng minh isolation cho các store chưa tồn tại; code không gọi sang gateway và Product Spec quy định shared gateway session không thuộc reset scope.
- Chi tiết fixture/API hash: [seed manifest](../tests/results/phase-04/20261008T154151+0700-demo-factory/evidence/seed-manifest.json). Lệnh và log đã lọc: [commands](../tests/results/phase-04/20261008T154151+0700-demo-factory/evidence/commands.md). DOM assertions đã nhìn trực tiếp: [UI inspection](../tests/results/phase-04/20261008T154151+0700-demo-factory/evidence/ui-assertions.md).

## Kiểm tra

- Alembic current: `20261008_0003 (head)`.
- Toàn bộ API tests: 10 passed (3 health + 5 regression/integration Phase 03 + 2 Phase 04), có một cảnh báo deprecation của Starlette TestClient/httpx; không có failure.
- Web `oxlint`, TypeScript và Vite production build: pass với Node 24.21.0.
- API local `/api/v1/health/ready`: HTTP 200, database `ok`; `/api/v1/demo/dashboard`: HTTP 200, demo-only fixture.
- HTTP POST reset hai lần liên tiếp trả 200 và cùng manifest hash `03e1126c…`.
- UI DOM: approval queue có một pending fixture; Finance hiển thị unknown và không hiển thị số 0; mọi màn hình có banner DEMO; reset có JS confirm. Screenshot CUA đã được nhìn trong phiên nhưng không lưu thành artifact file; tiêu chí ảnh của P04-05 còn thiếu evidence tái kiểm tra trong report.
- Validator đã pass cấu trúc 24 checklist, 171 test definitions, source refs/contract hashes/local links, HTML và đủ 15 report cases Phase 04; targeted checker Phase 04 tiếp tục pass. Khi chốt, full-bundle rerun bị chặn bởi một Phase 01 report xuất hiện trong worktree có link tới `evidence/finding-c02.md` chưa tồn tại. File đó ngoài phase được giao nên giữ nguyên; validator không thay thế nội dung kiểm thử sản phẩm.

## Kết luận bàn giao

Phase 04 có triển khai và dữ liệu demo local để Chủ tịch review. Hai khoảng trống được giữ rõ trong [report kiểm định](../tests/results/phase-04/20261008T154151+0700-demo-factory/report.md): P04-03 chưa thể chứng minh ledger/thread/file-store isolation vì các store chưa tồn tại; P04-05 chưa có ảnh UI được lưu thành evidence. Kết luận kỹ thuật của batch là **chưa đủ bằng chứng**; trạng thái master-plan là **Chờ nghiệm thu**, không phải Hoàn tất. Không có inference grant/model permission; dừng trước Phase 05.
