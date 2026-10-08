# Kết quả kiểm tra bộ tài liệu

- `rtk proxy python3 docs/tests/scripts/render.py` — exit 0; đồng bộ `index.html` từ Markdown.
- `rtk proxy python3 docs/tests/scripts/validate.py --batch docs/tests/results/phase-01/20261008T154512+0700-phase01` — PASS: 24 checklist, 171 test, C01–C08, AC/source refs/hash, IG/R, HTML consistency; báo cáo Phase 01 đủ 15 cases và evidence links.
- `rtk proxy python3 evidence/check_reports.py` — PASS: parser chấp nhận fixture hợp lệ; từ chối 8 lỗi gồm clean/not-run, thiếu case, loại case bắt buộc, link hỏng, thống kê sai, tag lặp, thiếu gate và PASS khi test chưa chạy.
- `rtk proxy git diff --check -- AGENTS.md README.md docs/tests` — exit 0.
- Không chạy test sản phẩm, DB hay inference để kiểm bộ tài liệu.
