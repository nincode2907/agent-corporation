# UI acceptance review

## Cách kiểm tra

Đã dùng Chrome/Playwright với Owner session cục bộ trên site local. Script giữ secret trong bộ nhớ, không lưu vào screenshot/manifest và đăng xuất sau lượt kiểm tra. Runtime dashboard và các trang đọc dữ liệu không gửi inference. Desktop: 1440×900; mobile: 390×844.

Ảnh gốc và số đo nằm trong `evidence/screenshots/`; `evidence/visual-acceptance.json` ghi assertions, viewport, lỗi trang/console và logout. `evidence/contact-sheet.png` gom ảnh để review nhanh.

## Kết quả

| Hạng mục | Kết quả | Ghi chú |
|---|---|---|
| Dashboard | Đạt | Hiển thị Demo Corporation và số lượng 3 hồ sơ. |
| Employee và EmployeeVersion | Đạt | Runtime form có 3 lựa chọn và chọn được version. |
| Model profile, authorization, grant | Đạt | Mô tả rõ profile; CG01 strict bị chặn và không có grant hợp lệ. |
| Start | Đạt | Disabled khi thiếu grant/CG01; không tạo Run trong DB dùng chung. |
| Live Office | Một phần | Điều hướng và responsive đạt; ledger không có Runtime Run nên lane rỗng, Office không trình bày ba employee với trạng thái. Không tạo Run giả trong DB dùng chung. |
| Inspector và Replay | Đạt cho empty/history view | Điều hướng và hiển thị empty/read-only state thành công. DB dùng chung không có lịch sử Runtime Run để kiểm tra chi tiết Run. |
| Playground | Đạt cho route/read-only state | Mở trang; không tạo Playground session/turn. Dữ liệu Playground tách biệt Runtime. |
| Unknown reconciliation | Đạt trong stack tổng hợp riêng | `interrupted`/`unresolved`; usage và cost `unknown`; dispatch guard vẫn giữ; không có force-unlock. |
| Responsive | Đạt về tràn ngang | Các viewport trong manifest có `scrollWidth` bằng chiều rộng viewport. |

### Synthetic reconciliation

`evidence/reconciliation-smoke.mjs` dùng Compose project riêng, Owner giả, fake gate và fake worker không có network transport tới gateway. Một synthetic Run được dispatch bằng transport giả, worker riêng bị dừng, lease được làm hết hạn trong DB dùng một lần, rồi service recovery ghi nhận unknown. Màn hình cho thấy `unresolved`, usage/cost `unknown`, dispatch guard giữ nguyên và không có hành động force-unlock. Logout và `docker compose down --volumes` chỉ áp dụng cho stack/volume tổng hợp đã cách ly; kiểm tra sau chạy xác nhận stack đó được dọn.

## Điểm còn thiếu

Acceptance yêu cầu Live Office thể hiện ba employee với state. Deployment hiện có ba employee fixture nhưng không có Run để xác định state. Office chỉ render employee từ Run đã ghi; không suy diễn trạng thái từ fixture. Đây là thiếu hụt thật về tiêu chí hiển thị, không thể kết luận đạt bằng dashboard count. Cần quyết định riêng về fixture/read-only view hoặc tạo dữ liệu chấp nhận trong scope tổng hợp; không dùng dữ liệu runtime chung.

Console báo một lỗi trong lần điều hướng UI (không có page error); không ảnh hưởng assertions hoặc health. Chưa xác định nội dung lỗi và không dùng nó làm bằng chứng về lỗi dịch vụ.

## Gemini

**NOT PERFORMED.** Không có phiên/công cụ Gemini được ủy quyền để gửi ảnh đã đăng nhập. Gói review đã khử credential gồm contact sheet, ảnh gốc, manifest viewport và hành trình kiểm tra; không có cookie, Owner secret hay secret runtime.
