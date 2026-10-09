# Commands and observations — Phase 05 r003

Run from repository root. No gateway/API service was contacted or restarted; no inference or DB writes.

| Check | Command | Result |
| --- | --- | --- |
| Remake source hashes | `rtk proxy python3 -c '...'` | 8/8 hashes matched files listed in remake source manifest |
| API regression | `rtk proxy uv run --project apps/api pytest apps/api/tests/test_health.py apps/api/tests/test_codex_gateway.py -q` | Exit 0; 9 passed in 0.53s |
| Web lint | `rtk proxy npm run --prefix apps/web lint` | Exit 0 |
| Web production build | `rtk proxy npm run --prefix apps/web build` | Exit 0; TypeScript and Vite 8.3.3 |
| Tool versions | `rtk proxy node --version && rtk proxy npm --version && rtk proxy uv --version` | Node v24.21.0; npm 11.19.0; uv 0.12.23 |
| Remake + retest source hashes | `rtk proxy python3 -c '...'` | 22/22 manifest hashes match |
| Diff whitespace | `rtk proxy git diff --check` | Exit 0 |
| API/auth/queue source review | `rtk rg -n "authenticated|principal|Owner|owner|queue|retry|fallback|allowlist|create_task|include_router|router" apps/api/src/agent_corporation_api apps/api/tests` | Only codex GET probe route; no authenticated principal/profile or durable gateway queue/policy surfaced. Search hits shown in report context; no secrets inspected. |
| Current dependency/status review | `rtk sed -n '397,450p' docs/master-plan.md`; inspect `AGENTS.md` | Phase 04 and 05 remain Chờ nghiệm thu |
| Test report validator | `rtk proxy python3 docs/tests/scripts/validate.py --batch docs/tests/results/phase-05/20261009T111044+0700-r003-test` | Exit 0; 15 cases/links valid; HTML deterministic, 24 phases, `lang=vi` and favicon verified |
| Roadmap render | `rtk proxy python3 scripts/render_plan.py` | Exit 0; synced `docs/master-plan.html` from Markdown; 24 phases |
| Rendered tracker data | `rtk proxy python3 -c '...'` | Phase 05 test batch r003 loaded from report with verdict `chưa đủ bằng chứng`; phase status remains `Chờ nghiệm thu`; pipeline state `blocked` |

The explicit no-probe boundary means the offline status is not re-observed in this batch. r002 live evidence is historical context only.
