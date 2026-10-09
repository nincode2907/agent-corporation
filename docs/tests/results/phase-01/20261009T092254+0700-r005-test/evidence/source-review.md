# Rà soát source độc lập — Phase 01 r005

- Đọc [README](../../../../../../README.md), [master plan](../../../../../master-plan.md), [checklist Phase 01](../../../../phases/phase-01.md), [RULES](../../../../RULES.md), [Product Spec](../../../../../product-spec.md), [ADR-0001](../../../../../decisions/0001-v1-foundation.md), Compose, Vite, API settings/health/demo routers, DB readiness, migrations 0001–0003, tests health/demo factory và Dev Hub registry.
- Phase 01 phụ thuộc Phase 00; master plan giữ trạng thái `Chờ nghiệm thu`. Remake nguồn chỉ đổi README command sang `npm --prefix apps/web ci`; hash runtime/lock/source Phase 01 khớp manifest r004.
- README command mới được chạy nguyên văn trên clean copy. Demo UI được khởi động trên DB riêng đã migrate/seed tường minh; baseline 0001 được kiểm trên database khác hoàn toàn trong cùng server isolated.
- Health failure path được chứng minh live trên API, Vite proxy và UI khi DB test dừng; không chỉ dựa vào mock. Không có source edit trong batch này.
