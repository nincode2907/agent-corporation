# Kiểm định Phase 06 — 20261009T121142+0700-r002-test

## Thông tin batch

- Phase: 06
- Test batch: 20261009T121142+0700-r002-test
- Vòng: r002
- Bắt đầu / kết thúc: 2026-10-09T12:11:42+07:00 / 2026-10-09T12:16:45.864836+07:00
- Người/AI kiểm định: /root/independent_06_07_qa
- Độc lập với AI triển khai/remake: /root và implementation agents ≠ /root/independent_06_07_qa
- Yêu cầu/phạm vi được giao: Chủ tịch yêu cầu fix blocker, thực hiện lại Phase06/07; QA không sửa productcode.
- Source: [manifest](evidence/source-manifest.json); dirty worktree, khôngcommit.
- Môi trường/config/tool versions: [commands](evidence/commands.md); PostgreSQLdisposable, fake credentials.
- Inference: 0; Ownergrant thực tế0; khôngsharedgatewayprobe/POST.
- Dependency/quyết định nghiệm thu: [master-plan](../../../../master-plan.md); chưanghiệmthu05/06/07, userauthorizesimplementation nhưnggrantCG01riêng.
- Supersedes: [r001](../20261008T170343+0700-r001-test/report.md)
- Remake nguồn: Không có; triển khai lại theo chỉ thị unblock của Chủ tịch.
- Kết luận kỹ thuật: cần sửa
- Quyết định Chủ tịch: Chưa có

## Mapping và phạm vi kiểm định

| Tiêu chí | Test IDs | Bắt buộc |
| --- | --- | --- |
| AC1 livecompleted/errors | P06-03, P06-04 | Có |
| AC2 isolation/policy | P06-01, P06-02, P06-08 | Có |
| AC3 limits/usage | P06-05, P06-06, P06-07 | Có |

## Tổng hợp

| Tag | Số test |
| --- | --- |
| clean | 6 |
| need-change | 10 |
| suggestion | 0 |

| Result | Số test |
| --- | --- |
| pass | 6 |
| fail | 5 |
| blocked | 5 |
| not-run | 0 |
| not-applicable | 0 |

## Kết quả từng test

### C01 — Phạm vi và diff

- Nguồn/tiêu chí: [Checklist](../../../phases/phase-06.md), [RULES](../../../RULES.md), [Spec](../../../../product-spec.md).
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

- Nguồn/tiêu chí: [Checklist](../../../phases/phase-06.md), [RULES](../../../RULES.md), [Spec](../../../../product-spec.md).
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

- Nguồn/tiêu chí: [Checklist](../../../phases/phase-06.md), [RULES](../../../RULES.md), [Spec](../../../../product-spec.md).
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

- Nguồn/tiêu chí: [Checklist](../../../phases/phase-06.md), [RULES](../../../RULES.md), [Spec](../../../../product-spec.md).
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

- Nguồn/tiêu chí: [Checklist](../../../phases/phase-06.md), [RULES](../../../RULES.md), [Spec](../../../../product-spec.md).
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

- Nguồn/tiêu chí: [Checklist](../../../phases/phase-06.md), [RULES](../../../RULES.md), [Spec](../../../../product-spec.md).
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

- Nguồn/tiêu chí: [Checklist](../../../phases/phase-06.md), [RULES](../../../RULES.md), [Spec](../../../../product-spec.md).
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

- Nguồn/tiêu chí: [Checklist](../../../phases/phase-06.md), [RULES](../../../RULES.md), [Spec](../../../../product-spec.md).
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

### P06-01 — Grant defaultdeny

- Nguồn/tiêu chí: [Checklist](../../../phases/phase-06.md), [RULES](../../../RULES.md), [Spec](../../../../product-spec.md).
- Bắt buộc: có
- Điều kiện/môi trường: Isolated PostgreSQL18.6, nonprivilegedapprole, fakeOwnersecret/fixtures, no inference.
- Bước/lệnh: [commands](evidence/commands.md); actualPG/API và sourceinspection đúng scope.
- Kỳ vọng: Đáp ứng đầy đủ contract của testID trong checklist; live criteria chỉ pass cógrant/proof/evidence thật.
- Thực tế: Unit mismatchphase/batch/purpose/model/effort/revoked/expiry/request/concurrency + PGstop/revoke/missinggrant PASS; 0network.
- Kết quả phản biện: none
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [observations](evidence/runtime-observations.md), [manifest](evidence/source-manifest.json), [independent cases](evidence/independent-cases.py).
- Xử lý/đề xuất: Giữ kết quả; kiểm regression khi source sửa.

### P06-02 — Sandbox/CG01 boundary

- Nguồn/tiêu chí: [Checklist](../../../phases/phase-06.md), [RULES](../../../RULES.md), [Spec](../../../../product-spec.md).
- Bắt buộc: có
- Điều kiện/môi trường: Isolated PostgreSQL18.6, nonprivilegedapprole, fakeOwnersecret/fixtures, no inference.
- Bước/lệnh: [commands](evidence/commands.md); actualPG/API và sourceinspection đúng scope.
- Kỳ vọng: Đáp ứng đầy đủ contract của testID trong checklist; live criteria chỉ pass cógrant/proof/evidence thật.
- Thực tế: CG01 JSON[] gâyAttributeError; cần failclosed typeregular checks. Liveisolation/privacy vẫn blocked, không thaybằngfixture.
- Kết quả phản biện: none
- Tag: need-change
- Kết quả: fail
- Mức độ: major
- Evidence: [observations](evidence/runtime-observations.md), [manifest](evidence/source-manifest.json), [independent cases](evidence/independent-cases.py).
- Xử lý/đề xuất: Remake trong06/07 theo evidence; live CG01/grant giữblocked tớiquyết định riêng. ThiếuevidenceisolatedUI/crash/SSE giải quyết bằng retest.

### P06-03 — Turn textonly thật

- Nguồn/tiêu chí: [Checklist](../../../phases/phase-06.md), [RULES](../../../RULES.md), [Spec](../../../../product-spec.md).
- Bắt buộc: có
- Điều kiện/môi trường: Isolated PostgreSQL18.6, nonprivilegedapprole, fakeOwnersecret/fixtures, no inference.
- Bước/lệnh: [commands](evidence/commands.md); actualPG/API và sourceinspection đúng scope.
- Kỳ vọng: Đáp ứng đầy đủ contract của testID trong checklist; live criteria chỉ pass cógrant/proof/evidence thật.
- Thực tế: Chưa cógrantOwner cho batchnày/CG01proof; không gọi modelthật.
- Kết quả phản biện: none
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Evidence: [observations](evidence/runtime-observations.md), [manifest](evidence/source-manifest.json), [independent cases](evidence/independent-cases.py).
- Xử lý/đề xuất: Remake trong06/07 theo evidence; live CG01/grant giữblocked tớiquyết định riêng. ThiếuevidenceisolatedUI/crash/SSE giải quyết bằng retest.

### P06-04 — Error/timeout/unknown

- Nguồn/tiêu chí: [Checklist](../../../phases/phase-06.md), [RULES](../../../RULES.md), [Spec](../../../../product-spec.md).
- Bắt buộc: có
- Điều kiện/môi trường: Isolated PostgreSQL18.6, nonprivilegedapprole, fakeOwnersecret/fixtures, no inference.
- Bước/lệnh: [commands](evidence/commands.md); actualPG/API và sourceinspection đúng scope.
- Kỳ vọng: Đáp ứng đầy đủ contract của testID trong checklist; live criteria chỉ pass cógrant/proof/evidence thật.
- Thực tế: FakeHTTP302/socketclose/502/504/toolproposal unknown, PGlease recoveryfenced stalecompleted; không autoretry unknown.
- Kết quả phản biện: none
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [observations](evidence/runtime-observations.md), [manifest](evidence/source-manifest.json), [independent cases](evidence/independent-cases.py).
- Xử lý/đề xuất: Giữ kết quả; kiểm regression khi source sửa.

### P06-05 — Resource reservation race

- Nguồn/tiêu chí: [Checklist](../../../phases/phase-06.md), [RULES](../../../RULES.md), [Spec](../../../../product-spec.md).
- Bắt buộc: có
- Điều kiện/môi trường: Isolated PostgreSQL18.6, nonprivilegedapprole, fakeOwnersecret/fixtures, no inference.
- Bước/lệnh: [commands](evidence/commands.md); actualPG/API và sourceinspection đúng scope.
- Kỳ vọng: Đáp ứng đầy đủ contract của testID trong checklist; live criteria chỉ pass cógrant/proof/evidence thật.
- Thực tế: PGconcurrency/globalguard/rollback PASS nhưng completedmissingusage cho phép samegrantcallmới, bỏunresolvedreservation.
- Kết quả phản biện: none
- Tag: need-change
- Kết quả: fail
- Mức độ: major
- Evidence: [observations](evidence/runtime-observations.md), [manifest](evidence/source-manifest.json), [independent cases](evidence/independent-cases.py).
- Xử lý/đề xuất: Remake trong06/07 theo evidence; live CG01/grant giữblocked tớiquyết định riêng. ThiếuevidenceisolatedUI/crash/SSE giải quyết bằng retest.

### P06-06 — Stop/abort baseline

- Nguồn/tiêu chí: [Checklist](../../../phases/phase-06.md), [RULES](../../../RULES.md), [Spec](../../../../product-spec.md).
- Bắt buộc: có
- Điều kiện/môi trường: Isolated PostgreSQL18.6, nonprivilegedapprole, fakeOwnersecret/fixtures, no inference.
- Bước/lệnh: [commands](evidence/commands.md); actualPG/API và sourceinspection đúng scope.
- Kỳ vọng: Đáp ứng đầy đủ contract của testID trong checklist; live criteria chỉ pass cógrant/proof/evidence thật.
- Thực tế: FakeHTTPcancellation và durablequeuedstop PASS; livegatewaycancellation cầngrant/CG01 chưa có.
- Kết quả phản biện: none
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Evidence: [observations](evidence/runtime-observations.md), [manifest](evidence/source-manifest.json), [independent cases](evidence/independent-cases.py).
- Xử lý/đề xuất: Remake trong06/07 theo evidence; live CG01/grant giữblocked tớiquyết định riêng. ThiếuevidenceisolatedUI/crash/SSE giải quyết bằng retest.

### P06-07 — Usage provenance

- Nguồn/tiêu chí: [Checklist](../../../phases/phase-06.md), [RULES](../../../RULES.md), [Spec](../../../../product-spec.md).
- Bắt buộc: có
- Điều kiện/môi trường: Isolated PostgreSQL18.6, nonprivilegedapprole, fakeOwnersecret/fixtures, no inference.
- Bước/lệnh: [commands](evidence/commands.md); actualPG/API và sourceinspection đúng scope.
- Kỳ vọng: Đáp ứng đầy đủ contract của testID trong checklist; live criteria chỉ pass cógrant/proof/evidence thật.
- Thực tế: Gatewaynumeric/null parsing PASS; missingusage reservation bịrelease, cần giữunresolved và late reconciliation theoSpec11.
- Kết quả phản biện: none
- Tag: need-change
- Kết quả: fail
- Mức độ: major
- Evidence: [observations](evidence/runtime-observations.md), [manifest](evidence/source-manifest.json), [independent cases](evidence/independent-cases.py).
- Xử lý/đề xuất: Remake trong06/07 theo evidence; live CG01/grant giữblocked tớiquyết định riêng. ThiếuevidenceisolatedUI/crash/SSE giải quyết bằng retest.

### P06-08 — Snapshot/idle/task lifecycle

- Nguồn/tiêu chí: [Checklist](../../../phases/phase-06.md), [RULES](../../../RULES.md), [Spec](../../../../product-spec.md).
- Bắt buộc: có
- Điều kiện/môi trường: Isolated PostgreSQL18.6, nonprivilegedapprole, fakeOwnersecret/fixtures, no inference.
- Bước/lệnh: [commands](evidence/commands.md); actualPG/API và sourceinspection đúng scope.
- Kỳ vọng: Đáp ứng đầy đủ contract của testID trong checklist; live criteria chỉ pass cógrant/proof/evidence thật.
- Thực tế: runs_list readonlymissingcompanyFKfail; taskstatusqueued không theo runtimedispatch/completion/stop. Profile checkpoint/historicaltools-off phầnđãpass.
- Kết quả phản biện: none
- Tag: need-change
- Kết quả: fail
- Mức độ: major
- Evidence: [observations](evidence/runtime-observations.md), [manifest](evidence/source-manifest.json), [independent cases](evidence/independent-cases.py).
- Xử lý/đề xuất: Remake trong06/07 theo evidence; live CG01/grant giữblocked tớiquyết định riêng. ThiếuevidenceisolatedUI/crash/SSE giải quyết bằng retest.

## Integration / release gates

| Gate áp dụng | PASS / FAIL / BLOCKED | Test IDs | Evidence |
| --- | --- | --- | --- |
| Không có IG riêng; điều kiện livephase | BLOCKED | C03, P06-02, P06-03, P06-06 | CG01/grant thực tế thiếu |

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
