# Kiểm định Phase 07 — 20261009T121142+0700-r002-test

## Thông tin batch

- Phase: 07
- Test batch: 20261009T121142+0700-r002-test
- Vòng: r002
- Bắt đầu / kết thúc: 2026-10-09T12:11:42+07:00 / 2026-10-09T12:16:45.865663+07:00
- Người/AI kiểm định: /root/independent_06_07_qa
- Độc lập với AI triển khai/remake: /root và implementation agents ≠ /root/independent_06_07_qa
- Yêu cầu/phạm vi được giao: Chủ tịch yêu cầu fix blocker, thực hiện lại Phase06/07; QA không sửa productcode.
- Source: [manifest](evidence/source-manifest.json); dirty worktree, khôngcommit.
- Môi trường/config/tool versions: [commands](evidence/commands.md); PostgreSQLdisposable, fake credentials.
- Inference: 0; Ownergrant thực tế0; khôngsharedgatewayprobe/POST.
- Dependency/quyết định nghiệm thu: [master-plan](../../../../master-plan.md); chưanghiệmthu05/06/07, userauthorizesimplementation nhưnggrantCG01riêng.
- Supersedes: [r001](../20261009T105531+0700-r001-test/report.md)
- Remake nguồn: Không có; triển khai lại theo chỉ thị unblock của Chủ tịch.
- Kết luận kỹ thuật: cần sửa
- Quyết định Chủ tịch: Chưa có

## Mapping và phạm vi kiểm định

| Tiêu chí | Test IDs | Bắt buộc |
| --- | --- | --- |
| AC1 committedsequence/reconnect | P07-01, P07-02, P07-03 | Có |
| AC2 heartbeat/unknown | P07-04, P07-05 | Có |
| AC3 recovery/no duplicates/context/gap | P07-05, P07-06, P07-07 | Có |

## Tổng hợp

| Tag | Số test |
| --- | --- |
| clean | 7 |
| need-change | 8 |
| suggestion | 0 |

| Result | Số test |
| --- | --- |
| pass | 7 |
| fail | 1 |
| blocked | 7 |
| not-run | 0 |
| not-applicable | 0 |

## Kết quả từng test

### C01 — Phạm vi và diff

- Nguồn/tiêu chí: [Checklist](../../../phases/phase-07.md), [RULES](../../../RULES.md), [Spec](../../../../product-spec.md).
- Bắt buộc: có
- Điều kiện/môi trường: Isolated PostgreSQL18.6, nonprivilegedapprole, fakeOwnersecret/fixtures, no inference.
- Bước/lệnh: [commands](evidence/commands.md); actualPG/API và sourceinspection đúng scope.
- Kỳ vọng: Đáp ứng đầy đủ contract của testID trong checklist; live criteria chỉ pass cógrant/proof/evidence thật.
- Thực tế: Đúng scope06/07 và auth dependency được giao unblock; không Phase08, không thay sharedgateway.
- Kết quả phản biện: none
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [observations](evidence/runtime-observations.md), [manifest](evidence/source-manifest.json), [independent cases](evidence/independent-cases.py).
- Xử lý/đề xuất: Giữ kết quả; kiểm regression khi source sửa.

### C02 — Dependency và quyết định

- Nguồn/tiêu chí: [Checklist](../../../phases/phase-07.md), [RULES](../../../RULES.md), [Spec](../../../../product-spec.md).
- Bắt buộc: có
- Điều kiện/môi trường: Isolated PostgreSQL18.6, nonprivilegedapprole, fakeOwnersecret/fixtures, no inference.
- Bước/lệnh: [commands](evidence/commands.md); actualPG/API và sourceinspection đúng scope.
- Kỳ vọng: Đáp ứng đầy đủ contract của testID trong checklist; live criteria chỉ pass cógrant/proof/evidence thật.
- Thực tế: Phase05 chưa nghiệmthu; user cho phép sửa blocker, không cấpgrant/CG01 hoặc tựnghiệmthu.
- Kết quả phản biện: none
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Evidence: [observations](evidence/runtime-observations.md), [manifest](evidence/source-manifest.json), [independent cases](evidence/independent-cases.py).
- Xử lý/đề xuất: Remake trong06/07 theo evidence; live CG01/grant giữblocked tớiquyết định riêng. ThiếuevidenceisolatedUI/crash/SSE giải quyết bằng retest.

### C03 — Criteria/demo

- Nguồn/tiêu chí: [Checklist](../../../phases/phase-07.md), [RULES](../../../RULES.md), [Spec](../../../../product-spec.md).
- Bắt buộc: có
- Điều kiện/môi trường: Isolated PostgreSQL18.6, nonprivilegedapprole, fakeOwnersecret/fixtures, no inference.
- Bước/lệnh: [commands](evidence/commands.md); actualPG/API và sourceinspection đúng scope.
- Kỳ vọng: Đáp ứng đầy đủ contract của testID trong checklist; live criteria chỉ pass cógrant/proof/evidence thật.
- Thực tế: Demo modelthật và runthật tớiUI cầngrantbatch/CG01 chưa có. Mapping giữ đủAC.
- Kết quả phản biện: none
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Evidence: [observations](evidence/runtime-observations.md), [manifest](evidence/source-manifest.json), [independent cases](evidence/independent-cases.py).
- Xử lý/đề xuất: Remake trong06/07 theo evidence; live CG01/grant giữblocked tớiquyết định riêng. ThiếuevidenceisolatedUI/crash/SSE giải quyết bằng retest.

### C04 — Không dispatch âm thầm

- Nguồn/tiêu chí: [Checklist](../../../phases/phase-07.md), [RULES](../../../RULES.md), [Spec](../../../../product-spec.md).
- Bắt buộc: có
- Điều kiện/môi trường: Isolated PostgreSQL18.6, nonprivilegedapprole, fakeOwnersecret/fixtures, no inference.
- Bước/lệnh: [commands](evidence/commands.md); actualPG/API và sourceinspection đúng scope.
- Kỳ vọng: Đáp ứng đầy đủ contract của testID trong checklist; live criteria chỉ pass cógrant/proof/evidence thật.
- Thực tế: Unit/API routes defaultdeny, health/GET/auth/profile không POSTmodel; workerexplicit, trangidle khôngautostart.
- Kết quả phản biện: none
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [observations](evidence/runtime-observations.md), [manifest](evidence/source-manifest.json), [independent cases](evidence/independent-cases.py).
- Xử lý/đề xuất: Giữ kết quả; kiểm regression khi source sửa.

### C05 — Auth/scope/redaction

- Nguồn/tiêu chí: [Checklist](../../../phases/phase-07.md), [RULES](../../../RULES.md), [Spec](../../../../product-spec.md).
- Bắt buộc: có
- Điều kiện/môi trường: Isolated PostgreSQL18.6, nonprivilegedapprole, fakeOwnersecret/fixtures, no inference.
- Bước/lệnh: [commands](evidence/commands.md); actualPG/API và sourceinspection đúng scope.
- Kỳ vọng: Đáp ứng đầy đủ contract của testID trong checklist; live criteria chỉ pass cógrant/proof/evidence thật.
- Thực tế: RealPGauth/CSRF/profile/scope/expiry/logout tests PASS; sensitivevalidation và feedredaction PASS.
- Kết quả phản biện: none
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [observations](evidence/runtime-observations.md), [manifest](evidence/source-manifest.json), [independent cases](evidence/independent-cases.py).
- Xử lý/đề xuất: Giữ kết quả; kiểm regression khi source sửa.

### C06 — Markdown/HTML

- Nguồn/tiêu chí: [Checklist](../../../phases/phase-07.md), [RULES](../../../RULES.md), [Spec](../../../../product-spec.md).
- Bắt buộc: có
- Điều kiện/môi trường: Isolated PostgreSQL18.6, nonprivilegedapprole, fakeOwnersecret/fixtures, no inference.
- Bước/lệnh: [commands](evidence/commands.md); actualPG/API và sourceinspection đúng scope.
- Kỳ vọng: Đáp ứng đầy đủ contract của testID trong checklist; live criteria chỉ pass cógrant/proof/evidence thật.
- Thực tế: Root đang đồng bộ tài liệu/UI; snapshotr002 chưa có finalrender/browser, cầnr003 xácminh.
- Kết quả phản biện: none
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Evidence: [observations](evidence/runtime-observations.md), [manifest](evidence/source-manifest.json), [independent cases](evidence/independent-cases.py).
- Xử lý/đề xuất: Remake trong06/07 theo evidence; live CG01/grant giữblocked tớiquyết định riêng. ThiếuevidenceisolatedUI/crash/SSE giải quyết bằng retest.

### C07 — Regression

- Nguồn/tiêu chí: [Checklist](../../../phases/phase-07.md), [RULES](../../../RULES.md), [Spec](../../../../product-spec.md).
- Bắt buộc: có
- Điều kiện/môi trường: Isolated PostgreSQL18.6, nonprivilegedapprole, fakeOwnersecret/fixtures, no inference.
- Bước/lệnh: [commands](evidence/commands.md); actualPG/API và sourceinspection đúng scope.
- Kỳ vọng: Đáp ứng đầy đủ contract của testID trong checklist; live criteria chỉ pass cógrant/proof/evidence thật.
- Thực tế: FullAPI57tests56pass1fail do runtimeGETcounterFK; readhelper cần sửa và rerun.
- Kết quả phản biện: none
- Tag: need-change
- Kết quả: fail
- Mức độ: major
- Evidence: [observations](evidence/runtime-observations.md), [manifest](evidence/source-manifest.json), [independent cases](evidence/independent-cases.py).
- Xử lý/đề xuất: Remake trong06/07 theo evidence; live CG01/grant giữblocked tớiquyết định riêng. ThiếuevidenceisolatedUI/crash/SSE giải quyết bằng retest.

### C08 — Evidence tái kiểm định

- Nguồn/tiêu chí: [Checklist](../../../phases/phase-07.md), [RULES](../../../RULES.md), [Spec](../../../../product-spec.md).
- Bắt buộc: có
- Điều kiện/môi trường: Isolated PostgreSQL18.6, nonprivilegedapprole, fakeOwnersecret/fixtures, no inference.
- Bước/lệnh: [commands](evidence/commands.md); actualPG/API và sourceinspection đúng scope.
- Kỳ vọng: Đáp ứng đầy đủ contract của testID trong checklist; live criteria chỉ pass cógrant/proof/evidence thật.
- Thực tế: Sourcehashes/commands/fixturecanary/exactIDs; no inference, reporthonest, resources scoped retainedfortest.
- Kết quả phản biện: none
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [observations](evidence/runtime-observations.md), [manifest](evidence/source-manifest.json), [independent cases](evidence/independent-cases.py).
- Xử lý/đề xuất: Giữ kết quả; kiểm regression khi source sửa.

### P07-01 — Lưu trước phát

- Nguồn/tiêu chí: [Checklist](../../../phases/phase-07.md), [RULES](../../../RULES.md), [Spec](../../../../product-spec.md).
- Bắt buộc: có
- Điều kiện/môi trường: Isolated PostgreSQL18.6, nonprivilegedapprole, fakeOwnersecret/fixtures, no inference.
- Bước/lệnh: [commands](evidence/commands.md); actualPG/API và sourceinspection đúng scope.
- Kỳ vọng: Đáp ứng đầy đủ contract của testID trong checklist; live criteria chỉ pass cógrant/proof/evidence thật.
- Thực tế: PGfeed chỉ đọccommitted, transactionrollback khôngemit/counter, outboxdurable; frame unit PASS.
- Kết quả phản biện: none
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [observations](evidence/runtime-observations.md), [manifest](evidence/source-manifest.json), [independent cases](evidence/independent-cases.py).
- Xử lý/đề xuất: Giữ kết quả; kiểm regression khi source sửa.

### P07-02 — Ordering/reconnect

- Nguồn/tiêu chí: [Checklist](../../../phases/phase-07.md), [RULES](../../../RULES.md), [Spec](../../../../product-spec.md).
- Bắt buộc: có
- Điều kiện/môi trường: Isolated PostgreSQL18.6, nonprivilegedapprole, fakeOwnersecret/fixtures, no inference.
- Bước/lệnh: [commands](evidence/commands.md); actualPG/API và sourceinspection đúng scope.
- Kỳ vọng: Đáp ứng đầy đủ contract của testID trong checklist; live criteria chỉ pass cógrant/proof/evidence thật.
- Thực tế: PGpagecursorordered/dedupPASS; HTTP/SSE disconnect→reconnect chưa thực hiệnởr002, cần isolatedstream evidence.
- Kết quả phản biện: none
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Evidence: [observations](evidence/runtime-observations.md), [manifest](evidence/source-manifest.json), [independent cases](evidence/independent-cases.py).
- Xử lý/đề xuất: Remake trong06/07 theo evidence; live CG01/grant giữblocked tớiquyết định riêng. ThiếuevidenceisolatedUI/crash/SSE giải quyết bằng retest.

### P07-03 — Gap/cursor boundary

- Nguồn/tiêu chí: [Checklist](../../../phases/phase-07.md), [RULES](../../../RULES.md), [Spec](../../../../product-spec.md).
- Bắt buộc: có
- Điều kiện/môi trường: Isolated PostgreSQL18.6, nonprivilegedapprole, fakeOwnersecret/fixtures, no inference.
- Bước/lệnh: [commands](evidence/commands.md); actualPG/API và sourceinspection đúng scope.
- Kỳ vọng: Đáp ứng đầy đủ contract của testID trong checklist; live criteria chỉ pass cógrant/proof/evidence thật.
- Thực tế: PGcountergapraisesEventGap; session/scope/tamper/expiry cursorunit + authenticatedAPIinvalidcursor400 + lastIDconflict400 PASS.
- Kết quả phản biện: none
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [observations](evidence/runtime-observations.md), [manifest](evidence/source-manifest.json), [independent cases](evidence/independent-cases.py).
- Xử lý/đề xuất: Giữ kết quả; kiểm regression khi source sửa.

### P07-04 — Heartbeat/offline UI

- Nguồn/tiêu chí: [Checklist](../../../phases/phase-07.md), [RULES](../../../RULES.md), [Spec](../../../../product-spec.md).
- Bắt buộc: có
- Điều kiện/môi trường: Isolated PostgreSQL18.6, nonprivilegedapprole, fakeOwnersecret/fixtures, no inference.
- Bước/lệnh: [commands](evidence/commands.md); actualPG/API và sourceinspection đúng scope.
- Kỳ vọng: Đáp ứng đầy đủ contract của testID trong checklist; live criteria chỉ pass cógrant/proof/evidence thật.
- Thực tế: PGheartbeat guardPASS; browser actualstale/offline chưa xong sourceUI, cần r003 runtime/browser evidence.
- Kết quả phản biện: none
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Evidence: [observations](evidence/runtime-observations.md), [manifest](evidence/source-manifest.json), [independent cases](evidence/independent-cases.py).
- Xử lý/đề xuất: Remake trong06/07 theo evidence; live CG01/grant giữblocked tớiquyết định riêng. ThiếuevidenceisolatedUI/crash/SSE giải quyết bằng retest.

### P07-05 — Crash/unknown outcome

- Nguồn/tiêu chí: [Checklist](../../../phases/phase-07.md), [RULES](../../../RULES.md), [Spec](../../../../product-spec.md).
- Bắt buộc: có
- Điều kiện/môi trường: Isolated PostgreSQL18.6, nonprivilegedapprole, fakeOwnersecret/fixtures, no inference.
- Bước/lệnh: [commands](evidence/commands.md); actualPG/API và sourceinspection đúng scope.
- Kỳ vọng: Đáp ứng đầy đủ contract của testID trong checklist; live criteria chỉ pass cógrant/proof/evidence thật.
- Thực tế: PGleaseexpire recovery/idempotency/fencingPASS; actual disposableworkerprocesskillcheckpoint cònthiếu, khôngclaimcrashtest từ source.
- Kết quả phản biện: none
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Evidence: [observations](evidence/runtime-observations.md), [manifest](evidence/source-manifest.json), [independent cases](evidence/independent-cases.py).
- Xử lý/đề xuất: Remake trong06/07 theo evidence; live CG01/grant giữblocked tớiquyết định riêng. ThiếuevidenceisolatedUI/crash/SSE giải quyết bằng retest.

### P07-06 — Session/context recovery

- Nguồn/tiêu chí: [Checklist](../../../phases/phase-07.md), [RULES](../../../RULES.md), [Spec](../../../../product-spec.md).
- Bắt buộc: có
- Điều kiện/môi trường: Isolated PostgreSQL18.6, nonprivilegedapprole, fakeOwnersecret/fixtures, no inference.
- Bước/lệnh: [commands](evidence/commands.md); actualPG/API và sourceinspection đúng scope.
- Kỳ vọng: Đáp ứng đầy đủ contract của testID trong checklist; live criteria chỉ pass cógrant/proof/evidence thật.
- Thực tế: StatelessHTTP apphistory/checkpoints bềnvững, 401failed khôngresumefailedgateway session; expiredOwner401 và no newPOST tested.
- Kết quả phản biện: none
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [observations](evidence/runtime-observations.md), [manifest](evidence/source-manifest.json), [independent cases](evidence/independent-cases.py).
- Xử lý/đề xuất: Giữ kết quả; kiểm regression khi source sửa.

### P07-07 — Run thật đến UI

- Nguồn/tiêu chí: [Checklist](../../../phases/phase-07.md), [RULES](../../../RULES.md), [Spec](../../../../product-spec.md).
- Bắt buộc: có
- Điều kiện/môi trường: Isolated PostgreSQL18.6, nonprivilegedapprole, fakeOwnersecret/fixtures, no inference.
- Bước/lệnh: [commands](evidence/commands.md); actualPG/API và sourceinspection đúng scope.
- Kỳ vọng: Đáp ứng đầy đủ contract của testID trong checklist; live criteria chỉ pass cógrant/proof/evidence thật.
- Thực tế: Chưagrantbatch vàCG01, khôngliveinference; fakefeedkhôngpassrunthật.
- Kết quả phản biện: none
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Evidence: [observations](evidence/runtime-observations.md), [manifest](evidence/source-manifest.json), [independent cases](evidence/independent-cases.py).
- Xử lý/đề xuất: Remake trong06/07 theo evidence; live CG01/grant giữblocked tớiquyết định riêng. ThiếuevidenceisolatedUI/crash/SSE giải quyết bằng retest.

## Integration / release gates

| Gate áp dụng | PASS / FAIL / BLOCKED | Test IDs | Evidence |
| --- | --- | --- | --- |
| Không có IG riêng; điều kiện livephase | BLOCKED | C03, P07-07 | CG01/grant thực tế thiếu |

## Bypass Attempts

| Rule | Attempt | Result |
| --- | --- | --- |
| Owner scope | Login othercompany withoutscope | 403PASS actualPG |
| CSRF | Writeprofile noCSRF | 403PASS |
| ProfileCAS | Reuseversion0 | 409PASS |
| Missingusage | Nextsamegrantreservation | FAIL |
| CG01proof | JSONlist | FAIL |

## Cleanup, giới hạn và bàn giao

- Cleanup: Chỉ dataset/container disposable củaQA; giữcontainer cho r003, xóa sau retest. KhôngsharedDB/service/credentials.
- Chưa kiểm chứng: liveinference/isolation/privacy/cancellation và UI/SSE/crashruntime chưa có evidence đầy đủởr002.
- Cần sửa: runtimeGETreadtransaction, malformedproof failclosed, missingusage reservation/late reconciliation, tasklifecycle; đồng bộdocs/UI và bổsung stream/crash evidence.
- Bước tiếp theo: Rootremake→AItestđộclậpr003; khôngnghiệmthu/sang08.
- Bàn giao: Systematic risk-based coverage in assigned scope; kếtluận cần sửa. Blockrelease nănglựcruntime thật tớiCG01/grant evidence.
