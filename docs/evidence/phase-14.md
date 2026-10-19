# Evidence Phase 14 — HR contracts

Ngày: 15/10/2026 (Asia/Ho_Chi_Minh)

## Đã triển khai

- `apps/api/src/agent_corporation_api/modules/hr/contracts.py`: proposal ghi nhu cầu/evidence, contract type, model/tools, cost status/basis/source, probation criteria; Owner decision contract không tự tạo employee/grant; assessment giữ unknown và evidence; offboard plan từ chối assignment mới và tách queued/running/unknown để cancel/stop/reconcile; giữ lịch sử.
- Offboard revision guards yêu cầu integer thực, dương, đúng revision; bool không được chấp nhận như `1`.
- Unit tests: `rtk proxy uv run --project apps/api pytest apps/api/tests/test_phase14_hr_contracts.py apps/api/tests/test_phase15_memory_contracts.py -q` → **14 passed**.
- Independent retest: [Phase 14 r002](tests/results/phase-14/20261015T094531+0700-r002-test/report.md) xác nhận 10/10 synthetic invalid revision inputs bị từ chối.

## Ranh giới và blockers

Đây là contract thuần, chưa có Owner API/session authorization, audit persistence, fixed probation suite, real employee mutation, grant revoke, execution stop/drain receipts, history queries hoặc race/idempotency tests. Phase 13 chưa nghiệm thu. Không chạy DB/runtime/inference; không tạo hay sa thải nhân viên.
