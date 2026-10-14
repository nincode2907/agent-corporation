# C06 / C08 — Validation r005

rtk proxy python3 scripts/render_plan.py: exit0,24 phase,1 hoàn tất.

rtk proxy python3 docs/tests/scripts/validate.py --batch docs/tests/results/phase-05/20261014T150201+0700-r005-test: exit0.

```text
PASS cấu trúc:24 checklist,171 test riêng,C01–C08,AC/source refs/hash,IG/R và local links.
PASS HTML:deterministic/đồng bộ,đủ phase,lang=vi/favicon,IDs/links.
PASS report phase-05/20261014T150201+0700-r005-test/report.md:15 cases có fields/tag/result/evidence links.
LIMIT:validator chỉ kiểm cấu trúc/links,không đánh giá nội dung evidence hoặc nghiệm thu.
```

Một lần tạo report bị lỗi escape trong script tổng hợp nên file chưa ghi; đã sửa harness, không thay kết quả test sản phẩm. Report cuối giữ14clean/pass,1need-change/blockedCG01.
