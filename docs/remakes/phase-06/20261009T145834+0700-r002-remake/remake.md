# Remake Phase 06 — 20261009T145834+0700-r002-remake

## Thông tin vòng sửa

- Phase: 06
- Remake batch: 20261009T145834+0700-r002-remake
- Người/AI remake: Codex `/root`, runtime06/runtime_ui
- Vòng: r002
- Report nguồn: [AI test r002](../../../tests/results/phase-06/20261009T121142+0700-r002-test/report.md)
- Bắt đầu / kết thúc: 2026-10-09T14:58:34+07:00 / 2026-10-09T15:04:32.019155+07:00 (đối chiếu và ghi snapshot bàn giao)
- Phạm vi/quyền: Sửa findings trong Phase06–07 theo chỉ thị fix blocker; không tự nghiệm thu, không mở Phase08, không gọi inference hay sửa/restart gateway dùng chung.
- Source trước/sau: Manifest report nguồn và [manifest sau sửa](evidence/source-manifest.json); worktree dirty, giữ nguyên thay đổi trước đó.
- Inference: Không gọi; grant thật0. Tests dùng PG/transport fixture riêng có nhãn.
- Kết luận vòng sửa: Đã sửa lỗi code và đồng bộ hồ sơ; chờ AI test độc lập chốt retest r003. CG01 và run thật vẫn bị chặn.

## Mapping results → thay đổi

| Test ID / tag-result nguồn | Nguyên nhân | Thay đổi thực tế / file refs | Trạng thái xử lý | Test cần rerun |
| --- | --- | --- | --- | --- |
| C02 | Dependency chưa được Chủ tịch nghiệm thu; chỉ thị hiện tại cho phép sửa code nền, không cấp CG01/grant. | Giữ trạng thái chính thức và ghi nguồn, không tự nghiệm thu Phase05/06. | blocked | C02, regression liên quan |
| C03 | Demo cần model thật và grant riêng; không dùng fixture để thay gate. | Không chạy inference; UI/HTTP thử nghiệm riêng được QA kiểm, demo thật vẫn chờ CG01/grant. | blocked | C03, regression liên quan |
| C06 | UI/tài liệu chưa đồng bộ ở snapshot r002. | RuntimePanel heartbeat worker/SSE riêng, GET cập nhật run, cache có nhãn; README/spec/evidence/master-plan đồng bộ. Pipeline sắp theo số vòng, có 14 regression tests. | changed | C06, regression liên quan |
| C07 | GET/list runtime dùng transaction ghi counter gây FK lỗi cho scope không tồn tại. | service.transaction(write=False) cho đường đọc; không INSERT/lock counter/guard khi GET. Regression được rerun trên PostgreSQL disposable. | changed | C07, regression liên quan |
| P06-02 | Proof CG01 dạng JSON list/FIFO có thể exception/block thay vì deny. | gates.py mở nofollow/nonblocking, fstat regular/0600/owner/size, kiểm dict/expiry/fingerprint/endpoint và reason enum. Proof live isolation/privacy/cancellation vẫn chưa có. | changed | P06-02, regression liên quan |
| P06-03 | Chưa có run thật được grant riêng. | Giữ default deny; không gọi model/gateway chat. | blocked | P06-03, regression liên quan |
| P06-05 | Completed với usage=null giải phóng khả năng gọi thêm cùng grant. | Giữ unresolved trên cùng grant; global PG guard cho toàn app và unknown outcome vẫn giữ guard. Atomic reserve, rollback và cross-company race có test. | changed | P06-05, regression liên quan |
| P06-06 | Fake socket close/stop đạt; hủy gateway thật chưa được kiểm chứng. | Giữ trạng thái in-flight/unknown và chặn bước mới; không coi close UI là provider đã hủy. Live case chờ gate/grant riêng. | blocked | P06-06, regression liên quan |
| P06-07 | Thiếu usage bị coi đã settle; chưa ghi nhận usage tới muộn. | Migration0006: correction bất biến/dedup theo request span, đối chiếu gateway ID từ adapter; không đổi outcome gốc, used requests hoặc expiry/revocation. Không có API nhập usage tùy ý. TOKEN_USAGE_RECORDED giữ provenance và null khác0. | changed | P06-07, regression liên quan |
| P06-08 | Task vẫn queued khi run waiting/completed/stop; GET thiếu scope gây FK lỗi. | Lifecycle task/event/checkpoint atomic; completed run → task reviewing, không accepted; unknown → blocked, stop queued → cancelled. Snapshot giữ Owner profile version và effective grant/policy/history. | changed | P06-08, regression liên quan |

## Chi tiết từng finding

### C02 — Dependency và quyết định

- Expected/actual nguồn: Xem case C02 trong [report r002](../../../tests/results/phase-06/20261009T121142+0700-r002-test/report.md).
- Nguyên nhân: Dependency chưa được Chủ tịch nghiệm thu; chỉ thị hiện tại cho phép sửa code nền, không cấp CG01/grant.
- Trạng thái xử lý: blocked
- Thay đổi: Giữ trạng thái chính thức và ghi nguồn, không tự nghiệm thu Phase05/06.
- Phản biện: Không có.
- Kiểm tra trong lúc sửa: Xem [commands](evidence/commands.md). Changed chỉ ghi nhận code/evidence đã làm, không tự đóng finding.
- Còn thiếu/blocker: Retest độc lập đầy đủ; case cần inference thật vẫn chờ CG01 và grant mới.
- Retest cần chạy: C02, happy path/negative/race và regression theo checklist, không gọi model trái grant.

### C03 — Criteria/demo

- Expected/actual nguồn: Xem case C03 trong [report r002](../../../tests/results/phase-06/20261009T121142+0700-r002-test/report.md).
- Nguyên nhân: Demo cần model thật và grant riêng; không dùng fixture để thay gate.
- Trạng thái xử lý: blocked
- Thay đổi: Không chạy inference; UI/HTTP thử nghiệm riêng được QA kiểm, demo thật vẫn chờ CG01/grant.
- Phản biện: Không có.
- Kiểm tra trong lúc sửa: Xem [commands](evidence/commands.md). Changed chỉ ghi nhận code/evidence đã làm, không tự đóng finding.
- Còn thiếu/blocker: Retest độc lập đầy đủ; case cần inference thật vẫn chờ CG01 và grant mới.
- Retest cần chạy: C03, happy path/negative/race và regression theo checklist, không gọi model trái grant.

### C06 — Markdown/HTML

- Expected/actual nguồn: Xem case C06 trong [report r002](../../../tests/results/phase-06/20261009T121142+0700-r002-test/report.md).
- Nguyên nhân: UI/tài liệu chưa đồng bộ ở snapshot r002.
- Trạng thái xử lý: changed
- Thay đổi: RuntimePanel heartbeat worker/SSE riêng, GET cập nhật run, cache có nhãn; README/spec/evidence/master-plan đồng bộ. Pipeline sắp theo số vòng, có 14 regression tests.
- Phản biện: Không có.
- Kiểm tra trong lúc sửa: Xem [commands](evidence/commands.md). Changed chỉ ghi nhận code/evidence đã làm, không tự đóng finding.
- Còn thiếu/blocker: Retest độc lập đầy đủ; case cần inference thật vẫn chờ CG01 và grant mới.
- Retest cần chạy: C06, happy path/negative/race và regression theo checklist, không gọi model trái grant.

### C07 — Regression

- Expected/actual nguồn: Xem case C07 trong [report r002](../../../tests/results/phase-06/20261009T121142+0700-r002-test/report.md).
- Nguyên nhân: GET/list runtime dùng transaction ghi counter gây FK lỗi cho scope không tồn tại.
- Trạng thái xử lý: changed
- Thay đổi: service.transaction(write=False) cho đường đọc; không INSERT/lock counter/guard khi GET. Regression được rerun trên PostgreSQL disposable.
- Phản biện: Không có.
- Kiểm tra trong lúc sửa: Xem [commands](evidence/commands.md). Changed chỉ ghi nhận code/evidence đã làm, không tự đóng finding.
- Còn thiếu/blocker: Retest độc lập đầy đủ; case cần inference thật vẫn chờ CG01 và grant mới.
- Retest cần chạy: C07, happy path/negative/race và regression theo checklist, không gọi model trái grant.

### P06-02 — Sandbox/CG01 boundary

- Expected/actual nguồn: Xem case P06-02 trong [report r002](../../../tests/results/phase-06/20261009T121142+0700-r002-test/report.md).
- Nguyên nhân: Proof CG01 dạng JSON list/FIFO có thể exception/block thay vì deny.
- Trạng thái xử lý: changed
- Thay đổi: gates.py mở nofollow/nonblocking, fstat regular/0600/owner/size, kiểm dict/expiry/fingerprint/endpoint và reason enum. Proof live isolation/privacy/cancellation vẫn chưa có.
- Phản biện: Không có.
- Kiểm tra trong lúc sửa: Xem [commands](evidence/commands.md). Changed chỉ ghi nhận code/evidence đã làm, không tự đóng finding.
- Còn thiếu/blocker: Retest độc lập đầy đủ; case cần inference thật vẫn chờ CG01 và grant mới.
- Retest cần chạy: P06-02, happy path/negative/race và regression theo checklist, không gọi model trái grant.

### P06-03 — Turn textonly thật

- Expected/actual nguồn: Xem case P06-03 trong [report r002](../../../tests/results/phase-06/20261009T121142+0700-r002-test/report.md).
- Nguyên nhân: Chưa có run thật được grant riêng.
- Trạng thái xử lý: blocked
- Thay đổi: Giữ default deny; không gọi model/gateway chat.
- Phản biện: Không có.
- Kiểm tra trong lúc sửa: Xem [commands](evidence/commands.md). Changed chỉ ghi nhận code/evidence đã làm, không tự đóng finding.
- Còn thiếu/blocker: Retest độc lập đầy đủ; case cần inference thật vẫn chờ CG01 và grant mới.
- Retest cần chạy: P06-03, happy path/negative/race và regression theo checklist, không gọi model trái grant.

### P06-05 — Resource reservation race

- Expected/actual nguồn: Xem case P06-05 trong [report r002](../../../tests/results/phase-06/20261009T121142+0700-r002-test/report.md).
- Nguyên nhân: Completed với usage=null giải phóng khả năng gọi thêm cùng grant.
- Trạng thái xử lý: changed
- Thay đổi: Giữ unresolved trên cùng grant; global PG guard cho toàn app và unknown outcome vẫn giữ guard. Atomic reserve, rollback và cross-company race có test.
- Phản biện: Không có.
- Kiểm tra trong lúc sửa: Xem [commands](evidence/commands.md). Changed chỉ ghi nhận code/evidence đã làm, không tự đóng finding.
- Còn thiếu/blocker: Retest độc lập đầy đủ; case cần inference thật vẫn chờ CG01 và grant mới.
- Retest cần chạy: P06-05, happy path/negative/race và regression theo checklist, không gọi model trái grant.

### P06-06 — Stop/abort baseline

- Expected/actual nguồn: Xem case P06-06 trong [report r002](../../../tests/results/phase-06/20261009T121142+0700-r002-test/report.md).
- Nguyên nhân: Fake socket close/stop đạt; hủy gateway thật chưa được kiểm chứng.
- Trạng thái xử lý: blocked
- Thay đổi: Giữ trạng thái in-flight/unknown và chặn bước mới; không coi close UI là provider đã hủy. Live case chờ gate/grant riêng.
- Phản biện: Không có.
- Kiểm tra trong lúc sửa: Xem [commands](evidence/commands.md). Changed chỉ ghi nhận code/evidence đã làm, không tự đóng finding.
- Còn thiếu/blocker: Retest độc lập đầy đủ; case cần inference thật vẫn chờ CG01 và grant mới.
- Retest cần chạy: P06-06, happy path/negative/race và regression theo checklist, không gọi model trái grant.

### P06-07 — Usage provenance

- Expected/actual nguồn: Xem case P06-07 trong [report r002](../../../tests/results/phase-06/20261009T121142+0700-r002-test/report.md).
- Nguyên nhân: Thiếu usage bị coi đã settle; chưa ghi nhận usage tới muộn.
- Trạng thái xử lý: changed
- Thay đổi: Migration0006: correction bất biến/dedup theo request span, đối chiếu gateway ID từ adapter; không đổi outcome gốc, used requests hoặc expiry/revocation. Không có API nhập usage tùy ý. TOKEN_USAGE_RECORDED giữ provenance và null khác0.
- Phản biện: Không có.
- Kiểm tra trong lúc sửa: Xem [commands](evidence/commands.md). Changed chỉ ghi nhận code/evidence đã làm, không tự đóng finding.
- Còn thiếu/blocker: Retest độc lập đầy đủ; case cần inference thật vẫn chờ CG01 và grant mới.
- Retest cần chạy: P06-07, happy path/negative/race và regression theo checklist, không gọi model trái grant.

### P06-08 — Snapshot/idle/task lifecycle

- Expected/actual nguồn: Xem case P06-08 trong [report r002](../../../tests/results/phase-06/20261009T121142+0700-r002-test/report.md).
- Nguyên nhân: Task vẫn queued khi run waiting/completed/stop; GET thiếu scope gây FK lỗi.
- Trạng thái xử lý: changed
- Thay đổi: Lifecycle task/event/checkpoint atomic; completed run → task reviewing, không accepted; unknown → blocked, stop queued → cancelled. Snapshot giữ Owner profile version và effective grant/policy/history.
- Phản biện: Không có.
- Kiểm tra trong lúc sửa: Xem [commands](evidence/commands.md). Changed chỉ ghi nhận code/evidence đã làm, không tự đóng finding.
- Còn thiếu/blocker: Retest độc lập đầy đủ; case cần inference thật vẫn chờ CG01 và grant mới.
- Retest cần chạy: P06-08, happy path/negative/race và regression theo checklist, không gọi model trái grant.

## Cleanup và bước tiếp theo

- Cleanup: Tests thuộc PostgreSQL/worker/browser preview riêng; không reset DB/project runtime hoặc gateway shared.
- Evidence: [manifest](evidence/source-manifest.json), [commands](evidence/commands.md).
- Retest tiếp theo: AI độc lập r003; liên kết vào sổ vòng khi report tồn tại.
- Blocker: CG01 proof thật, grant từng batch và nghiệm thu dependency; không tự đóng bằng fixture.
- Sổ vòng: [rounds](../../../tests/results/phase-06/README.md).
