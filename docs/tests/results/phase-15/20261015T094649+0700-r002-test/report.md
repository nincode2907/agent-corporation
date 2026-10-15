# Kiểm định Phase 15 — 20261015T094649+0700-r002-test

## Thông tin batch

- Phase: 15
- Test batch: 20261015T094649+0700-r002-test
- Vòng: r002
- Bắt đầu / kết thúc: 2026-10-15 09:46:49–09:46:50 +07:00 (Asia/Ho_Chi_Minh)
- Người/AI kiểm định: `/root/phase11_independent_test`
- Độc lập với AI triển khai/remake: kiểm định độc lập với `/root` theo pipeline được giao.
- Yêu cầu/phạm vi được giao: retest Phase 15 r001 locator validation fix; verify traversal-shaped refs rejected and valid namespaced ref accepted; no source edit, DB/runtime/inference.
- Source: dirty worktree, no commit snapshot; Phase 15 source/test hashes at [manifest](evidence/source-manifest.sha256).
- Môi trường/config/tool versions: Python project `apps/api`; focused pytest and synthetic contract construction with fake IDs; no `.env`/secret read.
- Inference: none; grant = 0.
- Dependency/quyết định nghiệm thu: Phase 14 not accepted; roadmap Phase 15 remains `Chưa triển khai`; no Owner acceptance.
- Supersedes: [Phase 15 r001](../20261015T094220+0700-r001-test/report.md).
- Remake nguồn: [Phase 15 r001 remake](../../../../remakes/phase-15/20261015T094458+0700-r001-remake/remake.md).
- Kết luận kỹ thuật: **chưa đủ bằng chứng**.
- Quyết định Chủ tịch: Chưa có.

## Mapping và phạm vi kiểm định

| Tiêu chí hiện tại / nguồn | Test IDs | Bắt buộc / tùy điều kiện | Ghi chú |
| --- | --- | --- | --- |
| C01–C08 theo [RULES §5](../../../RULES.md) | C01–C08 | Bắt buộc | Source freeze/remake, dependency, demo, dispatch, data boundary, docs, regression, report recheck. |
| AC1: retrieval and promotion enforce company/environment/ACL | P15-01, P15-02 | Bắt buộc | Locator fix verified; ACL still supplied by trusted caller and no backend store. |
| AC2: run snapshot resolves source/version and rollback preserves history | P15-03, P15-04 | Bắt buộc | Pure immutable/append contracts only; persistence/run snapshot absent. |
| AC3: no full chat-history stuffing; untrusted data does not override policy | P15-01, P15-05, P15-06 | Bắt buộc | No real context builder, redaction/retention/resume integration. |
| Required reviewer promotion → next-run exact version and cross-department denial demo | P15-02…P15-04 | Bắt buộc | No end-to-end demo; Phase 14 dependency remains unaccepted. |

## Tổng hợp

| Tag | Số test |
| --- | ---: |
| clean | 6 |
| need-change | 8 |
| suggestion | 0 |

| Result | Số test |
| --- | ---: |
| pass | 6 |
| fail | 0 |
| blocked | 8 |
| not-run | 0 |
| not-applicable | 0 |

## Kết quả từng test

### C01 — Phạm vi và diff

- Nguồn/tiêu chí: [RULES C01](../../../RULES.md); Phase 15 source/test/remake files.
- Bắt buộc: có.
- Điều kiện/môi trường: dirty worktree; no product source edits.
- Bước/lệnh: `rtk git status --short`; compare source hashes with remake record.
- Kỳ vọng: review authorized Phase 15 locator fix only and preserve other changes.
- Thực tế: current contract/test hashes match remake record; no source edit made.
- Kết quả phản biện: accepted — P15 locator validator fix is verified by fresh negative and positive cases.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [source manifest](evidence/source-manifest.sha256); [remake record](../../../../remakes/phase-15/20261015T094458+0700-r001-remake/remake.md).
- Xử lý/đề xuất: none.

### C02 — Dependency và nguồn quyết định

- Nguồn/tiêu chí: [Phase 15 roadmap](../../../../master-plan.md#phase-15--context-và-trí-nhớ-có-kiểm-chứng), checklist, Spec REQ17.
- Bắt buộc: có.
- Điều kiện/môi trường: read-only docs review.
- Bước/lệnh: read current roadmap/checklist/spec/ADR references.
- Kỳ vọng: dependency/status/grant accurately reported.
- Thực tế: dependency Phase 14 not accepted; Phase 15 remains `Chưa triển khai`; no Owner acceptance/grant.
- Kết quả phản biện: none.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [checklist](../../../phases/phase-15.md); [roadmap](../../../../master-plan.md).
- Xử lý/đề xuất: keep remaining runtime blockers explicit.

### C03 — Đủ criteria và demo

- Nguồn/tiêu chí: [Phase 15 AC/demo](../../../../master-plan.md#phase-15--context-và-trí-nhớ-có-kiểm-chứng), P15-01…06.
- Bắt buộc: có.
- Điều kiện/môi trường: contract unit tests only; no trusted ACL/persistence/context builder/retrieval integration.
- Bước/lệnh: focused Phase 15 pytest; checklist/demo evidence review.
- Kỳ vọng: worker proposes, reviewer approves, next run uses exact version; cross-department deny, rollback/retention evidence available.
- Thực tế: only pure contracts and locator checks ran; no end-to-end demo, manifest persistence, next-run selection, redaction or resume artifacts.
- Kết quả phản biện: none.
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Evidence: [test output](evidence/test-output.txt); [checklist](../../../phases/phase-15.md).
- Xử lý/đề xuất: integrate required systems after Phase 14 acceptance and valid authorization.

### C04 — Không thực thi âm thầm

- Nguồn/tiêu chí: [RULES C04](../../../RULES.md); memory contract docstring.
- Bắt buộc: có.
- Điều kiện/môi trường: pure contracts; no runtime/model/tool dispatch.
- Bước/lệnh: source review and focused pytest.
- Kỳ vọng: no implicit source retrieval, persistence or dispatch.
- Thực tế: reviewed module explicitly delegates ACL to trusted caller and does not persist/retrieve/grant authority; no dispatch path.
- Kết quả phản biện: none.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [source](../../../../../apps/api/src/agent_corporation_api/modules/memory/contracts.py); [test output](evidence/test-output.txt).
- Xử lý/đề xuất: integration remains blocked separately.

### C05 — Scope và dữ liệu nhạy cảm

- Nguồn/tiêu chí: [RULES C05](../../../RULES.md); Phase 15 locator and data boundary.
- Bắt buộc: có.
- Điều kiện/môi trường: synthetic strings and UUIDs only; no file dereference/secrets.
- Bước/lệnh: direct `ContextSource` negative/positive matrix.
- Kỳ vọng: traversal/path-shaped locators rejected; opaque namespaced ID accepted.
- Thực tế: rejects `../../outside`, `artifact:../../outside`, `/tmp/outside`, and unnamespaced `plain-identifier`; accepts `artifact:ctx-1`. No dereference attempted; no claim of runtime file escape test.
- Kết quả phản biện: accepted — r001 locator finding closed at the contract boundary.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [synthetic output](evidence/test-output.txt); [source hash](evidence/source-manifest.sha256).
- Xử lý/đề xuất: future storage resolver must still map opaque IDs to scoped storage; that integration remains untested.

### C06 — Tài liệu và bản nhìn

- Nguồn/tiêu chí: [RULES C06](../../../RULES.md); roadmap Markdown/HTML policy.
- Bắt buộc: có.
- Điều kiện/môi trường: read-only; no roadmap status change or render.
- Bước/lệnh: compare current checklist and report; renderer not run.
- Kỳ vọng: no status changes; docs/HTML consistency validated within authorized scope.
- Thực tế: roadmap/status unchanged; Markdown/HTML were already dirty; no HTML consistency check run.
- Kết quả phản biện: none.
- Tag: need-change
- Kết quả: blocked
- Mức độ: minor
- Evidence: [checklist](../../../phases/phase-15.md); worktree status reviewed.
- Xử lý/đề xuất: authorized documentation pipeline can verify sync later; no status edit in this review.

### C07 — Regression liên quan

- Nguồn/tiêu chí: [RULES C07](../../../RULES.md); Phase 15 contract suite.
- Bắt buộc: có.
- Điều kiện/môi trường: safe focused unit suite only.
- Bước/lệnh: `rtk proxy uv run --project apps/api pytest apps/api/tests/test_phase15_memory_contracts.py -q`.
- Kỳ vọng: focused regressions pass; note integration limits.
- Thực tế: 8 passed, exit 0; suite still does not cover trusted ACL service, persistence, next-run resolver, redaction or resume.
- Kết quả phản biện: accepted for the locator validation fix.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [test output](evidence/test-output.txt).
- Xử lý/đề xuất: add integration proofs when dependencies exist.

### C08 — Có thể tái kiểm định

- Nguồn/tiêu chí: [RULES C08](../../../RULES.md); [report template](../../../templates/report.md).
- Bắt buộc: có.
- Điều kiện/môi trường: case blocks, source hashes, command logs, local links.
- Bước/lệnh: verify all IDs/tags, relative links and `phase_test_report` parser.
- Kỳ vọng: all criteria independently addressable and evidence reproducible.
- Thực tế: 14 individual cases; current source manifest; focused and canary output; remake/supersedes link.
- Kết quả phản biện: none.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: report, [manifest](evidence/source-manifest.sha256), [renderer parse/link check](evidence/report-structure-check.txt).
- Xử lý/đề xuất: no additional action.

### P15-01 — Context năm lớp

- Nguồn/tiêu chí: [checklist P15-01](../../../phases/phase-15.md); AC3.
- Bắt buộc: có.
- Điều kiện/môi trường: contract suite and locator canary; no real context builder.
- Bước/lệnh: focused tests `test_five_context_layers_require_their_own_scope_keys`, `test_context_manifest_is_explicit_bounded_and_deterministic_for_same_selection`; direct locator matrix.
- Kỳ vọng: five scopes exact; context is ACL/budget bounded; only safe namespaced refs; no unnecessary chat history.
- Thực tế: scope/manifest budget/hash tests pass and path-shaped refs now reject. No real builder proves actual selected bytes, source versions or omission of full chat history.
- Kết quả phản biện: accepted for path-shaped locator sub-finding; whole criterion remains incomplete.
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Evidence: [test output](evidence/test-output.txt); [source manifest](evidence/source-manifest.sha256).
- Xử lý/đề xuất: retain locator validator and add builder/transport integration evidence when implemented.

### P15-02 — Retrieval/promotion scope

- Nguồn/tiêu chí: [checklist P15-02](../../../phases/phase-15.md); AC1.
- Bắt buộc: có.
- Điều kiện/môi trường: trusted caller supplies ACL; no service/DB layer.
- Bước/lệnh: focused tests for unauthorized refs, cross-company, layer, retrieval exact version.
- Kỳ vọng: backend denies unauthorized read and write across company/environment/ACL.
- Thực tế: pure contract denies missing authorized ref and wrong scope; trusted ACL backend/storage enforcement was not present or run.
- Kết quả phản biện: none.
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Evidence: [test output](evidence/test-output.txt); memory contract source.
- Xử lý/đề xuất: integrate trusted backend ACL on retrieval and promotion.

### P15-03 — Promotion có proof

- Nguồn/tiêu chí: [checklist P15-03](../../../phases/phase-15.md); reviewer/Owner and proof contract.
- Bắt buộc: có.
- Điều kiện/môi trường: pure promotion helpers; reviewer grant is a ref only.
- Bước/lệnh: focused promotion tests.
- Kỳ vọng: proposal hash, evidence, scope, expiry, valid reviewer/Owner authority and immutable audit before new version.
- Thực tế: contract tests verify payload/scope/role/grant-ref presence and no policy change; no grant validation, Owner authorization, durable audit or real promotion inbox.
- Kết quả phản biện: none.
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Evidence: [test output](evidence/test-output.txt); memory source.
- Xử lý/đề xuất: add valid grant/Owner backend checks and append-only persistence.

### P15-04 — Version/rollback/expiry

- Nguồn/tiêu chí: [checklist P15-04](../../../phases/phase-15.md); AC2.
- Bắt buộc: có.
- Điều kiện/môi trường: immutable model/helper tests only; no durable store or run pins.
- Bước/lệnh: focused rollback/expiry/retrieval tests.
- Kỳ vọng: rollback appends without mutating old history; expiry and run-specific exact version enforced.
- Thực tế: pure rollback appends a new version and retrieval helper checks scope/version/expiry; no persistence, old/new run snapshot or rollback authorization evidence.
- Kết quả phản biện: none.
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Evidence: [test output](evidence/test-output.txt); source manifest.
- Xử lý/đề xuất: integrate version persistence, Owner review and run snapshot pinning.

### P15-05 — Untrusted context

- Nguồn/tiêu chí: [checklist P15-05](../../../phases/phase-15.md); AC3.
- Bắt buộc: có.
- Điều kiện/môi trường: proposal policy field tests only; no injected content/context pipeline.
- Bước/lệnh: focused negative policy-change assertion.
- Kỳ vọng: untrusted content cannot become policy or expand model/tool permissions.
- Thực tế: policy-change request field is constrained/rejected; no adversarial context ingestion, policy diff or permission path exists in tested slice.
- Kết quả phản biện: none.
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Evidence: [test output](evidence/test-output.txt); memory source.
- Xử lý/đề xuất: prove injection denial and zero permission delta in isolated integration fixtures.

### P15-06 — Redaction/retention/resume

- Nguồn/tiêu chí: [checklist P15-06](../../../phases/phase-15.md); retention/resume requirements.
- Bắt buộc: có.
- Điều kiện/môi trường: no storage/redaction/resume integration.
- Bước/lệnh: source review and focused unit suite only.
- Kỳ vọng: raw sensitive history not leaked/persisted; hashes/provenance retained; incomplete resume asks for missing input.
- Thực tế: manifest has hash/ref/byte count fields; no actual redaction, retention, transcript handling or resume state tested.
- Kết quả phản biện: none.
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Evidence: [source](../../../../../apps/api/src/agent_corporation_api/modules/memory/contracts.py); [test output](evidence/test-output.txt).
- Xử lý/đề xuất: implement and test canary redaction/retention/resume paths after storage/context integration.

## Integration / release gates

| Gate áp dụng | PASS / FAIL / BLOCKED | Test IDs | Batch/grant/config/evidence và gate trước |
| --- | --- | --- | --- |
| Phase 15: không có IG riêng | BLOCKED | C03, C06, P15-01…P15-06 | Locator boundary fix verified; Phase 14 unaccepted; trusted ACL/persistence/context builder/retrieval/promotion/rollback/run snapshot/redaction/resume integration absent; grant 0. |

## Cleanup, giới hạn và bàn giao

- Cleanup: synthetic strings/UUIDs only; no persistent resources.
- Chưa kiểm chứng: C03/C06 and P15-01…06 end-to-end due missing Phase 14 acceptance, trusted ACL service, persistence, builder, retrieval, approval/audit, run snapshots, rollback/expiry enforcement, redaction/retention/resume.
- Cần sửa: no reproduced locator-validation defect; P15-01 still `need-change/blocked` for missing builder evidence, not a locator bug.
- Đề xuất tùy chọn: none.
- Blocker summary: Phase 14 unaccepted; trusted ACL/persistence/context builder/retrieval/promotion/rollback and resume integrations absent; inference grant = 0.
- Bước tiếp theo: locator sub-finding verified and closed; continue Phase 15 only after dependent integrations and authorization are available.
- Bàn giao: independent r002 snapshot supersedes r001; confirms safe locator validation but does not assert phase acceptance or status change.
