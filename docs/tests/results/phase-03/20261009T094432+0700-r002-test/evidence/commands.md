# Commands — Phase 03 r002

| Lệnh/thao tác | Exit/kết quả | Quan sát |
| --- | ---: | --- |
| `rtk proxy uv run --project apps/api pytest apps/api/tests/test_phase03_persistence.py -q` | 0 | 8 passed in 1.60s trên PostgreSQL local; fixtures dùng UUID riêng và cleanup theo fixture. |
| PostgreSQL 18.6 disposable mới; Alembic `upgrade head` rồi `current` | 0 | Upgrade sạch từ DB rỗng; current `20261008_0003 (head)`. |
| Cùng target pytest với DSN đã redact trỏ tới disposable DB/app role | 0 | 8 passed in 1.59s trên DB sạch đã migrate. |
| Fixture restart biệt lập: gọi `create_work_order` internal command qua app role; tạo run/state/checkpoint bằng migration role; `append_event` qua app role; start Uvicorn loopback port 50327; GET `/api/v1/health/ready`; stop và start lại process; GET ready; query lại bằng app role | 0 | Ready trả `{"status":"ok","checks":{"database":"ok"}}` trước/sau. Sau restart counts vẫn `tasks=1, runs=1, checkpoints=1, events=2`; ID và giới hạn fixture tại [restart observation](P03-08-restart-observation.md). |
| Dừng Uvicorn test và disposable PostgreSQL containers | 0 | Cả hai test process được dừng; `docker ps` sau đó chỉ còn containers hiện hữu, không còn test container. DB/API dùng chung không dừng/restart. |
| `rtk proxy python3 scripts/render_plan.py` | 0 | HTML đồng bộ từ Markdown, 24 phases, 1 phase hoàn tất; Phase03 vẫn Chờ nghiệm thu. |
| `rtk proxy python3 docs/tests/scripts/validate.py` | 0 | Cấu trúc checklist 24/171; HTML; Phase03 r002 17 cases and all reports validated. |
| `rtk proxy npm run --prefix apps/web build` / `lint` | 0/0 | Regression UI build/lint pass. |

DSN/passwords đã được redact trước lưu; chỉ dùng password giả trong container disposable. Không đọc/in `.env`; không gọi codex-server/model; inference grant = 0. Container host binding ngẫu nhiên loopback-only, dữ liệu nằm trong container writable layer và biến mất khi container dừng (`--rm`); không để lại volume.
