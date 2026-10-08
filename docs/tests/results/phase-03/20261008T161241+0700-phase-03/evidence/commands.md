# Lệnh và kết quả đã chạy

Shell qua `/Users/buivannin/.local/bin/rtk proxy`.

- `curl --fail --silent --show-error http://127.0.0.1:15501/api/v1/health/ready` — exit 0; `{"status":"ok","checks":{"database":"ok"}}`.
- `npm run --prefix apps/web build` — exit 0; `tsc -b` và Vite build thành công.
- `uv run --project apps/api pytest apps/api/tests/test_phase03_persistence.py -q` — exit 0; `5 passed in 1.38s`.
- `uv run --project apps/api alembic -c apps/api/alembic.ini current` — exit 0; current `20261008_0003 (head)`; read-only.
- Sau khi tạo report: `python3 docs/tests/scripts/validate.py --batch docs/tests/results/phase-03/20261008T161241+0700-phase-03` — exit 0; PASS cấu trúc 24 checklist/171 test, HTML đồng bộ; report batch có đủ 15/17 cases, tags/results/evidence links.

Không chạy API full suite, không chạy migration upgrade/downgrade, không restart service, không inference.

- `python3 docs/tests/scripts/validate.py` (toàn repo) — exit 1 ở report Phase 04 hiện có: `Report verdict sai: **chưa đủ bằng chứng**`; validator đòi giá trị thuần. Không chỉnh report ngoài phase được giao. Validation từng batch Phase 02/03 vẫn PASS.
