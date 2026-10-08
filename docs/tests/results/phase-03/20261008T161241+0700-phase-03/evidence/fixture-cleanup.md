# Phase 03 fixture isolation and cleanup

`test_phase03_persistence.py::scoped_company` tạo 2 environment bằng `uuid4`, tạo company riêng cho từng scope và company thứ hai trong environment chính. Test ghi chỉ trong scope vừa tạo. Fixture teardown duyệt domain tables theo thứ tự dependency và DELETE WHERE environment_id bằng chính hai UUID đó rồi xóa đúng hai environment. Không truncate, không seed/reset scope demo hiện hữu.

Đã xác minh readiness trước khi chạy. Command test trả `5 passed in 1.38s`; cleanup nằm trong fixture teardown. Hạn chế: teardown chỉ được xác nhận qua source, test không in row counts sau cleanup.
