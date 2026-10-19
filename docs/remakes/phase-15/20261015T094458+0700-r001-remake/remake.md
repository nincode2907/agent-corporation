# Remake Phase 15 — 20261015T094458+0700-r001-remake

- Phase: 15
- Vòng: r001
- Report nguồn: [20261015T094220+0700-r001-test/report.md](../../../tests/results/phase-15/20261015T094220+0700-r001-test/report.md)
- AI triển khai/remake: `/root`
- Source: dirty worktree, không có commit snapshot.

## Finding được xử lý

### C05 / P15-01 — Context content locator chấp nhận path-shaped ref (major)

- Nguyên nhân: `ContextSource.content_ref` chỉ có ràng buộc độ dài, trong khi các ref khác dùng namespace + identifier opaque.
- Trạng thái xử lý: `changed`.
- Thay đổi: thêm validator opaque-ref cho `content_ref`, từ chối path/traversal và ref không namespace; bổ sung negative test `../../outside`.
- Files: `apps/api/src/agent_corporation_api/modules/memory/contracts.py`; `apps/api/tests/test_phase15_memory_contracts.py`.
- Hash sau thay đổi: `contracts.py` `d95871aee0d679f50ee3790f8192e54f43b72ec02e5a0ee899a36ab7f706b449`; test `d51c8073d8b83f0797d975fc6b9e80bd723b7e5a8a4568256465c973770ec214`.
- Validation: `rtk proxy uv run --project apps/api pytest apps/api/tests/test_phase14_hr_contracts.py apps/api/tests/test_phase15_memory_contracts.py -q` → 14 passed; `rtk git diff --check` → exit 0.
- Chờ retest độc lập r002.

## Blockers còn lại

Trusted ACL service, durable context/version storage, real context builder, retrieval, promotion approval/audit, rollback/expiry enforcement and resume/redaction integration remain absent. Phase 14 chưa nghiệm thu. No database/runtime/inference was used.
