# Kiểm định Phase 00 — Chốt đặc tả V1

> Checklist dự kiến, chưa có kết quả test. AI đọc lại nguồn hiện tại trước mỗi batch; không gắn tag sẵn hay tự nghiệm thu.

[Rule](../RULES.md) · [Điểm vào](../README.md) · [Mẫu report](../templates/report.md) · [Roadmap](../../master-plan.md) · [Spec V1](../../product-spec.md) · [ADR](../../decisions/0001-v1-foundation.md)

## Nguồn và ranh giới

- Phase: 00
- Dependency từ roadmap: Không có
- Yêu cầu liên quan: REQ01
- Gate: Không có gate IG riêng; vẫn kiểm criteria phase và C01–C08
- Contract hash: 4956afec8243173e76d4b03d92082b1c328042858f9e0bec9d9d286e88ab2bc5

Hash đối chiếu scope/demo/criteria/delivery/limits/evidence/dependency tại thời điểm soạn, không bao gồm status/nhật ký. Nguồn đổi thì cập nhật kế hoạch, không sửa report cũ. Snapshot bên dưới giúp traceability; nguồn hiện tại vẫn ưu tiên.

### Phạm vi phải đọc

- Chốt Chairman Mode, Operator Mode, 3 tầng quan sát và các luồng chính.
- Chốt ranh giới V1, stack đề xuất, trạng thái Work Order/run và hợp đồng event.
- Chốt các điểm còn mở: codex-server contract/version, authentication, ngân sách demo và môi trường sandbox.

### Demo bắt buộc

Mở docs/product-spec.html, chọn từng bước trong demo đặc tả F01: Work Order → plan → approval → worker/tools → review → bàn giao → Chủ tịch nghiệm thu. Đây là mô phỏng logic bằng dữ liệu đặc tả, chưa gọi model/tool.

### Giới hạn phase

Không tạo UI sản phẩm, không gọi inference.

### Evidence bàn giao cần đối chiếu

Evidence tại docs/evidence/phase-00.md: dependency Không có; 26 requirements/14 screens/8 flows/30 events/R1–R8; gateway source hashes + GET health 200; checks tài liệu/links/examples/MD–HTML/syntax/phạm vi. Không có runtime/E2E tests hay inference.

## Mapping nghiệm thu → test

Mỗi AC là gạch đầu dòng nghiệm thu roadmap hiện tại khi soạn. Kiểm thêm C01–C08 theo rule; tiêu chí thay đổi cần remap trong report. Mọi case dưới đây bắt buộc trong phạm vi phase; không gọi inference nếu chưa có grant, mà ghi blocked cho case cần run thật.

| Tiêu chí | Kỳ vọng từ roadmap | Test IDs tối thiểu |
| --- | --- | --- |
| AC1 | Từng yêu cầu cốt lõi truy ra phase và tiêu chí nghiệm thu. | P00-01 |
| AC2 | Không còn điểm mở có thể làm sai thiết kế Phase 01–03; ghi rõ giả định được chấp nhận. | P00-02 |
| AC3 | Chủ tịch chốt phạm vi V1 và cơ chế chạy thử có inference. | P00-03 |

## Ca kiểm định riêng của phase

Mỗi dòng là một test phải có record kết quả riêng. Các biến thể negative/race trong dòng ghi sub-results/evidence để không bỏ sót; nếu một biến thể bắt buộc chưa đạt, cả test không clean. C01–C08 cũng phải có record riêng.

| ID | Test | Bước/điều kiện | Kỳ vọng | Evidence cần lưu | Nguồn bổ sung |
| --- | --- | --- | --- | --- | --- |
| P00-01 | Traceability V1 | Đối chiếu REQ01–REQ26 với screens S01–S14, flows F01–F08 và phase | Mỗi requirement có criteria/evidence; không mất phạm vi cốt lõi | Ma trận refs và output validator | Spec §3/4/14 |
| P00-02 | Baseline 01–03 | Đọc D01–D08, schema/state/events/auth/queue và O01–O07 | Đủ quyết định để scaffold; điểm mở có owner/deadline/deny behavior | Bảng quyết định và refs ADR | Spec §5/7/8/9/15 |
| P00-03 | Grant và authority | Đối chiếu spec/ADR/roadmap và candidate grant | Owner quyết định; candidate không cấp inference; grants riêng phase/batch | Refs policy và record quyền hiện tại | Spec §10/11/15 |
| P00-04 | Gate tích hợp và release | Đọc CG01, IG03/08/12/16/20 và R1–R8 | Có tiêu chí đo/evidence; không claim đã chạy runtime | Gate matrix và nguồn | Spec §6/13 |
| P00-05 | Contract examples | Chạy validate_phase00.py sau kiểm tra tác động renderer lên docs hiện tại | WorkOrder/Event JSON, states, IDs và refs hợp lệ; không inference | Exit/output đã lọc | Spec §7/8/9 |
| P00-06 | Demo đặc tả | Mở F01 trên product-spec.html, đi qua nhánh approval/rework/acceptance | Đúng thứ tự/state, ghi là đặc tả; không giả run thật | Ảnh thao tác và source comparison | Spec §4 |
| P00-07 | Đồng bộ tài liệu | Đối chiếu MD/HTML/spec/ADR/roadmap, links/lang/favicon và syntax | Các bản nhìn khớp nguồn; không tự thay status/nghiệm thu | Validator output và ảnh nếu thực hiện | Spec §16 |

## Lệnh và điều kiện chạy

Các lệnh đã tồn tại tại lúc soạn (từ root), chưa được chạy trong lượt tạo tài liệu này:

```sh
rtk proxy python3 scripts/validate_phase00.py
```

Phase 00 validator gọi renderer và có thể cập nhật HTML: kiểm diff/bản nhìn trước khi chạy. Pytest Phase 03 kết nối DB thật và tạo/xóa fixtures qua migration role: xác minh scope/cleanup từ source và chỉ chạy trên DB kiểm định được phép. Build/lint không thay proof runtime/UX. Migration `current` chỉ đọc version; `upgrade/downgrade`, restart và faults phải chuẩn bị môi trường riêng theo rule.

## Kết luận và lưu kết quả

Tạo `docs/tests/results/phase-00/<test_batch_id>/report.md` và `evidence/`. Ghi C01–C08 + P00-01…P00-07 + case bổ sung; mỗi test có đúng một tag `clean`, `need-change`, `suggestion`, result, expected/actual và evidence. Thống kê đầy đủ, kết luận kỹ thuật theo rule, quyết định Chủ tịch riêng. Tiếp tục remake/retest theo RULES.md khi còn need-change giải quyết được trong Phase 00; không tự chuyển phase. Nếu chỉ được giao test không sửa hoặc gặp blocker thật, lưu kết quả và điều kiện tiếp tục.
