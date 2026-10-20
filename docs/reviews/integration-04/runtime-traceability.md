# Integration Sprint 04 — Runtime traceability

## Finding

A Playground message does **not** create a first-class Run. ADR-0003 and product spec §3/§9 define it as a separate Phase 06 demo interaction. `playground/service.py:36-41,132-150` persists a `playground_turns` row and emits `PLAYGROUND_*` events with `task_id=None`, `run_id=None`, and `correlation_id=session_id`. `playground/worker.py:52-57` claims only Playground turns; `service.py:205-228` stores the outcome and usage on that turn. Its profile and demo employee snapshots do not establish a `Run` or employee-to-run relation.

The first-class Run path is the Phase 06/07 bounded runtime path. `execution/router.py:77-83` exposes Owner-protected `POST /api/v1/runtime/runs`; `execution/service.py:113-153` creates the task, run, runtime state, profile/policy snapshots, checkpoint and `RUN_CREATED` event atomically. `RuntimePanel.tsx:287,342` has a one-run text-analysis form that calls this API only after the Owner selects an existing grant and CG01 reports allowed. `execution/service.py:189-232` reserves the request, records `model_calls`, moves the run to `waiting_model`, emits run-correlated events and saves a non-replay checkpoint. The explicit CLI worker at `execution/worker.py:53-91` performs recovery before claim; `execute_reserved` accepts an injected transport and heartbeats while waiting.

This is not the Work Order queue worker journey. `/api/v1/work-orders` creates/queues tasks and persists queue leases in `work/queue.py`, but no worker connects that queue claim to `runtime_runs`. `main.py` supervises only the Development Playground worker. A direct Runtime Run creates its own generic task and is separate from the queued Work Order screen. The Run/profile snapshot has no assigned `employee_id` or employee profile version, and the Office projection cannot display an executing employee. No API route for reading artifact content exists; artifact metadata is internal to runtime persistence. The Runtime grant API accepts Phase 06/07 (`execution/router.py:16-20`), but its one-click UI helper hardcodes a Phase 06 test grant (`RuntimePanel.tsx:273-284`); no Phase 07 IG08 grant form exists.

## Actual implementation trace

| User action | API command | Persisted task/run | Worker | Model call | Event and SSE | Office | Inspector | Replay |
|---|---|---|---|---|---|---|---|---|
| Send Playground message | `POST /api/v1/playground/sessions/{id}/messages` | `playground_turns`; no Work Order or Run | App lifespan worker claims Playground queue only | Stateless text call attached to turn; no Run `model_calls` association | `PLAYGROUND_*`; session-correlated event can appear on Owner feed/SSE, with null `run_id` | No matching Run lane | Cannot select same Run | Cannot filter to that turn as a Run |
| Submit one Runtime text analysis | `POST /api/v1/runtime/runs` via RuntimePanel | Service creates generic Work Order/task + `runs` + `runtime_runs` in one transaction | Explicit Runtime CLI worker only; no normal app-start dispatch bridge | `model_calls` row with run/request-span IDs; only after reservation | Run/task/request-span IDs; saved before SSE from event store | Shows Run status, but no employee relation | Selects Run and its run-filtered events; profile snapshot version is not surfaced | Read-only event window; filter/seek/reload controls |
| Create/enqueue Work Order | `POST /api/v1/work-orders`, then `/actions` with `enqueue` | Work Order, revision, state and queue entry | Queue claim/lease code exists, but is not wired to Runtime Run dispatch | None in the implemented Phase 09 queue path | Task events have no Run ID | Shows task/queue state only | No correlated runtime Run exists | No Run timeline |

### Correlation and identity limits

- Runtime event correlation uses the Run ID (`execution/service.py:23-27`); request-span IDs are carried in runtime call events and checkpoints (`:214-231`). Event rows have stable IDs and per-company sequence; `/api/v1/events/stream` and `/snapshot-v1` are Owner-scoped reads (`observability/router.py:32-77`).
- `runs.profile_snapshot` records the selected Owner model/effort, tools-off policy, and grant (`execution/service.py:132-143`). It does not bind the Run to an employee/profile revision. The inspector currently renders the same Run/task/model/effort/usage, not the stored snapshot identity.
- Replay uses the event/snapshot projection already loaded in `RuntimePanel.tsx:407-412`; it does not re-execute. Runtime and snapshot tests assert unknown usage stays null and state reads do not dispatch.
- Cross-company reads for event/snapshot routes are covered by scoped API tests. No artifact-content route is registered, so a negative artifact HTTP request cannot be demonstrated as an existing API contract.

### Decision for IG08

Use the first-class Runtime route as the only possible bounded Run source for a non-inference rehearsal. Do not treat a Playground turn or Work Order queue entry as a Run. The current architecture still cannot satisfy the exact requested “active employee + assigned profile/version + queued Work Order worker” UI journey: employee assignment/projection and the Work Order-to-Runtime executor bridge are Phase 09 dependencies. The direct Runtime form plus explicit worker can verify Run/event/no-replay semantics in disposable tests, but not the full product workflow or IG08 acceptance.
