# TDG-CG01 — Quyết định target inference trước khi xây chat backend

> Trạng thái: OPEN / chưa quyết định. Thiết kế sau review Chủ tịch 14/10/2026. CG01 vẫn BLOCKED, không proof/grant/inference hoặc thay đổi môi trường trong đợt này.

[Bản trực quan](cg01-technical-decision.html) · [CG01 evidence đã kiểm](../reviews/cg01-20261014/report.md) · [Employee Chat](employee-chat.md)

## 1. Vị trí và thẩm quyền

Gate kỹ thuật nằm ở Phase 05–06, phải chốt target trước inference đầu tiên và trước triển khai backend Employee Chat Phase 13. Không trì hoãn tới Phase 23. Tài liệu/prototype và fixture design vẫn làm được khi blocked; không tự bắt đầu phase.

AI báo cáo capability/gap bằng evidence; Chủ tịch chọn phương án target và quyền kiểm định/thay đổi được phép. Operator kiểm chứng và cấp proof sau khi đủ evidence thật. TDG-CG01 không thay CG01, grant, budget, stop hay nghiệm thu phase. Đồng ý target không đồng nghĩa cho phép provisioning, thay shared gateway, dùng credential hoặc gọi model. Chấp thuận residual risk không cho phép bỏ requirement bắt buộc chưa đạt.

## 2. Nhận định hiện tại từ bằng chứng

Source gateway hiện tại đã tắt nhiều native tools, bỏ user config/rules và dùng runtime thư mục tạm; chưa có bằng chứng runtime thực thi đầy đủ các ranh giới này. Provider còn dùng HOME/CODEX_HOME; native observer đọc native storage. Chat stateless không đồng nghĩa không lưu rollout. Socket abort/kill child chưa chứng minh upstream hủy hoặc dừng mọi subprocess. Proof chỉ ràng buộc một tập source, không chứng minh build/config/OS/retention thực tế.

Vì vậy chưa thể kết luận gateway hiện tại đạt CG01, cũng chưa có evidence để khẳng định mọi cách triển khai codex-server đều không thể đạt. Workflow quyết định target hiện vẫn OPEN; kết luận vận hành hiện tại là KEEP-BLOCKED (chưa đủ điều kiện dispatch), không phải một quyết định qualification đã hoàn tất. Hướng chuẩn bị đề xuất: một target dành riêng với HOME/CODEX_HOME/DATA_DIR và observer storage tách biệt, OS read/network boundary và retention có thể kiểm chứng. Đây là đề xuất cần Owner quyết định, chưa tạo instance hay chọn port mới.

## 3. Tiêu chí quyết định và đầu ra

| Tiêu chí bắt buộc | Giữ target hiện tại chỉ khi | Phải trình isolated gateway/remediation khi |
| --- | --- | --- |
| Loaded runtime identity | Có chain process → binary/dist/lock/config/SDK/CLI hash và chính sách áp dụng | Không thể gắn evidence với build thực hoặc shared changes không kiểm soát được |
| Read/context boundary | OS/process evidence chứng minh không đọc ngoài input/auth scope được duyệt; native observer cũng tách đúng phạm vi | Shared HOME/native storage hoặc quyền đọc chéo không thể cưỡng chế/kiểm chứng tại target này |
| Privacy/persistence | Inventory rollout/session/log/SQLite/temp/backup; Owner chọn retention; có access/deletion evidence và provider/account policy phù hợp | Không thể thực hiện retention/access theo yêu cầu hoặc private chat lẫn native/shared data |
| Cancellation | Đo abort/child/socket/late usage theo V05–06; nêu upstream limitations và đáp ứng tiêu chí dừng đã chốt | Không đáp ứng stop bound cần thiết hoặc cần sửa lifecycle/cancel mà shared instance không được phép thay |
| Proof/platform | Evidence thật, runtime binding, expiry, trusted permissions; Windows cần ACL tương đương hoặc platform hỗ trợ được chốt rõ | POSIX gate không áp dụng an toàn trên platform đích hoặc proof không ràng buộc boundary cần thiết |

| Kết quả TDG | Điều kiện và hành động kế tiếp |
| --- | --- |
| KEEP-BLOCKED | Thiếu evidence/authorization hoặc còn tiêu chí bắt buộc fail; ghi gap/Owner/next action, không dispatch |
| CURRENT-TARGET-QUALIFIED | Tất cả tiêu chí đủ evidence trên target hiện tại, independent review đạt, Owner chốt phạm vi sử dụng; sau đó mới operator issuance proof theo quy trình và grant từng batch riêng |
| ISOLATED-PROPOSAL-REQUIRED | Một tiêu chí không thể đáp ứng trên target shared; trình phương án tách process/user/container/storage/auth/observer/network/retention với validation/rollback; vẫn blocked đến khi target mới được duyệt, tạo và qualified |

“Có HTTP 200”, “tools=[]”, “đã login”, “một canary không bị đọc” hoặc “Owner chấp nhận rủi ro” riêng lẻ không phải CURRENT-TARGET-QUALIFIED.

## 4. Quy trình từ OPEN tới quyết định

1. Chốt threat model và data scope cho private chat; Owner chọn retention, platform và giới hạn cancellation cần đáp ứng. Đối chiếu V01–V07 trong báo cáo CG01, không tự nới baseline.
2. Non-inference discovery được cấp: đọc source/manifest, GET metadata và metadata proof; không đọc secret/transcript, không restart shared instance. Phần này đã có evidence ngày 14/10/2026.
3. Chuẩn bị hồ sơ target hiện tại và proposal target riêng: diagram boundary, data inventory, effective non-secret config, capability gaps, auth provisioning references, resource/cost uncertainty, allocation plan theo registry, rollback/cleanup. Chỉ là tài liệu, chưa thi hành.
4. Owner duyệt riêng test environment và các thay đổi cần thiết. Fixture CLI/transport + fake data + disposable DB kiểm wiring/OS/cancel/retention trước; không có production proof đạt từ mock.
5. Nếu cần provider thật để hoàn tất read/cancel verification, trình qualification procedure độc lập trên target cô lập, model/effort/cases/input giả, max requests kể cả retry, concurrency, timeout, expiry và accounting rõ. Chỉ chạy khi được cấp authorization riêng; không đi qua worker bằng proof tạm hoặc bypass CG01. Task hiện tại cấm thực thi bước này.
6. AI review evidence, đưa một trong ba kết quả kèm fail/unknown/residual limitations và platform scope. Chủ tịch chọn target và phê duyệt phần thay đổi; nếu thiếu bằng chứng thì giữ blocked.
7. Chỉ operator có đủ evidence mới phát hành proof hợp lệ. App sau đó vẫn cần grant đúng phase/batch/operation, budgets và Emergency Stop. IGCHAT kiểm tích hợp sau Phase 19, không thay qualification trước Phase 06.

## 5. Gói proposal cô lập cần trình nếu target hiện tại không đạt

- Process/user/container riêng; mount/read allowlist tối thiểu, deny ngoài scope và egress policy; tách tool executor khỏi inference.
- HOME/CODEX_HOME/DATA_DIR, auth material, rollout/session/SQLite/WAL/log/temp/backup và native observer riêng; không copy credential qua chat hoặc từ store shared tùy tiện.
- Contract HTTP/stateless tương thích, source/runtime fingerprint inventory, model/effort support; không tự đổi provider/baseline.
- Retention/purge/access/restore policy có evidence, bảo toàn audit/ledger và không hứa upstream deletion ngoài khả năng kiểm chứng.
- Cancel/timeout/stop lifecycle với yêu cầu đo rõ, unknown handling và late usage; không hứa hard token/USD cap khi contract thiếu.
- Port/hostname proposal theo Dev Hub registry; kế hoạch reserve → verify → configure chỉ sau Owner cấp quyền. Validation, rollback và cleanup không tác động shared target.

## 6. Chủ tịch còn cần quyết định

| Quyết định | Gợi ý để duyệt, chưa thực thi |
| --- | --- |
| Target qualification | Chuẩn bị phương án gateway dành riêng, giữ shared target blocked đến khi có evidence đạt; không tự provisioning |
| Platform V1 | macOS/Linux trước hoặc bổ sung Windows ACL/trust design và kiểm chứng tương đương trước inference Windows |
| Data/retention | Loại dữ liệu được phép gửi, retention local/provider, quyền truy cập và yêu cầu xóa/backup; app-private không bằng provider-private |
| Cancel acceptance | Thời gian stop cần đo, bằng chứng process/upstream có thể lấy và cách xử lý usage unknown; không coi socket đóng là xác nhận provider dừng |
| Test authorization | Nếu muốn tiến hành qualification sau này: phê duyệt environment và batch/model/limits/expiry cụ thể; không có grant hoặc inference authorization phát sinh từ tài liệu này |

Đây là các quyết định chuẩn bị cho lượt triển khai/kiểm định được giao sau, không phải câu hỏi phê duyệt ngầm hoặc điều kiện cần trả lời để hoàn tất việc chỉnh tài liệu hiện tại.
