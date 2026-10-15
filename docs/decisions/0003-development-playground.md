# ADR-0003 — Development Playground Mode

> Ngày: 14/10/2026 · Phạm vi: phần bổ sung demo của Phase 06 · Quyết định thiết kế theo yêu cầu Chủ tịch; implementation và kiểm định được ghi trong master plan. Không là nghiệm thu production hoặc grant inference hiện tại.

## Bối cảnh

Lượt inference thật đã thành công nhưng grant một request và worker thủ công làm gián đoạn thử nghiệm. Cần trò chuyện tự nhiên trong demo trong khi runtime Work Order và CG01 production vẫn giữ hợp đồng hiện có. Đây là Playground thử nghiệm, không triển khai Employee Chat S15/IGCHAT production của các phase sau.

## Quyết định

- Tạo route `#playground` và module API `/api/v1/playground`, bảng `playground_sessions`/`playground_turns` riêng. Không tạo Work Order, task, runtime run hay quyền nhân viên từ tin nhắn.
- Tái sử dụng Owner session/CSRF/Host/Origin, RLS, event/outbox allocator, transport HTTP giới hạn và global dispatch guard. Background worker do FastAPI lifespan quản lý, chỉ nhận queue Playground của demo cố định. Không tự dispatch Work Order.
- Owner chọn nhân viên demo, model/effort và chấp nhận chính sách Development Playground v1 khi tạo Session Grant. Model profile được kiểm catalog rồi snapshot theo version. Grant từ 1–100 requests, thời hạn 1–240 phút, concurrency 1, timeout mỗi request tối đa 120 giây. UI mặc định gợi ý 20 requests/30 phút; không cấp trước khi Owner bấm nút. Grant không gia hạn/tăng hạn mức/tái cấp tự động. Đăng xuất hoặc expiry của Owner session gốc dừng grant.
- Một lần cấp quyền cho cả session. Mỗi tin nhắn có idempotency key bền vững; cùng key/nội dung trả lại turn cũ, khác nội dung bị từ chối. Một pending turn mỗi session; một HTTP call toàn app nhờ guard dùng chung.
- Worker reserve request và tăng used count atomically trước POST. Tools, tool_choice, network tools và fallback đều bị cố định off phía backend, API từ chối trường cấu hình tools. Không có executor file/terminal/deploy/company mutation. Response chứa tool calls bị từ chối thành unknown.
- Lịch sử nằm trong PostgreSQL; gateway dùng stateless endpoint. Context gồm persona demo tối thiểu và tối đa 10 cặp hoàn tất gần nhất, giảm từ cặp cũ nhất để dưới 48 KB. Mọi turn lưu history/profile/policy snapshot. Prompt/output không đưa vào event feed; event gắn correlation_id=session và payload session_id/turn_id.
- Usage chỉ xác nhận từ response gateway, thiếu là `null`/unknown, chi phí unknown. Không suy token từ text hoặc dùng native/global totals. Không chặn chat tiếp chỉ vì usage chưa có, vì grant này giới hạn request chứ không tuyên bố token/USD hard cap.
- Stop trước dispatch hủy queued turn. Stop/expiry/logout khi request đang bay đóng HTTP và giữ outcome unknown; worker chết sau reservation được lease recovery thành unknown, không replay. Global guard giữ đến khi Owner xác nhận đã kiểm tra request gateway kết thúc. Xác nhận này không đổi outcome/usage unknown, không refund request và không gửi lại tin cũ. Late completion sau recovery bị fence.
- Policy Playground là ngoại lệ riêng dựa trên Owner consent đã lưu, demo cố định và gateway HTTP literal loopback hợp lệ. Không đọc/ghi proof hoặc gọi `runtime_gate` để tự đánh verified. `verified=false` luôn được ghi. Grant runtime cũ không dùng được cho Playground và ngược lại.

## Ranh giới gateway

Source gateway đang chạy trên Windows được truy từ listener 15600 tới `F:/Workspace/dev/projects/local-tools/local-server`. README/schema/provider đã được đọc: transport stateless, usage gồm wrapper; provider cấu hình web_search disabled, shell/unified_exec/apps/plugins/multi-agent/computer-use off, network_access false, read-only và từ chối agent tool events. Đây là cấu hình/source evidence, chưa là proof isolation/privacy/retention/cancellation. Không sửa gateway chung hoặc cấu hình production CG01.

## Nghiệm thu tách biệt

Playground có checklist DPG01–DPG10 riêng: Owner/consent/demo scope, multi-turn, auto worker, limits/expiry/concurrency, idempotency, Stop, crash/restart/no replay, tools deny, trace/unknown usage, UI recovery. Test tự động dùng gateway giả và PostgreSQL disposable; inference thật chỉ khi Owner cấp Session Grant thực tế. Mock không là evidence model entitlement hoặc isolation production.

Production Phase 06 và release R1–R8/CG01/IGCHAT giữ nguyên các điều kiện. PASS Playground không đánh Phase 06 Hoàn tất hoặc mở công ty thật. Hạn chế: không streaming token, native cancellation/read isolation chưa chứng minh, unknown có thể cần Owner đối chiếu, lịch sử context có cửa sổ, API process phải đang chạy.

Migration `20261014_0009` bổ sung hai bảng/RLS và merge hai heads 0008 hiện có; không sửa dữ liệu Work Order cũ. Seed/reset demo có FK RESTRICT nên từ chối reset nếu còn session Playground; không xóa ngầm lịch sử/grant/calls.
