# Kiểm định Phase 05 — 20261009T111044+0700-r003-test

## Thông tin batch

- Phase: 05
- Test batch: 20261009T111044+0700-r003-test
- Vòng: r003
- Bắt đầu / kết thúc: 2026-10-09T11:10:44+07:00 / 2026-10-09T11:14:08+07:00
- Người/AI kiểm định: Codex agent `/root/phase05_retest`
- Độc lập với AI triển khai/remake: Có; remake do `/root` thực hiện, reviewer là agent riêng.
- Yêu cầu/phạm vi được giao: Retest độc lập các disposition của remake Phase 05 r002; không gọi inference, không probe/restart codex-server, không ghi DB, không sửa source sản phẩm.
- Source: Worktree dirty; không dùng commit làm đại diện. [Manifest](evidence/source-manifest.json) ghi hash các file được kiểm.
- Môi trường/config/tool versions: local; Node v24.21.0, npm 11.19.0, uv 0.12.23; không đọc `.env` hay credential.
- Inference: Không gọi; grant = 0.
- Dependency/quyết định nghiệm thu: Phase 04 vẫn Chờ nghiệm thu theo master-plan; Phase 05 cũng Chờ nghiệm thu. Không coi dependency hoàn tất.
- Supersedes: [report r002](../20261008T165952+0700-r002-test/report.md)
- Remake nguồn: [remake r002](../../../../remakes/phase-05/20261009T110817+0700-r002-remake/remake.md)
- Kết luận kỹ thuật: chưa đủ bằng chứng
- Quyết định Chủ tịch: Chưa có nghiệm thu Phase 05.

## Mapping và phạm vi kiểm định

| Tiêu chí hiện tại / nguồn | Test IDs | Bắt buộc / tùy điều kiện | Ghi chú |
| --- | --- | --- | --- |
| Phase 05 phụ thuộc 03, 04; master-plan là nguồn trạng thái | C02 | Bắt buộc | Phase 04 chưa nghiệm thu |
| Health/models và contract gateway; probe live chỉ GET | P05-01 | Bắt buộc | Không probe theo chỉ thị; finding vẫn blocked |
| Offline/401/schema mismatch và demo UI manual | C03, P05-02 | Bắt buộc | Adapter tests chạy lại; UI không mở để tránh đụng runtime/probe |
| Catalog không chứng minh entitlement; profile Owner-only | P05-03, P05-04 | Bắt buộc | Chưa có principal/auth backend |
| 429 queue bounded và fallback Owner allowlist | P05-05 | Bắt buộc | Chưa có queue/policy bền vững |
| CG01 isolation/privacy/retention; không đổi gateway chung | C01, P05-06 | Bắt buộc | Static evidence; không gửi input |
| No inference; report/HTML consistency; regression | C04–C08, P05-07 | Bắt buộc | Không có gate IG riêng; CG01 vẫn blocked |

## Tổng hợp

| Tag | Số test |
| --- | ---: |
| clean | 9 |
| need-change | 6 |
| suggestion | 0 |

| Result | Số test |
| --- | ---: |
| pass | 9 |
| fail | 0 |
| blocked | 6 |
| not-run | 0 |
| not-applicable | 0 |

## Kết quả từng test

### C01 — Phạm vi và diff

- Nguồn/tiêu chí: [Yêu cầu retest](../../../../master-plan.md#phase-05--kết-nối-codex-server-local), [manifest remake](../../../../remakes/phase-05/20261009T110817+0700-r002-remake/evidence/source-manifest.json).
- Bắt buộc: có
- Điều kiện/môi trường: Reviewer độc lập; gateway/API runtime không đụng tới; source hash của remake được đối chiếu trực tiếp.
- Bước/lệnh: Đối chiếu scope được giao, remake và git status; kiểm tra SHA-256 các file trong manifest remake.
- Kỳ vọng: Không có sửa source ngoài phase; không inference, DB write, service restart hoặc gateway probe.
- Thực tế: Tám hash source/evidence trong manifest remake khớp byte-for-byte. Không sửa source sản phẩm; các test regression chỉ chạy unit/ASGI fixture.
- Kết quả phản biện: none
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [manifest kiểm định](evidence/source-manifest.json), [commands](evidence/commands.md).
- Xử lý/đề xuất: Không.

### C02 — Dependency và nguồn trạng thái

- Nguồn/tiêu chí: [Master-plan Phase 04/05](../../../../master-plan.md#phase-05--kết-nối-codex-server-local), [AGENTS.md](../../../../../AGENTS.md).
- Bắt buộc: có
- Điều kiện/môi trường: Kiểm tra tài liệu hiện hành sau remake.
- Bước/lệnh: Đối chiếu status trong AGENTS.md và master-plan cùng dependency Phase 04.
- Kỳ vọng: Không tự đánh dấu phase/dependency hoàn tất; các nguồn trạng thái nhất quán.
- Thực tế: Cả hai nguồn ghi Phase 04 và Phase 05 Chờ nghiệm thu. Dependency Phase 04 chưa được nghiệm thu; roadmap giữ nguyên.
- Kết quả phản biện: none
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [manifest](evidence/source-manifest.json), [master-plan](../../../../master-plan.md).
- Xử lý/đề xuất: Không.

### C03 — Tiêu chí và demo

- Nguồn/tiêu chí: [Nghiệm thu Phase 05](../../../../master-plan.md#phase-05--kết-nối-codex-server-local), [checklist demo](../../../phases/phase-05.md).
- Bắt buộc: có
- Điều kiện/môi trường: Không probe gateway và không đụng runtime; API fixture tests và web build được phép.
- Bước/lệnh: Chạy API health/gateway tests và web lint/build; không mở UI/runtime.
- Kỳ vọng: Demo quan sát được, gồm health/models và trạng thái offline/401/schema mismatch; không inference.
- Thực tế: Fixture tests xác minh mapping error; build đạt. UI/demo mở được và live health/models chưa được kiểm tra trong batch này theo giới hạn được giao.
- Kết quả phản biện: none
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Evidence: [commands](evidence/commands.md), [blocker](evidence/P05-01-remediation-review.md).
- Xử lý/đề xuất: Cần lượt kiểm tra demo/UI riêng không gọi probe gateway hoặc cửa sổ vận hành được phép để xác minh màn hình. Không tính build là demo.

### C04 — Không thực thi âm thầm

- Nguồn/tiêu chí: Phase 05 giới hạn không inference; [Spec §6](../../../../product-spec.md).
- Bắt buộc: có
- Điều kiện/môi trường: Source review và fake transport tests.
- Bước/lệnh: Đọc router/adapter/main và chạy `test_codex_gateway.py`.
- Kỳ vọng: Chỉ nút thủ công gọi probe; probe chỉ GET allowlist, không POST/session/tool/model.
- Thực tế: Router chỉ expose GET `/api/v1/codex/probe`; adapter chỉ GET `/health` và `/v1/models`. Spy test xác nhận đúng hai GET; không thấy call path inference trong startup/health.
- Kết quả phản biện: none
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [commands](evidence/commands.md), [manifest](evidence/source-manifest.json).
- Xử lý/đề xuất: Không.

### C05 — Scope và secret

- Nguồn/tiêu chí: Phase 05 auth ref/redaction và secret handling.
- Bắt buộc: có
- Điều kiện/môi trường: Fake secret canary trong unit test; không đọc `.env`.
- Bước/lệnh: Chạy adapter tests và đọc normalized output.
- Kỳ vọng: Không trả token ra response/UI; catalog không khẳng định entitlement.
- Thực tế: Canary test pass; response chỉ giữ model IDs, boolean auth config và `entitlement_verified=false`. Không có secret thật được đọc.
- Kết quả phản biện: none
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [commands](evidence/commands.md), [adapter tests](../../../../../apps/api/tests/test_codex_gateway.py).
- Xử lý/đề xuất: Không.

### C06 — Tài liệu và bản nhìn

- Nguồn/tiêu chí: [Tài liệu Phase 05](../../../../master-plan.md#phase-05--kết-nối-codex-server-local), quy tắc đồng bộ Markdown/HTML.
- Bắt buộc: có
- Điều kiện/môi trường: Report r003 và roadmap được render sau khi thêm batch.
- Bước/lệnh: Chạy validator report, render roadmap, kiểm HTML có Phase 05 status và lang vi.
- Kỳ vọng: HTML khớp Markdown; trạng thái vẫn Chờ nghiệm thu; không hiện tick false-positive.
- Thực tế: Render/validator thành công; HTML có lang="vi", trạng thái Phase 05 vẫn Chờ nghiệm thu, và tab Kiểm thử hiển thị blocked theo r003.
- Kết quả phản biện: none
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [commands](evidence/commands.md), [HTML roadmap](../../../../master-plan.html).
- Xử lý/đề xuất: Không.

### C07 — Regression liên quan

- Nguồn/tiêu chí: Gateway adapter + health endpoints; web bundle.
- Bắt buộc: có
- Điều kiện/môi trường: Không ghi DB; chỉ API tests, lint và build.
- Bước/lệnh: `pytest apps/api/tests/test_health.py apps/api/tests/test_codex_gateway.py -q`; web lint/build.
- Kỳ vọng: Unit/ASGI health + probe cases, lint, TypeScript/build pass.
- Thực tế: 9 passed; lint exit 0; TypeScript/Vite build exit 0. Không chạy DB suite vì không có source diff và không ghi DB theo scope.
- Kết quả phản biện: none
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [commands](evidence/commands.md).
- Xử lý/đề xuất: Không.

### C08 — Report tái kiểm tra được

- Nguồn/tiêu chí: [RULES §3.4, §4, §7](../../../RULES.md).
- Bắt buộc: có
- Điều kiện/môi trường: Batch r003 với report, manifest, commands và blocker evidence.
- Bước/lệnh: `rtk proxy python3 docs/tests/scripts/validate.py --batch docs/tests/results/phase-05/20261009T111044+0700-r003-test`.
- Kỳ vọng: C01–C08/P05-01…07 đủ tag/result, link evidence và thống kê khớp.
- Thực tế: Validator chấp nhận đầy đủ 15 ca và evidence links.
- Kết quả phản biện: none
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [manifest](evidence/source-manifest.json), [commands](evidence/commands.md), [report](report.md).
- Xử lý/đề xuất: Không.

### P05-01 — Contract và live probe

- Nguồn/tiêu chí: Phase 05 AC1/P05-01; gateway source/capability matrix.
- Bắt buộc: có
- Điều kiện/môi trường: Retest bị giới hạn rõ: không gọi/probe codex-server.
- Bước/lệnh: Source review adapter/router and r002 live probe record; no live HTTP.
- Kỳ vọng: Gateway source matrix and actual GET health/models response prove supported contract/auth/catalog.
- Thực tế: Remake correctly preserved finding as blocked. r002 source record reports gateway offline and no live response; this batch did not reprobe, so offline state is historical evidence only. Contract's live compatibility remains unverified.
- Kết quả phản biện: none
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Evidence: [remake](../../../../remakes/phase-05/20261009T110817+0700-r002-remake/remake.md), [historical probe](../20261008T165952+0700-r002-test/evidence/live-probe.md), [blocker review](evidence/P05-01-remediation-review.md).
- Xử lý/đề xuất: Keep open; needs an explicitly permitted live read-only probe and current evidence. Do not restart shared gateway.

### P05-02 — Offline/auth/schema mismatch

- Nguồn/tiêu chí: Phase 05 demo and checklist P05-02.
- Bắt buộc: có
- Điều kiện/môi trường: Fake adapter cases; no live probe.
- Bước/lệnh: Re-run gateway unit tests; review UI error normalization/build.
- Kỳ vọng: Offline/401/429/schema mismatch are safely normalized; secret is not exposed; UI contract errors do not crash.
- Thực tế: 9 API tests passed, including offline, 401, 429, schema mismatch, proxy bypass and redaction. Web lint/build pass. UI interaction itself was not repeated; C03 records that gap.
- Kết quả phản biện: none
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [commands](evidence/commands.md), [adapter tests](../../../../../apps/api/tests/test_codex_gateway.py).
- Xử lý/đề xuất: No adapter-level change; UI demo evidence remains tracked under C03.

### P05-03 — Catalog, entitlement and profile

- Nguồn/tiêu chí: Phase 05 P05-03; Spec §§6, 10.
- Bắt buộc: có
- Điều kiện/môi trường: Source review + unit tests; no fake Owner principal.
- Bước/lệnh: Run catalog/entitlement tests; inspect API routes and identity/auth implementation.
- Kỳ vọng: Catalog is not entitlement; model/effort profile is changed by authenticated Owner only.
- Thực tế: Catalog remains `entitlement_verified=false` and tests pass. Source has no authenticated identity/principal or profile route, so Owner profile criteria cannot be exercised. Remake correctly did not invent Owner identity.
- Kết quả phản biện: none
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Evidence: [remake](../../../../remakes/phase-05/20261009T110817+0700-r002-remake/remake.md), [blocker review](evidence/P05-01-remediation-review.md), [source manifest](evidence/source-manifest.json).
- Xử lý/đề xuất: Keep open until real authenticated Owner identity/profile path and approved dependency are available.

### P05-04 — Owner-only profile

- Nguồn/tiêu chí: Phase 05 P05-04; Spec §10.
- Bắt buộc: có
- Điều kiện/môi trường: Review API routes and auth source; no mutation attempt.
- Bước/lệnh: Search current API source/tests for principal/auth middleware and profile route.
- Kỳ vọng: Agent denied, Owner update audited/versioned, secret remains backend-only.
- Thực tế: No auth middleware/principal or Owner profile write route exists in inspected API; actual authorization behavior cannot be established. Remake did not add a fake endpoint.
- Kết quả phản biện: none
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Evidence: [blocker review](evidence/P05-01-remediation-review.md), [manifest](evidence/source-manifest.json).
- Xử lý/đề xuất: Keep open pending approved identity/authorization capability; retest deny/allow/audit at API layer then.

### P05-05 — 429 queue and fallback allowlist

- Nguồn/tiêu chí: Phase 05 AC3/P05-05; Spec §§6, 11.
- Bắt buộc: có
- Điều kiện/môi trường: Static API source review and fake 429 adapter tests only.
- Bước/lệnh: Inspect adapter, router and source for durable queue, Owner allowlist and bounded retry.
- Kỳ vọng: Requeue/backoff bounded; fallback restricted to Owner-approved allowlist; unknown side effects are not retried.
- Thực tế: Adapter reports `rate_limited` without retry; inspected API has no gateway queue or Owner fallback policy. Remake's refusal to add an in-memory queue or fabricated policy is correct, but this acceptance criterion remains unresolved.
- Kết quả phản biện: none
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Evidence: [blocker review](evidence/P05-01-remediation-review.md), [adapter tests](../../../../../apps/api/tests/test_codex_gateway.py).
- Xử lý/đề xuất: Keep open pending approved queue/policy design and restart/resume/idempotency evidence.

### P05-06 — CG01 isolation and privacy

- Nguồn/tiêu chí: Spec §6 CG01; Phase 05 P05-06.
- Bắt buộc: có
- Điều kiện/môi trường: Static source/evidence review only; no prompt/input sent and no gateway contact.
- Bước/lệnh: Read Phase 05 evidence and remake disposition; no live execution.
- Kỳ vọng: Prove isolation/read boundary and retention before submitting input; if missing, block and report the gap without changing shared gateway.
- Thực tế: Existing evidence says read-only mode does not isolate filesystem reads and chat may persist thread/rollout. Remake preserved this boundary. This reviewer did not retest gateway capability, so the gate remains blocked.
- Kết quả phản biện: none
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Evidence: [Phase 05 capability evidence](../../../../evidence/phase-05.md), [remake](../../../../remakes/phase-05/20261009T110817+0700-r002-remake/remake.md).
- Xử lý/đề xuất: Keep CG01 blocked until read/isolation/retention evidence or an explicit decision resolves it; no input sent.

### P05-07 — Không inference từ probe

- Nguồn/tiêu chí: Phase 05 limits and inference grant rule.
- Bắt buộc: có
- Điều kiện/môi trường: Static router/source review and fake request spy.
- Bước/lệnh: Run API tests and inspect GET-only adapter call path.
- Kỳ vọng: Probe makes no inference/session/tool request; no implicit grant.
- Thực tế: Spy asserts exactly health and models GET; app exposes only manual probe route; no inference was requested; grant=0.
- Kết quả phản biện: none
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [commands](evidence/commands.md), [source manifest](evidence/source-manifest.json).
- Xử lý/đề xuất: Không.

## Integration / release gates

| Gate áp dụng | PASS / FAIL / BLOCKED | Test IDs | Batch/grant/config/evidence và gate trước |
| --- | --- | --- | --- |
| Phase 05 không có IG riêng; CG01 decision gate | BLOCKED | C03, P05-01, P05-03, P05-04, P05-05, P05-06 | r003; grant 0; no gateway probe by explicit scope; Phase 04 pending; Owner auth, queue/policy and CG01 evidence absent. |

## Remake r002 disposition

Các blocker của remake được **accepted là blocker hợp lệ**, không phải finding đã đóng: P05-01 live contract, P05-03 Owner profile, P05-04 authorization, P05-05 durable queue/fallback và P05-06 CG01. Không có disposition nào bị rejected. Các tiêu chí bắt buộc vẫn mở; không tick hoàn tất.

## Cleanup, giới hạn và bàn giao

- Cleanup: Không gọi gateway, không gọi inference, không ghi DB, không restart service; không sửa source sản phẩm.
- Chưa kiểm chứng: Live gateway health/models/auth; UI/demo tương tác batch này; Owner profile/auth; durable queue/fallback; CG01 runtime capabilities.
- Cần sửa/giải quyết: P05-01/03/04/05/06 cùng C03 đang blocked; cần runtime/quyết định/dependency được phép rồi chạy batch test mới.
- Đề xuất tùy chọn: Không có.
- Bước tiếp theo: Pipeline vẫn **Review bị chặn**; không bắt đầu phase khác. Có thể tiếp tục retest Phase 05 khi blocker được xử lý và phạm vi cho phép.
- Bàn giao: Report r003 và evidence; Phase 05 vẫn Chờ nghiệm thu.
