# Bộ kiểm định theo phase

Bộ rule cho AI đọc sau khi triển khai một phase hoặc khi Chủ tịch yêu cầu kiểm định lại. Có checklist cho Phase 00–23, mẫu báo cáo và nơi lưu evidence từng đợt. Đây là kế hoạch kiểm định, không phải bằng chứng các phase đã đạt.

[Bản trực quan](index.html) · [Rule bắt buộc](RULES.md) · [Mẫu báo cáo](templates/report.md) · [Kết quả kiểm định](results/README.md)

## Cách dùng

1. Đọc `AGENTS.md` root → `docs/tests/RULES.md` → `docs/tests/phases/phase-NN.md`.
2. Đọc block Phase NN và dependency trong [master-plan](../master-plan.md), phần spec/ADR được checklist dẫn tới, diff/source/test thực tế và evidence bàn giao. Đối chiếu nguồn hiện tại, không lấy checklist cũ làm đặc tả mới.
3. Chốt phạm vi batch, môi trường test, danh sách test bắt buộc và quyền đã có. Chạy các kiểm tra được phép; giữ test bị chặn trong báo cáo.
4. Lưu `docs/tests/results/phase-NN/<test_batch_id>/report.md` và evidence đã lọc. Gắn một tag cho **mỗi** test, ghi kết quả, kỳ vọng, thực tế và đường dẫn evidence.
5. Báo kết luận kỹ thuật, lỗi cần sửa và đề xuất. Dừng ở phase được giao; Chủ tịch quyết định nghiệm thu riêng.

Yêu cầu mẫu cho AI:

> Kiểm định Phase 03 theo docs/tests/RULES.md và docs/tests/phases/phase-03.md. Đọc nguồn hiện tại, chạy test phù hợp trong phạm vi được phép, lưu report và evidence theo test_batch_id trong docs/tests/results/phase-03/. Gắn clean/need-change/suggestion cho từng test. Không inference, không tự sửa code, nghiệm thu hoặc chuyển phase.

## Ý nghĩa tag

| Tag | Khi dùng | Ảnh hưởng |
| --- | --- | --- |
| `clean` | Test đã chạy, đạt đủ kỳ vọng, có evidence kiểm chứng | Đủ bằng chứng kỹ thuật cho test này |
| `need-change` | Test fail, bị chặn, chưa chạy hoặc thiếu evidence bắt buộc | Chưa đủ để xác nhận tiêu chí; nêu lỗi hay khoảng trống, không bịa bug |
| `suggestion` | Tiêu chí đã đạt nhưng có cải tiến tùy chọn; hoặc case tùy điều kiện được loại trừ hợp lệ | Không dùng cho lỗi hay tiêu chí bắt buộc chưa chứng minh |

Tag khác kết quả thực thi và mức độ lỗi. Xem quy tắc chi tiết trong [RULES.md](RULES.md).

## Checklist theo phase

| Phase | Checklist | Test riêng | Gate |
| --- | --- | --- | --- |
| 00 | [Chốt đặc tả V1](phases/phase-00.md) | 7 | — |
| 01 | [Dựng nền phát triển local](phases/phase-01.md) | 7 | — |
| 02 | [Khung giao diện Chủ tịch](phases/phase-02.md) | 7 | — |
| 03 | [Dữ liệu và bằng chứng bền vững](phases/phase-03.md) | 9 | IG03 |
| 04 | [Nhà máy công ty demo](phases/phase-04.md) | 7 | — |
| 05 | [Kết nối Codex server local](phases/phase-05.md) | 7 | — |
| 06 | [Agent đầu tiên chạy trong sandbox](phases/phase-06.md) | 8 | — |
| 07 | [Luồng event và khôi phục kết nối](phases/phase-07.md) | 7 | — |
| 08 | [Live Office và Agent Inspector](phases/phase-08.md) | 7 | IG08 |
| 09 | [Bảng nhiệm vụ và hàng đợi](phases/phase-09.md) | 7 | — |
| 10 | [Quyền hạn và hộp phê duyệt](phases/phase-10.md) | 7 | — |
| 11 | [Hệ thống công cụ thực thi](phases/phase-11.md) | 7 | — |
| 12 | [Điều phối nhiều nhân viên](phases/phase-12.md) | 7 | IG12 |
| 13 | [Tổ chức và hồ sơ nhân viên](phases/phase-13.md) | 7 | — |
| 14 | [Tuyển dụng và thử việc](phases/phase-14.md) | 6 | — |
| 15 | [Context và trí nhớ có kiểm chứng](phases/phase-15.md) | 6 | — |
| 16 | [Tài chính và ngân sách](phases/phase-16.md) | 8 | IG16 |
| 17 | [Benchmark và chất lượng](phases/phase-17.md) | 6 | — |
| 18 | [Đề xuất tối ưu có thử nghiệm](phases/phase-18.md) | 6 | — |
| 19 | [Sự cố và dừng khẩn cấp](phases/phase-19.md) | 7 | — |
| 20 | [Lịch làm việc và báo cáo điều hành](phases/phase-20.md) | 7 | IG20 |
| 21 | [Wizard thành lập tập đoàn](phases/phase-21.md) | 7 | — |
| 22 | [Bảo vệ dữ liệu và khôi phục](phases/phase-22.md) | 7 | — |
| 23 | [Nghiệm thu và phát hành V1](phases/phase-23.md) | 10 | R1–R8 + IG03/08/12/16/20 |

## Công cụ tài liệu local

Từ root repo; các lệnh này chỉ đọc/ghi tài liệu trong `docs/tests/`, không kết nối DB, gateway hoặc chạy test sản phẩm:

```sh
rtk proxy python3 docs/tests/scripts/render.py
rtk proxy python3 docs/tests/scripts/validate.py
```

`validate.py` kiểm tra đủ 24 phase, test IDs, mapping tới tiêu chí roadmap/spec, links, report đã lưu và HTML đồng bộ. Nó không chứng minh sản phẩm đã đạt. Dùng `--batch docs/tests/results/phase-NN/<test_batch_id>` để kiểm tra riêng một báo cáo trước bàn giao. Placeholder trong template không phải kết quả test.

## Cập nhật bộ kiểm định

Sửa Markdown trước. Khi roadmap/spec đổi phạm vi, đối chiếu và cập nhật checklist phase liên quan, giữ IDs cũ cho cùng tiêu chí; thêm ID mới nếu bổ sung test, không tái dùng ID cho nghĩa khác. Thay đổi checklist không sửa báo cáo cũ. Render lại `index.html` và chạy validator trong cùng lượt. HTML là trang hướng dẫn/tra cứu; AI luôn đọc Markdown đầy đủ.

Bộ này được soạn từ nguồn local ngày 08/10/2026. Không hardcode trạng thái phase hay inference grant hiện tại trong checklist; mỗi đợt phải đọc nguồn và quyền tại thời điểm chạy.
