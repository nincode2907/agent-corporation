# Kiểm định Phase 09 — 20261011T224700+0700-r001-test

## Thông tin batch

- Phase: 09
- Test batch: `20261011T224700+0700-r001-test`
- Vòng: r001
- Bắt đầu / kết thúc: 2026-10-11 22:47 +07:00 (Asia/Ho_Chi_Minh; kiểm tra trong một lượt)
- Người/AI kiểm định: `/root/phase09_qa`
- Độc lập với AI triển khai/remake: Có; source/remake agent là `/root`.
- Yêu cầu/phạm vi được giao: Kiểm định độc lập source Phase 09; không sửa source sản phẩm; chạy kiểm tra an toàn không chạm DB dùng chung; ghi report và sổ vòng; không đổi roadmap/trạng thái phase.
- Source: HEAD `f74320e2ff20516ec93fbfe3413cfb953695b51d` + dirty worktree. Manifest/hash: [source-manifest.md](source-manifest.md).
- Môi trường/config/tool versions: Windows PowerShell; Python/uv từ `apps/api/.venv`; PostgreSQL integration không được bật; chi tiết lệnh ở [commands.md](commands.md). Không đọc `.env`.
- Inference: Không gọi; grant = 0 theo roadmap.
- Dependency/quyết định nghiệm thu: Phase 09 phụ thuộc Phase 08; master-plan ghi Phase 08 bị chặn và Phase 09 đang triển khai. Chưa có quyết định nghiệm thu Chủ tịch; report này không đổi trạng thái roadmap.
- Supersedes: Không có.
- Remake nguồn: Không có ở vòng đầu.
- Kết luận kỹ thuật: chưa đủ bằng chứng
- Quyết định Chủ tịch: Chưa có.

## Mapping và phạm vi kiểm định

| Tiêu chí hiện tại / nguồn | Test IDs | Bắt buộc / tùy điều kiện | Ghi chú |
| --- | --- | --- | --- |
| C01–C08 theo `docs/tests/RULES.md` | C01–C08 | Bắt buộc | Scope, dependency, evidence/demo, dispatch, boundary, docs, regression, reproducibility. |
| Roadmap AC1: hai worker không nhận cùng lease; không vượt concurrency/nhân run | P09-02 | Bắt buộc | Lease integration test có nhưng opt-in; test không chạy khi chưa xác nhận disposable PostgreSQL. |
| Roadmap AC2: pause/checkpoint/resume không hứa resume giữa token | P09-04, P09-05 | Bắt buộc | Cần state/API/UI và recovery evidence. |
| Roadmap AC3: Owner acceptance riêng; rework giữ evidence | P09-06 | Bắt buộc | Cần persisted run/review/rework evidence. |
| Work Order contract và queue durability/priority/crash | P09-01, P09-03 | Bắt buộc | Schema validation có regression; DB state, migration và crash chưa được chứng minh. |
| Task board/filter/actions | P09-07 | Bắt buộc | Cần browser/UI và đối chiếu API state. |

## Tổng hợp

| Tag | Số test |
| --- | ---: |
| clean | 5 |
| need-change | 10 |
| suggestion | 0 |

| Result | Số test |
| --- | ---: |
| pass | 5 |
| fail | 0 |
| blocked | 9 |
| not-run | 1 |
| not-applicable | 0 |

## Kết quả từng test

### C01 — Phạm vi và diff

- Nguồn/tiêu chí: [Phase 09 checklist](../../../phases/phase-09.md); `git status`/diff được ghi trong [source-manifest](source-manifest.md).
- Bắt buộc: có
- Điều kiện/môi trường: Dirty worktree; Phase 09 queue lease source, migration và test là thay đổi mục tiêu; `docs/start-windows-macos.md` là untracked riêng, không thuộc source test.
- Bước/lệnh: `rtk proxy git status --short`; `rtk proxy git diff --stat`; `rtk proxy git diff -- apps/api/src/agent_corporation_api/modules/work/queue.py`.
- Kỳ vọng: Không lấn sang Phase 10, giữ thay đổi ngoài scope, ghi nhận dirty source.
- Thực tế: Source diff nằm trong queue lease Phase 09; có migration/test Phase 09 chưa track và một tài liệu hướng dẫn untracked ngoài scope được giữ nguyên. Không thấy thay đổi Phase 10 trong danh sách dirty.
- Kết quả phản biện: none
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [source-manifest.md](source-manifest.md).
- Xử lý/đề xuất: Tiếp tục kiểm định đúng Phase 09.

### C02 — Dependency và nguồn quyết định

- Nguồn/tiêu chí: [master-plan](../../../../master-plan.md), [Phase 09 checklist](../../../phases/phase-09.md), [spec](../../../../product-spec.md), [ADR](../../../../decisions/0001-v1-foundation.md).
- Bắt buộc: có
- Điều kiện/môi trường: Đọc trạng thái roadmap và criteria hiện tại.
- Bước/lệnh: Đọc các tài liệu trên; không truy cập database.
- Kỳ vọng: Báo rõ dependency Phase 08 và không tự nghiệm thu/chuyển phase.
- Thực tế: Roadmap ghi Phase 08 bị chặn, Phase 09 đang triển khai; phase 09 chưa được nghiệm thu. Đây là dependency/blocker cho bàn giao phase, không được biến thành PASS bằng unit tests.
- Kết quả phản biện: none
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [master-plan](../../../../master-plan.md), [phase checklist](../../../phases/phase-09.md).
- Xử lý/đề xuất: Giữ nguyên roadmap; Chủ tịch quyết định nghiệm thu riêng.

### C03 — Đủ criteria và demo

- Nguồn/tiêu chí: AC1–AC3 và demo bắt buộc trong [Phase 09 checklist](../../../phases/phase-09.md).
- Bắt buộc: có
- Điều kiện/môi trường: Không có demo hai task chạy qua pause, restart worker, resume và safe retry trong batch này.
- Bước/lệnh: Không chạy; integration/UI demo cần môi trường và evidence riêng.
- Kỳ vọng: Artifact mở được cho demo bắt buộc và mọi AC có bằng chứng đúng loại.
- Thực tế: Chưa có demo hoặc evidence runtime; các lệnh unit không bao phủ checklist đầy đủ.
- Kết quả phản biện: none
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Evidence: Checklist và [commands.md](commands.md).
- Xử lý/đề xuất: Bổ sung demo Phase 09 cùng artifact/evidence; không chạy bằng DB chưa xác minh disposable.

### C04 — Không thực thi âm thầm

- Nguồn/tiêu chí: RULES C04; scope Phase 09; spec về grant, dispatch và inference.
- Bắt buộc: có
- Điều kiện/môi trường: Source review + unit tests; không có inference grant.
- Bước/lệnh: Review `claim_next`, `heartbeat_claim`, `task_action` trong [queue.py](../../../../../apps/api/src/agent_corporation_api/modules/work/queue.py); chạy unit tests ở [commands.md](commands.md).
- Kỳ vọng: Claim chỉ cấp lease; không tự tạo run, dispatch model/tool hoặc gọi inference.
- Thực tế: `claim_next` chỉ cập nhật queue lease; docstring và body không tạo run/dispatch. Lease test dự kiến assert không có row `runs`, nhưng integration tests đã skip nên phần assertion này chưa có runtime evidence. Unit/API test chạy không gọi inference.
- Kết quả phản biện: none
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [queue.py](../../../../../apps/api/src/agent_corporation_api/modules/work/queue.py), [commands.md](commands.md).
- Xử lý/đề xuất: Rerun kiểm chứng DB assertion khi có disposable PostgreSQL.

### C05 — Scope và dữ liệu nhạy cảm

- Nguồn/tiêu chí: RULES C05; ADR D05/D06; RLS/boundary contracts trong spec.
- Bắt buộc: có
- Điều kiện/môi trường: Không dùng secret thật; không có DB được xác nhận disposable.
- Bước/lệnh: Review `set_company_scope`, các query giới hạn `environment_id/company_id`; không chạy cross-scope DB test.
- Kỳ vọng: Scope giữ xuyên queue/heartbeat và data boundary được chứng minh bằng negative tests.
- Thực tế: Query source nhận scope và filter cả environment/company; chưa có negative RLS/runtime evidence của migration mới. Không đọc `.env` hoặc session/token.
- Kết quả phản biện: none
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Evidence: [queue.py](../../../../../apps/api/src/agent_corporation_api/modules/work/queue.py), [commands.md](commands.md).
- Xử lý/đề xuất: Chạy boundary/RLS tests trên PostgreSQL disposable, bao gồm heartbeat sai scope và migration policy/grants.

### C06 — Tài liệu và bản nhìn

- Nguồn/tiêu chí: RULES C06; [Phase 09 checklist](../../../phases/phase-09.md); report structure.
- Bắt buộc: có
- Điều kiện/môi trường: Tài liệu test local.
- Bước/lệnh: `rtk proxy python3 -X utf8 docs/tests/scripts/validate.py --batch docs/tests/results/phase-09/20261011T224700+0700-r001-test`.
- Kỳ vọng: Report đủ structure/IDs/links, docs kiểm định hợp lệ; không sửa roadmap/status.
- Thực tế: Batch validator dừng ở link tương đối hỏng trong report Phase 01 cũ (`../../../../../../dev-hub/projects.yml`); Phase 09 report riêng được kiểm tra bằng link/structure helper. Trong lúc review, implementation agent cập nhật Markdown `master-plan.md` và `evidence/phase-09.md`, rồi báo đã render HTML roadmap; trạng thái Phase 09 vẫn Đang triển khai.
- Kết quả phản biện: none
- Tag: need-change
- Kết quả: blocked
- Mức độ: info
- Evidence: [commands.md](commands.md).
- Xử lý/đề xuất: Sửa hoặc điều kiện hóa link môi trường trong report Phase 01 cũ rồi chạy full validator; đồng bộ HTML từ thay đổi Markdown theo project instructions. Link report Phase 01 ngoài scope Phase 09.

### C07 — Regression liên quan

- Nguồn/tiêu chí: RULES C07; thay đổi Work Order schema/queue lease Phase 09.
- Bắt buộc: có
- Điều kiện/môi trường: Unit/API tests không cần database; lease integration được giữ opt-in.
- Bước/lệnh: `rtk proxy uv run --project apps/api pytest apps/api/tests/test_phase09_work_orders.py apps/api/tests/test_phase09_queue_leases.py -q`.
- Kỳ vọng: Work Order contract regression đạt; integration tests không kết nối DB khi chưa opt-in.
- Thực tế: 12 passed, 2 skipped; hai lease integration tests skip vì `PHASE_QUEUE_TEST_ISOLATED` chưa bật. Có một cảnh báo deprecation của Starlette TestClient.
- Kết quả phản biện: none
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [commands.md](commands.md).
- Xử lý/đề xuất: Không diễn giải hai test skip thành pass; lease persistence/race vẫn được mở ở P09-02/03.

### C08 — Có thể tái kiểm định

- Nguồn/tiêu chí: RULES C08; report template; source manifest.
- Bắt buộc: có
- Điều kiện/môi trường: Batch r001, dirty worktree được hash.
- Bước/lệnh: Validator batch và hash manifest; xem [commands.md](commands.md), [source-manifest.md](source-manifest.md).
- Kỳ vọng: Có IDs/tags, expected/actual, command/evidence, source hashes và giới hạn; có link từ sổ vòng.
- Thực tế: Report/source manifest/command evidence và sổ vòng được tạo, liên kết trong docs; validator batch pass.
- Kết quả phản biện: none
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [report.md](report.md), [commands.md](commands.md), [source-manifest.md](source-manifest.md).
- Xử lý/đề xuất: Khi remake/retest, tạo batch r002; không ghi đè lịch sử.

### P09-01 — WorkOrder validation

- Nguồn/tiêu chí: Phase 09 AC/criteria P09-01; spec §7.
- Bắt buộc: có
- Điều kiện/môi trường: Pydantic/router unit tests chạy không cần DB.
- Bước/lệnh: Test focused `test_phase09_work_orders.py`; kết quả 12 pass tổng hợp, trong đó schema validation có coverage.
- Kỳ vọng: Thiếu field/invalid scope, budget, deadline, stop/assignee bị từ chối trước queue; revision/DB snapshot không bị ghi.
- Thực tế: Schema/API validation regression pass; không có DB test chứng minh invalid request không ghi revision/queue ở source hiện tại trong batch này.
- Kết quả phản biện: none
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Evidence: [commands.md](commands.md), [test_phase09_work_orders.py](../../../../../apps/api/tests/test_phase09_work_orders.py).
- Xử lý/đề xuất: Chạy persistence test trên disposable PostgreSQL để xác minh DB state không đổi.

### P09-02 — Lease/concurrency race

- Nguồn/tiêu chí: Phase 09 AC1/P09-02; spec §7/8.
- Bắt buộc: có
- Điều kiện/môi trường: Test tồn tại dưới opt-in; không xác nhận được disposable PostgreSQL nên env opt-in không bật.
- Bước/lệnh: `rtk proxy uv run --project apps/api pytest apps/api/tests/test_phase09_queue_leases.py -q` (2 skipped; không mở DB).
- Kỳ vọng: Nhiều worker chỉ có một active lease theo cap; không tạo run/dispatch trùng; heartbeat token fencing hoạt động.
- Thực tế: Chỉ code/static review; không có parallel test runtime. Source khóa claim bằng transaction advisory lock theo environment/company, giới hạn concurrency 1, token-fence heartbeat. Chưa chứng minh race behavior thực tế.
- Kết quả phản biện: none
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Evidence: [queue lease tests](../../../../../apps/api/tests/test_phase09_queue_leases.py), [commands.md](commands.md).
- Xử lý/đề xuất: Cấp môi trường PostgreSQL disposable riêng, áp migration head rồi chạy test race và đối chiếu DB state.

### P09-03 — Durable queue/crash

- Nguồn/tiêu chí: Phase 09 P09-03; spec §8.
- Bắt buộc: có
- Điều kiện/môi trường: Không có disposable PostgreSQL/worker runtime được xác nhận.
- Bước/lệnh: Không chạy migration hoặc restart worker trên môi trường dùng chung.
- Kỳ vọng: Hai task được lưu bền, ordering theo priority; crash/lease expiry reconcile đúng, không retry side effect chưa xác định.
- Thực tế: Migration và query source được review; không có migration runtime, restart/crash evidence hay durable DB snapshots.
- Kết quả phản biện: none
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Evidence: [migration](../../../../../apps/api/migrations/versions/20261011_0008_queue_leases.py), [commands.md](commands.md).
- Xử lý/đề xuất: Chạy migration/crash/restart tests trên DB disposable; với side effect không rõ outcome phải giữ blocked/reconciling, không tự retry.

### P09-04 — Pause/resume checkpoint

- Nguồn/tiêu chí: Phase 09 AC2/P09-04; spec §8/10.
- Bắt buộc: có
- Điều kiện/môi trường: Source review/unit tests; không có browser hoặc persisted run/checkpoint fixture.
- Bước/lệnh: Không có UI/runtime test trong batch.
- Kỳ vọng: Pause chặn bước mới; resume recheck quyền/budget/approval tại boundary/checkpoint, không resume giữa token.
- Thực tế: Queue action clears lease fields on pause/resume, nhưng source chưa có checkpoint/resume target evidence trong lease path; UI behavior không được kiểm chứng. Các integration assertions liên quan đã skip.
- Kết quả phản biện: none
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Evidence: [queue.py](../../../../../apps/api/src/agent_corporation_api/modules/work/queue.py), [commands.md](commands.md).
- Xử lý/đề xuất: Cung cấp persisted checkpoint/resume evidence, permission/budget recheck và UI/API test; không quảng cáo tiếp tục giữa inference/token.

### P09-05 — Retry/idempotency

- Nguồn/tiêu chí: Phase 09 P09-05; spec §8.
- Bắt buộc: có
- Điều kiện/môi trường: Không có DB/runtime retry fixture.
- Bước/lệnh: Source review; không phát sinh retry side effect.
- Kỳ vọng: Safe retry có attempt mới; unknown side effect bị chặn; task terminal retry tạo task mới/lineage.
- Thực tế: Test lease token fencing mới không chứng minh retry receipts/outcome reconciliation hay attempt/task lineage.
- Kết quả phản biện: none
- Tag: need-change
- Kết quả: not-run
- Mức độ: major
- Evidence: [Phase 09 checklist](../../../phases/phase-09.md), [commands.md](commands.md).
- Xử lý/đề xuất: Thực hiện negative/idempotency tests với fixture disposable; không tự retry khi unknown.

### P09-06 — Review/rework/acceptance

- Nguồn/tiêu chí: Phase 09 AC3/P09-06; spec §8/10.
- Bắt buộc: có
- Điều kiện/môi trường: Không có persisted completed run/review fixture.
- Bước/lệnh: Không chạy DB flow.
- Kỳ vọng: Completed khác accepted; chỉ Owner acceptance; rework lưu evidence cũ và tạo attempt/revision đúng.
- Thực tế: Schema/unit regression không chứng minh persisted actor/evaluation/event history. Không có DB evidence trong batch.
- Kết quả phản biện: none
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Evidence: [Phase 09 checklist](../../../phases/phase-09.md), [commands.md](commands.md).
- Xử lý/đề xuất: Chạy persisted state/actor/evaluation tests trên disposable PostgreSQL.

### P09-07 — Task board filters/actions

- Nguồn/tiêu chí: Phase 09 P09-07; spec §3/8.
- Bắt buộc: có
- Điều kiện/môi trường: Không có browser session/test evidence trong batch này.
- Bước/lệnh: Không chạy UI flow.
- Kỳ vọng: Tạo/giao/lọc/blocked/cancel hiển thị assignee/history đúng; cancel chặn bước mới.
- Thực tế: Không có screenshot hay đối chiếu UI/API state. Unit tests không cover task board behavior.
- Kết quả phản biện: none
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Evidence: [Phase 09 checklist](../../../phases/phase-09.md), [commands.md](commands.md).
- Xử lý/đề xuất: Chạy browser/UI kiểm định không inference và lưu ảnh/state comparison.

## Integration / release gates

Phase 09 không có IG riêng theo checklist. Không áp dụng IG riêng; AC/criteria vẫn chưa đủ bằng chứng. Dependency Phase 08 đang bị chặn.

## Cleanup, giới hạn và bàn giao

- Cleanup: Không tạo fixture, không ghi DB, không thay đổi code sản phẩm.
- Chưa kiểm chứng: P09-01 DB no-write, P09-02 lease race, P09-03 migration/crash/restart, P09-04 checkpoint/UI pause-resume, P09-05 retry/outcome reconciliation, P09-06 review/acceptance persistence, P09-07 task board; chưa có disposable PostgreSQL hoặc browser evidence.
- Cần sửa: Không kết luận source bug trực tiếp trong kiểm định tĩnh; cần hoàn thiện evidence/tests của các case bắt buộc. Tất cả issue trên đang need-change vì chưa đủ bằng chứng, không phải khẳng định test fail.
- Đề xuất tùy chọn: Sau khi môi trường disposable được provision, thêm CI job chỉ bật `PHASE_QUEUE_TEST_ISOLATED=1` khi URL được kiểm chứng là disposable. Không bật biến này trên DB dùng chung.
- Bước tiếp theo: Remake/evidence follow-up trong Phase 09 và r002 retest; không mở/chuyển Phase 10.
- Bàn giao: Report, commands và source manifest của batch r001; Chủ tịch nghiệm thu riêng.
