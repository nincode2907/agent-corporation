# P03-08 — isolated backend restart observation

Disposable environment: PostgreSQL 18.6 Alpine by pinned image digest; fresh database upgraded through Alembic head. Test-only fake credentials were used and redacted from this file. Container listened on an OS-assigned `127.0.0.1` port. The application role was non-superuser/non-BYPASSRLS.

Fixture scope IDs:

- environment: `1d8f8c61-2638-47b6-b798-f45d54cfa7f2`
- company: `1b1e2c6e-fc1b-485e-9b83-81307d0ef1bb`
- task: `ae402901-e315-4614-a6db-a80a43290018`
- run: `bf8fdf0d-c8c0-4ad6-8aaa-3c9fac4e75a4`
- checkpoint: `e023a7e6-c035-46b8-b94d-5bf01f8f2d03`

Task/revision/state/event/outbox were created using the Phase 03 `create_work_order` internal command with the application role. Run, execution-state and checkpoint rows were seeded using the migration role because the Phase 03 product currently has no run-creation command. A checkpoint event was appended through the application role. Before API start, app-role scoped query returned `{tasks:1, runs:1, checkpoints:1, events:2}`.

Uvicorn was started as a separate process on loopback port 50327; readiness returned database `ok`. That process was stopped and started again on the same port; readiness again returned database `ok`. A new SQLAlchemy process using the application role and matching company scope returned `{tasks:1, runs:1, checkpoints:1, events:2}` for the same IDs. No public domain HTTP read route was added or assumed; verification reads were scoped database reads after restart.

Cleanup: Uvicorn process stopped; disposable `--rm` PostgreSQL container stopped and removed; shared PostgreSQL/API remained running. No inference/model/tool execution.

Limit: run/checkpoint rows were fixture-seeded directly by migration role rather than produced through an application run API. This proves persistence across a real backend-process restart, while not proving a domain HTTP API or run creation path that Phase 03 does not implement.
