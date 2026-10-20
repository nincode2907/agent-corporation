# Local Deployment & Visual Acceptance 06

**Ngày:** 20/10/2026 (Asia/Ho_Chi_Minh)  
**Kết quả:** triển khai hoàn tất; kiểm định runtime đạt; UI nghiệm thu một phần.  
**Phạm vi quyền:** deployment và kiểm tra UI. Không có inference, grant mới, CG01 override, thay gateway hay chuyển trạng thái phase.

## Kết quả

- Đã chạy `docker compose up --build` trên Compose project Agent Corporation hiện hữu. Giữ nguyên PostgreSQL volume `agent-corporation_agent_corporation_postgres` cùng các volume database/runtime secrets và artifacts. Không reset, seed, xóa volume hay restart Codex gateway.
- Migration chạy thành công từ `20261014_0009` lên `20261020_0010`. PostgreSQL, API, web healthy; API readiness và web health endpoint đều trả `ok`.
- Còn đúng một Runtime worker đang chạy. Advisory lock của worker được giữ trên PostgreSQL; lần thử lấy cùng lock từ session phụ bị từ chối như mong đợi.
- Demo Corporation còn 1 bản ghi và 3 employee. Sau deploy: 0 Runtime runs, 0 model calls, 0 grant còn hiệu lực/chưa dùng hết, dispatch guard trống. Playground có 0 session/turn; kiểm định không tạo Playground session.
- CG01 vẫn strict và bị chặn vì `missing_or_invalid_proof`. Release check tiếp tục bị chặn. Không gọi inference và không tạo grant.
- Đã đăng nhập bằng Owner session cục bộ chỉ để kiểm tra UI. Một session thử nghiệm dở dang đã được thu hồi; session thứ hai đã đăng xuất. Không ghi secret hoặc cookie vào artifact.
- Đã kiểm tra dashboard, chọn employee và EmployeeVersion trong Runtime form, thông báo profile/gate/grant, Start bị khóa, Inspector, Replay, Office và Playground. Desktop 1440×900, mobile 390×844; các trang đã đo không tràn ngang.
- Office hiện hiển thị các lane run rỗng và fixture phòng ban. Do ledger dùng chung có 0 Runtime runs, Office **không hiển thị ba employee như các thẻ có trạng thái**. Không bơm Run tổng hợp vào DB dùng chung; tiêu chí này còn thiếu bằng chứng và cần xử lý UX/product riêng.
- Stack tổng hợp cô lập xác minh được giao diện unknown reconciliation: Run `interrupted`, phân loại `unresolved`, usage/cost `unknown`, guard vẫn giữ và không có force-unlock. Dữ liệu synthetic, fake worker/transport; đã xóa stack và volumes sau kiểm tra.
- Gemini UX review: **NOT PERFORMED** — không có giao diện Gemini được ủy quyền để gửi ảnh. Đã lưu gói ảnh và hành trình đã khử credential để review độc lập.

## Bằng chứng và tài liệu

- [deployment-verification.md](deployment-verification.md): preflight, backup, migration, worker, rollback.
- [ui-review.md](ui-review.md): ma trận giao diện, giới hạn nghiệm thu và kết quả Gemini.
- [next-actions.md](next-actions.md): việc còn lại và điều kiện cho demo model thật.
- [evidence/contact-sheet.png](evidence/contact-sheet.png): ảnh tổng hợp; ảnh gốc và manifest trong `evidence/screenshots/`.

## Kết luận nghiệm thu

Deployment và kiểm soát không-inference đạt. UI đạt một phần; Live Office chưa chứng minh được ba hồ sơ employee cùng trạng thái vì không có Runtime Run trong dữ liệu dùng chung. Không cập nhật trạng thái Phase 06–08 và không nghiệm thu thay Chủ tịch. Demo model thật cần một đợt riêng sau khi CG01 strict có proof hợp lệ và được Chủ tịch cấp grant riêng theo scope, hạn mức và thời hạn.
