# Kiểm định Phase 01 — 20261008T154512+0700-phase01

## Thông tin batch

- Phase: 01
- Test batch: 20261008T154512+0700-phase01
- Bắt đầu / kết thúc: 2026-10-08T15:45:12+07:00 / 2026-10-08T15:47:00+07:00
- Người/AI kiểm định: Codex
- Yêu cầu/phạm vi được giao: Chạy test Phase 01.
- Source: Worktree đang dirty vì Phase 03–04. Source hashes ở [manifest](evidence/source-manifest.json).
- Môi trường/config/tool versions: Local workstation; PostgreSQL/API đã chạy trước batch; Vite được khởi động trong PTY; pins ở manifest.
- Inference: Không gọi; grant hiện tại là 0.
- Dependency/quyết định nghiệm thu: Phase 00–03 Hoàn tất; Phase 04 đang triển khai theo chỉ thị Chủ tịch. Phase 01 đã được duyệt trước đây; report này không đổi trạng thái chính thức.
- Supersedes: Không có.
- Kết luận kỹ thuật: cần sửa
- Quyết định Chủ tịch: Chưa có cho finding mới trong report này.

## QA verdict

**READY WITH KNOWN ISSUES (P2 documentation issue).** Batch còn thiếu kiểm tra fresh install và migration trên DB sạch, nên chưa xác nhận lại được hai phần đó.

Finding P2: README nói proxy hoạt động trên IPv4/IPv6, trong khi cấu hình được Chủ tịch xác nhận và listener thực tế chỉ hỗ trợ IPv4 loopback. Đường IPv4 vẫn hoạt động. Không tái hiện lỗi sản phẩm Phase 01. Chi tiết trong [finding C02](evidence/finding-c02.md).

## Tổng hợp

| Tag | Số test |
| --- | --- |
| clean | 9 |
| need-change | 3 |
| suggestion | 3 |

| Result | Số test |
| --- | --- |
| pass | 12 |
| fail | 1 |
| blocked | 1 |
| not-run | 1 |
| not-applicable | 0 |

## Kết quả từng test

### C01 — Phạm vi và dirty worktree

- Nguồn/tiêu chí: Yêu cầu chạy test Phase 01.
- Bắt buộc: có
- Điều kiện/môi trường: Worktree có thay đổi Phase 03–04; không sửa implementation.
- Bước/lệnh: Đối chiếu AGENTS, roadmap, git status và danh sách lệnh.
- Kỳ vọng: Không chạy phase khác hoặc đổi dữ liệu ngoài phạm vi.
- Thực tế: Chỉ chạy health test, build/lint, route GET và migration metadata read-only.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [manifest](evidence/source-manifest.json), [commands](evidence/commands.md)
- Xử lý/đề xuất: Không.

### C02 — Dependency và sự nhất quán của nguồn

- Nguồn/tiêu chí: Root AGENTS.md Runtime Phase 01; Dev Hub registry; README runtime.
- Bắt buộc: có
- Điều kiện/môi trường: Registry và listener hiện tại.
- Bước/lệnh: Đối chiếu README, AGENTS.md, registry và kiểm tra IPv4/IPv6.
- Kỳ vọng: Tài liệu mô tả đúng bind hiện có.
- Thực tế: README nói IPv4/IPv6; hướng dẫn Chủ tịch/registry nói Caddy chỉ bind IPv4 loopback, và IPv6 probe không kết nối được. Đường IPv4 trả đúng app.
- Tag: need-change
- Kết quả: fail
- Mức độ: minor
- Evidence: [finding](evidence/finding-c02.md), [routes](evidence/routes.md)
- Xử lý/đề xuất: Đồng bộ README về IPv4-only ở lượt sửa tài liệu được giao; không nới bind/proxy.

### C03 — Mapping tiêu chí và demo

- Nguồn/tiêu chí: Phase 01 AC1–AC3 trong roadmap và checklist P01.
- Bắt buộc: có
- Điều kiện/môi trường: Phase 01.
- Bước/lệnh: Đối chiếu từng AC với P01-01…P01-07.
- Kỳ vọng: Không bỏ tiêu chí; test chưa chạy được ghi rõ.
- Thực tế: AC1–AC3 đều có mapping; fresh install và DB mới được ghi là chưa kiểm.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [checklist](../../../phases/phase-01.md), [bảng kết quả](./report.md)
- Xử lý/đề xuất: Không.

### C04 — Không gọi model/tool âm thầm

- Nguồn/tiêu chí: Phase 01 scope và inference grant hiện tại 0.
- Bắt buộc: có
- Điều kiện/môi trường: Batch chỉ chạy test health, build/lint, GET và mở trang.
- Bước/lệnh: Kiểm API health path, UI, network operations trong batch.
- Kỳ vọng: Không dispatch inference/tool.
- Thực tế: Không POST model/tool; health dùng GET; UI ghi grant chưa cấp và demo fixture không gọi model.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [routes](evidence/routes.md), [commands](evidence/commands.md)
- Xử lý/đề xuất: Không.

### C05 — Secret và scope

- Nguồn/tiêu chí: Phase 01 secret handling; rule C05.
- Bắt buộc: có
- Điều kiện/môi trường: Chỉ kiểm metadata; không đọc nội dung .env.
- Bước/lệnh: stat mode và git check-ignore; health test kiểm thông báo lỗi đã lọc.
- Kỳ vọng: Mode 0600, Git ignore, không tiết lộ lỗi DB.
- Thực tế: Mode 600; .env ignored; unit test khẳng định chi tiết private connection không nằm trong response.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [commands](evidence/commands.md)
- Xử lý/đề xuất: Không.

### C06 — Tài liệu và browser

- Nguồn/tiêu chí: Phase 01 web lang/favicon/health.
- Bắt buộc: có
- Điều kiện/môi trường: Web build và runtime local.
- Bước/lệnh: Build, kiểm HTML, mở Chrome và GET favicon.
- Kỳ vọng: lang vi; favicon; trang và health hoạt động.
- Thực tế: Build thành công; lang=vi; favicon HTTP 200; browser thấy API/PostgreSQL readiness đúng. IPv6 documentation mismatch nằm riêng ở C02.
- Tag: suggestion
- Kết quả: pass
- Mức độ: info
- Evidence: [routes](evidence/routes.md), [commands](evidence/commands.md)
- Xử lý/đề xuất: Đồng bộ câu mô tả mạng trong README theo finding C02.

### C07 — Regression trực tiếp

- Nguồn/tiêu chí: Health route và Vite API proxy Phase 01.
- Bắt buộc: có
- Điều kiện/môi trường: Không chạy DB-writing tests của Phase 03–04.
- Bước/lệnh: Chạy health tests, build/lint, gọi API và same-origin readiness.
- Kỳ vọng: Health contract đúng, build/lint không lỗi.
- Thực tế: 3 health tests pass; API liveness/readiness và Vite proxy 200; build/lint exit 0.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [commands](evidence/commands.md), [routes](evidence/routes.md)
- Xử lý/đề xuất: Toàn bộ suite không chạy vì hiện có test DB-writing Phase 03–04.

### C08 — Report có thể tái kiểm tra

- Nguồn/tiêu chí: Rule C08; schema report.
- Bắt buộc: có
- Điều kiện/môi trường: Batch riêng, evidence đã lọc.
- Bước/lệnh: Kiểm report completeness và chạy validate.py --batch.
- Kỳ vọng: Tất cả test có tag/result/evidence; không chứa secret.
- Thực tế: 15 test records gồm C01–C08 và P01-01…P01-07; source manifest/evidence không chứa .env content.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [manifest](evidence/source-manifest.json), [commands](evidence/commands.md)
- Xử lý/đề xuất: Validator sẽ chạy sau khi report hoàn tất.

### P01-01 — Cài và chạy local

- Nguồn/tiêu chí: Phase 01 AC1.
- Bắt buộc: có
- Điều kiện/môi trường: Dependencies đã có; Phase 04 đang dùng API/DB local.
- Bước/lệnh: Chạy build/lint và Vite; không chạy npm ci/uv sync để tránh sửa môi trường dùng chung.
- Kỳ vọng: Có thể cài/chạy/check theo README từ môi trường sạch.
- Thực tế: Build/lint và app hiện tại hoạt động; fresh install chưa được chạy trong batch.
- Tag: need-change
- Kết quả: not-run
- Mức độ: major
- Evidence: [commands](evidence/commands.md), [routes](evidence/routes.md)
- Xử lý/đề xuất: Cần môi trường riêng để kiểm tra clean install; chưa phải bug được tái hiện.

### P01-02 — Liveness và readiness

- Nguồn/tiêu chí: Phase 01 AC1; test_health.py.
- Bắt buộc: có
- Điều kiện/môi trường: Unit ASGI và runtime DB hiện healthy.
- Bước/lệnh: Chạy health test; GET API trực tiếp và qua Vite.
- Kỳ vọng: Live tách DB; ready báo trạng thái DB và sanitize lỗi.
- Thực tế: 3 tests pass; direct và same-origin readiness 200. DB-unavailable được kiểm bằng mock trong unit; không dừng DB dùng bởi Phase 04.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [commands](evidence/commands.md), [routes](evidence/routes.md)
- Xử lý/đề xuất: Không outage test trên DB đang dùng.

### P01-03 — Migration baseline

- Nguồn/tiêu chí: Phase 01 AC1; Alembic baseline và chain.
- Bắt buộc: có
- Điều kiện/môi trường: PostgreSQL hiện là head 0003 và được Phase 04 sử dụng.
- Bước/lệnh: Chạy Alembic current/history read-only; không tạo DB hoặc chạy upgrade.
- Kỳ vọng: Kiểm upgrade baseline từ DB sạch và migration không sinh schema sai.
- Thực tế: Current=0003; history xác nhận 0001→0002→0003. Fresh-base migration không được chạy trên DB đang dùng.
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Evidence: [commands](evidence/commands.md), [bằng chứng Phase 01 lịch sử](../../../../evidence/phase-01.md), [manifest](evidence/source-manifest.json)
- Xử lý/đề xuất: Chạy trên DB kiểm định riêng khi có môi trường đó; không sửa DB Phase 04.

### P01-04 — Secret local

- Nguồn/tiêu chí: Phase 01 AC1.
- Bắt buộc: có
- Điều kiện/môi trường: Metadata file .env.
- Bước/lệnh: stat mode và check-ignore, không đọc giá trị.
- Kỳ vọng: Mode 0600 và Git ignore.
- Thực tế: Mode 600; .env bị ignore.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [commands](evidence/commands.md)
- Xử lý/đề xuất: Không.

### P01-05 — Registry và binds

- Nguồn/tiêu chí: Phase 01 AC2; Dev Hub mapping; root AGENTS runtime Phase 01.
- Bắt buộc: có
- Điều kiện/môi trường: Block 15500–15599; host local.
- Bước/lệnh: Đối chiếu registry, Compose, Vite, API, listener và proxy.
- Kỳ vọng: Mapping khớp; loopback IPv4 theo capability được Chủ tịch xác nhận; không ingress LAN.
- Thực tế: Web 15500/API 15501/Postgres 15510 đúng registry; Caddy port 80 và route IPv4 loopback; hostname proxy trả 200. IPv6 không bind được theo hướng dẫn hiện hành.
- Tag: suggestion
- Kết quả: pass
- Mức độ: info
- Evidence: [routes](evidence/routes.md), [finding](evidence/finding-c02.md), [manifest](evidence/source-manifest.json)
- Xử lý/đề xuất: README còn mô tả IPv6; xem C02.

### P01-06 — URL và browser

- Nguồn/tiêu chí: Phase 01 AC3; hostname registry.
- Bắt buộc: có
- Điều kiện/môi trường: Vite chạy trong PTY; Chrome.
- Bước/lệnh: GET web/health direct, hostname/proxy, favicon; mở trang Chrome.
- Kỳ vọng: Đường IPv4 được công bố trả đúng app và API; ghi rõ IPv6 capability.
- Thực tế: Direct và hostname 200; browser render đúng; health proxy 200. ::1 không có listener theo giới hạn host đã được Chủ tịch xác nhận.
- Tag: suggestion
- Kết quả: pass
- Mức độ: info
- Evidence: [routes](evidence/routes.md), [finding](evidence/finding-c02.md)
- Xử lý/đề xuất: Giữ IPv4-only trong docs.

### P01-07 — Không agent/inference

- Nguồn/tiêu chí: Phase 01 giới hạn; inference default deny.
- Bắt buộc: có
- Điều kiện/môi trường: Grant=0; batch chỉ GET/test/build/lint.
- Bước/lệnh: Kiểm startup/health path và UI; không gửi model request.
- Kỳ vọng: Không worker/inference từ startup/health/UI fixture.
- Thực tế: Batch không gọi inference; API health path không gửi model request; UI ghi grant chưa cấp.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [routes](evidence/routes.md), [commands](evidence/commands.md)
- Xử lý/đề xuất: Không.

## Integration / release gates

| Gate áp dụng | PASS / FAIL / BLOCKED | Test IDs | Batch/grant/config/evidence và gate trước |
| --- | --- | --- | --- |
| Không có IG riêng cho Phase 01 | — | — | Roadmap Phase 01 |

## Cleanup, giới hạn và bàn giao

- Cleanup: Không tạo/xóa DB fixtures. Vite dev server vẫn chạy trong terminal tương tác session 86814 để log/runtime còn sẵn; API/PostgreSQL không bị restart.
- Chưa kiểm chứng: P01-01 fresh install (not-run); P01-03 migration từ DB sạch (blocked); live DB outage không thử.
- Cần sửa: C02/P2 — README IPv6 proxy statement lệch với cấu hình hiện hành.
- Đề xuất tùy chọn: P01-05/P01-06 ghi nhận IPv4-only theo giới hạn môi trường.
- Bàn giao: Report và evidence trong batch. Phase 01 vẫn Hoàn tất theo quyết định đã có; không tự chuyển phase.
