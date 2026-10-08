# Lệnh và kết quả — Phase 04

Tất cả shell commands chạy từ root repo với `/Users/buivannin/.local/bin/rtk proxy`.

| Lệnh | Kết quả quan sát |
| --- | --- |
| `uv run --project apps/api alembic -c apps/api/alembic.ini upgrade head` | Exit 0; migration 20261008_0002 → 20261008_0003 |
| `uv run --project apps/api alembic -c apps/api/alembic.ini current` | Exit 0; `20261008_0003 (head)` |
| `uv run --project apps/api python scripts/seed_demo.py --seed` | Exit 0 sau khi script tự nạp package path; trả fixture v1, 2 departments, 3 employees, 5 tasks, 20 events; không inference |
| `uv run --project apps/api pytest apps/api/tests -q` | Exit 0; `10 passed` (3 health, 5 Phase 03 integration, 2 Phase 04); một Starlette `TestClient`/httpx deprecation warning |
| `npm run lint` trong `apps/web` | Exit 0; `oxlint` |
| `npm run build` trong `apps/web` | Exit 0; TypeScript + Vite production build |
| GET `http://127.0.0.1:15501/api/v1/health/ready` | HTTP 200; `database=ok` |
| GET `http://127.0.0.1:15501/api/v1/demo/dashboard` | HTTP 200; scope kind=demo, usage unknown, inference requests=0 |
| GET `http://agent-corporation.localhost/api/v1/health/ready` | HTTP 200 qua proxy local IPv4 |
| POST `/api/v1/demo/reset` `{confirmed:true}` lặp 2 lần qua HTTP local | `200,200`; manifest `03e1126c…` giống nhau |
| Browser DOM kiểm tra overview, approval, finance và reset prompt | Pass các assertion nêu ở `ui-assertions.md`; screenshot không được lưu thành artifact |
| `python3 docs/tests/scripts/validate.py` trước report | Exit 0; 24 checklist, 171 case definitions, C01–C08/source refs/HTML consistent; report phase chưa được thêm ở thời điểm đó |
| `python3 scripts/render_phase00.py` | Exit 0; Product Spec/ADR HTML regenerated từ Markdown |
| `python3 scripts/render_plan.py` | Exit 0; 24 phase, 4 phase hoàn tất; Phase 04 chờ nghiệm thu |
| `python3 docs/tests/scripts/render.py` | Exit 0; `docs/tests/index.html` regenerated từ Markdown |
| `python3 docs/tests/scripts/validate.py --batch docs/tests/results/phase-04/20261008T154151+0700-demo-factory` | Exit 0; 24 checklists, 171 test definitions, C01–C08, AC/hash/refs, HTML, 15 report cases/links hợp lệ |
| Targeted `check_report()` trên report Phase 04 | Exit 0; đủ 15 ID/case, fields/tags/results/evidence links hợp lệ |
| Rerun full bundle validator lúc chốt | Blocked bởi report Phase 01 `20261008T154512+0700-phase01` mới có trong worktree: link tới `evidence/finding-c02.md` không tồn tại. Không sửa file ngoài scope Phase 04. |
| `git diff --check` | Exit 0; không có whitespace errors |

## Negative cases

- `POST /api/v1/demo/reset` với `{"confirmed":false}` qua FastAPI TestClient: HTTP 400.
- `POST` có `environment_id`/`company_id` tự chọn: HTTP 422 (Pydantic `extra=forbid`).
- Canary benchmark và synthetic-real artifact metadata/hash/storage key giữ nguyên sau hai reset. Mỗi environment/company/task/artifact canary được xóa theo ID trong teardown test.
- Tất cả fixture tasks có `max_model_requests=0`; unit/integration tests và GET/reset route không gọi codex-server/model.
