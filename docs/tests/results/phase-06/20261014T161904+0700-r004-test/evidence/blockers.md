# Cần thêm điều kiện để hoàn tất các ca bị chặn

- Phase 06/07: CG01 cần proof thật về isolation/read boundary, privacy/retention và cancellation; sau đó Chủ tịch cấp grant riêng có scope đúng phase/test batch/purpose/model/effort/request cap/concurrency/timeout/expiry. Hiện grant thật = 0; không inference được chạy.
- Phase 07/08: cần run thật được cấp phép, event store/SSE/UI có correlation, reconnect và replay evidence. IG08 giữ BLOCKED.
- PostgreSQL integration: test fixtures hiện dùng settings database và có insert/update/delete cleanup. Cần một PostgreSQL disposable được xác minh riêng, migration fixture riêng và cleanup ID-scoped; chưa có môi trường này trong batch nên không kết nối DB đang chạy.
- Phase 09: implement/verify persistent worker leases, concurrency, restart/crash reconciliation and safe retry lineage; current queue commands alone do not satisfy these criteria.
