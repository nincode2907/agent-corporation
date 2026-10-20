# Integration Fix 05 — Vertical slice

## Kết quả

Đã nối đường đi first-class Runtime Run từ Owner đã đăng nhập → nhân viên demo hiện hành → grant đã cấp tường minh → Run text-only → Runtime worker được Compose giám sát → event đã commit → Live Office → Inspector → Replay chỉ đọc.

Đây là kiểm định bằng dữ liệu giả lập trong stack Docker/PostgreSQL dùng riêng. Gate adapter và transport giả chỉ được gắn trong harness; `RUNTIME_CG01_DEMO_TEST_OVERRIDE=false`, CG01 thật chưa được xác minh, không gọi Codex gateway/model và kết quả này không nghiệm thu Phase 06–08.

## Nối employee với Run

- API `GET /api/v1/runtime/employees` trả nhân viên active/probation cùng EmployeeVersion mới nhất trong đúng demo scope đã khóa.
- `POST /api/v1/runtime/runs` bắt buộc `employee_id` và `employee_version_id`. Service khóa lifecycle nhân viên, xác nhận employee/version thuộc đúng environment/company, đúng version mới nhất và còn được giao việc.
- Run giữ `employee_version_id` cùng snapshot employee, Owner model profile, model/effort được grant cho phép và policy/grant. Employee identity/version được đưa vào system context dưới dạng metadata; tools vẫn tắt.
- Event của Runtime Run lưu cùng `run_id`, `task_id`, `agent_id` và `employee_version_id`. EmployeeVersion lịch sử không bị thay khi hồ sơ hiện hành đổi. Run cũ không có employee vẫn đọc được và hiện “Chưa phân công nhân viên”.
- Không cần migration: dùng `runs.employee_version_id`, EmployeeVersion, snapshot và các bảng/runtime liên kết đã có.

## Worker và trạng thái

Compose khởi chạy một Runtime worker với PostgreSQL advisory lock theo scope. Lock giữ trên cùng một physical connection đến lúc worker thoát; tiến trình cạnh tranh không dispatch. Worker kiểm tra gate trước claim và ngay trước transport, phục hồi `dispatched` hết lease thành `unknown`, không phát lại request không chắc kết quả. `Playground` vẫn dùng worker/queue riêng.

Dừng trước khi gọi transport là lỗi cục bộ đã biết, kết thúc Run và giải phóng dispatch guard. Nếu request đã được gọi rồi bị hủy/đóng trước final response, Run thành `unknown`/`interrupted`, guard vẫn giữ để ngăn một request thứ hai khi kết quả gateway chưa thể xác minh. Hiện chưa có Owner reconciliation route cho unknown call; đây là blocker vận hành cần giải quyết trước khi bật inference thật.

## Trình duyệt và DB

Chrome desktop 1440×900 và mobile 390×844 đã đi qua form Owner, waiting state, Office, link từ employee sang Inspector đúng Run, link sang Replay đúng Run, seek và reload. Ba Run synthetic đã hoàn tất; mỗi Run có đúng một model_call và 10 event được đối chiếu cùng employee/version/task/run.

Replay trước/sau có cùng số lượng: 3 Runtime Run, 3 model_call, 54 event, 8 Work Order, 4 artifact, 9 checkpoint và 3 request đã dùng. Chi phí hiển thị chưa biết. Ảnh và số liệu đối chiếu nằm trong `evidence/`.

## Ranh giới còn lại

Chưa nối Work Order queue/lease với Runtime Run. Không thêm executor thứ hai. Phase 09 nên nhận accepted Work Order revision và tạo first-class Run qua cùng Runtime service, giữ nguyên task/revision/assignee/grant, idempotency và policy. Chi tiết ở [phase09-bridge-plan.md](phase09-bridge-plan.md).
