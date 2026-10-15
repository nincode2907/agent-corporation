# Commands and evidence — Phase 07 r005

Tất cả shell commands dùng tiền tố `rtk`. No secrets, Owner cookies, gateway prompts or live event payloads were read or saved.

## Focused API regression

```text
rtk proxy uv run --project apps/api pytest apps/api/tests/test_phase07_feed.py apps/api/tests/test_phase06_runtime.py apps/api/tests/test_phase09_work_orders.py apps/api/tests/test_owner_auth.py -q
exit 0
54 passed, 9 skipped, 1 deprecation warning in 1.49s
```

This covers event cursor tamper/expiry/session/scope checks, safe event envelope/frame, advanced Last-Event-ID route precedence, and adjacent Owner/runtime/work-order regressions.

## Full API suite on disposable PostgreSQL

```text
rtk proxy uv run --project apps/api python scripts/test_playground_isolated.py
exit 0
Alembic: fresh disposable DB upgraded to head (20261014_0009).
pytest: 143 passed, 11 skipped, 1 warning in 18.36s.
Disposable Playground test database/role removed; runtime data unchanged.
```

Runner review before execution: generates a random `ac_pgtest_<16 hex>` DB and matching role, uses those names in test/migration URLs, sets `PLAYGROUND_TEST_ISOLATED=1`, migrates only that DB, runs `apps/api/tests`, then drops the exact generated DB with `FORCE` and exact generated role. No runtime DB migration/seed/reset was run.

## Web checks

```text
rtk proxy npm run --prefix apps/web lint
exit 0 (oxlint, no diagnostics)

rtk proxy npm run --prefix apps/web build
exit 0 (tsc -b and Vite production build; 21 modules transformed)
```

## Source evidence and limitations

- Read r004 report, r004 remake, current Phase 07 checklist, RULES, master-plan dependency summary, event router/feed, cursor tests and RuntimePanel reconnect path.
- `test_stream_uses_advanced_last_event_id_on_eventsource_reconnect` constructs query cursor + advanced Last-Event-ID, verifies stream returns 200 and `page()` receives the header value.
- `RuntimePanel.tsx` updates its saved cursor from SSE IDs/heartbeat, keeps EventSource retrying on transient network/5xx errors, probes read-only event page on `onerror`, and presents a gap/reload message for 400/409/410/422 or inconsistent sequence state.
- Browser network drop/reconnect was not exercised; no browser tool path for network interception was used in r005. No live inference/grant/gateway access.
- Parent will add final r005 summary to Markdown and render roadmap after this report; this agent did not render or edit master-plan.
