# Kiểm định Phase 01 — 20261009T091446+0700-r004-test

## Thông tin batch

- Phase: 01
- Test batch: 20261009T091446+0700-r004-test
- Vòng: r004
- Bắt đầu / kết thúc: 2026-10-09 09:14:46 / 09:21:08 +07:00 (Asia/Ho_Chi_Minh)
- Người/AI kiểm định: Codex QA độc lập (`/root/phase01_independent_test`), khác AI điều phối/remake (`/root`).
- Yêu cầu/phạm vi được giao: “review lại phase 1”; chỉ kiểm định Phase 01, không sửa implementation.
- Source: commit `e44bc19783e15b29311f467a2be86943b76d847f` + dirty worktree; [manifest/hash](evidence/source-manifest.json).
- Môi trường/config/tool versions: macOS arm64; Node 24.21.0/npm 11.19.0; uv 0.12.23; Docker 20.10.23; runtime hiện hữu loopback IPv4.
- Inference: Không gọi; grant = 0. Không gọi gateway probe.
- Dependency/quyết định nghiệm thu: Phase 00 đã nghiệm thu; Phase 01 hiện “Chờ nghiệm thu”. Report này không thay đổi trạng thái chính thức.
- Supersedes: [r003](../20261009T091040+0700-r003-test/report.md), vì report đó đánh clean P01-01 sau khi chỉ chạy `npm ci` từ `apps/web`, không thử lệnh README `npm ci --prefix apps/web`; batch này chạy lại đúng README command trong bản sao sạch và ghi finding. Source Phase 01 runtime/lockfile/README/checklist không đổi từ r002; `docs/master-plan.md` đổi để ghi trạng thái review.
- Remake nguồn: [r001](../../../../remakes/phase-01/20261009T085800+0700-r001-remake/remake.md); r002 là self-retest của AI remake và không được tính là kiểm định độc lập.
- Kết luận kỹ thuật: cần sửa
- Lý do kết luận: Lệnh cài frontend trong README fail trên bản sao sạch; ba phần demo/failure/migration còn bị chặn do không tác động DB dùng chung.
- Quyết định Chủ tịch: Chưa có quyết định nghiệm thu mới.

## QA verdict

**READY WITH KNOWN ISSUES (P2 setup/documentation issue).** Có workaround cài frontend đã xác minh; nên sửa hướng dẫn trước khi bàn giao setup cho môi trường sạch. Kết luận kỹ thuật theo RULES Phase vẫn là **cần sửa** vì một tiêu chí cài đặt bắt buộc thất bại. Không coi r002 tự retest là review độc lập.

## Mapping và phạm vi kiểm định

| Tiêu chí hiện tại / nguồn | Test IDs | Bắt buộc / tùy điều kiện | Ghi chú |
| --- | --- | --- | --- |
| AC1 — lệnh cài/chạy/check không cần secret trong Git | P01-01…P01-04 | Bắt buộc | Lệnh cài đúng README được tái hiện trong bản sao sạch; health/build hiện trạng chạy. |
| AC2 — mapping service khớp registry | P01-05 | Bắt buộc | Registry + Compose/Vite + listener read-only. |
| AC3 — URL loopback/proxy được xác minh bằng HTTP/browser | P01-06 | Bắt buộc | IPv4 direct, Vite proxy, Caddy app hostname và Chrome UI. IPv6 không được cấu hình theo capability registry hiện hành. |
| Demo môi trường sạch, DB down và không có agent | C03, P01-02, P01-07 | Bắt buộc | Không dừng DB hoặc reset runtime; kiểm source, unit negative case và UI read-only. |
| C01–C08 theo RULES | C01–C08 | Bắt buộc | Có record riêng từng case bên dưới. |

## Tổng hợp

| Tag | Số test |
| --- | ---: |
| clean | 11 |
| need-change | 4 |
| suggestion | 0 |

| Result | Số test |
| --- | ---: |
| pass | 11 |
| fail | 1 |
| blocked | 3 |
| not-run | 0 |
| not-applicable | 0 |

## Kết quả từng test

### C01 — Phạm vi và dirty worktree

- Nguồn/tiêu chí: [RULES C01](../../../RULES.md); [checklist Phase 01](../../../phases/phase-01.md).
- Bắt buộc: có
- Điều kiện/môi trường: Chỉ Phase 01; checkout dirty có tài liệu/pipeline của lượt trước.
- Bước/lệnh: `rtk proxy git status --short`; đối chiếu manifest r002 và source hashes hiện tại.
- Kỳ vọng: Không sửa Phase khác, không mất thay đổi người dùng, report tách biệt theo batch.
- Thực tế: Không sửa source. Runtime/lockfile/README/checklist Phase 01 khớp r002; master-plan thay đổi do ghi trạng thái chờ review và nhật ký. Batch/evidence mới nằm đúng scope Phase 01.
- Kết quả phản biện: none
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [source-review](evidence/source-review.md), [manifest](evidence/source-manifest.json).
- Xử lý/đề xuất: Không.

### C02 — Dependency và nguồn quyết định

- Nguồn/tiêu chí: [Phase 01 roadmap](../../../../master-plan.md); [ADR](../../../../decisions/0001-v1-foundation.md); Dev Hub registry; AGENTS runtime rules.
- Bắt buộc: có
- Điều kiện/môi trường: Đối chiếu read-only, không reserve hoặc đổi port.
- Bước/lệnh: Đọc dependency Phase 00, README/ADR/AGENTS, registry service block và test hiện trạng.
- Kỳ vọng: Phase 01 chỉ dựa Phase 00; port/hostname và giới hạn phù hợp registry/capability.
- Thực tế: Phase 00 là dependency; registry block 15500–15599 khớp web 15500, API 15501, PostgreSQL 15510. App hostname proxy bật trên IPv4; API subdomain không bật proxy. Spec/ADR không cấp inference grant.
- Kết quả phản biện: none
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [routes](evidence/routes.md), [source-review](evidence/source-review.md), [registry entry](../../../../../../dev-hub/projects.yml).
- Xử lý/đề xuất: Không.

### C03 — Mapping tiêu chí và demo

- Nguồn/tiêu chí: AC1–AC3 roadmap; demo bắt buộc: khởi động môi trường sạch và xem health khi DB down.
- Bắt buộc: có
- Điều kiện/môi trường: Runtime Phase 04 đang dùng DB; không được dừng/reset DB hoặc tạo môi trường migration.
- Bước/lệnh: Đối chiếu AC với P01 IDs; review live app/health và source test.
- Kỳ vọng: Mapping đủ; demo xác nhận được hướng dẫn từ sạch và nhánh DB-down trên environment riêng.
- Thực tế: Mapping đủ, trang/health hiện chạy; chưa chạy lại toàn demo môi trường sạch + DB-down vì không có DB/runtime cô lập được cấp cho lượt này. Dữ liệu demo Phase 04 hiện có nên trang này không chứng minh thời điểm seed.
- Kết quả phản biện: none
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Evidence: [phase checklist](../../../phases/phase-01.md), [routes](evidence/routes.md), [commands](evidence/commands.md).
- Xử lý/đề xuất: Chạy demo trong môi trường riêng khi được cấp; không dừng DB dùng chung.

### C04 — Không gọi model/tool âm thầm

- Nguồn/tiêu chí: RULES C04; inference grant hiện tại = 0; Phase 01 chỉ cần health.
- Bắt buộc: có
- Điều kiện/môi trường: GET health/app; không bấm gateway probe.
- Bước/lệnh: Trace `main.py`, `App.tsx`, gateway adapter; mở trang Cấu hình & sức khỏe; gọi GET health.
- Kỳ vọng: Startup/health không gửi chat/session/tool; gateway probe chỉ thực hiện khi chủ động yêu cầu.
- Thực tế: API health chỉ trả liveness/readiness; UI chỉ gọi health và GET demo dashboard; source cho thấy gateway probe gắn nút riêng, adapter chỉ GET health/models. UI hiển thị “Chưa chạy probe trong phiên này”; batch không gửi model request.
- Kết quả phản biện: none
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [source review](evidence/source-review.md), [routes](evidence/routes.md).
- Xử lý/đề xuất: Không.

### C05 — Secret và scope dữ liệu

- Nguồn/tiêu chí: RULES C05; Phase 01 secret local; demo/real tách biệt.
- Bắt buộc: có
- Điều kiện/môi trường: Metadata `.env` בלבד; không in/đọc nội dung.
- Bước/lệnh: `rtk proxy stat -f '%Sp %N' .env`; `rtk proxy git check-ignore -v .env`; đọc `.env.example`.
- Kỳ vọng: `.env` mode 0600, bị ignore; mẫu chỉ có giá trị hướng dẫn; không dùng/reset dữ liệu thật.
- Thực tế: Mode `0600`, `.env` match `.gitignore`; `.env.example` chỉ chứa hướng dẫn và giá trị sinh tự động. Không đọc secret; không ghi/xóa DB.
- Kết quả phản biện: none
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [commands](evidence/commands.md), [source review](evidence/source-review.md).
- Xử lý/đề xuất: Không.

### C06 — Tài liệu, ngôn ngữ và trình duyệt

- Nguồn/tiêu chí: RULES C06; Phase 01 trang health local, `lang=vi`, favicon.
- Bắt buộc: có
- Điều kiện/môi trường: Browser Chrome qua Caddy hostname IPv4; không thao tác ghi.
- Bước/lệnh: Đọc source HTML; GET trang/favicon/health; mở Chrome tab mới tới `/#settings`.
- Kỳ vọng: Trang tiếng Việt tải được, favicon hợp lệ, API/DB hiển thị trạng thái thực.
- Thực tế: `lang="vi"`; favicon HTTP 200; Chrome accessibility tree cho thấy trang Cấu hình & sức khỏe, API và PostgreSQL “Đang hoạt động”; same-origin readiness và hostname health đều trả 200/DB ok.
- Kết quả phản biện: none
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [routes](evidence/routes.md), [source review](evidence/source-review.md).
- Xử lý/đề xuất: Không.

### C07 — Regression trực tiếp

- Nguồn/tiêu chí: Health routes, Vite proxy, web production build; Phase 01 בלבד.
- Bắt buộc: có
- Điều kiện/môi trường: Test health dùng ASGI/mock DB; build trên checkout, không chạy suite ghi DB của Phase 03–04.
- Bước/lệnh: `rtk proxy uv run --project apps/api pytest apps/api/tests/test_health.py -q`; `rtk proxy npm run --prefix apps/web build`; GET live/ready.
- Kỳ vọng: Health contract/error sanitization tests pass; TypeScript/Vite build và runtime health pass.
- Thực tế: 3/3 health tests pass, web build exit 0; direct API, Vite proxy, Caddy hostname health đều 200. Lệnh cài README riêng fail ở P01-01.
- Kết quả phản biện: none
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [commands](evidence/commands.md), [routes](evidence/routes.md).
- Xử lý/đề xuất: Regression không thay cho xử lý finding cài đặt P01-01.

### C08 — Report có thể tái kiểm định

- Nguồn/tiêu chí: RULES C08; report template.
- Bắt buộc: có
- Điều kiện/môi trường: Batch r004; evidence chỉ chứa kết quả đã lọc.
- Bước/lệnh: Kiểm đầy đủ IDs/tags/links; chạy validator `--batch` sau khi lưu.
- Kỳ vọng: 15 cases C01–C08/P01-01…07; đúng tag/result, source manifest, evidence links tồn tại; không chứa secrets.
- Thực tế: Validator pass cấu trúc 24 checklist, 171 definitions, HTML sync và đủ 15 report cases; batch-local counts khớp 11 pass + 1 fail + 3 blocked; 6 Markdown files trong batch có local links tồn tại. Validator không chấm nội dung evidence. Chi tiết [validation evidence](evidence/validation.md).
- Kết quả phản biện: none
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [manifest](evidence/source-manifest.json), [commands](evidence/commands.md), [routes](evidence/routes.md).
- Xử lý/đề xuất: Không.

### P01-01 — Cài và chạy local

- Nguồn/tiêu chí: AC1; [README setup](../../../../../README.md).
- Bắt buộc: có
- Điều kiện/môi trường: Bản sao sạch của `apps/web`, không cài vào worktree dùng chung.
- Bước/lệnh: Tái hiện `rtk proxy npm ci --prefix` trỏ tới thư mục web tạm từ root; sau đó chạy `rtk proxy npm ci` với cwd là thư mục web tạm; build checkout hiện tại.
- Kỳ vọng: Lệnh README cài dependency theo lockfile trong môi trường sạch; app build được.
- Thực tế: README command exit 1 (`EUSAGE`, `Missing: web@0.0.0 from lock file`); lệnh cwd `apps/web` exit 0 (28 packages, audit 0 vulnerabilities). Build hiện trạng exit 0. Đây là lỗi setup có workaround.
- Kết quả phản biện: none
- Tag: need-change
- Kết quả: fail
- Mức độ: major
- Evidence: [finding](evidence/finding-p01-01.md), [commands](evidence/commands.md).
- Xử lý/đề xuất: Remake sửa hướng dẫn setup sang lệnh đã xác minh rồi chạy retest độc lập; không sửa source trong vai trò tester.

### P01-02 — Liveness và readiness

- Nguồn/tiêu chí: AC1; demo Phase 01; [health checklist](../../../phases/phase-01.md).
- Bắt buộc: có
- Điều kiện/môi trường: Runtime DB dùng chung; không được stop/fault. Unit failure test an toàn.
- Bước/lệnh: Chạy `test_health.py`; GET liveness/readiness direct + Vite/Caddy proxy; đọc `main.py`.
- Kỳ vọng: Liveness luôn 200; readiness phản ánh DB; khi DB down trả 503 đã lọc và UI báo trạng thái.
- Thực tế: Unit suite 3 pass, gồm DB failure mock 503 không lộ exception; các endpoint live hiện 200 khi DB sẵn. Không thực hiện outage runtime vì DB dùng chung.
- Kết quả phản biện: none
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Evidence: [commands](evidence/commands.md), [routes](evidence/routes.md), [source review](evidence/source-review.md).
- Xử lý/đề xuất: Cần môi trường riêng để chạy demo live DB-down; tuyệt đối không dừng DB hiện hữu.

### P01-03 — Migration baseline

- Nguồn/tiêu chí: AC1; baseline migration Phase 01.
- Bắt buộc: có
- Điều kiện/môi trường: DB hiện hữu đang ở head 0003, được phase khác sử dụng.
- Bước/lệnh: Chỉ chạy `alembic current` read-only.
- Kỳ vọng: Upgrade từ DB sạch tạo baseline đúng, idempotent, không có domain schema phase sau.
- Thực tế: DB hiện tại là `20261008_0003 (head)`. Không chạy upgrade/migration trên DB này; batch r004 không có DB sạch cấp riêng, nên migration baseline chưa được rerun độc lập.
- Kết quả phản biện: none
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Evidence: [commands](evidence/commands.md); source-only/hash comparison tại [manifest](evidence/source-manifest.json).
- Xử lý/đề xuất: Chạy upgrade/current/idempotency trên DB cô lập trong batch được cấp.

### P01-04 — Secret local

- Nguồn/tiêu chí: AC1; Spec secret handling.
- Bắt buộc: có
- Điều kiện/môi trường: Chỉ metadata, không đọc `.env`.
- Bước/lệnh: stat mode và Git ignore; đọc mẫu `.env.example`.
- Kỳ vọng: Mode 0600, file bị ignore, template không chứa secret thật.
- Thực tế: Mode 0600; `.env` bị ignore; mẫu chỉ có các giá trị sinh bằng script.
- Kết quả phản biện: none
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [commands](evidence/commands.md).
- Xử lý/đề xuất: Không.

### P01-05 — Registry và binds

- Nguồn/tiêu chí: AC2; Dev Hub registry và Runtime Phase 01.
- Bắt buộc: có
- Điều kiện/môi trường: Read-only toàn block/registry/listener; không đổi cấu hình.
- Bước/lệnh: Đối chiếu registry, Compose, Vite, README và `lsof`.
- Kỳ vọng: Service mapping đúng block; tất cả service publish local-only theo capability Chủ tịch đã xác nhận.
- Thực tế: Registry 15500 web, 15501 API, 15510 PostgreSQL khớp Compose/Vite/README. Listener chỉ `127.0.0.1` IPv4. Caddy app hostname bật proxy IPv4; API/database hostname không proxy. IPv6 không được bind trong môi trường này.
- Kết quả phản biện: none
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [routes](evidence/routes.md), [source review](evidence/source-review.md), registry entry qua [C02](#c02--dependency-và-nguồn-quyết-định).
- Xử lý/đề xuất: Không.

### P01-06 — URL đã xác minh

- Nguồn/tiêu chí: AC3; hostname/dev route hiện được publish.
- Bắt buộc: có
- Điều kiện/môi trường: Chỉ IPv4 loopback; Chrome dùng hostname app đã đăng ký.
- Bước/lệnh: GET trang/favicon/API health/Vite proxy/app hostname; mở Chrome tại `agent-corporation.localhost/#settings`.
- Kỳ vọng: Đúng app và readiness qua đường công bố; browser hiển thị trạng thái dịch vụ; không claim IPv6.
- Thực tế: Tất cả URL được công bố trả 200; browser hiển thị đúng trang và API/DB đang hoạt động. Listener chỉ loopback IPv4. API subdomain có registry `proxy_enabled: false` nên không được coi là URL đã công bố.
- Kết quả phản biện: none
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [routes](evidence/routes.md).
- Xử lý/đề xuất: Không.

### P01-07 — Chưa có agent/inference

- Nguồn/tiêu chí: Phase 01 giới hạn; grant mặc định 0.
- Bắt buộc: có
- Điều kiện/môi trường: Landing/settings, health GET và source trace; không probe gateway.
- Bước/lệnh: Đọc API startup/routes, UI initialization và factory; mở landing/settings read-only.
- Kỳ vọng: Không tạo real company, chạy worker/agent, seed/reset tự động, hoặc gọi model khi mở trang/health.
- Thực tế: Không có startup hook; GET demo dashboard chỉ đọc; reset riêng POST sau confirmation; gateway probe chỉ khi bấm nút, không bấm. UI hiện có demo fixture Phase 04 từ môi trường trước đó; lượt này không xác nhận thời điểm tạo fixture.
- Kết quả phản biện: none
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [source review](evidence/source-review.md), [routes](evidence/routes.md).
- Xử lý/đề xuất: Không.

## Bypass attempts

| Ranh giới | Cách thử | Kết quả | Severity |
| --- | --- | --- | --- |
| Inference grant = 0 | Mở trang/check health thay vì gateway probe | Chỉ health + dashboard GET; source cho thấy probe chỉ từ nút; không gọi model | PASS / info |
| Demo không tự seed/reset | GET landing/dashboard; reset cần POST và confirmation | GET dashboard chỉ đọc; không gửi POST; thời điểm tạo fixture hiện có chưa xác định | PASS / info |
| Local-only services | Đối chiếu listeners trong toàn block | Web/API/DB chỉ bind `127.0.0.1`; IPv6/ingress LAN không được tuyên bố | PASS / info |
| Auth/business route bypass | Tìm route auth Phase 01 | Phase 01 không cung cấp auth route; không kiểm thử bypass quyền của phase sau | NOT APPLICABLE |

## Regression coverage

Health unit tests 3/3 pass; API live/ready direct và qua Vite/Caddy hostname đều trả đúng khi DB hoạt động; favicon và app page 200; production build pass. Không chạy toàn bộ backend suite vì fixtures Phase 03–04 kết nối DB dùng chung và có INSERT/DELETE. Không chạy migration, outage hoặc seed.

## Tested, not tested và bị chặn

- Đã kiểm: source và hash Phase 01; Dev Hub mapping; secret metadata; health unit; web build; direct/proxy HTTP; Chrome settings UI; npm install command README trong temp clean copy và workaround canonical.
- Chưa chạy: toàn bộ demo khởi động từ môi trường sạch và browser hiển thị DB-down (C03/P01-02); migration từ DB sạch/idempotency (P01-03); IPv6 bind (capability hiện không hỗ trợ và không được yêu cầu).
- Không thể an toàn ở lượt này: stop/fault/reset/migrate DB Phase 04 đang dùng; chạy toàn suite chứa test DB-writing.
- Kết quả kỹ thuật: cần sửa do P01-01 fail; ngoài ra còn blocker evidence cho demo/migration độc lập.

## Thứ tự xử lý

### Must fix

- P01-01 (major theo checklist phase; P2 theo release QA): sửa README cài frontend, kiểm lại clean install từ đúng working directory.

### Should fix

- C03/P01-02 và P01-03: chạy trên môi trường test cô lập để chứng minh demo DB-down và migration baseline; không dùng DB hiện tại.

### Can defer

- Không có issue tùy chọn riêng.

### Ignore / acceptable

- IPv6 listener không hỗ trợ là giới hạn đã ghi trong registry và runtime rules; chỉ công bố IPv4 loopback.
- `api.agent-corporation.localhost` không nằm trong service proxy được bật; không xem là endpoint Phase 01 công bố.

## Automation recommendations

- Thêm smoke check CI cho đúng lệnh cài ghi trong README từ bản sao sạch để tránh lệch cwd/`--prefix`.
- Giữ health failure test ở unit layer; demo DB-down và migration baseline chạy trên PostgreSQL test cô lập.

## Final recommendation

Remake Phase 01 theo finding P01-01, sau đó giao AI test độc lập retest bằng report r004. P01-02/P01-03 chỉ được đóng khi có environment riêng và evidence chạy lại; không suy ra từ `alembic current` trên DB hiện tại hoặc report self-retest r002. Không tự nghiệm thu Phase 01.
