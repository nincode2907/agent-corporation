# Kiểm định Phase 03 — Dữ liệu và bằng chứng bền vững

> Checklist dự kiến, chưa có kết quả test. AI đọc lại nguồn hiện tại trước mỗi batch; không gắn tag sẵn hay tự nghiệm thu.

[Rule](../RULES.md) · [Điểm vào](../README.md) · [Mẫu report](../templates/report.md) · [Roadmap](../../master-plan.md) · [Spec V1](../../product-spec.md) · [ADR](../../decisions/0001-v1-foundation.md)

## Nguồn và ranh giới

- Phase: 03
- Dependency từ roadmap: 01, 02
- Yêu cầu liên quan: REQ05, REQ07, REQ08
- Gate: IG03
- Contract hash: ba1829b14bb55626abb4a88b8a43449ea5b972d489bfe511ed3688e6003b2159

Hash đối chiếu scope/demo/criteria/delivery/limits/evidence/dependency tại thời điểm soạn, không bao gồm status/nhật ký. Nguồn đổi thì cập nhật kế hoạch, không sửa report cũ. Snapshot bên dưới giúp traceability; nguồn hiện tại vẫn ưu tiên.

### Phạm vi phải đọc

- Schema company/environment, department, employee_version, Work Order, run, approval, policy và artifacts.
- Event store ngay từ đầu: company/task/run/agent IDs, occurred/received time, correlation/parent, sequence, sensitivity và dedup key.
- Execution state độc lập event; transaction/outbox, checkpoints, migration, isolation và chỉ mục theo đường truy vấn.

### Demo bắt buộc

Tạo task demo bằng fixture, restart backend, đối chiếu task, run và event vẫn còn.

### Giới hạn phase

Chưa streaming live; không đợi Phase 07 mới tạo event store.

### Evidence bàn giao cần đối chiếu

Schema diagram, migration test, isolation/state/outbox test.

## Mapping nghiệm thu → test

Mỗi AC là gạch đầu dòng nghiệm thu roadmap hiện tại khi soạn. Kiểm thêm C01–C08 theo rule; tiêu chí thay đổi cần remap trong report. Mọi case dưới đây bắt buộc trong phạm vi phase; không gọi inference nếu chưa có grant, mà ghi blocked cho case cần run thật.

| Tiêu chí | Kỳ vọng từ roadmap | Test IDs tối thiểu |
| --- | --- | --- |
| AC1 | Chuyển trạng thái sai bị từ chối; event và state không lệch do transaction thất bại. | P03-03, P03-04 |
| AC2 | Query khác company/environment không đọc được dữ liệu ngoài phạm vi. | P03-01, P03-05 |
| AC3 | Event trùng không nhân đôi; secret thử nghiệm được lọc trước persistence. | P03-06, P03-07 |

## Ca kiểm định riêng của phase

Mỗi dòng là một test phải có record kết quả riêng. Các biến thể negative/race trong dòng ghi sub-results/evidence để không bỏ sót; nếu một biến thể bắt buộc chưa đạt, cả test không clean. C01–C08 cũng phải có record riêng.

| ID | Test | Bước/điều kiện | Kỳ vọng | Evidence cần lưu | Nguồn bổ sung |
| --- | --- | --- | --- | --- | --- |
| P03-01 | Schema và scoped FK | So migration/schema với entities và composite keys/index/query paths | Domain nền đủ; không tham chiếu company/environment chéo | Schema diagram/catalog và negative insert tests | Spec §7 |
| P03-02 | Migration bền vững | Upgrade DB test sạch và snapshot baseline 01, đọc bằng process/connection mới | Đúng version, data/history còn; không coi fresh connection là restart backend | Migration outputs và counts/hash | Spec §7 |
| P03-03 | State/revision | Valid transition rồi sai transition/stale expected_version trên fixture | Sai state/version bị deny, không mutate history/event | State/event before/after, pytest refs | Spec §7/8 |
| P03-04 | Atomic state/event/outbox | Inject lỗi sau state trước event/outbox; commit ca thành công | Rollback toàn bộ revision/state/event/outbox/counter; commit cùng transaction | Counts và failpoint output | Spec §7/9 |
| P03-05 | RLS và scope | Query/write thiếu scope, company khác, environment khác bằng app role | Deny/filter đúng; app non-owner/non-superuser/non-BYPASSRLS; không rò pool scope | Role metadata, RLS/FK tests | Spec §7/10 |
| P03-06 | Envelope/dedup/sequence | Ghi event lặp và concurrent writers cùng company, đọc ordered stream | Không duplicate, sequence ổn định, IDs/time/correlation/sensitivity đủ | Event IDs/seq + concurrency output | Spec §9 |
| P03-07 | Redaction trước lưu | Canary giả ở fields/nested/free text, kiểm revision/event/outbox | Canary không persist hoặc lọt logs; còn correlation | Redacted assertions và source | Spec §9/10 |
| P03-08 | Restart demo fixture | Tạo task/run/events test trong scope; restart riêng backend test, truy IDs | Task/run/checkpoint/events còn, không inference/streaming sớm | Before/after IDs/counts + restart logs | Spec §7/9 |
| P03-09 | IG03 | Đối chiếu internal command/API layer hiện có → PostgreSQL; chạy rollback/restart/dedup/cross-scope | Nền tích hợp PASS có DB thật; nếu chưa có public domain API không thêm route để pass | IG03 report + IDs/test refs, nêu lớp chưa có | Spec §13 |

## Lệnh và điều kiện chạy

Các lệnh đã tồn tại tại lúc soạn (từ root), chưa được chạy trong lượt tạo tài liệu này:

```sh
rtk proxy uv run --project apps/api pytest apps/api/tests/test_phase03_persistence.py
rtk proxy uv run --project apps/api alembic -c apps/api/alembic.ini current
rtk proxy npm run --prefix apps/web build
```

Phase 00 validator gọi renderer và có thể cập nhật HTML: kiểm diff/bản nhìn trước khi chạy. Pytest Phase 03 kết nối DB thật và tạo/xóa fixtures qua migration role: xác minh scope/cleanup từ source và chỉ chạy trên DB kiểm định được phép. Build/lint không thay proof runtime/UX. Migration `current` chỉ đọc version; `upgrade/downgrade`, restart và faults phải chuẩn bị môi trường riêng theo rule.

## Kết luận và lưu kết quả

Gate IG03 phải có verdict riêng và links evidence theo spec §13. Không PASS từ mock nếu nguồn yêu cầu runtime thật. IG03 chưa có public API thì ghi lớp đã kiểm, mismatch/blocked cho proof API còn thiếu; không thêm feature để né gate.

Tạo `docs/tests/results/phase-03/<test_batch_id>/report.md` và `evidence/`. Ghi C01–C08 + P03-01…P03-09 + case bổ sung; mỗi test có đúng một tag `clean`, `need-change`, `suggestion`, result, expected/actual và evidence. Thống kê đầy đủ, kết luận kỹ thuật theo rule, quyết định Chủ tịch riêng. Tiếp tục remake/retest theo RULES.md khi còn need-change giải quyết được trong Phase 03; không tự chuyển phase. Nếu chỉ được giao test không sửa hoặc gặp blocker thật, lưu kết quả và điều kiện tiếp tục.
