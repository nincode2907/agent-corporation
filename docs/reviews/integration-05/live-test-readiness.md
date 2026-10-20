# Integration Fix 05 — Local demo readiness

## Verified 19/10/2026

- Existing app answered on `127.0.0.1:15501`: readiness HTTP 200, PostgreSQL `ok`.
- Existing Nginx answered on `127.0.0.1:15500`: readiness HTTP 200.
- `GET /api/v1/demo/dashboard` returned HTTP 200 and `available=true` from both API and Nginx.
- `http://agent-corporation.localhost/` loaded the actual local dashboard in Chrome. After the initial fixture-loading state, it showed Demo Corporation, 3 employee profiles, 2 departments, 5 fixture Work Orders and 20 fixture events; no reset was used.

This indicates the earlier Sprint 04 “demo unavailable” result is not currently caused by missing seed data, migration or an unavailable API. The prior browser observation was transient or stale; its exact historical cause cannot be determined from the current healthy state.

The shared containers were not rebuilt or restarted for this task. The full Fix 05 browser flow was exercised against the disposable stack. To load the new source into the existing local deployment after review, run `docker compose up --build` from the project root, then `docker compose up`; this reuses existing volumes and does not reset the demo. It starts the supervised Runtime worker, which still requires the existing Owner grant and CG01/resource checks before any dispatch. This task did not authorize a real model request.

## Owner steps

1. Open `http://agent-corporation.localhost/#settings`.
2. On the local machine, read the existing Owner credential only when needed with `docker compose exec api cat /runtime-secrets/owner-secret`; enter it in the local UI. Do not paste it into a report or support ticket.
3. The runtime panel lists current demo employees and displays model/profile, grant and CG01 status. Selecting a person or opening Office does not call a model.
4. Start remains unavailable until a valid Owner-issued grant matches phase, purpose, model/effort, scope, remaining request limit and expiry, and the trusted CG01 policy allows dispatch. Start does not create or renew a grant.

No valid grant was created in the existing deployment for this task. No real model was called. The authenticated fake-gateway demonstration used an isolated app, synthetic Owner credential, disposable PostgreSQL volume, explicit synthetic grants and a fake gate/transport; it has been removed. Its `demo-test/verified=false` status is not production/release proof.

## Production readiness boundary

The UI and demo fixture are available for inspection. A real inference demonstration is **not authorized or ready based on this batch**: CG01 evidence, an Owner-approved run-specific inference grant, and a decision for unresolved in-flight `unknown` outcomes/reconciliation are still required. Keep the existing shared runtime and demo fixture as-is; do not reset them.
