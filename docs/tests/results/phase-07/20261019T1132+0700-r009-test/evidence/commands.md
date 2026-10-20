# Phase 07 r009 — commands and environment

All commands ran from the repository root through `rtk`. The isolated test runner used a unique disposable PostgreSQL database/role and removed those resources at completion. It did not use the shared Runtime database. No live model request or grant was used.

| Purpose | Command | Result |
|---|---|---|
| Final implementation run and synthetic evidence | `rtk proxy env IG08_EVIDENCE_PATH=docs/reviews/integration-04/evidence/synthetic-runtime-restart.json uv run --project apps/api python scripts/test_playground_isolated.py` | 245 passed, 3 skipped, 1 warning. Disposable DB/role removed. |
| Independent retest | `rtk proxy uv run --project apps/api python scripts/test_playground_isolated.py` | 245 passed, 3 skipped, 1 warning in 27.71s; independent addendum records scope. |
| Web regression | `rtk proxy npm run --prefix apps/web build` | TypeScript and Vite build passed in implementation and independent runs. |
| Roadmap and whitespace | `rtk proxy git diff --check`; `rtk proxy python3 scripts/render_plan.py` | Passed; roadmap rendered from Markdown. |

The synthetic restart artifact is linked from the Sprint 04 report; it contains only generated test IDs and synthetic state. The independent rerun did not rewrite it.
