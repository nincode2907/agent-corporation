# API test coverage reconciliation

## Why the totals differ

The earlier Fix 05.1 result (252 passed, 3 skipped, 1 warning) used the supported PostgreSQL-isolated runner `rtk uv run --project apps/api python scripts/test_playground_isolated.py`. The UI Fix 07 result (217 passed, 38 skipped, 1 warning) used raw `rtk uv run --project apps/api pytest apps/api/tests`, without that runner's opt-in PostgreSQL environment variables. The 35 difference is exactly 20 + 13 + 2 persistence-backed cases that are skipped in the raw invocation and enabled by the isolated runner. This is a command/environment discrepancy, not evidence that tests were deleted or that product code regressed.

The 35 exact collected test cases are:

### 20 Phase 06 Runtime persistence cases

Without `PHASE_RUNTIME_TEST_ISOLATED=1`, these use the fixture's intentional opt-in skip:

1. `test_atomic_grant_race_complete_artifact_snapshot_and_scope`
2. `test_missing_wrong_grant_stop_and_revocation_before_dispatch`
3. `test_unknown_reconciliation_is_owner_audited_idempotent_and_keeps_guard`
4. `test_employee_assignment_is_scoped_current_and_immutable`
5. `test_supervised_fake_worker_waits_completes_and_correlates_one_employee_run`
6. `test_supervised_worker_cg01_denial_keeps_run_queued`
7. `test_supervised_worker_advisory_lock_contender_release_and_reacquire`
8. `test_worker_shutdown_before_http_is_known_failure_and_releases_dispatch_guard`
9. `test_crash_recovery_is_fenced_unknown_and_no_replay`
10. `test_runtime_worker_process_restart_heartbeats_and_never_replays_unknown_post`
11. `test_gateway_expiry_invalidation_and_disconnect_keep_app_checkpoint_without_replay[401-failed]`
12. `test_gateway_expiry_invalidation_and_disconnect_keep_app_checkpoint_without_replay[403-failed]`
13. `test_gateway_expiry_invalidation_and_disconnect_keep_app_checkpoint_without_replay[None-unknown]`
14. `test_429_requeue_bounded_without_fallback_and_usage_unknown`
15. `test_dispatch_transaction_rollback_no_reservation_or_events`
16. `test_global_dispatch_guard_cross_company_race_and_heartbeat`
17. `test_missing_usage_holds_same_grant_reservation_read_is_side_effect_free`
18. `test_grant_expires_while_queued_task_blocks_without_span`
19. `test_late_usage_correction_is_immutable_dedup_and_gateway_bound`
20. `test_fenced_late_usage_never_revives_unknown_call_or_grant`

### 13 Playground persistence cases

Without `PLAYGROUND_TEST_ISOLATED=1`, these require the runner's disposable PostgreSQL database:

1. `test_multi_turn_history_snapshots_usage_unknown_and_work_order_isolation`
2. `test_session_and_send_idempotency_concurrent_duplicate_and_concurrency`
3. `test_expired_grant_before_send_and_before_dispatch_never_calls`
4. `test_limit_exceeded_and_replay_same_key_does_not_spend_again`
5. `test_stop_queued_and_revoke_are_durable_without_dispatch`
6. `test_in_flight_stop_expiry_logout_close_transport_unknown_and_no_retry[stop]`
7. `test_in_flight_stop_expiry_logout_close_transport_unknown_and_no_retry[expiry]`
8. `test_in_flight_stop_expiry_logout_close_transport_unknown_and_no_retry[logout]`
9. `test_worker_crash_restart_fences_late_completion_keeps_unknown_guard_and_consumed_request`
10. `test_rls_fail_closed_scope_and_profile_policy_acceptance`
11. `test_real_worker_process_crash_and_new_process_recovery_never_replays`
12. `test_grant_effective_expiry_is_bounded_by_owner_session`
13. `test_work_order_runtime_and_playground_share_capacity_without_dispatching_each_others_jobs`

### 2 Phase 04 demo factory cases

These are skipped unless `PLAYGROUND_TEST_ISOLATED=1` **and** the database name matches the runner's `ac_pgtest_*` isolation guard:

1. `test_demo_seed_and_reset_are_deterministic_and_scope_limited`
2. `test_demo_reset_http_requires_confirmation_and_rejects_scope_targets`

`pytest --collect-only` confirmed 35 exact cases. The raw-run's other skips are independent: the macOS-inapplicable Owner ACL case and two Phase 09 queue lease cases requiring `PHASE_QUEUE_TEST_ISOLATED=1`. The supported runner enables Playground and Phase 06 persistence coverage but intentionally does not enable Phase 09 queue tests.

## Supported runner attempted for this closure

`rtk uv run --project apps/api python scripts/test_playground_isolated.py` applied the disposable database migrations through `20261020_0010` and began the API suite. It ended with **227 passed, 1 failed, 25 errors, 3 skipped, 1 warning** (188.51 seconds). PostgreSQL connections then failed with “server closed the connection unexpectedly”; runner cleanup could not reconnect to drop the disposable database. Docker inspection showed PostgreSQL, API and web all exited at `2026-10-20T03:45:13Z` with exit code 255 and `OOMKilled=false`, while the worker restarted and remained up without DB access. The suite result is therefore incomplete and is not represented as a product regression verdict. The first failure's traceback was not retained as a review artifact, so it is not attributed to application code.

**Conclusion:** the original 35 count change is explained by opt-in skips. The supported isolated run is inconclusive because its shared PostgreSQL host became unavailable. No test was modified to change counts.

## Phase 08 r008 → r009, by criterion

| Criterion | r008 | r009 | Reconciliation |
|---|---|---|---|
| C01 | clean/pass | clean/pass | Same scope-control evidence. |
| C02 | clean/pass | clean/pass | Same dependency/contract conclusion. |
| C03 | need-change/blocked | need-change/blocked | No authorized live Run in either batch. |
| C04 | clean/pass | clean/pass | Both establish no dispatch on reads within their tested scope; r009 adds browser counters. |
| C05 | need-change/blocked | need-change/blocked | Cross-company/environment and complete redaction checks remain incomplete. |
| C06 | clean/pass | clean/pass | Blocker descriptions remain accurate. |
| C07 | clean/pass (245/3) | clean/pass (217/38) | The API commands differed. The raw r009 invocation skipped 35 opt-in DB tests; its count alone does not show a regression. This closure attempted the supported runner, but the run was interrupted by shared PostgreSQL loss (227 pass, 1 fail, 25 errors, 3 skipped). C07's full regression evidence is now **inconclusive** pending a stable supported run; historical r008/r009 results remain valid for the invocations actually run. |
| C08 | clean/pass | clean/pass | Both batches have scoped synthetic evidence; this closure's failed shared deployment is separately documented and has no new phase acceptance. |
| P08-01 | need-change/blocked | need-change/blocked | Neither batch had an authorized live Run; synthetic UI coverage does not meet live criterion. |
| P08-02 | need-change/blocked | need-change/blocked | r009 adds synthetic EmployeeVersion identity and stale-link coverage, but live/cross-entry Phase 08 evidence remains absent. |
| P08-03 | need-change/blocked | need-change/blocked | No complete authenticated Replay filter/seek/reload DB comparison in either batch. |
| P08-04 | need-change/blocked | need-change/blocked | No complete cross-scope actor/API/SSE/UI proof in either batch. |
| P08-05 | clean/pass | need-change/blocked | r008's source-level redaction/history-label evidence remains historically valid. r009 applies the criterion to source-to-event payload comparison and live output claims, which it did not run. This is missing evidence against the fuller acceptance, not a regression or new product scope. |
| P08-06 | clean/pass | need-change/blocked | r008's recovery test and historical authenticated stale/offline captures remain valid for those states. r009 additionally asks for full gap/filter/reconnect/usage provenance and fresh active-Run UI coverage, not established by the batch. This is missing evidence against the fuller acceptance, not a regression. |
| P08-07 | need-change/blocked | need-change/blocked | Both require an Owner-authorized live text-only Run and IG08 evidence; no grant or inference was used. |

Thus the headline movement from 8 clean / 7 blocked to 6 clean / 9 blocked is **not new product scope and is not evidence of a product regression**. P08-05 and P08-06's narrower r008 evidence is preserved, while r009 correctly blocks the fuller verification it attempted. C07 also needs the supported-run result to be completed; the interrupted run cannot clear or establish a product failure.
