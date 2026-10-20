# Kiểm định Phase 08 — 20261019T102129+0700-r007-test

## Thông tin batch

- Phase: 08
- Vòng: r007
- Test batch: `20261019T102129+0700-r007-test`
- Bắt đầu / kết thúc: 2026-10-19T10:21:29+07:00 / 2026-10-19T10:53:54+07:00
- Người/AI kiểm định: Codex `/root`; kiểm định độc lập `/root/stabilization03_independent`
- Phạm vi: Owner UX, snapshot projection and Replay recovery regressions, Phase 08 readiness; không thực hiện live demo.
- Source commit: `6c7f7bd`; working tree dirty. Các thay đổi Docker một-compose đang có và UI Lens artifacts của người dùng được giữ nguyên.
- Evidence source: [source manifest](evidence/source-manifest.json); [commands, runtime facts and screenshots](../../../../../docs/reviews/stabilization-03/evidence/commands.md); [browser result](../../../../../docs/reviews/stabilization-03/evidence/browser-result.json); [independent addendum](independent-addendum.md).
- Inference/grant: không gọi inference, không tạo grant, không chạy live run.
- Dependency: Phase 07 giữ Bị chặn; Phase 08 và IG08 giữ **Bị chặn**.
- Supersedes: [Phase 08 r006](../20261018T232151+0700-r006-test/report.md). Remake nguồn: không có.
- Kết luận kỹ thuật: **chưa đủ bằng chứng**. Read projection, auth navigation and fixture recovery đạt; active-run correlation, full Replay side-effect audit, browser negative scope tests and IG08 remain open.
- Quyết định Chủ tịch: chưa có.

## Mapping criteria

| Tiêu chí / nguồn | Test IDs | Bắt buộc | Phạm vi |
| --- | --- | --- | --- |
| Roadmap Phase 08 AC1: UI evidence originates from real run; fixture clearly labeled | P08-01, P08-02, P08-06 | có | Current browser recovery is synthetic; live active run not authorized |
| Roadmap Phase 08 AC2: Replay is read-only and scoped | P08-03, P08-04 | có | Snapshot read-only API and browser GET fixture; artifact negative browser checks missing |
| Roadmap Phase 08 AC3: explicit summaries do not expose hidden reasoning | P08-05 | có | Redacted public event projection and UI summary source reviewed |
| Checklist Phase 08 C01–C08 | C01–C08 | có | Scope, dependency, demo, side effects, privacy, docs, regression, evidence |

## Tổng hợp

| Tag | Số test | Result | Số test |
| --- | ---: | --- | ---: |
| clean | 8 | pass | 8 |
| need-change | 7 | fail | 0 |
| suggestion | 0 | blocked | 7 |
|  |  | not-run | 0 |
|  |  | not-applicable | 0 |

`need-change + blocked` denotes mandatory criteria without sufficient evidence, not a confirmed product defect.

## Kết quả từng test

### C01 — Giữ đúng task scope và các dirty changes khác

- Nguồn/tiêu chí: [C01–C08 trong RULES.md §5](../../../../tests/RULES.md)
- Bắt buộc: có
- Điều kiện/môi trường: isolated PostgreSQL suite và/hoặc Owner-authenticated browser; không inference, không grant.
- Bước/lệnh: xem [commands/evidence](../../../../../docs/reviews/stabilization-03/evidence/commands.md); kết quả ghi tại [batch evidence](evidence/source-manifest.json).
- Kỳ vọng: Giữ đúng task scope và các dirty changes khác
- Thực tế: Snapshot/recovery scope implemented; unrelated Docker changes and user UI Lens artifacts preserved; hashes recorded
- Kết quả phản biện: none
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [manifest](evidence/source-manifest.json); no commit/push
- Xử lý/đề xuất: no commit/push

### C02 — Dependency, contract and current roadmap reconciled

- Nguồn/tiêu chí: [C01–C08 trong RULES.md §5](../../../../tests/RULES.md)
- Bắt buộc: có
- Điều kiện/môi trường: isolated PostgreSQL suite và/hoặc Owner-authenticated browser; không inference, không grant.
- Bước/lệnh: xem [commands/evidence](../../../../../docs/reviews/stabilization-03/evidence/commands.md); kết quả ghi tại [batch evidence](evidence/source-manifest.json).
- Kỳ vọng: Dependency, contract and current roadmap reconciled
- Thực tế: ADR-0004, product spec §9 and Phase 08 checklist agree; Phase 07 dependency and IG08 live-run requirement remain
- Kết quả phản biện: none
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [ADR-0004](../../../../../docs/decisions/0004-scoped-observability-snapshot.md), [plan](../../../../../docs/master-plan.md)
- Xử lý/đề xuất: Không cần sửa; giữ blocker và status theo báo cáo.

### C03 — All acceptance criteria mapped to appropriate demo

- Nguồn/tiêu chí: [C01–C08 trong RULES.md §5](../../../../tests/RULES.md)
- Bắt buộc: có
- Điều kiện/môi trường: isolated PostgreSQL suite và/hoặc Owner-authenticated browser; không inference, không grant.
- Bước/lệnh: xem [commands/evidence](../../../../../docs/reviews/stabilization-03/evidence/commands.md); kết quả ghi tại [batch evidence](evidence/source-manifest.json).
- Kỳ vọng: All acceptance criteria mapped to appropriate demo
- Thực tế: Fixture UI recovery is labeled and useful, but no authorized real run exists for Office/Inspector correlation
- Kết quả phản biện: none
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Evidence: P08-01, P08-02, P08-07; Owner grant required
- Xử lý/đề xuất: Owner grant required

### C04 — Page/readiness/replay never dispatches tools or inference

- Nguồn/tiêu chí: [C01–C08 trong RULES.md §5](../../../../tests/RULES.md)
- Bắt buộc: có
- Điều kiện/môi trường: isolated PostgreSQL suite và/hoặc Owner-authenticated browser; không inference, không grant.
- Bước/lệnh: xem [commands/evidence](../../../../../docs/reviews/stabilization-03/evidence/commands.md); kết quả ghi tại [batch evidence](evidence/source-manifest.json).
- Kỳ vọng: Page/readiness/replay never dispatches tools or inference
- Thực tế: Runtime read-only counters before/after show no active calls/turns; browser requests contained no business writes beyond Owner login/logout; no model/tool routes were requested
- Kết quả phản biện: none
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [commands](../../../../../docs/reviews/stabilization-03/evidence/commands.md), [browser result](../../../../../docs/reviews/stabilization-03/evidence/browser-result.json)
- Xử lý/đề xuất: Không cần sửa; giữ blocker và status theo báo cáo.

### C05 — Scope and sensitive information boundaries hold

- Nguồn/tiêu chí: [C01–C08 trong RULES.md §5](../../../../tests/RULES.md)
- Bắt buộc: có
- Điều kiện/môi trường: isolated PostgreSQL suite và/hoặc Owner-authenticated browser; không inference, không grant.
- Bước/lệnh: xem [commands/evidence](../../../../../docs/reviews/stabilization-03/evidence/commands.md); kết quả ghi tại [batch evidence](evidence/source-manifest.json).
- Kỳ vọng: Scope and sensitive information boundaries hold
- Thực tế: Snapshot RLS/scope tests pass on disposable DB; browser uses real Owner session but records no credential/session data; historical text/IDs blurred
- Kết quả phản biện: none
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: `test_stabilization03_snapshot.py`; [sanitized evidence](../../../../../docs/reviews/stabilization-03/evidence/commands.md)
- Xử lý/đề xuất: [sanitized evidence](../../../../../docs/reviews/stabilization-03/evidence/commands.md)

### C06 — Documentation/view matches evidence without phase-status change

- Nguồn/tiêu chí: [C01–C08 trong RULES.md §5](../../../../tests/RULES.md)
- Bắt buộc: có
- Điều kiện/môi trường: isolated PostgreSQL suite và/hoặc Owner-authenticated browser; không inference, không grant.
- Bước/lệnh: xem [commands/evidence](../../../../../docs/reviews/stabilization-03/evidence/commands.md); kết quả ghi tại [batch evidence](evidence/source-manifest.json).
- Kỳ vọng: Documentation/view matches evidence without phase-status change
- Thực tế: Markdown plan updated and HTML rendered; Phase 08 remains Bị chặn; no acceptance text added
- Kết quả phản biện: none
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [master plan](../../../../../docs/master-plan.md), [roadmap HTML](../../../../../docs/master-plan.html)
- Xử lý/đề xuất: Không cần sửa; giữ blocker và status theo báo cáo.

### C07 — Changed API/UI dependency regressions are covered

- Nguồn/tiêu chí: [C01–C08 trong RULES.md §5](../../../../tests/RULES.md)
- Bắt buộc: có
- Điều kiện/môi trường: isolated PostgreSQL suite và/hoặc Owner-authenticated browser; không inference, không grant.
- Bước/lệnh: xem [commands/evidence](../../../../../docs/reviews/stabilization-03/evidence/commands.md); kết quả ghi tại [batch evidence](evidence/source-manifest.json).
- Kỳ vọng: Changed API/UI dependency regressions are covered
- Thực tế: Isolated API suite 244 passed/3 skipped/1 warning; web build and authenticated browser recovery pass
- Kết quả phản biện: none
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [commands](../../../../../docs/reviews/stabilization-03/evidence/commands.md)
- Xử lý/đề xuất: Không cần sửa; giữ blocker và status theo báo cáo.

### C08 — Evidence is reproducible and appropriately limited

- Nguồn/tiêu chí: [C01–C08 trong RULES.md §5](../../../../tests/RULES.md)
- Bắt buộc: có
- Điều kiện/môi trường: isolated PostgreSQL suite và/hoặc Owner-authenticated browser; không inference, không grant.
- Bước/lệnh: xem [commands/evidence](../../../../../docs/reviews/stabilization-03/evidence/commands.md); kết quả ghi tại [batch evidence](evidence/source-manifest.json).
- Kỳ vọng: Evidence is reproducible and appropriately limited
- Thực tế: Hash manifest, dual test reports, browser metadata and 14 redacted captures; explicit fixture/live distinction
- Kết quả phản biện: none
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [batch manifest](evidence/source-manifest.json), [screenshot inventory](../../../../../docs/reviews/stabilization-03/evidence/commands.md)
- Xử lý/đề xuất: Không cần sửa; giữ blocker và status theo báo cáo.

### P08-01 — Office derives employee/run status from a real authorized run

- Nguồn/tiêu chí: [checklist phase-08.md](../../../phases/phase-08.md)
- Bắt buộc: có
- Điều kiện/môi trường: isolated PostgreSQL suite và/hoặc Owner-authenticated browser; không inference, không grant.
- Bước/lệnh: xem [commands/evidence](../../../../../docs/reviews/stabilization-03/evidence/commands.md); kết quả ghi tại [batch evidence](evidence/source-manifest.json).
- Kỳ vọng: Office derives employee/run status from a real authorized run
- Thực tế: Snapshot projects stored runs, but browser fixture has no active real run and no employee mapping
- Kết quả phản biện: none
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Evidence: [next actions](../../../../../docs/reviews/stabilization-03/next-actions.md); live run needs IG08 grant
- Xử lý/đề xuất: live run needs IG08 grant

### P08-02 — Dashboard/task/org open shared Inspector with consistent IDs, tabs and source

- Nguồn/tiêu chí: [checklist phase-08.md](../../../phases/phase-08.md)
- Bắt buộc: có
- Điều kiện/môi trường: isolated PostgreSQL suite và/hoặc Owner-authenticated browser; không inference, không grant.
- Bước/lệnh: xem [commands/evidence](../../../../../docs/reviews/stabilization-03/evidence/commands.md); kết quả ghi tại [batch evidence](evidence/source-manifest.json).
- Kỳ vọng: Dashboard/task/org open shared Inspector with consistent IDs, tabs and source
- Thực tế: Run projection limit and fields pass API integration tests; no real active run to correlate across entry points; artifact/tool source still unavailable
- Kết quả phản biện: none
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Evidence: Independent addendum; requires authorized active run and Inspector/API negative coverage
- Xử lý/đề xuất: requires authorized active run and Inspector/API negative coverage

### P08-03 — Replay cursor/filter/seek/reload is read-only with no DB mutation

- Nguồn/tiêu chí: [checklist phase-08.md](../../../phases/phase-08.md)
- Bắt buộc: có
- Điều kiện/môi trường: isolated PostgreSQL suite và/hoặc Owner-authenticated browser; không inference, không grant.
- Bước/lệnh: xem [commands/evidence](../../../../../docs/reviews/stabilization-03/evidence/commands.md); kết quả ghi tại [batch evidence](evidence/source-manifest.json).
- Kỳ vọng: Replay cursor/filter/seek/reload is read-only with no DB mutation
- Thực tế: New browser checks recovery/read and no business POST; isolated API checks snapshot read-only. This batch did not repeat full filter/seek and before/after DB table comparison
- Kết quả phản biện: none
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Evidence: Prior Sprint 02 result is historical only; rerun focused browser + metadata-only DB comparison
- Xử lý/đề xuất: rerun focused browser + metadata-only DB comparison

### P08-04 — Cross-company/environment access is denied and redaction enforced in browser/API

- Nguồn/tiêu chí: [checklist phase-08.md](../../../phases/phase-08.md)
- Bắt buộc: có
- Điều kiện/môi trường: isolated PostgreSQL suite và/hoặc Owner-authenticated browser; không inference, không grant.
- Bước/lệnh: xem [commands/evidence](../../../../../docs/reviews/stabilization-03/evidence/commands.md); kết quả ghi tại [batch evidence](evidence/source-manifest.json).
- Kỳ vọng: Cross-company/environment access is denied and redaction enforced in browser/API
- Thực tế: API scope/RLS/redaction integration checks pass; second-company browser Inspector/artifact retrieval test was not run
- Kết quả phản biện: none
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Evidence: Add disposable actor/company negative route coverage; do not use a real second Owner
- Xử lý/đề xuất: do not use a real second Owner

### P08-05 — Decision summary is explicit and does not expose hidden reasoning

- Nguồn/tiêu chí: [checklist phase-08.md](../../../phases/phase-08.md)
- Bắt buộc: có
- Điều kiện/môi trường: isolated PostgreSQL suite và/hoặc Owner-authenticated browser; không inference, không grant.
- Bước/lệnh: xem [commands/evidence](../../../../../docs/reviews/stabilization-03/evidence/commands.md); kết quả ghi tại [batch evidence](evidence/source-manifest.json).
- Kỳ vọng: Decision summary is explicit and does not expose hidden reasoning
- Thực tế: Inspector copy says no explicit summary is present; event payload passes existing public redaction; UI shows only permitted event summary and withheld state, not raw reasoning
- Kết quả phản biện: none
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: `eventSummary` in `RuntimePanel.tsx`, `public_event` in observability feed, screenshot [Inspector desktop](../../../../../docs/reviews/stabilization-03/evidence/screenshots/inspector-before-1440x900.png)
- Xử lý/đề xuất: Không cần sửa; giữ blocker và status theo báo cáo.

### P08-06 — Reconnect/error/usage states are accurate on the same persisted run

- Nguồn/tiêu chí: [checklist phase-08.md](../../../phases/phase-08.md)
- Bắt buộc: có
- Điều kiện/môi trường: isolated PostgreSQL suite và/hoặc Owner-authenticated browser; không inference, không grant.
- Bước/lệnh: xem [commands/evidence](../../../../../docs/reviews/stabilization-03/evidence/commands.md); kết quả ghi tại [batch evidence](evidence/source-manifest.json).
- Kỳ vọng: Reconnect/error/usage states are accurate on the same persisted run
- Thực tế: Fixture recovery shows historical gap, duplicate suppression and out-of-order recovery; real read-only SSE shows offline/stale/heartbeat recovery. There is no active run to test same-run usage provenance or unknown outcome display.
- Kết quả phản biện: none
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Evidence: [browser result](../../../../../docs/reviews/stabilization-03/evidence/browser-result.json); requires active run and interruption evidence
- Xử lý/đề xuất: requires active run and interruption evidence

### P08-07 — IG08 live text-only run reaches persisted event store, SSE, Office, Inspector and Replay

- Nguồn/tiêu chí: [checklist phase-08.md](../../../phases/phase-08.md)
- Bắt buộc: có
- Điều kiện/môi trường: isolated PostgreSQL suite và/hoặc Owner-authenticated browser; không inference, không grant.
- Bước/lệnh: xem [commands/evidence](../../../../../docs/reviews/stabilization-03/evidence/commands.md); kết quả ghi tại [batch evidence](evidence/source-manifest.json).
- Kỳ vọng: IG08 live text-only run reaches persisted event store, SSE, Office, Inspector and Replay
- Thực tế: Not run; no new Owner grant and the sprint explicitly prohibited inference
- Kết quả phản biện: none
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Evidence: IG08 stays **BLOCKED**; see [Owner-controlled procedure](../../../../../docs/reviews/stabilization-03/next-actions.md)
- Xử lý/đề xuất: see [Owner-controlled procedure](../../../../../docs/reviews/stabilization-03/next-actions.md)

## Integration gate

| Gate | Verdict | IDs | Evidence / required prerequisite |
| --- | --- | --- | --- |
| IG08 | **BLOCKED** | P08-01, P08-02, P08-06, P08-07 | No grant/live run in this batch. Owner must choose demo scope, profile/model, purpose, one request, concurrency 1, ≤120s, expiry, and CG01 mode before a fresh test batch. |

## Cleanup and handoff

- Disposable DB/role were cleaned by the isolated runner. Browser logged out the temporary Owner session. Runtime DB contains no model-call or Playground-turn rows after the test. No live run or usage was created.
- Seven mandatory criteria remain blocked: C03, P08-01, P08-02, P08-03, P08-04, P08-06 and P08-07.
- No confirmed failure requires a remake. IG08 cannot pass from snapshots or synthetic SSE fixtures. Phase 08 remains Bị chặn and awaits Owner authorization for a separate grant-bound batch.
