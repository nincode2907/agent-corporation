# UI Fix 07 — Quyết định UX

## Mục tiêu màn hình

Live Office là roster nhân sự trong scope Owner hiện tại. Nhân viên và cơ cấu tổ chức vẫn xuất hiện khi chưa có Runtime Run; Run chỉ bổ sung trạng thái và bằng chứng thực thi đã lưu.

## Nguồn và ngữ nghĩa trạng thái

- Roster lấy từ `GET /api/v1/runtime/employees`, nguồn Owner-scoped có EmployeeVersion hiện hành, lifecycle, role và department. Không dựng lại employee hoặc department từ fixture giao diện.
- Trạng thái thực thi so theo đúng EmployeeVersion được lưu trong Run. Run cũ vẫn có trong lịch sử nhưng không đổi trạng thái của version hiện hành.
- `Không có Run đang hoạt động` chỉ hiển thị khi Runtime status đã tải và SSE feed đang live. API offline, stream stale/gap/reconnecting và đang tải có trạng thái riêng; các trạng thái đó không kết luận nhân viên idle.
- Chỉ Run đã lưu ở các trạng thái active mới làm thẻ hiện hoạt động. Failed/unknown được tách rõ; unknown có liên kết đọc reconciliation.
- Profile trong Run gần nhất lấy từ Run đó. Nếu chưa có Run trên EmployeeVersion hiện hành, thẻ ghi model/effort của Owner là cấu hình dùng chung, không phải cấu hình riêng của nhân viên.

## Hành động

- “Mở form Runtime” giữ chính xác `employee_id` và `employee_version_id`. Nếu version thay đổi trước khi form tải, form để trống lựa chọn và giải thích blocker, không tự chuyển sang version khác.
- Chi tiết hồ sơ hiển thị ID/version/lifecycle/phòng ban đã biết. Lịch sử giữ link Inspector/Replay cùng Run ID; link reconciliation chỉ có khi Run outcome unknown.
- Inspector và Replay nhận `run_id` từ URL hash mỗi lần điều hướng, không chỉ lúc mount.
- Runtime Start hiển thị blocker backend/UI hiện tại cho profile chưa lưu, employee/version, grant, CG01, tài nguyên và Run chưa đối chiếu. Không tự tạo hoặc gia hạn grant.

## Bố cục và khả năng tiếp cận

- Giữ bảng màu, panel, typography và controls đã có; thêm lưới roster theo phòng ban thật, card nhận diện gọn, trạng thái đọc nhanh và history disclosure.
- Desktop dùng nhiều cột theo độ rộng khả dụng; mobile chuyển một cột, cho phép ID dài xuống dòng và giữ hành động trong tầm bấm.
- Dùng nhãn tiếng Việt, heading/landmark, `details/summary`, focus ring cho bàn phím, trạng thái tải/lỗi có thông báo, và tôn trọng `prefers-reduced-motion`.
- Không thêm typing/thinking/token animation, 3D, Employee Chat hay model inference.

## Chẩn đoán bất thường Deployment 06

Ảnh mobile cũ được tái kiểm bằng hai capture: trạng thái ngay sau chuyển trang là shell/skeleton trong lúc Owner session và dữ liệu tải; trạng thái sau khi route sẵn sàng hiển thị Playground ở 390 px không tràn ngang. Bằng chứng phù hợp với capture timing/conditional loading hơn là màn hình chủ ý để trống. Nó không đủ để khẳng định chính xác frame cũ được chụp ở thời điểm nào.

Console error duy nhất là HTTP 401 cho `GET /api/v1/owner/session` trước khi đăng nhập. Đây là response của Owner gate; sau đăng nhập không có `pageerror`. Không sửa code để che response 401 này.

## Giới hạn còn lại

Office chỉ nhận tối đa 20 Run gần nhất từ API; copy trên thẻ ghi rõ giới hạn này. Run ngoài cửa sổ đó không thể được khẳng định là không tồn tại. Mock transport chỉ dùng kiểm định UI cô lập; không chứng minh CG01, entitlement hoặc IG08.
