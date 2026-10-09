# Rà soát nguồn độc lập — Phase 01 r003

- Đọc [master plan](../../../../../master-plan.md), [checklist Phase 01](../../../../phases/phase-01.md), [RULES](../../../../RULES.md), [Product Spec](../../../../../product-spec.md), [ADR-0001](../../../../../decisions/0001-v1-foundation.md), README, Compose, web/API entrypoints, settings, DB readiness, health tests, migration và Dev Hub registry.
- Dependency được ghi là Phase 00; trạng thái Phase 01 hiện `Chờ nghiệm thu`. Các hướng dẫn đang khóa scope ở Phase 01 và inference grant = 0.
- AC1 được kiểm qua lock install/build/start clean-room/API health/isolated migration; AC2 qua registry/listeners; AC3 qua HTTP direct/proxy và browser.
- Sai khác bắt buộc được xác nhận tại P01-01: README chỉ dẫn `npm ci --prefix apps/web` nhưng lệnh thất bại khi chạy trên bản sao sạch với npm 11.19.0; cách chạy từ cwd `apps/web` pass. Không sửa source. Hash các phần source liên quan nằm trong [manifest](source-manifest.json).
- Phase 03 integration test có thể ghi/xóa fixture và phụ thuộc DB; không chạy trên runtime DB dùng chung. Regression chỉ dùng health unit tests/build/lint cùng GET read-only.
