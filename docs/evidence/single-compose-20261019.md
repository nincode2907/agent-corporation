# Runtime một file Compose — 19/10/2026

## Thay đổi

Theo yêu cầu Chủ tịch, startup chỉ còn `docker compose up --build` trong thư mục gốc; những lần sau `docker compose up`. Không cần `.env`, runtime Python/Node trên host, `run.sh`, `run.bat` hay Compose bootstrap riêng. Gateway local vẫn chạy ngoài stack tại endpoint cũ; không sửa server chung.

`compose.yml` điều phối bootstrap → PostgreSQL → migration → API → Nginx. Bootstrap networkless đọc checkout chỉ đọc, tạo credential một lần trong volume hoặc nhập credential/Owner cũ. API chỉ nhận app config/Owner; admin DB config nằm ở volume riêng cho PostgreSQL/migration. Cấu hình DB khác persisted state bị từ chối. Đã xóa wrapper và file Compose bootstrap cũ.

## Kiểm chứng

| Kiểm tra | Tag | Bằng chứng/kết quả |
|---|---|---|
| Compose parse không `.env` | `clean` | `docker compose --env-file /dev/null config --quiet` exit0 |
| Regression native | `clean` | 8 module: compose initializer, Docker gateway, CG01 demo mode, codex gateway, Phase06 runtime, Playground, Owner auth, health: **103 passed, 1 skipped** |
| Regression trong Linux image | `clean` | Cùng suite: **103 passed, 1 skipped**; network none, DB giả; skip dành cho Windows |
| Kiểm tra độc lập | `clean` | AI test khác: **17 passed**, kiểm source/config và phân tách credential; [report r001](../tests/results/docker/20261019-single-compose-r001/report.md) |
| Stack mới không `.env` | `clean` | `rtk proxy python3 scripts/test_docker_isolated.py` exit0; bootstrap sinh config, PostgreSQL mới, migration, API, Nginx đều khởi động |
| Chạy Compose lần hai | `clean` | Runner so sánh fingerprint nội bộ Owner/app config trước/sau: giữ nguyên; không in secret/hash |
| Session và proxy | `clean` | Runner: Owner login/session, Host/Origin/CSRF, SSE first frame <5s; restart giữ session/DB, logout thu hồi; recreate API vẫn qua Nginx |
| DB mất kết nối | `clean` | Chỉ trên stack tạm: liveness200, readiness503 |
| Dữ liệu runtime trước/sau | `clean` | Backup `.local/backups/before-single-compose-20261019.dump` mode0600; 32 bảng không đổi count, Alembic head `20261014_0009`; giữ volume `agent-corporation_agent_corporation_postgres` |
| Runtime đang chạy | `clean` | `docker compose up` attached terminal; bootstrap/migrate exit0, PostgreSQL/API/web healthy; loopback ports15510/15501/15500 giữ nguyên |
| Runtime config/Owner | `clean` | Exec API: UID1000, secret0600, Owner hợp lệ, `get_settings()` đọc config; không mount admin volume và app config không có migration URL |
| HTTP thực tế | `clean` | Trang gốc và `/api/v1/health/ready` qua `127.0.0.1:15500` và `agent-corporation.localhost`:200; API direct readiness200 |
| Kết nối gateway cũ | `clean` | GET `/api/v1/codex/probe`: available, health/catalog ok, 7 model, entitlement_verified=false; không inference |

Root thực hiện regression/isolated stack và chuyển runtime; AI độc lập chỉ xác minh phạm vi ghi trong r001. Stack tạm đã xóa đúng project/volumes riêng. Runtime không xóa volume; chỉ xóa container `secrets-init` cũ đã dừng. Trước chuyển đổi, model call dispatched và Playground queued/dispatched đều0.

## Giới hạn

Không gọi inference, tạo grant hoặc nghiệm thu phase. Giữ nguyên các trạng thái trong master plan và các gate/giới hạn hiện có. Docker Desktop Windows chưa được kiểm trên phần cứng Windows. Gateway/catalog không chứng minh entitlement hay CG01 production. Backup/secret local không đưa vào Git.
