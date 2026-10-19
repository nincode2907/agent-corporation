# Remake Phase 12 — 20261015T091254+0700-r001-remake

- Phase: 12
- Vòng: r001
- Report nguồn: [20261015T091102+0700-r001-test/report.md](../../../tests/results/phase-12/20261015T091102+0700-r001-test/report.md)
- Người triển khai/remake: `/root`
- Nguồn trước/sau: worktree dirty, không có commit snapshot; hashes sau thay đổi ở dưới.

## Findings được xử lý

### P12-02 — Handoff cho phép thiếu evidence (major)

- Nguyên nhân: `Handoff.evidence_refs` có `default_factory=list`; validator chỉ lọc ref path-like nên danh sách trống hợp lệ.
- Trạng thái xử lý: `changed`.
- Thay đổi: bắt buộc 1–50 refs; mỗi ref phải theo namespace ASCII + identifier opaque, từ chối ref rỗng, traversal `..`, slash/backslash và token không đúng grammar.
- Test bổ sung: handoff với `evidence_refs=[]` hoặc `artifact:` bị Pydantic từ chối.
- Hardening kèm theo: `DelegationLimits` từ chối bool/float thay vì chấp nhận do Python bool là int subclass.
- Files: `apps/api/src/agent_corporation_api/modules/orchestration/contracts.py`; `apps/api/tests/test_phase12_orchestration_contracts.py`.
- Hash sau thay đổi: `contracts.py` `7bde67176c3741b0d3507109c1a6d8f8cb27631c2f5a9164da1cc22da17b0a36`; `test_phase12_orchestration_contracts.py` `6e25f5e758163f76aeb5a8dc13c16d96ab9dbd8e6774b855067ec652f8466089`.
- Local validation: `rtk proxy uv run --project apps/api pytest apps/api/tests/test_phase12_orchestration_contracts.py apps/api/tests/test_phase13_organization_contracts.py -q` → 14 passed; `rtk git diff --check` → exit 0.
- Chờ retest độc lập r002; issue chưa đóng cho đến khi report retest xác minh.

## Không đổi / còn blocked

P12-03…07 và runtime portion của C03/C04/P12-01 vẫn blocked: không có integrated executor, atomic budget reservation, stop propagation, persistent receipts, sandbox/demo, reviewer rework/Owner acceptance hoặc grant IG12. Không gọi DB, runtime hay inference. Không thay đổi Phase 11 dependency hoặc quyết định nghiệm thu.
