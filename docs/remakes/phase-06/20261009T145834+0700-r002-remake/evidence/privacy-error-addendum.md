# Bổ sung xử lý lỗi DB trước khi chốt retest r003

Phát hiện khi rà lại source: exception SQLAlchemy chưa được xử lý ở runtime API/worker CLI có thể đưa SQL bound parameters chứa input/history vào traceback. Bổ sung generic503 cho API (no-store) và worker CLI dừng exit1 bằng thông báo chung; không phát lại call, giữ cơ chế lease recovery/fence hiện có. Không thay gateway, grant hoặc kiến trúc.

Kiểm tra remake: `rtk proxy uv run --project apps/api pytest apps/api/tests/test_sensitive_validation.py apps/api/tests/test_phase06_runtime.py apps/api/tests/test_phase07_feed.py -q`: exit0,34 pass. Hai regression mới dùng StatementError với secret canary giả, xác minh API trả503 không echo tham số và worker exit1 không in canary/traceback. Không DB hoặc inference thật.

Đây là bổ sung cuối của source; [manifest bổ sung](privacy-error-manifest.json) lưu hash sau sửa. Manifest/source snapshot trước đó được giữ nguyên. Kết luận độc lập thuộc report r003, không tự đánh dấu clean hoặc hoàn tất phase.
