# Kiểm định Phase 06 — 20261014T233046+0700-r009-test

## Thông tin batch

- Phase: 06; vòng r009; test batch `20261014T233046+0700-r009-test`.
- Thời điểm: 14/10/2026, Asia/Saigon.
- Phạm vi: xác minh một lượt inference thật trên UI theo grant tạm Chủ tịch đã cấp; không nghiệm thu toàn phase.
- Profile đã lưu từ UI: `gpt-6-luna`, effort `medium`, profile v1.
- Grant: Phase 06, batch `phase06-ui-b4375333`, 1 request, concurrency 1, timeout 120s, max requeues 0, tools off, expiry 15 phút. Owner xác nhận cấp grant ngay trước thao tác.
- Prompt: “Trả lời bằng tiếng Việt trong tối đa 2 câu: vì sao một tác vụ không nên tự động retry khi kết quả lần gọi trước chưa rõ?” Không chứa dữ liệu riêng tư.
- Run: `100bc3c8-3944-4bed-94aa-770364161b3c`; model `gpt-6-luna`; trạng thái `completed`; outcome `final_response`.
- Gateway: Codex server local qua adapter của ứng dụng. Không gửi request trực tiếp ngoài app.
- Kết luận batch: **4 pass / 1 blocked / 0 fail**. Đây là kiểm thử một lượt, không phải nghiệm thu Phase 06.
- Official status: Phase 06 tiếp tục **Bị chặn**; Chủ tịch chưa nghiệm thu phase.

## Kết quả

### P06-03 — Một turn text-only thật

- Kỳ vọng: một run được cấp qua UI tới model đã chọn, text-only, không tools.
- Thực tế: UI tạo run; worker scoped `--once` dispatch đúng một request. UI hiển thị `completed`, model/effort khớp profile và output cuối cùng:
  “Vì lần gọi trước có thể đã thực hiện hành động dù phản hồi bị mất; retry mù quáng có thể gây tác dụng phụ hoặc xử lý trùng lặp. Chỉ nên retry khi xác định thao tác an toàn lặp lại hoặc có cơ chế idempotency để ngăn lặp.”
- Kết quả: pass
- Tag: clean
- Mức độ: info
- Xử lý/đề xuất: Chỉ kết luận lượt demo được cấp này.

### P06-07 — Nguồn usage

- Kỳ vọng: usage trả về được ghi và liên kết với run; không suy ra chi phí khi chưa có pricing.
- Thực tế: UI hiển thị prompt 10,354 tokens, completion 81, total 10,435; có event `TOKEN_USAGE_RECORDED` và `LLM_CALL_COMPLETED`. Cost basis/giá: unknown.
- Kết quả: pass
- Tag: clean
- Mức độ: info
- Xử lý/đề xuất: Giữ cost basis là unknown.

### P06-12 — Grant, tools và giới hạn lượt

- Kỳ vọng: grant đúng scope/model/limits; tools không bật; không vượt quá một request.
- Thực tế: grant event và run/call events có trong UI; worker payload source đặt `tools=[]`, `tool_choice=none`, `parallel_tool_calls=false`; run kết thúc sau một call. Sau khi tải lại trạng thái, không còn grant đủ điều kiện gửi run, phù hợp `max_requests=1`.
- Kết quả: pass
- Tag: clean
- Mức độ: info
- Xử lý/đề xuất: Không cấp grant khác hoặc gửi thêm request.

### P06-17 — Cấp grant từ UI Owner

- Kỳ vọng: thao tác tường minh dùng profile đã lưu, audit được ghi, cấp grant không tự dispatch.
- Thực tế: sau khi Owner lưu profile v1, nút “Cấp grant test một lượt” tạo grant và UI báo “Chưa gọi model”; chỉ sau nút gửi run mới có `RUN_CREATED`.
- Kết quả: pass
- Tag: clean
- Mức độ: info
- Xử lý/đề xuất: Grant UI không tự dispatch.

### P06-02 — Isolation inference thật

- Thực tế: lượt test dùng demo waiver `mode=demo-test`, `verified=false`; không chạy proof/canary/isolation suite.
- Kết quả: blocked
- Tag: need-change
- Mức độ: major
- Xử lý/đề xuất: Không coi lượt gọi này là bằng chứng CG01; strict/release gate vẫn bắt buộc.

## Giới hạn và sự cố khởi chạy

- Lệnh module ban đầu kết thúc với `ModuleNotFoundError` trước khi worker reserve run hoặc dispatch POST. Không phát sinh call từ lệnh đó. Lệnh `python -c` nạp `apps/api/src` rồi chạy cùng worker đã exit 0 và hoàn tất đúng run đã tạo; không tạo run thứ hai.
- Thời gian hoàn tất xấp xỉ 46 giây, dưới timeout 120 giây. Không thử cancellation, gateway error, timeout, race/concurrency hoặc retry.
- DB lưu profile/grant/run/events trong runtime demo; chưa chạy disposable-DB persistence/race/restart suite.
- Chỉ một model được gọi. Không đoán giá tiền từ token usage.
- Evidence và command đã redact; không đọc/ghi secret vào report. Xem [runtime checks](evidence/runtime-checks.md), [commands](evidence/commands.md), [source manifest](evidence/source-manifest.json), [r008](../20261014T231522+0700-r008-test/report.md) và [remake r007](../../../remakes/phase-06/20261014T231406+0700-r007-remake/remake.md).
