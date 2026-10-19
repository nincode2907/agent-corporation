# Kiểm định Phase 11 — 20261015T085652+0700-r004-test

## Thông tin batch

- Phase: 11
- Test batch: `20261015T085652+0700-r004-test`
- Vòng: r004
- Bắt đầu / kết thúc: 2026-10-15 08:56:52–09:02:32 +07:00 (Asia/Ho_Chi_Minh)
- Người/AI kiểm định: `/root/phase11_independent_test`, độc lập với AI remake `/root`
- Yêu cầu/phạm vi: kiểm định r003 remake; full prior redaction matrix, escaped JSON quote/backslash, valid JSON, full-value replacement, hash/byte_count; safe focused regression; không sửa source/master-plan.
- Source: dirty worktree, chưa có commit; [source manifest](evidence/source-manifest.json) có hashes SHA-256. `redaction.py` modified, Phase 11 tools/tests untracked.
- Môi trường: macOS, Python 3.14.8, pytest 9.0.2, uv project `apps/api`.
- Inference: không gọi; grant hiện hành = 0.
- Dependency/quyết định: [Phase 11 roadmap](../../../../master-plan.md#phase-11--hệ-thống-công-cụ-thực-thi), [checklist](../../../phases/phase-11.md), [spec](../../../../product-spec.md), [ADR-0001](../../../../decisions/0001-v1-foundation.md). Phase 10 approval chưa tích hợp executor; Phase 09 lease/recovery/retry còn thiếu.
- Supersedes: [r003 report](../20261015T085217+0700-r003-test/report.md).
- Remake nguồn: [r003 remake](../../../../remakes/phase-11/20261015T085600+0700-r003-remake/remake.md).
- Kết luận kỹ thuật: **chưa đủ bằng chứng** — trong các source path được triển khai, không còn leak canary; executor/end-to-end cases vẫn blocked.
- Quyết định Chủ tịch: Chưa có.

## Mapping criteria

| Tiêu chí / nguồn | IDs | Bắt buộc | Phạm vi |
| --- | --- | --- | --- |
| RULES §5 common checks | C01–C08 | Có | Mỗi case riêng dưới đây. |
| AC1: chặn file/secret ngoài workspace và tool/network ngoài allowlist | P11-01, P11-02, P11-03 | Có | Reader/validator unit pass; executor enforcement chưa có. |
| AC2: run thật có diff/test exit/artifact; redaction giữ correlation | P11-05, P11-06 | Có | Local file adapter redaction/metadata đã kiểm; các runtime channels/correlation chưa chạy được. |
| AC3: retry không lặp side effect khi outcome unknown | P11-04, P11-07 | Có | Approval/receipt/replay chưa nối executor. |
| Demo: sửa file, chạy test, đọc trang allowlist trong sandbox; thử traversal/command deny | C03, P11-02/03/05 | Có | Sandbox/runtime demo còn thiếu. |

## Tổng hợp

| Tag | Số test |
| --- | ---: |
| clean | 6 |
| need-change | 9 |
| suggestion | 0 |

| Result | Số test |
| --- | ---: |
| pass | 6 |
| fail | 0 |
| blocked | 9 |
| not-run | 0 |
| not-applicable | 0 |

## Kết quả từng test

### C01 — Phạm vi và diff

- Nguồn/tiêu chí: [RULES §5](../../../RULES.md#5-kiểm-tra-chung-cho-mọi-phase), chỉ thị r004.
- Bắt buộc: Có.
- Điều kiện/môi trường: Dirty worktree sau remake r003.
- Bước/lệnh: `rtk git status --short`; kiểm SHA-256 trong [manifest](evidence/source-manifest.json).
- Kỳ vọng: Snapshot nhận diện đủ code/test và không có thay đổi phase ngoài scope.
- Thực tế: Redaction module modified; tools/tests và artifacts untracked; không có master-plan edit do reviewer.
- Kết quả phản biện: none.
- Tag: clean.
- Kết quả: pass.
- Mức độ: info.
- Evidence: [manifest](evidence/source-manifest.json), [commands](evidence/commands.md).
- Xử lý/đề xuất: Không có.

### C02 — Dependency và nguồn quyết định

- Nguồn/tiêu chí: [roadmap Phase 11](../../../../master-plan.md#phase-11--hệ-thống-công-cụ-thực-thi), [spec ToolAction/Receipt](../../../../product-spec.md#7-mô-hình-dữ-liệu-logic-và-các-bất-biến), [ADR-0001 D06](../../../../decisions/0001-v1-foundation.md).
- Bắt buộc: Có.
- Điều kiện/môi trường: Đọc roadmap/checklist/spec/remake hiện hành.
- Bước/lệnh: Static comparison; không tin status checkbox.
- Kỳ vọng: Ghi đúng blockers, không nâng trạng thái.
- Thực tế: Phase 11 vẫn “Chưa triển khai”; Phase 10 approval chưa dispatch executor; Phase 09 lease/recovery/retry chưa đạt; inference grant = 0.
- Kết quả phản biện: none.
- Tag: clean.
- Kết quả: pass.
- Mức độ: info.
- Evidence: [roadmap](../../../../master-plan.md#phase-11--hệ-thống-công-cụ-thực-thi), [r003 remake](../../../../remakes/phase-11/20261015T085600+0700-r003-remake/remake.md).
- Xử lý/đề xuất: Giữ nguyên dependency gates.

### C03 — Đủ criteria và demo

- Nguồn/tiêu chí: [RULES §5 C03](../../../RULES.md#5-kiểm-tra-chung-cho-mọi-phase), [demo Phase 11](../../../../master-plan.md#phase-11--hệ-thống-công-cụ-thực-thi), [checklist](../../../phases/phase-11.md).
- Bắt buộc: Có.
- Điều kiện/môi trường: Không có sandbox app/runtime.
- Bước/lệnh: Map từng AC/demo vào P11 cases.
- Kỳ vọng: Mở được demo runtime với write/test/read + artifact và negative cases.
- Thực tế: Hiện chỉ read-only local file adapter; chưa có sandbox, write/terminal/network/browser/artifact/demo runtime.
- Kết quả phản biện: none.
- Tag: need-change.
- Kết quả: blocked.
- Mức độ: major.
- Evidence: [manifest](evidence/source-manifest.json), [commands](evidence/commands.md).
- Xử lý/đề xuất: Chờ executor/sandbox và Phase 09–10 dependency.

### C04 — Không thực thi âm thầm

- Nguồn/tiêu chí: [RULES §5 C04](../../../RULES.md#5-kiểm-tra-chung-cho-mọi-phase), [spec replay](../../../../product-spec.md#9-event-contract-v1-và-replay).
- Bắt buộc: Có.
- Điều kiện/môi trường: Source trace; không bật API/worker.
- Bước/lệnh: `rtk rg -n 'validate_proposal|execute_read_file|WorkspaceReader|list_tools' apps/api/src apps/api/tests/test_phase11_tools.py`.
- Kỳ vọng: Không có mở trang/health/seed/replay dispatch trái scope.
- Thực tế: Không có production executor/API call site cho tools trong source search. Runtime dispatch counter/spy chưa tồn tại.
- Kết quả phản biện: none.
- Tag: need-change.
- Kết quả: blocked.
- Mức độ: major.
- Evidence: [commands](evidence/commands.md).
- Xử lý/đề xuất: Kiểm dispatch counter/network evidence khi integration tồn tại.

### C05 — Scope và dữ liệu nhạy cảm

- Nguồn/tiêu chí: [RULES §5 C05](../../../RULES.md#5-kiểm-tra-chung-cho-mọi-phase), [spec redaction](../../../../product-spec.md#9-event-contract-v1-và-replay).
- Bắt buộc: Có.
- Điều kiện/môi trường: Canary giả qua read-only `execute_read_file`; fixture trong `TemporaryDirectory`.
- Bước/lệnh: Chạy [JSON/canary matrix](evidence/P11-06-json-matrix.py).
- Kỳ vọng: Secret labels/headers/JSON values/PEM redacted trước reader output.
- Thực tế: Full matrix không có canary nào còn trong response, gồm JSON `token` có escaped quote/backslash; không dùng dữ liệu/secret thật.
- Kết quả phản biện: none.
- Tag: clean.
- Kết quả: pass.
- Mức độ: info.
- Evidence: [probe](evidence/P11-06-json-matrix.py), [commands](evidence/commands.md).
- Xử lý/đề xuất: C05 scoped reader behavior pass; các runtime outputs/log persistence vẫn thuộc P11-06 và chưa được nghiệm chứng.

### C06 — Tài liệu và bản nhìn

- Nguồn/tiêu chí: [RULES §5 C06](../../../RULES.md#5-kiểm-tra-chung-cho-mọi-phase), [master-plan Phase 11](../../../../master-plan.md#phase-11--hệ-thống-công-cụ-thực-thi).
- Bắt buộc: Có.
- Điều kiện/môi trường: Đối chiếu roadmap/checklist/remake; không sửa docs nguồn.
- Bước/lệnh: Static review; không render khi roadmap không đổi.
- Kỳ vọng: Giữ status phase; report không overclaim.
- Thực tế: Roadmap vẫn “Chưa triển khai”; không thay master-plan hoặc HTML.
- Kết quả phản biện: none.
- Tag: clean.
- Kết quả: pass.
- Mức độ: info.
- Evidence: [roadmap](../../../../master-plan.md#phase-11--hệ-thống-công-cụ-thực-thi), [remake](../../../../remakes/phase-11/20261015T085600+0700-r003-remake/remake.md).
- Xử lý/đề xuất: Không có doc-source change cần render.

### C07 — Regression liên quan

- Nguồn/tiêu chí: [RULES §5 C07](../../../RULES.md#5-kiểm-tra-chung-cho-mọi-phase); Phase 11 reader and shared redaction changes.
- Bắt buộc: Có.
- Điều kiện/môi trường: Focused API tests; không DB.
- Bước/lệnh: `rtk proxy uv run --project apps/api pytest apps/api/tests/test_phase11_tools.py apps/api/tests/test_sensitive_validation.py -q`.
- Kỳ vọng: Test pass; ghi deprecation warning riêng.
- Thực tế: 26 passed, 1 StarletteDeprecationWarning về `httpx`/`starlette.testclient`, 1.28s.
- Kết quả phản biện: none.
- Tag: clean.
- Kết quả: pass.
- Mức độ: info.
- Evidence: [commands](evidence/commands.md).
- Xử lý/đề xuất: Không có test failure.

### C08 — Có thể tái kiểm định

- Nguồn/tiêu chí: [RULES §5 C08](../../../RULES.md#5-kiểm-tra-chung-cho-mọi-phase), [RULES §7](../../../RULES.md#7-quy-ước-tên-thư-mục-file-và-liên-kết-vòng).
- Bắt buộc: Có.
- Điều kiện/môi trường: Report/evidence r004 snapshot.
- Bước/lệnh: Kiểm manifest/hash, đủ case tags, relative links, probe commands.
- Kỳ vọng: Report tự chứa evidence và có thể tái chạy.
- Thực tế: Tất cả 15 case records, source hashes, canary script, commands và blocker summary được ghi; link check chạy sau khi report hoàn tất.
- Kết quả phản biện: none.
- Tag: clean.
- Kết quả: pass.
- Mức độ: info.
- Evidence: [manifest](evidence/source-manifest.json), [commands](evidence/commands.md).
- Xử lý/đề xuất: Không có.

### P11-01 — Tool schema/capability

- Nguồn/tiêu chí: [checklist](../../../phases/phase-11.md#ca-kiểm-định-riêng-của-phase), [spec permissions](../../../../product-spec.md#10-quyền-auth-và-inference-gates).
- Bắt buộc: Có.
- Điều kiện/môi trường: Focused validator tests; no executor.
- Bước/lệnh: Focused pytest.
- Kỳ vọng: Bad args/version/tool/capability/actor denied before executor.
- Thực tế: Local negative validator tests pass; production policy caller/actor scope/executor integration absent.
- Kết quả phản biện: none.
- Tag: need-change.
- Kết quả: blocked.
- Mức độ: major.
- Evidence: [commands](evidence/commands.md), [manifest](evidence/source-manifest.json).
- Xử lý/đề xuất: Chờ policy/approval integration, rồi verify bypasses.

### P11-02 — File escape

- Nguồn/tiêu chí: [checklist](../../../phases/phase-11.md#ca-kiểm-định-riêng-của-phase), spec workspace/artifact boundary.
- Bắt buộc: Có.
- Điều kiện/môi trường: Existing tmp_path unit tests.
- Bước/lệnh: Focused pytest.
- Kỳ vọng: No outside-root read/write in executor/artifact access.
- Thực tế: Local path traversal/symlink/output cap tests pass; OS sandbox, file write, artifact API, task-root authority integration absent.
- Kết quả phản biện: none.
- Tag: need-change.
- Kết quả: blocked.
- Mức độ: major.
- Evidence: [commands](evidence/commands.md), [manifest](evidence/source-manifest.json).
- Xử lý/đề xuất: Runtime boundary test cần sandbox.

### P11-03 — Network/terminal boundary

- Nguồn/tiêu chí: [checklist](../../../phases/phase-11.md#ca-kiểm-định-riêng-của-phase), Phase 11 roadmap scope.
- Bắt buộc: Có.
- Điều kiện/môi trường: Không chạy terminal/network.
- Bước/lệnh: Registry/source inspection.
- Kỳ vọng: Egress/command deny, timeout/output caps ở sandbox.
- Thực tế: Chỉ có read-file adapter; không có terminal/browser/network executor hoặc sandbox.
- Kết quả phản biện: none.
- Tag: need-change.
- Kết quả: blocked.
- Mức độ: major.
- Evidence: [manifest](evidence/source-manifest.json), [commands](evidence/commands.md).
- Xử lý/đề xuất: Cần sandbox runtime trước test.

### P11-04 — Approval/receipt/idempotency

- Nguồn/tiêu chí: [checklist](../../../phases/phase-11.md#ca-kiểm-định-riêng-của-phase), [spec ToolAction/Receipt](../../../../product-spec.md#7-mô-hình-dữ-liệu-logic-và-các-bất-biến).
- Bắt buộc: Có.
- Điều kiện/môi trường: No side effects.
- Bước/lệnh: So roadmap Phase 09/10 với tool call sites.
- Kỳ vọng: Action prepared, approval consumed atomically; receipt/idempotency; unknown not retried.
- Thực tế: Phase 10 approval chưa tích hợp executor; Phase 09 lease/recovery/retry còn thiếu; tool receipt lifecycle chưa có.
- Kết quả phản biện: none.
- Tag: need-change.
- Kết quả: blocked.
- Mức độ: major.
- Evidence: [roadmap](../../../../master-plan.md#phase-11--hệ-thống-công-cụ-thực-thi), [commands](evidence/commands.md).
- Xử lý/đề xuất: Chờ dependencies; giữ unknown blocked.

### P11-05 — Run code thật trong sandbox

- Nguồn/tiêu chí: [checklist](../../../phases/phase-11.md#ca-kiểm-định-riêng-của-phase), demo/AC2.
- Bắt buộc: Có.
- Điều kiện/môi trường: Grant = 0; sandbox runtime absent.
- Bước/lệnh: Source inventory, no execution.
- Kỳ vọng: Real run, diff, test exit, artifact, linked trace.
- Thực tế: Không có write/code/terminal/browser/network/artifact path; không dùng mock.
- Kết quả phản biện: none.
- Tag: need-change.
- Kết quả: blocked.
- Mức độ: major.
- Evidence: [manifest](evidence/source-manifest.json), [roadmap](../../../../master-plan.md#phase-11--hệ-thống-công-cụ-thực-thi).
- Xử lý/đề xuất: Cần sandbox và explicit grant đúng batch.

### P11-06 — Redaction/correlation

- Nguồn/tiêu chí: [checklist](../../../phases/phase-11.md#ca-kiểm-định-riêng-của-phase), [spec redaction/correlation](../../../../product-spec.md#9-event-contract-v1-và-replay).
- Bắt buộc: Có.
- Điều kiện/môi trường: Probe toàn matrix qua `execute_read_file`; không runtime logs/Inspector.
- Bước/lệnh: [Canary matrix](evidence/P11-06-json-matrix.py) + focused pytest.
- Kỳ vọng: Canary ở args/stdout/stderr/file diff/prompt redacted, JSON remains valid, full JSON secret value replaced, correlation IDs retained.
- Thực tế: Trong file reader, tất cả canary matrix đã che; escaped JSON token value được thay toàn phần; parsed output vẫn là JSON hợp lệ; hash and byte_count match filtered bytes. Tuy nhiên args/stdout/stderr/diff/prompt, Inspector/event correlation/persistence chưa tồn tại để test.
- Kết quả phản biện: none.
- Tag: need-change.
- Kết quả: blocked.
- Mức độ: major.
- Evidence: [probe](evidence/P11-06-json-matrix.py), [commands](evidence/commands.md).
- Xử lý/đề xuất: Không còn source leak được phát hiện trong paths đã code. Retest end-to-end sau khi các channels/executor/trace integration tồn tại.

### P11-07 — Replay và external denial

- Nguồn/tiêu chí: [checklist](../../../phases/phase-11.md#ca-kiểm-định-riêng-của-phase), [spec replay/external authority](../../../../product-spec.md#9-event-contract-v1-và-replay).
- Bắt buộc: Có.
- Điều kiện/môi trường: No replay/external action dispatch.
- Bước/lệnh: Source call-site search.
- Kỳ vọng: Replay is read-only; external send/deploy denied absent authorization.
- Thực tế: Replay/external connector/dispatch counter paths do not exist in Phase 11 code.
- Kết quả phản biện: none.
- Tag: need-change.
- Kết quả: blocked.
- Mức độ: major.
- Evidence: [commands](evidence/commands.md), [manifest](evidence/source-manifest.json).
- Xử lý/đề xuất: Verify when integration exists; no connector added in this test.

## Integration / release gates

| Gate áp dụng | Verdict | Test IDs | Evidence |
| --- | --- | --- | --- |
| Phase 11 không có IG riêng | Không áp dụng | C01–C08, P11-01…07 | Phase 11 checklist; criteria remain mandatory. |

## Cleanup, giới hạn và bàn giao

- Cleanup: Canary probe dùng `TemporaryDirectory`; pytest dùng fixtures riêng.
- Source finding: Không phát hiện trong redaction source/adapter paths được retest.
- Chưa đủ bằng chứng: C03/C04, P11-01…05/P11-07; P11-06 end-to-end channels/correlation cũng blocked. Phase 10 approval chưa integrated, Phase 09 lease/retry/recovery còn thiếu; chưa có OS sandbox/terminal/network/write/artifact/replay; inference grant = 0.
- Kết luận kỹ thuật: **chưa đủ bằng chứng** — 6 clean, 9 blocked, không fail. Không nghiệm thu Phase 11 hoặc cập nhật master-plan.
- Bước tiếp theo: Chạy các case runtime sau khi dependency, sandbox, trace paths và quyền/grant đúng batch đã sẵn sàng.
