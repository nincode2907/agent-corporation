# Fixture isolation and cleanup

`test_demo_seed_and_reset_are_deterministic_and_scope_limited` chạy trên fixed UUID demo environment/company đang `kind=demo`, `release_locked=true`. GET trước test xác nhận manifest hiện tại trùng baseline v1. Test gọi `ensure_demo_scope`, rồi reset ba lần; assert manifest/version/state counts/approval/retry/artifact/unknown usage/inference count.

Test tạo UUID mới cho benchmark và synthetic-real environment/company/task/artifact. Sau reset, assert SHA-256 và storage_key của artifacts còn nguyên. Cuối happy path, xóa các rows canary theo chính IDs và assert không còn environment kind=real. Final GET sau suite trả đúng manifest trước test. Đây là test dùng PostgreSQL thật, không mock DB.

`test_demo_reset_http_requires_confirmation_and_rejects_scope_targets` khẳng định false confirmation → 400; extra environment/company targets → 422; dashboard trả đúng fixed demo IDs. Không gửi reset HTTP hợp lệ trong case này.

Test tạo canary real tổng hợp tạm thời trong local DB test, không phải công ty người dùng; đã cleanup. Không có ledger schema/thread namespace/file store để đặt canary tương ứng.
