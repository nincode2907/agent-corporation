# Integration Fix 05.1 — Browser smoke evidence

**Date:** 20/10/2026 · **Target:** disposable Integration 05 stack at `127.0.0.1:15502`, isolated named Compose project/volumes, synthetic Owner credential, `RUNTIME_CG01_DEMO_TEST_OVERRIDE=false`, fake API/worker transport only.

- Opened the overview and Office routes in Chrome. The overview rendered Demo Corporation fixture state, three employee profiles, and explicit “no model call”/unknown usage wording.
- Office first showed the Owner sign-in gate. After signing into the disposable synthetic Owner scope, it showed authenticated scope plus empty, labeled counts for processing, queued, completed-awaiting-acceptance, failed, and unknown outcomes.
- Did not create a grant or Runtime Run in this browser smoke. Therefore the interrupted-Run reconciliation panel was not exercised in-browser; its auth, API, rendering contract, concurrency and late-usage behavior are covered by isolated API tests and TypeScript/Vite build.
- Cleaned up the disposable stack and its named volumes after the smoke. Shared containers, database and gateway were not used or modified.

This is a smoke check of rendered navigation/auth/empty states, not a live-model or CG01 verification.
