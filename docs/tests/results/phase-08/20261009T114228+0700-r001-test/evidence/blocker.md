# Phase 08 dependency blocker — r001

- Roadmap dependency Phase 08 là Phase 07; Phase 07 đang `Bị chặn`, xem [Phase 07 preflight](../../../phase-07/20261009T105531+0700-r001-test/report.md).
- Phase 07 phụ thuộc Phase 06. Phase 06 bị chặn tại Phase 05/CG01: chưa có proof inference isolation/read boundary/privacy-retention và inference grant = 0. Xem [Phase 06 preflight](../../../phase-06/20261008T170343+0700-r001-test/report.md) và [Phase 05 evidence](../../../../../evidence/phase-05.md).
- API hiện chưa có Owner-authenticated session/scope, SSE event feed hoặc Phase 06 execution worker/run thật; Phase 07 preflight đã xác nhận. Không mở public event route dựa trên company/environment IDs do client tự khai.
- IG08 bắt buộc một run thật text-only → events đã lưu → SSE → Office/Inspector/replay và audit IG03. Fixture/mock chỉ được dùng cho UI tests có nhãn và không đủ PASS gate.
- Vì dependency chưa có, không sửa source Phase 08 theo dữ liệu giả hoặc tạo endpoint/permission mới để né boundary. Không inference, không probe/restart gateway, không ghi DB.
- Điều kiện tiếp tục: dependency Phase 06/07 và các quyết định/gates upstream được xử lý; có Owner-authenticated scope boundary/SSE; sau đó Phase 08 được giao lại để triển khai và kiểm chứng IG08. Nếu IG08 cần inference, cần grant mới, riêng cho đúng test batch/mục đích/hạn mức/expiry.
