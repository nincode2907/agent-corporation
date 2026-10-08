# UI observations — Phase 02

- Desktop 1848 CSS px: sidebar điều hướng 14 trang, header, dashboard title, demo banner, panels và trạng thái API/DB hiện diện; screenshot được quan sát trong phiên CUA nhưng không được ghi thành file trong workspace.
- Sidebar: 14/14 link điều hướng tới hash tương ứng và heading trang khớp. Back từ onboarding về settings và reload vẫn giữ #settings.
- Hai góc nhìn: Vận hành/Chủ tịch đổi aria-pressed và heading; source handler chỉ đổi local state `mode`.
- Keyboard: Tab tới S06, Enter mở approvals; Shift+Tab quay S13; Escape giữ focus trên S14; focus-visible rule có trong CSS.
- Mobile viewport: 390×844; innerWidth=390, document clientWidth=375, document scrollWidth=375; không có tràn ngang ở document. Menu sidebar có overflow-x:auto và mục cuối có thể được mở bằng link. Screenshot mobile được quan sát nhưng không lưu file.
- Metadata: html lang=vi; icon là SVG data URI.
- Dashboard hiển thị nhãn Demo/fixture cho mọi count; usage unknown, cost chưa xác định, inference=0.
- Không bấm reset demo/probe, không gọi API mutation.
