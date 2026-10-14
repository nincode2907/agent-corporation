# CG01 — Báo cáo kiểm tra và kế hoạch xác minh

Ngày 14/10/2026 · Phạm vi: integration Agent Corporation → gateway `127.0.0.1:15600`. Đây là review source và kiểm tra đọc an toàn, không phải nghiệm thu CG01. [Bản trực quan](report.html) · [Evidence JSON](evidence.json) ghi thời gian, HTTP kết quả, metadata file, listener và SHA-256 của nguồn đã đọc.

**Kết luận: BLOCKED.** `check_gate` thực tế trả `allowed: false`, `reason: missing_or_invalid_proof`. `.local/` và `.local/cg01-proof.json` đều chưa tồn tại. Không tạo proof, không tạo grant, không gửi inference và không đổi/restart gateway. CG01 giữ nguyên trạng thái chặn.

## VERIFIED

| Phạm vi | Bằng chứng được kiểm tra | Điều đã xác minh và giới hạn |
| --- | --- | --- |
| Live HTTP | GET `/health`, `/v1/models`, `/api/models` đều 200; body trong evidence | Gateway trả health/catalog; không chứng minh model entitlement, login, inference isolation hoặc retention. |
| Live listener | `lsof`: Node PID 86867, IPv4 `127.0.0.1:15600` | Listener gateway được quan sát là loopback tại thời điểm kiểm tra; chưa kiểm tra toàn bộ reverse proxy/OS firewall/đường truy cập khác. |
| Proof hiện tại | `lstat` đường dẫn mặc định và `check_gate` bằng module hiện tại | Proof mặc định thiếu; gate đóng. Không đọc `.env`, credential, lịch sử chat hoặc DB dùng chung. Không khẳng định cấu hình runtime bí mật có cùng mọi giá trị mặc định. |
| App dispatch, source | `execution/worker.py`, `gateway.py`, `gates.py` | Worker kiểm gate trước reservation và kiểm lại ngay trước dispatch; payload text có `tools: []`, `tool_choice: none`, `parallel_tool_calls: false`, `n: 1`, `stream: false`. App dùng stateless POST `/v1/chat/completions`, không cần gateway sessions. |
| App cancellation, source | `worker.py`, `gateway.py` | Worker kiểm stop/grant expiry định kỳ khoảng 0,2 giây cộng thời gian DB/scheduling; cancel task đóng socket. Kết quả ghi `unknown`, không tự khẳng định provider đã dừng hoặc tự phát lại POST. Transport timeout cũng `unknown`. |
| Gateway provider, source | `src/provider.ts` | Provider gọi CLI bằng executable/args, `--ignore-user-config`, `--ignore-rules`, runtime thư mục tạm, model instructions riêng, `project_doc_max_bytes=0`, web search disabled; tắt shell/unified exec/apps/plugins/multi-agent/computer-use; sandbox read-only và approval never. Env whitelist loại API key/proxy tùy biến. Đây là cấu hình phòng vệ trong source, chưa phải bằng chứng CLI đang chạy thực thi đủ mọi cờ. |
| Read boundaries, source | Provider + config + native observer | Provider vẫn truyền HOME và có thể CODEX_HOME; không có OS/container filesystem allowlist thể hiện trong source. Native observer chủ động đọc native SQLite và rollout trong `NATIVE_CODEX_HOME`, mặc định CODEX_HOME hoặc `~/.codex`, rồi giữ metadata/usage. Phạm vi đọc của observer khác phạm vi quyền đọc của model. |
| Tool rejection, source | `assertNoAgentTools` sau `thread.run` | Gateway từ chối kết quả có command/file/MCP/web-search items. Kiểm sau turn không chứng minh tool chưa thực thi; prompt cấm tool cũng không thay permission enforcement. |
| Persistence, source/docs | `server.ts`, `sessions.ts`, `metrics.ts`, `native-usage.ts`, README, TECHNICAL | Stateless app endpoint tạo thread mới nhưng **không bật ephemeral**. Chỉ dashboard `/api/playground/chat` bật ephemeral. Gateway sessions lưu messages/thread ID trong `sessions.json`; xóa session không xóa CLI rollout. Metrics lưu metadata/token/timing/pricing; native collector parse nội dung rollout nhưng chỉ lưu metadata/usage vào DB riêng. |
| Cancellation gateway, source | `server.ts`, `provider.ts`, `index.ts` | Disconnect/timeout/shutdown abort controller; signal đưa vào `spawn`; finally gọi kill child nếu cần. Không thấy API cancel theo app call ID, provider acknowledgement, kill-tree hoặc force-kill escalation trong source. Session đang bận không xóa được (409). |

Nguồn gateway có SDK và CLI package cài tại chỗ phiên bản `0.160.0`. Evidence chứa hash cả source, lockfile, vài file dist và package metadata để đối chiếu. Không build/restart, không chạy binary/SDK hoặc gọi model trong lượt này. **Chưa xác minh process live dùng đúng source/dist/binary/config đã đọc**; hash file trên đĩa không chứng minh loaded process hay child executable identity.

## NOT VERIFIED

1. **Isolation/read enforcement thật:** chưa chứng minh CLI không đọc HOME, CODEX_HOME, thư mục công ty khác, file hệ thống/credential, MCP/integrations hoặc đi mạng ngoài provider được cho phép. Read-only chủ yếu nói về ghi file; không tự chứng minh giới hạn đọc. Chưa có kết quả canary, OS deny logs, process tracing hoặc test trên đúng build đang phục vụ.
2. **Privacy/retention thật:** chưa kiểm effective CODEX_HOME/DATA_DIR, runtime file modes, CLI rollout/log/SQLite/WAL/backups, log service/proxy, và dữ liệu sau crash/restart/deletion. Session TTL mặc định 24 giờ là expiration logic, không là bảo đảm xóa vật lý đúng 24 giờ: init/get có thể chỉ bỏ record khỏi RAM và ghi đĩa ở lần save sau. Gateway metrics/native metadata không có retention tự xóa theo source đã đọc. Retention phía tài khoản ChatGPT/provider, quyền truy cập và điều khoản áp dụng chưa được chứng minh bằng thông tin tài khoản đã được Owner cho phép xem.
3. **Cancellation thật:** source thể hiện yêu cầu abort/đóng socket; chưa chứng minh child/grandchild kết thúc, request upstream dừng tính usage, hoặc hoàn tất trong giới hạn thời gian. Không có hard token/USD cap giữa lượt trong contract hiện tại. Hủy HTTP không hoàn tác dữ liệu đã gửi hoặc usage đã phát sinh.
4. **CG01 provenance:** proof schema hiện tại là operator attestation đơn giản, chưa ràng buộc mạnh với build live, cài đặt CLI, cấu hình effective, OS/container policy hoặc nội dung evidence. Chưa thể ký xác nhận ba capability dựa trên kiểm tra HTTP/source.
5. **Windows:** implementation gate dùng `os.getuid`, `os.O_NOFOLLOW`, POSIX owner/mode 0600; chưa có ACL/trusted-handle tương đương cho Windows. Có thể thiếu API/platform behavior, không chỉ sai mode. File `run.bat` không chứng minh CG01 chạy được an toàn trên Windows. Không chuyển sang file world-readable hoặc bỏ check để giải quyết portability.

## Schema proof và những gì gate thực sự kiểm tra

Nguồn chuẩn hiện tại: [`gates.py`](../../../apps/api/src/agent_corporation_api/modules/execution/gates.py). Không có JSON Schema độc lập hoặc schema version trong implementation hiện tại.

| Trường/điều kiện | Kiểm tra trong code |
| --- | --- |
| Đường dẫn | Worker lấy `runtime_gate_path`, mặc định `.local/cg01-proof.json`; immediate parent không là symlink. File mở O_RDONLY + O_NOFOLLOW + O_NONBLOCK. |
| Metadata file | Regular file, UID bằng process hiện tại, mode chính xác 0600, kích thước ≤ 16384 bytes. |
| Nội dung | Parse JSON thành object. Trường không biết không bị từ chối. |
| `gateway_base_url` | Nếu caller cung cấp base URL: phải bằng base URL sau bỏ slash cuối. Worker hiện có cung cấp. |
| `expires_at` | ISO datetime có timezone và lớn hơn `now` UTC. Không có issued_at, max lifetime hoặc clock rollback defense. |
| `gateway_fingerprint` | Khớp SHA-256 ghép tên file + bytes theo thứ tự `package.json`, `src/server.ts`, `src/schema.ts`, `src/provider.ts`, `src/config.ts`. Snapshot hiện tại `78f0a5ae3caa013fe3f667aee69855f08711380e6da3c98e51d56cce10b80a37`. |
| `evidence_refs` | Chỉ yêu cầu list không rỗng; chưa kiểm kiểu từng phần tử, đường dẫn tồn tại, hash evidence, trạng thái test hay nội dung. |
| `isolation_verified` | Phải đúng boolean `true`. |
| `privacy_retention_verified` | Phải đúng boolean `true`. |
| `cancellation_verified` | Phải đúng boolean `true`. |

Gate không đọc/đánh giá lại evidence. Ba boolean là lời xác nhận của operator; `operator_evidence_verified` là tên reason trong code, không phải independent verifier. Không có chữ ký, issuer, môi trường/phase/test batch scope, binding approved model hay revocation ID trong proof. Grant là lớp riêng.

Fingerprint hiện **không bao gồm** lockfile, SDK/CLI binary, dist đang chạy, index/protocol/sessions/metrics/native observer/catalog, effective env/config, auth state, OS boundaries, retention policy hoặc provider terms. Immediate-parent symlink check không kiểm toàn bộ ancestor chain/owner/mode của directories và không là full TOCTOU-safe directory trust chain. Theo dõi các hạn chế này trong verification; không dùng proof match làm bằng chứng mọi runtime property khớp.

## Quy trình xác minh cụ thể để gỡ phần còn lại

| Bước | Cách làm và bằng chứng cần lưu | Quyền/điều kiện còn thiếu | Tiêu chí đạt |
| --- | --- | --- | --- |
| V01 — Chốt target | Operator ghi endpoint, OS/user/container identity, loaded build/process start, hashes source/dist/lockfile/CLI, effective **cấu hình không bí mật**, auth mode, mounted paths và network policy. Credential chỉ được provision nội bộ, không đưa report. | Owner phê duyệt isolated qualification environment và thay đổi gateway cần thiết; shared gateway không sửa/restart trong task này. | Có chain từ evidence → đúng binary/config/instance được kiểm; thay build/config/boundaries phải tái xác minh. |
| V02 — Isolation không model | Tạo instance/transport fixture riêng trong allocation đã reserve, fake HOME/CODEX_HOME/DATA_DIR, fake credential không dùng được, canary trong scope và ngoài scope. Stub CLI ghi args/env names/redacted env, thử đọc/ghi/đi mạng theo allowlist và thu OS denial/process evidence; không nhận nội dung nhạy cảm host. Kiểm caller không override đường dẫn/tool policy và không kế thừa rules/MCP/plugins. | Explicit isolated process/filesystem/ports execution; có thể cần OS/container sandbox và credentials riêng ở bước sau. | Fixture chứng minh wiring/OS boundaries theo threat model; **không đạt production model gate bằng mock**. |
| V03 — Read boundary với provider thật | Chỉ sau phương án qualification riêng được Owner phê duyệt: bounded canary prompts yêu cầu đọc ngoài scope/tool injection bằng chuỗi giả; đối chiếu OS access/egress audit, CLI events và canary. Không đưa secret hoặc private repo thật vào canary. Kiểm model khác nhau nếu capability khác nhau. | Owner authorization riêng nêu target isolated gateway, test cases, model/effort, tối đa requests tính cả retry, concurrency, timeout, expiry và usage/cost uncertainty. Chưa được cấp. | Không có truy cập ngoài allowlist/tool thực thi; negative evidence độc lập với lời model tự khai. Có giới hạn residual risk, không tuyên bố tuyệt đối từ một prompt. |
| V04 — Persistence/privacy | Trên isolated fake-data target, chụp **metadata/hashes không nội dung bí mật** trước/sau success/cancel/failure/restart/TTL/delete; kiểm sessions/rollouts/logs/SQLite/WAL/temp/backups, UID/mode/ACL và access tests; định nghĩa retention/deletion schedule và trace retention cần thiết. Xác minh provider/account policy từ nguồn chính thức/current settings khi được phép. | Owner chọn retention, chấp thuận provider data handling và boundary được yêu cầu; cho phép isolated storage/clock/restart/delete trên fixture riêng. Không xóa dữ liệu gateway shared. | Data inventory nêu chính xác ai thấy gì, ở đâu, bao lâu, xóa thế nào; deletion chứng minh đúng storage được tuyên bố; không hứa CLI/session DELETE xóa upstream. |
| V05 — Cancel không model | Stub transport/CLI riêng: disconnect client, timeout, stop, expiry, child hung/grandchild, process shutdown/crash, late result. Đo abort timing/process exits/socket closure; app call terminal unknown và reservation/ledger không replay. | Isolated execution fixture/DB riêng nếu cần; không model/grant. | Wiring cancel/stop đúng, không duplicate hoặc mất trace; kết quả vẫn không chứng minh upstream cancel. |
| V06 — Cancel provider thật | Trên isolated target và scope đã được cấp riêng, cancel in-flight bằng disconnect/timeout, quan sát child process/upstream evidence nếu có, reconcile call/usage muộn; ghi giới hạn không thể xác nhận upstream và budget vẫn giữ uncertainty. Không cố hủy request của người khác. | Authorization qualification inference riêng như V03, shared process untouched. Không có cách hợp lệ chạy bước này qua worker khi gate chưa đạt. | Operator xác nhận cancellation behavior thực đo và limitations đúng yêu cầu CG01; nếu không đủ thì giữ blocked hoặc thiết kế cancel capability mạnh hơn. |
| V07 — Proof issuance | Sau khi V01–V06 đủ bằng chứng thật và Owner chấp thuận residual risk: operator ghi proof đúng endpoint/fingerprint, refs immutable, expiry hữu hạn, owner/mode 0600; kiểm toàn chain/trust boundary; negative checks expired/hash mismatch/permission/symlink chỉ trong đường dẫn fixture riêng. | Chưa được phép tạo proof trong task này. Cần operator issuance dựa trên evidence thật; nếu platform/hardening cần code change thì scope riêng. | `check_gate` hợp lệ cho đúng runtime; evidence đầy đủ, chưa hết hạn. Inference vẫn cần grant đúng phase/batch riêng và budget/Emergency Stop. |

### Tránh vòng lặp cấp quyền cancellation

CG01 yêu cầu cancellation verified trong khi worker cấm inference trước CG01. Không tạo proof tạm/giả, không thêm bypass và không cấp grant app để thử qua gate. Giai đoạn fixture không model xác minh wiring trước. Nếu vẫn cần provider thật để hoàn tất CG01, Owner phải phê duyệt **quy trình gateway qualification riêng trên instance cô lập**, độc lập với app worker/grant; chốt accounting, model/test cases và giới hạn trước khi chạy. Kết quả qualification được operator xem xét để có thể cấp proof sau này. Đây là đề xuất authorization chưa được cấp, không phải quyền thực thi hiện có. Mock chỉ tạo evidence về fixture, không thay production isolation/privacy/cancellation.

## BLOCKED và việc cần Owner quyết định

- CG01 vẫn blocked do chưa có proof/evidence đủ cho ba capability. Probe HTTP không giải quyết các capability này.
- Cần chọn giữa giữ gateway shared bị chặn hoặc phê duyệt target cô lập với HOME/CODEX_HOME/DATA_DIR, OS read/network boundaries, retention và policy đã xác định. Không tự sửa/nới quyền gateway shared.
- Cần scope/authorization riêng cho qualification model thực, gồm giới hạn request/expiry và chấp nhận khả năng usage/cost/cancellation upstream chưa xác định. Task này cấm inference và grant; chưa thực thi bước đó.
- Nếu Windows nằm trong mục tiêu V1, cần thiết kế gate ACL/trust tương đương và kiểm trên Windows trước khi cho inference. Chưa xác minh portability.

Báo cáo này không đổi trạng thái phase, không nghiệm thu phase, không chấp nhận rủi ro thay Owner và không cấp quyền Employee Chat gửi model. Quyết định mở CG01 phải dựa trên evidence thực; thiết kế Employee Chat có thể tiến hành trong lúc runtime còn chặn.
