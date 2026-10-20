# Integration Sprint 04 — evidence commands

All commands ran from the Agent Corporation repository root with `rtk`. No secret, credential, Owner cookie or prompt was printed or stored.

| Check | Command | Outcome |
|---|---|---|
| Repository/runtime preflight | `rtk git status --short`; `rtk git rev-parse --short HEAD`; `rtk proxy docker compose ps` | HEAD `6c7f7bd`; pre-existing Docker, UI Lens and Stabilization 03 changes preserved. API/PostgreSQL/web were already healthy. |
| Current CG01 state | `rtk proxy docker compose exec -T api python -c '...runtime_gate...'` (prints only mode/verified/allowed/reason/override boolean) | Override false; mode strict; verified false; allowed false; reason `missing_or_invalid_proof`. |
| Gateway catalog | `rtk proxy curl --fail --silent --show-error --max-time 5 http://127.0.0.1:15600/api/models` | Read-only response; snapshot dated 2026-10-02 lists `gpt-6-luna`, chat support and `medium`. Catalog is not entitlement. No inference endpoint called. |
| Disposable PostgreSQL/API regression + subprocess restart | `rtk proxy env IG08_EVIDENCE_PATH=docs/reviews/integration-04/evidence/synthetic-runtime-restart.json uv run --project apps/api python scripts/test_playground_isolated.py` | Implementation run: 245 passed, 3 skipped, 1 warning. Runner created a unique disposable database/role, ran migrations and tests, then removed only that DB/role. Runtime data unchanged. |
| Web production build | `rtk proxy npm run --prefix apps/web build` | TypeScript and Vite production build passed. |
| Compose readiness | Existing service inspected; `rtk proxy docker compose exec -T api python -c '...'` read-only health routes | API, PostgreSQL and web healthy; no restart/rebuild. Independent verifier repeated health/readiness. |
| Browser status | Existing Chrome Agent Corporation tab, Office and overview inspected read-only through CUA | Office was at Owner login; Overview reported demo fixture unavailable. No Owner login, reset, mutation or screenshot evidence of a Run. |

The process test's transport is an injected coroutine that records entry and waits; it never opens a network connection. The restart path exercises the Runtime worker's normal `work(scope, once=True)` recovery before claim. All test Run/task/event IDs are classified `synthetic_test_data` in the JSON artifact.

The independent verifier reran the final isolated suite and build after the test robustness edits; see [`independent-addendum.md`](independent-addendum.md). It did not set `IG08_EVIDENCE_PATH`, so the synthetic evidence artifact remains the output of the implementation run.
