# Code risk — test canary cleanup on failure

In `apps/api/tests/test_phase04_demo_factory.py::test_demo_seed_and_reset_are_deterministic_and_scope_limited`, two external canary environments plus Work Orders/artifacts are inserted before repeated reset assertions. Their DELETE statements are after all manifest/state/canary assertions and are not registered as a pytest finalizer or protected by `try/finally`. If an assertion raises before those DELETEs, synthetic benchmark/real rows can remain in the shared DB.

This batch ran the happy path successfully, and its cleanup code executed. Failure-path cleanup was not injected because doing so before a finalizer exists would intentionally leave rows behind. Tag is `need-change/blocked`: source-verified risk, not a reproduced leak.
