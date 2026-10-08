# Live probe — Phase 05 r001

Thời điểm: 08/10/2026, Asia/Ho_Chi_Minh. Gọi adapter với cấu hình mặc định, chỉ GET `http://127.0.0.1:4000/health` và `/v1/models`.

Output đã lọc: `status=offline`, `health=unavailable`, `catalog=unavailable`, `models=[]`, `auth_configured=false`, `entitlement_verified=false`. Gateway không nhận kết nối. Không chạy/restart gateway, không gửi prompt, POST, session hay tool.
