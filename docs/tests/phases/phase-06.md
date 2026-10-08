# Kiểm định Phase 06 — Agent đầu tiên chạy trong sandbox

> Checklist dự kiến, chưa có kết quả test. AI đọc lại nguồn hiện tại trước mỗi batch; không gắn tag sẵn hay tự nghiệm thu.

[Rule](../RULES.md) · [Điểm vào](../README.md) · [Mẫu report](../templates/report.md) · [Roadmap](../../master-plan.md) · [Spec V1](../../product-spec.md) · [ADR](../../decisions/0001-v1-foundation.md)

## Nguồn và ranh giới

- Phase: 06
- Dependency từ roadmap: 05; nền event/state của 03
- Yêu cầu liên quan: REQ09, REQ10, REQ11, REQ18, REQ19, REQ22
- Gate: Không có gate IG riêng; vẫn kiểm criteria phase và C01–C08
- Contract hash: 490946f5e3f57adf9e1989d0053f3f0b2dffd3bc0427446f07011c9f0387ac8b

Hash đối chiếu scope/demo/criteria/delivery/limits/evidence/dependency tại thời điểm soạn, không bao gồm status/nhật ký. Nguồn đổi thì cập nhật kế hoạch, không sửa report cũ. Snapshot bên dưới giúp traceability; nguồn hiện tại vẫn ưu tiên.

### Phạm vi phải đọc

- Runtime do app quản lý vòng request/response; map X-Codex-Call-Id tới run, history/checkpoint, profile/policy snapshot và kết quả có cấu trúc.
- Trước request đầu: default deny, inference isolation được kiểm chứng, hạn mức lượt/thời gian/concurrency, quan sát usage cuối lượt và abort tối thiểu; tools chưa bật.
- Ghi event + usage nguồn gốc; xin hạn mức test được Chủ tịch cấp, không tự chạy inference từ UI mở trang.

### Demo bắt buộc

Agent demo xử lý một nhiệm vụ phân tích văn bản nhỏ; thử timeout, từ chối thao tác ngoài scope và dừng đang chạy.

### Giới hạn phase

Không tool mở rộng hay đa agent; USD hard cap chỉ cam kết khi biết pricing và có reservation bảo thủ.

### Evidence bàn giao cần đối chiếu

Trace thật đã lọc, artifact, timeout/deny/abort test, usage provenance.

## Mapping nghiệm thu → test

Mỗi AC là gạch đầu dòng nghiệm thu roadmap hiện tại khi soạn. Kiểm thêm C01–C08 theo rule; tiêu chí thay đổi cần remap trong report. Mọi case dưới đây bắt buộc trong phạm vi phase; không gọi inference nếu chưa có grant, mà ghi blocked cho case cần run thật.

| Tiêu chí | Kỳ vọng từ roadmap | Test IDs tối thiểu |
| --- | --- | --- |
| AC1 | Có request model thật hoàn tất với evidence; lỗi/aborted không hiển thị thành công. | P06-03, P06-04 |
| AC2 | Sandbox/policy kiểm tra hành vi thực; không thừa hưởng quyền unrestricted của phiên Codex hiện tại. | P06-01, P06-02, P06-08 |
| AC3 | Hết hạn mức thì chặn request mới; thiếu usage/cost ghi chưa biết; không cam kết chặn token giữa request khi gateway chưa hỗ trợ. | P06-05, P06-06, P06-07 |

## Ca kiểm định riêng của phase

Mỗi dòng là một test phải có record kết quả riêng. Các biến thể negative/race trong dòng ghi sub-results/evidence để không bỏ sót; nếu một biến thể bắt buộc chưa đạt, cả test không clean. C01–C08 cũng phải có record riêng.

| ID | Test | Bước/điều kiện | Kỳ vọng | Evidence cần lưu | Nguồn bổ sung |
| --- | --- | --- | --- | --- | --- |
| P06-01 | Grant trước dispatch | Thiếu/expired/revoked/wrong phase/batch/scope/model/stop-active bằng fake transport | Deny trước POST; không kế thừa grant hay quyền Codex | Negative tests + dispatch counts | Spec §10/11 |
| P06-02 | Sandbox/input boundary | Kiểm chứng isolation thật của inference environment, canary ngoài inputs | Không đọc secret/context ngoài scope; không đạt thì CG01 blocked | Isolation proof/gap report | Spec §6/10 |
| P06-03 | Một turn text-only thật | Chỉ với grant batch hiện tại, chạy nhiệm vụ văn bản nhỏ tin cậy | Response/artifact thật, mapping request span/gateway call/run; tools off | Redacted trace/artifact/usage refs | Spec §6/9/11 |
| P06-04 | Error/timeout/unknown | Fake failure/timeout; thử live timeout chỉ nếu grant cho phép | Không báo success; unknown reconcile, không auto retry 502/504 | State/event/attempt evidence | Spec §6/8 |
| P06-05 | Resource limits race | Concurrent reserve/dispatch, hết requests/time/concurrency/expiry | 0 dispatch mới trái limits, giữ unresolved thiếu usage; không quảng cáo hard token/USD cap | Reservation/dispatch race logs | Spec §10/11 |
| P06-06 | Stop/abort baseline | Stop trong waiting với mock; live chỉ theo grant, verify gateway cancellation | Chặn bước mới; báo in-flight/unknown thật, không coi UI đóng là abort | Stop epochs, gateway/app evidence | Spec §10/11 |
| P06-07 | Usage provenance | Có/thiếu/late usage bằng fake payload và live response đã được cấp | Confirmed/estimated/unknown riêng, không token-from-text/native totals | Ledger/call mapping assertions | Spec §11 |
| P06-08 | Snapshot và idle | So profile/policy/history/checkpoint run; mở trang idle sau hoàn tất | Snapshot bền vững, không model loop hay real employee/company | DB/source and request counts | Spec §7/10 |

## Lệnh và điều kiện chạy

Chưa có command runtime được xác minh cho phase này khi soạn. Khi phase được triển khai, đọc manifest/scripts/test source và README hiện tại, chọn lệnh tồn tại, ghi lệnh/exit code vào report; không tự bịa endpoint, cài tool/global hoặc scaffold để chạy checklist.

## Kết luận và lưu kết quả

Tạo `docs/tests/results/phase-06/<test_batch_id>/report.md` và `evidence/`. Ghi C01–C08 + P06-01…P06-08 + case bổ sung; mỗi test có đúng một tag `clean`, `need-change`, `suggestion`, result, expected/actual và evidence. Thống kê đầy đủ, kết luận kỹ thuật theo rule, quyết định Chủ tịch riêng. Tiếp tục remake/retest theo RULES.md khi còn need-change giải quyết được trong Phase 06; không tự chuyển phase. Nếu chỉ được giao test không sửa hoặc gặp blocker thật, lưu kết quả và điều kiện tiếp tục.
