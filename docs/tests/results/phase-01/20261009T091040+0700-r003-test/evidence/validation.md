# Kiểm tra hồ sơ batch r003

- Lệnh: `rtk proxy python3 docs/tests/scripts/validate.py --batch docs/tests/results/phase-01/20261009T091040+0700-r003-test` — PASS; 24 checklist, 171 test riêng, C01–C08, AC/source refs/hash, IG/R, local links và HTML; report r003 có đủ 15 cases/tag/result/evidence links.
- Validator xác nhận cấu trúc tài liệu và liên kết, không đánh giá nội dung evidence hoặc nghiệm thu thay Chủ tịch.
- `rtk proxy git diff --check`: PASS.
- Không thay source sản phẩm hoặc trạng thái master plan.
