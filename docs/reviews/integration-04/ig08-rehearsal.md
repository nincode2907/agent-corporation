# Integration Sprint 04 — IG08 non-inference rehearsal

## Result

The requested end-to-end UI rehearsal is **blocked by current integration boundaries**. No run was created in the user's Docker database, no authenticated browser session was available, and no inference grant was created. Playground is intentionally turn-based and unlinked to Runtime Runs. The direct Runtime form is grant/CG01-gated, while the separate Work Order queue has no dispatch bridge to Runtime. The requested Office identity is also missing because Runtime Runs have no employee/profile-version association.

We did execute a narrower, real-subprocess recovery rehearsal with synthetic test data in a unique disposable PostgreSQL database and an injected fake transport. It exercised the Runtime service reservation and actual worker `execute_reserved` / `work` logic across a killed process and a fresh restart process. It did not call the gateway, create a tool action, or write to the shared Docker database. Evidence: [`synthetic-runtime-restart.json`](evidence/synthetic-runtime-restart.json) and [`commands.md`](evidence/commands.md).

## Simulated/verified sequence

| Requested step | Evidence/result |
|---|---|
| Owner submits a demo task through the UI | Not run: current browser showed the Owner login form and the demo fixture API reported unavailable. The test creates a direct Runtime task through the service, not a Work Order queue UI action. |
| Worker claims the task | Verified only in disposable test data: real worker child process reserved a Run and reached the injected fake transport. |
| Run enters `waiting_model` | Verified by the Runtime service transition and `LLM_CALL_STARTED` event before the fake transport waits. The full suite passed; test asserts persisted checkpoints/event order. |
| Office shows active employee/state | Blocked: no employee-to-Run relation or employee projection exists for Runtime Runs. No synthetic employee was assigned. |
| Fake gateway returns a controlled response | Not returned in the crash test: fake transport held the request open so the test could kill the process at the unknown-outcome boundary. Existing deterministic service tests cover controlled completed responses and usage provenance. |
| Response, usage and events persist | Existing isolated suite covers deterministic completion with fake outcome, artifact metadata, gateway call ID, usage provenance and run/task events. Unknown-crash evidence keeps usage null. |
| Inspector and Replay show the same Run | API/source correlation is implemented, but no authenticated UI run could be created in the app. The UI rehearsal is blocked; prior Sprint 03 screenshots are historical recovery fixtures only. |
| Replay does not dispatch again | Service/process recovery test verifies one fake transport entry, one model-call row, unknown result and no second reservation. Replay HTTP/UI filter/seek before/after database comparison was not executed in this batch. |

Every persisted ID in the JSON evidence is generated disposable **synthetic test data**, not production activity. No result here passes IG08: the gate requires an authorized live model Run.

## UI and accessibility checks

- Anonymous/expired state was visible in Chrome at desktop size; protected Office displayed a login form, and the current overview reported that the demo fixture was unavailable.
- Changed the shell's static `Cần session Owner` wording to the neutral access requirement `Yêu cầu quyền Owner` in `apps/web/src/App.tsx`. Authentication, CSRF and API authorization were not changed. Production build passed.
- Authenticated desktop/mobile screenshots for a real active Run were not captured because there was no active Owner session and no valid live Run. Sprint 03's redacted Owner-authenticated desktop/mobile screenshots remain available as historical UI recovery evidence in [`stabilization-03/evidence`](../stabilization-03/evidence/commands.md); they are not this rehearsal.
- Gemini was open but signed out, so no feedback was sent or claimed. A sanitized flow review package is in [`evidence/ux-review-package.md`](evidence/ux-review-package.md).
