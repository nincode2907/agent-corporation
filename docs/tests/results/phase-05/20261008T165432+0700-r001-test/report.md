# Kiểm định Phase 05 — 20261008T165432+0700-r001-test

## Thông tin batch

- Phase: 05
- Test batch: 20261008T165432+0700-r001-test
- Vòng: r001
- Bắt đầu / kết thúc: 2026-10-08T16:54:32+07:00 / 2026-10-08T16:55:15+07:00
- Người/AI kiểm định: Codex
- Yêu cầu/phạm vi được giao: “làm lại test rồi tiếp phase 6”; retest Phase 05 theo flow test/remake/retest, kiểm dependency, grant hiện tại 0.
- Source: Worktree dirty do các thay đổi Phase 05 từ lượt trước và tài liệu/test do Chủ tịch cập nhật trong lúc đó; không dùng commit đơn lẻ. [Manifest](evidence/source-manifest.json) có file list/hash phần đã kiểm.
- Môi trường/config/tool versions: local; API 15501 và Vite 15500 có process đang chạy; API process chưa nạp route Phase 05; codex-server 4000 offline. Node 24.21.0, npm 11.19.0, uv 0.12.23.
- Inference: Không gọi; grant = 0.
- Dependency/quyết định nghiệm thu: Phase 03 complete. Phase 04 đang Chờ nghiệm thu trong master-plan và report retest mới kết luận cần sửa/blocked; root AGENTS ghi “đang triển khai”, gây mismatch. Phase 05 chưa đạt gate CG01. Yêu cầu hiện tại cho phép test Phase 05 rồi tiếp Phase 06, nhưng không tự nghiệm thu dependency.
- Supersedes: [report legacy Phase 05 trước](../20261008T161028+0700-phase05-probe/report.md)
- Remake nguồn: Không có ở vòng đầu.
- Kết luận kỹ thuật: cần sửa
- Quyết định Chủ tịch: Chưa có nghiệm thu Phase 05.

## Mapping nghiệm thu → test

| Tiêu chí hiện tại / nguồn | Test IDs | Bắt buộc / tùy điều kiện | Ghi chú |
| --- | --- | --- | --- |
| Phase 05 dependency 03,04; master-plan là trạng thái chuẩn | C02 | Bắt buộc | AGENTS lệch master-plan; Phase 04 vẫn chưa nghiệm thu |
| Gateway contract, health/models live, capability/version/auth | P05-01 | Bắt buộc | Server 4000 offline; API app route process hiện tại 404 |
| Offline/auth/schema UI và demo manual GET | C03, C06, P05-02 | Bắt buộc | Browser probe lỗi làm React unmount |
| Secret handling, no inference, model catalog != entitlement | C04, C05, P05-03, P05-07 | Bắt buộc | Fake adapter tests chạy; profile Owner vẫn thiếu auth |
| Owner-only model profile và fallback/429 queue | P05-03, P05-04, P05-05 | Bắt buộc | Chưa có authenticated Owner hoặc durable queue/allowlist |
| CG01 isolation/privacy/retention; không sửa shared gateway | C01, P05-06 | Bắt buộc | Source review; không gửi inputs khi proof thiếu |
| Docs/HTML/report completeness và regression | C07, C08 | Bắt buộc | 9 API tests, lint/build, validator |

## Tổng hợp

| Tag | Số test |
| --- | ---: |
| clean | 6 |
| need-change | 9 |
| suggestion | 0 |

| Result | Số test |
| --- | ---: |
| pass | 6 |
| fail | 4 |
| blocked | 5 |
| not-run | 0 |
| not-applicable | 0 |

## Kết quả từng test

### C01 — Phạm vi và dirty worktree

- Nguồn/tiêu chí: Chỉ retest Phase 05 trước khi tiếp tục; giữ nguyên thay đổi Chủ tịch và không gọi inference.
- Bắt buộc: có
- Điều kiện/môi trường: Worktree có thay đổi Phase 05, cập nhật RULES/checklists và report Phase 02–04 song song.
- Bước/lệnh: Kiểm `git status`, master-plan, AGENTS; các batch khác không sửa.
- Kỳ vọng: Không đụng Phase 06 implementation trong vòng này, không restart API/DB/gateway.
- Thực tế: Chỉ retest Phase 05; API/PostgreSQL/gateway không restart; grant=0.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [manifest](evidence/source-manifest.json), [commands](evidence/commands.md)
- Xử lý/đề xuất: Không.

### C02 — Dependency và nguồn trạng thái

- Nguồn/tiêu chí: Root [AGENTS.md](../../../../../AGENTS.md) và [master-plan Phase 04/05](../../../../master-plan.md); master-plan là nguồn chuẩn.
- Bắt buộc: có
- Điều kiện/môi trường: Phase 04 master-plan đang Chờ nghiệm thu; report retest Phase 04 mới có need-change; AGENTS nói Phase 04 đang triển khai.
- Bước/lệnh: Đối chiếu các trạng thái hiện hành.
- Kỳ vọng: Tài liệu runtime không đưa status mâu thuẫn; dependency 04 chỉ được coi hoàn tất khi có nghiệm thu.
- Thực tế: AGENTS và master-plan lệch. Phase 04 chưa có nghiệm thu, Phase 05 còn chờ nghiệm thu.
- Tag: need-change
- Kết quả: fail
- Mức độ: minor
- Evidence: [Phase 04 retest](../../phase-04/20261008T162050+0700-demo-factory/report.md), [master-plan](../../../../master-plan.md), [AGENTS](../../../../../AGENTS.md)
- Xử lý/đề xuất: Đồng bộ câu status trong AGENTS với nguồn chuẩn; không tự đổi status roadmap hay nghiệm thu Phase 04.

### C03 — Tiêu chí và demo

- Nguồn/tiêu chí: Phase 05 AC1–AC3 và demo bắt buộc.
- Bắt buộc: có
- Điều kiện/môi trường: API hiện tại chưa nạp route gateway; Vite đang HMR source mới.
- Bước/lệnh: Mở Settings và bấm probe; kiểm response GET của API.
- Kỳ vọng: Offline/auth/schema errors hiển thị trong UI, không phá trang.
- Thực tế: API trả 404 cho probe route; UI tin payload đúng schema, ném exception và trang trắng.
- Tag: need-change
- Kết quả: fail
- Mức độ: major
- Evidence: [UI error](evidence/P05-02-ui-error.md), [commands](evidence/commands.md)
- Xử lý/đề xuất: Frontend kiểm status/schema trước state update, hiển thị lỗi an toàn.

### C04 — Không thực thi âm thầm

- Nguồn/tiêu chí: Phase 05 no inference; Spec §6.
- Bắt buộc: có
- Điều kiện/môi trường: Fake transport, probe chỉ sau nút bấm.
- Bước/lệnh: 9 API tests và đọc call path.
- Kỳ vọng: Startup/health/profile không gọi gateway; manual probe chỉ GET allowlist, không POST/session/tool.
- Thực tế: Spy test ghi hai GET `/health`, `/v1/models`; nút UI tạo GET probe duy nhất; không có POST/model.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [test file](../../../../../apps/api/tests/test_codex_gateway.py), [commands](evidence/commands.md)
- Xử lý/đề xuất: Không.

### C05 — Scope và secret

- Nguồn/tiêu chí: Phase 05 auth ref/redaction; test canary.
- Bắt buộc: có
- Điều kiện/môi trường: Fake secret canary; không đọc `.env`.
- Bước/lệnh: Kiểm normalized output và request spy.
- Kỳ vọng: Không lộ Bearer/token; catalog không bị hiểu là entitlement.
- Thực tế: Tests pass; secret canary không nằm trong response; chỉ có boolean auth config và model IDs; entitlement luôn false.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [test file](../../../../../apps/api/tests/test_codex_gateway.py), [manifest](evidence/source-manifest.json)
- Xử lý/đề xuất: Không.

### C06 — Tài liệu và bản nhìn

- Nguồn/tiêu chí: Root language/accessibility; Phase 05 Settings UI; roadmap HTML.
- Bắt buộc: có
- Điều kiện/môi trường: Browser QA tab, web/API local cũ.
- Bước/lệnh: Mở Settings; bấm manual GET; quan sát render/console; kiểm lint/build.
- Kỳ vọng: Nội dung tiếng Việt, error state dùng được; React không crash khi API contract sai.
- Thực tế: Trước probe Settings render; sau HTTP 404 thì React unmount trang. `lang=vi`, lint/build pass không phát hiện runtime exception.
- Tag: need-change
- Kết quả: fail
- Mức độ: major
- Evidence: [UI error](evidence/P05-02-ui-error.md), [commands](evidence/commands.md)
- Xử lý/đề xuất: Sửa parser trạng thái frontend và kiểm tra lại trực quan.

### C07 — Regression liên quan

- Nguồn/tiêu chí: Health/adapter backend và web bundle.
- Bắt buộc: có
- Điều kiện/môi trường: Không làm DB writes; API/DB Phase 04 đang dùng.
- Bước/lệnh: `uv run --project apps/api pytest apps/api/tests/test_health.py apps/api/tests/test_codex_gateway.py -q`; web lint/build.
- Kỳ vọng: API health/adapter regression pass, lint/build pass.
- Thực tế: 9 passed (1.33s), lint exit 0, build TypeScript/Vite exit 0. DB suites Phase 03/04 không chạy.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [commands](evidence/commands.md)
- Xử lý/đề xuất: Không restart service/database đang dùng.

### C08 — Report tái kiểm tra được

- Nguồn/tiêu chí: Test Rules C08, round workflow.
- Bắt buộc: có
- Điều kiện/môi trường: Batch r001 có source manifest, commands và UI/live evidence.
- Bước/lệnh: `rtk proxy python3 docs/tests/scripts/validate.py --batch docs/tests/results/phase-05/20261008T165432+0700-r001-test`; kiểm 15 case và links.
- Kỳ vọng: Required IDs/tags/fields/links hợp lệ; report snapshot không sửa sau remediation.
- Thực tế: PASS — targeted validator chấp nhận 15 case, thống kê/tag/result, evidence links và batch path. Không thay report này sau khi bắt đầu remake.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [manifest](evidence/source-manifest.json), [commands](evidence/commands.md), [report](report.md)
- Xử lý/đề xuất: Không.

### P05-01 — Contract và live probe

- Nguồn/tiêu chí: Phase 05 AC1/P05-01; gateway source fingerprint.
- Bắt buộc: có
- Điều kiện/môi trường: Gateway 127.0.0.1:4000 offline; API 15501 là process cũ.
- Bước/lệnh: Đọc gateway source; GET local gateway adapter và `/api/v1/codex/probe`.
- Kỳ vọng: Source matrix đúng và HTTP live health/models xác nhận contract.
- Thực tế: Source xác nhận health/models; live gateway offline; app route 404. Không có response runtime để xác nhận auth/catalog.
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Evidence: [live probe](evidence/live-probe.md), [commands](evidence/commands.md), [manifest](evidence/source-manifest.json)
- Xử lý/đề xuất: Cần gateway tự chạy theo cấu hình hiện hữu và API build mới được vận hành trong cửa sổ được phép; không tự restart shared services.

### P05-02 — Offline/auth/schema mismatch

- Nguồn/tiêu chí: Phase 05 demo và checklist P05-02.
- Bắt buộc: có
- Điều kiện/môi trường: Fake adapter cases pass; browser gọi current API process cũ.
- Bước/lệnh: 9 tests fake; CUA click manual probe với HTTP 404 thực.
- Kỳ vọng: Fake + live-shaped errors hiển thị an toàn, không crash, token không lộ.
- Thực tế: Adapter tests pass offline/401/429/schema; UI xử lý HTTP 404 sai và crash `reading 'length'`.
- Tag: need-change
- Kết quả: fail
- Mức độ: major
- Evidence: [UI error](evidence/P05-02-ui-error.md), [commands](evidence/commands.md)
- Xử lý/đề xuất: Xử lý `response.ok` và validate payload trước khi set state; thêm fallback contract error.

### P05-03 — Catalog, entitlement và profile

- Nguồn/tiêu chí: Phase 05 P05-03, Spec §6/10.
- Bắt buộc: có
- Điều kiện/môi trường: Fake catalog tests; không có Owner principal.
- Bước/lệnh: Test parsing/entitlement marker; kiểm identity model profile.
- Kỳ vọng: Catalog không chứng minh entitlement; Owner chọn model/effort trong profile đã xác thực.
- Thực tế: Catalog được gắn entitlement=false; owner profile chưa triển khai do API thiếu authenticated identity.
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Evidence: [source tests](../../../../../apps/api/tests/test_codex_gateway.py), [Phase 05 evidence](../../../../evidence/phase-05.md)
- Xử lý/đề xuất: Cần identity/auth backend thuộc quyết định/phạm vi riêng; không dùng mode UI làm quyền.

### P05-04 — Owner-only profile

- Nguồn/tiêu chí: Phase 05 P05-04, Spec §10.
- Bắt buộc: có
- Điều kiện/môi trường: Không có auth middleware/principal.
- Bước/lệnh: Kiểm API routes/settings, không tự khai actor.
- Kỳ vọng: Agent bị deny, Owner ghi được profile/audit.
- Thực tế: Không có cơ chế xác thực Owner để làm phép thử đúng lớp; không tạo endpoint ghi giả bảo mật.
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Evidence: [manifest](evidence/source-manifest.json), [Phase 05 evidence](../../../../evidence/phase-05.md)
- Xử lý/đề xuất: Chờ identity/authorization backend; retest negative Owner/agent.

### P05-05 — 429 queue và fallback allowlist

- Nguồn/tiêu chí: Phase 05 nghiệm thu/P05-05, Spec §6/11.
- Bắt buộc: có
- Điều kiện/môi trường: Fake 429 adapter pass; chưa có durable run queue hoặc Owner fallback allowlist.
- Bước/lệnh: Xem policy/orchestration source; không tạo model request.
- Kỳ vọng: Bounded requeue/backoff và fallback chỉ trong allowlist Owner.
- Thực tế: Probe hiển thị rate_limited, không retry; queue/profile policy chưa có.
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Evidence: [test file](../../../../../apps/api/tests/test_codex_gateway.py), [Phase 05 evidence](../../../../evidence/phase-05.md)
- Xử lý/đề xuất: Cần queue/policy bền vững; không thêm retry RAM/fallback.

### P05-06 — CG01 isolation/privacy

- Nguồn/tiêu chí: Spec §6 CG01; Phase 05 P05-06.
- Bắt buộc: có
- Điều kiện/môi trường: Gateway source static review; không gửi input.
- Bước/lệnh: Đối chiếu provider/sessions/TECHNICAL trong source manifest.
- Kỳ vọng: Có proof isolation/read boundary và retention trước khi gửi bất cứ input nào.
- Thực tế: `read-only` không cô lập quyền đọc file user; sessions/rollout có thể lưu prompt. Gate chưa đạt; server chung không đổi.
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Evidence: [capability gap](../../../../evidence/phase-05.md), [manifest](evidence/source-manifest.json)
- Xử lý/đề xuất: Theo CG01 chờ quyết định/capability proof; cần grant mới nếu đợt test tương lai có inference.

### P05-07 — Không inference từ probe

- Nguồn/tiêu chí: Phase 05 limit; grant 0.
- Bắt buộc: có
- Điều kiện/môi trường: Probe UI manual và fake spy.
- Bước/lệnh: Kiểm test request counter và GET app URL.
- Kỳ vọng: Probe chỉ GET, không tạo run/session/model call.
- Thực tế: Không có POST; chỉ GET probe; grant=0.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [test file](../../../../../apps/api/tests/test_codex_gateway.py), [commands](evidence/commands.md)
- Xử lý/đề xuất: Không.

## Integration / release gates

| Gate áp dụng | PASS / FAIL / BLOCKED | Test IDs | Batch/grant/config/evidence và gate trước |
| --- | --- | --- | --- |
| Không có IG riêng; CG01 decision gate | BLOCKED | P05-01, P05-03, P05-04, P05-05, P05-06 | Round r001; grant 0; gateway offline; Phase 04 chưa nghiệm thu; isolation/privacy và Owner/queue controls chưa chứng minh. |

## Cleanup, giới hạn và bàn giao

- Cleanup: Không ghi database, tạo gateway session, hay thay đổi service/config; API/web hiện hữu không restart.
- Chưa kiểm chứng: Live gateway/auth/model catalog; Owner model profile; 429 queue/fallback; CG01; Phase 04 dependency.
- Cần sửa: C02 source status mismatch; C03/C06/P05-02 UI crash với HTTP error. Các blocker P05-01/03/04/05/06 cần state/quyền/capability ngoài phép thử này.
- Đề xuất tùy chọn: Không có.
- Bước tiếp theo: Remake các lỗi tài liệu/UI trong scope Phase 05, rồi retest r002; blocker ngoài quyền sẽ giữ lại.
- Bàn giao: Kết luận hiện tại **cần sửa**; chưa nghiệm thu Phase 05.
