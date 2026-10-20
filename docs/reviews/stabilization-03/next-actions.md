# Stabilization Sprint 03 — next actions

## Phase 07

1. Snapshot recovery contract and the bounded UI recovery path are implemented and verified by isolated PostgreSQL/API and browser-fixture tests. The authenticated navigation path was confirmed with one Owner login. No phase status change was made.
2. Offline/stale UI and heartbeat recovery now pass against the authenticated read-only Owner event feed. Remaining runtime evidence is a worker/server process restart with event continuity and an actual authorized run through the event UI. Lease-expiry crash recovery logic passed in the disposable database suite.
3. Gateway session expiry/invalidation/disconnect were exercised with fake transport; the application checkpoint/request correlation is retained and no retry is permitted. A live gateway interruption/cancellation claim remains out of scope; unknown outcomes require reconciliation.

## Phase 08 / IG08 — preparation only

1. Before a live demonstration, the Owner must decide a fresh Phase 08 batch and grant: exact demo scope, profile/model, purpose, one request total, concurrency 1, maximum 120 seconds, expiry timestamp, and CG01 mode (`strict` or the already-authorized demo exception). No grant was created for Sprint 03.
2. Before dispatch, verify the worker can dispatch only the explicitly granted Playground queue, the selected demo environment is isolated, tools and fallback are off, and stop controls are available. Do not create a Work Order or auto-renew a grant.
3. Execute at most one text-only request only after that decision. Correlate persisted run/event IDs through Office → Inspector → Replay; read usage only from an authoritative gateway result and report missing values as `unknown`.
4. If the request times out, disconnects, or otherwise has an unknown outcome, inspect checkpoint/idempotency and do not retry. Keep the grant exhausted/expired and stop the worker after evidence capture.
5. IG08 remains **BLOCKED** until the Owner-authorized live run and required event/UI/usage/reconnect evidence exist. Browser fixtures and snapshot integration tests cannot pass IG08.

## Other remaining Phase 08 evidence

- Add negative browser/API checks for a second test-company actor against Inspector and artifact routes when those routes and a disposable scoped fixture are available.
- Compare Replay DB metadata immediately before/after a focused filter/seek/reload journey; session login/logout rows must be accounted for separately.
- Re-run Office/Inspector/Replay against an active authorized run after IG08 approval. Keep screenshots sanitized before writing them to the report directory.

No work is authorized here for Phase 11 or another phase. No AI inference, grant creation, live run, phase transition, commit or push was performed in Sprint 03.
