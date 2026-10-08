# Probe gateway live đã lọc

- Thời điểm: 2026-10-08, Asia/Ho_Chi_Minh.
- Lệnh: `rtk proxy python3 -c 'import sys; sys.path.insert(0,"src"); from agent_corporation_api.modules.codex_gateway.adapter import ProbeSettings, probe_gateway; print(probe_gateway(ProbeSettings()))'` (chạy tại `apps/api/`).
- Output: `{'status': 'offline', 'health': 'unavailable', 'catalog': 'unavailable', 'models': [], 'auth_configured': False, 'entitlement_verified': False, 'message': 'Không kết nối được gateway local; kiểm tra dịch vụ mà không thay cấu hình dùng chung.'}`
- Nguồn lỗi đã lọc: hai GET loopback gặp connection refused; không đọc/log exception, header hoặc secret.
- Không khởi động/restart server chung. Không POST, tạo session, prompt, inference hoặc fallback.
