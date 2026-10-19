# Evidence Phase 13 — Contract nền

Ngày: 15/10/2026 (Asia/Ho_Chi_Minh)

## Đã triển khai

- `apps/api/src/agent_corporation_api/modules/organization/contracts.py`: organization snapshot kiểm tra ID duy nhất, scope company/environment, department/reporting cycles và tham chiếu bị thiếu; employee profile version pin contract type, role/persona/model/reasoning, capability/ref và cặp policy ID/version; helper tạo version kế tiếp chỉ khi expected version còn hiện hành.
- `apps/api/tests/test_phase13_organization_contracts.py`: kiểm định graph hợp lệ, cross-scope, chu kỳ, dangling refs, profile validation và stale version conflict.
- Chạy `rtk proxy uv run --project apps/api pytest apps/api/tests/test_phase12_orchestration_contracts.py apps/api/tests/test_phase13_organization_contracts.py -q`: **14 passed** (gồm cả contract Phase 12), exit 0.

## Ranh giới và phần còn thiếu

Đây là contract/validator thuần, chưa có migration/CRUD, authorization Owner-only, immutable DB versions, run snapshots, Inspector/workload/UI, hoặc Employee Chat. Phase 12 chưa nghiệm thu; quyết định target TDG-CG01 vẫn OPEN và baseline 03/06/07/08/10 chưa được nghiệm thu cho chat. Vì vậy chat backend/send, gateway session và inference giữ đóng; Phase 13 chưa đủ bằng chứng kỹ thuật và chưa có quyết định nghiệm thu.

Kiểm định độc lập được ghi riêng tại `docs/tests/results/phase-13/`.
