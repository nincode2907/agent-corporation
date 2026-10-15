# Lệnh và quan sát r005

Tester: `/root/cg01_demo_review`, độc lập với `/root` triển khai. Tất cả chạy từ root Windows checkout; chỉ fixture local, không inference/DB/shared gateway/.env.

1. `rtk proxy uv run --project apps/api --no-sync pytest apps/api/tests/test_cg01_demo_mode.py apps/api/tests/test_phase06_runtime.py apps/api/tests/test_codex_gateway.py -q`
   - Exit 0: **48 passed, 8 skipped**, 1 Starlette/httpx deprecation warning, 1.69s.
   - 8 skip là strict POSIX proof/file-owner fixtures; Windows strict unsupported-platform deny có test riêng pass. Không coi skip là proof đạt.
2. `rtk proxy npm run --prefix apps/web build`
   - Exit 0: TypeScript + Vite v8.3.3; 19 modules; build đạt. Không thay browser/Owner runtime QA.
3. `rtk proxy uv run --project apps/api --no-sync python -X utf8 docs/tests/results/phase-06/20261014T211528+0700-r005-test/evidence/P06-12-fixture.py`
   - Final exit 0: CSRF/Origin/Host/cross-site negative 6, GrantInput negative 6, happy paths 2 PASS; policy SQL JSON và checkpoint `cg01_at_creation` PASS; demo worker tới đúng một fake executor PASS. Không gọi transport, không DB.
   - Chuẩn bị fixture có hai lỗi harness đã sửa trước final: import source thiếu sys.path; worker config fixture thiếu `codex_server_api_key`. Đây không phải lỗi implementation. Final script được lưu để tái chạy.
4. `rtk proxy uv run --project apps/api --no-sync python -X utf8 -c "import platform,pytest,fastapi; print('Python',platform.python_version(),'platform',platform.system(),'pytest',pytest.__version__,'FastAPI',fastapi.__version__)"`
   - Exit 0: Python 3.14.3, Windows, pytest 9.0.2, FastAPI 0.142.4.
5. `rtk git rev-parse HEAD` và `rtk git status --short`, `rtk proxy git diff -- apps/api/src apps/web/src/RuntimePanel.tsx README.md docs/product-spec.md docs/master-plan.md .env.example`
   - HEAD `3cb08c1259cd52ce7094313159e3b53fb2880481`, dirty files được hash trong manifest. Source review strict/default/loopback/API/worker/Owner/CSRF/grant/stop/tools-off/UI/docs.

Thông tin parent, không tính là test độc lập: npm lint đạt; render_phase00 đạt; validate_phase00 dưới UTF8 bị chặn bởi link `../../codex-server/README.md` vì sibling checkout chưa tồn tại. HTTP web15500/API15501 live200; gateway15600 health unavailable. Tester không xác minh lại runtime hay gọi authenticated status.

Không chạy release-check CLI trên real settings vì rule cấm đọc .env; pytest gọi `release_check` bằng settings fixture: override bật bị từ chối; strict thiếu proof bị từ chối. Không chứng minh proof strict hợp lệ trên POSIX trong batch Windows này.

6. `rtk proxy python -X utf8 scripts/render_plan.py`
   - Final exit 0: đồng bộ24phases/1hoàn tất. Report đã dùng canonical case blocks, các test bổ sung đánh số P06-09…P06-16 phù hợp parser hiện tại và checklist parent cập nhật. Lần chuẩn bị report dạng bảng chưa parse được đã chuyển trước chốt; không sửa renderer.
7. `rtk proxy python -X utf8 -c "import sys; sys.path.insert(0,'scripts'); import render_plan; r=render_plan.phase_test_report('06'); assert len(r['cases'])==24; assert r['round']=='r005'; print('Roadmap parser PASS',len(r['cases']),'cases;',r['round'],r['verdict'])"`
   - Exit0: parser24cases/r005/chưa đủ bằng chứng. Kiểm report riêng:24uniqueIDs,13clean/pass+11need-change/blocked, evidence relative links tồn tại; manifest sha256 refreshed tại thời gian thực.

Runtime web/API200 là process khởi động trước source task theo identity parent, không chứng minh code mới chạy. Parent có thể ghi attachment activation sau batch; không trộn local flag hoặc post-restart status vào kết quả fixture của tester.
