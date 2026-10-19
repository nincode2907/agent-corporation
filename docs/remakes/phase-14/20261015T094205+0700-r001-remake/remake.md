# Remake Phase 14 — 20261015T094205+0700-r001-remake

- Phase: 14
- Vòng: r001
- Report nguồn: [20261015T094007+0700-r001-test/report.md](../../../tests/results/phase-14/20261015T094007+0700-r001-test/report.md)
- AI triển khai/remake: `/root`
- Source: dirty worktree, không có commit snapshot.

## Finding được xử lý

### P14-05 — Boolean vượt revision guard (major)

- Nguyên nhân: Python coi `True == 1`; revision guards so sánh giá trị mà không xác nhận kiểu ở cả điểm vào và hoàn tất offboard.
- Trạng thái xử lý: `changed`.
- Thay đổi: `begin_offboard` yêu cầu `current_revision` và `expected_revision` là integer thực, dương, bằng nhau; `complete_offboard` yêu cầu `current_revision` là integer thực, dương, đúng revision hiện hành.
- Regression: thêm negative assertions cho `expected_revision=True` ở begin và `current_revision=True` ở complete.
- Files: `apps/api/src/agent_corporation_api/modules/hr/contracts.py`; `apps/api/tests/test_phase14_hr_contracts.py`.
- Hash sau thay đổi: `contracts.py` `fa15a3f557b7e5a952eddb7b678f17696cbcc6c8d5356d9fd791f0b7ea801505`; `test_phase14_hr_contracts.py` `fcd5e0bf8894135fa376b02d48361a6157d5cbd74973b5e2fbf801429363bb48`.
- Validation: `rtk proxy uv run --project apps/api pytest apps/api/tests/test_phase14_hr_contracts.py apps/api/tests/test_phase15_memory_contracts.py -q` → 14 passed; `rtk git diff --check` → exit 0.
- Chờ retest độc lập r002; chưa đóng issue cho đến khi được xác nhận.

## Blockers còn lại

Owner auth/API, proposal audit persistence, fixed probation suite, offboard race/idempotency, durable grant revoke và lệnh stop/drain thật chưa có trong contract slice. Phase 13 chưa nghiệm thu. Không chạy DB/runtime/inference và không tạo/sa thải nhân viên.
