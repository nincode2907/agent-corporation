# Kiểm định Phase 06 — 20261008T170343+0700-r001-test

## Thông tin batch

- Phase: 06
- Test batch: 20261008T170343+0700-r001-test
- Vòng: r001
- Bắt đầu / kết thúc: 2026-10-08T17:03:43+07:00 / 2026-10-08T17:06:52+07:00
- Người/AI kiểm định: Codex
- Yêu cầu/phạm vi được giao: “làm lại test rồi tiếp phase 6”; sau Phase 05 r002, kiểm dependency Phase 06 trước implementation; chỉ tiến hành khi an toàn.
- Source: Dirty worktree, giữ các thay đổi Chủ tịch và remediation Phase 05. [Manifest](evidence/source-manifest.json) ghi hash nguồn liên quan.
- Môi trường/config/tool versions: local; API tests trong ASGI; codex-server 127.0.0.1:4000 offline; app API không restart; grant 0.
- Inference: Không gọi; không gửi inputs; grant riêng cho batch này = 0.
- Dependency/quyết định nghiệm thu: Phase 03 Hoàn tất; Phase 04 Chờ nghiệm thu; Phase 05 Chờ nghiệm thu, r002 chưa đủ bằng chứng. Dependency 05 và CG01 chưa đạt, nên Phase 06 bị chặn trước implementation.
- Supersedes: Không có; r001 của Phase 06.
- Remake nguồn: Không có.
- Kết luận kỹ thuật: chưa đủ bằng chứng
- Quyết định Chủ tịch: Chưa có nghiệm thu Phase 06; yêu cầu tiếp tục phase không cấp inference grant.

## Mapping nghiệm thu → test

| Tiêu chí hiện tại / nguồn | Test IDs | Bắt buộc / tùy điều kiện | Ghi chú |
| --- | --- | --- | --- |
| Phase 06 dependency 05 + nền 03 | C02, C03 | Bắt buộc | Phase 05 còn blocked; 03 có event/state baseline |
| Grant/default deny và isolation/input boundary | P06-01, P06-02 | Bắt buộc | Chưa có Owner/grant service; CG01 chưa đạt |
| Model turn, errors, limits, stop và usage | P06-03…P06-07 | Bắt buộc | Không test live khi grant 0; dispatcher chưa có |
| Persisted snapshot/history/checkpoint và idle | P06-08, C04 | Bắt buộc | Có nền run/checkpoint/events; chưa có profile/policy/model-call snapshot và dispatcher |
| Tài liệu, regression, evidence | C01, C05…C08 | Bắt buộc | Docs/HTML, no inference, API sanity tests, validator |

## Tổng hợp

| Tag | Số test |
| --- | ---: |
| clean | 7 |
| need-change | 9 |
| suggestion | 0 |

| Result | Số test |
| --- | ---: |
| pass | 7 |
| fail | 0 |
| blocked | 9 |
| not-run | 0 |
| not-applicable | 0 |

## Kết quả từng test

### C01 — Phạm vi và worktree

- Nguồn/tiêu chí: Yêu cầu chỉ retest Phase 05 rồi tiếp Phase 06; giữ thay đổi sẵn có.
- Bắt buộc: có
- Điều kiện/môi trường: Worktree dirty, nhiều report Phase 02–05 do Chủ tịch/agent khác đã tạo.
- Bước/lệnh: Kiểm `git status`, manifest và phạm vi thay đổi.
- Kỳ vọng: Không sửa lịch sử report; không restart shared services, không inference, không sang Phase 07.
- Thực tế: Giữ nguyên lịch sử; chỉ tạo preflight Phase 06 và cập nhật trạng thái/HTML Phase 06; grant 0.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [manifest](evidence/source-manifest.json), [commands](evidence/commands.md)
- Xử lý/đề xuất: Không.

### C02 — Dependency và nguồn quyết định

- Nguồn/tiêu chí: [Master plan](../../../../master-plan.md), [Phase 05 r002](../../phase-05/20261008T165952+0700-r002-test/report.md), [ADR D06/CG01](../../../../decisions/0001-v1-foundation.md).
- Bắt buộc: có
- Điều kiện/môi trường: Phase 04 pending; Phase 05 chưa đủ bằng chứng; grant 0.
- Bước/lệnh: Đối chiếu trạng thái và gate trước implementation.
- Kỳ vọng: Không xem phase dependency là hoàn tất chỉ vì được giao phase sau; ghi blocker chính xác.
- Thực tế: Phase 06 được đặt Bị chặn; Phase 04/05 còn chờ nghiệm thu, CG01 chưa đạt; không tự nghiệm thu.
- Tag: clean
- Kết quả: pass
- Mức độ: major
- Evidence: [blocked dependency](evidence/blocked-dependency.md), [Phase 05 report](../../phase-05/20261008T165952+0700-r002-test/report.md)
- Xử lý/đề xuất: Chờ quyết định/gate đã nêu trong evidence.

### C03 — Criteria và demo Phase 06

- Nguồn/tiêu chí: Phase 06 AC1–AC3 trong roadmap và [checklist](../../../../tests/phases/phase-06.md).
- Bắt buộc: có
- Điều kiện/môi trường: Dispatcher/model call chưa tồn tại; Phase 05/CG01/grant chưa đạt.
- Bước/lệnh: Map criteria vào P06-01…P06-08; kiểm API route và source.
- Kỳ vọng: Demo model thật chỉ sau grant/isolation; nếu gate thiếu thì không gửi input.
- Thực tế: Không có demo agent; dispatch dừng trước implementation theo prerequisite; AC1–AC3 chưa thể được nghiệm thu.
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Evidence: [blocked dependency](evidence/blocked-dependency.md), [checklist](../../../../tests/phases/phase-06.md)
- Xử lý/đề xuất: Tiếp tục sau khi các gate Phase 05/CG01 và điều kiện grant/auth được giải quyết.

### C04 — Không inference/dispatch âm thầm

- Nguồn/tiêu chí: Spec §§6,10; không tự chạy khi mở UI/health.
- Bắt buộc: có
- Điều kiện/môi trường: API source hiện tại, grant 0.
- Bước/lệnh: Đọc router registration và call path trong [main.py](../../../../../apps/api/src/agent_corporation_api/main.py) cùng [codex adapter](../../../../../apps/api/src/agent_corporation_api/modules/codex_gateway/adapter.py).
- Kỳ vọng: Health/UI không gửi chat/session/model request; chỉ có probe GET thủ công.
- Thực tế: Router đăng ký demo và gateway read-only; không có execution dispatcher hoặc chat POST route. Không có inference request trong batch.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [commands](evidence/commands.md), [manifest](evidence/source-manifest.json)
- Xử lý/đề xuất: Giữ default-deny trước khi thêm dispatch.

### C05 — Scope và dữ liệu nhạy cảm

- Nguồn/tiêu chí: Spec §6/CG01 và project boundaries.
- Bắt buộc: có
- Điều kiện/môi trường: Phase 05 gate chưa đạt; dữ liệu private/local.
- Bước/lệnh: Kiểm lệnh/evidence; không gọi endpoint inference.
- Kỳ vọng: Không gửi task inputs/secrets tới gateway khi isolation/retention chưa chứng minh.
- Thực tế: Chỉ GET health đã thất bại kết nối; không gửi prompt/input, không đọc/in ra secret, không thay đổi gateway.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [blocked dependency](evidence/blocked-dependency.md), [commands](evidence/commands.md)
- Xử lý/đề xuất: Không.

### C06 — Tài liệu và bản nhìn

- Nguồn/tiêu chí: Markdown chuẩn và HTML roadmap đồng bộ; tiếng Việt/lang/favicon.
- Bắt buộc: có
- Điều kiện/môi trường: Cập nhật Phase 06 thành Bị chặn và nhật ký preflight.
- Bước/lệnh: Render bằng `rtk proxy python3 scripts/render_plan.py`; kiểm HTML qua validator.
- Kỳ vọng: HTML đọc đúng status/cập nhật từ master-plan, không tự đánh dấu DONE.
- Thực tế: Ghi blocker và report link trong Markdown, render HTML; validator xác nhận deterministic, đủ phase, `lang=vi`, favicon và links.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [render/validator commands](evidence/commands.md), [master-plan HTML](../../../../master-plan.html)
- Xử lý/đề xuất: Không.

### C07 — Regression liên quan

- Nguồn/tiêu chí: Sanity health/gateway Phase 05 trước khi chạm runtime.
- Bắt buộc: có
- Điều kiện/môi trường: Unit/ASGI tests; không DB writes.
- Bước/lệnh: `rtk proxy uv run --project apps/api pytest apps/api/tests/test_health.py apps/api/tests/test_codex_gateway.py -q`.
- Kỳ vọng: Health/probe contract tests pass; không cần inference.
- Thực tế: Exit 0; 9 passed (0.42s). Không chạy DB integration, vì không có Phase 06 code và phase dừng ở preflight.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [commands](evidence/commands.md)
- Xử lý/đề xuất: DB/Phase 03 regression sẽ chạy khi implementation được mở lại.

### C08 — Report tái kiểm định được

- Nguồn/tiêu chí: Test Rules C08, manifest/report/link contract.
- Bắt buộc: có
- Điều kiện/môi trường: Batch r001 có manifest/evidence/report.
- Bước/lệnh: `rtk proxy python3 docs/tests/scripts/validate.py --batch docs/tests/results/phase-06/20261008T170343+0700-r001-test`.
- Kỳ vọng: C01–C08 + P06-01…P06-08 có đủ tags/results/evidence; links hợp lệ.
- Thực tế: PASS — report r001 có 16 ca, đúng summary/tag/result/evidence links; checklist/source hashes, rendered HTML và local links cũng đạt.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [manifest](evidence/source-manifest.json), [commands](evidence/commands.md), [report](report.md)
- Xử lý/đề xuất: Không.

### P06-01 — Grant trước dispatch

- Nguồn/tiêu chí: Phase 06 P06-01; spec §§10–11.
- Bắt buộc: có
- Điều kiện/môi trường: Chưa có grant evaluator/dispatcher; không cấp grant.
- Bước/lệnh: Review runtime routes/schema và định nghĩa test.
- Kỳ vọng: Deny trước POST cho grant thiếu/hết hạn/revoked/sai phase-batch-scope-model/stop-active.
- Thực tế: Không có dispatch path để kiểm các negative cases; nullable Work Order `execution_grant_id` không là quyền thực thi.
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Evidence: [blocked dependency](evidence/blocked-dependency.md), [commands](evidence/commands.md)
- Xử lý/đề xuất: Cần Owner-authenticated grant store/evaluator và tests trước dispatch.

### P06-02 — Isolation/input boundary

- Nguồn/tiêu chí: CG01, Phase 06 P06-02, spec §6.
- Bắt buộc: có
- Điều kiện/môi trường: Gateway shared offline; không gửi canary/prompt.
- Bước/lệnh: So sánh capability/source review với requirement isolation/read boundary/retention.
- Kỳ vọng: Không input nếu environment isolation và data retention chưa chứng minh.
- Thực tế: `read-only` không cô lập quyền đọc file; prompt có thể nằm trong thread/rollout. CG01 BLOCKED.
- Tag: need-change
- Kết quả: blocked
- Mức độ: critical
- Evidence: [Phase 05 gap](../../../../evidence/phase-05.md), [blocked dependency](evidence/blocked-dependency.md)
- Xử lý/đề xuất: Giữ blocked; cần decision/capability proof trước mọi input.

### P06-03 — Một turn text-only thật

- Nguồn/tiêu chí: Phase 06 AC1/P06-03.
- Bắt buộc: có
- Điều kiện/môi trường: Không có inference grant cho Phase 06 r001; dependency Phase 05 pending; gateway offline.
- Bước/lệnh: Không gửi request; kiểm grant status và live health.
- Kỳ vọng: Run thật chỉ với grant riêng, capability/privacy gates pass và có trace/artifact.
- Thực tế: Không gọi POST, không có response/artifact thật; điều kiện test đều thiếu.
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Evidence: [blocked dependency](evidence/blocked-dependency.md), [commands](evidence/commands.md)
- Xử lý/đề xuất: Chủ tịch cần cấp grant riêng sau khi CG01 đạt và dependency được quyết định.

### P06-04 — Error/timeout/unknown

- Nguồn/tiêu chí: Phase 06 P06-04; spec §§6,8.
- Bắt buộc: có
- Điều kiện/môi trường: Chưa có execution state machine/dispatcher cho model call.
- Bước/lệnh: Kiểm implementation và test fixtures có sẵn.
- Kỳ vọng: Failure/timeout không báo success; unknown reconcile, không auto retry request có outcome chưa rõ.
- Thực tế: Phase 03 có run state/checkpoint nền nhưng chưa có gateway attempt/event handling; chưa chạy được cases.
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Evidence: [blocked dependency](evidence/blocked-dependency.md), [manifest](evidence/source-manifest.json)
- Xử lý/đề xuất: Cần implement state/attempt behavior trong Phase 06 sau gate.

### P06-05 — Resource limits và reservation race

- Nguồn/tiêu chí: Phase 06 P06-05, spec §§10–11.
- Bắt buộc: có
- Điều kiện/môi trường: Không có grant/reservation ledger hoặc authenticated Owner.
- Bước/lệnh: Kiểm migrations và module routes/source.
- Kỳ vọng: Concurrent reserve/dispatch, request/time/concurrency/expiry enforced server-side.
- Thực tế: Chỉ có JSON `budget_limits`/`stop_conditions` trên task revision; không có durable reservation hoặc atomic dispatcher claim.
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Evidence: [blocked dependency](evidence/blocked-dependency.md), [commands](evidence/commands.md)
- Xử lý/đề xuất: Cần model/service reservation bền vững và race tests trước dispatch.

### P06-06 — Stop/abort

- Nguồn/tiêu chí: Phase 06 P06-06, spec §§6,10–11.
- Bắt buộc: có
- Điều kiện/môi trường: Không có live model request/dispatcher; grant 0.
- Bước/lệnh: Review cancellation contract và app runtime.
- Kỳ vọng: Stop chặn step mới, abort request đang chạy, trạng thái in-flight/unknown trung thực.
- Thực tế: Chưa có app request để abort; không dùng UI hide/fake state làm bằng chứng gateway cancellation.
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Evidence: [blocked dependency](evidence/blocked-dependency.md), [commands](evidence/commands.md)
- Xử lý/đề xuất: Cần unit state tests; live abort chỉ sau grant riêng/capability.

### P06-07 — Usage provenance

- Nguồn/tiêu chí: Phase 06 P06-07; spec §§6,11.
- Bắt buộc: có
- Điều kiện/môi trường: Không có ModelCall ledger hoặc response đã được cấp phép.
- Bước/lệnh: Kiểm schema/source và không gọi gateway chat.
- Kỳ vọng: Confirmed/estimated/unknown provenance; thiếu usage không ghi 0.
- Thực tế: Chưa có persistence cho model call/usage; không có live response; chưa thể chứng minh provenance.
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Evidence: [blocked dependency](evidence/blocked-dependency.md), [manifest](evidence/source-manifest.json)
- Xử lý/đề xuất: Cần ModelCall/usage records gắn call IDs và settlement tests.

### P06-08 — Snapshot và idle

- Nguồn/tiêu chí: Phase 06 P06-08; spec §§7,10.
- Bắt buộc: có
- Điều kiện/môi trường: Phase 03 đã có checkpoints/events; chưa có profile/grant snapshot runtime.
- Bước/lệnh: Đọc migrations, router registrations và lưu lượng idle hiện có.
- Kỳ vọng: Durable profile/policy/history/checkpoint snapshot và không loop/gọi model khi idle.
- Thực tế: Nền run/checkpoint/event có; ModelCall/grant/profile snapshot và dispatcher không tồn tại. C04 xác nhận không có đường dispatch.
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Evidence: [blocked dependency](evidence/blocked-dependency.md), [commands](evidence/commands.md)
- Xử lý/đề xuất: Implement và persistence verification khi Phase 06 được mở lại.

## Integration / release gates

| Gate áp dụng | PASS / FAIL / BLOCKED | Test IDs | Batch/grant/config/evidence và gate trước |
| --- | --- | --- | --- |
| Dependency + CG01 pre-dispatch | BLOCKED | C02, P06-01, P06-02, P06-03 | Phase 04/05 chưa nghiệm thu; grant 0; gateway 4000 offline; isolation/read boundary/retention chưa chứng minh. |

## Cleanup, giới hạn và bàn giao

- Cleanup: Không DB writes, model calls, gateway sessions, service restarts hoặc config changes.
- Chưa kiểm chứng: Tất cả P06-01…P06-08 runtime acceptance; Phase 04/05 acceptance, CG01, grant.
- Cần sửa: Phase 06 chưa implementation; dừng trước dispatcher/migration/API vì dependency/CG01/grant gates.
- Đề xuất tùy chọn: Không có.
- Bước tiếp theo: Chờ điều kiện unblock nêu trong [dependency evidence](evidence/blocked-dependency.md); không tự sang Phase 07.
- Bàn giao: Phase 06 status Bị chặn; không có runtime demo hoặc inference; report này là preflight, không là nghiệm thu.
