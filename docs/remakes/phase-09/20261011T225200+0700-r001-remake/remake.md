# Remake Phase 09 — 20261011T225200+0700-r001-remake

## Thông tin vòng sửa

- Phase: 09
- Remake batch: `20261011T225200+0700-r001-remake`
- Người/AI remake: `/root`
- Vòng: r001
- Report nguồn: [kiểm định độc lập r001](../../../tests/results/phase-09/20261011T224700+0700-r001-test/report.md)
- Bắt đầu / kết thúc: 2026-10-11 22:52 +07:00 (Asia/Ho_Chi_Minh)
- Phạm vi/quyền: Triển khai Phase 09 theo yêu cầu “code trước phase 10”; không làm Phase 10, không gọi inference, không chạy migration lên DB dùng chung.
- Source trước/sau: HEAD `f74320e2ff20516ec93fbfe3413cfb953695b51d` + dirty worktree; cập nhật HTML roadmap sau sửa Markdown. Hash/lệnh trong [source-manifest](source-manifest.md).
- Inference: Không gọi; grant = 0.
- Kết luận vòng sửa: C06 được đồng bộ HTML; các thiếu hụt kiểm chứng persistence/runtime bị chặn bởi chưa có PostgreSQL disposable và dependency Phase 08.

## Mapping results → thay đổi

| Test ID / tag-result nguồn | Nguyên nhân | Thay đổi thực tế / file refs | Trạng thái xử lý | Test cần rerun |
| --- | --- | --- | --- | --- |
| C03 `need-change/blocked` | Chưa có demo queue qua pause/restart/resume/retry | Không dựng runtime/demo khi chưa có disposable DB; điều kiện ghi trong [evidence Phase 09](../../../evidence/phase-09.md) | blocked | Demo hai task khi có runtime test riêng |
| C05 `need-change/blocked` | Chưa có DB để kiểm RLS/scope trên migration mới | Không chạy migration hoặc ghi DB dùng chung | blocked | RLS/cross-scope tests trên PostgreSQL disposable |
| C06 `need-change/blocked` | Markdown được cập nhật sau vòng test; HTML chưa có trong snapshot nguồn | Đã chạy `rtk proxy python3 -X utf8 scripts/render_plan.py`; full validator còn dừng ở link máy-local cũ của report Phase 01 ngoài scope | changed | Kiểm tra HTML/sync và full validator khi xử lý link môi trường |
| P09-01 `need-change/blocked` | Thiếu assertion DB no-write cho invalid submission | Không có disposable DB; không sửa ngoài kiểm chứng hợp lệ đã có | blocked | Validation persistence test trong DB disposable |
| P09-02 `need-change/blocked` | Lease race chưa chạy trên PostgreSQL | Test tích hợp đã có nhưng opt-in; không bật khi chưa xác nhận DB riêng | blocked | Parallel claim, cap, fencing và no-duplicate state |
| P09-03 `need-change/blocked` | Chưa chạy migration/crash/recovery | Không có DB disposable/worker runtime; lease hết hạn chỉ requeue an toàn khi chưa có dispatch | blocked | Migration, restart, expired lease, priority ordering |
| P09-04 `need-change/blocked` | Chưa có checkpoint/browser evidence và Phase 08 còn bị chặn | Không nối queue với inference worker | blocked | Pause/resume ở checkpoint và UI evidence; không resume giữa token |
| P09-05 `need-change/not-run` | Chưa có retry/outcome receipt persistence test | Không retry side effect unknown hoặc nối dispatcher | blocked | Known-safe retry, unknown deny, attempt/lineage trên fixture riêng |
| P09-06 `need-change/blocked` | Thiếu persisted run/review/acceptance flow | Chưa có runtime fixture/DB disposable | blocked | Owner-only acceptance, rework history/evidence persistence |
| P09-07 `need-change/blocked` | Thiếu browser/API state comparison | Không có runtime session đã xác minh | blocked | Task board flows, filters, cancel/pause, screenshot + API state |

## Chi tiết C06 — Tài liệu và bản nhìn

- Expected/actual nguồn: Đồng bộ Markdown → HTML và report links; [C06 report](../../../tests/results/phase-09/20261011T224700+0700-r001-test/report.md).
- Nguyên nhân: Renderer chưa chạy tại lúc report r001 được chốt; validator toàn bộ bị dừng bởi link môi trường cũ `../../../../../../dev-hub/projects.yml` trong Phase 01.
- Trạng thái xử lý: changed.
- Thay đổi: Chạy renderer, kết quả `Đã đồng bộ docs\master-plan.html: 24 phase; 1 hoàn tất.` Markdown giữ Phase 09 `Đang triển khai`.
- Phản biện: Link Phase 01 trỏ workspace ngoài repo và không được sửa trong scope Phase 09.
- Kiểm tra trong lúc sửa: `rtk proxy python3 -X utf8 scripts/render_plan.py` exit 0; `rtk proxy git diff --check` exit 0. Đây không phải kết quả retest độc lập.
- Còn thiếu/blocker: Full docs validator vẫn bị chặn bởi link máy-local cũ; không thay đổi Phase 01 artifact.
- Retest cần chạy: Independent retest trong results vòng kế tiếp cho C06; phần còn lại cần điều kiện DB/browser/runtime riêng.

## Chi tiết các blocker còn lại

P09-01..07 và C03/C05 chưa được sửa thành “đạt”; đây là thiếu evidence/runtime, không phải source bug đã tái hiện. Cần môi trường PostgreSQL disposable cho persistence/race/recovery và runtime/browser test. Phase 08 vẫn `Bị chặn`, nên queue lease không được nối vào worker dispatch.

## Cleanup và bước tiếp theo

- Cleanup: Không tạo fixture DB và không ghi dữ liệu; integration suite vẫn opt-in và đã skip.
- Evidence: [source manifest](source-manifest.md), [commands](commands.md).
- Retest tiếp theo: r002 chỉ sau khi kiểm tra độc lập C06; P09 runtime tests sau khi có DB/browser test riêng.
- Blocker/giới hạn: Phase 08 chưa nghiệm thu; PostgreSQL disposable chưa được xác nhận; grant inference = 0.
- Sổ vòng: [results/phase-09](../../../tests/results/phase-09/README.md).
