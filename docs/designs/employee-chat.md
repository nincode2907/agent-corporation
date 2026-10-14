# Employee Chat — trao đổi riêng với nhân viên AI

> Bản điều chỉnh sau review Chủ tịch ngày 14/10/2026; đồng ý kiến trúc tổng thể, thiết kế chi tiết chưa chốt. Chưa triển khai, chưa kiểm thử sản phẩm, chưa nghiệm thu. CG01 giữ BLOCKED; không cấp grant hoặc gọi inference.

[Bản thiết kế trực quan](employee-chat.html) · [Prototype tương tác và trạng thái](employee-chat-prototype.html) · [Technical decision gate](cg01-technical-decision.md) · [Đặc tả V1](../product-spec.md) · [Roadmap](../master-plan.md) · [CG01](../reviews/cg01-20261014/report.md)

## 1. Mục đích và phạm vi riêng tư

Chủ tịch có thể mở cuộc trò chuyện một-một với bất kỳ nhân viên nào thuộc công ty đang chọn, để hỏi, trao đổi và xem xét ý tưởng. Nhân viên offboarded hoặc chưa có profile được duyệt vẫn có trang lịch sử/giải thích khóa; không dispatch cho hồ sơ không đủ điều kiện. Nhân viên idle không tự gọi model. Không tạo Work Order hoặc thay đổi tổ chức khi gửi tin nhắn.

“Riêng” nghĩa là nội dung chỉ được đọc qua phiên Owner đã xác thực và backend trong đúng environment/company/employee/conversation. Nhân viên khác, supervisor, báo cáo tổng hợp và context/memory retrieval không được tự đọc hay lập chỉ mục nội dung chat. Đây không phải cam kết mã hóa đầu-cuối hoặc gateway không lưu prompt: gateway/provider vẫn nhận context đã chọn; giới hạn lưu giữ phải được xác minh qua CG01 và thông báo trước khi gửi. Một Owner local trong V1; không thêm tài khoản nhân viên người dùng.

## 2. Các lối vào và màn hình S15

| Lối vào | Hành động | Dữ liệu được giữ |
| --- | --- | --- |
| Hồ sơ nhân viên S07 | Nút “Trao đổi riêng” cạnh tên/vai trò | Employee ID, company/environment; không mang task context ngầm |
| Org chart S07 | Chọn nhân viên → panel hồ sơ → “Trao đổi riêng” | Cùng employee; giữ vị trí sơ đồ khi quay lại |
| Agent Inspector S03 | Tab “Trao đổi riêng” hoặc nút ở header | Mở conversation của nhân viên; task/run chỉ là link tham khảo, không tự chép vào prompt |

S15 dùng chung một route `/employees/:employeeId/chat/:conversationId?`, trong scope phiên Owner; backend xác minh ID thuộc scope. Danh sách nhiều cuộc hội thoại trên cùng nhân viên, không gộp nhân viên khác. Reload/đổi lối vào mở cùng conversation theo ID; mở trang chỉ GET, không gửi model. “Cuộc trò chuyện mới” tạo thread rỗng theo lệnh Owner có CSRF/idempotency, không inference. Mặc định mở thread gần nhất còn phù hợp, không tự đổi profile của thread cũ.

### Bố cục và hệ thống thị giác

Kế thừa nền kem nhạt, chữ xanh đen, đường viền mảnh và typography hệ thống hiện có. Dùng trang làm việc, không hero marketing hoặc avatar giả đang suy nghĩ. Thanh đầu: breadcrumb công ty → nhân viên, tên/vai trò, trạng thái lifecycle, nhãn “Trao đổi riêng”. Tách nhãn môi trường demo/benchmark/real luôn nhìn thấy.

Desktop chat-first: danh sách hội thoại 176 px, message area lấy toàn bộ phần còn lại, Inspector mặc định đóng. Ở 1440 px vùng chat 1264 px khi đóng Inspector và 964 px khi mở trong prototype đã kiểm tra; nội dung tin tối đa 76 ký tự mỗi dòng, cỡ chữ 16 px/line-height 1.65. Inspector mở rộng khoảng 300 px theo yêu cầu và có nút thu gọn luôn thấy. Header chỉ giữ tên/vai trò, model/profile ngắn và trạng thái; context/policy/provenance/version manifest và detailed metrics nằm trong Inspector. Tin Chủ tịch và nhân viên có tên, thời gian, trạng thái lưu, action menu; tránh bubble màu gây khó đọc đoạn dài. Tin model render Markdown đã sanitize, không HTML hoặc action handler do model cung cấp.

Composer ghim cuối gồm textarea có label, hướng dẫn phím tắt và trạng thái quyền gửi gọn, nút “Gửi” và “Dừng phản hồi” khi có call đang chạy. Enter xuống dòng; Ctrl/Cmd+Enter gửi; hỗ trợ IME. Giữ draft local theo scope/conversation khi lỗi, không đưa vào logs/URL; xóa draft khi logout/đổi company theo policy riêng tư. Không upload file hoặc đọc đường dẫn host trong chat V1.

Inspector đóng mặc định, mở bằng nút “Thông tin”; có approved employee/profile/model/effort/context/policy versions, byte/context cap, trạng thái grant và budget, các call IDs, tokens, chi phí/basis/coverage; “Xem lần gọi” mở Inspector metadata và “Nguồn context” xem manifest được phép. Nếu chưa có call, hiển thị “Chưa có lượt gọi”; nếu call thiếu usage, hiển thị “Chưa biết”. Không có live token counter hoặc token streaming giả. Câu trả lời chỉ xuất hiện sau final response đã commit.

Mobile 390 px: một cột, message area không bị chia cột; danh sách hội thoại và Inspector mở thành modal sheet/drawer bằng nút có label. Native dialog giữ focus, Escape/Đóng trả focus về nút mở; composer không che tin cuối hoặc lỗi; không cuộn ngang. Keyboard truy cập đủ ba lối vào, focus trở lại đúng nhân viên; transcript `role=log` với thông báo trạng thái ngắn `aria-live=polite`, không đọc lại toàn bộ lịch sử mỗi SSE event. Contrast, reduced motion, textarea label và focus ring theo design system; `lang=vi`, favicon. Bản HTML đính kèm là prototype tài liệu, dữ liệu minh họa, không kết nối API.

### Trạng thái cần thiết kế

| Trạng thái | Thông báo và hành động |
| --- | --- |
| Chưa có hội thoại | “Trao đổi riêng với [tên]”; gợi ý câu hỏi tĩnh theo vai trò, click chỉ điền draft |
| Loading / lỗi tải | Skeleton thật trong lúc GET; lỗi và nút tải lại; không sinh tin chào model tự động |
| Signed out / session hết hạn | Khóa gửi, yêu cầu đăng nhập; transcript không hiển thị cho phiên khác |
| CG01 blocked | Dòng trung tính ngay composer: “Đang chờ xác minh gateway · Xem bước xử lý”; không dùng banner lỗi trong transcript. Giữ lịch sử/draft; Send khóa; hướng dẫn mở technical decision gate và điều kiện còn thiếu |
| Thiếu/hết hạn/revoked grant hoặc budget | Dòng composer “Chưa có hạn mức phù hợp · Xem hướng dẫn”; phân biệt thiếu grant, grant hết hạn và hết budget trong phần giải thích mở thêm; link Quản trị, không cấp grant ngay tại chat |
| Chờ hàng đợi / đang chờ model | Hiển thị elapsed từ timestamps có nguồn; không hứa token-by-token |
| Đang dừng / outcome unknown | Phân biệt yêu cầu dừng, HTTP đã đóng, provider đã xác nhận hủy; không báo “đã hủy hoàn toàn” khi thiếu bằng chứng |
| Offline / timeout / crash | Giữ tin đã commit; call unknown và chặn gửi lại call đó; nút xem sự cố/đối chiếu |
| Profile/context đã đổi hoặc nhân viên offboarded | Lịch sử vẫn giữ version cũ; khóa lượt mới, cho xem diff và tạo nhánh bằng version được duyệt khi đủ điều kiện |
| Emergency Stop | Banner toàn ứng dụng, khóa gửi và dispatch; chỉ Owner gỡ tại trung tâm sự cố |
| Context quá lớn | Nêu cap và nguồn; cho chọn đoạn/nhánh mới hoặc yêu cầu tóm tắt được duyệt; không cắt im lặng |
| Archived / nội dung đã purge | Read-only; tombstone và lý do retention; không tái tạo nội dung từ gateway |

## 3. Profile, model và context

Conversation pin `employee_version_id`, approved model profile version, model/effort, context manifest version và policy version. Mỗi turn có snapshot riêng của cùng bộ tham chiếu và hash context envelope; prompt builder phía backend chỉ dùng nguồn được cấp, không tin model tự khai version. Từ chối profile chưa được duyệt, model không được cho phép hoặc entitlement chưa được xác minh trong phạm vi được cấp. Không fallback model tự động.

Khi có version mới, không âm thầm cập nhật conversation cũ. Owner xem diff và chọn “Bắt đầu với phiên bản mới”, tạo conversation nhánh có link về bản cũ; chỉ các đoạn Owner chọn và được ACL cho phép mới được mang sang. Thu hồi quyền/lifecycle/retention có hiệu lực ngay: snapshot lịch sử không phải quyền tiếp tục dùng context đã bị thu hồi.

Context gồm policy hệ thống, profile nhân viên được duyệt, context corporate/department/employee theo ACL và lịch sử của đúng conversation. Không tự lấy task context, chat nhân viên khác hoặc trí nhớ gateway. Nội dung người dùng/model là dữ liệu không tin cậy; không thể sửa permission hay prompt policy có thẩm quyền. Mỗi lần gửi recheck quyền đọc mọi nguồn; nguồn hết hạn/mất quyền → chặn và yêu cầu Owner chọn lại.

App lưu transcript và context manifest trong PostgreSQL/artifact store có ACL; tiếp tục sau restart bằng lịch sử app, gửi stateless tới `/v1/chat/completions`, không dùng gateway session ID làm khóa durability. Cap đề xuất cho chat V1: tối đa 128 messages và toàn bộ HTTP JSON không quá 64 KiB để phù hợp transport hiện tại; giới hạn nào nhỏ hơn được áp dụng. Tóm tắt bằng model là một call có grant/budget riêng, có nguồn và Owner duyệt summary version; không thay thế hay xóa bản gốc ngầm.

## 4. Dữ liệu và luồng giao dịch đề xuất

| Thực thể dự kiến | Ràng buộc |
| --- | --- |
| Conversation | UUID + environment/company/employee, Owner actor, title, version pins, active/archived, revision; composite scoped FK và RLS |
| ChatMessage | conversation ID + seq, role Owner/assistant/system-notice do server cấp, body ref/digest, timestamps, turn ID; append-only, sửa tin tạo nhánh/version |
| ChatTurn / ContextManifest | Một user message + selected context refs + expected conversation revision; pending/queued/reserved/dispatching/completed/failed/unknown/cancelled; approved snapshot refs |
| ModelCall / Reservation / Ledger | `subject_type=chat` + chat_turn_id; subject task/run hoặc chat, đúng một loại; gateway call ID nullable, usage/price nullable và provenance |
| ChatEvent / Outbox | Company sequence + private conversation refs; actor/versions/call/stop epoch; không chứa body trong SSE chung |
| PromotionDraft / ProposalLink | Owner-selected message IDs/version hashes, redacted excerpts, target draft/proposal ID, expected versions và approval refs |

Đây là schema cần triển khai bằng migration Phase 13–16, không phải bảng đã có. `runtime_runs`/model call/event hiện tại thiên về task/run: không tạo task giả để chat. Mở rộng subject discriminated union và registry/event schema bằng migration kiểm tra FK/RLS; quy tắc hiện có “run có task” vẫn giữ nguyên. Event chat dự kiến: CONVERSATION_CREATED, CHAT_MESSAGE_COMMITTED, CHAT_TURN_STATE_CHANGED, CHAT_PROMOTION_DRAFTED; dùng chung LLM_CALL_*, TOKEN_USAGE_RECORDED và budget events sau khi hỗ trợ subject chat. Không giả chúng đã tồn tại trong catalogue hiện tại.

Send command: Owner session + CSRF + verified scope → validate employee/version/context/CG01/grant/budget/stop → transaction ghi user message, turn, queue job và outbox với idempotency key + expected revision. Khóa một active turn/conversation; global concurrency baseline 1, cùng pool với Work Order, không dùng chat để vượt cap. Hai tab gửi đồng thời: một command thắng, tab còn lại nhận conflict kèm reload; double-submit cùng key trả cùng receipt.

Dispatch: claim lease → recheck CG01/expiry/Owner scope/lifecycle/approved versions/context ACL/stop epoch → atomically reserve request/budget + call span và commit → recheck trước HTTP → text-only request với tools=[], tool_choice=none, stream=false, explicit model/effort. Không có tool executor trong route chat; không cấp credential ghi cấu hình cho model. Tool-call output hoặc lệnh đổi cấu hình không được dispatch; hiển thị lỗi/phản hồi đã lọc, ghi audit. Nếu response là lời gợi ý, chỉ hiển thị văn bản.

Finish: transaction commit assistant message + turn result + usage/ledger/events; sau commit mới báo UI. Timeout/disconnect/crash/stop race → unknown, không tự resend. 429 chỉ requeue khi có bằng chứng chưa dispatch và còn grant, giữ bounded attempts. Lease hết hạn không phải bằng chứng request chưa chạy. Restart/reconnect chỉ đọc saved state; unknown phải đối chiếu call/outcome trước khi Owner chủ động thử lượt mới. Late usage append correction một lần vào call gốc, không mở lại grant. Không dùng gateway stats chung để suy tokens của conversation.

## 5. Quyền, grant, ngân sách và Emergency Stop

Chat dùng cùng CG01 hợp lệ và cơ chế Owner grant, không có exemption vì là “trò chuyện”. Grant cần operation scope `employee_chat`, environment/company/employee/conversation hoặc allowlist hẹp, phase/test_batch_id/purpose, model/effort, request cap gồm retry/summary, concurrency, timeout, expiry và cost basis. Grant Work Order không tự áp sang chat; đây là extension phải triển khai, API hiện tại chưa có đầy đủ fields chat. Hiện không tạo grant. UI chỉ chọn grant Owner đã cấp và phù hợp.

Mỗi request tính vào giới hạn company/employee/conversation và grant; reservation atomic với pool Work Order. Thiếu usage giữ unresolved/unknown và xử lý theo policy, không release thành zero. Cost có amount nullable, currency/basis/pricing version/source; API-equivalent là ước tính, không hóa đơn subscription. Không cam kết token hoặc USD hard cap trong một request khi gateway không nhận max_tokens/không có giá đáng tin.

Period operating cost gồm cả chat trong kỳ; drilldown riêng company → employee → conversation → turn → call. Chat không vào mẫu số “task được nghiệm thu”; tạo task từ chat không chuyển hồi tố chi phí chat thành task cost hoặc tính hai lần. Một call có đúng một cost subject; báo cáo có filter/coverage/as_of và corrections.

Emergency Stop durable chặn mọi chat dispatch mới cùng Work Order và tools; abort HTTP app đang chờ, ghi stop epoch và outcome thực tế. Không dừng shared gateway hoặc call ứng dụng khác. Resume sau Owner gỡ stop vẫn recheck gate/grant/versions/ACL và unknown; không phát lại tin cũ. Chat không được tự sửa cấu hình, quyền, model, nhân viên, tổ chức, memory hoặc cấp việc qua lời model. Backend từ chối các action này trong mode chat kể cả khi prompt yêu cầu.

### Drilldown usage/cost ở conversation và từng message

Conversation hiển thị tóm tắt nhỏ “Tokens / chi phí” có thể mở; không nhồi ledger vào header. Tổng tính theo tập request_span_id duy nhất của conversation, gồm retries và summary calls được cấp; không cộng lại tokens lặp ở nhiều message. Coverage ghi rõ số call có nguồn/tổng call và thời điểm as_of. Khi còn call unknown, tổng là phần đã biết + số call chưa biết, không gọi đó là tổng đầy đủ.

| Mức xem | Nội dung và provenance | Quy tắc confirmed / estimated / unknown |
| --- | --- | --- |
| Conversation | Tổng unique call, confirmed input/output/total, số unknown, cost tách basis/currency, coverage và as_of | Không cộng confirmed/estimated/unknown thành một số không nhãn; thiếu price không làm mất tokens đã confirmed |
| Assistant message | Link “Lượt gọi & chi phí” → chat_turn_id → request_span_id → gateway_call_id nullable, model/profile/context refs | Usage do gateway final response là confirmed của toàn turn (gồm system/context/history), không chỉ text câu trả lời |
| Owner message | Chỉ rõ không có usage đo riêng; link đến turn phản hồi liên quan | Không tự chia token/cost theo số ký tự hoặc gán cùng cost cho cả user và assistant message |
| Call / ledger | Source response/receipt ref, measured_at, usage dimensions, reservation, pricing version/source_at, cost basis/currency, corrections | Confirmed usage có thể đi cùng estimated API-equivalent cost; giá/usage thiếu → unknown; không gắn confirmed cho hóa đơn subscription từ phép nhân API price |

Unknown usage và unknown cost là hai trường độc lập. Ước tính phải hiển thị “Ước tính tham khảo” và nguồn/phiên bản; zero chỉ hiển thị khi có nguồn xác nhận 0. Late correction là entry append-only vào đúng call/message/turn gốc, conversation cập nhật as_of, không đếm trùng hoặc chuyển vào task tạo sau. Prototype chỉ dùng fixture có nhãn; không là giá hoặc usage thật.

## 6. Chuyển hội thoại thành công việc hoặc đề xuất

1. Owner chọn đoạn tin cụ thể và bấm “Tạo bản nháp công việc” hoặc “Soạn đề xuất”. Không quét/phát tán toàn bộ hội thoại.
2. Review sheet trình bày trích đoạn được chọn, nguồn/version, dữ liệu riêng nào sẽ được chia sẻ, mục tiêu/đầu ra/criteria dự kiến và assignee/scope. Soạn thủ công không inference; nếu muốn AI điền nháp, đó là call được cấp riêng.
3. Chỉ sau màn review có trích đoạn được chọn, mục tiêu, đầu ra, criteria, assignee, dữ liệu chia sẻ và cảnh báo chưa thực thi, Owner bấm “Xác nhận tạo bản nháp”. Trước thao tác này không tồn tại task/draft/queue item/proposal persistent nào; modal review chỉ là UI state. Owner sửa và xác nhận tạo draft bằng CSRF/idempotency/expected revision. Chỉ lưu draft và link provenance, không enqueue, approval hoặc inference tự động.
4. Work Order submit và proposal approval dùng quy trình quyền/grant/payload hash/version/expiry hiện có, có review riêng cho tác động. Hủy review sheet không tạo đối tượng; double click không tạo trùng; stale excerpt/version phải review lại.

Nhân viên đích/reviewer chỉ thấy trích đoạn Owner đã duyệt theo ACL của draft/proposal; không được đọc transcript gốc. Proposal đổi quyền/model/HR vẫn phải qua inbox owner-only; lời đồng ý trong chat không được coi là quyết định quyền.

## 7. Lộ trình và dependency

Giữ 24 phase và trạng thái nghiệm thu hiện tại. Đây là bổ sung phạm vi thiết kế, không giao triển khai các phase.

| Phase | Bổ sung | Điều kiện |
| --- | --- | --- |
| 05–06 | TDG-CG01 quyết định khả năng target + CG01 verification và baseline grant/reservation/cancel/stop | Không bỏ gate; mọi test model cần authorization đúng batch |
| 09–10 | Work Order draft/proposal review contract; authorization của subject chat | Tách command chat và task, no implicit submit/config change |
| 13 | S15 + ba lối vào; conversation/message/turn schema, RLS, approved pins, durable resume, text-only chat backend | Sau 12, target của TDG-CG01 được Owner chốt và baseline 03/06/07/08/10; fixtures và non-inference QA; gửi thật còn khóa đến IGCHAT |
| 14 | Offboard/drain/revoke dừng chat đúng version | Không xóa history; chặn lượt mới theo lifecycle |
| 15 | Context ACL/version manifest/summary/retention, chat riêng không auto promotion | Sau 14; khớp cap transport và source permissions |
| 16 | Subject-aware ledger/budget/concurrency và conversation drilldown | Sau 15; unknown/late usage không zero/double count |
| 19 | Emergency Stop/cancel/crash/recovery của chat cùng Work Order | Sau 18, chat 13/15/16 và authorization 10 |
| IGCHAT | Checkpoint sau 19, trước 20; không là phase mới | 13/14/15/16/19 được kiểm định; CG01 + batch grant hợp lệ cho live tests; phần thiếu giữ BLOCKED |
| 22–23 | Backup/retention/privacy và release UI/E2E employee chat | IGCHAT + restore chat + Owner nghiệm thu V1; real vẫn khóa đến release |

Không tạo dependency ngược 13 → 19: Phase 13 bàn giao foundation/fixture với send bị khóa; Phase 19 mới đóng tích hợp để mở live employee chat. Không có cơ chế “demo mode” bỏ CG01 hoặc giả chat thật. Trước IGCHAT PASS, chỉ batch kiểm định trên môi trường cô lập đã được Owner cấp quyền mới được dispatch các ca live của IGCHAT; mỗi call vẫn kiểm CG01/grant/budget/stop bình thường. Đây là qualification test qua luồng được kiểm soát, không mở gửi cho sử dụng thông thường hoặc tạo gate exemption. General send chỉ được mở sau IGCHAT đạt, và real usage còn phải chờ release decision.

### Technical decision gate phải xử lý sớm

[TDG-CG01](cg01-technical-decision.md) nằm trong 05–06, trước inference đầu tiên và trước backend chat Phase 13. Kết quả là KEEP-BLOCKED, CURRENT-TARGET-QUALIFIED hoặc ISOLATED-PROPOSAL-REQUIRED; chưa có quyết định trong đợt này. Gate quyết định target không thay proof CG01, không cấp quyền provisioning/inference, và Owner không thể biến bằng chứng chưa đủ thành PASS chỉ bằng chấp nhận rủi ro. Phương án cô lập cần được trình cụ thể và phê duyệt riêng trước thay đổi.

## 8. Tiêu chí kiểm chứng dự kiến

Tất cả ca sau là NOT RUN, không có tag clean hoặc tuyên bố pass. Khi triển khai, AI tester độc lập ghi results/remakes theo RULES và đặt tag cho từng ca dựa trên bằng chứng.

| Case | Kiểm chứng / evidence cần có | Phase |
| --- | --- | --- |
| EC01 | Ba entry points mở đúng employee/company/thread; desktop/390 px, Inspector mặc định thu gọn, keyboard/focus và empty/loading/error/blocked/grant states | 13, 23 |
| EC02 | Cross-company/environment/employee và non-Owner API/DB/attachment refs bị deny; private transcript không vào SSE/log/search/memory khác | 13, 15, 22 |
| EC03 | Profile/context pins; revoked ACL, model/profile change, offboard → không dispatch; nhánh mới cần Owner chọn | 13–15 |
| EC04 | CG01 thiếu/expiry/fingerprint mismatch, thiếu/revoked/expired/wrong operation grant, budget exhausted → zero POST | 13, 16, 19 |
| EC05 | Double submit/two tabs/worker race → một user message/turn/reservation; task + chat cùng pool không vượt cap | 13, 16 |
| EC06 | Restart/reconnect lưu history/pins chính xác, stateless gửi lại approved envelope; không gateway memory, no auto inference | 13, 15 |
| EC07 | Tool/config/permission/model/HR instruction và tool_calls không có side effect; sanitized rendering/CSRF/session expiry | 10, 13, 22 |
| EC08 | Conversation/message→turn→call drilldown, confirmed/estimated/unknown độc lập, coverage/as_of, unknown tokens/cost, late usage correction/dedup; subject chat không tạo task cost hoặc accepted-task KPI giả | 16 |
| EC09 | Stop/abort/timeout/crash và race; no new dispatch sau stop, unknown không auto resend; provider cancellation chỉ claim theo evidence thật | 19 |
| EC10 | Select excerpts → review → draft/proposal, cancel/stale/double click; không enqueue/approval tự động, không rò transcript | 09–10, 13, 15 |
| EC11 | Backup/restore/retention purge/tombstones giữ ledger và scope/pins; không phát lại call | 22 |
| EC12 | Live Chairman → employee reply → restart/resume → usage/cost trace và stop trong isolated authorized environment | IGCHAT, 23 |

IGCHAT cần fixture/negative/concurrency evidence EC01–10 ở baseline 13–19 và run thật có grant cho EC12/cancellation liên quan; EC11 backup/restore cùng hardening EC02/07 ở 22 là điều kiện release 23, không phải prerequisite của checkpoint trước 20; không thay live evidence bằng mock. Private tại app không đủ nếu CG01 chưa xác minh gateway persistence/retention/read boundary. Release R1–R8 phải bao phủ chat tương ứng với task.

## 9. Điều chỉnh sau review và kiểm chứng prototype

Phạm vi lần chỉnh: chỉ Markdown/HTML thiết kế; không thay app, gateway, worker hoặc grant. Prototype là tài liệu tương tác không lưu dữ liệu, không gọi API, không tạo task; mọi nút xác nhận nghiệp vụ thật bị khóa. Kết quả kiểm tra desktop/390 px, focus và các trạng thái sẽ được ghi trong [UI review](../reviews/employee-chat-ui-20261014.md). Kiểm chứng prototype không thay EC01–EC12 của sản phẩm chưa triển khai.
