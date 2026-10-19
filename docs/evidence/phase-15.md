# Evidence Phase 15 — Context/memory contracts

Ngày: 15/10/2026 (Asia/Ho_Chi_Minh)

## Đã triển khai

- `apps/api/src/agent_corporation_api/modules/memory/contracts.py`: context scope cho corporate/department/employee/task/working; context manifest có giới hạn source/bytes và digest snapshot; yêu cầu exact allowlist refs từ caller; các content/source/evidence locators dùng opaque namespace refs.
- Promotion proposal giữ source/evidence provenance; Owner bắt buộc cho corporate layer, reviewer cần grant; quyết định gắn SHA-256 payload; policy change bị từ chối; version frozen, CAS và rollback tạo version mới không sửa lịch sử cũ.
- Unit tests: `rtk proxy uv run --project apps/api pytest apps/api/tests/test_phase14_hr_contracts.py apps/api/tests/test_phase15_memory_contracts.py -q` → **14 passed**.
- Independent retest: [Phase 15 r002](tests/results/phase-15/20261015T094649+0700-r002-test/report.md) xác nhận opaque content refs, từ chối traversal/path-shaped refs.

## Ranh giới và blockers

Pure contracts không thay trusted ACL checker. Chưa có persistence/RLS, context builder/retrieval thật, promotion/audit inbox, run version snapshot, redaction/retention/resume/chat integration. Phase 14 chưa nghiệm thu; inference grant = 0. Chưa chạy DB/runtime/inference.
