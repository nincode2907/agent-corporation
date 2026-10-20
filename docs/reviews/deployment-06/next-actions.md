# Next actions

1. Chủ tịch review deployment evidence và nghiệm thu riêng. Trạng thái Phase 06–08 vẫn theo `docs/master-plan.md`; deployment này không tự đánh dấu phase hoàn tất.
2. Chốt cách Live Office cần thể hiện ba employee khi chưa có Runtime Run. Nếu cần trạng thái live, dùng dữ liệu tổng hợp trong scope tạm được cách ly; không chèn Run giả vào Demo Corporation dùng chung.
3. Nếu cần UX review độc lập, gửi gói đã khử credential trong `evidence/` qua một Gemini session được ủy quyền.
4. Chưa có quyền cho demo model thật: CG01 strict còn blocked vì thiếu proof hợp lệ và hiện không có inference grant. Khi muốn demo, trước tiên hoàn tất quy trình proof strict theo yêu cầu release; sau đó Chủ tịch cấp một grant riêng với phase, scope, model/effort, hạn mức và expiry đã chốt. Cần approval riêng cho lần live-model demonstration; approval này không được suy ra từ deployment 06.

Không tạo grant, không gọi model và không bật demo override trong bước hiện tại.
