# Remake Phase 07 — 20261009T145834+0700-r002-remake

## Thông tin vòng sửa

- Phase: 07
- Remake batch: 20261009T145834+0700-r002-remake
- Người/AI remake: Codex `/root`, runtime06/runtime_ui
- Vòng: r002
- Report nguồn: [AI test r002](../../../tests/results/phase-07/20261009T121142+0700-r002-test/report.md)
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
| P07-02 | Thiếu evidence HTTP disconnect/reconnect ở r002, chưa xác nhận bug source. | Giữ feed/cursor; AI độc lập thực hiện HTTP/SSE loopback thật, Last-Event-ID reconnect và logout thu hồi stream ở retest. | no-change | P07-02, regression liên quan |
| P07-04 | UI thiếu đối chiếu heartbeat worker và trạng thái stale/offline. | Worker heartbeat/lease riêng với kết nối SSE, GET poll10s chỉ active run, event-triggered refresh; cache có nhãn chưa đối chiếu và logout hủy timer/stream. | changed | P07-04, regression liên quan |
| P07-05 | Thiếu process-kill evidence và cần task lifecycle theo recovery. | Recovery giữ unknown/fence, task blocked và không tạo attempt mới; AI độc lập SIGKILL worker của fixture riêng để kiểm chứng. | changed | P07-05, regression liên quan |
| P07-07 | Run thật tới UI cần grant/CG01 chưa được cấp. | Không thay mock thành run thật; giữ blocker và test IDs. | blocked | P07-07, regression liên quan |

## Chi tiết từng finding

### C02 — Dependency và quyết định

- Expected/actual nguồn: Xem case C02 trong [report r002](../../../tests/results/phase-07/20261009T121142+0700-r002-test/report.md).
- Nguyên nhân: Dependency chưa được Chủ tịch nghiệm thu; chỉ thị hiện tại cho phép sửa code nền, không cấp CG01/grant.
- Trạng thái xử lý: blocked
- Thay đổi: Giữ trạng thái chính thức và ghi nguồn, không tự nghiệm thu Phase05/06.
- Phản biện: Không có.
- Kiểm tra trong lúc sửa: Xem [commands](evidence/commands.md). Changed chỉ ghi nhận code/evidence đã làm, không tự đóng finding.
- Còn thiếu/blocker: Retest độc lập đầy đủ; case cần inference thật vẫn chờ CG01 và grant mới.
- Retest cần chạy: C02, happy path/negative/race và regression theo checklist, không gọi model trái grant.

### C03 — Criteria/demo

- Expected/actual nguồn: Xem case C03 trong [report r002](../../../tests/results/phase-07/20261009T121142+0700-r002-test/report.md).
- Nguyên nhân: Demo cần model thật và grant riêng; không dùng fixture để thay gate.
- Trạng thái xử lý: blocked
- Thay đổi: Không chạy inference; UI/HTTP thử nghiệm riêng được QA kiểm, demo thật vẫn chờ CG01/grant.
- Phản biện: Không có.
- Kiểm tra trong lúc sửa: Xem [commands](evidence/commands.md). Changed chỉ ghi nhận code/evidence đã làm, không tự đóng finding.
- Còn thiếu/blocker: Retest độc lập đầy đủ; case cần inference thật vẫn chờ CG01 và grant mới.
- Retest cần chạy: C03, happy path/negative/race và regression theo checklist, không gọi model trái grant.

### C06 — Markdown/HTML

- Expected/actual nguồn: Xem case C06 trong [report r002](../../../tests/results/phase-07/20261009T121142+0700-r002-test/report.md).
- Nguyên nhân: UI/tài liệu chưa đồng bộ ở snapshot r002.
- Trạng thái xử lý: changed
- Thay đổi: RuntimePanel heartbeat worker/SSE riêng, GET cập nhật run, cache có nhãn; README/spec/evidence/master-plan đồng bộ. Pipeline sắp theo số vòng, có 14 regression tests.
- Phản biện: Không có.
- Kiểm tra trong lúc sửa: Xem [commands](evidence/commands.md). Changed chỉ ghi nhận code/evidence đã làm, không tự đóng finding.
- Còn thiếu/blocker: Retest độc lập đầy đủ; case cần inference thật vẫn chờ CG01 và grant mới.
- Retest cần chạy: C06, happy path/negative/race và regression theo checklist, không gọi model trái grant.

### C07 — Regression

- Expected/actual nguồn: Xem case C07 trong [report r002](../../../tests/results/phase-07/20261009T121142+0700-r002-test/report.md).
- Nguyên nhân: GET/list runtime dùng transaction ghi counter gây FK lỗi cho scope không tồn tại.
- Trạng thái xử lý: changed
- Thay đổi: service.transaction(write=False) cho đường đọc; không INSERT/lock counter/guard khi GET. Regression được rerun trên PostgreSQL disposable.
- Phản biện: Không có.
- Kiểm tra trong lúc sửa: Xem [commands](evidence/commands.md). Changed chỉ ghi nhận code/evidence đã làm, không tự đóng finding.
- Còn thiếu/blocker: Retest độc lập đầy đủ; case cần inference thật vẫn chờ CG01 và grant mới.
- Retest cần chạy: C07, happy path/negative/race và regression theo checklist, không gọi model trái grant.

### P07-02 — Ordering/reconnect

- Expected/actual nguồn: Xem case P07-02 trong [report r002](../../../tests/results/phase-07/20261009T121142+0700-r002-test/report.md).
- Nguyên nhân: Thiếu evidence HTTP disconnect/reconnect ở r002, chưa xác nhận bug source.
- Trạng thái xử lý: no-change
- Thay đổi: Giữ feed/cursor; AI độc lập thực hiện HTTP/SSE loopback thật, Last-Event-ID reconnect và logout thu hồi stream ở retest.
- Phản biện: Không có.
- Kiểm tra trong lúc sửa: Xem [commands](evidence/commands.md). Changed chỉ ghi nhận code/evidence đã làm, không tự đóng finding.
- Còn thiếu/blocker: Retest độc lập đầy đủ; case cần inference thật vẫn chờ CG01 và grant mới.
- Retest cần chạy: P07-02, happy path/negative/race và regression theo checklist, không gọi model trái grant.

### P07-04 — Heartbeat/offline UI

- Expected/actual nguồn: Xem case P07-04 trong [report r002](../../../tests/results/phase-07/20261009T121142+0700-r002-test/report.md).
- Nguyên nhân: UI thiếu đối chiếu heartbeat worker và trạng thái stale/offline.
- Trạng thái xử lý: changed
- Thay đổi: Worker heartbeat/lease riêng với kết nối SSE, GET poll10s chỉ active run, event-triggered refresh; cache có nhãn chưa đối chiếu và logout hủy timer/stream.
- Phản biện: Không có.
- Kiểm tra trong lúc sửa: Xem [commands](evidence/commands.md). Changed chỉ ghi nhận code/evidence đã làm, không tự đóng finding.
- Còn thiếu/blocker: Retest độc lập đầy đủ; case cần inference thật vẫn chờ CG01 và grant mới.
- Retest cần chạy: P07-04, happy path/negative/race và regression theo checklist, không gọi model trái grant.

### P07-05 — Crash/unknown outcome

- Expected/actual nguồn: Xem case P07-05 trong [report r002](../../../tests/results/phase-07/20261009T121142+0700-r002-test/report.md).
- Nguyên nhân: Thiếu process-kill evidence và cần task lifecycle theo recovery.
- Trạng thái xử lý: changed
- Thay đổi: Recovery giữ unknown/fence, task blocked và không tạo attempt mới; AI độc lập SIGKILL worker của fixture riêng để kiểm chứng.
- Phản biện: Không có.
- Kiểm tra trong lúc sửa: Xem [commands](evidence/commands.md). Changed chỉ ghi nhận code/evidence đã làm, không tự đóng finding.
- Còn thiếu/blocker: Retest độc lập đầy đủ; case cần inference thật vẫn chờ CG01 và grant mới.
- Retest cần chạy: P07-05, happy path/negative/race và regression theo checklist, không gọi model trái grant.

### P07-07 — Run thật đến UI

- Expected/actual nguồn: Xem case P07-07 trong [report r002](../../../tests/results/phase-07/20261009T121142+0700-r002-test/report.md).
- Nguyên nhân: Run thật tới UI cần grant/CG01 chưa được cấp.
- Trạng thái xử lý: blocked
- Thay đổi: Không thay mock thành run thật; giữ blocker và test IDs.
- Phản biện: Không có.
- Kiểm tra trong lúc sửa: Xem [commands](evidence/commands.md). Changed chỉ ghi nhận code/evidence đã làm, không tự đóng finding.
- Còn thiếu/blocker: Retest độc lập đầy đủ; case cần inference thật vẫn chờ CG01 và grant mới.
- Retest cần chạy: P07-07, happy path/negative/race và regression theo checklist, không gọi model trái grant.

## Cleanup và bước tiếp theo

- Cleanup: Tests thuộc PostgreSQL/worker/browser preview riêng; không reset DB/project runtime hoặc gateway shared.
- Evidence: [manifest](evidence/source-manifest.json), [commands](evidence/commands.md).
- Retest tiếp theo: AI độc lập r003; liên kết vào sổ vòng khi report tồn tại.
- Blocker: CG01 proof thật, grant từng batch và nghiệm thu dependency; không tự đóng bằng fixture.
- Sổ vòng: [rounds](../../../tests/results/phase-07/README.md).
