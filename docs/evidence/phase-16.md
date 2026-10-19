# Evidence Phase 16 — Finance and budget contracts

Ngày: 15/10/2026 (Asia/Ho_Chi_Minh)

## Đã triển khai

- `apps/api/src/agent_corporation_api/modules/finance/contracts.py`: source-versioned cumulative usage snapshot selection; pricing snapshot có version/effective time; cost fact giữ basis, currency, certainty, source và pricing ref riêng; unknown không nhận số tiền kể cả 0; finance ledger entry gắn environment/company/employee/task/model/call và thời gian.
- Chat call được tách khỏi accepted-task cohort. Aggregate period dùng `occurred_at`; aggregate accepted-task lifetime nhận cohort attribution rõ ràng, phát hiện duplicate call, và không cộng chung currency/basis khác nhau hoặc coi unknown là zero.
- Reservation transition có expected revision, terminal-state guard và unresolved state không settle như zero. Đây là pure contract; chưa có transaction/CAS database hoặc race proof.
- Focused fixture tests cùng Phase 15 memory regression sau hai vòng remake: `rtk proxy uv run --project apps/api pytest apps/api/tests/test_phase16_finance_contracts.py apps/api/tests/test_phase17_quality_contracts.py apps/api/tests/test_phase15_memory_contracts.py` → **24 passed**.
- Independent r001 bắt được bool/float validation bypass, empty period thành confirmed zero và aggregate cross-company; r002 xác nhận đã sửa nhưng tìm thấy malformed settlement call ref. Remake r002 thêm opaque-ref validation và validated state transition; independent r003 xác nhận toàn bộ local source boundaries pass, không còn source failure. Xem [r001](../tests/results/phase-16/20261015T100829+0700-r001-test/report.md), [r002](../tests/results/phase-16/20261015T101533+0700-r002-test/report.md), [r003](../tests/results/phase-16/20261015T102032+0700-r003-test/report.md) và [remake r002](../remakes/phase-16/20261015T102032+0700-r002-remake/remake.md).

## Ranh giới và blockers

Chưa có ledger/reservation persistence, reserve atomicity dưới concurrency, budget grant enforcement theo task/day/month, pricing lookup/cost calculation, correction versioning, finance dashboard/drilldown, source reconciliation hay demo hai task + retry. Vì inference grant = 0, IG16 calls/usage thật bị blocked; contract/fixture không thay gate. Phase 15/06 còn trạng thái chưa nghiệm thu. Technical phase conclusion: chưa đủ bằng chứng.
