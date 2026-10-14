# Tài liệu thiết kế

- Employee Chat revision 02: `employee-chat.md` là hợp đồng thiết kế; `employee-chat-prototype.html` là prototype tương tác độc lập, chỉ DOM, không network/storage/API; `employee-chat.html` ghép bản đọc trực quan và prototype.
- `cg01-technical-decision.md/.html`: decision workflow OPEN, dispatch KEEP-BLOCKED; không thay proof/grant.
- Đợt review này chỉ cập nhật Markdown/HTML theo yêu cầu Chủ tịch, không đổi script hoặc app code. `scripts/render_phase00.py` đồng bộ spec/ADR-0001/roadmap như cũ. Renderer `scripts/render_employee_chat_docs.py` thuộc revision 01; không chạy để ghi đè Employee Chat revision 02. Muốn tự động hóa renderer revision 02 cần scope riêng; khi sửa các cặp tài liệu này, cập nhật Markdown trước và đồng bộ HTML trực tiếp, giữ prototype mới.
