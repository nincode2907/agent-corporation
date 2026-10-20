# Phase 09 — Work Order → Runtime Run bridge recommendation

## Decision

Keep `Runtime Run` as the only model-dispatch/execution engine. Phase 09 adds a narrow queue adapter that turns one accepted Work Order revision into one Runtime Run using the existing authorization and execution path. Do not make the queue worker call the model independently.

## Recommended flow

1. Owner creates/reviews a Work Order revision and explicitly enqueues it under existing Phase 09 controls.
2. A queue lease claimant records `(task_id, revision, lease_id, worker_id)` and validates the accepted revision, assignee, budget, stop conditions and current environment/company scope.
3. The adapter resolves the Owner grant for that revision and calls the existing Runtime Run creation service with the existing `task_id` and revision. It must not create a duplicate generic task. Run identity is bound to the immutable EmployeeVersion assigned by the Work Order revision.
4. A unique bridge receipt keyed by `(environment_id, company_id, task_id, revision)` stores the Run ID and request hash. Retries of bridge delivery return the same Run; a different payload for the same key is rejected.
5. Runtime worker reserves and dispatches under the existing global capacity guard, grant concurrency, CG01 and resource checks. The queue worker does not dispatch inference.
6. Runtime events update queue/task execution projection through a transactional outbox or idempotent consumer. `completed` moves to review/acceptance; `unknown`/interrupted blocks the task and requires explicit reconciliation; stop/pause prevents new reservation.

## Invariants and tests for Phase 09

- One active bridge receipt and at most one Runtime Run per Work Order revision; competing claimants and redelivery cannot duplicate a call.
- Queue lease fencing prevents stale workers from changing task state or attaching a different Run.
- Cross-company, offboarded/stale employee, wrong revision, expired/revoked/mismatched grant, CG01 deny, exhausted budget and stop all fail before model transport.
- Pause/resume, crash between receipt and Run creation, crash after Run creation, expired lease, known pre-HTTP cancellation and unknown in-flight outcome are tested in disposable PostgreSQL with fake transport.
- `unknown` is never auto-replayed. Owner reconciliation semantics and dispatch-guard release must be decided and tested before real inference; retain the guard until there is authoritative evidence.
- Work Order accepted/rejected is a human decision and is never inferred from model completion.
- Playground queue remains independent.

## Data and migration guidance

Prefer a small `work_order_runtime_bindings`/receipt table with scoped unique key, immutable payload hash, Work Order revision, lease fencing token and `run_id` foreign key. Add FORCE RLS and grants consistent with the existing schema. Preserve historical Work Orders without a Runtime Run. If schema constraints allow, reuse the existing `runs.task_id` + `task_revision` relationship and `employee_version_id`; do not add another employee identity column to Runtime state.

## Out of scope here

No queue bridge, queue migration, or new executor was implemented in Integration Fix 05. This recommendation is a Phase 09 input only; it does not authorize the next phase or an inference grant.
