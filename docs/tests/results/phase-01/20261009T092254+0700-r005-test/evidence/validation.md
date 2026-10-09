# Xác thực report r005

Chạy từ repository root:

```text
rtk proxy python3 docs/tests/scripts/validate.py --batch docs/tests/results/phase-01/20261009T092254+0700-r005-test
```

Kết quả:

```text
PASS cấu trúc: 24 checklist, 171 test riêng, C01–C08, AC/source refs/hash, IG/R và local links.
PASS HTML: deterministic/đồng bộ, đủ phase, lang=vi/favicon, IDs/links.
PASS report phase-01/20261009T092254+0700-r005-test/report.md: 15 cases có fields/tag/result/evidence links.
LIMIT: 1 report phase, 0 report bộ tài liệu được kiểm cấu trúc; chưa chạy test sản phẩm/inference, chưa đánh giá nội dung evidence hoặc nghiệm thu.
```

Validator xác nhận định dạng, IDs, hash/refs và local links; không thay thế kết quả runtime trong [commands](commands.md), [routes](routes.md), [browser](browser.md), hoặc quyết định nghiệm thu của Chủ tịch.
