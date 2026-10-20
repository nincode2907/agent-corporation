# Verification commands and observations

Date: 20/10/2026 Asia/Ho_Chi_Minh. Commands were run from the project root; shell commands use `rtk`.

| Command | Exit/result |
|---|---|
| `rtk uv run --project apps/api pytest apps/api/tests/test_phase06_runtime.py -q` | 28 passed; 1 Starlette/httpx deprecation warning. |
| `rtk uv run --project apps/api python scripts/test_playground_isolated.py` | Final source: 252 passed, 3 skipped, 1 warning in 27.67s; disposable PostgreSQL DB/role removed. Skips: Windows-only Owner ACL test on macOS and two opt-in Phase 09 queue tests; warning: Starlette/httpx deprecation. |
| `rtk npm run --prefix apps/web build` | TypeScript + Vite production build passed. |
| `rtk proxy docker compose config --quiet` | Exit 0. |
| `rtk proxy docker compose ps --format json` | API, PostgreSQL, web are healthy; no runtime worker container. |
| Read-only PostgreSQL queries via `docker compose exec -T postgres ... psql` | Alembic 0009; fixed-scope Demo Corporation matches once and has 3 employees; runtime_runs=0; model_calls=0; valid unexhausted grants=0; guard empty; existing named PostgreSQL volume intact. |
| Local GETs to API, web and gateway health/model endpoints | API/web/gateway HTTP 200; gateway active/queued requests 0; gateway model catalog includes `gpt-6-luna`. |
| CG01 read-only evaluation inside existing API container | strict; blocked; proof missing/invalid; verified=false. |

No prompt, gateway transcript, API key, Owner secret, or DB dump was read or saved.
