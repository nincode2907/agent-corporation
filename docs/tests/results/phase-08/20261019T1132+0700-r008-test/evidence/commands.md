# Phase 08 r008 — commands and environment

All commands ran from the repository root through `rtk`. Docker Runtime services were inspected read-only and not rebuilt or restarted. No Owner secret/session, user Runtime DB write, grant or inference was used.

| Purpose | Command | Result |
|---|---|---|
| API and isolated Runtime regression | `rtk proxy uv run --project apps/api python scripts/test_playground_isolated.py` | 245 passed, 3 skipped, 1 warning; disposable DB/role removed. |
| Web production build | `rtk proxy npm run --prefix apps/web build` | TypeScript and Vite build passed. |
| Roadmap and whitespace | `rtk proxy git diff --check`; `rtk proxy python3 scripts/render_plan.py` | Passed; roadmap rendered from Markdown. |
| Read-only runtime readiness | See [Sprint 04 command record](../../../../reviews/integration-04/evidence/commands.md). | Existing API/PostgreSQL/web were healthy; no restart/rebuild. |

No authenticated browser checks, DB before/after Replay snapshot, cross-company browser-denial checks, or screenshots were claimed in this batch. Prior Sprint 03 captures are historical regression context only.
