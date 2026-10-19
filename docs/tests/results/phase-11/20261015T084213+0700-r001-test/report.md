# Kiểm định Phase 11 — 20261015T084213+0700-r001-test

## Thông tin batch

- Phase: 11
- Test batch: `20261015T084213+0700-r001-test`
- Vòng: r001
- Bắt đầu / kết thúc: 2026-10-15 08:42:13–08:45:08 +07:00 (Asia/Ho_Chi_Minh)
- Người/AI kiểm định: `/root/phase11_independent_test`, độc lập với AI triển khai/remake `/root`
- Yêu cầu/phạm vi: chỉ kiểm định source dirty hiện tại theo giao việc điều phối; không sửa product source; không DB mutation, runtime dispatch, inference hay gateway; không cập nhật roadmap/render.
- Source: worktree không có commit xác định cho các file mới; các file Phase 11 dưới đây là untracked. Hash/SHA-256: [source-manifest.json](evidence/source-manifest.json). Không có tracked diff trong `git status` tại lúc kiểm tra.
- Môi trường: macOS; Python 3.14.8; pytest 9.0.2; uv project `apps/api`; source hiện tại sau chỉnh sửa fail-closed `O_NOFOLLOW` và phân loại `errno.ELOOP`.
- Inference: không gọi; grant hiện hành = 0.
- Dependency/quyết định: [Phase 11 roadmap](../../../../master-plan.md#phase-11--hệ-thống-công-cụ-thực-thi), [Phase 11 checklist](../../../phases/phase-11.md), [spec](../../../../product-spec.md), [ADR-0001](../../../../decisions/0001-v1-foundation.md). Phase 10 approval chưa tích hợp executor; Phase 09 lease/retry/recovery còn thiếu. Đây là dependency/status được roadmap ghi rõ, không coi phần tĩnh ở Phase 11 là executor hoàn tất.
- Supersedes: Không có.
- Remake nguồn: Không có ở vòng đầu.
- Kết luận kỹ thuật: **cần sửa** (redaction canary fail); ngoài ra còn các tiêu chí bắt buộc blocked do chưa có executor/sandbox và dependency.
- Quyết định Chủ tịch: Chưa có.

## Mapping và phạm vi kiểm định

| Tiêu chí hiện tại / nguồn | Test IDs | Bắt buộc | Ghi chú |
| --- | --- | --- | --- |
| C01–C08 của [RULES](../../../RULES.md#5-kiểm-tra-chung-cho-mọi-phase) | C01–C08 | Có | Mỗi mục có kết quả riêng bên dưới. |
| AC1: deny file/secret outside workspace; network/tool outside allowlist denied in executor | P11-01, P11-02, P11-03 | Có | Chỉ registry validator và reader cục bộ tồn tại; không thấy executor integration. |
| AC2: real run provides diff, test exit code, artifact; redaction retains correlation | P11-05, P11-06 | Có | Chưa có run thật hoặc artifact/diff pipeline; redaction bug được tái hiện với canary giả. |
| AC3: retry does not repeat side effect with unknown outcome | P11-04, P11-07 | Có | Approval Phase 10 chưa tích hợp executor; Phase 09 retry/recovery chưa hoàn tất. |
| Demo: edit in sandbox, run test, read allowlisted page; traversal/command outside scope denied | C03, P11-02, P11-03, P11-05 | Có | Demo chưa thể chạy; không scaffold hoặc gọi tool để lấp dependency. |

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

- Nguồn/tiêu chí: [RULES §5](../../../RULES.md#5-kiểm-tra-chung-cho-mọi-phase), chỉ thị giao kiểm Phase 11.
- Bắt buộc: Có.
- Điều kiện/môi trường: `git status --short`; source manifest của 4 file Phase 11 mới.
- Bước/lệnh: `rtk git status --short`; `rtk proxy shasum -a 256 ...` (chi tiết [commands](evidence/commands.md)).
- Kỳ vọng: Chỉ đụng scope Phase 11, giữ nguyên các thay đổi khác, nhận diện dirty/untracked source chính xác.
- Thực tế: Hai cây file untracked là `modules/tools/` và `test_phase11_tools.py`; không thấy tracked diff. Phạm vi đúng với implementation đang được review.
- Kết quả phản biện: none.
- Tag: clean.
- Kết quả: pass.
- Mức độ: info.
- Evidence: [source manifest](evidence/source-manifest.json).
- Xử lý/đề xuất: Không có.

### C02 — Dependency và nguồn quyết định

- Nguồn/tiêu chí: [roadmap Phase 10–11](../../../../master-plan.md#phase-11--hệ-thống-công-cụ-thực-thi), [spec ToolAction/Receipt và approval](../../../../product-spec.md#7-mô-hình-dữ-liệu-logic-và-các-bất-biến), [ADR-0001 D06](../../../../decisions/0001-v1-foundation.md).
- Bắt buộc: Có.
- Điều kiện/môi trường: Đối chiếu source docs hiện hành, không dựa checkbox cá nhân.
- Bước/lệnh: Đọc roadmap, spec, ADR, checklist và executor/approval call sites trong source.
- Kỳ vọng: Nêu chính xác dependency/gate và không gán nhãn hoàn tất khi thiếu tích hợp.
- Thực tế: Roadmap ghi Phase 10 đang triển khai, approval API chưa dispatch; Phase 09 thiếu lease/recovery/retry. Phase 11 vẫn “Chưa triển khai” ở nguồn chuẩn. Module hiện tại tự mô tả là validator và reader cho future isolated executor.
- Kết quả phản biện: none.
- Tag: clean.
- Kết quả: pass.
- Mức độ: info.
- Evidence: [roadmap/spec mapping](../../../../master-plan.md#phase-11--hệ-thống-công-cụ-thực-thi), [manifest](evidence/source-manifest.json).
- Xử lý/đề xuất: Giữ dependency làm blocker; không gộp Phase 10/09 vào review này.

### C03 — Đủ criteria và demo

- Nguồn/tiêu chí: [RULES §5 C03](../../../RULES.md#5-kiểm-tra-chung-cho-mọi-phase), [demo và acceptance Phase 11](../../../../master-plan.md#phase-11--hệ-thống-công-cụ-thực-thi), [checklist](../../../phases/phase-11.md).
- Bắt buộc: Có.
- Điều kiện/môi trường: Static review; không chạy runtime/tool.
- Bước/lệnh: Mapping AC1–AC3 và demo trong bảng phía trên.
- Kỳ vọng: Demo mở được, gồm edit/test/read thật trong sandbox và negative path traversal/command scope.
- Thực tế: Chưa có sandbox executor, terminal/browser/network, write, artifact/diff/test-exit capture. Demo bắt buộc chưa tồn tại. Local reader unit tests không thay demo.
- Kết quả phản biện: none.
- Tag: need-change.
- Kết quả: blocked.
- Mức độ: major.
- Evidence: [manifest](evidence/source-manifest.json), [commands](evidence/commands.md).
- Xử lý/đề xuất: Cần triển khai và kiểm chứng executor trong sandbox sau khi dependency Phase 09–10 đạt và các quyền riêng được cấp.

### C04 — Không thực thi âm thầm

- Nguồn/tiêu chí: [RULES §5 C04](../../../RULES.md#5-kiểm-tra-chung-cho-mọi-phase), [spec replay/tool flow](../../../../product-spec.md#9-event-contract-v1-và-replay).
- Bắt buộc: Có.
- Điều kiện/môi trường: Source trace, không khởi động API/worker.
- Bước/lệnh: `rtk rg -n 'validate_proposal|execute_read_file|WorkspaceReader|list_tools' apps/api/src apps/api/tests/test_phase11_tools.py`.
- Kỳ vọng: Không có mở trang/health/seed/replay nào dispatch model/tool ngoài quyền.
- Thực tế: Các symbol Phase 11 chỉ được dùng trong module mới và unit tests; không có production call site được tìm thấy. Điều này không chứng minh hành vi app/runtime không dispatch vì executor/API integration chưa có và không chạy runtime.
- Kết quả phản biện: none.
- Tag: need-change.
- Kết quả: blocked.
- Mức độ: major.
- Evidence: [commands](evidence/commands.md).
- Xử lý/đề xuất: Khi có đường dispatch, kiểm backend/executor với dispatch counter và chứng minh mở trang/health/replay không tăng counter.

### C05 — Scope và dữ liệu nhạy cảm

- Nguồn/tiêu chí: [RULES §5 C05](../../../RULES.md#5-kiểm-tra-chung-cho-mọi-phase), [spec redaction/secret policy](../../../../product-spec.md#9-event-contract-v1-và-replay), [Phase 11 P11-06](../../../phases/phase-11.md).
- Bắt buộc: Có.
- Điều kiện/môi trường: Chỉ dùng canary giả; không dùng secrets thật.
- Bước/lệnh: Rà `redact_text` và chạy repro synthetic Authorization/cookie; xem [evidence P11-06](evidence/P11-06-redaction.md).
- Kỳ vọng: Secret marker trong file output bị redacted trước khi tới agent/logs, correlation không mất.
- Thực tế: File reader gọi `redact_text`, nhưng mẫu text thiếu `authorization` và `cookie`; canary giả hai dạng này còn nguyên trong output. Đây là finding bảo mật code-verified; chưa có executor/log UI để xác định blast radius runtime.
- Kết quả phản biện: none.
- Tag: need-change.
- Kết quả: fail.
- Mức độ: major.
- Evidence: [redaction repro](evidence/P11-06-redaction.md), [commands](evidence/commands.md).
- Xử lý/đề xuất: Sửa redaction các định dạng credential cần hỗ trợ và thêm test canary dương tính/âm tính, rồi kiểm tra lại output ở các lớp lưu trữ/log/tool result.

### C06 — Tài liệu và bản nhìn

- Nguồn/tiêu chí: [RULES §5 C06](../../../RULES.md#5-kiểm-tra-chung-cho-mọi-phase), [roadmap Phase 11](../../../../master-plan.md#phase-11--hệ-thống-công-cụ-thực-thi), [checklist](../../../phases/phase-11.md).
- Bắt buộc: Có.
- Điều kiện/môi trường: Review tài liệu và link nguồn; không sửa tài liệu/roadmap trong batch.
- Bước/lệnh: Đối chiếu Markdown checklist với block Phase 11 ở master plan; xác nhận không cập nhật status/render.
- Kỳ vọng: Nguồn Markdown vẫn chuẩn; report không tự nâng trạng thái phase.
- Thực tế: AC/demo/dependency khớp. Phase 11 vẫn “Chưa triển khai”; không thay roadmap hoặc HTML. Không chạy validator/render vì batch chỉ ghi report evidence.
- Kết quả phản biện: none.
- Tag: clean.
- Kết quả: pass.
- Mức độ: info.
- Evidence: [mapping ở đầu report](#mapping-và-phạm-vi-kiểm-định), [manifest](evidence/source-manifest.json).
- Xử lý/đề xuất: Chưa có thay đổi tài liệu cần render.

### C07 — Regression liên quan

- Nguồn/tiêu chí: [RULES §5 C07](../../../RULES.md#5-kiểm-tra-chung-cho-mọi-phase), module registry/workspace và redaction được import.
- Bắt buộc: Có.
- Điều kiện/môi trường: Unit test cô lập dùng pytest `tmp_path`; không DB.
- Bước/lệnh: `rtk proxy uv run --project apps/api pytest apps/api/tests/test_phase11_tools.py`.
- Kỳ vọng: Test module hiện tại pass trên source sau thay đổi `O_NOFOLLOW`/`errno.ELOOP`.
- Thực tế: 15 passed; chạy hai lần trong phiên, lần cuối sau hardening source là 15 passed / 0.10s. Unit tests gồm schema/version/capability denial, traversal, absolute path, symlink escape/parent, output cap, binary/non-file và API key canary.
- Kết quả phản biện: none.
- Tag: clean.
- Kết quả: pass.
- Mức độ: info.
- Evidence: [commands](evidence/commands.md), [source manifest](evidence/source-manifest.json).
- Xử lý/đề xuất: Test pass không đóng các blocker executor/sandbox hay redaction formats chưa có test.

### C08 — Có thể tái kiểm định

- Nguồn/tiêu chí: [RULES §5 C08](../../../RULES.md#5-kiểm-tra-chung-cho-mọi-phase), [RULES §7](../../../RULES.md#7-quy-ước-tên-thư-mục-file-và-liên-kết-vòng).
- Bắt buộc: Có.
- Điều kiện/môi trường: Kiểm tra thủ công cấu trúc report/evidence và hash.
- Bước/lệnh: Kiểm tra C01–C08, P11-01…P11-07 mỗi ID có một tag/result; hash source trong manifest.
- Kỳ vọng: IDs đầy đủ, hash/commands/evidence liên kết được, trạng thái nói rõ.
- Thực tế: Report có đủ 15 ID, manifest hashes, commands, repro canary, expected/actual, result/tag/severity/action. Không giữ raw log chứa bí mật thật.
- Kết quả phản biện: none.
- Tag: clean.
- Kết quả: pass.
- Mức độ: info.
- Evidence: [source-manifest.json](evidence/source-manifest.json), [commands.md](evidence/commands.md).
- Xử lý/đề xuất: Không có.

### P11-01 — Tool schema/capability

- Nguồn/tiêu chí: [Phase 11 checklist](../../../phases/phase-11.md#ca-kiểm-định-riêng-của-phase), [spec quyền](../../../../product-spec.md#10-quyền-auth-và-inference-gates).
- Bắt buộc: Có.
- Điều kiện/môi trường: Unit validator tests; không executor dispatch.
- Bước/lệnh: Chạy focused pytest; xem test param invalid tool/version/capability/args.
- Kỳ vọng: Invalid schema/version, tool chưa allowlist, actor ngoài scope bị deny trước executor; proposal không trực tiếp chạy.
- Thực tế: Unit validator deny unknown `terminal.run`, version mismatch/bool, missing capability và extra args. Tuy nhiên trusted caller cấp `allowed_capabilities` chưa tồn tại; không có executor, actor/scope check hoặc policy/approval integration để chứng minh deny trước dispatch.
- Kết quả phản biện: none.
- Tag: need-change.
- Kết quả: blocked.
- Mức độ: major.
- Evidence: [test output/source hashes](evidence/commands.md), [manifest](evidence/source-manifest.json).
- Xử lý/đề xuất: Sau khi Phase 10 approval tích hợp executor, test direct/bypass path chứng minh capability do server policy cấp và backend deny trước dispatch.

### P11-02 — File escape

- Nguồn/tiêu chí: [Phase 11 checklist](../../../phases/phase-11.md#ca-kiểm-định-riêng-của-phase), [spec workspace/artifact boundaries](../../../../product-spec.md#7-mô-hình-dữ-liệu-logic-và-các-bất-biến).
- Bắt buộc: Có.
- Điều kiện/môi trường: Unit `tmp_path`, file giả và symlink trong test fixture.
- Bước/lệnh: Chạy focused pytest; tests thử traversal, absolute/Windows paths, symlink file/parent, output cap, binary và directory.
- Kỳ vọng: Không đọc/ghi ngoài root ở executor và artifact access, bao gồm secret canary.
- Thực tế: Read-only reader cục bộ từ chối traversal/symlink và kiểm tra regular file + output cap. Root do caller cung cấp; chưa có enforcement file allowlist/secret exclusion, artifact API hoặc OS sandbox. Không có file-write path để kiểm tra.
- Kết quả phản biện: none.
- Tag: need-change.
- Kết quả: blocked.
- Mức độ: major.
- Evidence: focused tests tại [commands](evidence/commands.md); [manifest](evidence/source-manifest.json).
- Xử lý/đề xuất: Kiểm chứng root cấp theo task, symlink/path race, secret policy, artifact access và write path bên trong môi trường sandbox thực.

### P11-03 — Network/terminal boundary

- Nguồn/tiêu chí: [Phase 11 checklist](../../../phases/phase-11.md#ca-kiểm-định-riêng-của-phase), [roadmap scope](../../../../master-plan.md#phase-11--hệ-thống-công-cụ-thực-thi).
- Bắt buộc: Có.
- Điều kiện/môi trường: Không chạy terminal/network tool.
- Bước/lệnh: Static source map; registry chỉ liệt kê `workspace.read_file`.
- Kỳ vọng: Egress ngoài allowlist/command ngoài scope bị chặn; timeout/output cap thực thi trong sandbox.
- Thực tế: Không có terminal, browser, network executor, timeout, process output cap hay sandbox code. Output cap hiện chỉ giới hạn byte cho file read adapter.
- Kết quả phản biện: none.
- Tag: need-change.
- Kết quả: blocked.
- Mức độ: major.
- Evidence: [source manifest](evidence/source-manifest.json), [commands](evidence/commands.md).
- Xử lý/đề xuất: Cần runtime sandbox/evidence cho egress deny, command deny, timeout, stdout/stderr cap; không tắt sandbox để đạt test.

### P11-04 — Approval/receipt/idempotency

- Nguồn/tiêu chí: [Phase 11 checklist](../../../phases/phase-11.md#ca-kiểm-định-riêng-của-phase), [spec approval/tool receipt](../../../../product-spec.md#7-mô-hình-dữ-liệu-logic-và-các-bất-biến), [approval states](../../../../product-spec.md#8-state-machines-cho-task-run-và-approval).
- Bắt buộc: Có.
- Điều kiện/môi trường: Không tạo action/approval side effect.
- Bước/lệnh: Đối chiếu Phase 10 API status, registry `side_effect`, và không có production call site.
- Kỳ vọng: Prepared trước dispatch; approval đúng hash/version; receipt/idempotency; unknown/disconnect không retry.
- Thực tế: Registry chỉ có read-only tool và không có receipt/action lifecycle; Phase 10 API chưa dispatch vào executor, Phase 09 lease/retry/recovery chưa hoàn thành. Không thể tạo approval-approved action trong scope an toàn.
- Kết quả phản biện: none.
- Tag: need-change.
- Kết quả: blocked.
- Mức độ: major.
- Evidence: [roadmap](../../../../master-plan.md#phase-11--hệ-thống-công-cụ-thực-thi), [commands](evidence/commands.md).
- Xử lý/đề xuất: Tích hợp durable approval consume, receipt, idempotency và reconcile theo kết quả đã biết; giữ unknown blocked, không retry.

### P11-05 — Run code thật trong sandbox

- Nguồn/tiêu chí: [Phase 11 checklist](../../../phases/phase-11.md#ca-kiểm-định-riêng-của-phase), [demo Phase 11](../../../../master-plan.md#phase-11--hệ-thống-công-cụ-thực-thi).
- Bắt buộc: Có.
- Điều kiện/môi trường: Không có grant inference/runtime sandbox; không dispatch.
- Bước/lệnh: Kiểm tra source/module/test inventory.
- Kỳ vọng: Sửa file nhỏ, chạy test, đọc trang allowlist; có diff/test exit/artifact/trace liên kết thật.
- Thực tế: Chỉ có local read-only text adapter; chưa có write/code/terminal/browser/network, artifact/diff manifest, sandbox, trace integration hoặc inference grant. Không dùng mock thay run bắt buộc.
- Kết quả phản biện: none.
- Tag: need-change.
- Kết quả: blocked.
- Mức độ: major.
- Evidence: [manifest](evidence/source-manifest.json), [commands](evidence/commands.md).
- Xử lý/đề xuất: Cần grant mới đúng phase/batch/cases trước run thật sau khi sandbox/capabilities đạt; kết quả Phase 10/Phase 09 cũng phải được giải quyết.

### P11-06 — Redaction/correlation

- Nguồn/tiêu chí: [Phase 11 checklist](../../../phases/phase-11.md#ca-kiểm-định-riêng-của-phase), [spec event redaction/correlation](../../../../product-spec.md#9-event-contract-v1-và-replay).
- Bắt buộc: Có.
- Điều kiện/môi trường: Chỉ canary giả; không có event/log persistence runtime.
- Bước/lệnh: Chạy synthetic redaction repro; focused pytest kiểm tra `api_key` và correlation metadata (`sha256`, `byte_count`).
- Kỳ vọng: Credential canaries trong content/log/diff/prompt được che trước khi rời trusted boundary; correlation IDs/metadata vẫn theo trace.
- Thực tế: `redact_text` giữ nguyên `Authorization: Basic test-canary-123` và `cookie=test-cookie-456`, đây là fail có thể tái hiện. Unit test thành công cho `api_key` không phủ các dạng này. Correlation chỉ hiện là file hash/byte count; chưa có run/tool correlation ID hay logs/Inspector để xác minh.
- Kết quả phản biện: none.
- Tag: need-change.
- Kết quả: fail.
- Mức độ: major.
- Evidence: [P11-06 canary](evidence/P11-06-redaction.md), [commands](evidence/commands.md).
- Xử lý/đề xuất: Sửa credential redaction, test Authorization/cookie/credential/private-key và multiline/spacing variants, sau đó retest output end-to-end. Root đã được báo trước mọi source edit.

### P11-07 — Replay và external denial

- Nguồn/tiêu chí: [Phase 11 checklist](../../../phases/phase-11.md#ca-kiểm-định-riêng-của-phase), [spec replay/external action](../../../../product-spec.md#9-event-contract-v1-và-replay), [authority matrix](../../../../product-spec.md#10-quyền-auth-và-inference-gates).
- Bắt buộc: Có.
- Điều kiện/môi trường: Không gọi replay/action/network.
- Bước/lệnh: Static search source/API call sites; compare registry and phase status.
- Kỳ vọng: Replay không dispatch; external send/deploy deny khi không có quyền và không thực hiện bên ngoài test env.
- Thực tế: Không có replay tool trace path, external connector, send/deploy tool hoặc dispatch counter trong module được giao. Chưa có runtime để chứng minh các deny.
- Kết quả phản biện: none.
- Tag: need-change.
- Kết quả: blocked.
- Mức độ: major.
- Evidence: [commands](evidence/commands.md), [manifest](evidence/source-manifest.json).
- Xử lý/đề xuất: Khi có executor/replay, xác minh read-only bằng dispatch counters và direct API attempts; external tools phải deny mặc định.

## Integration / release gates

| Gate áp dụng | Verdict | Test IDs | Evidence |
| --- | --- | --- | --- |
| Không có IG riêng cho Phase 11 | Không áp dụng | C01–C08, P11-01…07 vẫn bắt buộc | Checklist Phase 11 ghi rõ không có gate IG; không phát sinh grant. |

## Cleanup, giới hạn và bàn giao

- Cleanup: Chỉ pytest temporary fixtures trong `tmp_path`; tự cleanup theo pytest. Không tạo DB/runtime artifact hay external resource.
- Chưa kiểm chứng: C03/C04, P11-01…05, P11-07 bị blocked do executor/dependency/grant/runtime chưa có; correlation end-to-end cũng chưa được thực hiện ở P11-06.
- Cần sửa: C05/P11-06 — major redaction gap: Authorization/cookie canaries thoát qua `redact_text` vào output của reader. Evidence synthetic ở [P11-06-redaction.md](evidence/P11-06-redaction.md). Đã báo người điều phối trước khi có sửa.
- Blocker dependency: Phase 10 approval chưa nối executor; Phase 09 worker lease/retry/recovery thiếu. Chưa có OS sandbox, network/terminal, file-write/artifact/diff/replay path; grant inference = 0. Cần điều kiện này trước kiểm thử đầy đủ, không dùng mocks để thay run thật.
- Đề xuất tùy chọn: Chưa có; không dùng suggestion để che thiếu evidence bắt buộc.
- Bước tiếp theo: Remake finding redaction trong Phase 11 rồi retest vòng kế tiếp. Các case blocked chỉ chạy sau khi dependency/quyền tương ứng sẵn sàng; không tự bắt đầu phase khác.
- Bàn giao: Batch report này là snapshot của source theo manifest; kỹ thuật hiện **cần sửa**, không phải nghiệm thu Phase 11 và không cập nhật master-plan.
