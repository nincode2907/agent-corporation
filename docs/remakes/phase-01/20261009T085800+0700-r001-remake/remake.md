# Remake Phase 01 — 20261009T085800+0700-r001-remake

## Thông tin vòng sửa

- Phase: 01
- Remake batch: 20261009T085800+0700-r001-remake
- Vòng: r001 (report nguồn là batch legacy không có số vòng)
- Report nguồn: [20261008T154512+0700-phase01](../../../tests/results/phase-01/20261008T154512+0700-phase01/report.md)
- Bắt đầu / kết thúc: 2026-10-09 08:58:00 / 2026-10-09 09:01:33 +07:00
- Phạm vi/quyền: Remake Phase 01; kiểm chứng cài sạch, migration baseline và tài liệu. Không thay cấu hình gateway/shared proxy, không dừng DB/runtime dự án, không inference.
- Source trước/sau: `e44bc19783e15b29311f467a2be86943b76d847f` + dirty worktree; [manifest r002](../../../tests/results/phase-01/20261009T085957+0700-r002-test/evidence/source-manifest.json) ghi hashes. Không thay Phase 01 product source.
- Inference: Không gọi; grant = 0.
- Kết luận vòng sửa: Đã xử lý các khoảng trống cần thiết và chuyển sang retest r002; không có sửa sản phẩm mới.

## Mapping results → thay đổi

| Test ID / tag-result nguồn | Nguyên nhân | Thay đổi thực tế / file refs | Trạng thái xử lý | Test cần rerun |
| --- | --- | --- | --- | --- |
| [C02](../../../tests/results/phase-01/20261008T154512+0700-phase01/report.md) need-change/fail | Finding trong report legacy mô tả README cũ; README hiện tại đã được sửa sang IPv4-only trước lượt này | Không sửa thêm; xác minh README + AGENTS + Dev Hub cùng ghi IPv4 loopback; [routes](evidence/commands.md) | no-change | C02, P01-05, P01-06 |
| [P01-01](../../../tests/results/phase-01/20261008T154512+0700-phase01/report.md) need-change/not-run | Cài sạch chưa chạy vì không muốn sửa dependencies/runtime đang dùng chung | Tạo temp copy sạch, chạy `npm ci`, build, `uv sync --locked`, health tests; khởi tạo PG riêng và start API/Vite trong clean copy; [clean start](evidence/fresh-start.md), [commands](evidence/commands.md) | changed | P01-01, C07 |
| [P01-03](../../../tests/results/phase-01/20261008T154512+0700-phase01/report.md) need-change/blocked | DB dùng chung đang được phase khác sử dụng | PostgreSQL container/DB mới dùng Docker cấp ephemeral loopback port; chỉ migrate tới baseline 20261008_0001; xác minh version/schema/idempotency; [commands](evidence/commands.md) | changed | P01-03, C05 |
| Suggestions P01-05/P01-06 | IPv4-only cần nói rõ theo capability hiện tại | README/Dev Hub hiện đã nhất quán; không thay binding hoặc proxy | no-change | P01-05, P01-06 |

## Chi tiết từng finding

### C02 — README IPv6 proxy mismatch

- Expected/actual nguồn: Finding cũ nói README mô tả IPv4/IPv6 trong khi Caddy chỉ bind IPv4.
- Nguyên nhân: README hiện tại đã được sửa trước remediation này; report/evidence legacy giữ nguyên snapshot cũ.
- Thay đổi: Không sửa source; kiểm tra lại README, AGENTS.md và registry cùng giới hạn IPv4-only.
- Kiểm tra trong lúc sửa: `rtk proxy sed -n '24,48p' README.md`; `rtk proxy rg -n -C 4 'agent-corporation|15500|15501|15510' /Users/buivannin/Desktop/workspace/personal/dev-hub/projects.yml`.
- Còn thiếu/blocker: Không có.
- Retest cần chạy: C02, P01-05, P01-06.

### P01-01 — Clean install chưa chạy

- Expected/actual nguồn: README install/run commands hoạt động trên môi trường sạch; report cũ chỉ build/lint ở môi trường hiện tại.
- Nguyên nhân: Tránh ghi vào node_modules/venv dùng chung.
- Thay đổi: Copy apps/web và apps/api vào temp mới; `npm ci`, production build, `uv sync --locked`, health tests; chạy database độc lập và giữ runtime app project không bị thay đổi. Không đổi dependency/lockfile.
- Kiểm tra trong lúc sửa: Xem [clean-start evidence](evidence/fresh-start.md) và [commands](evidence/commands.md). Lần gọi `npm ci --prefix` từ root bị npm từ chối lock context; chạy canonical `npm ci` với cwd là web copy thì thành công.
- Còn thiếu/blocker: Không có.
- Retest cần chạy: P01-01 và regression C07; bằng chứng trực tiếp tại [r002](../../../tests/results/phase-01/20261009T085957+0700-r002-test/report.md).

### P01-03 — Migration từ DB sạch chưa kiểm

- Expected/actual nguồn: Phase 01 baseline upgrade từ DB rỗng, không tạo domain tables của phase sau và idempotent.
- Nguyên nhân: PostgreSQL hiện tại được Phase 04 dùng, không được reset hoặc mutate.
- Thay đổi: PostgreSQL 18.6-alpine digest từ Compose trong container mới, không project volume; Alembic tới `20261008_0001`; xác nhận `alembic_version` là bảng duy nhất và upgrade lặp không đổi revision/schema. Container/temp copy đã cleanup.
- Kiểm tra trong lúc sửa: Xem [commands evidence](evidence/commands.md).
- Còn thiếu/blocker: Không có.
- Retest cần chạy: P01-03; bằng chứng tại [r002](../../../tests/results/phase-01/20261009T085957+0700-r002-test/report.md).

## Cleanup và bước tiếp theo

- Cleanup: Test container `ac-p01-*` đã dừng; temp copy đã xóa. Shared PostgreSQL/API/Vite/Caddy không bị restart hoặc chỉnh.
- Evidence: [commands](evidence/commands.md), [source manifest](evidence/source-manifest.json).
- Retest tiếp theo: r002; [report](../../../tests/results/phase-01/20261009T085957+0700-r002-test/report.md).
- Blocker/giới hạn: Không còn blocker bắt buộc Phase 01.
- Sổ vòng: [README](../../../tests/results/phase-01/README.md).
