# Remake Phase 02 — 20261009T094205+0700-r001-remake

## Thông tin vòng sửa

- Phase: 02 — Khung giao diện Chủ tịch
- Vòng: r001 (report nguồn legacy)
- Report nguồn: [kiểm định Phase 02 legacy](../../../tests/results/phase-02/20261008T161241+0700-phase-02/report.md)
- Người/AI remake: Codex implementer trong phiên Chủ tịch giao remake
- Thời gian: 2026-10-09 +07:00
- Phạm vi/quyền: chỉ Phase 02; không đổi gateway, API/DB dùng chung, không gọi inference.
- Source trước/sau: dirty worktree; xem [manifest](evidence/source-manifest.json).
- Inference: không gọi; grant = 0.
- Kết luận vòng sửa: không có lỗi source đã xác nhận; hai finding vẫn cần kiểm định/evidence độc lập.

## Mapping results → thay đổi

| Test ID / kết quả nguồn | Nguyên nhân | Thay đổi thực tế | Trạng thái xử lý | Retest |
| --- | --- | --- | --- | --- |
| C02 — need-change / mismatch | `AGENTS.md` chưa phản ánh trạng thái roadmap hiện tại. | Đồng bộ dòng trạng thái hướng dẫn với `docs/master-plan.md`; không đổi quyết định kiến trúc. | changed | C02 và kiểm tra links/roadmap |
| P02-03 — need-change / blocked | Report cũ không kích hoạt failure/recovery qua network isolation; code hiện đã có error copy, nút tải lại fixture và nút kiểm tra health ở Settings. Chưa chứng minh trực tiếp recovery. | Không sửa source vì chưa tái hiện lỗi sản phẩm; giữ finding mở tới browser test độc lập có network failure/recovery. | blocked | Thử API failure → xác nhận error state → khôi phục API → thử CTA retry; không mutation/inference |
| P02-06 — need-change / blocked | Đo 390 px có trong ghi chú cũ nhưng screenshot không được lưu trong workspace. | Không đổi layout; cần screenshot + viewport/overflow metrics được giữ lại theo checklist. | blocked | Browser viewport 390×844, ảnh và scrollWidth/clientWidth; kiểm link cuối menu |
| P02-07 — suggestion / pass | Một số label 7–10 px là gợi ý readability, không phải acceptance failure report nguồn. | Để lại; không mở rộng thiết kế. | no-change | Không chặn đạt kỹ thuật |

## Chi tiết

### P02-03 — trạng thái lỗi và phục hồi

- Expected/actual nguồn: phân biệt loading/offline/error/empty và phục hồi; report chỉ quan sát health OK, không dùng network interception/fault fixture.
- Nguyên nhân: thiếu kiểm chứng; chưa có evidence rằng handler hỏng.
- Thay đổi: không sửa `App.tsx`/CSS. Source hiện có trạng thái ban đầu “Đang đọc fixture…”, error copy cho demo fetch, CTA “Tải lại dữ liệu demo”; Settings có health error và “Kiểm tra lại”.
- Trạng thái xử lý: blocked — cần retest độc lập tạo lỗi mạng có kiểm soát và xác minh phục hồi.
- Kiểm tra khi remake: source review `apps/web/src/App.tsx`; `npm run --prefix apps/web build` sẽ được chạy cùng regression ở bước bàn giao.

### P02-06 — viewport 390 px

- Expected/actual nguồn: số đo trước đó không có tràn document và link cuối menu dùng được; screenshot mobile không được lưu.
- Nguyên nhân: artefact bắt buộc chưa được giữ lại, không phải lỗi CSS đã xác nhận.
- Thay đổi: không sửa layout/breakpoints.
- Trạng thái xử lý: blocked — cần AI test độc lập giữ screenshot và số đo viewport/overflow trong `results`.
- Retest: viewport 390×844; ghi `innerWidth`, `documentElement.clientWidth`, `scrollWidth`; điều hướng S14; lưu ảnh vào batch test.

## Cleanup và bước tiếp theo

- Cleanup: không tạo hoặc sửa dữ liệu sản phẩm; không dừng/restart service dùng chung.
- Checks: xem [commands](evidence/commands.md); source hash ở [manifest](evidence/source-manifest.json).
- Retest tiếp theo: AI khác chạy r002 độc lập, lưu vào `docs/tests/results/phase-02/`.
- Trạng thái phase: Chờ nghiệm thu; chưa được đánh dấu Hoàn tất.
- Sổ vòng: [Phase 02](../../../tests/results/phase-02/README.md).
