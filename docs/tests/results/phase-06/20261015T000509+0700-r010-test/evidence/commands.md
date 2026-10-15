# Commands and evidence — r010

Tất cả lệnh shell chạy qua tiền tố `rtk`. Không có secret, Owner cookie, request body inference hay transcript nào được in/lưu.

## Isolated PostgreSQL/API suite

Initial invocation used the machine default Python and stopped before connecting to PostgreSQL or creating resources:

```text
rtk proxy python3 scripts/test_playground_isolated.py
exit 1: ModuleNotFoundError: No module named 'sqlalchemy'
```

Rerun with the locked API environment:

```text
rtk proxy uv run --project apps/api python scripts/test_playground_isolated.py
exit 0
Alembic: upgraded fresh disposable database through 20261014_0009.
pytest (final source retest after Owner-expiry/cross-lane changes): 142 passed, 11 skipped, 1 warning in 16.18s.
Disposable Playground test database/role removed; runtime data unchanged.
```

Runner details reviewed before execution: it generates a random `ac_pgtest_<hex>` DB and same-name role; creates a DB URL using those names; sets `PLAYGROUND_TEST_ISOLATED=1`; upgrades only that DB; runs full API suite; and finally drops exactly the generated DB/role. The fixture reset guard now requires that opt-in plus an `ac_pgtest_*` database. No live runtime DB migration or seed was run. The final retest includes Owner-session expiry bounding and shared Work Order/Playground dispatch-capacity tests.

## Web checks

```text
rtk proxy npm run --prefix apps/web lint
exit 0 (oxlint, no diagnostics)

rtk proxy npm run --prefix apps/web build
exit 0 (tsc -b and Vite production build; 21 modules transformed)
```

## Documentation render

```text
rtk proxy python3 -X utf8 scripts/render_phase00.py
exit 0: spec/ADR HTML synchronized (32 requirements, 15 screens, 35 events); master-plan.html synchronized (24 phases; 1 complete)
```

Manual output check: `master-plan.html` contains the r010 marker and batch ID; `product-spec.html` exists and is UTF-8-readable. Current HTML hashes are included in the source manifest.

An additional optional Phase 00 validator invocation returned exit 1 because its internal child invocation of `render_phase00.py` does not inherit the parent `-X utf8` option and fails to decode `docs/product-spec.md` with Windows cp1252. It then prints `PASS contract` from its remaining checks. The dedicated renderer invocation itself exited 0, and this validator behavior did not prevent r010 roadmap/spec HTML generation. This is recorded as a minor tooling suggestion outside Phase 06 implementation scope.

## Source review/runtime observation

- Read AGENTS.md, docs/tests/RULES.md, docs/tests/phases/phase-06.md, ADR-0003, master plan, r009 report/evidence, Playground service/router/worker/migration/settings/lifespan/UI and test files.
- Runtime browser view was reported by parent: already-authenticated Owner page at `#playground`; saved profile and employee list loaded; consent checkbox was empty and Create Grant disabled. This is only a UI-state observation. No login automation, grant creation, chat submission, Stop/reconcile click, or inference was performed in r010.
- Parent also reported read-only confirmation that the earlier completed runtime run/artifact persisted after a previous fixture reset transaction rolled back. This report records that as parent-provided evidence; r010 itself does not query or mutate that runtime data.

## Cleanup and limitations

- Isolated runner returned exit 0 and explicitly reported disposable DB/role removed.
- The default-Python failure occurred before DB setup; no cleanup was needed for that attempt.
- No shared gateway source/config, runtime grant, Owner secret, runtime DB migration, or model endpoint was changed/called.
