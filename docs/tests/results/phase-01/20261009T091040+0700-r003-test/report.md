# Kiểm định độc lập Phase 01 — 20261009T091040+0700-r003-test

## Thông tin batch

- Phase: 01
- Test batch: 20261009T091040+0700-r003-test
- Vòng: r003
- Bắt đầu / kết thúc: 2026-10-09 09:10:40 / 09:18:30 +07:00 (Asia/Ho_Chi_Minh)
- Người/AI kiểm định: `/root/independent_phase01_test`
- Độc lập với AI triển khai/remake: Có; remake do `/root` thực hiện, kiểm định này là agent khác.
- Yêu cầu/phạm vi được giao: Kiểm định độc lập sau remake Phase 01; chỉ Phase 01, không sửa source.
- Source: `e44bc19783e15b29311f467a2be86943b76d847f` + dirty worktree; [manifest và hash nguồn](evidence/source-manifest.json); [rà soát source](evidence/source-review.md).
- Môi trường/config/tool versions: macOS arm64; Node 24.21.0/npm 11.19.0; uv 0.12.23; Docker Server 20.10.23; PostgreSQL 18.6-alpine pinned digest; [lệnh và kết quả](evidence/commands.md).
- Inference: Không gọi; grant = 0; không probe Codex Server.
- Dependency/quyết định nghiệm thu: Phase 01 phụ thuộc Phase 00; Phase 00 được nghiệm thu về spec/baseline. Phase 01 đang `Chờ nghiệm thu`; report này không tự đổi trạng thái đó.
- Supersedes: [r002](../20261009T085957+0700-r002-test/report.md) — thay bằng kiểm định độc lập, không sửa report nguồn.
- Remake nguồn: [r001](../../../../remakes/phase-01/20261009T085800+0700-r001-remake/remake.md).
- Kết luận kỹ thuật: cần sửa
- Quyết định Chủ tịch: Chưa có quyết định nghiệm thu mới.

## Mapping tiêu chí

| Tiêu chí hiện tại / nguồn | Test IDs | Bắt buộc / tùy điều kiện | Ghi chú |
| --- | --- | --- | --- |
| AC1 — Lệnh cài/chạy/check thực tế, không cần secret trong Git | P01-01…P01-04 | Bắt buộc | Clean install/build, API/Vite startup, health, isolated migration và secret metadata. |
| AC2 — Mapping service khớp registry và listener trong block | P01-05 | Bắt buộc | Registry và listen sockets read-only. |
| AC3 — Chỉ công bố URL sau khi xác minh IPv4/proxy/browser | P01-06 | Bắt buộc | HTTP direct/proxy, favicon đúng path, Chrome accessibility tree. |
| Bảo vệ scope, dữ liệu và không tự chạy agent/inference | C01–C08, P01-07 | Bắt buộc | RULES.md và checklist Phase 01. |

## Tổng hợp

| Tag | Số test |
| --- | ---: |
| clean | 14 |
| need-change | 1 |
| suggestion | 0 |

| Result | Số test |
| --- | ---: |
| pass | 14 |
| fail | 1 |
| blocked | 0 |
| not-run | 0 |
| not-applicable | 0 |

## Kết quả từng test

### C01 — Phạm vi và diff

- Nguồn/tiêu chí: [Checklist Phase 01](../../../phases/phase-01.md); [RULES C01](../../../RULES.md).
- Bắt buộc: có
- Điều kiện/môi trường: Checkout dirty; không thay đổi source trong đợt test.
- Bước/lệnh: `git status --short`; `git diff -- apps/web apps/api README.md compose.yml docs/tests/phases/phase-01.md`; đối chiếu manifest.
- Kỳ vọng: Chỉ kiểm Phase 01, giữ thay đổi người dùng và không triển khai phase khác.
- Thực tế: Không có thay đổi Phase 01 product source do test/remake r001; các thay đổi roadmap/instructions/results sẵn có được giữ nguyên. Không commit, inference hay phase khác.
- Kết quả phản biện: none
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [source manifest](evidence/source-manifest.json).
- Xử lý/đề xuất: Không có.

### C02 — Dependency và nguồn quyết định

- Nguồn/tiêu chí: [Master plan](../../../../master-plan.md); [Phase 01 checklist](../../../phases/phase-01.md); [ADR-0001](../../../../decisions/0001-v1-foundation.md).
- Bắt buộc: có
- Điều kiện/môi trường: Đọc dependency, scope và trạng thái hiện tại.
- Bước/lệnh: Đối chiếu Phase 01 phụ thuộc Phase 00, REQ25/REQ26 và các nguồn hiện hành.
- Kỳ vọng: Dependency được đáp ứng; không dùng checkbox hoặc kết quả của cùng AI remake làm nghiệm thu.
- Thực tế: Phase 00 baseline được nghiệm thu; Phase 01 còn `Chờ nghiệm thu`. Kiểm định độc lập không ghi đè trạng thái chính thức.
- Kết quả phản biện: none
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [master plan](../../../../master-plan.md), [ADR](../../../../decisions/0001-v1-foundation.md), [source review](evidence/source-review.md).
- Xử lý/đề xuất: Không có.

### C03 — Tiêu chí và demo

- Nguồn/tiêu chí: AC1–AC3 trong [master plan](../../../../master-plan.md); [checklist](../../../phases/phase-01.md).
- Bắt buộc: có
- Điều kiện/môi trường: Browser local và clean-room install; không ghi/seed dữ liệu.
- Bước/lệnh: Đối chiếu mapping report; quan sát UI qua Chrome và HTTP; cài/build/start stack trong temp copy.
- Kỳ vọng: AC được ánh xạ đầy đủ; demo đúng loại và mở được. Việc AC1 có lệnh setup thất bại được giữ ở case P01-01.
- Thực tế: AC1–AC3 được ánh xạ tới P01-01…07. Chrome hiển thị UI `Agent Corporation · Tổng quan`, `Demo Corporation · fixture`, health sẵn sàng và inference chưa cấp; bản clean-room web/API khởi động được qua lệnh thay thế từ đúng thư mục web. Command được tài liệu hóa trong README fail và được ghi ở P01-01.
- Kết quả phản biện: none
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [browser](evidence/browser.md), [commands](evidence/commands.md).
- Xử lý/đề xuất: Không có.

### C04 — Không thực thi âm thầm

- Nguồn/tiêu chí: [RULES C04](../../../RULES.md); Phase 01 giới hạn không worker/agent/inference.
- Bắt buộc: có
- Điều kiện/môi trường: Chỉ GET health/pages; không bấm probe hoặc gửi POST.
- Bước/lệnh: Review health/router/source, UI grant/fixture; quan sát routes read-only.
- Kỳ vọng: Startup/page/health không dispatch model hoặc tool.
- Thực tế: Health chỉ liveness/readiness; UI hiển thị grant chưa cấp và fixture không gọi model; gateway probe chỉ được gắn vào thao tác tường minh, không được gọi trong batch. Không gửi prompt/session/model request.
- Kết quả phản biện: none
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [routes and scope](evidence/routes.md), [browser](evidence/browser.md).
- Xử lý/đề xuất: Không có.

### C05 — Secret và scope dữ liệu

- Nguồn/tiêu chí: [RULES C05](../../../RULES.md); Phase 01 P01-04.
- Bắt buộc: có
- Điều kiện/môi trường: Chỉ đọc metadata; môi trường PostgreSQL isolated dùng test credential giả.
- Bước/lệnh: `stat -f '%Lp %N' .env`; `git check-ignore -v .env`; kiểm tra placeholder `.env.example`.
- Kỳ vọng: `.env` mode 0600, Git ignore; không lộ giá trị secret, không dùng DB dùng chung cho migration.
- Thực tế: Mode 600 và bị ignore; `.env.example` chỉ dùng placeholder. DB migration chạy trên container mới, không mount project volume; giá trị `.env` không được đọc.
- Kết quả phản biện: none
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [commands](evidence/commands.md).
- Xử lý/đề xuất: Không có.

### C06 — Tài liệu, HTML và browser

- Nguồn/tiêu chí: [Phase 01 checklist](../../../phases/phase-01.md); các ranh giới UI Phase 01.
- Bắt buộc: có
- Điều kiện/môi trường: UI local hiện hành; không thay đổi trang.
- Bước/lệnh: Đọc accessibility tree; GET web/proxy/favicon; kiểm `lang` trong HTML.
- Kỳ vọng: UI tiếng Việt, favicon tồn tại và URL được kiểm xác nhận đúng app.
- Thực tế: Chrome đọc được tổng quan demo; HTML `lang="vi"`; `/favicon.svg` HTTP 200 ở direct/proxy (`/favicon.ico` không được khai báo và trả 404).
- Kết quả phản biện: none
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [browser](evidence/browser.md), [routes](evidence/routes.md).
- Xử lý/đề xuất: Không có.

### C07 — Regression trực tiếp

- Nguồn/tiêu chí: [P01-02](../../../phases/phase-01.md); test suite liên quan trực tiếp Phase 01.
- Bắt buộc: có
- Điều kiện/môi trường: Health unit tests; web build/lint; GET runtime read-only. Không chạy test Phase 03 ghi/xóa fixture trên DB dùng chung.
- Bước/lệnh: `pytest apps/api/tests/test_health.py -q`; `npm run --prefix apps/web build`; `npm run --prefix apps/web lint`.
- Kỳ vọng: Health semantics, web compile/lint và readiness hiện tại đều đạt.
- Thực tế: Unit test 3 passed gồm liveness, ready success, ready DB unavailable sanitized; build/lint exit 0; direct/proxy readiness 200.
- Kết quả phản biện: none
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [commands](evidence/commands.md).
- Xử lý/đề xuất: Không có.

### C08 — Report có thể tái kiểm định

- Nguồn/tiêu chí: [RULES C08](../../../RULES.md); [report template](../../../templates/report.md).
- Bắt buộc: có
- Điều kiện/môi trường: Batch r003 độc lập.
- Bước/lệnh: Đối chiếu IDs, tag/result/evidence/manifest và chạy validator batch.
- Kỳ vọng: Đủ C01–C08, P01-01…07; links hợp lệ; không đánh dấu nghiệm thu chính thức.
- Thực tế: Report có đủ 15 IDs; 14 pass và một need-change/fail. Project validator xác nhận batch đủ fields/tags/results/evidence links; master plan không bị sửa trong batch.
- Kết quả phản biện: none
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [manifest](evidence/source-manifest.json), report và [validator](evidence/validation.md).
- Xử lý/đề xuất: Không có.

### P01-01 — Cài và chạy local

- Nguồn/tiêu chí: [Phase 01 AC1/P01-01](../../../phases/phase-01.md); README runtime instructions.
- Bắt buộc: có
- Điều kiện/môi trường: Bản sao sạch từ source không có `.env`; PostgreSQL isolated.
- Bước/lệnh: Theo README chạy `npm ci --prefix $CLEAN_WEB_COPY` từ repo root; sau đó chạy workaround `npm ci` từ cwd bản sao web; `npm run build/lint`, `uv sync --locked`, health tests; start API và Vite trên port ephemeral loopback.
- Kỳ vọng: Lệnh cài được tài liệu hóa cùng pins/lock hoạt động trên môi trường sạch; web/API/PG chạy đúng stack.
- Thực tế: Command README tái hiện exit 1 với npm 11.19.0: `EUSAGE`, `Missing: web@0.0.0 from lock file`. Workaround từ cwd web pass; build/lint, API locked sync + 3 tests, isolated DB baseline, API readiness 200 và Vite root/favicon 200 đều đạt.
- Kết quả phản biện: none
- Tag: need-change
- Kết quả: fail
- Mức độ: major
- Evidence: [clean-room command log và repro](evidence/commands.md); [finding P01-01](evidence/finding-p01-01.md).
- Xử lý/đề xuất: Cập nhật README/setup command sang lệnh đã pass từ cwd `apps/web`, sau đó retest P01-01. AI test không sửa README.

### P01-02 — Liveness và readiness

- Nguồn/tiêu chí: [Phase 01 P01-02](../../../phases/phase-01.md); Spec §5/12.
- Bắt buộc: có
- Điều kiện/môi trường: PostgreSQL isolated cho API clean-room; không gây outage DB dự án.
- Bước/lệnh: Health tests và GET readiness/liveness direct/proxy.
- Kỳ vọng: Live tách ready; ready báo unavailable khi DB lỗi; ready OK khi DB hoạt động.
- Thực tế: Ba health unit tests pass; lỗi DB giả lập trả 503 với body đã sanitize; clean API readiness với DB riêng trả 200; runtime hiện tại direct/proxy trả 200.
- Kết quả phản biện: none
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [commands](evidence/commands.md), [routes](evidence/routes.md).
- Xử lý/đề xuất: Không có.

### P01-03 — Migration baseline

- Nguồn/tiêu chí: [Phase 01 P01-03](../../../phases/phase-01.md); Spec §5/7.
- Bắt buộc: có
- Điều kiện/môi trường: PostgreSQL test DB mới, không project volume.
- Bước/lệnh: Alembic upgrade tới `20261008_0001` hai lần, kiểm current và public schema.
- Kỳ vọng: Baseline đúng, idempotent, không domain schema phase sau.
- Thực tế: Hai lần upgrade exit 0; current `20261008_0001`; chỉ `public.alembic_version` tồn tại.
- Kết quả phản biện: none
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [commands](evidence/commands.md).
- Xử lý/đề xuất: Không có.

### P01-04 — Secret local

- Nguồn/tiêu chí: [Phase 01 P01-04](../../../phases/phase-01.md); Spec §10.
- Bắt buộc: có
- Điều kiện/môi trường: Local metadata và placeholder mẫu.
- Bước/lệnh: Kiểm mode, ignore và nội dung `.env.example` chỉ có placeholder; không đọc `.env`.
- Kỳ vọng: Secret cục bộ không tracked/không hiện trong UI/log/report.
- Thực tế: `.env` mode 0600, bị ignore; template dùng `GENERATE_WITH_BOOTSTRAP_SCRIPT`; không lưu credential thật.
- Kết quả phản biện: none
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [commands](evidence/commands.md).
- Xử lý/đề xuất: Không có.

### P01-05 — Registry và binds

- Nguồn/tiêu chí: [Phase 01 P01-05](../../../phases/phase-01.md); AGENTS runtime mapping.
- Bắt buộc: có
- Điều kiện/môi trường: Đọc registry/listener, không sửa allocation/proxy.
- Bước/lệnh: Đối chiếu toàn block trong registry và listener hiện thời.
- Kỳ vọng: Mapping khớp registry; local-only; không ingress LAN.
- Thực tế: Block `15500–15599`; web/API/PG lần lượt `15500/15501/15510`; listener đều `127.0.0.1`; web proxy IPv4 loopback theo registry.
- Kết quả phản biện: none
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [routes and binds](evidence/routes.md).
- Xử lý/đề xuất: Không có.

### P01-06 — URL đã xác minh

- Nguồn/tiêu chí: [Phase 01 P01-06](../../../phases/phase-01.md); README công bố local URL.
- Bắt buộc: có
- Điều kiện/môi trường: IPv4 direct và hostname proxy; browser local.
- Bước/lệnh: GET root, API health, favicon; mở UI qua Chrome.
- Kỳ vọng: Response thuộc đúng app; chỉ claim route được xác minh.
- Thực tế: Direct/proxy web và readiness đều HTTP 200; Chrome mở đúng tổng quan Agent Corporation; favicon SVG HTTP 200. Không khẳng định IPv6.
- Kết quả phản biện: none
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [routes](evidence/routes.md), [browser](evidence/browser.md).
- Xử lý/đề xuất: Không có.

### P01-07 — Chưa có agent

- Nguồn/tiêu chí: [Phase 01 P01-07](../../../phases/phase-01.md); Spec §2/10.
- Bắt buộc: có
- Điều kiện/môi trường: Browser/health GET và source review; grant inference = 0.
- Bước/lệnh: Đọc UI/source health, routers và gateway adapter; không bấm probe.
- Kỳ vọng: Không tự tạo agent/worker/seed/inference.
- Thực tế: UI chỉ hiển thị fixture; startup/health chỉ kiểm tra API/DB; không có worker dispatch trong Phase 01; không gửi prompt/session/model request.
- Kết quả phản biện: none
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [browser](evidence/browser.md), [routes](evidence/routes.md).
- Xử lý/đề xuất: Không có.

## Integration / release gates

| Gate áp dụng | PASS / FAIL / BLOCKED | Test IDs | Batch/grant/config/evidence và gate trước |
| --- | --- | --- | --- |
| Không có IG riêng cho Phase 01 | — | — | Checklist Phase 01; inference grant = 0. |

## Cleanup, giới hạn và bàn giao

- Cleanup: Đã dừng PostgreSQL test container, API/Vite test processes và xóa bản sao temp. Runtime/API/DB dự án giữ nguyên.
- Chưa kiểm chứng: Không có ca checklist bắt buộc còn thiếu. IPv6 không được claim vì bind capability hiện hành chỉ xác nhận IPv4.
- Cần sửa: P01-01 — README install command fail trên clean copy (major); sửa hướng dẫn setup và retest độc lập.
- Đề xuất tùy chọn: Không có.
- Bước tiếp theo: Remake P01-01 trong Phase 01 rồi tạo r004 independent retest. Kết luận kỹ thuật này không đổi master-plan, không đánh dấu phase hoàn tất và không mở phase tiếp.
- Bàn giao: [commands](evidence/commands.md), [routes](evidence/routes.md), [browser](evidence/browser.md), [source manifest](evidence/source-manifest.json), [batch validation](evidence/validation.md).
