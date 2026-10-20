# Minimal deployment plan — Infrastructure Fix 08 + UI Fix 07

**Status: ready for a separate Owner deployment authorization.** The current task authorized isolated verification only. Do not execute this plan until the Owner requests deployment.

## Before deployment

1. Re-read the current working tree, Compose config, container state, volumes, migration head, grants, dispatch guard, and worker state. Confirm a current recoverable PostgreSQL backup exists and verify its recorded checksum.
2. Confirm the shared database remains at `20261020_0010`, the Demo Corporation and its three EmployeeVersion records are intact, strict CG01 remains unchanged, no active model call or grant exists, and no global dispatch guard is held. If a precondition differs, stop and report it.
3. Review the exact source diff for Fix 08 and UI Fix 07. Preserve the existing database, runtime-secret, artifact, and Owner credential volumes. Do not run `down --volumes`, bootstrap, or migration unless separate evidence proves they are required and the Owner authorizes that action.

## Controlled API/web deployment

1. Rebuild/recreate only the Agent Corporation API and web services with the established Compose project, for example `rtk proxy docker compose up --build -d api web`. PostgreSQL may remain a healthy dependency; do not select `worker`, `proof-admin`, `bootstrap`, or `migrate`.
2. Verify API/web health and that API reports the existing schema compatible at `20261020_0010`. Confirm the three employees and department/version associations remain intact, strict CG01 is still blocked, no grant/model call/run appeared, and the Runtime worker remains stopped.
3. Confirm only the intended Agent Corporation service containers were recreated and all persistent volumes, backup, credentials, and settings remain unchanged.

## UI Fix 07 Owner review

After the deployed source passes the service checks, use the existing authorized local Owner session for read-only UI review:

- Overview → Live Office with all three employees and no Runs.
- Employee card → Runtime form with matching department/version identity and the CG01/grant blocker explained accurately.
- Inspector and Replay empty/historical states.
- Playground at desktop and mobile viewport.
- No duplicate dispatch from navigation/read requests.

Capture the UI Fix 07 review evidence requested in its closure task. Do not create shared Runs, Work Orders, grants, or fake employees. For animated Runtime states, reuse the disposable fake-transport environment. Do not invoke a real model or start the worker.

## Completion boundary

Record the resulting deployment and Owner UI review as evidence, then stop. Do not mark Phase 06–08 accepted automatically, start Phase 09, change CG01, grant inference, or commit/push.
