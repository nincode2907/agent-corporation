# Commands — Phase 03 remake r001

| Lệnh | Exit | Kết quả |
| --- | ---: | --- |
| `rtk proxy uv run --project apps/api pytest apps/api/tests/test_phase03_persistence.py -q` | 0 | `8 passed in 1.59s`; PostgreSQL fixture tạo và dọn UUID-owned test environments. |
| `rtk proxy sed -n '1,360p' apps/api/tests/test_phase03_persistence.py` | 0 | Đọc lại test source và assertions mới; chỉ đọc. |
| `rtk proxy npm run --prefix apps/web build` | 0 | Phase 02 regression: TypeScript/Vite build pass. |
| `rtk proxy npm run --prefix apps/web lint` | 0 | Phase 02 regression: Oxlint pass. |
| `rtk proxy python3 scripts/render_plan.py` | 0 | Roadmap HTML sinh lại từ Markdown. |
| `rtk proxy python3 docs/tests/scripts/validate.py` | 0 | 24 checklist/171 test; HTML deterministic/đồng bộ; existing reports pass structural validation. |
| `rtk proxy python3 -m compileall -q apps/api/src apps/api/tests` | 0 | Python syntax/bytecode compilation pass. |

Không restart/stop database hoặc API dùng chung, không chạy migration trên shared DB, không inference.
