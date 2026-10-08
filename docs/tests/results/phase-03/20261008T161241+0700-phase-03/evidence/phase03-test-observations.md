# Phase 03 persistence test observations

Command: `uv run --project apps/api pytest apps/api/tests/test_phase03_persistence.py -q`; exit 0, `5 passed in 1.38s`. Full pytest output is summarized in `commands.md`; assertions below come from the exact test source listed by SHA-256 in `source-manifest.json`.

- `test_app_role_is_non_privileged_and_rls_filters_other_company`: asserts `rolsuper=false`, `rolbypassrls=false`; SELECT by other company and other environment returns empty. Does not test missing scope, cross-scope INSERT, or pool scope reuse.
- `test_task_state_event_and_outbox_commit_dedup_and_fresh_connection`: same dedup key returns same work-order/event IDs; first sequence is 1; a fresh DB engine sees draft/version 1, stream sequence 1, pending outbox; transition to queued yields version 2; invalid transition and stale version raise; final state remains queued/version 2. No concurrent writer or full envelope assertion.
- `test_event_failure_rolls_back_work_order_revision_state_and_counter`: monkeypatch makes append_event raise after state work; asserts no work_order, task_execution_state, or event_stream_counter rows. It does not directly assert revisions/events/outbox.
- `test_secret_fields_are_redacted_before_event_and_revision_storage`: fake password/key/Bearer canaries absent from task revision and event; checks helper output. Does not inspect outbox or logs.
- `test_invalid_work_order_is_rejected_before_write`: missing acceptance criteria raises ValueError and leaves no work_order.

All fixture setup rows are under fresh UUID environment IDs; cleanup boundary is described in `fixture-cleanup.md`. No inference was called.
