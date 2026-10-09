# Bằng chứng kiểm định framework pipeline

Các lệnh qua `/Users/buivannin/.local/bin/rtk proxy`, từ root repo:

- `python3 -m unittest discover -s scripts/tests -v`: 13 tests, exit 0, OK. AI /root/pipeline_qa chạy độc lập lần cuối và xác nhận cùng kết quả.
- `python3 scripts/render_plan.py`: đồng bộ master-plan.html, 24 phase, 4 hoàn tất; không thay nghiệm thu.
- `python3 docs/tests/scripts/validate.py`: kiểm cấu trúc/checklists/tags/links/HTML, không chạy sản phẩm hay inference.
- `git diff --check`: exit 0.

## Test → sửa → test lại đã thực hiện

| Issue AI độc lập phát hiện | Remake thực tế | Retest |
| --- | --- | --- |
| Test/remake cùng timestamp sort remake trước test, mất trạng thái sửa | Thứ tự timestamp/round/test trước remake | test_same_second_orders_test_before_its_remake pass |
| Rejected rebuttal đi cùng pass có thể đóng issue/OK | Rejected luôn giữ open/pending và không ready | test_rejected_rebuttal_with_inconsistent_pass_never_becomes_ok pass |
| Case bắt buộc bị khai optional/not-applicable vẫn OK | Expected cases bắt buộc mandatory/pass, không tin verdict đơn lẻ | test_required_checklist_cases_cannot_be_marked_optional_to_get_ok pass; repro độc lập trở thành testing |

Giữ các report/remake phase có sẵn; chu kỳ này là framework, không gán kết quả cho Phase 05. Không DB, gateway inference, commit hoặc push.

## Giới hạn

Browser tool từ chối mở `file://` roadmap theo chính sách URL. Không chuyển sang localhost hay surface khác để vượt chặn. Node DOM stub chỉ kiểm HTML output và JavaScript; chưa xác minh layout, responsive và thao tác trong browser thực.

HTML là snapshot files đã render; pipeline AI chạy trong phiên được giao phase, không có daemon hay browser tự khởi động agent nền.
