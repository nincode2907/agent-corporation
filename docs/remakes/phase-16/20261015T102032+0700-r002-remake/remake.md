# Remake Phase 16 — 20261015T102032+0700-r002-remake

- Trạng thái xử lý: changed
- Report nguồn: [Phase 16 r002](../../../tests/results/phase-16/20261015T101533+0700-r002-test/report.md)
- Findings xử lý: P16-03 malformed call ref `../bad` được từ chối trước khi tạo settlement; `BudgetReservation.call_ref` dùng opaque-ref pattern và state transitions xây model đã validate, không dùng unchecked update.
- Boundary regressions: existing validation for real int revision/amount, dispatched-release deny, unresolved state và reservation limit được giữ.
- Test hiện tại: `rtk proxy uv run --project apps/api pytest apps/api/tests/test_phase16_finance_contracts.py apps/api/tests/test_phase17_quality_contracts.py apps/api/tests/test_phase15_memory_contracts.py` → 24 passed. Independent r003 pending.
- Chưa giải quyết trong pure contract: persistent atomic reserve/settle/release, source late-usage reconciliation, finance drilldown/dashboard và IG16 runtime; grant = 0.
