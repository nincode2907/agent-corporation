# Scoped snapshot recovery contract — Sprint 03

Decision: [ADR-0004 — Scoped Observability Snapshot](../../decisions/0004-scoped-observability-snapshot.md). Product spec §9 now references the decision. This adds an API/UI recovery contract and no schema migration.

## Read contract

`GET /api/v1/events/snapshot-v1` requires a valid Owner session and derives environment/company scope from that session. The route accepts no arbitrary scope parameters. The backend reads event counter, retained event window and run projection in one PostgreSQL `REPEATABLE READ`, `READ ONLY` transaction with company RLS set before data reads.

Response version `1` contains:

- the newest at most 200 redacted domain events;
- at most 20 run rows with the fields the Office/Inspector projection already consumes;
- the counter watermark, first retained sequence, replay window start and a `history_gap` flag;
- a signed event cursor bound to environment, company and Owner session at the watermark;
- server time.

Event payloads go through the existing public event redaction function. Run projections exclude raw artifacts and message bodies. The encoded response is capped at 512 KiB; larger payloads return HTTP 413 with an explicit error. Owner/session authorization errors remain 401/403. Database unavailability returns 503. Snapshot reads do not write application tables, create runs, dispatch tools or call the model.

## Consistency and recovery

The transaction establishes one repeatable-read snapshot. A commit after the watermark is read belongs to the next SSE page because the returned cursor is signed at that watermark. The client replaces event and run projections together, validates version/order/watermark, then reconnects SSE from the snapshot cursor. It deduplicates event IDs, rejects the same ID with a conflicting sequence and treats missing/out-of-order sequences as another recovery trigger.

The snapshot returns only retained history. It does not reconstruct events that retention removed. If the retained stream has a prefix gap or internal sequence hole, `history_gap=true`; Replay displays the missing-history boundary while current run state can still be refreshed. This prevents a recovery snapshot from implying that older history is complete.

To avoid a reconnect loop, the client bounds repeated snapshot recovery attempts. Invalid schema, repeated gaps and payload overflow remain visible as an error state rather than being silently accepted. A later explicit reload can retry after the cause is addressed.

## Failure and ownership boundaries

- An Owner from another scope cannot request a snapshot by supplying different company IDs; the route has no such inputs, and DB RLS remains active.
- Invalid, expired or differently scoped cursors use the existing cursor validation and produce a gap response; the UI uses the snapshot route for recovery.
- A gateway session is not available to resume through this API. Session rejection is never interpreted as permission to replay an inference request; application checkpoints remain authoritative and unknown outcomes stay unresolved.
- Snapshot recovery supports current read projections. It does not prove live run correlation, gateway cancellation, model entitlement, usage reconciliation, Inspector artifact access or IG08.

## Evidence limits

PostgreSQL integration tests exercise scope, consistent watermark, retention holes, response bounds, read-only behavior and concurrent commit ordering on disposable databases. Browser regression uses an authenticated Owner session and intercepted synthetic API/SSE responses to exercise gap, concurrent event, duplicate, out-of-order recovery and visible historical-gap states at desktop/mobile sizes. Neither fixture evidence is a live inference run or phase acceptance.
