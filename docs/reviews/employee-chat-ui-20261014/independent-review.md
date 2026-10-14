# Review độc lập — điều chỉnh thiết kế Employee Chat

Ngày: 14/10/2026. Reviewer: agent độc lập `/root/employee_chat_revision_review`; agent sửa tài liệu và kiểm tra trình duyệt là `/root`.

Phạm vi: đọc Markdown và source HTML thiết kế; không sửa prototype, không chạy app/product tests, không kiểm tra provider, không gọi inference hoặc tạo proof/grant. Kết quả trình duyệt do agent chính ghi riêng; review này không nhận là đã tự quan sát hình ảnh hoặc thao tác desktop/mobile.

## Findings và xác minh lại

| ID | Tag ban đầu | Finding | Xác minh source cuối | Tag cuối |
| --- | --- | --- | --- | --- |
| ECR01 | `need-change` | Empty/loading vẫn mở metrics có số call fixture dù chưa có dữ liệu hội thoại | `setState()` khóa conversation/Inspector metrics ở empty/loading và thay nội dung usage thành chưa có lượt gọi/đang tải; message actions được ẩn cùng transcript | `clean` |
| ECR02 | `need-change` | Inspector mobile tham chiếu aside ẩn và giữ trạng thái expanded sai khi dialog mở | `syncInspectorControl()` dùng `aria-controls=mobile-dialog`, `aria-haspopup=dialog`, bỏ expanded trên mobile; desktop vẫn dùng expanded của aside. Clone mobile bỏ ID trùng | `clean` |
| ECR03 | `need-change` | Preview bar còn từ tiếng Pháp | Đã đổi thành “Bản chỉnh 02” và “Dữ liệu minh họa” | `clean` |
| ECR04 | `suggestion` | TDG OPEN và KEEP-BLOCKED dễ bị hiểu là hai kết luận mâu thuẫn | Technical decision giải thích OPEN là workflow chưa chốt target, KEEP-BLOCKED là kết luận vận hành hiện tại | `clean` |

Nguồn của ECR01–03: [employee-chat-prototype.html](../../designs/employee-chat-prototype.html). ECR04: [technical decision](../../designs/cg01-technical-decision.md), mục 2. Tag `clean` ở đây chỉ xác nhận nội dung/source thiết kế đã giải quyết finding; không xác nhận Employee Chat sản phẩm hoạt động hoặc CG01 đạt.

## Review bảy yêu cầu

| Yêu cầu | Tag | Kết luận và bằng chứng source |
| --- | --- | --- |
| Chat-first, readable/responsive | `clean` | Prototype mặc định 176 px list, chat chiếm phần còn lại, Inspector ẩn; giới hạn dòng 76ch. Mobile một cột với dialog; viewport chat có transcript cuộn riêng và composer ngoài vùng cuộn. [Thiết kế](../../designs/employee-chat.md), mục 2; browser QA vẫn là nguồn cho kết quả hiển thị thật |
| Giảm mật độ kỹ thuật | `clean` | Context/policy/provenance/metrics nằm trong Inspector và disclosure. Header/chat không chứa manifest dài |
| CG01/grant gọn, có hướng xử lý | `clean` | Dòng trung tính dưới composer, đọc lịch sử/soạn draft vẫn được; help dẫn TDG hoặc Quản trị. Send luôn disabled trong prototype, không thao tác gate/grant |
| Owner review trước tạo task | `clean` | Review sheet nêu chưa tạo Work Order/task/proposal, chỉ chia sẻ excerpt; xác nhận nghiệp vụ disabled. Thiết kế mục 6 quy định trước review/confirm không có draft/task/queue/proposal persistent; submit/approval là bước riêng |
| Usage/cost có nguồn | `clean` | Drilldown conversation/message → turn/span/call; fixture ghi rõ input/output của toàn turn. Confirmed usage, estimated cost, unknown call độc lập; Owner message không bị gán cost trùng. Thiết kế mục 5 quy định unique spans, coverage/as_of, pricing sources và late correction |
| Technical decision trước inference/backend chat | `clean` | [TDG](../../designs/cg01-technical-decision.md) đặt ở 05–06, trước inference đầu tiên và backend Phase 13; có ba kết quả và proposal cô lập. Không có quyền bỏ requirement bắt buộc, cấp proof tạm hoặc provisioning ngầm |
| Desktop/mobile/keyboard/states | `clean` | Source có desktop/collapsible Inspector, breakpoint mobile, dialog labels, Escape/Tab/focus return, empty/loading/error/blocked/grant fixtures. Đây là review source; [UI review](../employee-chat-ui-20261014.md) ghi phạm vi và kết quả browser QA riêng |

Không còn finding thiết kế bắt buộc chưa xử lý trong phạm vi đã đọc. Không nâng tag này thành product acceptance, phase acceptance hoặc inference authorization.

## Dependency và quyết định của Chủ tịch

Đã đọc [master plan](../../master-plan.md), [product spec](../../product-spec.md) và [ADR-0002](../../decisions/0002-employee-chat.md): Phase 06 yêu cầu TDG/CG01 trước inference, Phase 13 chỉ bàn giao foundation với send khóa; context/finance/stop ở 15/16/19, IGCHAT sau 19 trước 20, restore/hardening ở 22–23. Không thấy dependency ngược 13 → 19 hoặc sự thay thế live evidence bằng mock. Qualification cô lập cần authorization riêng; không dùng worker với proof tạm để gỡ vòng phụ thuộc.

Các quyết định còn mở đã được ghi đủ trong TDG mục 6: target qualification/shared hay proposal riêng; platform V1 và Windows ACL; loại dữ liệu/retention local-provider/backup; tiêu chí cancellation và unknown usage; environment/batch/model/limits/expiry cho qualification tương lai. Những lựa chọn này cần Chủ tịch chốt trước triển khai/qualification được giao sau; không cản hoàn tất việc sửa tài liệu hiện tại, không phát sinh quyền thực thi.

CG01 vẫn BLOCKED. Bản thiết kế chi tiết chưa được tự chốt/nghiệm thu; không bắt đầu phase tiếp theo.

## Evidence bổ sung và ranh giới thay đổi

Đã đọc [browser-checks.json](browser-checks.json) do agent chính tạo: số đo desktop 1440 px, mobile 390 px, focus wrap/Escape return, metrics empty/loading và retest duplicate IDs đều có record. Record mobile Inspector ban đầu còn duplicate ID được giữ trong lịch sử; record `mobile-IDs-retest` cuối ghi `duplicates: []`. Đây là kiểm tra evidence của agent chính, không phải browser session do reviewer này chạy.

Agent chính xác nhận thay đổi Python trong working tree (`scripts/validate_phase00.py`, renderer chat đã có) là phần tồn tại trước lượt điều chỉnh này. Lượt hiện tại chỉ sửa Markdown/HTML và evidence tài liệu; không cần revert thay đổi của lượt trước. Không dùng git diff toàn working tree để quy mọi thay đổi sẵn có cho lượt review này.
