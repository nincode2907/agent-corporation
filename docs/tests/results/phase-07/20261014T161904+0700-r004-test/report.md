# Kiểm định Phase 07 — 20261014T161904+0700-r004-test

## Thông tin batch

- Phase: 07
- Test batch: 20261014T161904+0700-r004-test
- Vòng: r004
- Bắt đầu / kết thúc: 2026-10-14T16:19:04+07:00 / 2026-10-14T16:23:17+07:00 (Asia/Ho_Chi_Minh)
- Người/AI kiểm định: `/root/phase06_09_independent_check`
- Độc lập với AI triển khai/remake: tester agent riêng được giao bởi `/root`; không sửa product source.
- Yêu cầu/phạm vi: recheck Phase 06–09, test-only. Không inference, grant, shared DB/runtime changes hay master-plan status.
- Source: dirty worktree; xem [source manifest](evidence/source-manifest.json).
- Tool versions/commands: [commands](evidence/commands.md).
- Inference/grant: không gọi; grant thật = 0.
- Dependency: [master plan](../../../../master-plan.md), [phase checklist](../../../phases/phase-07.md), [product spec](../../../../product-spec.md).
- Supersedes: [r003](../20261009T145600+0700-r003-test/report.md)
- Remake nguồn: Không có remake mới từ report nguồn; batch này kiểm source hiện tại theo yêu cầu.
- Kết luận kỹ thuật: cần sửa
- Quyết định Chủ tịch: Chưa có.

## Mapping và phạm vi kiểm định

| Tiêu chí / nguồn | Test IDs | Bắt buộc | Ghi chú |
| --- | --- | --- | --- |
| AC1: committed sequence và reconnect không mất/nhân đôi | P07-01, P07-02, P07-03 | Có | P07-02/03 route regression fail. |
| AC2: heartbeat/offline và reconcile unknown | P07-04, P07-05 | Có | Runtime tests blocked. |
| AC3: crash không duplicate; app context recovery | P07-05, P07-06, P07-07 | Có | Live run blocked. |
| C01–C08 | C01–C08 | Có | RULES §5. |

## Tổng hợp

| Tag | Số test |
| --- | ---: |
| clean | 5 |
| need-change | 10 |
| suggestion | 0 |

| Result | Số test |
| --- | ---: |
| pass | 5 |
| fail | 2 |
| blocked | 8 |
| not-run | 0 |
| not-applicable | 0 |

## Kết quả từng test

### C01 — Phạm vi và diff

- Nguồn/tiêu chí: [RULES §5](../../../RULES.md).
- Bắt buộc: có.
- Điều kiện/môi trường: unit/fake fixture local; không gọi inference; không chạy DB integration.
- Bước/lệnh: xem [commands](evidence/commands.md); route probe cô lập, không truy cập DB.
- Kỳ vọng: Tiêu chí bắt buộc phải đạt và có evidence đúng loại.
- Thực tế: Chỉ đọc/chạy checks và tạo report/evidence trong phase; dirty worktree vốn có gồm Employee Chat docs và Phase10 migration của parent.
- Kết quả phản biện: none.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [commands](evidence/commands.md), [source manifest](evidence/source-manifest.json).
- Xử lý/đề xuất: Không có product source edit từ tester.

### C02 — Dependency và nguồn quyết định

- Nguồn/tiêu chí: [RULES §5](../../../RULES.md).
- Bắt buộc: có.
- Điều kiện/môi trường: unit/fake fixture local; không gọi inference; không chạy DB integration.
- Bước/lệnh: xem [commands](evidence/commands.md); route probe cô lập, không truy cập DB.
- Kỳ vọng: Cần có evidence/runtime/dependency; thiếu evidence không được gắn clean.
- Thực tế: 06 phụ thuộc CG01/05; 07→06; 08→07/IG08; 09→08. Master-plan ghi 06–08 blocked, 09 in progress; statuses nhất quán nhưng dependency chưa đủ.
- Kết quả phản biện: none.
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Evidence: [commands](evidence/commands.md), [source manifest](evidence/source-manifest.json) and [blockers](evidence/blockers.md).
- Xử lý/đề xuất: Giữ blocker; không suy nghiệm thu từ report cũ.

### C03 — Criteria và demo

- Nguồn/tiêu chí: [RULES §5](../../../RULES.md).
- Bắt buộc: có.
- Điều kiện/môi trường: unit/fake fixture local; không gọi inference; không chạy DB integration.
- Bước/lệnh: xem [commands](evidence/commands.md); route probe cô lập, không truy cập DB.
- Kỳ vọng: Cần có evidence/runtime/dependency; thiếu evidence không được gắn clean.
- Thực tế: Không có live demo Phase06–08; Phase09 demo hai task/pause/restart/resume/retry chưa có evidence.
- Kết quả phản biện: none.
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Evidence: [commands](evidence/commands.md), [source manifest](evidence/source-manifest.json) and [blockers](evidence/blockers.md).
- Xử lý/đề xuất: Cần đúng run/demo và evidence theo blocker.

### C04 — Không thực thi âm thầm

- Nguồn/tiêu chí: [RULES §5](../../../RULES.md).
- Bắt buộc: có.
- Điều kiện/môi trường: unit/fake fixture local; không gọi inference; không chạy DB integration.
- Bước/lệnh: xem [commands](evidence/commands.md); route probe cô lập, không truy cập DB.
- Kỳ vọng: Tiêu chí bắt buộc phải đạt và có evidence đúng loại.
- Thực tế: Tests dùng fake/local transport; source cho thấy idle/replay không dispatch inference/tool; Phase09 chưa có auto worker dispatch.
- Kết quả phản biện: none.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [commands](evidence/commands.md), [source manifest](evidence/source-manifest.json).
- Xử lý/đề xuất: Giữ gate rõ ràng; không gọi model.

### C05 — Scope và dữ liệu nhạy cảm

- Nguồn/tiêu chí: [RULES §5](../../../RULES.md).
- Bắt buộc: có.
- Điều kiện/môi trường: unit/fake fixture local; không gọi inference; không chạy DB integration.
- Bước/lệnh: xem [commands](evidence/commands.md); không kết nối DB shared.
- Kỳ vọng: Negative cross-scope checks và redaction evidence đủ ở các lớp backend/UI liên quan.
- Thực tế: Owner auth/cursor scope/redaction unit checks pass; cross-company/environment RLS/API integration chưa được rerun trên DB disposable. Evidence current batch chưa đủ để kết luận đầy đủ scope boundary.
- Kết quả phản biện: none.
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Evidence: [commands](evidence/commands.md), [source manifest](evidence/source-manifest.json), [blockers](evidence/blockers.md).
- Xử lý/đề xuất: Cần DB fixture disposable để kiểm RLS/API cross-scope và cleanup scoped.

### C06 — Tài liệu và bản nhìn

- Nguồn/tiêu chí: [RULES §5](../../../RULES.md).
- Bắt buộc: có.
- Điều kiện/môi trường: unit/fake fixture local; không gọi inference; không chạy DB integration.
- Bước/lệnh: xem [commands](evidence/commands.md); route probe cô lập, không truy cập DB.
- Kỳ vọng: Tiêu chí bắt buộc phải đạt và có evidence đúng loại.
- Thực tế: Đối chiếu checklist/spec/roadmap; validate_phase00 đạt contract 32 requirements/15 screens/9 flows/35 baseline events; status không đổi.
- Kết quả phản biện: none.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [commands](evidence/commands.md), [source manifest](evidence/source-manifest.json).
- Xử lý/đề xuất: Không sửa docs/status trong test batch.

### C07 — Regression liên quan

- Nguồn/tiêu chí: [RULES §5](../../../RULES.md).
- Bắt buộc: có.
- Điều kiện/môi trường: unit/fake fixture local; không gọi inference; không chạy DB integration.
- Bước/lệnh: xem [commands](evidence/commands.md); route probe cô lập, không truy cập DB.
- Kỳ vọng: Tiêu chí bắt buộc phải đạt và có evidence đúng loại.
- Thực tế: 61 API unit/TestClient tests, web lint/build và docs validator pass; reconnect regression riêng fail được ghi tại P07-02/03.
- Kết quả phản biện: none.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [commands](evidence/commands.md), [source manifest](evidence/source-manifest.json).
- Xử lý/đề xuất: Suite tổng pass không loại bỏ finding cụ thể.

### C08 — Tái kiểm định được

- Nguồn/tiêu chí: [RULES §5](../../../RULES.md).
- Bắt buộc: có.
- Điều kiện/môi trường: unit/fake fixture local; không gọi inference; không chạy DB integration.
- Bước/lệnh: xem [commands](evidence/commands.md); route probe cô lập, không truy cập DB.
- Kỳ vọng: Tiêu chí bắt buộc phải đạt và có evidence đúng loại.
- Thực tế: Có source hashes, commands, blockers, regression probe, IDs/tags; git diff --check pass.
- Kết quả phản biện: none.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [commands](evidence/commands.md), [source manifest](evidence/source-manifest.json).
- Xử lý/đề xuất: Retest finding bằng batch mới.

### P07-01 — Lưu trước phát

- Nguồn/tiêu chí: [phase checklist](../../../phases/phase-07.md).
- Bắt buộc: có.
- Điều kiện/môi trường: unit/fake fixture local; không gọi inference; không chạy DB integration.
- Bước/lệnh: xem [commands](evidence/commands.md); route probe cô lập, không truy cập DB.
- Kỳ vọng: Cần có evidence/runtime/dependency; thiếu evidence không được gắn clean.
- Thực tế: Source dùng transaction/outbox; DB atomicity/failpoint test dùng fixture DB và không được chạy trên DB đang dùng.
- Kết quả phản biện: none.
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Evidence: [commands](evidence/commands.md), [source manifest](evidence/source-manifest.json) and [blockers](evidence/blockers.md).
- Xử lý/đề xuất: Chạy integration fixture trong PostgreSQL disposable.

### P07-02 — Ordering và reconnect

- Nguồn/tiêu chí: [phase checklist](../../../phases/phase-07.md).
- Bắt buộc: có.
- Điều kiện/môi trường: unit/fake fixture local; không gọi inference; không chạy DB integration.
- Bước/lệnh: xem [commands](evidence/commands.md); route probe cô lập, không truy cập DB.
- Kỳ vọng: A valid SSE reconnect with an advanced Last-Event-ID continues from that cursor; no 400.
- Thực tế: Route probe: stream query có cursor ban đầu và Last-Event-ID tiến tới cursor mới trả 400 `Cursor query và Last-Event-ID không khớp.` EventSource reconnect giữ query cũ nhưng gửi Last-Event-ID mới.
- Kết quả phản biện: none.
- Tag: need-change
- Kết quả: fail
- Mức độ: major
- Evidence: [route probe](evidence/reconnect_last_event_id.py), [observed output](evidence/reconnect-probe.txt), [commands](evidence/commands.md).
- Xử lý/đề xuất: Sửa cursor reconnect ở client/server; retest nhiều event và auto reconnect.

### P07-03 — Gap/cursor boundary

- Nguồn/tiêu chí: [phase checklist](../../../phases/phase-07.md).
- Bắt buộc: có.
- Điều kiện/môi trường: unit/fake fixture local; không gọi inference; không chạy DB integration.
- Bước/lệnh: xem [commands](evidence/commands.md); route probe cô lập, không truy cập DB.
- Kỳ vọng: Valid reconnect is distinct from a real cursor gap; UI explains a gap and reload action.
- Thực tế: Cursor tamper/scope/expiry unit tests pass; reconnect hợp lệ sau event lại 400 như P07-02, và EventSource onerror chỉ đặt reconnecting chứ không thông báo gap rõ.
- Kết quả phản biện: none.
- Tag: need-change
- Kết quả: fail
- Mức độ: major
- Evidence: [route probe](evidence/reconnect_last_event_id.py), [observed output](evidence/reconnect-probe.txt), [commands](evidence/commands.md).
- Xử lý/đề xuất: Sửa cùng P07-02; thử gap thật và trạng thái reload.

### P07-04 — Heartbeat/offline

- Nguồn/tiêu chí: [phase checklist](../../../phases/phase-07.md).
- Bắt buộc: có.
- Điều kiện/môi trường: unit/fake fixture local; không gọi inference; không chạy DB integration.
- Bước/lệnh: xem [commands](evidence/commands.md); route probe cô lập, không truy cập DB.
- Kỳ vọng: Cần có evidence/runtime/dependency; thiếu evidence không được gắn clean.
- Thực tế: Feed envelope unit tests pass; browser disconnect và worker heartbeat không được chạy trong batch.
- Kết quả phản biện: none.
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Evidence: [commands](evidence/commands.md), [source manifest](evidence/source-manifest.json) and [blockers](evidence/blockers.md).
- Xử lý/đề xuất: Browser/runtime QA với scope fixture an toàn.

### P07-05 — Crash và unknown outcome

- Nguồn/tiêu chí: [phase checklist](../../../phases/phase-07.md).
- Bắt buộc: có.
- Điều kiện/môi trường: unit/fake fixture local; không gọi inference; không chạy DB integration.
- Bước/lệnh: xem [commands](evidence/commands.md); route probe cô lập, không truy cập DB.
- Kỳ vọng: Cần có evidence/runtime/dependency; thiếu evidence không được gắn clean.
- Thực tế: Crash fencing cần PostgreSQL/worker fixture; không chạy với DB của app.
- Kết quả phản biện: none.
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Evidence: [commands](evidence/commands.md), [source manifest](evidence/source-manifest.json) and [blockers](evidence/blockers.md).
- Xử lý/đề xuất: DB disposable và worker runtime tách biệt; không dispatch model.

### P07-06 — Session/context recovery

- Nguồn/tiêu chí: [phase checklist](../../../phases/phase-07.md).
- Bắt buộc: có.
- Điều kiện/môi trường: unit/fake fixture local; không gọi inference; không chạy DB integration.
- Bước/lệnh: xem [commands](evidence/commands.md); route probe cô lập, không truy cập DB.
- Kỳ vọng: Cần có evidence/runtime/dependency; thiếu evidence không được gắn clean.
- Thực tế: Không test gateway session invalidation/recovery; không có run authorized.
- Kết quả phản biện: none.
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Evidence: [commands](evidence/commands.md), [source manifest](evidence/source-manifest.json) and [blockers](evidence/blockers.md).
- Xử lý/đề xuất: Fake adapter recovery suite, live only with CG01/grant.

### P07-07 — Run thật đến UI

- Nguồn/tiêu chí: [phase checklist](../../../phases/phase-07.md).
- Bắt buộc: có.
- Điều kiện/môi trường: unit/fake fixture local; không gọi inference; không chạy DB integration.
- Bước/lệnh: xem [commands](evidence/commands.md); route probe cô lập, không truy cập DB.
- Kỳ vọng: Cần có evidence/runtime/dependency; thiếu evidence không được gắn clean.
- Thực tế: Grant thật = 0; không có live run/events/SSE/UI correlation.
- Kết quả phản biện: none.
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Evidence: [commands](evidence/commands.md), [source manifest](evidence/source-manifest.json) and [blockers](evidence/blockers.md).
- Xử lý/đề xuất: IG08/live run sau CG01 và grant riêng.

## Integration / release gates

| Gate áp dụng | Verdict | Test IDs | Evidence/dependency |
| --- | --- | --- | --- |
| No dedicated IG | BLOCKED | C02, P07-07 | Dependency/live criteria lack evidence; no inference/grant. |

## Cleanup, limits, handoff

- Cleanup: No DB rows, migrations, runtime/process/container, browser session, gateway calls, inference or source product edits.
- Unverified: all need-change/blocked cases and conditions in [blockers](evidence/blockers.md).
- Needs change: P07-02/P07-03 major; reconnect mismatch reproduced.
- Optional suggestions: none.
- Next: Remake P07 reconnect within Phase 07, then independent retest; live cases still need CG01/grant.
- Handoff: technical test result only; no phase acceptance/status update.
