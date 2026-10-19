# IG08 live-test proposal — cần Chủ tịch quyết định

**Trạng thái:** đề xuất kế hoạch; chưa cấp grant, chưa gọi inference, chưa dispatch worker, chưa được xem là nghiệm thu.

## Mục tiêu

Kiểm chứng một lần chạy text-only trong scope demo cô lập và đường đi của evidence qua Work → Office → Inspector → Replay. Kiểm tra run/event IDs, trạng thái UI, dừng và lưu evidence. Không dùng kết quả này làm production acceptance.

## Phạm vi xin duyệt

| Thuộc tính | Đề xuất / lựa chọn cần Owner chốt |
| --- | --- |
| Phase / batch | Phase 08 / IG08; batch ID mới sau khi được duyệt |
| Environment | Demo local cô lập, tách dữ liệu/artifacts/threads/secrets khỏi company thật |
| Purpose | Một lần chạy text-only để kiểm chứng event persistence và UI correlation |
| Grant | Session/phase/batch scoped; Owner tạo; đúng purpose; không kế thừa giữa batch |
| Profile/model | **Owner chọn cụ thể**; không đề xuất entitlement/model thay Owner |
| Requests | 1 request tổng; không retry |
| Concurrency | 1 |
| Duration | Tối đa 120 giây; expiry grant là thời điểm cụ thể do Owner đặt trước khi bắt đầu |
| Tools | Tắt; không có side effect ngoài event/run lưu trong demo scope |
| CG01 | Owner chốt `strict` hoặc xác nhận ngoại lệ demo hiện hành. Không tuyên bố CG01 verified trong cả hai trường hợp. |

## Các bước nếu được duyệt

1. Tạo test batch và ghi hash/config không chứa secrets; xác minh đúng demo environment, Owner, purpose, request budget, concurrency, timeout/expiry, tools-off.
2. Xác minh worker chỉ dispatch queue Playground đã được grant; không tạo Work Order hoặc cấp/gia hạn grant tự động.
3. Tạo một request kiểm thử vô hại; ghi run ID/event IDs thực tế và timestamp. Không ghi prompt nhạy cảm vào artifact công khai.
4. Theo dõi persisted status, Office, Inspector và Replay. Correlate cùng run ID/event sequence; kiểm tra event feed reconnect nếu cần mà không gọi request lần hai.
5. Ghi usage/cost chỉ khi gateway/nguồn authoritative trả số liệu; nếu không có, ghi `unknown`. Không ước đoán.
6. Nếu timeout/cancellation không rõ kết quả, chốt unknown, kiểm tra checkpoint/idempotency và **không retry**. Đóng phiên, xác minh worker stopped, lưu sanitized evidence.

## Cổng an toàn và giới hạn

- Dừng nếu env/scope/Owner/profile/grant/expiry/config không khớp; nếu thấy tool bật; nếu budget/concurrency không được enforce; hoặc nếu worker có queue ngoài Playground.
- Đóng HTTP request không chứng minh Codex gateway đã hủy inference. Không retry request có side effect khi kết quả chưa rõ.
- Không dùng demo run để tuyên bố CG01 verified, entitlement production, usage/price chính xác nếu thiếu nguồn, hoặc nghiệm thu Phase 08.
- Trước Phase 23, tuân thủ AGENTS.md: chuyển sang `strict`, stop/restart worker, chạy `rtk proxy uv run --project apps/api python scripts/cg01_mode.py release-check` và chỉ tiếp tục nếu đạt.

## Quyết định tối thiểu cần từ Chủ tịch

Có duyệt tạo grant cho **một** IG08 demo test theo giới hạn ở trên không? Nếu có, quyết định cần ghi rõ: profile/model; demo scope; batch/purpose; `1 request`, concurrency `1`, tối đa `120s`; thời điểm expiry; CG01 mode (`strict` hoặc ngoại lệ demo được phép). Khi chưa có đủ quyết định này, không chạy.
