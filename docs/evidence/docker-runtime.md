# Docker runtime — 15/10/2026

## Phạm vi và quyền

Chủ tịch duyệt phương án đưa Agent Corporation vào Docker và yêu cầu triển khai ngày 15/10/2026. Đây là thay đổi runtime/deployment; không nghiệm thu hoặc mở phase mới. Gateway Codex vẫn chạy trên host, không sửa/restart/cấp grant hoặc gọi inference.

## Thay đổi

- Compose quản lý web Nginx, FastAPI, Playground worker trong API, PostgreSQL, migration và secret-init. Work Order worker là profile/lệnh tường minh; không bật trong deployment.
- Python 3.14.8, Node 24.21.0, Nginx và PostgreSQL dùng image digest; Python/npm dependency giữ lockfile. Build context loại `.env`, `.local`, dữ liệu và native dependencies.
- API/worker UID1000, readonly root filesystem, drop capabilities; migration credential chỉ trong migrate. Owner secret và CG01 metadata được copy giữ nội dung vào runtime volume, mode0600, mount read-only; năm source files gateway chỉ đọc để fingerprint.
- Gateway transport opt-in `docker-host` chỉ nhận `http://host.docker.internal:15600`, giữ HTTP Host `127.0.0.1:15600`; GET không dùng proxy/redirect. Strict CG01 proof phải khớp endpoint và transport, không tái dùng proof native. Operator model/grant/Stop/CSRF giữ nguyên.
- `run.sh`/`run.bat` bootstrap bằng Docker, build, chờ health và hiện logs; POSIX launcher truyền UID/GID người chạy để host files không thành root-owned trên Linux.

## Kiểm tra đã thực hiện

| Kiểm tra | Kết quả / giới hạn |
| --- | --- |
| Build API + web + API test image | PASS, lockfiles và image digests; frontend production bundle build thành công |
| Focused gateway/runtime/CG01/Owner/health fixtures | 99 passed, 1 Windows-only skipped; chạy cả native và Linux test image với `--network none`; không inference |
| Compose configuration / shell syntax | `docker compose config --quiet`, bootstrap config và `bash -n run.sh` PASS trên Compose2.15.1 |
| Stack cô lập | PostgreSQL/volumes/project riêng, không host ports, credential giả; fresh migration/secret-init/API/web PASS |
| Owner và proxy | UID1000/secret600, login/session, Host/Origin/CSRF deny, SSE first frame <5s qua Nginx PASS trên stack cô lập |
| Restart | Cookie Owner + secret + DB giữ qua API restart; logout hợp lệ thu hồi session PASS trên stack cô lập |
| Database-down | Chỉ dừng PG test riêng: liveness200/readiness503 PASS, cleanup project/volumes tạm |
| Container recreate / DNS | PASS trên stack cô lập: force-recreate API, Nginx resolver127.0.0.11 khôi phục proxy đến service hiện tại |
| Runtime thật | API/web/PG healthy; direct15500, API15501 readiness, hostname proxy trả200; IPv4 loopback publications giữ nguyên |
| Gateway thật | GET health/catalog qua API Docker: available, 7 model, entitlement_verified=false; không POST model |
| Browser | Chrome mở `http://agent-corporation.localhost/`, title Tổng quan, demo overview và health hoạt động; langvi/favicon có trong HTML |
| Dữ liệu trước/sau | Backup `.local/backups/before-docker-20261015.dump` mode0600; đối chiếu 28 bảng đã có: không đổi count. PG container/volume cũ giữ nguyên. Migration head từ0007 lên20261014_0009 |
| Không dispatch | Runtime `model_calls=0`, Playground turns=0, không tạo inference grant hoặc real company |
| CG01 | Runtime strict, missing_or_invalid_proof, verified=false; Docker deployment không nâng gate |

## Bằng chứng và vận hành

- [Independent r001](../tests/results/docker/20261015-docker-r001/report.md), [remake r001](../remakes/docker/20261015-docker-r001/remake.md), [independent r002](../tests/results/docker/20261015-docker-r002/report.md). Hai finding release-check transport/host UID được independent retest xác nhận đã sửa; không còn finding nguồn bắt buộc trong scope Docker Mac hiện tại.
- Giữ volume `agent-corporation_agent_corporation_postgres`. Không dùng `down --volumes` cho runtime. Backup có dữ liệu riêng, Git-ignore, không đưa vào evidence tracked.
- Registry Dev Hub chỉ cập nhật tên container web/API, giữ port/hostname/proxy chung. Gateway bind/config/process không thay đổi.
- Chưa kiểm định phần cứng Docker Desktop Windows hoặc remote Linux host networking. Docker Mac hiện tại đã kiểm định. Gateway connectivity không phải model entitlement hoặc live inference acceptance.
