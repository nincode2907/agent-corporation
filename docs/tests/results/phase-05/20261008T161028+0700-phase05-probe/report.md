# Kiểm định Phase 05 — 20261008T161028+0700-phase05-probe

## Thông tin batch

- Phase: 05
- Test batch: 20261008T161028+0700-phase05-probe
- Bắt đầu / kết thúc: 2026-10-08T16:10:28+07:00 / 2026-10-08T16:16:41+07:00
- Người/AI kiểm định: Codex
- Yêu cầu/phạm vi được giao: Sửa theo test Phase 01, lưu remake, sau đó triển khai Phase 05; chỉ Phase 05, kiểm tra dependency trước; không inference khi chưa có grant.
- Source: worktree dirty do batch này và các report Phase 02/03 xuất hiện độc lập trong workspace khi đang làm; các thay đổi đó được giữ nguyên, không sửa. Hashes/runtime của phần scope này ở [manifest](evidence/source-manifest.json).
- Môi trường/config/tool versions: local workstation; Node 24.21.0, npm 11.19.0, uv 0.12.23; API 15501/web 15500 đang chạy sẵn và không restart; codex-server 4000 offline.
- Inference: Không gọi; grant = 0. Chỉ GET local, test giả, build/lint.
- Dependency/quyết định nghiệm thu: Phase 03 hoàn tất; Phase 04 đang Chờ nghiệm thu với thiếu evidence ledger/thread/file-store isolation và screenshot. Chủ tịch trực tiếp chỉ thị tiếp Phase 05 sau remediation Phase 01, nhưng dependency Phase 04 không được coi là đã nghiệm thu; C02 ghi rõ blocked.
- Supersedes: Không có.
- Kết luận kỹ thuật: chưa đủ bằng chứng
- Quyết định Chủ tịch: Chưa có nghiệm thu Phase 05 trong lượt này.

## Mapping nghiệm thu → test

| Tiêu chí hiện tại / nguồn | Test IDs | Bắt buộc / tùy điều kiện | Ghi chú |
| --- | --- | --- | --- |
| Dependency 03,04; Phase 04 còn chờ nghiệm thu | C02 | Bắt buộc | Thực hiện Phase 05 theo chỉ thị trực tiếp; không đổi trạng thái dependency |
| Adapter, base URL, source contract, capability probe, secret redaction | P05-01, P05-02, P05-06 | Bắt buộc | Live gateway offline; source/test giả tách biệt rõ |
| Role/persona, model/tools/skills/policy và model selection/profile Owner-only | P05-03, P05-04 | Bắt buộc | Không có authenticated Owner identity; không giả quyền |
| Health/auth status và UI lỗi/khắc phục | C03, C06, P05-01, P05-02 | Bắt buộc | UI có manual GET probe, offline/auth/rate-limit/schema mismatch |
| Catalog không chứng minh entitlement; không inference từ probe | C04, C05, P05-03, P05-07 | Bắt buộc | Grant=0, không POST/session |
| Không đổi gateway shared; 429 queue và explicit fallback allowlist | C01, P05-05, P05-06 | Bắt buộc | Không có durable queue hay Owner allowlist; blocked |
| Code/test/doc/html đúng phase | C07, C08 | Bắt buộc | API tests, lint/build, Markdown trước và render HTML |

## Tổng hợp

| Tag | Số test |
| --- | ---: |
| clean | 7 |
| need-change | 7 |
| suggestion | 1 |

| Result | Số test |
| --- | ---: |
| pass | 8 |
| fail | 0 |
| blocked | 7 |
| not-run | 0 |
| not-applicable | 0 |

## Kết quả từng test

### C01 — Phạm vi và diff

- Nguồn/tiêu chí: Chỉ Phase 05 theo chỉ thị; giữ nguyên Phase 04, shared gateway và inference boundary.
- Bắt buộc: có
- Điều kiện/môi trường: Worktree có thay đổi Phase 01/05; các batch Phase 02/03 xuất hiện độc lập khi lượt này đang chạy.
- Bước/lệnh: Đối chiếu `git status`, plan và file diff; không restart API/DB/gateway.
- Kỳ vọng: Không mở Phase 06, không đổi gateway/proxy, không gửi inference.
- Thực tế: Sửa README remediation + adapter/API/UI/docs Phase 05; grant 0; gateway không đổi. Hai report Phase 02/03 được giữ nguyên, không đưa vào scope.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [manifest](evidence/source-manifest.json), [Phase 01 remake](../../../../remakes/phase-01-followup.md), [Phase 02 report](../../phase-02/20261008T161241+0700-phase-02/report.md), [Phase 03 report](../../phase-03/20261008T161241+0700-phase-03/report.md)
- Xử lý/đề xuất: Không.

### C02 — Dependency và nguồn quyết định

- Nguồn/tiêu chí: [Phase 05 dependency](../../../../master-plan.md); Phase 04 phải bàn giao trước 05.
- Bắt buộc: có
- Điều kiện/môi trường: Phase 04 đang Chờ nghiệm thu; report ghi P04-03 thiếu isolation evidence và P04-05 thiếu screenshot saved.
- Bước/lệnh: Đọc master-plan, evidence/report Phase 04; so với chỉ thị Chủ tịch hiện tại.
- Kỳ vọng: Dependency được nêu chính xác; không tự chuyển trạng thái.
- Thực tế: Chỉ thị hiện tại cho phép bắt đầu 05, nhưng không nghiệm thu Phase 04; các integration features 05 độc lập chạy, phần phụ thuộc chưa được chứng minh.
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Evidence: [Phase 04 evidence](../../../../evidence/phase-04.md), [Phase 04 report](../../phase-04/20261008T154151+0700-demo-factory/report.md)
- Xử lý/đề xuất: Giữ Phase 04 Chờ nghiệm thu; Chủ tịch quyết định remediation/acceptance trước khi khẳng định dependency đã đạt.

### C03 — Đủ tiêu chí và demo

- Nguồn/tiêu chí: Phase 05 roadmap AC1–AC3 và checklist P05.
- Bắt buộc: có
- Điều kiện/môi trường: API/UI hiện tại; probe được bấm thủ công.
- Bước/lệnh: API ASGI tests, web build; đối chiếu Settings UI và từng AC.
- Kỳ vọng: Manual GET probe, demo lỗi không inference; mọi AC có test/evidence.
- Thực tế: API route + Settings probe UI có; source/fake error variants được test; live gateway offline; profile/queue/privacy gaps được ghi riêng.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [commands](evidence/commands.md), [Phase 05 evidence](../../../../evidence/phase-05.md)
- Xử lý/đề xuất: Thiếu năng lực bắt buộc được phản ánh ở P05 cases, không che bằng demo.

### C04 — Không thực thi âm thầm

- Nguồn/tiêu chí: Phase 05 giới hạn no inference; Product Spec §6.
- Bắt buộc: có
- Điều kiện/môi trường: App startup/health/profile không gọi probe; adapter test dùng spy.
- Bước/lệnh: `pytest ...test_codex_gateway.py`; xem source router/UI.
- Kỳ vọng: Chỉ probe bấm tay; probe gồm hai GET allowlist; không POST chat/session/tool.
- Thực tế: Spy ghi đúng `/health`, `/v1/models`; không có request POST; startup/health/UI profile không auto probe.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [test source](../../../../../apps/api/tests/test_codex_gateway.py), [commands](evidence/commands.md)
- Xử lý/đề xuất: Không.

### C05 — Scope, secret và dữ liệu nhạy cảm

- Nguồn/tiêu chí: Phase 05 secret redaction; `codex-server/docs/TECHNICAL.md`.
- Bắt buộc: có
- Điều kiện/môi trường: Fake secret canary; `.env` content/session/transcript không đọc.
- Bước/lệnh: Secret canary assertion trong test; kiểm response adapter/UI contract.
- Kỳ vọng: Không trả/log token, không lấy model names làm entitlement, không gửi prompt.
- Thực tế: Canary không có trong normalized result; UI chỉ nhận boolean `auth_configured`; payload chỉ model IDs; inference=0.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [adapter tests](../../../../../apps/api/tests/test_codex_gateway.py), [source manifest](evidence/source-manifest.json)
- Xử lý/đề xuất: Không.

### C06 — Tài liệu và bản nhìn

- Nguồn/tiêu chí: Root AGENTS: tiếng Việt, Markdown source, HTML đồng bộ; README Phase 01 finding C02.
- Bắt buộc: có
- Điều kiện/môi trường: docs và React Settings UI.
- Bước/lệnh: README assertion; `npm run lint/build`; `python3 scripts/render_plan.py`.
- Kỳ vọng: IPv4-only statement đúng; HTML cùng trạng thái/nhật ký; UI tiếng Việt.
- Thực tế: README C02 assertion và web build/lint pass; roadmap HTML được render từ Markdown; `lang="vi"` giữ nguyên. Screenshot browser không được lưu trong batch.
- Tag: suggestion
- Kết quả: pass
- Mức độ: info
- Evidence: [Phase 01 remake](../../../../remakes/phase-01-followup.md), [commands](evidence/commands.md), [roadmap HTML](../../../../master-plan.html)
- Xử lý/đề xuất: Có thể lưu ảnh browser trong một đợt review visual sau; không coi là nghiệm thu Phase 04 screenshot.

### C07 — Regression liên quan

- Nguồn/tiêu chí: Health Phase 01–03 API và web UI bị diff tác động; tránh DB writes khi Phase 04 đang dùng runtime.
- Bắt buộc: có
- Điều kiện/môi trường: In-process health/adapter API tests; API live health + web GET hiện hữu.
- Bước/lệnh: `uv run --project apps/api pytest apps/api/tests/test_health.py apps/api/tests/test_codex_gateway.py -q`; web lint/build.
- Kỳ vọng: Health giữ nguyên, route probe không làm DB writes; UI build/lint pass.
- Thực tế: 9 API tests passed; lint/build pass; API/web GET 200. Không chạy P03/P04 DB-writing tests.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [commands](evidence/commands.md)
- Xử lý/đề xuất: Domain DB integration suite giữ ngoài scope để tránh ảnh hưởng Phase 04 runtime.

### C08 — Report có thể tái kiểm tra

- Nguồn/tiêu chí: Test Rules C08 và Phase 05 checklist.
- Bắt buộc: có
- Điều kiện/môi trường: Batch report/evidence local, không secrets.
- Bước/lệnh: Kiểm links, 15 IDs, tags/results và source hashes.
- Kỳ vọng: Mọi case có đúng 1 tag/result/evidence; không overclaim.
- Thực tế: Manifest, commands, live probe, report và evidence Phase 05 có đủ; validator tài liệu sẽ chạy khi đóng batch.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [manifest](evidence/source-manifest.json), [report](report.md)
- Xử lý/đề xuất: Không.

### P05-01 — Source contract và live probe

- Nguồn/tiêu chí: Roadmap Phase 05 AC1; Spec §6; checklist P05-01.
- Bắt buộc: có
- Điều kiện/môi trường: Source fingerprint đã ghi; local codex-server 4000 offline.
- Bước/lệnh: Đối chiếu README/server/schema/provider/config; gọi adapter live chỉ GET.
- Kỳ vọng: Capability matrix có nguồn; live health/models được lọc và xác nhận.
- Thực tế: Contract source xác nhận `GET /health`, `GET /v1/models`, no streaming/max_tokens; live GET connection refused nên không có response runtime.
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Evidence: [capability matrix](../../../../evidence/phase-05.md), [live probe](evidence/live-probe.md), [manifest](evidence/source-manifest.json)
- Xử lý/đề xuất: Cần codex-server được vận hành theo hiện trạng bình thường rồi test lại GET; không tự start/restart hoặc đổi shared config.

### P05-02 — Offline/auth/schema mismatch

- Nguồn/tiêu chí: Roadmap demo lỗi; Phase 05 checklist P05-02.
- Bắt buộc: có
- Điều kiện/môi trường: Fake adapter transport, không gọi gateway.
- Bước/lệnh: Test offline, 401, 429, malformed catalog và available response.
- Kỳ vọng: Status/message đúng và đã lọc; không lộ token.
- Thực tế: Các variant API test pass; thông báo chung không bao gồm exception/header/secret. UI runtime chưa được mở với API build mới vì API Phase 04 đang chạy và không restart; do đó chưa quan sát trực tiếp UI cho offline/auth/schema mismatch.
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Evidence: [tests](../../../../../apps/api/tests/test_codex_gateway.py), [commands](evidence/commands.md)
- Xử lý/đề xuất: Khi có cửa sổ runtime được phép restart/serve API build mới, kiểm tra trực quan cả error states; hiện không làm gián đoạn API/DB Phase 04.

### P05-03 — Model catalog, entitlement và profile

- Nguồn/tiêu chí: Roadmap Phase 05 scope; checklist P05-03; Spec §6/10.
- Bắt buộc: có
- Điều kiện/môi trường: Model catalog chỉ có từ source/fake; không có live entitlement check, không có Owner identity.
- Bước/lệnh: Test catalog parsing và UI marker `entitlement_verified=false`; kiểm có lựa chọn model profile được Owner xác thực không.
- Kỳ vọng: Catalog không suy entitlement; Owner chọn model/effort trong profile được xác thực.
- Thực tế: Catalog semantics đúng; UI không khẳng định entitlement. Owner-only profile chưa được triển khai vì chưa có authenticated identity; không hardcode model.
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Evidence: [adapter](../../../../../apps/api/src/agent_corporation_api/modules/codex_gateway/adapter.py), [Settings UI](../../../../../apps/web/src/App.tsx)
- Xử lý/đề xuất: Cần identity/authorization Owner đáng tin ở backend trước khi cho phép ghi profile; không dùng UI mode/header actor làm permission.

### P05-04 — Owner-only profile

- Nguồn/tiêu chí: Phase 05 checklist P05-04; Product Spec §10.
- Bắt buộc: có
- Điều kiện/môi trường: API hiện chưa có auth middleware hoặc danh tính Owner xác thực.
- Bước/lệnh: Kiểm router/API auth source và Settings UI.
- Kỳ vọng: Agent bị deny, Owner được ghi profile và audit/version.
- Thực tế: Chưa có auth principal để phân biệt Owner/agent; không tạo write endpoint insecure. UI hiển thị profile chưa cấu hình.
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Evidence: [auth source search](evidence/commands.md), [Settings UI](../../../../../apps/web/src/App.tsx)
- Xử lý/đề xuất: Chốt/triển khai identity/authorization trong phase được giao có auth scope; retest Owner và agent denial.

### P05-05 — 429, bounded retry queue và fallback

- Nguồn/tiêu chí: Phase 05 nghiệm thu; checklist P05-05; Spec §6/11.
- Bắt buộc: có
- Điều kiện/môi trường: Phase 05 không có durable model-call queue hoặc fallback allowlist/policy Owner; gateway offline.
- Bước/lệnh: Fake 429 status path; kiểm source queue/policy hiện có.
- Kỳ vọng: 429 vào queue bounded/backoff; fallback chỉ danh sách Owner duyệt; unknown không retry.
- Thực tế: Adapter trả `rate_limited`, không retry/fallback. Không có queue/profile policy; không thể chứng minh requeue bằng fake transport.
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Evidence: [test](../../../../../apps/api/tests/test_codex_gateway.py), [Phase 05 evidence](../../../../evidence/phase-05.md)
- Xử lý/đề xuất: Tích hợp queue khi orchestration/persistence được triển khai; không tự thêm queue RAM hoặc fallback model.

### P05-06 — CG01 isolation/privacy/retention

- Nguồn/tiêu chí: Product Spec §6 CG01; Phase 05 checklist P05-06.
- Bắt buộc: có
- Điều kiện/môi trường: Static source review; không gửi bất kỳ input nào.
- Bước/lệnh: Đọc `codex-server/src/provider.ts`, `sessions.ts`, `docs/TECHNICAL.md`.
- Kỳ vọng: Trước input, xác minh isolation/read boundary và retention; nếu không đạt thì gap report + blocked, không sửa gateway chung.
- Thực tế: CLI sandbox `read-only` không ngăn đọc user files; gateway sessions lưu messages và stateless chat có thể ghi Codex rollout. Không có đủ proof isolation/privacy. Không sửa server và không gửi prompt.
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Evidence: [capability/privacy matrix](../../../../evidence/phase-05.md), [source manifest](evidence/source-manifest.json)
- Xử lý/đề xuất: Theo CG01 giữ blocked; chờ quyết định Chủ tịch về phương án/đợt kiểm tra có scope+grant riêng. Nghiệm thu Phase 00 không cấp grant.

### P05-07 — Không inference từ probe

- Nguồn/tiêu chí: Phase 05 limit; checklist P05-07; grant hiện tại 0.
- Bắt buộc: có
- Điều kiện/môi trường: Probe manual; adapter spy tests.
- Bước/lệnh: Ghi calls của fake adapter, inspect startup/health/profile code.
- Kỳ vọng: 0 POST inference, không tạo session/run; chỉ GET khi Owner chủ động bấm.
- Thực tế: Spy chỉ có hai GET allowlist; route không expose POST; không startup probe/session/run; grant=0.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [adapter tests](../../../../../apps/api/tests/test_codex_gateway.py), [commands](evidence/commands.md)
- Xử lý/đề xuất: Không.

## Integration / release gates

| Gate áp dụng | PASS / FAIL / BLOCKED | Test IDs | Batch/grant/config/evidence và gate trước |
| --- | --- | --- | --- |
| Không có IG riêng cho Phase 05; CG01 privacy decision gate | BLOCKED | C02, P05-01, P05-04, P05-05, P05-06 | Batch `20261008T161028+0700-phase05-probe`, grant 0; Phase 04 chưa nghiệm thu; gateway live offline; Owner auth/queue/privacy proof thiếu. Giữ gateway chung nguyên trạng. |

## Cleanup, giới hạn và bàn giao

- Cleanup: Không tạo dữ liệu DB, gateway session, artifact hoặc fixture ghi bền; API/web server cũ không restart; không đổi shared gateway/proxy.
- Chưa kiểm chứng: C02 dependency Phase 04; P05-01 live server GET/auth; P05-03/04 Owner profile; P05-05 durable queue/allowlist; P05-06 CG01 privacy/isolation. Các case blocked cần dependency/permission/capability evidence cụ thể như từng test nêu.
- Cần sửa: Các blocker major trên trước khi coi toàn bộ năng lực Phase 05 nghiệm thu. Không có lỗi bắt buộc đã tái hiện trong adapter/UI tests.
- Đề xuất tùy chọn: C06 lưu screenshot UI riêng khi có phiên review visual; không thay evidence screenshot Phase 04.
- Bàn giao: Adapter/API/UI probe read-only và docs; kỹ thuật **chưa đủ bằng chứng**, Phase 05 đang Chờ Chủ tịch nghiệm thu. Phase 04 giữ Chờ nghiệm thu; dừng tại Phase 05, không sang Phase 06.
