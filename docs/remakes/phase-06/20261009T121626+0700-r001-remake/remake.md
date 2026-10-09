# Remake Phase 06 — 20261009T121626+0700-r001-remake

## Thông tin vòng sửa

- Phase: 06
- Remake batch: 20261009T121626+0700-r001-remake
- Người/AI remake: Codex `/root`, agents triển khai owner_auth/runtime06/runtime_ui
- Vòng: r001
- Report nguồn: [preflight r001](../../../tests/results/phase-06/20261008T170343+0700-r001-test/report.md)
- Bắt đầu / kết thúc: 2026-10-09T12:16:26+07:00 / 2026-10-09T12:16:26+07:00 (thời điểm ghi snapshot bàn giao code)
- Phạm vi/quyền: Chủ tịch yêu cầu fix blocker và thực hiện lại Phase06–07; gồm prerequisites cần thiết; không nghiệm thu dependency/phase, không gọi inference, không sửa/restart gateway chung.
- Source trước/sau: Source preflight nguồn và [snapshot code mới](evidence/source-manifest.json); giữ worktree dirty có sẵn.
- Inference: Không gọi; grant hiện tại0. Transport giả chỉ cho kiểm thử riêng, không thay run thật.
- Kết luận vòng sửa: Đã triển khai source; cần AI độc lập retest. CG01 và lượt inference thật vẫn bị chặn.

## Mapping results → thay đổi

| Test ID / tag-result nguồn | Nguyên nhân | Thay đổi thực tế / file refs | Trạng thái xử lý | Test cần rerun |
| --- | --- | --- | --- | --- |
| C03 — need-change/blocked nguồn | Dependency chưa được triển khai | Gate/demo thật vẫn thiếu CG01 và grant; không gọi inference. | blocked | C03, regression và các biến thể checklist |
| P06-01 — need-change/blocked nguồn | Dependency chưa được triển khai | Owner session/CSRF/profile bền vững; PG grants, reserve/dispatch guard, model calls/checkpoint/artifact/usage, worker text-only/stop/recovery. Gateway app default đồng bộ15600 theo registry và health/models GET. | changed | P06-01, regression và các biến thể checklist |
| P06-02 — need-change/blocked nguồn | Dependency chưa được triển khai | Gate/demo thật vẫn thiếu CG01 và grant; không gọi inference. | blocked | P06-02, regression và các biến thể checklist |
| P06-03 — need-change/blocked nguồn | Dependency chưa được triển khai | Gate/demo thật vẫn thiếu CG01 và grant; không gọi inference. | blocked | P06-03, regression và các biến thể checklist |
| P06-04 — need-change/blocked nguồn | Dependency chưa được triển khai | Owner session/CSRF/profile bền vững; PG grants, reserve/dispatch guard, model calls/checkpoint/artifact/usage, worker text-only/stop/recovery. Gateway app default đồng bộ15600 theo registry và health/models GET. | changed | P06-04, regression và các biến thể checklist |
| P06-05 — need-change/blocked nguồn | Dependency chưa được triển khai | Owner session/CSRF/profile bền vững; PG grants, reserve/dispatch guard, model calls/checkpoint/artifact/usage, worker text-only/stop/recovery. Gateway app default đồng bộ15600 theo registry và health/models GET. | changed | P06-05, regression và các biến thể checklist |
| P06-06 — need-change/blocked nguồn | Dependency chưa được triển khai | Owner session/CSRF/profile bền vững; PG grants, reserve/dispatch guard, model calls/checkpoint/artifact/usage, worker text-only/stop/recovery. Gateway app default đồng bộ15600 theo registry và health/models GET. | changed | P06-06, regression và các biến thể checklist |
| P06-07 — need-change/blocked nguồn | Dependency chưa được triển khai | Owner session/CSRF/profile bền vững; PG grants, reserve/dispatch guard, model calls/checkpoint/artifact/usage, worker text-only/stop/recovery. Gateway app default đồng bộ15600 theo registry và health/models GET. | changed | P06-07, regression và các biến thể checklist |
| P06-08 — need-change/blocked nguồn | Dependency chưa được triển khai | Owner session/CSRF/profile bền vững; PG grants, reserve/dispatch guard, model calls/checkpoint/artifact/usage, worker text-only/stop/recovery. Gateway app default đồng bộ15600 theo registry và health/models GET. | changed | P06-08, regression và các biến thể checklist |

## Chi tiết và giới hạn

Owner session/CSRF/profile bền vững; PG grants, reserve/dispatch guard, model calls/checkpoint/artifact/usage, worker text-only/stop/recovery. Gateway app default đồng bộ15600 theo registry và health/models GET.

- Trạng thái xử lý: changed cho phần code trong mapping; blocked cho gate/run thật. Không coi changed là clean.
- Kiểm tra trong lúc sửa: Owner auth units và runtime units đã chạy bởi agent; root lint/build đạt. Root phát hiện regression numeric usage bị regex secret redaction che mất và đã sửa helper với test canary. Các kiểm tra này không nghiệm thu phase.
- Phản biện: Không có.
- Còn thiếu/blocker: Inference isolation/read boundary và privacy/retention/cancellation proof CG01; grant Owner riêng cho batch/purpose/model/scope/requests/concurrency/timeout/expiry. Source gateway shared vẫn read-only, không chứng minh cô lập đọc.
- Retest cần chạy: AI độc lập kiểm actual PG migrations/RLS/session/reservation/race/stop/recovery/feed/CSRF/usage, web lint/build và checklist đầy đủ. Live case chỉ sau gate/grant.
- Cleanup: Không tạo request model hoặc thay dữ liệu shared; tests dùng PostgreSQL disposable.
- Evidence: [manifest](evidence/source-manifest.json), [commands](evidence/commands.md).
- Sổ vòng: [phase rounds](../../../tests/results/phase-06/README.md).
