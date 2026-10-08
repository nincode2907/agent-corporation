# Kiểm định Phase 04 — 20261008T162050+0700-demo-factory

## Thông tin batch

- Phase: 04
- Test batch: 20261008T162050+0700-demo-factory
- Bắt đầu / kết thúc: 2026-10-08T16:20:50+07:00 / 2026-10-08T16:20:50+07:00 (Asia/Ho_Chi_Minh)
- Người/AI kiểm định: Codex
- Yêu cầu/phạm vi được giao: User yêu cầu “test phase 4”; kiểm định đúng Phase 04 và regression dependency Phase 03.
- Source: commit `edb550c`; worktree dirty, các thay đổi owner khác được giữ nguyên; [source manifest/hashes](evidence/source-manifest.json).
- Môi trường/config/tool versions: API `127.0.0.1:15501`; web `127.0.0.1:15500`; PostgreSQL `127.0.0.1:15510`; readiness ok; Alembic `20261008_0003`; [commands](evidence/commands.md). Không ghi secret.
- Inference: Không gọi; grant=0.
- Dependency/quyết định nghiệm thu: Phase 03 được ghi Hoàn tất và regression 5 tests pass. Master plan ghi Phase 04 Chờ nghiệm thu. AGENTS.md ghi Phase 04 đang triển khai — mismatch tại C02. Không cập nhật trạng thái chính thức.
- Supersedes: [batch trước](../20261008T154151+0700-demo-factory/report.md); batch mới đánh giá lại runtime/source hiện tại.
- Kết luận kỹ thuật: cần sửa
- Quyết định Chủ tịch: Chưa có.

## Mapping và phạm vi kiểm định

| Tiêu chí hiện tại / nguồn | Test IDs | Bắt buộc / tùy điều kiện | Ghi chú |
| --- | --- | --- | --- |
| AC1 — fixture seed/version và không inference | P04-01, P04-07 | Bắt buộc | Reset/test trên scope demo fixed. |
| AC2 — reset không xóa scope khác | P04-02, P04-03, P04-04 | Bắt buộc | Artifact/record canaries chạy; ledger/thread/file stores chưa tồn tại. |
| AC3 — UI/report không trộn demo vào real | P04-05, P04-06 | Bắt buộc | Runtime DOM checked; screenshot chưa lưu. |
| C01–C08 theo RULES.md | C01–C08 | Bắt buộc | Mỗi record bên dưới. |

## Tổng hợp

| Tag | Số test |
| --- | --- |
| clean | 12 |
| need-change | 4 |
| suggestion | 0 |

| Result | Số test |
| --- | --- |
| pass | 12 |
| fail | 1 |
| blocked | 3 |
| not-run | 0 |
| not-applicable | 0 |

## Kết quả từng test

### C01 — Phạm vi và diff

- Nguồn/tiêu chí: Chỉ thị user “test phase 4”; AGENTS.md § phase scope
- Bắt buộc: có
- Điều kiện/môi trường: API/PostgreSQL local; test dùng fixed demo scope khóa release và UUID canaries; UI kiểm read-only; inference grant=0.
- Bước/lệnh: Đối chiếu status/diff và roadmap; không sửa implementation/phase status.
- Kỳ vọng: Chỉ kiểm Phase 04 và dependency regression; preserve changes owner.
- Thực tế: Worktree dirty với thay đổi Phase 05 và artifacts Phase 02/03/05. Batch chỉ thêm report/evidence Phase 04; commit nền edb550c.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [evidence](evidence/source-manifest.json)
- Xử lý/đề xuất: Không xử lý.
### C02 — Dependency và nguồn quyết định

- Nguồn/tiêu chí: docs/master-plan.md Phase 03/04; AGENTS.md § Hướng dẫn áp dụng
- Bắt buộc: có
- Điều kiện/môi trường: API/PostgreSQL local; test dùng fixed demo scope khóa release và UUID canaries; UI kiểm read-only; inference grant=0.
- Bước/lệnh: Đối chiếu dependency và trạng thái roadmap/hướng dẫn.
- Kỳ vọng: Phase 03 accepted; Phase 04 trạng thái nhất quán giữa nguồn.
- Thực tế: Phase 03 Hoàn tất. AGENTS.md nói Phase 04 đang triển khai; master-plan.md nói Chờ nghiệm thu. Master plan là chuẩn trạng thái; mismatch được xác nhận.
- Tag: need-change
- Kết quả: fail
- Mức độ: minor
- Evidence: [evidence](evidence/source-manifest.json)
- Xử lý/đề xuất: Chủ tịch đồng bộ nguồn hướng dẫn và roadmap; không tự đổi trạng thái.
### C03 — Đủ criteria và demo

- Nguồn/tiêu chí: docs/tests/phases/phase-04.md AC1–AC3; docs/master-plan.md Phase 04
- Bắt buộc: có
- Điều kiện/môi trường: API/PostgreSQL local; test dùng fixed demo scope khóa release và UUID canaries; UI kiểm read-only; inference grant=0.
- Bước/lệnh: Map AC1→P04-01/07; AC2→P04-02/03/04; AC3→P04-05/06; mở dashboard.
- Kỳ vọng: Mọi AC có case; demo đúng loại fixture và phạm vi.
- Thực tế: Mapping đủ; dashboard fixture local mở được. P04-03/P04-05 còn thiếu proof được ghi riêng.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [evidence](evidence/commands.md)
- Xử lý/đề xuất: Không xử lý.
### C04 — Không thực thi âm thầm

- Nguồn/tiêu chí: RULES.md C04; demo factory/router; test output
- Bắt buộc: có
- Điều kiện/môi trường: API/PostgreSQL local; test dùng fixed demo scope khóa release và UUID canaries; UI kiểm read-only; inference grant=0.
- Bước/lệnh: Đọc call path và kết quả inference_requests; chỉ điều hướng UI.
- Kỳ vọng: Seed/reset/dashboard không gọi model/tool/gateway.
- Thực tế: Test response có inference_requests=0; factory chỉ ghi DB fixture; UI copy nói rõ không gọi model. Không probe/reset qua UI hoặc gọi gateway.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [evidence](evidence/fixture-isolation.md)
- Xử lý/đề xuất: Không xử lý.
### C05 — Scope và dữ liệu nhạy cảm

- Nguồn/tiêu chí: RULES.md C05; test_phase04_demo_factory.py teardown
- Bắt buộc: có
- Điều kiện/môi trường: API/PostgreSQL local; test dùng fixed demo scope khóa release và UUID canaries; UI kiểm read-only; inference grant=0.
- Bước/lệnh: Review canary/environment UUID và cleanup; không đọc .env.
- Kỳ vọng: Benchmark/synthetic-real canary tách demo, cleanup đúng ID; không dùng secrets thật.
- Thực tế: Test dùng UUID canary mới cho benchmark/real Work Order + artifact metadata; kiểm tra giữ nguyên hash/storage_key qua reset rồi xóa đúng artifacts/tasks/company/environments theo ID. No real owner data/secret.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [evidence](evidence/fixture-isolation.md)
- Xử lý/đề xuất: Giới hạn ledger/thread/file store ở P04-03.
### C06 — Tài liệu và bản nhìn

- Nguồn/tiêu chí: RULES.md C06; checklist and report template
- Bắt buộc: có
- Điều kiện/môi trường: API/PostgreSQL local; test dùng fixed demo scope khóa release và UUID canaries; UI kiểm read-only; inference grant=0.
- Bước/lệnh: Chạy validator per-batch, kiểm DOM lang/favicon và links.
- Kỳ vọng: Report/links valid; UI lang=vi/favicon; không tự nâng phase status.
- Thực tế: lang=vi, favicon SVG; validator batch pass cấu trúc/links. Master-plan status không đổi. Full repo validator không chạy.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [evidence](evidence/commands.md)
- Xử lý/đề xuất: Không xử lý.
### C07 — Regression liên quan

- Nguồn/tiêu chí: RULES.md C07; dependency Phase 03; web UI
- Bắt buộc: có
- Điều kiện/môi trường: API/PostgreSQL local; test dùng fixed demo scope khóa release và UUID canaries; UI kiểm read-only; inference grant=0.
- Bước/lệnh: Chạy Phase 03 persistence + Phase 04 demo factory tests, web lint/build, alembic current.
- Kỳ vọng: Persistence/scope/reset regression và UI build pass.
- Thực tế: 7 tests pass (5 Phase 03, 2 Phase 04); oxlint/build pass; Alembic current 20261008_0003 head.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [evidence](evidence/commands.md)
- Xử lý/đề xuất: Không chạy API full suite; Phase 05 code/tests ngoài scope.
### C08 — Có thể tái kiểm định

- Nguồn/tiêu chí: RULES.md C08
- Bắt buộc: có
- Điều kiện/môi trường: API/PostgreSQL local; test dùng fixed demo scope khóa release và UUID canaries; UI kiểm read-only; inference grant=0.
- Bước/lệnh: Lưu hashes, exact commands/output summary, UI assertions, cleanup boundaries; validate batch.
- Kỳ vọng: Mọi case tag/result/evidence đủ, không chứa secret.
- Thực tế: Manifest/hash và evidence notes đã lưu; validator Phase 04 batch pass 16 cases. Screenshot được xem trực tiếp nhưng chưa có ảnh lưu trong workspace.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [evidence](evidence/commands.md)
- Xử lý/đề xuất: Validator không đánh giá thay nội dung evidence.
### P04-01 — Seed deterministic

- Nguồn/tiêu chí: phase-04.md AC1/P04-01; product-spec §12
- Bắt buộc: có
- Điều kiện/môi trường: API/PostgreSQL local; test dùng fixed demo scope khóa release và UUID canaries; UI kiểm read-only; inference grant=0.
- Bước/lệnh: Chạy test deterministic/reset lặp và so manifest hashes/counts.
- Kỳ vọng: Seed version/IDs/data ổn định, inference=0.
- Thực tế: Test xác nhận 3 lần reset cho cùng manifest; seed_version=1; 2 departments/3 employees/5 tasks/20 events; inference_requests=0. Baseline và final GET cùng hash 03e1126c….
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [evidence](evidence/fixture-isolation.md)
- Xử lý/đề xuất: Không xử lý.
### P04-02 — Reset lặp an toàn

- Nguồn/tiêu chí: phase-04.md P04-02; product-spec §12
- Bắt buộc: có
- Điều kiện/môi trường: API/PostgreSQL local; test dùng fixed demo scope khóa release và UUID canaries; UI kiểm read-only; inference grant=0.
- Bước/lệnh: Chạy integration test reset fixed demo scope nhiều lần; GET dashboard sau test.
- Kỳ vọng: Dataset trở về baseline, không duplicate/corrupt links.
- Thực tế: Test chạy trên fixed release-locked demo UUID; manifest hash giữ nguyên trước/sau; trạng thái approval/retry/artifact assertions pass. Không reset qua browser UI.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [evidence](evidence/fixture-isolation.md)
- Xử lý/đề xuất: Không xử lý.
### P04-03 — Isolation đầy đủ

- Nguồn/tiêu chí: phase-04.md P04-03; product-spec §7/12
- Bắt buộc: có
- Điều kiện/môi trường: API/PostgreSQL local; test dùng fixed demo scope khóa release và UUID canaries; UI kiểm read-only; inference grant=0.
- Bước/lệnh: Chạy canary benchmark + synthetic-real và so hash/storage keys sau reset; review schema availability.
- Kỳ vọng: Reset demo không xóa data ở benchmark/real artifacts/ledger/thread scopes.
- Thực tế: Benchmark và synthetic-real Work Order/artifact canaries giữ nguyên và được cleanup. Ledger schema, app thread namespace, file store chưa tồn tại nên phần isolation đó không thể kiểm chứng.
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Evidence: [evidence](evidence/fixture-isolation.md)
- Xử lý/đề xuất: Thêm canary/test cho ledger/thread/file store khi các domain này được triển khai; không giả lập chúng bằng mock.
### P04-04 — Deny reset sai scope

- Nguồn/tiêu chí: phase-04.md P04-04; product-spec §10/12
- Bắt buộc: có
- Điều kiện/môi trường: API/PostgreSQL local; test dùng fixed demo scope khóa release và UUID canaries; UI kiểm read-only; inference grant=0.
- Bước/lệnh: API test gửi confirmed=false và confirmed=true kèm forged environment/company targets.
- Kỳ vọng: Request bị từ chối trước delete/action; reset không nhận arbitrary scope.
- Thực tế: Test pass: confirmed=false trả 400; thêm environment_id/company_id bị Pydantic extra-forbid trả 422. Test không gọi reset khi request sai.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [evidence](evidence/fixture-isolation.md)
- Xử lý/đề xuất: Không xử lý.
### P04-05 — Nhãn demo/report filters

- Nguồn/tiêu chí: phase-04.md AC3/P04-05; product-spec §3/12
- Bắt buộc: có
- Điều kiện/môi trường: API/PostgreSQL local; test dùng fixed demo scope khóa release và UUID canaries; UI kiểm read-only; inference grant=0.
- Bước/lệnh: Mở Dashboard, Work, Approvals, Inspector, Finance; kiểm body labels/unknown states.
- Kỳ vọng: Mọi dữ liệu demo có nhãn; KPI real không trộn fixture; Finance không hiện usage=0.
- Thực tế: Browser runtime: dashboard/work/approval/inspector đều ghi Demo/fixture; Finance ghi DEMO·UNKNOWN, “Chưa biết”, không usage thực/ledger. Ảnh chụp đã xem trong phiên nhưng chưa được lưu thành file evidence; query/ref mapping tách real chưa có store.
- Tag: need-change
- Kết quả: blocked
- Mức độ: minor
- Evidence: [evidence](evidence/ui-observations.md)
- Xử lý/đề xuất: Lưu screenshot/DOM evidence vào batch mới; kiểm filter mapping real khi domain real có mặt.
### P04-06 — States và unknown fixture

- Nguồn/tiêu chí: phase-04.md P04-06; product-spec §8/9/11
- Bắt buộc: có
- Điều kiện/môi trường: API/PostgreSQL local; test dùng fixed demo scope khóa release và UUID canaries; UI kiểm read-only; inference grant=0.
- Bước/lệnh: Chạy test assertions và xem Work/Approvals/Inspector/Finance.
- Kỳ vọng: Idle/running/waiting/failed/approval/retry đúng contract; usage unknown, không bịa trạng thái live.
- Thực tế: Test assert statuses draft/executing/awaiting_approval/failed/rework, pending approval=1, failed artifact, retry attempts 1&2, usage_status=unknown, usd_cost_micros=null; UI ghi fixture.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [evidence](evidence/fixture-isolation.md)
- Xử lý/đề xuất: Không xử lý.
### P04-07 — Không inference hoặc user company

- Nguồn/tiêu chí: phase-04.md AC1/P04-07; product-spec §2/10/12
- Bắt buộc: có
- Điều kiện/môi trường: API/PostgreSQL local; test dùng fixed demo scope khóa release và UUID canaries; UI kiểm read-only; inference grant=0.
- Bước/lệnh: Spy qua output inference count; kiểm synthetic-real canary cleanup và UI read-only.
- Kỳ vọng: 0 model requests; không tạo company thật của người dùng; canary synthetic xóa đúng scope.
- Thực tế: Test response inference_requests=0; temporary synthetic-real test row bị dọn và final DB không còn environment kind=real theo assertion; app dashboard demo-only. No gateway/model call.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [evidence](evidence/fixture-isolation.md)
- Xử lý/đề xuất: Không xử lý.
### P04-08 — Cleanup canary khi test thất bại

- Nguồn/tiêu chí: Rủi ro test harness: apps/api/tests/test_phase04_demo_factory.py
- Bắt buộc: có
- Điều kiện/môi trường: API/PostgreSQL local; test dùng fixed demo scope khóa release và UUID canaries; UI kiểm read-only; inference grant=0.
- Bước/lệnh: Review thứ tự assertion và DELETE; không ép test fail vì sẽ cố ý để lại canary nếu cleanup không finally-scoped.
- Kỳ vọng: Canary được cleanup cả khi assertion/exception trước cleanup.
- Thực tế: Code risk: DELETE canaries đặt sau các reset/data/hash assertions, không nằm trong finally/fixture finalizer. Happy path batch này pass và cleanup chạy; failure path chưa được fault-injected.
- Tag: need-change
- Kết quả: blocked
- Mức độ: minor
- Evidence: [evidence](evidence/cleanup-risk.md)
- Xử lý/đề xuất: Đưa canary IDs vào fixture finalizer/context manager; kiểm chứng cleanup khi test body raise.

## Integration / release gates

Phase 04 không có gate IG riêng; dependency/regression Phase 03 được ghi tại C02/C07.

## Cleanup, giới hạn và bàn giao

- Cleanup: Test đã reset duy nhất fixed `kind=demo`, `release_locked=true` UUID scope về baseline. Benchmark và synthetic-real canary dùng UUID ngẫu nhiên, đã bị xóa theo ID bởi happy-path test. Final dashboard manifest giữ hash `03e1126c…`. Không restart service/DB hoặc gọi inference.
- Chưa kiểm chứng: P04-03 ledger/thread/file-store isolation vì các store chưa có; P04-05 screenshot retained; P04-08 cleanup path nếu assertion fail. C02 là mismatch trạng thái.
- Cần xử lý: C02 đồng bộ AGENTS/master-plan. P04-08 nên đặt cleanup trong finalizer. Blockers P04-03/05 cần evidence tương ứng; chưa xác nhận lỗi runtime.
- Đề xuất tùy chọn: Không có.
- Bàn giao: [runtime UI observations](evidence/ui-observations.md), [fixture/isolation assertions](evidence/fixture-isolation.md), [test cleanup risk](evidence/cleanup-risk.md), [commands](evidence/commands.md), [source manifest](evidence/source-manifest.json). Không tự nghiệm thu hoặc đổi trạng thái Phase 04.
