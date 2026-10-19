# Evidence Phase 17 — Benchmark and quality contracts

Ngày: 15/10/2026 (Asia/Ho_Chi_Minh)

## Đã triển khai

- `apps/api/src/agent_corporation_api/modules/quality/contracts.py`: manifest versioned cho suite/dataset/evaluator/constraints; deterministic evaluator so hash output fixture và lưu evidence ref; không dựa riêng vào LLM judge.
- Candidate summary ghi sample size, denominator, success/unknown counts, first-pass rate, latency P50/P95, intervention rate và Wilson 95% interval. Candidate mismatch suite/constraints bị từ chối. Tournament chỉ đề xuất winner nếu mỗi profile đủ minimum sample và interval leader tách khỏi runner-up; result yêu cầu Owner approval và khai báo không mutation config.
- Focused fixture tests cùng Phase 15 memory và Phase 16 finance sau hai vòng remake: `rtk proxy uv run --project apps/api pytest apps/api/tests/test_phase16_finance_contracts.py apps/api/tests/test_phase17_quality_contracts.py apps/api/tests/test_phase15_memory_contracts.py` → **24 passed**.
- Independent r001 bắt được required case omission, winner dựa trên caller-forged summary và Phase17 history mâu thuẫn giữa Markdown/HTML; r002 xác nhận đã sửa nhưng tìm thấy repeated sample/evidence refs thổi phồng cỡ mẫu. Remake r002 từ chối refs trùng; independent r003 xác nhận các local boundaries và Markdown/HTML consistency pass. Xem [r001](../tests/results/phase-17/20261015T100829+0700-r001-test/report.md), [r002](../tests/results/phase-17/20261015T101533+0700-r002-test/report.md), [r003](../tests/results/phase-17/20261015T102032+0700-r003-test/report.md) và [remake r002](../remakes/phase-17/20261015T102032+0700-r002-remake/remake.md).

## Ranh giới và blockers

Chưa có harness chạy benchmark profile, isolated dataset/artifact/call/finance namespace, regression comparison/CI, failure artifact drilldown, UI dashboard, Owner config approval flow hoặc tournament inference. Không có grant riêng nên không chạy model; Phase 16/IG16 cũng chưa nghiệm thu. Các fixture chứng minh pure contracts, không phải benchmark thực nghiệm. Technical phase conclusion: chưa đủ bằng chứng.
