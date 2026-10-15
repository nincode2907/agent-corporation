# Kiểm định Phase 15 — 20261015T094220+0700-r001-test

## Thông tin batch

- Phase: 15
- Test batch: 20261015T094220+0700-r001-test
- Vòng: r001
- Bắt đầu / kết thúc: 2026-10-15 09:42:20–09:42:28 +07:00 (Asia/Ho_Chi_Minh)
- Người/AI kiểm định: `/root/phase11_independent_test`
- Độc lập với AI triển khai/remake: kiểm định độc lập theo giao việc của `/root`; không có thông tin agent triển khai cụ thể.
- Yêu cầu/phạm vi được giao: review/test contract Phase 14–15; riêng batch này đánh giá Phase 15 hiện tại; không sửa source, không DB/migration/runtime/inference.
- Source: dirty worktree, không có commit snapshot; Phase 15 manifest/hash tại [source manifest](evidence/source-manifest.sha256).
- Môi trường/config/tool versions: Python project `apps/api`; pytest qua `uv run`; synthetic contract call với dữ liệu giả; không đọc `.env`/secret.
- Inference: không gọi; grant = 0.
- Dependency/quyết định nghiệm thu: Phase 14 chưa nghiệm thu; roadmap Phase 15 `Chưa triển khai`; Owner acceptance/grant không có.
- Supersedes: không có, vòng đầu.
- Remake nguồn: không có, vòng đầu.
- Kết luận kỹ thuật: **cần sửa**.
- Quyết định Chủ tịch: Chưa có.

## Mapping và phạm vi kiểm định

| Tiêu chí hiện tại / nguồn | Test IDs | Bắt buộc / tùy điều kiện | Ghi chú |
| --- | --- | --- | --- |
| C01–C08 theo [RULES §5](../../../RULES.md) | C01–C08 | Bắt buộc | Scope, dependency, demo, dispatch, data boundary, docs, regression, reproducibility. |
| AC1: Retrieval/promotion cùng kiểm company/environment/ACL ở backend | P15-01, P15-02 | Bắt buộc | Contract pure nhận ACL từ caller; chưa có service backend/storage. |
| AC2: run snapshot truy nguồn/version, rollback giữ history | P15-03, P15-04 | Bắt buộc | Pure contract có immutable version/append rollback; snapshot persistence thiếu. |
| AC3: không nhồi history, untrusted data không đổi quyền | P15-01, P15-05, P15-06 | Bắt buộc | Không có context builder/retrieval/resume/redaction path thực. |
| Demo reviewer promotion → next run đúng version; cross-department deny | P15-02, P15-03, P15-04 | Bắt buộc | Chưa có end-to-end demo, dependency Phase 14 chưa accepted. |

## Tổng hợp

| Tag | Số test |
| --- | ---: |
| clean | 5 |
| need-change | 9 |
| suggestion | 0 |

| Result | Số test |
| --- | ---: |
| pass | 5 |
| fail | 2 |
| blocked | 7 |
| not-run | 0 |
| not-applicable | 0 |

## Kết quả từng test

### C01 — Phạm vi và diff

- Nguồn/tiêu chí: [RULES C01](../../../RULES.md); Phase 15 source/test files trong manifest.
- Bắt buộc: có.
- Điều kiện/môi trường: dirty worktree; chỉ đọc source/tests.
- Bước/lệnh: `rtk git status --short`; đọc module, test và docs Phase 15.
- Kỳ vọng: review đúng scope Phase 15, giữ thay đổi người dùng.
- Thực tế: chỉ Phase 15 contract/test reviewed; không sửa source.
- Kết quả phản biện: none.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [manifest](evidence/source-manifest.sha256).
- Xử lý/đề xuất: không có.

### C02 — Dependency và nguồn quyết định

- Nguồn/tiêu chí: [Phase 15 roadmap](../../../../master-plan.md#phase-15--context-và-trí-nhớ-có-kiểm-chứng), checklist, Spec REQ17/ADR.
- Bắt buộc: có.
- Điều kiện/môi trường: đọc roadmap/checklist/spec; không tự nghiệm thu.
- Bước/lệnh: source review.
- Kỳ vọng: dependency Phase 14, status và grant được báo chính xác.
- Thực tế: dependency Phase 14 chưa được nghiệm thu; Phase 15 đang `Chưa triển khai`; không có Owner acceptance hoặc inference grant.
- Kết quả phản biện: none.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [checklist](../../../phases/phase-15.md); [roadmap](../../../../master-plan.md).
- Xử lý/đề xuất: duy trì blockers ở dưới.

### C03 — Đủ criteria và demo

- Nguồn/tiêu chí: [Phase 15 AC/demo](../../../../master-plan.md#phase-15--context-và-trí-nhớ-có-kiểm-chứng), P15-01…06.
- Bắt buộc: có.
- Điều kiện/môi trường: contract-only; không có Owner authorization, persistence, context builder hoặc worker runtime.
- Bước/lệnh: focused pytest; đối chiếu checklist evidence/demo.
- Kỳ vọng: verified context, reviewer promotion, next-run selected version, cross-department denial, rollback/retention/resume evidence.
- Thực tế: 14 contract tests pass; không có end-to-end demo, persisted manifest/memory, retrieval/resume state hay actual redaction evidence.
- Kết quả phản biện: none.
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Evidence: [focused test output](evidence/test-output.txt); [checklist](../../../phases/phase-15.md).
- Xử lý/đề xuất: cần dependency Phase 14 được chấp nhận và integration/evidence path trong scope.

### C04 — Không thực thi âm thầm

- Nguồn/tiêu chí: [RULES C04](../../../RULES.md); memory module docstring.
- Bắt buộc: có.
- Điều kiện/môi trường: pure contract source/tests; không runtime/model/tool dispatch.
- Bước/lệnh: review module; focused suite.
- Kỳ vọng: context/promotion helpers không tự truy cập nguồn ngoài, persist hay dispatch.
- Thực tế: module docstring explicitly says trusted caller provides ACL and module does not persist, retrieve or grant authority; no dispatch path in reviewed source.
- Kết quả phản biện: none.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [source](../../../../../apps/api/src/agent_corporation_api/modules/memory/contracts.py); [test output](evidence/test-output.txt).
- Xử lý/đề xuất: real retrieval/promotion remain blocked separately.

### C05 — Scope và dữ liệu nhạy cảm

- Nguồn/tiêu chí: [RULES C05](../../../RULES.md); Phase 15 path/ACL boundary and content provenance.
- Bắt buộc: có.
- Điều kiện/môi trường: synthetic identifier only; no real files/secrets touched.
- Bước/lệnh: instantiate `ContextSource` with `content_ref="../../outside"`; source review.
- Kỳ vọng: content locator cannot smuggle a path traversal string into a manifest; external resolver must receive an opaque ref.
- Thực tế: `ContextSource.content_ref` accepts `../../outside` (min/max length only) and `build_context_manifest` serializes it. No dereference was attempted, so traversal is not proven; however the contract fails to enforce its opaque locator boundary and downstream path resolution could escape scope.
- Kết quả phản biện: none.
- Tag: need-change
- Kết quả: fail
- Mức độ: major
- Evidence: [reproduction](evidence/test-output.txt); [source](../../../../../apps/api/src/agent_corporation_api/modules/memory/contracts.py).
- Xử lý/đề xuất: enforce opaque locator grammar at `ContextSource` construction and test traversal-shaped values; make any eventual resolver map opaque IDs to scoped storage rather than filesystem paths.

### C06 — Tài liệu và bản nhìn

- Nguồn/tiêu chí: [RULES C06](../../../RULES.md); roadmap Markdown/HTML policy.
- Bắt buộc: có.
- Điều kiện/môi trường: read-only review; không render roadmap vì không đổi phase status.
- Bước/lệnh: đối chiếu Phase 15 Markdown/checklist/report; không chạy renderer.
- Kỳ vọng: report không tự nâng status; Markdown/HTML sync được kiểm chứng khi cần.
- Thực tế: không sửa roadmap/HTML hay render; source worktree đã dirty ở cả hai files; HTML consistency chưa được verified trong batch này.
- Kết quả phản biện: none.
- Tag: need-change
- Kết quả: blocked
- Mức độ: minor
- Evidence: [checklist](../../../phases/phase-15.md); `git status --short` reviewed in-session.
- Xử lý/đề xuất: docs pipeline/authorized renderer can verify consistency after reports/remakes; no status change in this test.

### C07 — Regression liên quan

- Nguồn/tiêu chí: [RULES C07](../../../RULES.md); Phase 15 contract tests and adjacent Phase 14 contracts.
- Bắt buộc: có.
- Điều kiện/môi trường: exact safe focused command; no DB/runtime.
- Bước/lệnh: `rtk proxy uv run --project apps/api pytest apps/api/tests/test_phase14_hr_contracts.py apps/api/tests/test_phase15_memory_contracts.py -q`.
- Kỳ vọng: focused regression result recorded with scope limits.
- Thực tế: 14 passed; exit 0. This does not cover persistence, actual retrieval/resume, Owner grant authority, or the path-like content locator canary absent from the suite.
- Kết quả phản biện: none.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [test output](evidence/test-output.txt).
- Xử lý/đề xuất: add the content_ref negative canary in remake; rerun after source changes.

### C08 — Có thể tái kiểm định

- Nguồn/tiêu chí: [RULES C08](../../../RULES.md); [report template](../../../templates/report.md).
- Bắt buộc: có.
- Điều kiện/môi trường: canonical report blocks, hashes and evidence.
- Bước/lệnh: check report IDs/tags, manifest and command output.
- Kỳ vọng: all C/P cases individually tagged; fresh hashes/expected/actual/evidence.
- Thực tế: 14 individually tagged cases, current source/docs hashes and exact commands saved; relative links target local batch/source docs.
- Kết quả phản biện: none.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: report, [manifest](evidence/source-manifest.sha256), [renderer parse/link check](evidence/report-structure-check.txt).
- Xử lý/đề xuất: automated link check not run.

### P15-01 — Context năm lớp

- Nguồn/tiêu chí: [checklist P15-01](../../../phases/phase-15.md); roadmap AC3.
- Bắt buộc: có.
- Điều kiện/môi trường: synthetic contract tests; no content resolver/context builder.
- Bước/lệnh: focused pytest `test_five_context_layers_require_their_own_scope_keys`, `test_context_manifest_is_explicit_bounded_and_deterministic_for_same_selection`; synthetic locator check.
- Kỳ vọng: five scopes exact; ACL/budget/provenance bounded; locators safe and context selection excludes unneeded history.
- Thực tế: scope, manifest hashing and declared byte budgets pass; `ContextSource.content_ref="../../outside"` is accepted, and no actual context builder proves selected content corresponds to bounded bytes or excludes chat history.
- Kết quả phản biện: none.
- Tag: need-change
- Kết quả: fail
- Mức độ: major
- Evidence: [test output](evidence/test-output.txt); [source](../../../../../apps/api/src/agent_corporation_api/modules/memory/contracts.py).
- Xử lý/đề xuất: fix opaque locator validation and add path traversal negative test; context builder/transport cap remains blocked integration work.

### P15-02 — Retrieval/promotion scope

- Nguồn/tiêu chí: [checklist P15-02](../../../phases/phase-15.md); roadmap AC1.
- Bắt buộc: có.
- Điều kiện/môi trường: ACL is a trusted caller supplied `authorized_refs`; no service/backend or DB.
- Bước/lệnh: focused pytest `test_context_selection_denies_unapproved_refs_cross_company_and_unallowed_layer`, retrieval version test.
- Kỳ vọng: backend denies wrong company/environment and unauthorized refs on both read/write.
- Thực tế: pure builder rejects missing ACL refs and cross-company scope; `memory_is_retrievable` checks exact scope/version/expiry. Caller is the trust boundary, no backend enforcement/storage was tested.
- Kết quả phản biện: none.
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Evidence: [test output](evidence/test-output.txt); module source.
- Xử lý/đề xuất: integrate trusted backend ACL for retrieval and promotion; cross-department runtime denial/demo remains blocked.

### P15-03 — Promotion có proof

- Nguồn/tiêu chí: [checklist P15-03](../../../phases/phase-15.md); proposal → review → version flow.
- Bắt buộc: có.
- Điều kiện/môi trường: pure proposal/decision tests; reviewer grant is a supplied ref; no Owner auth or durable audit.
- Bước/lệnh: focused pytest `test_promotion_requires_evidence_review_scope_and_never_accepts_policy_changes`, `test_rejected_expired_or_cross_scope_memory_proposal_cannot_promote`.
- Kỳ vọng: payload hash, evidence refs, scope, expiry, role and grant gates; no agent assertion becomes policy.
- Thực tế: contract tests verify hash/scope/role/grant-ref presence, rejection and no policy-change field. They do not prove the grant is valid/current, Owner identity, audit persistence or post-review run context.
- Kết quả phản biện: none.
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Evidence: [test output](evidence/test-output.txt); [source](../../../../../apps/api/src/agent_corporation_api/modules/memory/contracts.py).
- Xử lý/đề xuất: integrate verified reviewer/Owner authorization, grant checks and append-only audit store before promotion can be accepted.

### P15-04 — Version/rollback/expiry

- Nguồn/tiêu chí: [checklist P15-04](../../../phases/phase-15.md); roadmap AC2.
- Bắt buộc: có.
- Điều kiện/môi trường: in-memory immutable model/helper tests; no persisted snapshots or next-run retrieval.
- Bước/lệnh: focused pytest `test_rollback_appends_a_new_version_and_does_not_mutate_prior_versions`, expiry/retrieval tests.
- Kỳ vọng: rollback appends version, preserves prior versions, expires correctly; old run pins remain resolvable.
- Thực tế: helper appends version 3 from versions 1/2 and preserves input objects; retrieval helper enforces exact version and expiry. Persistence, old/new run snapshot identity and rollback authorization are unverified.
- Kết quả phản biện: none.
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Evidence: [test output](evidence/test-output.txt); source manifest.
- Xử lý/đề xuất: durable version store, rollback Owner/reviewer gate and run snapshot integration are required.

### P15-05 — Untrusted context

- Nguồn/tiêu chí: [checklist P15-05](../../../phases/phase-15.md); roadmap AC3.
- Bắt buộc: có.
- Điều kiện/môi trường: static proposal field/contract tests only; no injected document/context runtime.
- Bước/lệnh: focused pytest policy-change negative case.
- Kỳ vọng: prompt injection/untrusted text cannot become policy or increase model/tool permissions.
- Thực tế: `requested_policy_change=True` is rejected and the proposal cannot encode policy change; no adversarial source ingestion, policy diff or tool/model authorization path exists in reviewed scope.
- Kết quả phản biện: none.
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Evidence: [test output](evidence/test-output.txt); memory contract source.
- Xử lý/đề xuất: retain untrusted provenance through real context assembly and prove denied promotion/no permission delta with isolated fixtures.

### P15-06 — Redaction/retention/resume

- Nguồn/tiêu chí: [checklist P15-06](../../../phases/phase-15.md); roadmap context retention/resume constraints.
- Bắt buộc: có.
- Điều kiện/môi trường: no storage, redaction, transcript, or resume integration in current module.
- Bước/lệnh: source review and focused contract tests only.
- Kỳ vọng: raw sensitive history is not leaked/persisted; manifest preserves hashes/provenance; incomplete resume requires input instead of inventing state.
- Thực tế: manifest carries content hash/ref/byte count, but no redaction/retention/resume behavior is implemented or exercised. Locator-path defect also needs fixing before any resolver is added.
- Kết quả phản biện: none.
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Evidence: [source](../../../../../apps/api/src/agent_corporation_api/modules/memory/contracts.py); [test output](evidence/test-output.txt).
- Xử lý/đề xuất: add integration-specific canary redaction/retention/resume proofs; require opaque scoped locator as a prerequisite.

## Integration / release gates

| Gate áp dụng | PASS / FAIL / BLOCKED | Test IDs | Batch/grant/config/evidence và gate trước |
| --- | --- | --- | --- |
| Phase 15: không có IG riêng | BLOCKED | C03, P15-02…P15-06 | Contract foundation only; Phase 14 unaccepted; no trusted ACL persistence/context builder/retrieval/promotion/rollback/resume integration; inference grant 0. P15-01/C05 path-shaped locator finding is independently fail. |

## Cleanup, giới hạn và bàn giao

- Cleanup: chỉ synthetic UUID/string fixtures, không tạo tài nguyên persistent.
- Chưa kiểm chứng: C03/C06, P15-02…06 vì dependency Phase 14 chưa accepted và trusted ACL, persistence, context builder, retrieval, valid promotion grant, run snapshot, rollback authorization, redaction/retention/resume integration chưa có.
- Cần sửa: C05/P15-01 major — `ContextSource.content_ref` accepts traversal-shaped value. No dereference/escape was attempted; source defect is the missing opaque locator constraint.
- Đề xuất tùy chọn: none.
- Blocker summary: Phase 14 acceptance; Owner/reviewer authorization and valid grant integration; ACL/persistence/context selection/retrieval/promotion store; run snapshots/rollback; prompt injection, redaction, retention and resume paths; inference grant = 0.
- Bước tiếp theo: remake locator validation and add negative regression; retest on new frozen source. Separately keep all runtime criteria blocked until their dependencies and authorization exist.
- Bàn giao: report/evidence is a technical test snapshot only; no Owner acceptance and no phase status change.
