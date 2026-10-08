# Kiểm định Phase 02 — 20261008T161241+0700-phase-02

## Thông tin batch

- Phase: 02
- Test batch: 20261008T161241+0700-phase-02
- Bắt đầu / kết thúc: 2026-10-08T16:12:41+07:00 / 2026-10-08T16:12:41+07:00 (Asia/Ho_Chi_Minh)
- Người/AI kiểm định: Codex
- Yêu cầu/phạm vi được giao: User yêu cầu “test phase 2 + 3”; batch này chỉ kiểm định Phase 02.
- Source: commit `edb550c`; worktree dirty, các thay đổi owner được giữ nguyên; [manifest/hash/file list](evidence/source-manifest.json).
- Môi trường/config/tool versions: Web `127.0.0.1:15500`; API `127.0.0.1:15501`; PostgreSQL `127.0.0.1:15510`; readiness ok; migration head `20261008_0003`; [commands](evidence/commands.md).
- Inference: Không gọi; grant=0. Không probe gateway, reset fixture hoặc tạo task/run qua UI.
- Dependency/quyết định nghiệm thu: Phase 00–03 ghi Hoàn tất trong master plan; AGENTS.md hướng dẫn Phase 04 đang triển khai nhưng master-plan ghi Chờ nghiệm thu — được ghi ở C02. Không cập nhật trạng thái.
- Supersedes: Không có.
- Kết luận kỹ thuật: cần sửa
- Quyết định Chủ tịch: Chưa có.

## Mapping và phạm vi kiểm định

| Tiêu chí hiện tại / nguồn | Test IDs | Bắt buộc / tùy điều kiện | Ghi chú |
| --- | --- | --- | --- |
| AC1 | Không có số giả trình bày như dữ liệu thật. | P02-04 | Bắt buộc |
| AC2 | Luồng điều hướng chính dùng được bằng bàn phím, lang vi và favicon đúng. | P02-01, P02-05 | Bắt buộc |
| AC3 | Không tràn ngang ở 390 px; desktop giữ thứ bậc nội dung rõ. | P02-06, P02-07 | Bắt buộc |
| Kiểm tra chung theo RULES.md §§5–7 | C01–C08 | Bắt buộc | Từng record bên dưới. |

## Tổng hợp

| Tag | Số test |
| --- | --- |
| clean | 11 |
| need-change | 3 |
| suggestion | 1 |

| Result | Số test |
| --- | --- |
| pass | 12 |
| fail | 1 |
| blocked | 2 |
| not-run | 0 |
| not-applicable | 0 |

## Kết quả từng test

### C01 — Phạm vi và diff

- Nguồn/tiêu chí: Chỉ thị kiểm định Phase 02 + 03; root AGENTS.md § phase
- Bắt buộc: có
- Điều kiện/môi trường: Runtime local read-only; Phase 03 persistence test dùng UUID fixture/teardown riêng khi có liên quan.
- Bước/lệnh: Đối chiếu git status/diff trước và sau; không sửa source hoặc chuyển phase.
- Kỳ vọng: Chỉ đánh giá hai phase được giao; giữ nguyên thay đổi đang có của Chủ tịch.
- Thực tế: Worktree có thay đổi owner trong UI/API/Phase 04 và docs/remakes; batch không sửa các file đó. Commit nền edb550c.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [evidence](evidence/commands.md)
- Xử lý/đề xuất: Không cần xử lý.
### C02 — Dependency và nguồn quyết định

- Nguồn/tiêu chí: docs/master-plan.md §6; AGENTS.md Phase/owner guidance
- Bắt buộc: có
- Điều kiện/môi trường: Runtime local read-only; Phase 03 persistence test dùng UUID fixture/teardown riêng khi có liên quan.
- Bước/lệnh: So sánh status Phase 00–04 trong master plan với hướng dẫn được cung cấp.
- Kỳ vọng: Phase 00–03 complete; trạng thái Phase 04 đồng nhất giữa nguồn vận hành.
- Thực tế: Phase 00–03 được ghi complete. AGENTS.md ghi Phase 04 đang triển khai; master-plan.md ghi Phase 04 chờ nghiệm thu. Mismatch xác nhận được; master plan là nguồn chuẩn trạng thái.
- Tag: need-change
- Kết quả: fail
- Mức độ: minor
- Evidence: [evidence](evidence/commands.md)
- Xử lý/đề xuất: Chủ tịch đồng bộ một nguồn trạng thái; không chỉnh roadmap trong batch kiểm định.
### C03 — Đủ criteria và demo

- Nguồn/tiêu chí: docs/tests/phases/phase-02.md § Mapping; docs/master-plan.md Phase 02
- Bắt buộc: có
- Điều kiện/môi trường: Runtime local read-only; Phase 03 persistence test dùng UUID fixture/teardown riêng khi có liên quan.
- Bước/lệnh: Đối chiếu AC1–AC3 và demo dashboard với test P02-01…07; mở ứng dụng local.
- Kỳ vọng: Mọi AC có test; khung demo mở được và data không giả làm dữ liệu thật.
- Thực tế: AC1→P02-04; AC2→P02-01/P02-05; AC3→P02-06/P02-07. Dashboard mở với nhãn Demo/fixture.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [evidence](evidence/commands.md)
- Xử lý/đề xuất: Không cần xử lý.
### C04 — Không thực thi âm thầm

- Nguồn/tiêu chí: RULES.md C04; apps/web/src/App.tsx
- Bắt buộc: có
- Điều kiện/môi trường: Runtime local read-only; Phase 03 persistence test dùng UUID fixture/teardown riêng khi có liên quan.
- Bước/lệnh: Mở route, đổi mode, điều hướng; rà source các effect và handler.
- Kỳ vọng: Không gọi model/tool/gateway khi mở trang; chỉ thực hiện health/dashboard GET đã nêu.
- Thực tế: Không gọi probe/reset hay model. Nút probe/reset không được bấm; source tách các handler tường minh. Grant hiển thị 0.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [evidence](evidence/commands.md)
- Xử lý/đề xuất: Không cần xử lý.
### C05 — Scope và dữ liệu nhạy cảm

- Nguồn/tiêu chí: RULES.md C05; apps/api/tests/test_phase03_persistence.py
- Bắt buộc: có
- Điều kiện/môi trường: Runtime local read-only; Phase 03 persistence test dùng UUID fixture/teardown riêng khi có liên quan.
- Bước/lệnh: Dùng fixture test có UUID mới; xem redaction assertions và cleanup; không đọc .env.
- Kỳ vọng: Không dùng secret thật; fixture chỉ xóa rows theo environment ID của batch.
- Thực tế: Test dùng secret canary giả; teardown chỉ xóa domain rows thuộc hai UUID environment vừa tạo. Không đọc/in .env.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [evidence](evidence/commands.md)
- Xử lý/đề xuất: Không cần xử lý.
### C06 — Tài liệu và bản nhìn

- Nguồn/tiêu chí: RULES.md C06; phase checklists; apps/web/index.html
- Bắt buộc: có
- Điều kiện/môi trường: Runtime local read-only; Phase 03 persistence test dùng UUID fixture/teardown riêng khi có liên quan.
- Bước/lệnh: Build web; đọc `lang`, favicon qua browser DOM; đối chiếu checklist hiện có.
- Kỳ vọng: Build và tài liệu phase hợp lệ; trang có lang vi/favicon.
- Thực tế: Build thành công; browser DOM lang=vi và favicon SVG data URI. Docs checklist/link/hash được validator kiểm tra theo batch; validator toàn repo dừng ở report Phase 04 có verdict bọc markdown (xem commands.md).
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [evidence](evidence/commands.md)
- Xử lý/đề xuất: Không cần xử lý.
### C07 — Regression liên quan

- Nguồn/tiêu chí: RULES.md C07; Phase 02/03 dependency 01/02
- Bắt buộc: có
- Điều kiện/môi trường: Runtime local read-only; Phase 03 persistence test dùng UUID fixture/teardown riêng khi có liên quan.
- Bước/lệnh: Chạy web build và pytest Phase 03 persistence; không chạy cả suite vì Phase 04 đang hoạt động.
- Kỳ vọng: Kiểm tra regression liên quan mà không tác động fixture ngoài phạm vi.
- Thực tế: Build pass; 5 test Phase 03 pass. Không chạy full API suite hoặc restart shared services.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [evidence](evidence/commands.md)
- Xử lý/đề xuất: Không cần xử lý.
### C08 — Có thể tái kiểm định

- Nguồn/tiêu chí: RULES.md C08
- Bắt buộc: có
- Điều kiện/môi trường: Runtime local read-only; Phase 03 persistence test dùng UUID fixture/teardown riêng khi có liên quan.
- Bước/lệnh: Lưu source hashes, commands, UI observations, test output summary và cleanup scope; chạy validator.
- Kỳ vọng: Mỗi test có tag/result/evidence link; report đủ batch metadata và không chứa secrets.
- Thực tế: Tạo manifest/hash và note đã lọc. Screenshot được quan sát live nhưng không có file ảnh workspace trong phiên này; các case phụ thuộc ảnh được giữ blocked.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [evidence](evidence/commands.md)
- Xử lý/đề xuất: Không cần xử lý.
### P02-01 — Điều hướng chính

- Nguồn/tiêu chí: phase-02.md AC2/P02-01; product-spec §3
- Bắt buộc: có
- Điều kiện/môi trường: Runtime local read-only; Phase 03 persistence test dùng UUID fixture/teardown riêng khi có liên quan.
- Bước/lệnh: Đi qua 14 link sidebar; kiểm hash/h1; back và reload.
- Kỳ vọng: Điều hướng đúng trang, nhãn/trạng thái phù hợp; reload giữ route.
- Thực tế: 14/14 hash khớp heading; back về #settings và reload giữ đúng #settings.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [evidence](evidence/ui-observations.md)
- Xử lý/đề xuất: Không cần xử lý.
### P02-02 — Hai mode Owner

- Nguồn/tiêu chí: phase-02.md P02-02; product-spec §2/10
- Bắt buộc: có
- Điều kiện/môi trường: Runtime local read-only; Phase 03 persistence test dùng UUID fixture/teardown riêng khi có liên quan.
- Bước/lệnh: Chọn Vận hành rồi Chủ tịch; xem pressed state, nội dung và source handler.
- Kỳ vọng: Mode chỉ đổi cách nhìn, không thay API permission/authority.
- Thực tế: UI đổi đúng heading và aria-pressed; text nói mode chỉ đổi trình bày; source chỉ setMode.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [evidence](evidence/ui-observations.md)
- Xử lý/đề xuất: Không cần xử lý.
### P02-03 — Empty/loading/error

- Nguồn/tiêu chí: phase-02.md P02-03; product-spec §3
- Bắt buộc: có
- Điều kiện/môi trường: Runtime local read-only; Phase 03 persistence test dùng UUID fixture/teardown riêng khi có liên quan.
- Bước/lệnh: Kiểm tra trạng thái API hiện tại và source fallback; không dừng API/DB dùng chung hoặc mock network.
- Kỳ vọng: Phân biệt loading/offline/error/empty và phục hồi sau lỗi.
- Thực tế: Health đang ok; các nhánh offline/error chưa được kích hoạt. Không thực hiện fault/network interception.
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Evidence: [evidence](evidence/ui-observations.md)
- Xử lý/đề xuất: Cần runtime/browser test cô lập hoặc network interception được cấp phép để kiểm tra lỗi và phục hồi.
### P02-04 — Không số/hoạt cảnh giả

- Nguồn/tiêu chí: phase-02.md AC1/P02-04; product-spec §2/3
- Bắt buộc: có
- Điều kiện/môi trường: Runtime local read-only; Phase 03 persistence test dùng UUID fixture/teardown riêng khi có liên quan.
- Bước/lệnh: Xem dashboard/Work Order và badge/labels; đọc source của fixture render.
- Kỳ vọng: Số demo không được trình bày như live; usage/chi phí không bị giả thành 0.
- Thực tế: Dashboard ghi Demo Corporation/fixture, 3 hồ sơ/2 phòng ban/5 Work Order/20 event fixture; usage UNKNOWN, chi phí chưa xác định và inference 0.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [evidence](evidence/ui-observations.md)
- Xử lý/đề xuất: Không cần xử lý.
### P02-05 — Bàn phím và semantics

- Nguồn/tiêu chí: phase-02.md AC2/P02-05; product-spec §3
- Bắt buộc: có
- Điều kiện/môi trường: Runtime local read-only; Phase 03 persistence test dùng UUID fixture/teardown riêng khi có liên quan.
- Bước/lệnh: Tab tới S06, Enter mở route; Shift+Tab lùi focus; kiểm Escape, aria labels, lang và favicon.
- Kỳ vọng: Luồng chính keyboard-operable, focus không trap, metadata tiếng Việt đúng.
- Thực tế: Tab tới S06; Enter mở #approvals; Shift+Tab lùi tới S13; Escape không làm mất focus; lang=vi, favicon có và mode có aria-pressed.
- Tag: clean
- Kết quả: pass
- Mức độ: info
- Evidence: [evidence](evidence/ui-observations.md)
- Xử lý/đề xuất: Không cần xử lý.
### P02-06 — Mobile 390 px

- Nguồn/tiêu chí: phase-02.md AC3/P02-06; product-spec §3/13
- Bắt buộc: có
- Điều kiện/môi trường: Runtime local read-only; Phase 03 persistence test dùng UUID fixture/teardown riêng khi có liên quan.
- Bước/lệnh: Browser viewport 390×844; đo clientWidth/document scrollWidth; mở link cuối menu mobile.
- Kỳ vọng: Không tràn ngang ở document; nav/action tới được trong vùng scroll ngang; nội dung không bị che.
- Thực tế: innerWidth=390; clientWidth=375; document scrollWidth=375 (không có tràn document). Nav có vùng scroll ngang; link S14 điều hướng được. Ảnh chụp chỉ quan sát live, không được lưu thành evidence file.
- Tag: need-change
- Kết quả: blocked
- Mức độ: major
- Evidence: [evidence](evidence/ui-observations.md)
- Xử lý/đề xuất: Giữ evidence ảnh mobile trong workspace rồi chạy batch mới; số đo hiện tại chứng minh không tràn document.
### P02-07 — Desktop hierarchy

- Nguồn/tiêu chí: phase-02.md P02-07; product-spec §3
- Bắt buộc: có
- Điều kiện/môi trường: Runtime local read-only; Phase 03 persistence test dùng UUID fixture/teardown riêng khi có liên quan.
- Bước/lệnh: Xem dashboard ở viewport mặc định; rà title/primary navigation/data panels và source tokens.
- Kỳ vọng: Thứ bậc nội dung rõ, không chồng lấn; các giá trị phân biệt fixture/service/unknown.
- Thực tế: Ảnh desktop được xem live: sidebar, title, banner demo, hai cột trạng thái và usage/mode hiển thị tách bạch. Không có file ảnh retained; font một số label rất nhỏ (8–10px CSS), đề nghị theo dõi readability.
- Tag: suggestion
- Kết quả: pass
- Mức độ: minor
- Evidence: [evidence](evidence/ui-observations.md)
- Xử lý/đề xuất: Tùy chọn: tăng cỡ một số nhãn/body nhỏ sau khi review trên màn hình mục tiêu; không thấy chồng lấn.
## Integration / release gates

Phase 02 không có gate IG riêng; các AC và C01–C08 được kiểm định ở trên.

## Cleanup, giới hạn và bàn giao

- Cleanup: Không ghi/xóa dữ liệu. Khôi phục viewport browser về mặc định; mode được trả về Chủ tịch.
- Chưa kiểm chứng: P02-03 offline/loading error-recovery; P02-06 ảnh 390px chưa được lưu workspace. C02 có mismatch trạng thái roadmap/hướng dẫn.
- Cần sửa: C02 cần Chủ tịch đồng bộ nguồn trạng thái Phase 04. P02-03/P02-06 là thiếu evidence/tooling, chưa xác nhận bug sản phẩm.
- Đề xuất tùy chọn: P02-07 theo dõi khả năng đọc của nhãn CSS nhỏ.
- Bàn giao: [commands](evidence/commands.md), [UI observations](evidence/ui-observations.md), [source manifest](evidence/source-manifest.json). Không nghiệm thu thay Chủ tịch.
