# Phase 07 dependency blocker — r001

- Roadmap dependency là Phase 06; Phase 06 hiện `Bị chặn`. Preflight record: [Phase 06 report](../../../phase-06/20261008T170343+0700-r001-test/report.md), [blocked dependency details](../../../phase-06/20261008T170343+0700-r001-test/evidence/blocked-dependency.md).
- Phase 05 còn Chờ nghiệm thu; CG01 chưa đạt vì codex-server `read-only` không chứng minh read isolation/privacy/retention. Shared gateway không được nới quyền, restart hoặc gửi task input để thử.
- Inference grant = 0. P07-07 run thật không được thực hiện; grant phase/test batch khác không kế thừa.
- API `main.py` chỉ đăng ký health, demo và gateway probe; chưa có Owner auth/session hoặc execution worker/dispatcher. Product spec §9 yêu cầu SSE lấy company/environment scope từ session. Không tạo event endpoint nhận scope do caller tự khai vì có thể lộ event cross-company.
- P07-05/06 crash/session recovery còn phụ thuộc lifecycle request/worker ở Phase 06; không thể chứng minh đúng semantics bằng mock.
- Điều kiện tiếp tục: dependency Phase 06 và CG01 được xử lý theo quyết định của Chủ tịch; có Owner-authenticated scope/session; nếu cần run thật, cấp inference grant riêng theo phase + batch + mục đích + hạn mức/expiry.

Không có thay đổi sản phẩm, DB, API runtime hoặc gateway trong preflight.
