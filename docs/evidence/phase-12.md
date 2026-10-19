# Evidence Phase 12 — Contract nền

Ngày: 15/10/2026 (Asia/Ho_Chi_Minh)

## Đã triển khai

- `apps/api/src/agent_corporation_api/modules/orchestration/contracts.py`: routing thuần deterministic; DAG subtask có giới hạn node/fan-out/depth/iteration; parent/correlation IDs; handoff metadata và opaque evidence refs.
- `apps/api/tests/test_phase12_orchestration_contracts.py`: negative/boundary tests cho route, DAG, duplicate/cyclic/missing references, limits và handoff refs.
- Chạy `rtk proxy uv run --project apps/api pytest apps/api/tests/test_phase12_orchestration_contracts.py apps/api/tests/test_phase13_organization_contracts.py -q`: **14 passed** (gồm cả contract Phase 13), exit 0.

## Ranh giới và phần còn thiếu

Đây là contract/validator thuần; không tạo task, reserve ngân sách, dispatch nhân viên/công cụ, hủy children, thực hiện review/rework hay ghi event/evidence bền vững. Không có demo multi-agent hoặc trace runtime. Phase 11 đang triển khai, nên P12-03…07 và IG12 bị chặn bởi executor, sandbox, durable orchestration, budget/stop và quyền inference riêng. Không inference được gọi; grant = 0. Đây chưa phải nghiệm thu phase.

Kiểm định độc lập được ghi riêng tại `docs/tests/results/phase-12/`.
