# Blockers / next evidence

- Browser/app was not started: empty/history/decision states, keyboard focus, responsive layout and real navigation unverified.
- Phase08 IG08 requires upstream proof and an authorized real saved event/run; no inference grant was available or requested.
- Phase09 still lacks worker lease/recovery/retry implementation; needs product work and isolated race/crash evidence.
- Phase10 migration/schema/RLS configuration is verified on the named disposable DB, but no scoped rows or CRUD lifecycle were exercised. Real isolation requires synthetic company/task fixtures and queries as the non-bypass app role; approval lifecycle, replay and consume/reserve race need DB service tests.
- Phase10 executor direct bypass and stop/policy epoch behavior need executor wiring plus isolated tests.
