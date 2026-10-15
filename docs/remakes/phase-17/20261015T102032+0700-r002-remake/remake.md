# Remake Phase 17 — 20261015T102032+0700-r002-remake

- Trạng thái xử lý: changed
- Report nguồn: [Phase 17 r002](../../../tests/results/phase-17/20261015T101533+0700-r002-test/report.md)
- Findings xử lý: P17-02 refuses duplicate sample/evidence refs in a candidate and across tournament profiles; repeated rows cannot inflate n or uncertainty. Required sample/evidence refs are unique within the tournament batch.
- Test hiện tại: `rtk proxy uv run --project apps/api pytest apps/api/tests/test_phase16_finance_contracts.py apps/api/tests/test_phase17_quality_contracts.py apps/api/tests/test_phase15_memory_contracts.py` → 24 passed. Independent r003 pending.
- Chưa giải quyết trong scope thuần: real benchmark harness/artifact isolation, KPI time-window/cost/rework query, CI regression, dashboard/Owner approval persistence và tournament inference; grant = 0.
