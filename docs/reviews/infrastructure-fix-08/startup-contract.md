# Startup contract — Infrastructure Fix 08

## Service boundaries

- `bootstrap` and `migrate` are in the `setup` profile. They are explicit operator actions and are not dependencies of API, web, PostgreSQL, or the Runtime worker.
- API depends only on healthy PostgreSQL. Web depends on healthy API. A normal restart cannot implicitly execute bootstrap or Alembic.
- The Work Order Runtime worker is in the separate `runtime-worker` profile and depends on healthy API and PostgreSQL. It is not part of the default `up` target.
- The Development Playground supervisor remains controlled by `PLAYGROUND_WORKER_ENABLED` inside API, preserving its current demo behavior. It can process only already-authorized Playground turns.

## New installation or a planned migration

Run each step deliberately from the repository root:

```sh
rtk proxy docker compose --profile setup run --build --rm --no-deps bootstrap
rtk proxy docker compose up -d --wait postgres
rtk proxy docker compose --profile setup run --build --rm --no-deps migrate
rtk proxy docker compose up --build -d api web
```

Bootstrap retains persisted database and Owner credentials and never installs or deletes CG01 proof. Migration is an explicit action. There is no automatic downgrade, reset, reseed, or credential regeneration. Back up and verify a recoverable backup before a production-like migration.

For an initialized database with compatible schema, a normal restart is:

```sh
rtk proxy docker compose up -d api web
# or, for containers already created and dependencies already running:
rtk proxy docker compose start api web
```

The API validates required configuration and read-only PostgreSQL catalog signatures at process startup and readiness. It checks required columns, including `runtime_reconciliation_decisions` from migration `20261020_0010`. An incompatible schema stops startup/readiness and names the explicit migration procedure; the API does not invoke Alembic.

## CG01 proof lifecycle

Normal bootstrap does not inspect or synchronize `.local/cg01-proof.json`; an absent source cannot remove an existing runtime proof. The explicit `proof-admin` service has no network, runs as UID 1000, mounts the runtime secret volume and gateway fingerprint source read-only, and logs only action metadata and hashes.

```sh
rtk proxy docker compose --profile operator run --rm proof-admin python scripts/manage_cg01_proof.py status
rtk proxy docker compose --profile operator run --rm -T proof-admin python scripts/manage_cg01_proof.py install --confirm install-cg01-proof < .local/cg01-proof.json
rtk proxy docker compose --profile operator run --rm proof-admin python scripts/manage_cg01_proof.py revoke --confirm revoke-cg01-proof
```

The installer accepts bytes only through stdin, verifies mode/ownership/size plus the existing strict gate's endpoint, transport, source fingerprint, expiry, evidence, and capability fields, then atomically replaces the runtime file. An invalid or expired proof is not installed. A retained stale proof continues to fail the strict gate. These commands do not grant inference; Owner grants, policy, and runtime checks remain separate.

## Migration from the previous Compose behavior

Previously API/PostgreSQL startup depended on bootstrap and migrate completion, so a Compose start could rerun setup. The new profile boundaries remove those implicit dependencies. Existing named volumes and data remain the source of truth. During a later controlled deployment, first verify the current revision and backup; if the database is already at `20261020_0010` and compatible, deploy API/web without running `migrate`. Do not run bootstrap just to restart an initialized stack. If an explicit migration is later required, take a verified backup and invoke the migration service as its own reviewed step.

The generated Compose regression verifies this contract in disposable volumes; that runtime verification is currently blocked by the Docker Desktop capacity preflight documented in the report.
