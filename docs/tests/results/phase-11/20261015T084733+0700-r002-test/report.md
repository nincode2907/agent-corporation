# Kiểm định Phase 11 — 20261015T084733+0700-r002-test

## Thông tin batch

- Phase: 11
- Test batch: `20261015T084733+0700-r002-test`
- Vòng: r002
- Bắt đầu / kết thúc: 2026-10-15 08:47:33–08:50:32 +07:00 (Asia/Ho_Chi_Minh)
- Người/AI kiểm định: `/root/phase11_independent_test`, độc lập với AI remake `/root`
- Yêu cầu/phạm vi: kiểm định lại remake r001, đặc biệt redaction canaries được chỉ định; chạy safe focused regression; không sửa source/master-plan, không DB/runtime dispatch/inference/gateway.
- Source: không có commit xác định cho worktree; [source-manifest.json](evidence/source-manifest.json) chứa hashes SHA-256 của module/test snapshot. `redaction.py` là tracked modified file; tools/tests là untracked.
- Môi trường: macOS; Python 3.14.8; pytest 9.0.2; uv project `apps/api`.
- Inference: không gọi; grant hiện hành = 0.
- Dependency/quyết định: [Phase 11 roadmap](../../../../master-plan.md#phase-11--hệ-thống-công-cụ-thực-thi), [checklist](../../../phases/phase-11.md), [spec](../../../../product-spec.md), [ADR-0001](../../../../decisions/0001-v1-foundation.md). Phase 10 approval chưa tích hợp executor; Phase 09 lease/recovery/retry chưa hoàn tất.
- Supersedes: [r001 report](../20261015T084213+0700-r001-test/report.md).
- Remake nguồn: [r001 remake](../../../../remakes/phase-11/20261015T084559+0700-r001-remake/remake.md).
- Kết luận kỹ thuật: **cần sửa** — JSON `token` và `authorization` field values vẫn lộ khỏi file reader; các acceptance criteria khác còn blocked.
- Quyết định Chủ tịch: Chưa có.

## Mapping và phạm vi kiểm định

| Tiêu chí / nguồn | Test IDs | Bắt buộc | Ghi chú |
| --- | --- | --- | --- |
| C01–C08 — [RULES §5](../../../RULES.md#5-kiểm-tra-chung-cho-mọi-phase) | C01–C08 | Có | Kết quả riêng bên dưới. |
| AC1: file/secret ngoài workspace, network/tool ngoài allowlist deny ở executor | P11-01, P11-02, P11-03 | Có | Unit test reader/validator chạy được; chưa có executor integration. |
| AC2: run thật, diff/test exit/artifact, redaction giữ correlation | P11-05, P11-06 | Có | Adapter canary đã kiểm tra; run thật/correlation event vẫn chưa có. |
| AC3: retry không lặp side effect khi outcome unknown | P11-04, P11-07 | Có | Approval chưa nối executor; worker/retry dependency còn thiếu. |
| Demo: sửa file/test/read trang allowlist trong sandbox, deny traversal/command ngoài scope | C03, P11-02, P11-03, P11-05 | Có | Không có sandbox runtime; demo blocked. |

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

- Nguồn/tiêu chí: [RULES §5](../../../RULES.md#5-kiểm-tra-chung-cho-mọi-phase), yêu cầu retest r002.
- Bắt buộc: Có.
- Điều kiện/môi trường: Dirty worktree; implementation/remake đang được kiểm định.
- Bước/lệnh: `rtk git status --short`; hash source qua lệnh trong [commands](evidence/commands.md).
- Kỳ vọng: Thay đổi chỉ thuộc remediation Phase 11; tester không sửa product source.
- Thực tế: Diff code gồm redaction module và Phase 11 tools/test files; ngoài ra có artifacts remake/test. Không có master-plan/product source change trong scope làm việc này.
- Kết quả phản biện: none.
- Tag: clean.
- Kết quả: pass.
- Mức độ: info.
- Evidence: [manifest](evidence/source-manifest.json), [commands](evidence/commands.md).
- Xử lý/đề xuất: Không có.

### C02 — Dependency và nguồn quyết định

- Nguồn/tiêu chí: [roadmap Phase 10–11](../../../../master-plan.md#phase-11--hệ-thống-công-cụ-thực-thi), [spec ToolAction/Receipt](../../../../product-spec.md#7-mô-hình-dữ-liệu-logic-và-các-bất-biến), [ADR D06](../../../../decisions/0001-v1-foundation.md).
- Bắt buộc: Có.
- Điều kiện/môi trường: So sánh nguồn hiện tại với report r001/remake.
- Bước/lệnh: Đọc block Phase 11/dependency và spec contracts.
- Kỳ vọng: Không nâng phase status hoặc đánh giá executor complete khi chưa tích hợp.
- Thực tế: Roadmap vẫn ghi Phase 11 “Chưa triển khai”; Phase 10 approval chưa tích hợp executor; Phase 09 lease/retry/recovery còn thiếu. Remake đúng scope khi chỉ sửa redaction reader/test.
- Kết quả phản biện: none.
- Tag: clean.
- Kết quả: pass.
- Mức độ: info.
- Evidence: [roadmap](../../../../master-plan.md#phase-11--hệ-thống-công-cụ-thực-thi), [remake](../../../../remakes/phase-11/20261015T084559+0700-r001-remake/remake.md).
- Xử lý/đề xuất: Giữ dependency/blocker như hiện tại.

### C03 — Đủ criteria và demo

- Nguồn/tiêu chí: [RULES §5 C03](../../../RULES.md#5-kiểm-tra-chung-cho-mọi-phase), [demo Phase 11](../../../../master-plan.md#phase-11--hệ-thống-công-cụ-thực-thi), [checklist](../../../phases/phase-11.md).
- Bắt buộc: Có.
- Điều kiện/môi trường: Không có sandbox app/runtime.
- Bước/lệnh: Mapping AC1–3 và demo theo checklist.
- Kỳ vọng: Demo thật sửa file, chạy test, đọc trang allowlist, có artifact/log và negative cases.
- Thực tế: Chỉ có read-only local adapter; không có sandbox executor, write/terminal/network/browser/artifact pipeline hay runtime demo.
- Kết quả phản biện: none.
- Tag: need-change.
- Kết quả: blocked.
- Mức độ: major.
- Evidence: [manifest](evidence/source-manifest.json), [commands](evidence/commands.md).
- Xử lý/đề xuất: Cần executor/sandbox và dependency Phase 09–10 đạt trước demo.

### C04 — Không thực thi âm thầm

- Nguồn/tiêu chí: [RULES §5 C04](../../../RULES.md#5-kiểm-tra-chung-cho-mọi-phase), [spec replay](../../../../product-spec.md#9-event-contract-v1-và-replay).
- Bắt buộc: Có.
- Điều kiện/môi trường: Static trace; không khởi động worker/API.
- Bước/lệnh: `rtk rg -n 'validate_proposal|execute_read_file|WorkspaceReader|list_tools' apps/api/src apps/api/tests/test_phase11_tools.py`.
- Kỳ vọng: Không có page/health/seed/replay dispatch trái scope.
- Thực tế: Call sites production của tools vẫn nằm trong module mới; không thấy endpoint/executor integration. Static search không chứng minh runtime dispatch ở app chưa tích hợp.
- Kết quả phản biện: none.
- Tag: need-change.
- Kết quả: blocked.
- Mức độ: major.
- Evidence: [commands](evidence/commands.md).
- Xử lý/đề xuất: Khi dispatch path có thật, kiểm bằng counter/spy/network evidence.

### C05 — Scope và dữ liệu nhạy cảm

- Nguồn/tiêu chí: [RULES §5 C05](../../../RULES.md#5-kiểm-tra-chung-cho-mọi-phase), [spec redaction](../../../../product-spec.md#9-event-contract-v1-và-replay), [P11-06](../../../phases/phase-11.md).
- Bắt buộc: Có.
- Điều kiện/môi trường: Synthetic canaries duy nhất, qua `WorkspaceReader`/`execute_read_file`.
- Bước/lệnh: Chạy [canary probe](evidence/P11-06-canary-check.py).
- Kỳ vọng: Credential fields bị che trước khi reader trả content; hash/byte_count giữ đúng giá trị trên output đã lọc.
- Thực tế: JSON `token` và `authorization` values còn nguyên. `sha256` có đủ 64 ký tự, khớp SHA-256 output đã redacted; `byte_count` khớp số byte output. Các canary còn lại trong danh sách kiểm tra không xuất hiện.
- Kết quả phản biện: none.
- Tag: need-change.
- Kết quả: fail.
- Mức độ: major.
- Evidence: [canary script](evidence/P11-06-canary-check.py), [commands/output](evidence/commands.md).
- Xử lý/đề xuất: Mở rộng reader text redaction cho JSON `token` và `authorization` field names (hoặc parse/redact JSON với fallback an toàn), thêm regression xác nhận field values không lộ.

### C06 — Tài liệu và bản nhìn

- Nguồn/tiêu chí: [RULES §5 C06](../../../RULES.md#5-kiểm-tra-chung-cho-mọi-phase), [master-plan Phase 11](../../../../master-plan.md#phase-11--hệ-thống-công-cụ-thực-thi).
- Bắt buộc: Có.
- Điều kiện/môi trường: Review tài liệu; không sửa roadmap.
- Bước/lệnh: Đối chiếu master-plan, checklist và remake.
- Kỳ vọng: Trạng thái phase không đổi; report mô tả đúng scope/evidence.
- Thực tế: Master-plan vẫn “Chưa triển khai”; không cập nhật/render roadmap. Remake/report nêu đúng blocker/runtime gaps.
- Kết quả phản biện: none.
- Tag: clean.
- Kết quả: pass.
- Mức độ: info.
- Evidence: [roadmap](../../../../master-plan.md#phase-11--hệ-thống-công-cụ-thực-thi), [remake](../../../../remakes/phase-11/20261015T084559+0700-r001-remake/remake.md).
- Xử lý/đề xuất: Không có thay đổi tài liệu cần đồng bộ.

### C07 — Regression liên quan

- Nguồn/tiêu chí: [RULES §5 C07](../../../RULES.md#5-kiểm-tra-chung-cho-mọi-phase); tools reader imports shared redaction module.
- Bắt buộc: Có.
- Điều kiện/môi trường: API unit tests cô lập; không DB.
- Bước/lệnh: `rtk proxy uv run --project apps/api pytest apps/api/tests/test_phase11_tools.py apps/api/tests/test_sensitive_validation.py -q`.
- Kỳ vọng: Focused tool + shared redaction regression pass; warning không bị che.
- Thực tế: 24 passed, 1 StarletteDeprecationWarning (`httpx`/`starlette.testclient`) in 1.01s. Unit pass không phát hiện JSON token/authorization leakage do các labels chưa có test riêng.
- Kết quả phản biện: none.
- Tag: clean.
- Kết quả: pass.
- Mức độ: info.
- Evidence: [commands](evidence/commands.md).
- Xử lý/đề xuất: Bổ sung hai field names bị thiếu vào redaction unit tests khi sửa finding.

### C08 — Có thể tái kiểm định

- Nguồn/tiêu chí: [RULES §5 C08](../../../RULES.md#5-kiểm-tra-chung-cho-mọi-phase), [RULES §7](../../../RULES.md#7-quy-ước-tên-thư-mục-file-và-liên-kết-vòng).
- Bắt buộc: Có.
- Điều kiện/môi trường: Report/evidence snapshot mới.
- Bước/lệnh: Kiểm tra hash manifest, tất cả IDs, links và lệnh/evidence.
- Kỳ vọng: C01–C08/P11-01…07 đủ record; source/config, expected/actual, cleanup, links tồn tại.
- Thực tế: Batch chứa đủ 15 IDs, hashes và canary script; command output ghi pass/fail chính xác; không lưu giá trị secret thật.
- Kết quả phản biện: none.
- Tag: clean.
- Kết quả: pass.
- Mức độ: info.
- Evidence: [manifest](evidence/source-manifest.json), [commands](evidence/commands.md).
- Xử lý/đề xuất: Không có.

### P11-01 — Tool schema/capability

- Nguồn/tiêu chí: [Phase 11 checklist](../../../phases/phase-11.md#ca-kiểm-định-riêng-của-phase), [spec permissions](../../../../product-spec.md#10-quyền-auth-và-inference-gates).
- Bắt buộc: Có.
- Điều kiện/môi trường: Focused unit tests, chưa có executor.
- Bước/lệnh: Chạy test module tools.
- Kỳ vọng: Invalid args/schema/version, tool chưa allowlist/actor ngoài scope deny trước executor.
- Thực tế: Unit validator negative cases pass; trusted server policy caller, actor scope check và executor dispatch chưa được nối.
- Kết quả phản biện: none.
- Tag: need-change.
- Kết quả: blocked.
- Mức độ: major.
- Evidence: [commands](evidence/commands.md), [manifest](evidence/source-manifest.json).
- Xử lý/đề xuất: Tích hợp và kiểm backend/executor bypass sau khi Phase 10 approval sẵn sàng.

### P11-02 — File escape

- Nguồn/tiêu chí: [Phase 11 checklist](../../../phases/phase-11.md#ca-kiểm-định-riêng-của-phase), spec workspace/artifact boundary.
- Bắt buộc: Có.
- Điều kiện/môi trường: tmp_path unit tests; không workspace production data.
- Bước/lệnh: Focused tests về traversal, absolute path, symlink, output cap.
- Kỳ vọng: Không thể truy cập ngoài task root tại executor/artifact boundary.
- Thực tế: Unit reader deny traversal/symlink và cap; chưa có OS sandbox, file-write, artifact API hoặc task-root assignment integration để chứng minh AC rộng.
- Kết quả phản biện: none.
- Tag: need-change.
- Kết quả: blocked.
- Mức độ: major.
- Evidence: [commands](evidence/commands.md), [manifest](evidence/source-manifest.json).
- Xử lý/đề xuất: Kiểm full boundary trên sandbox thật; giữ scope hiện tại fail closed.

### P11-03 — Network/terminal boundary

- Nguồn/tiêu chí: [Phase 11 checklist](../../../phases/phase-11.md#ca-kiểm-định-riêng-của-phase), roadmap Phase 11.
- Bắt buộc: Có.
- Điều kiện/môi trường: Không chạy tool/network.
- Bước/lệnh: Registry/source review.
- Kỳ vọng: Egress allowlist, command scope, timeout/output limits có enforcement thật.
- Thực tế: Chỉ có read-file adapter; không có terminal/browser/network executor hoặc OS sandbox. `max_bytes` hiện giới hạn read-file response.
- Kết quả phản biện: none.
- Tag: need-change.
- Kết quả: blocked.
- Mức độ: major.
- Evidence: [manifest](evidence/source-manifest.json), [commands](evidence/commands.md).
- Xử lý/đề xuất: Chờ sandbox và dependencies; kiểm allowlist/deny/timeout/output tại executor.

### P11-04 — Approval/receipt/idempotency

- Nguồn/tiêu chí: [Phase 11 checklist](../../../phases/phase-11.md#ca-kiểm-định-riêng-của-phase), [spec ToolAction/Receipt](../../../../product-spec.md#7-mô-hình-dữ-liệu-logic-và-các-bất-biến).
- Bắt buộc: Có.
- Điều kiện/môi trường: Không tạo side effect.
- Bước/lệnh: Đối chiếu roadmap Phase 10/09 và tool registry/source.
- Kỳ vọng: Approval prepared/consumed đúng payload; receipt/idempotency; unknown không retry.
- Thực tế: Phase 10 approvals chưa tích hợp executor; Phase 09 lease/retry/recovery còn thiếu. Reader là tool read-only, chưa có receipt/action lifecycle.
- Kết quả phản biện: none.
- Tag: need-change.
- Kết quả: blocked.
- Mức độ: major.
- Evidence: [roadmap](../../../../master-plan.md#phase-11--hệ-thống-công-cụ-thực-thi), [remake](../../../../remakes/phase-11/20261015T084559+0700-r001-remake/remake.md).
- Xử lý/đề xuất: Chạy khi approvals, worker recovery/retry và executor tích hợp; unknown outcome không dispatch lại.

### P11-05 — Run code thật trong sandbox

- Nguồn/tiêu chí: [Phase 11 checklist](../../../phases/phase-11.md#ca-kiểm-định-riêng-của-phase), demo/AC2 roadmap.
- Bắt buộc: Có.
- Điều kiện/môi trường: Inference grant = 0; sandbox runtime không có.
- Bước/lệnh: Source inventory; không thực thi.
- Kỳ vọng: Real sandbox run có file diff, test exit, artifact manifest và trace.
- Thực tế: Chưa có write/code/terminal/browser/network, artifact/diff/test-result path; không có grant. Không thay bằng mock.
- Kết quả phản biện: none.
- Tag: need-change.
- Kết quả: blocked.
- Mức độ: major.
- Evidence: [manifest](evidence/source-manifest.json), [roadmap](../../../../master-plan.md#phase-11--hệ-thống-công-cụ-thực-thi).
- Xử lý/đề xuất: Cần sandbox/capabilities và grant mới đúng test batch trước real run.

### P11-06 — Redaction/correlation

- Nguồn/tiêu chí: [Phase 11 checklist](../../../phases/phase-11.md#ca-kiểm-định-riêng-của-phase), [spec event redaction/correlation](../../../../product-spec.md#9-event-contract-v1-và-replay).
- Bắt buộc: Có.
- Điều kiện/môi trường: Synthetic canaries; probe qua actual `execute_read_file`; no runtime logs/Inspector.
- Bước/lệnh: Focused pytest + [canary script](evidence/P11-06-canary-check.py).
- Kỳ vọng: Basic/Bearer Authorization, Proxy-Authorization, Cookie/Set-Cookie, JSON credentials, private-key blocks đều redacted; output trả `sha256`/`byte_count` đúng trên redacted content; correlation end-to-end giữ nguyên.
- Thực tế: Header/cookie variants, JSON password/api_key/credential/access_token/secret/private_key và PEM private key đã che trong probe; JSON `token` và `authorization` còn lộ. `sha256` hiện diện và khớp output đã redacted; `byte_count` hiện diện và đúng. Correlation chỉ chứng minh metadata file hash/size; chưa có run/event/log correlation ID integration.
- Kết quả phản biện: none.
- Tag: need-change.
- Kết quả: fail.
- Mức độ: major.
- Evidence: [canary script](evidence/P11-06-canary-check.py), [commands/output](evidence/commands.md).
- Xử lý/đề xuất: Thêm JSON field handling cho `token`/`authorization` cùng regression; sau đó retest canaries. Chưa đóng P11-06 đến khi các formats pass và end-to-end trace có thể chạy.

### P11-07 — Replay và external denial

- Nguồn/tiêu chí: [Phase 11 checklist](../../../phases/phase-11.md#ca-kiểm-định-riêng-của-phase), [spec replay/external authority](../../../../product-spec.md#9-event-contract-v1-và-replay).
- Bắt buộc: Có.
- Điều kiện/môi trường: Không gọi external connector/replay.
- Bước/lệnh: Source call-site search và registry review.
- Kỳ vọng: Replay chỉ đọc; external send/deploy deny và không side effect.
- Thực tế: Chưa có replay tool trace, external connectors hoặc dispatch counter. Không thể tạo runtime negative proof.
- Kết quả phản biện: none.
- Tag: need-change.
- Kết quả: blocked.
- Mức độ: major.
- Evidence: [commands](evidence/commands.md), [manifest](evidence/source-manifest.json).
- Xử lý/đề xuất: Kiểm bằng dispatch counters/direct attempts khi các đường này tồn tại; không thêm connector trong batch này.

## Integration / release gates

| Gate áp dụng | Verdict | Test IDs | Evidence |
| --- | --- | --- | --- |
| Không có IG riêng Phase 11 | Không áp dụng | C01–C08, P11-01…07 | Checklist ghi rõ không có gate riêng; blockers vẫn áp dụng. |

## Cleanup, giới hạn và bàn giao

- Cleanup: Python probe dùng `TemporaryDirectory`, tự xóa; pytest chỉ dùng `tmp_path`. Không DB/runtime/external resources.
- Cần sửa: C05/P11-06 còn fail: JSON `token`/`authorization` values thoát tới tool response. Đã thông báo điều phối trước khi kết thúc report.
- Blockers: C03/C04, P11-01…05/P11-07 chưa chứng minh do Phase 10 approval/executor và Phase 09 lease/retry/recovery còn thiếu; chưa có OS sandbox/network/terminal/file-write/artifact/replay; inference grant = 0. P11-06 correlation end-to-end cũng còn blocked dù redaction unit/probe đã kiểm metadata local.
- Kết luận kỹ thuật: **cần sửa**; 5 clean, 2 fail, 8 blocked. Không nghiệm thu Phase 11, không đổi master-plan.
- Bước tiếp theo: Remake JSON `token`/`authorization` redaction và thêm regression test; chạy independent r003 cho source mới. Các test integration còn lại chỉ thực hiện khi điều kiện/grant riêng sẵn sàng.
