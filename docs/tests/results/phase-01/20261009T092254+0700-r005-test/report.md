# Kiểm định độc lập Phase 01 — 20261009T092254+0700-r005-test

## Thông tin batch

- Phase: 01
- Test batch: 20261009T092254+0700-r005-test
- Vòng: r005
- Bắt đầu / kết thúc: 2026-10-09 09:22:54 / 09:27:24 +07:00 (Asia/Ho_Chi_Minh)
- Người/AI kiểm định: `/root/independent_phase01_test`.
- Độc lập với AI triển khai/remake: Có; remake r004 do `/root` thực hiện.
- Yêu cầu/phạm vi được giao: Retest độc lập sau remake r004; Phase 01 only; tái chạy clean setup, demo startup, DB-down, baseline migration.
- Source: `e44bc19783e15b29311f467a2be86943b76d847f` + dirty worktree; [manifest/hash](evidence/source-manifest.json); [source review](evidence/source-review.md).
- Môi trường/config/tool versions: macOS arm64; Node 24.21.0/npm 11.19.0; Python 3.14.8/uv 0.12.23; Docker 20.10.23; PostgreSQL 18.6-alpine pinned digest; [commands](evidence/commands.md).
- Inference: Không gọi; grant = 0; không gateway probe.
- Dependency/quyết định nghiệm thu: Phase 01 phụ thuộc Phase 00 đã nghiệm thu baseline. Master plan hiện `Chờ nghiệm thu`; r005 không đổi trạng thái này.
- Supersedes: [r004](../20261009T091446+0700-r004-test/report.md) và retest lỗi setup của [r003](../20261009T091040+0700-r003-test/report.md); xác minh remake r004.
- Remake nguồn: [remake r004](../../../../remakes/phase-01/20261009T092011+0700-r004-remake/remake.md).
- Kết luận kỹ thuật: đạt
- Quyết định Chủ tịch: Chưa có quyết định nghiệm thu mới.

## Mapping tiêu chí

| Tiêu chí hiện tại / nguồn | Test IDs | Bắt buộc / tùy điều kiện | Ghi chú |
| --- | --- | --- | --- |
| AC1 — Lệnh cài/chạy/check hoạt động thực tế, không cần secret trong Git | P01-01…P01-04 | Bắt buộc | Exact README command trên bản sao sạch; demo/health; secret metadata và DB baseline. |
| AC2 — Mapping service khớp registry | P01-05 | Bắt buộc | Registry và listener read-only. |
| AC3 — URL chỉ được báo sau khi kiểm tra IPv4/proxy/browser | P01-06 | Bắt buộc | Direct/proxy/hostname GET và browser. |
| Demo môi trường sạch, khi DB dừng health báo lỗi đúng | C03, P01-02, P01-03 | Bắt buộc | Demo database, baseline database tách riêng; test outage live trong stack riêng. |
| Ranh giới scope/inference/evidence | C01–C08, P01-07 | Bắt buộc | Không chạm runtime/DB dùng chung; inference grant = 0. |

## Tổng hợp

| Tag | Số test |
| --- | ---: |
| clean | 15 |
| need-change | 0 |
| suggestion | 0 |

| Result | Số test |
| --- | ---: |
| pass | 15 |
| fail | 0 |
| blocked | 0 |
| not-run | 0 |
| not-applicable | 0 |

## Kết quả từng test

### C01 — Phạm vi và diff

- Nguồn/tiêu chí: [RULES C01](../../../RULES.md); [checklist Phase 01](../../../phases/phase-01.md).
- Bắt buộc: có
- Điều kiện/môi trường: Dirty worktree có thay đổi do remake r004 và điều phối; test không sửa product source.
- Bước/lệnh: `git status --short`; đối chiếu remake source manifest và hash r005.
- Kỳ vọng: Chỉ Phase 01, giữ thay đổi người dùng, không thay trạng thái ngoài quyền.
- Thực tế: Chỉ kiểm Phase 01; README đúng diff remediation r004; không thay source/product, DB, runtime, proxy hay master plan. Artifacts chỉ nằm trong batch test r005 và sổ kết quả Phase 01.
- Kết quả phản biện: none
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [manifest](evidence/source-manifest.json), [source review](evidence/source-review.md).
- Xử lý/đề xuất: Không.

### C02 — Dependency và nguồn quyết định

- Nguồn/tiêu chí: [master plan](../../../../master-plan.md); [ADR](../../../../decisions/0001-v1-foundation.md); [Phase 01 checklist](../../../phases/phase-01.md).
- Bắt buộc: có
- Điều kiện/môi trường: Read-only đối chiếu scope, trạng thái và dependency.
- Bước/lệnh: Đọc dependency Phase 00, README, product spec/ADR, report r004/remake r004 và registry.
- Kỳ vọng: Dependency được đáp ứng; report mới kiểm tra đúng remake; không tự nghiệm thu phase.
- Thực tế: Phase 00 baseline là dependency đã nghiệm thu. README command sau remake đã được kiểm thực tế; Phase 01 vẫn `Chờ nghiệm thu`.
- Kết quả phản biện: none
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [source review](evidence/source-review.md), [remake r004](../../../../remakes/phase-01/20261009T092011+0700-r004-remake/remake.md).
- Xử lý/đề xuất: Không.

### C03 — Mapping tiêu chí và demo

- Nguồn/tiêu chí: AC1–AC3; demo bắt buộc trong [master plan](../../../../master-plan.md).
- Bắt buộc: có
- Điều kiện/môi trường: Bản sao sạch web/API và database demo isolated; fixture chỉ ở DB batch.
- Bước/lệnh: Cài/chạy app từ copy sạch, provision và seed tường minh fixture demo trong DB riêng; kiểm dashboard/browser và DB-down flow.
- Kỳ vọng: Criteria ánh xạ đủ; demo mở được; lỗi database hiển thị khi DB ngừng.
- Thực tế: Browser mở demo `Demo Corporation · fixture`; liveness/readiness và dữ liệu demo hoạt động trước khi dừng DB; sau khi dừng DB riêng, UI báo PostgreSQL “Chưa kết nối”, readiness chưa đạt và demo không đọc được.
- Kết quả phản biện: none
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [commands](evidence/commands.md), [browser](evidence/browser.md), [routes](evidence/routes.md).
- Xử lý/đề xuất: Không.

### C04 — Không thực thi model/tool âm thầm

- Nguồn/tiêu chí: [RULES C04](../../../RULES.md); grant = 0; Phase 01 không có worker/agent.
- Bắt buộc: có
- Điều kiện/môi trường: GET app/health/dashboard; một POST reset fixture tường minh trong DB test để dựng demo; không probe gateway.
- Bước/lệnh: Review UI/API routes/source; theo dõi log API riêng; không bấm gateway probe.
- Kỳ vọng: Không có inference/chat/session/tool khi app mở/health; fixture chỉ được tạo bởi thao tác seed tường minh.
- Thực tế: API log chỉ có health/dashboard GET, một POST reset fixture explicit trong DB test, rồi health/dashboard GET; không chat/session/model/tool request. UI ghi inference grant 0; gateway probe chưa chạy.
- Kết quả phản biện: none
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [source review](evidence/source-review.md), [commands](evidence/commands.md), [browser](evidence/browser.md).
- Xử lý/đề xuất: Không.

### C05 — Secret và scope dữ liệu

- Nguồn/tiêu chí: [RULES C05](../../../RULES.md); P01-04; Spec §10/12.
- Bắt buộc: có
- Điều kiện/môi trường: Chỉ metadata `.env`; test databases và fixed demo scope được cô lập.
- Bước/lệnh: `stat`; `git check-ignore`; đọc `.env.example`; đối chiếu resource/container/database IDs.
- Kỳ vọng: Không đọc/ghi secret thật; không truy cập hoặc reset shared DB; demo/benchmark/real tách scope.
- Thực tế: `.env` mode 600 và bị Git ignore; template chỉ placeholder. Migration và demo fixture chỉ nằm trong hai DB của container kiểm thử; dừng đúng container test, không dùng named project volume.
- Kết quả phản biện: none
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [commands](evidence/commands.md), [manifest](evidence/source-manifest.json).
- Xử lý/đề xuất: Không.

### C06 — Tài liệu và browser

- Nguồn/tiêu chí: [RULES C06](../../../RULES.md); README/setup instructions; Phase 01 ngôn ngữ/favicons.
- Bắt buộc: có
- Điều kiện/môi trường: Clean app copy và hostname app hiện hành.
- Bước/lệnh: Đối chiếu README exact command; GET favicon; đọc accessibility tree khi DB sẵn và DB dừng.
- Kỳ vọng: Tiếng Việt, favicon hoạt động, lỗi trạng thái kết nối có thể quan sát; tài liệu không nâng status phase.
- Thực tế: `lang=vi`; favicon SVG HTTP 200; Chrome hiển thị trạng thái khỏe/lỗi tương ứng; README install command pass. Master plan vẫn `Chờ nghiệm thu`.
- Kết quả phản biện: none
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [browser](evidence/browser.md), [routes](evidence/routes.md), [commands](evidence/commands.md).
- Xử lý/đề xuất: Không.

### C07 — Regression trực tiếp

- Nguồn/tiêu chí: P01-01/02/03 và health/website behavior.
- Bắt buộc: có
- Điều kiện/môi trường: Clean install copy; DB-down tests dùng isolated container; shared Phase 04 DB không ghi.
- Bước/lệnh: Health unit suite, build/lint, exact npm README install, baseline migration, integration route checks.
- Kỳ vọng: Không tái phát finding; API liveness/readiness và web proxy giữ contract.
- Thực tế: Cài frontend theo README pass; 3 health tests pass; build/lint pass; baseline migration idempotent; API/Vite pass/fail health statuses đúng theo DB up/down.
- Kết quả phản biện: none
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [commands](evidence/commands.md), [routes](evidence/routes.md).
- Xử lý/đề xuất: Không.

### C08 — Report có thể tái kiểm định

- Nguồn/tiêu chí: [RULES C08](../../../RULES.md); [report template](../../../templates/report.md).
- Bắt buộc: có
- Điều kiện/môi trường: Batch r005; evidence lọc, không lưu secret/DB dump.
- Bước/lệnh: Validator với `--batch`, kiểm tra IDs/tags/links và source manifest.
- Kỳ vọng: 15 ca đầy đủ; local links tồn tại; report không đánh dấu phase hoàn tất.
- Thực tế: Validator batch pass; đủ 15 ca C01–C08/P01-01…P01-07; Phase 01 vẫn `Chờ nghiệm thu`.
- Kết quả phản biện: none
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [validation](evidence/validation.md), [source manifest](evidence/source-manifest.json).
- Xử lý/đề xuất: Không.

### P01-01 — Cài và chạy local

- Nguồn/tiêu chí: AC1; [README](../../../../../README.md); [P01-01 checklist](../../../phases/phase-01.md).
- Bắt buộc: có
- Điều kiện/môi trường: Clean copy; không dùng `.env`/node_modules checkout.
- Bước/lệnh: Từ root clean copy chạy đúng `npm --prefix apps/web ci`, build/lint, `uv sync --locked`; start app Vite/API và kiểm readiness.
- Kỳ vọng: Lệnh README cài theo lock; stack khởi động được với DB cô lập.
- Thực tế: Exact README command exit 0; 28 packages, không vulnerabilities; build/lint exit 0; API sync locked và health tests đạt; API/Vite copy chạy, dashboard demo 200 khi DB sẵn.
- Kết quả phản biện: none
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [commands](evidence/commands.md), [browser](evidence/browser.md).
- Xử lý/đề xuất: Đóng finding r004 bằng independent retest; không thay đổi source trong batch.

### P01-02 — Liveness và readiness

- Nguồn/tiêu chí: [P01-02 checklist](../../../phases/phase-01.md); Spec §5/12.
- Bắt buộc: có
- Điều kiện/môi trường: API copy gắn với DB test; chỉ dừng container PostgreSQL do batch tạo.
- Bước/lệnh: Kiểm health tests, gọi live/ready/dashboard khi DB sẵn; dừng test DB; gọi lại direct/Vite proxy và reload UI.
- Kỳ vọng: DB up → live 200/ready 200; DB down → live 200/ready 503 sạch; UI nêu API còn sống, DB unavailable.
- Thực tế: DB up: live/ready/dashboard 200. DB down: live 200; direct và Vite proxy ready 503 với body đã lọc; dashboard 503 generic; UI cho thấy PostgreSQL “Chưa kết nối” và thông báo readiness.
- Kết quả phản biện: none
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [commands](evidence/commands.md), [routes](evidence/routes.md), [browser](evidence/browser.md).
- Xử lý/đề xuất: Không.

### P01-03 — Migration baseline

- Nguồn/tiêu chí: [P01-03 checklist](../../../phases/phase-01.md); baseline Phase 01.
- Bắt buộc: có
- Điều kiện/môi trường: DB `p01_r005_baseline` rỗng trong PostgreSQL isolated; tách với database demo.
- Bước/lệnh: Alembic upgrade `20261008_0001` hai lần, kiểm current/version/schema.
- Kỳ vọng: Đạt baseline, upgrade lặp không thay đổi schema, không có domain tables phase sau.
- Thực tế: Hai lần exit 0; current và alembic_version đúng `20261008_0001`; public schema chỉ có `alembic_version`.
- Kết quả phản biện: none
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [commands](evidence/commands.md).
- Xử lý/đề xuất: Đóng blocker r004 bằng isolated migration retest.

### P01-04 — Secret local

- Nguồn/tiêu chí: [P01-04 checklist](../../../phases/phase-01.md); Spec §10.
- Bắt buộc: có
- Điều kiện/môi trường: Read-only metadata.
- Bước/lệnh: Kiểm mode và ignore; đọc template `.env.example`; không đọc `.env`.
- Kỳ vọng: `.env` mode 0600, bị ignore; mẫu không chứa secret thật.
- Thực tế: Mode 600, ignored; template dùng placeholder/bootstrap; không lưu/read secret.
- Kết quả phản biện: none
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [commands](evidence/commands.md).
- Xử lý/đề xuất: Không.

### P01-05 — Registry và binds

- Nguồn/tiêu chí: [P01-05 checklist](../../../phases/phase-01.md); AGENTS runtime mapping.
- Bắt buộc: có
- Điều kiện/môi trường: Registry/listener read-only.
- Bước/lệnh: Đối chiếu Dev Hub, Compose, Vite, README và toàn block listen sockets.
- Kỳ vọng: Mapping đúng allocation; project local-only; không ingress LAN.
- Thực tế: Registry block `15500–15599`, web/API/PG `15500/15501/15510`; Compose/Vite/README khớp; listener là 127.0.0.1 IPv4; app hostname proxy IPv4-only.
- Kết quả phản biện: none
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [routes](evidence/routes.md), [source review](evidence/source-review.md).
- Xử lý/đề xuất: Không.

### P01-06 — URL đã xác minh

- Nguồn/tiêu chí: [P01-06 checklist](../../../phases/phase-01.md); AC3.
- Bắt buộc: có
- Điều kiện/môi trường: GET IPv4 direct, hostname proxy, browser; không cấu hình IPv6.
- Bước/lệnh: GET route trực tiếp/proxy/favicon và mở Chrome.
- Kỳ vọng: Response đúng app; UI mở được qua hostname; chỉ công bố đường đã xác minh.
- Thực tế: Direct web/API và hostname web/readiness HTTP 200; favicon SVG 200; Chrome hiển thị đúng trang settings. Không claim IPv6 hoặc API subdomain.
- Kết quả phản biện: none
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [routes](evidence/routes.md), [browser](evidence/browser.md).
- Xử lý/đề xuất: Không.

### P01-07 — Chưa có agent

- Nguồn/tiêu chí: [P01-07 checklist](../../../phases/phase-01.md); giới hạn Phase 01.
- Bắt buộc: có
- Điều kiện/môi trường: Source trace và UI/network quan sát; no inference grant.
- Bước/lệnh: Đọc startup/routes/demo and gateway call path; browser load and HTTP access log review.
- Kỳ vọng: Không có worker/agent/model call/seed tự phát; seed fixture chỉ qua thao tác rõ ràng.
- Thực tế: Browser startup phát GET health/dashboard; fixture chỉ được seed bằng explicit POST `confirmed=true` trong DB test. Không gọi gateway/probe; grant 0; không tạo real company hay agent.
- Kết quả phản biện: none
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [source review](evidence/source-review.md), [commands](evidence/commands.md), [browser](evidence/browser.md).
- Xử lý/đề xuất: Không.

## Integration / release gates

| Gate áp dụng | PASS / FAIL / BLOCKED | Test IDs | Batch/grant/config/evidence và gate trước |
| --- | --- | --- | --- |
| Không có IG riêng cho Phase 01 | — | — | Checklist Phase 01; inference grant = 0. |

## Cleanup, giới hạn và bàn giao

- Cleanup: Container isolated đã dừng/tự xóa; API/Vite test processes dừng; temp source/dependencies xóa. DB/API/Vite/Caddy dùng chung không bị dừng/restart hoặc mutate.
- Chưa kiểm chứng: Không có case checklist bắt buộc còn thiếu trong phạm vi Phase 01; không claim IPv6.
- Cần sửa: Không phát hiện issue mở sau remake r004.
- Đề xuất tùy chọn: Không có.
- Bước tiếp theo: Bàn giao Chủ tịch nghiệm thu Phase 01. Không đổi status Markdown, không đánh dấu Hoàn tất, không mở phase kế tiếp.
- Bàn giao: [commands](evidence/commands.md), [routes](evidence/routes.md), [browser](evidence/browser.md), [source review](evidence/source-review.md), [manifest](evidence/source-manifest.json), [validation](evidence/validation.md).

