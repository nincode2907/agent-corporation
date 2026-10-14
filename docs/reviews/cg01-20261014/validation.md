# Kiểm tra tài liệu ngày 14/10/2026

- Phạm vi: CG01 review + Employee Chat design, không kiểm thử chat sản phẩm.
- `python3 scripts/render_phase00.py`: dựng spec/ADR/roadmap; 32 requirements, 15 screens, 35 baseline events, 24 phase, 1 phase hoàn tất.
- `python3 scripts/render_employee_chat_docs.py`: dựng 3 cặp tài liệu bổ sung; kiểm tra chạy lại cho cùng hash HTML.
- `python3 scripts/validate_phase00.py`: PASS contract/links/anchors/IDs/lang/favicon/JS syntax và đồng bộ HTML; có 9 flows, giữ event baseline và 2 JSON examples không cấp grant.
- Kiểm tra tĩnh riêng 3 HTML mới: PASS links, lang=vi/favicon, không trùng ID, không JavaScript hoặc client gọi mạng. Local Markdown links tồn tại.
- `git diff --check`: PASS.
- [Independent design review](design-review.md): hai finding về dependency/qualification đã sửa, retest tài liệu không còn finding giải quyết được.
- Visual QA: NOT VERIFIED. Browser tool từ chối mở URL file local theo security policy; không thử vòng qua hạn chế đó, không có screenshot hoặc tuyên bố desktop/mobile rendered pass.
- App tests/live Employee Chat: NOT RUN. Không inference, không proof/grant, không sửa hoặc restart shared gateway/DB. Proof mặc định vẫn không tồn tại; CG01 BLOCKED.
