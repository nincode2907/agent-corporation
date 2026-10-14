# Review UI Employee Chat — sau review Chủ tịch

> Ngày 14/10/2026. Chỉ kiểm tra prototype HTML thiết kế; không triển khai app/worker/gateway, không inference/proof/grant, không bắt đầu phase hoặc nghiệm thu sản phẩm. CG01 vẫn BLOCKED.

[Bản trực quan](employee-chat-ui-20261014.html) · [Prototype](../designs/employee-chat-prototype.html) · [Thiết kế](../designs/employee-chat.md) · [Independent review](employee-chat-ui-20261014/independent-review.md) · [Browser evidence](employee-chat-ui-20261014/browser-checks.json)

## Phạm vi và cách kiểm

Chrome qua CUA, viewport desktop 1440×1000 và mobile 390×844. Preview chỉ phục vụ bản sao HTML tài liệu từ thư mục tạm riêng trên 127.0.0.1:15593 trong block dự án đã kiểm registry/listeners; không phục vụ root repo, secret hay API. Tab/viewport/server QA được dọn sau kiểm tra. Không chạy application tests hoặc worker.

## Kết quả prototype

| Case | Tag | Kết quả | Evidence và giới hạn |
| --- | --- | --- | --- |
| UI01 — Chat-first desktop | clean | PASS | List 176 px, chat 1264 px khi Inspector đóng; mở Inspector 300 px thì chat 964 px. No horizontal overflow ở 1440 px. [Desktop](employee-chat-ui-20261014/desktop-1440.jpg), [Inspector](employee-chat-ui-20261014/desktop-inspector.jpg), browser record desktop-inspector-final |
| UI02 — Mobile 390 px | clean | PASS | scrollWidth=390, viewport=390; composerBottom=844 bằng chiều cao viewport; transcript cuộn riêng. [Mobile](employee-chat-ui-20261014/mobile-390-blocked.jpg), record mobile-layout-final |
| UI03 — Empty/loading/error/blocked/grant | clean | PASS | Đã đổi selector ở desktop và mobile. Empty/loading khóa metrics và không công bố số liệu fixture cũ; error tách lỗi tải khỏi gate, giữ bản nháp; blocked/grant chỉ dòng hướng dẫn composer. [Empty](employee-chat-ui-20261014/mobile-390-empty.jpg), [loading](employee-chat-ui-20261014/mobile-390-loading.jpg), [error](employee-chat-ui-20261014/mobile-390-error.jpg), [grant](employee-chat-ui-20261014/mobile-390-grant.jpg); browser evidence ghi từng state |
| UI04 — Keyboard/focus | clean | PASS | Enter mở review; Shift+Tab từ nút đầu quay về nút cuối; outline 3 px; Escape đóng và trả focus review-open. Mobile Inspector Escape trả focus inspector-open. Chỉ keyboard của prototype, không nghiệm thu assistive technology |
| UI05 — Inspector disclosure | clean | PASS | Đóng mặc định; desktop aria-expanded khớp; mobile aria-haspopup=dialog và controls trỏ mobile-dialog. Retest mobile không còn duplicate IDs. [Mobile Inspector](employee-chat-ui-20261014/mobile-inspector.jpg), browser record mobile-IDs-retest |
| UI06 — Chat → Work Order review | clean | PASS | Review sheet hiển thị excerpt, goal/output/criteria/recipient và dữ liệu chia sẻ trước tạo draft. Confirm nghiệp vụ bị disable trong prototype; cancel/Escape không tạo gì. [Review](employee-chat-ui-20261014/review-before-draft.jpg). Không kiểm backend idempotency/authorization vì chưa triển khai |
| UI07 — Usage/cost source drilldown | clean | PASS | Link assistant message mở whole-turn/call nguồn, confirmed usage/estimated API-equivalent cost/unknown call; user message chỉ dẫn turn liên quan, không phân bổ tokens giả. Coverage/as_of và correction có trong contract. [Drilldown](employee-chat-ui-20261014/message-call-drilldown.jpg). Chỉ fixture, không là số liệu hoặc giá thật |
| UI08 — TDG/dependency và quyền | clean | PASS tài liệu | Independent review xác nhận TDG OPEN trước inference06/backend chat13, không bypass/temporary proof, Owner decisions đầy đủ; IGCHAT không có vòng phụ thuộc EC11. Không có nghĩa gateway đã qualified |
| UI09 — Thiết bị thật/assistive technology | suggestion | NOT RUN | Chưa kiểm bàn phím ảo iOS/Android, safe-area thiết bị thật, VoiceOver/TalkBack hoặc trình duyệt khác; đưa vào EC01 sản phẩm Phase13/23. Không dùng viewport emulation thay nghiệm thu thiết bị thật |

## Findings đã sửa trong vòng này

Independent review ECR01–03: metrics sai ở empty/loading, semantics Inspector mobile, từ chưa Việt hóa. Tất cả được sửa và đọc lại; [review độc lập](employee-chat-ui-20261014/independent-review.md) ghi tag ban đầu/cuối.

Browser QA ban đầu phát hiện Escape và vòng focus chưa hoạt động đúng trong môi trường kiểm tra. Đã bổ sung xử lý Escape/Tab và trả focus trong HTML prototype; retest ghi focus-wrap/Escape restore đạt. Một ID trùng ở Inspector clone được phát hiện và loại bỏ, record retest cuối duplicates=[] giữ cùng evidence lịch sử. Mobile composer ban đầu nằm ngoài viewport; đã tách transcript scroll và bounded chat viewport, retest composerBottom=844. Những thay đổi này chỉ trong prototype tài liệu, không ứng dụng thật.

## Quyết định còn cần Chủ tịch

- Chốt target qualification: giữ target hiện tại nếu có evidence đáp ứng đủ hoặc phê duyệt chuẩn bị phương án gateway riêng; hiện dispatch KEEP-BLOCKED và decision OPEN.
- Chọn data scope/retention local-provider và chính sách backup/xóa; chốt platform V1 (Windows cần ACL/trust tương đương trước inference).
- Chốt tiêu chí cancellation, giới hạn chứng minh upstream và cách xử lý unknown usage/cost.
- Nếu giao qualification sau này: authorization riêng cho environment/thay đổi và batch/model/request cap/concurrency/timeout/expiry. Không có quyền này phát sinh từ việc duyệt thiết kế.

Chi tiết và các kết quả quyết định tại [TDG-CG01](../designs/cg01-technical-decision.md). Các lựa chọn không cản hoàn tất bản chỉnh tài liệu, và chưa được tự chọn thay Chủ tịch.

## Kiểm tra tài liệu và giới hạn bàn giao

Markdown được sửa trước rồi đồng bộ HTML cho thiết kế, TDG, ADR-0002, spec và roadmap. Giữ nguyên 24 phase, trạng thái nghiệm thu và CG01. Chỉ bản thiết kế và evidence tài liệu thay đổi trong lượt này; Python/app changes có trước lượt review được giữ nguyên. Renderer chat revision01 không được dùng ghi đè revision02; xem docs/designs/README.md.

Kết quả cấu trúc/liên kết/lang/favicon/JS syntax và git diff whitespace được kiểm tra riêng. PASS prototype không thay EC01–EC12/IGCHAT sản phẩm hoặc CG01 verification thực tế.
