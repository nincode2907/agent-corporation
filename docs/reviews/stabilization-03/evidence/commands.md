# Sprint 03 verification commands

All commands were run from the repository root with the required `rtk` prefix. No command printed the Owner secret or a gateway credential.

| Check | Command / procedure | Outcome |
| --- | --- | --- |
| Isolated API suite — implementation run | `rtk proxy uv run --project apps/api python scripts/test_playground_isolated.py` | Exit 0; 244 passed, 3 skipped, 1 existing deprecation warning. Runner created and removed disposable PostgreSQL database and role. |
| Isolated API suite — independent run | Same command, executed by `/root/stabilization03_independent` | Exit 0; 244 passed, 3 skipped, 1 warning. Independent addenda: [Phase 07](../../../tests/results/phase-07/20261019T102129+0700-r008-test/independent-addendum.md), [Phase 08](../../../tests/results/phase-08/20261019T102129+0700-r007-test/independent-addendum.md). |
| Web production build | `rtk proxy npm run --prefix apps/web build` | Exit 0; TypeScript and Vite production build succeeded. |
| Browser harness syntax | `rtk proxy node --check docs/reviews/stabilization-03/evidence/authenticated-recovery.mjs` | Exit 0. |
| Browser Owner/auth, recovery and connection state | `rtk proxy env PLAYWRIGHT_MODULE_ROOT=/tmp/ac-stabilization03-playwright PLAYWRIGHT_EXECUTABLE='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome' APP_BASE_URL=http://agent-corporation.localhost/ AUTH_REVIEW_OUTPUT=docs/reviews/stabilization-03/evidence node docs/reviews/stabilization-03/evidence/authenticated-recovery.mjs` | Exit 0; Owner login/logout succeeded; 7/7 navigation checks had no password form; 14 screenshots; 0 page errors. Snapshot recovery used 2 fixture snapshots, accepted event 42, deduplicated its repeat, recovered out-of-order event 44 at watermark 43, and exposed the earlier retention gap. Real Owner SSE showed offline, returned online, showed stale while a heartbeat was held, then recovered after heartbeat. |
| Temporary browser dependency | `npm install --prefix /tmp/ac-stabilization03-playwright playwright@1.55.0` | Installed under `/tmp` for this browser run only; no repo/package lock or global dependency change. Uses installed Google Chrome 155.0.8059.80. |
| Runtime rebuild/start | `rtk proxy docker compose up --build` | Attached runtime logs remain visible in the interactive terminal. API startup and migration completed; `GET /api/v1/health/ready` returned 200. PostgreSQL reported an existing data directory and retained its volume. |
| Runtime state preflight | Read-only SQL in a `READ ONLY` transaction before rebuild | `model_calls` in `dispatched`/`unknown`: 0; Playground turns in `queued`/`dispatched`: 0. |
| Runtime state post-check | Read-only aggregate SQL in a `READ ONLY` transaction after browser run | No `model_calls` rows; no Playground turns. The Owner test session was logged out by the browser test. |
| Diff whitespace | `rtk proxy git diff --check` | Exit 0 at the implementation checkpoint; final documentation and harness syntax were checked again before report close. |

## Harness diagnostics excluded from pass totals

The first browser launch could not resolve Playwright from `apps/web`; no browser session was started. Intermediate harness attempts had an overly strict rendered-text assertion, an event route glob that omitted cursor query parameters, and an offline-state attempt that did not close the held SSE request. Those harness-only attempts are excluded from results. The final harness uses DOM sequence/type fields, releases synthetic routes before testing live read-only SSE, and deliberately aborts a held request while the browser is offline; its final run above succeeded. None of these attempts made product writes or dispatched work.

## Screenshot files

- Office: [desktop](screenshots/office-before-1440x900.png), [mobile](screenshots/office-before-390x844.png)
- Inspector: [desktop](screenshots/inspector-before-1440x900.png), [mobile](screenshots/inspector-before-390x844.png)
- Replay before recovery: [desktop](screenshots/replay-before-1440x900.png), [mobile](screenshots/replay-before-390x844.png)
- Replay after recovery: [desktop](screenshots/replay-after-recovery-1440x900.png), [mobile](screenshots/replay-after-recovery-390x844.png)
- Replay offline: [desktop](screenshots/replay-offline-1440x900.png), [mobile](screenshots/replay-offline-390x844.png)
- Replay with stalled heartbeat: [desktop](screenshots/replay-stale-1440x900.png), [mobile](screenshots/replay-stale-390x844.png)
- Replay after heartbeat recovery: [desktop](screenshots/replay-heartbeat-recovered-1440x900.png), [mobile](screenshots/replay-heartbeat-recovered-390x844.png)

Historical Playground text and opaque IDs are blurred before files are saved. The browser result stores only request methods/paths and synthetic fixture outcomes; it excludes secret, cookies, CSRF values, event cursors and request bodies.
