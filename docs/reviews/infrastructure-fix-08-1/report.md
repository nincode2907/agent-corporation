# Infrastructure Fix 08.1 — runtime verification unblock

## Outcome

**Current outcome (2026-10-20): the isolated runtime verification is complete and passed.** A bounded container measured fresh Docker Desktop Linux VM `/proc/meminfo` available memory above the unchanged threshold. API/Runtime/Playground tests, explicit migration, startup smoke, and isolated cleanup all passed. The telemetry-blocked outcome below is historical and was superseded. No shared Agent Corporation service or data was changed. See [final verification results](verification-results.md) and the [combined deployment plan](final-deployment-plan.md).

The shared API is currently stopped with exit code 143, not running/unhealthy. At exit it had 102 healthcheck failures. API, PostgreSQL, and web health checks all timed out at 3 seconds during the same interval; API readiness had returned 200 earlier, and shutdown was graceful. This points to transient shared latency/resource pressure, but retained evidence cannot prove the exact cause. No API-specific healthcheck code defect is confirmed.

## Changes

- Removed the unsafe inference that Docker VM free memory equals `MemTotal` minus summed container memory usage.
- Added explicit fail-closed resource classifications, bounded info/stats commands, measurement provenance/freshness requirements, and validation of empty, malformed, or partial stats.
- Added a capacity evaluator that rejects stale or conflicting readings and requires at least 2.5 GiB measured VM-available memory. Existing thresholds remain unchanged.
- Kept denied preflight ahead of Compose resource startup and retained the resource classification in the failed run manifest.
- Added focused guard tests; no shared service, database, grant, proof, volume, or global Docker setting was changed.

## Initial verification (historical; superseded)

- Focused unit tests: **14 passed, 0 failed, 0 skipped, 0 warnings**.
- Full isolated API/Runtime/Playground suite and disposable migration: **not run**; counts N/A.
- Docker resource result: `TELEMETRY_UNAVAILABLE`; `CAPACITY_CONFIRMED` not established.
- Isolated Compose resources created: none. Cleanup: not needed.
- API/web/database current status: all stopped; Runtime worker remains stopped.
- No migration, deployment, inference, grant, or shared-service intervention occurred.

## Owner decision requested at that time

Authorize one isolated verification run on a dedicated CI/external runner whose Docker VM exposes a fresh, reliable available-memory reading and meets the unchanged budget (at least 2.5 GiB available, 4 GiB total, 2 CPUs, and 2 GiB workspace disk). This avoids pausing or changing the shared local stack and Docker Desktop allocation. No run will be initiated until that runner and authorization are available.

See [Docker diagnostics](docker-diagnostics.md), [API health diagnosis](api-health.md), [verification results](verification-results.md), and [sanitized evidence](evidence/docker-current.json).

## Final disposition

Owner-authorized Fix 08/08.1 runtime verification passed. No deployment, migration against shared PostgreSQL, proof/grant/CG01 change, Runtime worker start, inference, phase acceptance, or commit/push was performed. The old API-health and shared-container observations above are historical; re-inspect actual state during the separately authorized deployment preflight.
