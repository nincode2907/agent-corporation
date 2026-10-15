# Kiểm định Phase 11 — 20261015T085217+0700-r003-test

## Thông tin batch

- Phase: 11
- Test batch: `20261015T085217+0700-r003-test`
- Vòng: r003
- Bắt đầu / kết thúc: 2026-10-15 08:52:17–08:55:05 +07:00 (Asia/Ho_Chi_Minh)
- Người/AI kiểm định: `/root/phase11_independent_test`, độc lập với AI remake `/root`
- Yêu cầu/phạm vi: kiểm định remake r002, toàn bộ redaction matrix + escaped quote/backslash variants, hash/byte_count; chạy safe regression; không sửa source/master-plan, không DB/runtime dispatch/inference/gateway.
- Source: worktree dirty, chưa có commit; [manifest](evidence/source-manifest.json) có hash SHA-256 source/test snapshot. `redaction.py` modified; tools/tests untracked.
- Môi trường: macOS; Python 3.14.8; pytest 9.0.2; `uv` project `apps/api`.
- Inference: không gọi; grant hiện hành = 0.
- Dependency/quyết định: [Phase 11 roadmap](../../../../master-plan.md#phase-11--hệ-thống-công-cụ-thực-thi), [checklist](../../../phases/phase-11.md), [spec](../../../../product-spec.md), [ADR-0001](../../../../decisions/0001-v1-foundation.md). Phase 10 approval chưa tích hợp executor; Phase 09 lease/recovery/retry chưa hoàn tất.
- Supersedes: [r002 test](../20261015T084733+0700-r002-test/report.md).
- Remake nguồn: [r002 remake](../../../../remakes/phase-11/20261015T085118+0700-r002-remake/remake.md).
- Kết luận kỹ thuật: **cần sửa** — escaped JSON `token` string làm lộ suffix canary; criteria runtime khác còn blocked.
- Quyết định Chủ tịch: Chưa có.

## Mapping criteria

| Tiêu chí / nguồn | IDs | Bắt buộc | Phạm vi |
| --- | --- | --- | --- |
| RULES §5 common review | C01–C08 | Có | Mỗi test có kết quả riêng bên dưới. |
| AC1: deny file/secret ngoài workspace và network/tool ngoài allowlist | P11-01, P11-02, P11-03 | Có | Registry/reader unit tests hiện có; chưa có executor enforcement. |
| AC2: run thật có diff/test exit/artifact, redaction giữ correlation | P11-05, P11-06 | Có | Probe reader redaction/metadata; run thật và correlation event chưa có. |
| AC3: retry không lặp side effect khi outcome unknown | P11-04, P11-07 | Có | Approval/receipt/replay runtime chưa tích hợp. |
| Demo Phase 11: sửa file, chạy test, đọc trang allowlist trong sandbox; deny traversal/command ngoài scope | C03, P11-02/03/05 | Có | Sandbox/runtime demo chưa tồn tại. |

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

- Nguồn/tiêu chí: [RULES §5](../../../RULES.md#5-kiểm-tra-chung-cho-mọi-phase), chỉ thị r003.
- Bắt buộc: Có.
- Điều kiện/môi trường: Dirty worktree; reviewer không sửa product source/master-plan.
- Bước/lệnh: `rtk git status --short`; SHA-256 trong [manifest](evidence/source-manifest.json).
- Kỳ vọng: Chỉ remediation/test/evidence Phase 11, nhận diện dirty files và snapshot.
- Thực tế: `redaction.py` là tracked modification; tools/test và artifacts batch là untracked. Không có phase/master-plan edit từ tester.
- Kết quả phản biện: none.
- Tag: clean.
- Kết quả: pass.
- Mức độ: info.
- Evidence: [manifest](evidence/source-manifest.json), [commands](evidence/commands.md).
- Xử lý/đề xuất: Không có.

### C02 — Dependency và nguồn quyết định

- Nguồn/tiêu chí: [roadmap Phase 11](../../../../master-plan.md#phase-11--hệ-thống-công-cụ-thực-thi), [spec ToolAction/Receipt](../../../../product-spec.md#7-mô-hình-dữ-liệu-logic-và-các-bất-biến), [ADR-0001](../../../../decisions/0001-v1-foundation.md).
- Bắt buộc: Có.
- Điều kiện/môi trường: Đối chiếu nguồn hiện hành và remake r002.
- Bước/lệnh: Đọc roadmap, Phase 11 checklist, spec sections 7/9/10, ADR D06 và remake.
- Kỳ vọng: Ghi đúng dependency, không suy ra executor/phase đã đạt.
- Thực tế: Phase 11 roadmap vẫn “Chưa triển khai”; Phase 10 approval chưa nối executor; Phase 09 lease/retry/recovery còn thiếu. Remake chỉ đổi redaction/test.
- Kết quả phản biện: none.
- Tag: clean.
- Kết quả: pass.
- Mức độ: info.
- Evidence: [roadmap](../../../../master-plan.md#phase-11--hệ-thống-công-cụ-thực-thi), [remake r002](../../../../remakes/phase-11/20261015T085118+0700-r002-remake/remake.md).
- Xử lý/đề xuất: Giữ các dependency làm blocker.

### C03 — Đủ criteria và demo

- Nguồn/tiêu chí: [RULES §5 C03](../../../RULES.md#5-kiểm-tra-chung-cho-mọi-phase), [demo/acceptance Phase 11](../../../../master-plan.md#phase-11--hệ-thống-công-cụ-thực-thi), [checklist](../../../phases/phase-11.md).
- Bắt buộc: Có.
- Điều kiện/môi trường: Không có sandbox app/runtime.
- Bước/lệnh: Mapping AC1–3 với P11 cases.
- Kỳ vọng: Demo runtime gồm sửa file/test/read allowlisted page, artifacts, negative cases.
- Thực tế: Chỉ có read-only file reader; chưa có sandbox, write/terminal/network/browser, artifact/diff pipeline hoặc demo runtime.
- Kết quả phản biện: none.
- Tag: need-change.
- Kết quả: blocked.
- Mức độ: major.
- Evidence: [manifest](evidence/source-manifest.json), [commands](evidence/commands.md).
- Xử lý/đề xuất: Cần executor/sandbox và Phase 09–10 dependency trước demo.

### C04 — Không thực thi âm thầm

- Nguồn/tiêu chí: [RULES §5 C04](../../../RULES.md#5-kiểm-tra-chung-cho-mọi-phase), [spec replay](../../../../product-spec.md#9-event-contract-v1-và-replay).
- Bắt buộc: Có.
- Điều kiện/môi trường: Source trace, không khởi động runtime.
- Bước/lệnh: `rtk rg -n 'validate_proposal|execute_read_file|WorkspaceReader|list_tools' apps/api/src apps/api/tests/test_phase11_tools.py`.
- Kỳ vọng: Không có implicit dispatch trái quyền từ page/health/seed/replay.
- Thực tế: Production references chỉ ở tools module; không có API/executor integration call site. Không chạy runtime nên chưa chứng minh no-dispatch ở mức app.
- Kết quả phản biện: none.
- Tag: need-change.
- Kết quả: blocked.
- Mức độ: major.
- Evidence: [commands](evidence/commands.md).
- Xử lý/đề xuất: Khi dispatch path tồn tại, kiểm dispatch counter/spy và network evidence.

### C05 — Scope và dữ liệu nhạy cảm

- Nguồn/tiêu chí: [RULES §5 C05](../../../RULES.md#5-kiểm-tra-chung-cho-mọi-phase), [spec redaction](../../../../product-spec.md#9-event-contract-v1-và-replay).
- Bắt buộc: Có.
- Điều kiện/môi trường: Canaries tổng hợp qua `WorkspaceReader`/`execute_read_file`; output/log không chứa secret thật.
- Bước/lệnh: Chạy [P11-06 synthetic probe](evidence/P11-06-canary-check.py).
- Kỳ vọng: Credentials—including JSON strings with quotes and backslashes—redacted before tool response; hash and byte_count computed over redacted output.
- Thực tế: Escaped `token` string canary survives after an escaped quote; script reports `leaking_cases=["json_escaped_token"]`. Hash is 64 hex and matches filtered output; byte_count matches filtered output (451 bytes). Other tested canaries were absent.
- Kết quả phản biện: none.
- Tag: need-change.
- Kết quả: fail.
- Mức độ: major.
- Evidence: [probe script](evidence/P11-06-canary-check.py), [commands](evidence/commands.md).
- Xử lý/đề xuất: Handle escaped JSON string syntax safely (e.g. parse/redact/re-serialize valid JSON or use escape-aware matcher); test escaped quotes/backslashes and ensure no suffix remains.

### C06 — Tài liệu và bản nhìn

- Nguồn/tiêu chí: [RULES §5 C06](../../../RULES.md#5-kiểm-tra-chung-cho-mọi-phase), [master-plan Phase 11](../../../../master-plan.md#phase-11--hệ-thống-công-cụ-thực-thi).
- Bắt buộc: Có.
- Điều kiện/môi trường: Tài liệu hiện hành; không chỉnh roadmap.
- Bước/lệnh: Đối chiếu roadmap/checklist/remake, không render vì không có doc-source change.
- Kỳ vọng: Không đổi phase status; ghi chính xác scope và missing evidence.
- Thực tế: Phase 11 vẫn “Chưa triển khai”; roadmap không bị chỉnh; report giữ các blockers runtime/dependency.
- Kết quả phản biện: none.
- Tag: clean.
- Kết quả: pass.
- Mức độ: info.
- Evidence: [roadmap](../../../../master-plan.md#phase-11--hệ-thống-công-cụ-thực-thi), [remake](../../../../remakes/phase-11/20261015T085118+0700-r002-remake/remake.md).
- Xử lý/đề xuất: Không có thay đổi tài liệu cần render.

### C07 — Regression liên quan

- Nguồn/tiêu chí: [RULES §5 C07](../../../RULES.md#5-kiểm-tra-chung-cho-mọi-phase); Phase 11 tools and shared redaction module.
- Bắt buộc: Có.
- Điều kiện/môi trường: Focused unit suite dùng fixtures; không DB.
- Bước/lệnh: `rtk proxy uv run --project apps/api pytest apps/api/tests/test_phase11_tools.py apps/api/tests/test_sensitive_validation.py -q`.
- Kỳ vọng: Current focused tests pass; warning được ghi rõ.
- Thực tế: 25 passed, 1 StarletteDeprecationWarning từ `httpx`/`starlette.testclient`, 0.99s. Suite không có escaped-quote canary case; custom probe đã phát hiện gap đó.
- Kết quả phản biện: none.
- Tag: clean.
- Kết quả: pass.
- Mức độ: info.
- Evidence: [commands](evidence/commands.md).
- Xử lý/đề xuất: Thêm case escaped JSON string sau khi xử lý finding.

### C08 — Có thể tái kiểm định

- Nguồn/tiêu chí: [RULES §5 C08](../../../RULES.md#5-kiểm-tra-chung-cho-mọi-phase), [RULES §7](../../../RULES.md#7-quy-ước-tên-thư-mục-file-và-liên-kết-vòng).
- Bắt buộc: Có.
- Điều kiện/môi trường: Batch r003 files, source hashes, links.
- Bước/lệnh: Kiểm đủ IDs/tags, manifest, links và commands.
- Kỳ vọng: Tái chạy canary, nhận diện chính xác source snapshot và blockers.
- Thực tế: Có 15 case records, manifest, synthetic probe, commands và cleanup; không lưu real secrets.
- Kết quả phản biện: none.
- Tag: clean.
- Kết quả: pass.
- Mức độ: info.
- Evidence: [manifest](evidence/source-manifest.json), [commands](evidence/commands.md).
- Xử lý/đề xuất: Không có.

### P11-01 — Tool schema/capability

- Nguồn/tiêu chí: [checklist](../../../phases/phase-11.md#ca-kiểm-định-riêng-của-phase), [spec permissions](../../../../product-spec.md#10-quyền-auth-và-inference-gates).
- Bắt buộc: Có.
- Điều kiện/môi trường: Validator unit tests; không dispatch.
- Bước/lệnh: Focused pytest run.
- Kỳ vọng: Invalid schema/version/tool/capability/actor deny trước executor.
- Thực tế: Negative validator unit cases pass; production policy caller, actor/scope integration và executor chưa có.
- Kết quả phản biện: none.
- Tag: need-change.
- Kết quả: blocked.
- Mức độ: major.
- Evidence: [commands](evidence/commands.md), [manifest](evidence/source-manifest.json).
- Xử lý/đề xuất: Cần executor/policy integration rồi kiểm bypass.

### P11-02 — File escape

- Nguồn/tiêu chí: [checklist](../../../phases/phase-11.md#ca-kiểm-định-riêng-của-phase), spec workspace/artifact boundary.
- Bắt buộc: Có.
- Điều kiện/môi trường: `tmp_path` fixture tests.
- Bước/lệnh: Focused pytest covers traversal, absolute path, symlink, output cap.
- Kỳ vọng: Deny outside-root access in actual executor/artifact boundary.
- Thực tế: Local reader negative tests pass; OS sandbox, artifact API, task-root authority, write path remain unimplemented.
- Kết quả phản biện: none.
- Tag: need-change.
- Kết quả: blocked.
- Mức độ: major.
- Evidence: [commands](evidence/commands.md), [manifest](evidence/source-manifest.json).
- Xử lý/đề xuất: Verify full path boundary in sandbox after integration.

### P11-03 — Network/terminal boundary

- Nguồn/tiêu chí: [checklist](../../../phases/phase-11.md#ca-kiểm-định-riêng-của-phase), Phase 11 roadmap scope.
- Bắt buộc: Có.
- Điều kiện/môi trường: No network/terminal test.
- Bước/lệnh: Registry and source review.
- Kỳ vọng: Egress allowlist, command scope, timeout/output limits are enforced.
- Thực tế: Only read_file exists; no terminal/network/browser executor or sandbox.
- Kết quả phản biện: none.
- Tag: need-change.
- Kết quả: blocked.
- Mức độ: major.
- Evidence: [manifest](evidence/source-manifest.json), [commands](evidence/commands.md).
- Xử lý/đề xuất: Implement and verify sandbox controls later; do not disable sandbox.

### P11-04 — Approval/receipt/idempotency

- Nguồn/tiêu chí: [checklist](../../../phases/phase-11.md#ca-kiểm-định-riêng-của-phase), [spec ToolAction/Receipt](../../../../product-spec.md#7-mô-hình-dữ-liệu-logic-và-các-bất-biến).
- Bắt buộc: Có.
- Điều kiện/môi trường: No side-effect actions.
- Bước/lệnh: Compare source call sites and Phase 09/10 status.
- Kỳ vọng: Approved prepared action, receipt/idempotency, unknown outcome not retried.
- Thực tế: Approval still not integrated with executor; Phase 09 lease/retry/recovery missing; no tool action lifecycle.
- Kết quả phản biện: none.
- Tag: need-change.
- Kết quả: blocked.
- Mức độ: major.
- Evidence: [roadmap](../../../../master-plan.md#phase-11--hệ-thống-công-cụ-thực-thi), [commands](evidence/commands.md).
- Xử lý/đề xuất: Verify after dependencies land; unknown must stay blocked.

### P11-05 — Run code thật trong sandbox

- Nguồn/tiêu chí: [checklist](../../../phases/phase-11.md#ca-kiểm-định-riêng-của-phase), demo/AC2.
- Bắt buộc: Có.
- Điều kiện/môi trường: No grant; no sandbox runtime.
- Bước/lệnh: Static source inventory.
- Kỳ vọng: Real code run, diff/test exit/artifact, linked trace.
- Thực tế: No write/code/terminal/browser/network/artifact path; grant=0. No mock substituted.
- Kết quả phản biện: none.
- Tag: need-change.
- Kết quả: blocked.
- Mức độ: major.
- Evidence: [manifest](evidence/source-manifest.json), [roadmap](../../../../master-plan.md#phase-11--hệ-thống-công-cụ-thực-thi).
- Xử lý/đề xuất: Requires isolated sandbox and explicit batch grant after dependencies.

### P11-06 — Redaction/correlation

- Nguồn/tiêu chí: [checklist](../../../phases/phase-11.md#ca-kiểm-định-riêng-của-phase), [spec redaction/correlation](../../../../product-spec.md#9-event-contract-v1-và-replay).
- Bắt buộc: Có.
- Điều kiện/môi trường: Synthetic canaries through file adapter; no runtime logs/Inspector.
- Bước/lệnh: Focused pytest and [full synthetic probe](evidence/P11-06-canary-check.py).
- Kỳ vọng: Full prior header/cookie/JSON/PEM matrix plus escaped quotes/backslashes are redacted; hash and byte_count match redacted content; end-to-end correlation preserved.
- Thực tế: All prior plain matrix cases and JSON `token`/`authorization` are now removed. Escaped JSON `token` value `before "quoted" backslash \\ json-escaped-token-canary` leaks its trailing `json-escaped-token-canary` segment. SHA-256 is present and matches returned filtered content; byte_count matches returned filtered content (451 bytes). No run/event correlation ID exists to verify.
- Kết quả phản biện: none.
- Tag: need-change.
- Kết quả: fail.
- Mức độ: major.
- Evidence: [probe script](evidence/P11-06-canary-check.py), [commands](evidence/commands.md).
- Xử lý/đề xuất: Make JSON string handling escape-aware or parse/redact valid JSON; add quoted/backslash regression and assert no canary suffix remains.

### P11-07 — Replay và external denial

- Nguồn/tiêu chí: [checklist](../../../phases/phase-11.md#ca-kiểm-định-riêng-của-phase), [spec replay/external authority](../../../../product-spec.md#9-event-contract-v1-và-replay).
- Bắt buộc: Có.
- Điều kiện/môi trường: No replay/external call.
- Bước/lệnh: Source call-site search.
- Kỳ vọng: Replay is read-only; external send/deploy denied without authorization.
- Thực tế: No replay/external connector or dispatch counter exists in Phase 11 integration.
- Kết quả phản biện: none.
- Tag: need-change.
- Kết quả: blocked.
- Mức độ: major.
- Evidence: [commands](evidence/commands.md), [manifest](evidence/source-manifest.json).
- Xử lý/đề xuất: Test with counters/direct attempts once implementation exists.

## Integration / release gates

| Gate áp dụng | Verdict | Test IDs | Evidence |
| --- | --- | --- | --- |
| Phase 11 không có IG riêng | Không áp dụng | C01–C08, P11-01…07 | Checklist xác nhận; các criteria phase vẫn bắt buộc. |

## Cleanup, giới hạn và bàn giao

- Cleanup: Synthetic probe dùng `TemporaryDirectory`; pytest chỉ dùng isolated temporary fixtures.
- Finding cần sửa: C05/P11-06 — escaped quote trong JSON secret string khiến regex chỉ che prefix; suffix token canary vẫn tới reader output.
- Blockers: C03/C04, P11-01…05/P11-07 do Phase 10 approval chưa tích hợp, Phase 09 worker retry/recovery chưa đạt, chưa có sandbox/terminal/network/write/artifact/replay runtime và inference grant=0. P11-06 end-to-end correlation cũng chưa chạy.
- Kết luận kỹ thuật: **cần sửa** — 5 clean, 2 fail, 8 blocked. Không nghiệm thu phase; không sửa master-plan.
- Bước tiếp theo: Remake escape-aware JSON redaction + regression fixture; independent r004 retest sau khi source mới có.
