# Kiểm định Phase 06 — 20261009T145600+0700-r003-test

## Thông tin batch

- Phase: 06
- Test batch: 20261009T145600+0700-r003-test
- Vòng: r003
- Bắt đầu / kết thúc: 2026-10-09T14:56:00+07:00 / 2026-10-09T15:15:26.125294+07:00
- Người/AI kiểm định: /root/independent_06_07_qa
- Độc lập với AI triển khai/remake: /root, runtime06 và runtime_ui khác /root/independent_06_07_qa.
- Yêu cầu/phạm vi được giao: Chủ tịch yêu cầu fix blocker và thực hiện lại Phase06–07; agent này chỉ test, không sửa source sản phẩm.
- Source: Dirty worktree; [manifest](evidence/source-manifest.json), source cuối đã được bàn giao 14:58:34+07:00.
- Môi trường/config/tool versions: [commands](evidence/commands.md); PostgreSQL18.6 disposable, Python3.14.8/pytest9.0.2, uv0.12.23, Node24.21.0/Vite8.3.3.
- Inference: Không gọi; grant thật 0, không probe/shared gateway POST. Grants và outcomes fixture chỉ trong PostgreSQL disposable.
- Dependency/quyết định nghiệm thu: [master-plan](../../../../master-plan.md); chỉ thị cho phép sửa nền, chưa có nghiệm thu dependency/CG01/grant.
- Supersedes: [r002](../20261009T121142+0700-r002-test/report.md)
- Remake nguồn: [r002 remake](../../../../remakes/phase-06/20261009T145834+0700-r002-remake/remake.md)
- Kết luận kỹ thuật: chưa đủ bằng chứng
- Quyết định Chủ tịch: Chưa có

## Mapping và phạm vi kiểm định

| Criteria | Test IDs | Bắt buộc |
| --- | --- | --- |
| AC1 model thật/error/abort | P06-03, P06-04 | Có |
| AC2 policy/isolation | P06-01, P06-02, P06-08 | Có |
| AC3 limits/usage | P06-05, P06-06, P06-07 | Có |

## Tổng hợp

| Tag | Số test |
| --- | --- |
| clean | 10 |
| need-change | 6 |
| suggestion | 0 |

| Result | Số test |
| --- | --- |
| pass | 10 |
| fail | 0 |
| blocked | 6 |
| not-run | 0 |
| not-applicable | 0 |

## Kết quả từng test

### C01 — Phạm vi và diff

- Nguồn/tiêu chí: [checklist](../../../phases/phase-06.md), [rule](../../../RULES.md), [Spec](../../../../product-spec.md).
- Bắt buộc: có
- Điều kiện/môi trường: PG disposable và canary/fake transport; các live criteria vẫn yêu cầu grant/CG01 thật.
- Bước/lệnh: [commands](evidence/commands.md); lệnh tests exit0, thao tác UI qua CUA theo [observations](evidence/runtime-observations.md).
- Kỳ vọng: Đúng contract của testID; phải kiểm đủ biến thể, không dùng fixture thay criteria run thật.
- Thực tế: Chỉ sửa nền Phase 06–07 và dependency auth/profile đã được giao; giữ worktree dirty, không triển khai Phase 08.
- Kết quả phản biện: none
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [C07-api-suite.txt](evidence/C07-api-suite.txt), [suite](evidence/C07-api-suite.txt), [manifest](evidence/source-manifest.json).
- Xử lý/đề xuất: Bản sửa/kiểm chứng đã được AI độc lập xác nhận; giữ regression.

### C02 — Dependency và quyết định nghiệm thu

- Nguồn/tiêu chí: [checklist](../../../phases/phase-06.md), [rule](../../../RULES.md), [Spec](../../../../product-spec.md).
- Bắt buộc: có
- Điều kiện/môi trường: PG disposable và canary/fake transport; các live criteria vẫn yêu cầu grant/CG01 thật.
- Bước/lệnh: [commands](evidence/commands.md); lệnh tests exit0, thao tác UI qua CUA theo [observations](evidence/runtime-observations.md).
- Kỳ vọng: Đúng contract của testID; phải kiểm đủ biến thể, không dùng fixture thay criteria run thật.
- Thực tế: Dependency Phase 05/CG01 và nghiệm thu chưa đầy đủ. Chỉ thị hiện tại cho phép sửa nền 06–07; không cấp grant hoặc tự nghiệm thu dependency.
- Kết quả phản biện: none
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Evidence: [runtime-observations.md](evidence/runtime-observations.md), [suite](evidence/C07-api-suite.txt), [manifest](evidence/source-manifest.json).
- Xử lý/đề xuất: Giữ blocker thật đến khi dependency/CG01/grant đúng batch được Chủ tịch quyết định; không tự gọi inference.

### C03 — Criteria và demo đúng loại

- Nguồn/tiêu chí: [checklist](../../../phases/phase-06.md), [rule](../../../RULES.md), [Spec](../../../../product-spec.md).
- Bắt buộc: có
- Điều kiện/môi trường: PG disposable và canary/fake transport; các live criteria vẫn yêu cầu grant/CG01 thật.
- Bước/lệnh: [commands](evidence/commands.md); lệnh tests exit0, thao tác UI qua CUA theo [observations](evidence/runtime-observations.md).
- Kỳ vọng: Đúng contract của testID; phải kiểm đủ biến thể, không dùng fixture thay criteria run thật.
- Thực tế: Đã kiểm UI, HTTP/SSE và worker fixture cô lập. Demo bắt buộc với model thật vẫn chưa có grant và CG01; không thay bằng fixture.
- Kết quả phản biện: none
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Evidence: [runtime-observations.md](evidence/runtime-observations.md), [suite](evidence/C07-api-suite.txt), [manifest](evidence/source-manifest.json).
- Xử lý/đề xuất: Giữ blocker thật đến khi dependency/CG01/grant đúng batch được Chủ tịch quyết định; không tự gọi inference.

### C04 — Không thực thi âm thầm

- Nguồn/tiêu chí: [checklist](../../../phases/phase-06.md), [rule](../../../RULES.md), [Spec](../../../../product-spec.md).
- Bắt buộc: có
- Điều kiện/môi trường: PG disposable và canary/fake transport; các live criteria vẫn yêu cầu grant/CG01 thật.
- Bước/lệnh: [commands](evidence/commands.md); lệnh tests exit0, thao tác UI qua CUA theo [observations](evidence/runtime-observations.md).
- Kỳ vọng: Đúng contract của testID; phải kiểm đủ biến thể, không dùng fixture thay criteria run thật.
- Thực tế: Mở Settings, đăng nhập, lưu profile và reload không gọi model. Worker explicit; missing proof/grant deny. Test transport là fake, gateway thực tế không được gọi.
- Kết quả phản biện: none
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [C05-independent-runtime.txt](evidence/C05-independent-runtime.txt), [suite](evidence/C07-api-suite.txt), [manifest](evidence/source-manifest.json).
- Xử lý/đề xuất: Bản sửa/kiểm chứng đã được AI độc lập xác nhận; giữ regression.

### C05 — Auth, scope và dữ liệu nhạy cảm

- Nguồn/tiêu chí: [checklist](../../../phases/phase-06.md), [rule](../../../RULES.md), [Spec](../../../../product-spec.md).
- Bắt buộc: có
- Điều kiện/môi trường: PG disposable và canary/fake transport; các live criteria vẫn yêu cầu grant/CG01 thật.
- Bước/lệnh: [commands](evidence/commands.md); lệnh tests exit0, thao tác UI qua CUA theo [observations](evidence/runtime-observations.md).
- Kỳ vọng: Đúng contract của testID; phải kiểm đủ biến thể, không dùng fixture thay criteria run thật.
- Thực tế: Real PG + HTTP xác minh session hashes, Owner scope, CSRF, profile CAS, expiry/logout. Feed chỉ metadata; canary không bị echo trong validation/SSE, SQL error API503 hoặc worker CLI stderr (53 final units).
- Kết quả phản biện: none
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [C05-independent-runtime.txt](evidence/C05-independent-runtime.txt), [suite](evidence/C07-api-suite.txt), [manifest](evidence/source-manifest.json).
- Xử lý/đề xuất: Bản sửa/kiểm chứng đã được AI độc lập xác nhận; giữ regression.

### C06 — Markdown và HTML

- Nguồn/tiêu chí: [checklist](../../../phases/phase-06.md), [rule](../../../RULES.md), [Spec](../../../../product-spec.md).
- Bắt buộc: có
- Điều kiện/môi trường: PG disposable và canary/fake transport; các live criteria vẫn yêu cầu grant/CG01 thật.
- Bước/lệnh: [commands](evidence/commands.md); lệnh tests exit0, thao tác UI qua CUA theo [observations](evidence/runtime-observations.md).
- Kỳ vọng: Đúng contract của testID; phải kiểm đủ biến thể, không dùng fixture thay criteria run thật.
- Thực tế: Đã đối chiếu Markdown/spec/ADR/evidence/current implementation. validate_phase00 đạt35events/3HTMLdeterministic/langvi/favicon/JS; framework14 tests và report validators16/15IDs/links đạt. Pipeline logicalround chọn r003, không coi timestamp remake muộn hơn là sửa chưa được retest.
- Kết quả phản biện: none
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [C06-docs-final.txt](evidence/C06-docs-final.txt), [suite](evidence/C07-api-suite.txt), [manifest](evidence/source-manifest.json).
- Xử lý/đề xuất: Đồng bộ đã được AI độc lập xác minh; root sẽ render lại projection theo report chốt.

### C07 — Regression liên quan

- Nguồn/tiêu chí: [checklist](../../../phases/phase-06.md), [rule](../../../RULES.md), [Spec](../../../../product-spec.md).
- Bắt buộc: có
- Điều kiện/môi trường: PG disposable và canary/fake transport; các live criteria vẫn yêu cầu grant/CG01 thật.
- Bước/lệnh: [commands](evidence/commands.md); lệnh tests exit0, thao tác UI qua CUA theo [observations](evidence/runtime-observations.md).
- Kỳ vọng: Đúng contract của testID; phải kiểm đủ biến thể, không dùng fixture thay criteria run thật.
- Thực tế: PG/schema runtime source đạt full API 73/73 trước bổ sung handler SQL redaction. Sau bổ sung: 53 non-DB units đạt, gồm API503 không echo parameters và worker CLI exit1 không traceback. Independent PG/API/SSE/process-kill 5/5, framework14/14, web lint/build/diff check đạt. Không rerun PG sau handler-only patch; service/migrations không đổi.
- Kết quả phản biện: none
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [C07-api-suite.txt](evidence/C07-api-suite.txt), [suite](evidence/C07-api-suite.txt), [manifest](evidence/source-manifest.json).
- Xử lý/đề xuất: Bản sửa/kiểm chứng đã được AI độc lập xác nhận; giữ regression.

### C08 — Có thể tái kiểm định

- Nguồn/tiêu chí: [checklist](../../../phases/phase-06.md), [rule](../../../RULES.md), [Spec](../../../../product-spec.md).
- Bắt buộc: có
- Điều kiện/môi trường: PG disposable và canary/fake transport; các live criteria vẫn yêu cầu grant/CG01 thật.
- Bước/lệnh: [commands](evidence/commands.md); lệnh tests exit0, thao tác UI qua CUA theo [observations](evidence/runtime-observations.md).
- Kỳ vọng: Đúng contract của testID; phải kiểm đủ biến thể, không dùng fixture thay criteria run thật.
- Thực tế: Đủ IDs, commands, executable independent cases, source hashes, scoped cleanup và evidence. Không dùng pass unit để nghiệm thu live criteria.
- Kết quả phản biện: none
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [commands.md](evidence/commands.md), [suite](evidence/C07-api-suite.txt), [manifest](evidence/source-manifest.json).
- Xử lý/đề xuất: Bản sửa/kiểm chứng đã được AI độc lập xác nhận; giữ regression.

### P06-01 — Grant trước dispatch

- Nguồn/tiêu chí: [checklist](../../../phases/phase-06.md), [rule](../../../RULES.md), [Spec](../../../../product-spec.md).
- Bắt buộc: có
- Điều kiện/môi trường: PG disposable và canary/fake transport; các live criteria vẫn yêu cầu grant/CG01 thật.
- Bước/lệnh: [commands](evidence/commands.md); lệnh tests exit0, thao tác UI qua CUA theo [observations](evidence/runtime-observations.md).
- Kỳ vọng: Đúng contract của testID; phải kiểm đủ biến thể, không dùng fixture thay criteria run thật.
- Thực tế: Unit và PG kiểm missing/revoked/expired/wrong phase/batch/purpose/model/effort, requests/concurrency, stop. Atomically reserve trước transport; negative cases không có POST.
- Kết quả phản biện: none
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [C07-api-suite.txt](evidence/C07-api-suite.txt), [suite](evidence/C07-api-suite.txt), [manifest](evidence/source-manifest.json).
- Xử lý/đề xuất: Bản sửa/kiểm chứng đã được AI độc lập xác nhận; giữ regression.

### P06-02 — Sandbox/input và CG01

- Nguồn/tiêu chí: [checklist](../../../phases/phase-06.md), [rule](../../../RULES.md), [Spec](../../../../product-spec.md).
- Bắt buộc: có
- Điều kiện/môi trường: PG disposable và canary/fake transport; các live criteria vẫn yêu cầu grant/CG01 thật.
- Bước/lệnh: [commands](evidence/commands.md); lệnh tests exit0, thao tác UI qua CUA theo [observations](evidence/runtime-observations.md).
- Kỳ vọng: Đúng contract của testID; phải kiểm đủ biến thể, không dùng fixture thay criteria run thật.
- Thực tế: Đã xác minh bản sửa: JSON list/null/string/invalid, directory/FIFO/symlink đều fail closed. Isolation/privacy/retention/cancellation của inference thật chưa được chứng minh; live case vẫn blocked.
- Kết quả phản biện: none
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Evidence: [C07-api-suite.txt](evidence/C07-api-suite.txt), [suite](evidence/C07-api-suite.txt), [manifest](evidence/source-manifest.json).
- Xử lý/đề xuất: Giữ blocker thật đến khi dependency/CG01/grant đúng batch được Chủ tịch quyết định; không tự gọi inference.

### P06-03 — Một turn text-only thật

- Nguồn/tiêu chí: [checklist](../../../phases/phase-06.md), [rule](../../../RULES.md), [Spec](../../../../product-spec.md).
- Bắt buộc: có
- Điều kiện/môi trường: PG disposable và canary/fake transport; các live criteria vẫn yêu cầu grant/CG01 thật.
- Bước/lệnh: [commands](evidence/commands.md); lệnh tests exit0, thao tác UI qua CUA theo [observations](evidence/runtime-observations.md).
- Kỳ vọng: Đúng contract của testID; phải kiểm đủ biến thể, không dùng fixture thay criteria run thật.
- Thực tế: Không có Owner inference grant cho batch r003; CG01 thật chưa đạt. Không gọi model, không tạo trace/artifact thật giả.
- Kết quả phản biện: none
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Evidence: [runtime-observations.md](evidence/runtime-observations.md), [suite](evidence/C07-api-suite.txt), [manifest](evidence/source-manifest.json).
- Xử lý/đề xuất: Giữ blocker thật đến khi dependency/CG01/grant đúng batch được Chủ tịch quyết định; không tự gọi inference.

### P06-04 — Error/timeout/unknown

- Nguồn/tiêu chí: [checklist](../../../phases/phase-06.md), [rule](../../../RULES.md), [Spec](../../../../product-spec.md).
- Bắt buộc: có
- Điều kiện/môi trường: PG disposable và canary/fake transport; các live criteria vẫn yêu cầu grant/CG01 thật.
- Bước/lệnh: [commands](evidence/commands.md); lệnh tests exit0, thao tác UI qua CUA theo [observations](evidence/runtime-observations.md).
- Kỳ vọng: Đúng contract của testID; phải kiểm đủ biến thể, không dùng fixture thay criteria run thật.
- Thực tế: Fake HTTP và PG kiểm 302, 401, 429, 502/504, tool proposal, cancellation/worker exceptions, lease expiry. Unknown được fence; late success không ghi đè hoặc auto retry.
- Kết quả phản biện: none
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [C07-api-suite.txt](evidence/C07-api-suite.txt), [suite](evidence/C07-api-suite.txt), [manifest](evidence/source-manifest.json).
- Xử lý/đề xuất: Bản sửa/kiểm chứng đã được AI độc lập xác nhận; giữ regression.

### P06-05 — Resource limits và race

- Nguồn/tiêu chí: [checklist](../../../phases/phase-06.md), [rule](../../../RULES.md), [Spec](../../../../product-spec.md).
- Bắt buộc: có
- Điều kiện/môi trường: PG disposable và canary/fake transport; các live criteria vẫn yêu cầu grant/CG01 thật.
- Bước/lệnh: [commands](evidence/commands.md); lệnh tests exit0, thao tác UI qua CUA theo [observations](evidence/runtime-observations.md).
- Kỳ vọng: Đúng contract của testID; phải kiểm đủ biến thể, không dùng fixture thay criteria run thật.
- Thực tế: PG concurrency/global guard xuyên company, request/expiry limits, bounded 429 requeue, rollback và stop đều đạt. Independent case xác minh missing usage giữ reservation cùng grant. Không quảng cáo hard token/USD cap.
- Kết quả phản biện: none
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [C05-independent-runtime.txt](evidence/C05-independent-runtime.txt), [suite](evidence/C07-api-suite.txt), [manifest](evidence/source-manifest.json).
- Xử lý/đề xuất: Bản sửa/kiểm chứng đã được AI độc lập xác nhận; giữ regression.

### P06-06 — Stop/abort baseline

- Nguồn/tiêu chí: [checklist](../../../phases/phase-06.md), [rule](../../../RULES.md), [Spec](../../../../product-spec.md).
- Bắt buộc: có
- Điều kiện/môi trường: PG disposable và canary/fake transport; các live criteria vẫn yêu cầu grant/CG01 thật.
- Bước/lệnh: [commands](evidence/commands.md); lệnh tests exit0, thao tác UI qua CUA theo [observations](evidence/runtime-observations.md).
- Kỳ vọng: Đúng contract của testID; phải kiểm đủ biến thể, không dùng fixture thay criteria run thật.
- Thực tế: Fake socket cancellation, stop/revoke queued và stop in-flight đều được kiểm. Hủy CLI/gateway thật còn thiếu grant/CG01; đóng UI không được coi là abort provider đã xác minh.
- Kết quả phản biện: none
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Evidence: [C07-api-suite.txt](evidence/C07-api-suite.txt), [suite](evidence/C07-api-suite.txt), [manifest](evidence/source-manifest.json).
- Xử lý/đề xuất: Giữ blocker thật đến khi dependency/CG01/grant đúng batch được Chủ tịch quyết định; không tự gọi inference.

### P06-07 — Usage provenance và late correction

- Nguồn/tiêu chí: [checklist](../../../phases/phase-06.md), [rule](../../../RULES.md), [Spec](../../../../product-spec.md).
- Bắt buộc: có
- Điều kiện/môi trường: PG disposable và canary/fake transport; các live criteria vẫn yêu cầu grant/CG01 thật.
- Bước/lệnh: [commands](evidence/commands.md); lệnh tests exit0, thao tác UI qua CUA theo [observations](evidence/runtime-observations.md).
- Kỳ vọng: Đúng contract của testID; phải kiểm đủ biến thể, không dùng fixture thay criteria run thật.
- Thực tế: PG 0006 kiểm immutable correction, dedup/conflict, gateway UUID/span binding, revocation/expiry và unknown fence; không hồi sinh grant. Null/0/cache/reasoning được phân biệt. Live usage từ response thật chưa có grant, nên toàn case vẫn blocked.
- Kết quả phản biện: none
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Evidence: [C07-api-suite.txt](evidence/C07-api-suite.txt), [suite](evidence/C07-api-suite.txt), [manifest](evidence/source-manifest.json).
- Xử lý/đề xuất: Giữ blocker thật đến khi dependency/CG01/grant đúng batch được Chủ tịch quyết định; không tự gọi inference.

### P06-08 — Snapshot, lifecycle và idle

- Nguồn/tiêu chí: [checklist](../../../phases/phase-06.md), [rule](../../../RULES.md), [Spec](../../../../product-spec.md).
- Bắt buộc: có
- Điều kiện/môi trường: PG disposable và canary/fake transport; các live criteria vẫn yêu cầu grant/CG01 thật.
- Bước/lệnh: [commands](evidence/commands.md); lệnh tests exit0, thao tác UI qua CUA theo [observations](evidence/runtime-observations.md).
- Kỳ vọng: Đúng contract của testID; phải kiểm đủ biến thể, không dùng fixture thay criteria run thật.
- Thực tế: GET/list runtime read-only và missing company không còn FK/write side effect. Snapshot giữ Owner profile version, effective grant/policy/history; task transitions + TASK_STARTED atomic, completed → reviewing, unknown → blocked, không accepted. UI waiting không bịa token/worker active.
- Kết quả phản biện: none
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [P06-08-worker-stale.png](evidence/P06-08-worker-stale.png), [suite](evidence/C07-api-suite.txt), [manifest](evidence/source-manifest.json).
- Xử lý/đề xuất: Bản sửa/kiểm chứng đã được AI độc lập xác nhận; giữ regression.

## Integration / release gates

| Gate áp dụng | PASS / FAIL / BLOCKED | Test IDs | Evidence |
| --- | --- | --- | --- |
| Không có IG riêng; live phase criteria | BLOCKED | C03, P06-02, P06-03, P06-06, P06-07 | Chưa có proof CG01 và grant thật |

## Bypass Attempts

| Rule | Attempt | Result |
| --- | --- | --- |
| Owner scope | Login company không được cấp | 403, PASS actualPG |
| CSRF | PUT profile thiếu token | 403, PASS |
| Profile version | Gửi lại version0 sau save | 409, PASS |
| Missing usage | Reserve thêm cùng grant | Deny/unresolved, PASS |
| CG01 metadata | JSON list/FIFO/symlink | Fail closed, PASS |
| Unknown outcome | Crash/late completion/restart | 1 span, no replay, PASS |

## Cleanup, giới hạn và bàn giao

- Cleanup: Chỉ fixture/PG/worker/browser preview của QA. Browser viewport đã reset, tab QA đã đóng; riêng PID preview đã dừng. Container đã xác minh name/label/image rồi docker rm -fv; anonymous volume riêng đã được dọn. Không còn container QA. Fake canary credential và metadata preview cũng đã xóa; evidence giữ nguyên.
- Một lượt independent rerun bị nhiễu do browser fixture còn giữ global guard: đây là guard hoạt động đúng. QA dọn đúng fake reservation và rerun5/5; không đổi source/hạ expectation.
- Chưa kiểm chứng: Demo/run, read isolation/privacy/retention/cancellation và usage thật từ model; không có grant.
- Cần sửa: Không còn lỗi source đã tái hiện trong r002; phần mandatory live/dependency vẫn bị chặn, Projection tài liệu đã xác minh.
- Bước tiếp theo: Dừng phần runtime sản phẩm tại gate; inference chỉ sau grant/CG01 riêng. Không nghiệm thu hoặc tự Phase08.
- Bàn giao: Systematic risk-based coverage completed for assigned scope; kết luận chưa đủ bằng chứng do live gates, không claim phase hoàn tất.
