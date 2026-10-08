# Kiểm định Phase 04 — 20261008T154151+0700-demo-factory

## Thông tin batch

- Phase: 04
- Test batch: 20261008T154151+0700-demo-factory
- Bắt đầu / kết thúc: 2026-10-08T15:41:51+07:00 / 2026-10-08T15:51:20+07:00 (Asia/Ho_Chi_Minh)
- Người/AI kiểm định: Codex
- Yêu cầu/phạm vi được giao: Chỉ triển khai Phase 04, kiểm dependency, cập nhật evidence và HTML, bàn giao chờ Chủ tịch nghiệm thu; không sang Phase 05 và không inference.
- Source: Baseline `2fd2a8f`; worktree dirty, không có commit mới cho batch này. File list/hashes trong [source manifest](evidence/source-manifest.json); diff chứa sẵn thay đổi các phase trước, được giữ nguyên.
- Môi trường/config/tool versions: macOS local; PostgreSQL Compose local; Alembic 20261008_0003; Python 3.14; FastAPI/SQLAlchemy theo lock; Node 24.21.0, oxlint, TypeScript, Vite theo lock; API loopback 127.0.0.1:15501; web 127.0.0.1:15500. Không lưu config secrets.
- Inference: Không gọi; không được cấp grant, model call, codex-server hoặc session.
- Dependency/quyết định nghiệm thu: Phase 03 được Chủ tịch duyệt trực tiếp “ok duyệt”; migration 0002 và app role/RLS đã có. IG03 integration được chạy lại bằng Phase 03 regression suite trong batch này; Phase 04 checklist không có gate riêng. Phase 05 chưa được giao.
- Supersedes: Không có.
- Kết luận kỹ thuật: chưa đủ bằng chứng
- Quyết định Chủ tịch: Chưa có quyết định nghiệm thu Phase 04.

## Mapping và phạm vi kiểm định

| Tiêu chí hiện tại / nguồn | Test IDs | Bắt buộc / tùy điều kiện | Ghi chú |
| --- | --- | --- | --- |
| C01–C08 theo `docs/tests/RULES.md` | C01–C08 | Bắt buộc | Scope Phase 04 và regression Phase 03 bị tác động |
| AC1 — fixture có seed/version, seed/reset không gọi model | P04-01, P04-07 | Bắt buộc | Seed tường minh, khóa request 0 |
| AC2 — reset không xóa artifact/ledger/thread ngoài demo | P04-02, P04-03, P04-04 | Bắt buộc | Canary metadata kiểm tra được; ledger/thread/file store chưa tồn tại |
| AC3 — dashboard/Inspector/finance không trộn demo vào real | P04-05, P04-06 | Bắt buộc | UI DOM + fixed scope; thiếu ảnh lưu thành file |
| IG03 — integration gate sau Phase 03, trước Phase 04 | C02, C07 | Bắt buộc dependency | Suite Phase 03 rerun trong batch này; evidence tại commands và tests |

## Tổng hợp

| Tag | Số test |
| --- | --- |
| clean | 12 |
| need-change | 3 |
| suggestion | 0 |

| Result | Số test |
| --- | --- |
| pass | 12 |
| fail | 0 |
| blocked | 3 |
| not-run | 0 |
| not-applicable | 0 |

## Kết quả từng test

### C01 — Phạm vi và diff

- Nguồn/tiêu chí: [Yêu cầu Phase 04](../../../../master-plan.md#phase-04--nhà-máy-công-ty-demo)
- Bắt buộc: có
- Điều kiện/môi trường: Worktree có thay đổi từ nhiều phase trước; đánh giá file scope Phase 04 riêng và không ghi đè thay đổi cũ.
- Bước/lệnh: Đối chiếu yêu cầu, master-plan, diff và [source manifest](evidence/source-manifest.json).
- Kỳ vọng: Chỉ Phase 04 + tài liệu dependency liên quan; không bắt đầu Phase 05.
- Thực tế: Thêm demo factory/reset/API/UI/test/evidence; cập nhật status Phase 03 stale và Phase 04. Sửa một relative link hỏng trong Phase 01 checklist để chạy global validator, không đổi tiêu chí/implementation Phase 01. Không sửa codex-server, shared proxy, port hoặc quyền gateway.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [source manifest](evidence/source-manifest.json), [phase evidence](../../../../evidence/phase-04.md)
- Xử lý/đề xuất: Không có.

### C02 — Dependency và nguồn quyết định

- Nguồn/tiêu chí: [Master plan Phase 04](../../../../master-plan.md#phase-04--nhà-máy-công-ty-demo), [Phase 03 evidence](../../../../evidence/phase-03.md), Product Spec §13 IG03.
- Bắt buộc: có
- Điều kiện/môi trường: PostgreSQL local healthy; migration 0002 hiện hữu; người dùng đã chấp thuận Phase 03.
- Bước/lệnh: Xác nhận history “ok duyệt”, `alembic current`; chạy regression persistence Phase 03; đọc contract IG03.
- Kỳ vọng: Dependency accepted, durable schema/RLS sẵn có; integration transaction/dedup/rollback/cross-scope được chứng minh.
- Thực tế: Migration 0002 có trước migration 0003; test suite Phase 03 chạy lại và pass; IG03 được ghi là pass trong batch này. Evidence Phase 03 được đồng bộ trạng thái.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [commands](evidence/commands.md), [Phase 03 evidence](../../../../evidence/phase-03.md), [Product Spec](../../../../product-spec.md#13-integration-verification-gates)
- Xử lý/đề xuất: IG08/12/16/20 còn pending theo roadmap; không thuộc phase này.

### C03 — Đủ criteria và demo

- Nguồn/tiêu chí: Mapping AC1–AC3 trong checklist [Phase 04](../../../phases/phase-04.md).
- Bắt buộc: có
- Điều kiện/môi trường: Seed v1 cố định và browser local.
- Bước/lệnh: Test manifest/reset/API; đối chiếu UI assertions.
- Kỳ vọng: Có fixture đúng state/version, dashboard có thể mở, nhãn demo và unknown rõ.
- Thực tế: Factory, API và UI hoạt động; 2 AC được kiểm đầy đủ trên phần đã tồn tại. P04-03/P04-05 còn blockers được ghi riêng, không suy thành đạt.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [seed manifest](evidence/seed-manifest.json), [UI assertions](evidence/ui-assertions.md)
- Xử lý/đề xuất: Xem kết quả từng P04 case.

### C04 — Không thực thi âm thầm

- Nguồn/tiêu chí: RULES C04; Product Spec §10/§12; AC1.
- Bắt buộc: có
- Điều kiện/môi trường: Seed, reset, GET dashboard, page open; không có grant.
- Bước/lệnh: Đọc import/call path tại demo factory/router/seed; chạy endpoint và tests; kiểm tra output có `inference_requests=0`.
- Kỳ vọng: Không gọi model/tool/session khi seed/reset/mở trang.
- Thực tế: Mã phase 04 không import gateway/provider/client; thao tác chỉ truy vấn/ghi PostgreSQL. Không có request inference hoặc codex-server.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [source manifest](evidence/source-manifest.json), [commands](evidence/commands.md)
- Xử lý/đề xuất: Không có.

### C05 — Scope và dữ liệu nhạy cảm

- Nguồn/tiêu chí: RULES C05; Product Spec §7/§12; AC2.
- Bắt buộc: có
- Điều kiện/môi trường: App role với forced RLS; canary artifact metadata benchmark và synthetic-real.
- Bước/lệnh: Chạy test reset lặp và kiểm tra canary hashes/storage key; đọc whitelist delete trong migration.
- Kỳ vọng: Demo reset không ảnh hưởng record ngoài fixed demo; không xóa gateway session hay dữ liệu khác.
- Thực tế: Canary benchmark và synthetic-real không đổi sau reset; code chỉ DELETE theo fixed demo environment + company trong danh sách bảng. Thread/ledger/file store chưa tồn tại, được ghi blocked tại P04-03.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [Phase 04 test](../../../../../apps/api/tests/test_phase04_demo_factory.py), [migration](../../../../../apps/api/migrations/versions/20261008_0003_demo_reset.py), [commands](evidence/commands.md)
- Xử lý/đề xuất: Blocker chưa có store được theo dõi riêng; không dùng scope canary để giả lập domain chưa có.

### C06 — Tài liệu và bản nhìn

- Nguồn/tiêu chí: RULES C06; AGENTS project instructions.
- Bắt buộc: có
- Điều kiện/môi trường: Markdown chuẩn, renderer roadmap và validator tests.
- Bước/lệnh: `rtk proxy python3 scripts/render_plan.py`; `rtk proxy python3 scripts/render_phase00.py`; `rtk proxy python3 docs/tests/scripts/validate.py --batch docs/tests/results/phase-04/20261008T154151+0700-demo-factory`.
- Kỳ vọng: Markdown/HTML khớp, lang=vi/favicon/links hợp lệ, report tags đầy đủ; không nâng trạng thái.
- Thực tế: Roadmap, Product Spec và checklist HTML được render. Validator pass cấu trúc 24 checklist + report Phase 04, và targeted check pass 15 cases. Rerun toàn bộ bundle hiện dừng ở một Phase 01 report mới trong worktree đang tham chiếu `evidence/finding-c02.md` chưa tồn tại; không phải file của batch này nên được giữ nguyên. Phase 04 vẫn Chờ nghiệm thu; thiếu screenshot được báo tại P04-05.
- Tag: need-change
- Kết quả: blocked
- Mức độ: minor
- Evidence: [render/validation output](evidence/commands.md), [phase HTML](../../../../master-plan.html), [Product Spec HTML](../../../../product-spec.html)
- Xử lý/đề xuất: Hoàn tất/đính kèm evidence của report Phase 01 trong phase tương ứng; không sửa report phase khác trong lượt Phase 04.

### C07 — Regression liên quan

- Nguồn/tiêu chí: RULES C07; IG03; regression dependency Phase 03 và code frontend thay đổi.
- Bắt buộc: có
- Điều kiện/môi trường: PostgreSQL local; Python/Node versions đã ghi; không inference.
- Bước/lệnh: `uv run --project apps/api pytest apps/api/tests -q`; `npm run lint`; `npm run build` trong `apps/web`.
- Kỳ vọng: Persistence/RLS/event regression pass; frontend lint/type/build pass.
- Thực tế: Toàn bộ 10 API tests pass (3 health, 5 Phase 03, 2 Phase 04); oxlint và TypeScript/Vite build pass. IG03 luồng covered: DB persistence/fresh connection, state+event/outbox, dedup, rollback và cross-scope deny. Không có test real inference gateway.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [commands](evidence/commands.md), [test source](../../../../../apps/api/tests/test_phase03_persistence.py)
- Xử lý/đề xuất: Starlette báo deprecation cho TestClient/httpx; chưa ảnh hưởng kết quả.

### C08 — Có thể tái kiểm định

- Nguồn/tiêu chí: RULES C08.
- Bắt buộc: có
- Điều kiện/môi trường: Batch mới có source hashes, commands, manifest, UI checks và report.
- Bước/lệnh: Kiểm cấu trúc `docs/tests/scripts/validate.py --batch ...`; kiểm tra link evidence và exact IDs.
- Kỳ vọng: Source/config/version, expected/actual, tag/result, evidence và cleanup scoped đủ.
- Thực tế: Report có C01–C08 + P04-01…07, file evidence liên kết; canaries được cleanup; 2 blocked cases không bị ghi pass.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [source manifest](evidence/source-manifest.json), [commands](evidence/commands.md)
- Xử lý/đề xuất: Validator không đánh giá nội dung evidence thay con người.

### P04-01 — Seed deterministic

- Nguồn/tiêu chí: [Checklist Phase 04](../../../phases/phase-04.md#ca-kiểm-định-riêng-của-phase); Product Spec §12.
- Bắt buộc: có
- Điều kiện/môi trường: Fixed demo scope đã provision; cùng seed/version.
- Bước/lệnh: Chạy `scripts/seed_demo.py --seed`, reset qua service/API nhiều lần, so sánh canonical dashboard manifests.
- Kỳ vọng: Cùng IDs/data/seed version và manifest hash; no model.
- Thực tế: Hai reset HTTP và 3 reset trong integration test cho hash ổn định `03e1126c…`; 2 phòng ban, 3 employees, 5 tasks, 20 events; inference 0.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [seed manifest](evidence/seed-manifest.json), [commands](evidence/commands.md)
- Xử lý/đề xuất: Hash bỏ volatile DB sequence/recorded time, bao gồm IDs/content/events fixture ổn định.

### P04-02 — Reset lặp an toàn

- Nguồn/tiêu chí: [Checklist P04-02](../../../phases/phase-04.md); AC2.
- Bắt buộc: có
- Điều kiện/môi trường: Scope demo cố định, app role, giao dịch atomic.
- Bước/lệnh: Reset 2 lần trong test và qua HTTP, đọc lại dashboard manifest/count/link refs.
- Kỳ vọng: Trở về cùng baseline, không duplicates/corrupt links.
- Thực tế: Hai POST HTTP trả 200, cùng hash; test xác nhận approvals, artifact metadata, run links, retry attempts và counts ổn định.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [commands](evidence/commands.md), [test source](../../../../../apps/api/tests/test_phase04_demo_factory.py)
- Xử lý/đề xuất: Reset chạy trong một transaction; event sequence counter giữ monotonic semantics.

### P04-03 — Isolation đầy đủ

- Nguồn/tiêu chí: [Checklist P04-03](../../../phases/phase-04.md); AC2; Product Spec §12.
- Bắt buộc: có
- Điều kiện/môi trường: Benchmark và synthetic-real canary artifact metadata đã được tạo ngoài demo; không có ledger/thread namespace hoặc artifact file store trong schema/runtime Phase 03.
- Bước/lệnh: Reset demo hai lần; so sánh canary hash/storage keys; audit migration delete whitelist và danh sách DB tables.
- Kỳ vọng: Benchmark/real artifact, ledger, thread metadata và storage ngoài demo không đổi; shared gateway session không bị dọn.
- Thực tế: Artifact metadata benchmark/real giữ nguyên; code không nhận path/scope arbitrary và không gọi gateway. Chưa thể tạo ledger/thread/file canaries ở app vì các store chưa tồn tại; không thể chứng minh đủ toàn bộ criteria.
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Evidence: [canary test](../../../../../apps/api/tests/test_phase04_demo_factory.py), [Phase 04 limitations](../../../../evidence/phase-04.md), [schema/test inventory](evidence/commands.md)
- Xử lý/đề xuất: Tái kiểm định isolation khi ledger, thread namespaces hoặc artifact file store được giao và tồn tại; không xóa native/shared gateway data.

### P04-04 — Deny reset sai scope

- Nguồn/tiêu chí: [Checklist P04-04](../../../phases/phase-04.md); AC2; Product Spec §10/§12.
- Bắt buộc: có
- Điều kiện/môi trường: HTTP API loopback và app DB role.
- Bước/lệnh: TestClient POST với confirmed=false và confirmed=true kèm giả `environment_id`/`company_id`; đọc DB guard function.
- Kỳ vọng: Từ chối trước delete; không hỗ trợ target real/benchmark.
- Thực tế: Body false trả 400; body target tự chọn trả 422 vì extra fields bị cấm. Backend function không có tham số, so `session_user` với app role và hardcode fixed demo IDs.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [negative cases](evidence/commands.md), [route](../../../../../apps/api/src/agent_corporation_api/modules/demo/router.py), [migration guard](../../../../../apps/api/migrations/versions/20261008_0003_demo_reset.py)
- Xử lý/đề xuất: Không cung cấp API provision demo cho client.

### P04-05 — Nhãn demo và report filters

- Nguồn/tiêu chí: [Checklist P04-05](../../../phases/phase-04.md); AC3.
- Bắt buộc: có
- Điều kiện/môi trường: Browser local, dashboard/approval/finance views; manifest fixed demo.
- Bước/lệnh: Mở các màn hình qua tab local; kiểm DOM assertion, nhãn và nguồn API scoped. Checklist yêu cầu ảnh được lưu.
- Kỳ vọng: Dashboard/Inspector/finance có label/filter scope, không nhập demo vào KPI real; có ảnh evidence tái kiểm tra.
- Thực tế: DOM xác nhận banner demo, approvals pending và finance unknown; backend trả đúng demo scope. Ảnh từng được hiển thị trong browser session nhưng công cụ screenshot không lưu được artifact vào workspace nên yêu cầu ảnh còn thiếu. Không có real KPI store trong Phase 04.
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Evidence: [DOM assertions và giới hạn ảnh](evidence/ui-assertions.md), [API response/commands](evidence/commands.md)
- Xử lý/đề xuất: Lưu ảnh screenshot từ browser trong batch kế tiếp; xác minh filter/source refs khi real report domain được triển khai.

### P04-06 — States và unknown fixture

- Nguồn/tiêu chí: [Checklist P04-06](../../../phases/phase-04.md); Product Spec §8/§9/§11.
- Bắt buộc: có
- Điều kiện/môi trường: Demo dashboard v1; usage unknown không có ledger thật.
- Bước/lệnh: Assert fixture statuses/runs/approval/artifact/usage trong API output và UI Finance.
- Kỳ vọng: Draft, running, awaiting approval, failed, retry; không bịa usage/cost bằng 0.
- Thực tế: Năm task đại diện đủ trạng thái; approval=1, failure metadata có, retry attempts 1–2; mọi usage/cost `unknown` và micros null.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [seed manifest](evidence/seed-manifest.json), [UI assertions](evidence/ui-assertions.md)
- Xử lý/đề xuất: Run state là fixture, được gắn nhãn; không biểu thị agent đang chạy thật.

### P04-07 — Không inference hoặc user company

- Nguồn/tiêu chí: [Checklist P04-07](../../../phases/phase-04.md); AC1; Product Spec §10/§12.
- Bắt buộc: có
- Điều kiện/môi trường: Seed/reset/dashboard app local, không grant.
- Bước/lệnh: Static call-path audit; seed/reset tests; query kiểm fixed demo kind/lock; teardown synthetic-real canary.
- Kỳ vọng: 0 model calls; không tạo tập đoàn thật của người dùng.
- Thực tế: Mã seed/router chỉ dùng DB; không có adapter/provider call path. Fixture reports `inference_requests=0`; test sau teardown không còn real-kind environments. Không có inference grant.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [source manifest](evidence/source-manifest.json), [seed manifest](evidence/seed-manifest.json), [test source](../../../../../apps/api/tests/test_phase04_demo_factory.py)
- Xử lý/đề xuất: Không mở model dispatch trong Phase 04.

## Integration / release gates

Phase 04 checklist không định nghĩa gate riêng; **gate phụ thuộc IG03** được kiểm tra qua C02/C07: pass trong batch này. IG08/12/16/20 không áp dụng cho Phase 04 và vẫn chưa thực hiện.

| Gate áp dụng | PASS / FAIL / BLOCKED | Test IDs | Batch/grant/config/evidence và gate trước |
| --- | --- | --- | --- |

Không có integration gate riêng cho Phase 04. Gate dependency IG03 được chạy lại và pass theo C02/C07. Các blocker P04-03/P04-05 là criteria của phase, không được nâng thành gate mới.

## Cleanup, giới hạn và bàn giao

- Cleanup: Benchmark và synthetic-real canary task/artifact/company/environment được xóa theo UUID trong test; database còn fixed demo fixture v1 phục vụ review. Không lưu DB dump hoặc secrets.
- Chưa kiểm chứng: P04-03 ledger/thread/file store; P04-05 screenshot file. Đây là thiếu evidence/domain runtime, không phải khẳng định có bug.
- Cần sửa: Không có fail đã xác nhận. Blocked cases cần evidence/store tương ứng trước khi Phase 04 có thể nhận kết luận kỹ thuật “đạt”.
- Đề xuất tùy chọn: Không có.
- Bàn giao: [Phase evidence](../../../../evidence/phase-04.md), [master-plan Markdown](../../../../master-plan.md), [master-plan HTML](../../../../master-plan.html), local UI `http://agent-corporation.localhost`. Chờ Chủ tịch nghiệm thu; không bắt đầu Phase 05.
