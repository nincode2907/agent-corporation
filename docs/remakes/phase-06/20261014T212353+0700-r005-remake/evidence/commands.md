# Commands — remake r005

Từ root repo, không inference hoặc DB write.

1. `rtk proxy uv run --project apps/api --no-sync python scripts/cg01_mode.py release-check`: trước sửa console Windows không in được diagnostic tiếng Việt, báo generic config error; exit nonzero. Với `python -X utf8` cho đúng BLOCKED, xác định lỗi encoding.
2. Sửa main() reconfigure stdout/stderr UTF-8; thêm subprocess fixture không đọc real env.
3. `rtk proxy uv run --project apps/api --no-sync pytest apps/api/tests/test_cg01_demo_mode.py -q`: exit 0; 17 passed, 1 upstream FastAPI/httpx deprecation warning.
4. `rtk proxy uv run --project apps/api --no-sync python scripts/cg01_mode.py release-check`: exit 1 (expected); output `CG01 release: BLOCKED · Ngoại lệ demo còn bật. Chuyển strict và dừng/restart worker trước Phase 23.` Không gọi model hoặc xuất secret.

Kiểm trước remake: focused runtime/gateway suites 48 passed/8 POSIX skipped; web build/lint pass. Document renderer UTF-8 pass. Full phase00 validator chưa đạt vì external gateway README `../../codex-server/README.md` không có ở checkout Windows; không tạo file giả để PASS.
