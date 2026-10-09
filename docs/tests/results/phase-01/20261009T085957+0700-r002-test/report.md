# Kiểm định Phase 01 — 20261009T085957+0700-r002-test

## Thông tin batch

- Phase: 01
- Test batch: 20261009T085957+0700-r002-test
- Vòng: r002
- Bắt đầu / kết thúc: 2026-10-09 08:59:57 / 2026-10-09 09:01:33 +07:00 (Asia/Ho_Chi_Minh)
- Người/AI kiểm định: Codex
- Yêu cầu/phạm vi được giao: Remake Phase 01 theo test hiện có; chỉ Phase 01.
- Source: `e44bc19783e15b29311f467a2be86943b76d847f` + dirty worktree; [manifest](evidence/source-manifest.json) ghi hash nguồn và giới hạn.
- Môi trường/config/tool versions: macOS arm64; Node 24.21.0/npm 11.19.0; uv 0.12.23; Docker 20.10.23; PostgreSQL 18.6-alpine đúng digest trong Compose. Runtime local Phase 01 bind loopback.
- Inference: Không gọi; grant = 0.
- Dependency/quyết định nghiệm thu: Phase 00/Phase 01 đã được Chủ tịch duyệt trước đây; không đổi trạng thái chính thức.
- Supersedes: [report legacy 20261008](../20261008T154512+0700-phase01/report.md)
- Remake nguồn: [remake r001](../../../../remakes/phase-01/20261009T085800+0700-r001-remake/remake.md)
- Kết luận kỹ thuật: đạt
- Quyết định Chủ tịch: Chưa có quyết định nghiệm thu mới cho đợt remake này.

## Mapping và phạm vi kiểm định

| Tiêu chí hiện tại / nguồn | Test IDs | Bắt buộc / tùy điều kiện | Ghi chú |
| --- | --- | --- | --- |
| AC1 — lệnh cài/chạy/check không cần secret trong Git | P01-01…P01-04 | Bắt buộc | Clean install + isolated DB baseline |
| AC2 — service mapping khớp registry | P01-05 | Bắt buộc | Read-only đối chiếu |
| AC3 — URL chỉ công bố sau khi kiểm tra | P01-06 | Bắt buộc | HTTP + Chrome; IPv4-only |
| Bảo vệ scope/secret/no inference và evidence | C01–C08, P01-07 | Bắt buộc | RULES.md |

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

### C01 — Phạm vi và dirty worktree

- Nguồn/tiêu chí: [Checklist Phase 01](../../../phases/phase-01.md); [RULES C01–C08](../../../RULES.md)
- Bắt buộc: có
- Điều kiện/môi trường: Phase 01; không inference; các bước destructive/DB chạy trong môi trường cô lập nếu có.
- Bước/lệnh: Đối chiếu checklist; commands/routes ghi tại evidence được dẫn.
- Kỳ vọng: Đạt tiêu chí và có evidence tái kiểm tra; không mở rộng phase hoặc dùng quyền không được cấp.
- Thực tế: Diff review; scope Phase 01 remediation only. Existing user changes retained. New files are remake/results evidence. No Phase 02+ implementation or shared runtime changes.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [source-manifest.json](evidence/source-manifest.json)
- Xử lý/đề xuất: Không có.
### C02 — Dependency và sự nhất quán của nguồn

- Nguồn/tiêu chí: [Checklist Phase 01](../../../phases/phase-01.md); [RULES C01–C08](../../../RULES.md)
- Bắt buộc: có
- Điều kiện/môi trường: Phase 01; không inference; các bước destructive/DB chạy trong môi trường cô lập nếu có.
- Bước/lệnh: Đối chiếu checklist; commands/routes ghi tại evidence được dẫn.
- Kỳ vọng: Đạt tiêu chí và có evidence tái kiểm tra; không mở rộng phase hoặc dùng quyền không được cấp.
- Thực tế: README hiện ghi Caddy/hostname chỉ publish IPv4 loopback; nội dung khớp AGENTS.md và Dev Hub registry. Finding IPv6 trong report legacy đã được sửa ở source hiện tại trước batch này; không thay proxy.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [routes.md](evidence/routes.md)
- Xử lý/đề xuất: Không có; report nguồn là snapshot cũ.
### C03 — Mapping tiêu chí và demo

- Nguồn/tiêu chí: [Checklist Phase 01](../../../phases/phase-01.md); [RULES C01–C08](../../../RULES.md)
- Bắt buộc: có
- Điều kiện/môi trường: Phase 01; không inference; các bước destructive/DB chạy trong môi trường cô lập nếu có.
- Bước/lệnh: Đối chiếu checklist; commands/routes ghi tại evidence được dẫn.
- Kỳ vọng: Đạt tiêu chí và có evidence tái kiểm tra; không mở rộng phase hoặc dùng quyền không được cấp.
- Thực tế: AC1–AC3 tiếp tục được ánh xạ tới P01-01…P01-07 theo checklist. Clean install và start frontend/API/PostgreSQL chạy trong isolated environment; runtime/browser local cũng được kiểm read-only.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [phase-01.md](../../../phases/phase-01.md)
- Xử lý/đề xuất: Không có.
### C04 — Không gọi model/tool âm thầm

- Nguồn/tiêu chí: [Checklist Phase 01](../../../phases/phase-01.md); [RULES C01–C08](../../../RULES.md)
- Bắt buộc: có
- Điều kiện/môi trường: Phase 01; không inference; các bước destructive/DB chạy trong môi trường cô lập nếu có.
- Bước/lệnh: Đối chiếu checklist; commands/routes ghi tại evidence được dẫn.
- Kỳ vọng: Đạt tiêu chí và có evidence tái kiểm tra; không mở rộng phase hoặc dùng quyền không được cấp.
- Thực tế: Chỉ GET web/health; source health không dispatch model; adapter chỉ có probe GET ở phase sau và không được gọi. Grant=0, không có POST/session/model request trong batch.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [routes.md](evidence/routes.md)
- Xử lý/đề xuất: Không có.
### C05 — Secret và scope

- Nguồn/tiêu chí: [Checklist Phase 01](../../../phases/phase-01.md); [RULES C01–C08](../../../RULES.md)
- Bắt buộc: có
- Điều kiện/môi trường: Phase 01; không inference; các bước destructive/DB chạy trong môi trường cô lập nếu có.
- Bước/lệnh: Đối chiếu checklist; commands/routes ghi tại evidence được dẫn.
- Kỳ vọng: Đạt tiêu chí và có evidence tái kiểm tra; không mở rộng phase hoặc dùng quyền không được cấp.
- Thực tế: .env chỉ được kiểm metadata: mode 0600 và Git ignore. Clean DB độc lập, trust chỉ bên trong container thử nghiệm local; không đọc/copy .env thật, không đụng DB dự án.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [commands.md](evidence/commands.md)
- Xử lý/đề xuất: Không có.
### C06 — Tài liệu và browser

- Nguồn/tiêu chí: [Checklist Phase 01](../../../phases/phase-01.md); [RULES C01–C08](../../../RULES.md)
- Bắt buộc: có
- Điều kiện/môi trường: Phase 01; không inference; các bước destructive/DB chạy trong môi trường cô lập nếu có.
- Bước/lệnh: Đối chiếu checklist; commands/routes ghi tại evidence được dẫn.
- Kỳ vọng: Đạt tiêu chí và có evidence tái kiểm tra; không mở rộng phase hoặc dùng quyền không được cấp.
- Thực tế: HTML source lang=vi; favicon direct HTTP 200; Chrome render trang loopback và accessibility tree xác nhận title/nội dung. Direct web/API, same-origin readiness và hostname IPv4 đều 200.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [routes.md](evidence/routes.md)
- Xử lý/đề xuất: Không có.
### C07 — Regression trực tiếp

- Nguồn/tiêu chí: [Checklist Phase 01](../../../phases/phase-01.md); [RULES C01–C08](../../../RULES.md)
- Bắt buộc: có
- Điều kiện/môi trường: Phase 01; không inference; các bước destructive/DB chạy trong môi trường cô lập nếu có.
- Bước/lệnh: Đối chiếu checklist; commands/routes ghi tại evidence được dẫn.
- Kỳ vọng: Đạt tiêu chí và có evidence tái kiểm tra; không mở rộng phase hoặc dùng quyền không được cấp.
- Thực tế: Health tests 3 passed; npm production build và lint exit 0; direct API liveness/readiness và Vite same-origin readiness HTTP 200.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [commands.md](evidence/commands.md)
- Xử lý/đề xuất: Không có.
### C08 — Report có thể tái kiểm tra

- Nguồn/tiêu chí: [Checklist Phase 01](../../../phases/phase-01.md); [RULES C01–C08](../../../RULES.md)
- Bắt buộc: có
- Điều kiện/môi trường: Phase 01; không inference; các bước destructive/DB chạy trong môi trường cô lập nếu có.
- Bước/lệnh: Đối chiếu checklist; commands/routes ghi tại evidence được dẫn.
- Kỳ vọng: Đạt tiêu chí và có evidence tái kiểm tra; không mở rộng phase hoặc dùng quyền không được cấp.
- Thực tế: Report có đủ 15 IDs C01–C08/P01-01…07, mỗi case có tag/result/expected/actual/evidence. Manifest hash và validator của batch được chạy sau khi ghi report.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [source-manifest.json](evidence/source-manifest.json)
- Xử lý/đề xuất: Không có.
### P01-01 — Cài và chạy local

- Nguồn/tiêu chí: [Checklist Phase 01](../../../phases/phase-01.md); Phase 01 criteria
- Bắt buộc: có
- Điều kiện/môi trường: Phase 01; không inference; các bước destructive/DB chạy trong môi trường cô lập nếu có.
- Bước/lệnh: Đối chiếu checklist; commands/routes ghi tại evidence được dẫn.
- Kỳ vọng: Đạt tiêu chí và có evidence tái kiểm tra; không mở rộng phase hoặc dùng quyền không được cấp.
- Thực tế: Trong bản sao sạch, npm ci/build và uv sync --locked/API health tests pass; PostgreSQL mới migrate baseline; API khởi động readiness 200 và Vite khởi động trả trang/favicon 200 trên loopback ephemeral. Browser/runtime local cũng mở được UI. Evidence clean start ở remake r001.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [commands.md](../../../../remakes/phase-01/20261009T085800+0700-r001-remake/evidence/fresh-start.md)
- Xử lý/đề xuất: Không có.
### P01-02 — Liveness và readiness

- Nguồn/tiêu chí: [Checklist Phase 01](../../../phases/phase-01.md); Phase 01 criteria
- Bắt buộc: có
- Điều kiện/môi trường: Phase 01; không inference; các bước destructive/DB chạy trong môi trường cô lập nếu có.
- Bước/lệnh: Đối chiếu checklist; commands/routes ghi tại evidence được dẫn.
- Kỳ vọng: Đạt tiêu chí và có evidence tái kiểm tra; không mở rộng phase hoặc dùng quyền không được cấp.
- Thực tế: 3 health unit tests pass; API liveness HTTP 200; readiness trực tiếp và qua Vite HTTP 200 với database=ok. Không stop DB đang dùng; nhánh DB-unavailable được kiểm trong unit mock ở suite health.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [commands.md](evidence/commands.md)
- Xử lý/đề xuất: Không có.
### P01-03 — Migration baseline

- Nguồn/tiêu chí: [Checklist Phase 01](../../../phases/phase-01.md); Phase 01 criteria
- Bắt buộc: có
- Điều kiện/môi trường: Phase 01; không inference; các bước destructive/DB chạy trong môi trường cô lập nếu có.
- Bước/lệnh: Đối chiếu checklist; commands/routes ghi tại evidence được dẫn.
- Kỳ vọng: Đạt tiêu chí và có evidence tái kiểm tra; không mở rộng phase hoặc dùng quyền không được cấp.
- Thực tế: DB mới, không project volume: upgrade tới revision 20261008_0001 thành công, current đúng revision; public schema chỉ có alembic_version; upgrade lặp lại pass, không tạo domain tables Phase 03.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [commands.md](../../../../remakes/phase-01/20261009T085800+0700-r001-remake/evidence/fresh-start.md)
- Xử lý/đề xuất: Không có.
### P01-04 — Secret local

- Nguồn/tiêu chí: [Checklist Phase 01](../../../phases/phase-01.md); Phase 01 criteria
- Bắt buộc: có
- Điều kiện/môi trường: Phase 01; không inference; các bước destructive/DB chạy trong môi trường cô lập nếu có.
- Bước/lệnh: Đối chiếu checklist; commands/routes ghi tại evidence được dẫn.
- Kỳ vọng: Đạt tiêu chí và có evidence tái kiểm tra; không mở rộng phase hoặc dùng quyền không được cấp.
- Thực tế: .env mode 0600, Git ignored; không đọc giá trị hoặc ghi secret thật vào artifacts.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [commands.md](evidence/commands.md)
- Xử lý/đề xuất: Không có.
### P01-05 — Registry và binds

- Nguồn/tiêu chí: [Checklist Phase 01](../../../phases/phase-01.md); Phase 01 criteria
- Bắt buộc: có
- Điều kiện/môi trường: Phase 01; không inference; các bước destructive/DB chạy trong môi trường cô lập nếu có.
- Bước/lệnh: Đối chiếu checklist; commands/routes ghi tại evidence được dẫn.
- Kỳ vọng: Đạt tiêu chí và có evidence tái kiểm tra; không mở rộng phase hoặc dùng quyền không được cấp.
- Thực tế: Dev Hub block 15500–15599 và map web 15500/API 15501/Postgres 15510 khớp AGENTS/Compose; listener/service chỉ trên IPv4 loopback. Proxy hostname remote là 127.0.0.1.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [routes.md](evidence/routes.md)
- Xử lý/đề xuất: Không có.
### P01-06 — URL đã xác minh

- Nguồn/tiêu chí: [Checklist Phase 01](../../../phases/phase-01.md); Phase 01 criteria
- Bắt buộc: có
- Điều kiện/môi trường: Phase 01; không inference; các bước destructive/DB chạy trong môi trường cô lập nếu có.
- Bước/lệnh: Đối chiếu checklist; commands/routes ghi tại evidence được dẫn.
- Kỳ vọng: Đạt tiêu chí và có evidence tái kiểm tra; không mở rộng phase hoặc dùng quyền không được cấp.
- Thực tế: Direct IPv4 web/API, same-origin API proxy, favicon và hostname proxy đều HTTP 200; Chrome hiển thị ứng dụng tại URL direct IPv4. IPv6 không được claim.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [routes.md](evidence/routes.md)
- Xử lý/đề xuất: Không có.
### P01-07 — Chưa có agent

- Nguồn/tiêu chí: [Checklist Phase 01](../../../phases/phase-01.md); Phase 01 criteria
- Bắt buộc: có
- Điều kiện/môi trường: Phase 01; không inference; các bước destructive/DB chạy trong môi trường cô lập nếu có.
- Bước/lệnh: Đối chiếu checklist; commands/routes ghi tại evidence được dẫn.
- Kỳ vọng: Đạt tiêu chí và có evidence tái kiểm tra; không mở rộng phase hoặc dùng quyền không được cấp.
- Thực tế: UI ghi inference grant chưa cấp; startup/health source chỉ tạo app và thực hiện SELECT 1 khi readiness, không có dispatch/model call. Batch không seed, không gửi POST hay prompt.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [routes.md](evidence/routes.md)
- Xử lý/đề xuất: Không có.

## Integration / release gates

| Gate áp dụng | PASS / FAIL / BLOCKED | Test IDs | Batch/grant/config/evidence và gate trước |
| --- | --- | --- | --- |
| Không có IG riêng cho Phase 01 | — | — | Roadmap Phase 01; inference grant = 0 |

## Cleanup, giới hạn và bàn giao

- Cleanup: Dừng container PostgreSQL cô lập và xóa temp copy sau kiểm chứng; runtime/API/PostgreSQL dự án không restart/stop.
- Chưa kiểm chứng: Không còn case checklist bắt buộc chưa chạy trong phạm vi này; không thử outage trên PostgreSQL đang dùng.
- Cần sửa: Không còn issue trong report legacy; README hiện tại đã mô tả đúng IPv4-only.
- Đề xuất tùy chọn: Không có.
- Bước tiếp theo: Remake/retest kỹ thuật đạt; không thay trạng thái Markdown, không tự chuyển phase.
- Bàn giao: [Lệnh/runtime evidence](evidence/commands.md), [HTTP/browser](evidence/routes.md), [source manifest](evidence/source-manifest.json), [remake r001](../../../../remakes/phase-01/20261009T085800+0700-r001-remake/remake.md).
