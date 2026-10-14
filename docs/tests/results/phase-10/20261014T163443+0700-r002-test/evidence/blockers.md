# Remaining blockers

- Isolated PostgreSQL migration/schema/RLS metadata passes, but no synthetic scoped rows or create/decision/replay lifecycle were exercised. Need isolated DB fixture-driven service tests, including cross-company visibility and idempotency.
- No executor boundary in the tested flow; direct API/tool bypass, reserve/consume atomicity and stop/policy epoch race remain blocked.
- Browser was not started; approval inbox empty/history/decision UI, keyboard focus, responsive layout and cookie/Origin behavior remain unverified.
- Dependency Phase09 is not accepted and still has worker/retry findings.
