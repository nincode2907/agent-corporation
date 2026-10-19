# Stabilization Sprint 02 — next actions

Thứ tự đề xuất, không tự thực hiện phase kế tiếp:

1. **Owner quyết định snapshot recovery contract cho Phase 07.** Hiện cursor retention gap trả 409 nhưng thiếu API lấy snapshot và cursor khởi đầu mới. Chốt dữ liệu snapshot, scope, version/cursor binding, giới hạn kích thước, và cách UI thay thế state trước khi triển khai.
2. **Đóng test gateway session recovery trong Phase 07.** Dùng fake gateway trả expired/invalid session và xác minh không replay request side effect; giữ unknown outcome làm consumed, không tự retry.
3. **Owner quyết định IG08 live demo test** theo [đề xuất](ig08-live-test-proposal.md). Chỉ sau khi có grant đúng scope/batch/purpose/limit/expiry mới chạy. Nếu yêu cầu release acceptance trước Phase 23, trước đó phải chuyển CG01 sang strict, stop/restart worker và đạt `release-check` như AGENTS.md quy định.
4. **Chạy IG08 theo batch được Owner duyệt**, ghi run/event IDs thật, request/response provenance, usage/cost chỉ từ nguồn xác nhận, UI correlation và cleanup. Nếu request result không rõ, dừng và điều tra checkpoint; không retry.
5. **Bổ sung Phase 08 scope-negative evidence.** Với actor/company fixture trong test database, kiểm HTTP event feed và các endpoint Inspector/artifact nếu route có tồn tại; giữ browser ở Owner test session, không tạo Owner thứ hai thật.
6. **Sau khi có evidence còn thiếu, kiểm định độc lập và để Chủ tịch nghiệm thu.** Cập nhật Markdown rồi render HTML cùng lượt; không tự chuyển phase.

## Điểm dừng hiện tại

- Phase 07: còn gap snapshot contract và gateway-session recovery; live run tới UI không được phép trong Sprint 02.
- Phase 08 / IG08: chờ quyết định/grant cụ thể của Owner; không inference.
- Phase status của roadmap vẫn giữ nguyên.
