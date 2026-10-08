# Kiểm định Phase 02 — Khung giao diện Chủ tịch

> Checklist dự kiến, chưa có kết quả test. AI đọc lại nguồn hiện tại trước mỗi batch; không gắn tag sẵn hay tự nghiệm thu.

[Rule](../RULES.md) · [Điểm vào](../README.md) · [Mẫu report](../templates/report.md) · [Roadmap](../../master-plan.md) · [Spec V1](../../product-spec.md) · [ADR](../../decisions/0001-v1-foundation.md)

## Nguồn và ranh giới

- Phase: 02
- Dependency từ roadmap: 01
- Yêu cầu liên quan: REQ03, REQ04, REQ26
- Gate: Không có gate IG riêng; vẫn kiểm criteria phase và C01–C08
- Contract hash: 30dd8e93768cde3d9e2f4369c7aeafcb0695634f755b2052242ac6dce528fd4a

Hash đối chiếu scope/demo/criteria/delivery/limits/evidence/dependency tại thời điểm soạn, không bao gồm status/nhật ký. Nguồn đổi thì cập nhật kế hoạch, không sửa report cũ. Snapshot bên dưới giúp traceability; nguồn hiện tại vẫn ưu tiên.

### Phạm vi phải đọc

- Design system, navigation, trang dashboard và hai chế độ Chủ tịch/Vận hành.
- Empty/loading/error states, layout responsive, bàn phím và focus.
- Phác khung Live Office, Inspector, task, phê duyệt, tài chính, tổ chức.

### Demo bắt buộc

Đi từ dashboard vào task và inspector shell ở desktop/mobile; xem khi API lỗi. Dùng CSS breakpoint 390 px để xác minh không tràn ngang.

### Giới hạn phase

Chưa có agent đang hoạt động; không dựng hoạt cảnh giả.

### Evidence bàn giao cần đối chiếu

Ảnh desktop/mobile, kiểm tra accessibility và các trạng thái.

## Mapping nghiệm thu → test

Mỗi AC là gạch đầu dòng nghiệm thu roadmap hiện tại khi soạn. Kiểm thêm C01–C08 theo rule; tiêu chí thay đổi cần remap trong report. Mọi case dưới đây bắt buộc trong phạm vi phase; không gọi inference nếu chưa có grant, mà ghi blocked cho case cần run thật.

| Tiêu chí | Kỳ vọng từ roadmap | Test IDs tối thiểu |
| --- | --- | --- |
| AC1 | Không có số giả trình bày như dữ liệu thật. | P02-04 |
| AC2 | Luồng điều hướng chính dùng được bằng bàn phím, lang vi và favicon đúng. | P02-01, P02-05 |
| AC3 | Không tràn ngang ở 390 px; desktop giữ thứ bậc nội dung rõ. | P02-06, P02-07 |

## Ca kiểm định riêng của phase

Mỗi dòng là một test phải có record kết quả riêng. Các biến thể negative/race trong dòng ghi sub-results/evidence để không bỏ sót; nếu một biến thể bắt buộc chưa đạt, cả test không clean. C01–C08 cũng phải có record riêng.

| ID | Test | Bước/điều kiện | Kỳ vọng | Evidence cần lưu | Nguồn bổ sung |
| --- | --- | --- | --- | --- | --- |
| P02-01 | Điều hướng chính | Đi dashboard/task/Inspector/phê duyệt/tài chính/tổ chức, back/reload | Khung nhất quán, đúng nhãn và trạng thái chưa triển khai | Ảnh và danh sách thao tác | Spec §3 |
| P02-02 | Hai mode Owner | Đổi Chủ tịch/Vận hành bằng chuột và bàn phím | Mode chỉ đổi cách nhìn, không tuyên bố quyền khác hay API mới | Ảnh/source route review | Spec §2/10 |
| P02-03 | Empty/loading/error | Dùng delay/offline/mock response không inference, phục hồi API | Phân biệt trống/đang tải/lỗi/offline; phục hồi đúng | Network conditions và ảnh trước/sau | Spec §3 |
| P02-04 | Không số/hoạt cảnh giả | So dashboard/Live Office shell/metrics với source và network | Không fixture/số giả như thật; preview ghi chưa dữ liệu | Source/ảnh/call counts | Spec §2/3 |
| P02-05 | Bàn phím và semantics | Tab/Shift-Tab/Enter/Escape, xem focus, labels, heading và lang/favicon | Luồng chính không mất focus/trap, labels đọc được, tiếng Việt | Interaction notes và ảnh/DOM | Spec §3 |
| P02-06 | Mobile 390 px | Dùng viewport browser đúng 390 px, đo scrollWidth/clientWidth và điều hướng | Không tràn ngang hoặc che thao tác; CSS breakpoint đơn lẻ chưa đủ | Ảnh + số đo viewport/overflow | Spec §3/13 |
| P02-07 | Desktop hierarchy | Mở desktop, xem title/primary action/sidebar, các state | Đọc được, không chồng lấn, dùng tokens/component nhất quán | Ảnh desktop và source refs | Spec §3 |

## Lệnh và điều kiện chạy

Các lệnh đã tồn tại tại lúc soạn (từ root), chưa được chạy trong lượt tạo tài liệu này:

```sh
rtk proxy npm run --prefix apps/web build
rtk proxy npm run --prefix apps/web lint
```

Phase 00 validator gọi renderer và có thể cập nhật HTML: kiểm diff/bản nhìn trước khi chạy. Pytest Phase 03 kết nối DB thật và tạo/xóa fixtures qua migration role: xác minh scope/cleanup từ source và chỉ chạy trên DB kiểm định được phép. Build/lint không thay proof runtime/UX. Migration `current` chỉ đọc version; `upgrade/downgrade`, restart và faults phải chuẩn bị môi trường riêng theo rule.

## Kết luận và lưu kết quả

Tạo `docs/tests/results/phase-02/<test_batch_id>/report.md` và `evidence/`. Ghi C01–C08 + P02-01…P02-07 + case bổ sung; mỗi test có đúng một tag `clean`, `need-change`, `suggestion`, result, expected/actual và evidence. Thống kê đầy đủ, kết luận kỹ thuật theo rule, quyết định Chủ tịch riêng. Dừng tại Phase 02.
