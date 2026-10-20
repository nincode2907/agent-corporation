# Shared API health diagnosis

**Observed:** 2026-10-20 07:38 UTC. No service was started or changed.

## Current state

The API, PostgreSQL, and web containers are stopped. API exited with code 143, `OOMKilled=false`; PostgreSQL and web exited with code 0. The Runtime worker remains stopped. API live and ready endpoints refuse connections because the container is stopped. This replaces the earlier `running/unhealthy` snapshot in the Fix 08 report.

## Health history and likely cause

At API exit, Docker retained `unhealthy` with 102 failures. Its latest five checks between 06:35:58Z and 06:36:53Z all reported `Health check exceeded timeout (3s)`. PostgreSQL's latest five checks in the same interval also exceeded 3 seconds; web had two timeout failures after passing earlier checks. Before the last timeout interval, the API log records readiness requests returning HTTP 200 through 06:19:38Z. The API then logged a normal graceful shutdown from 06:37:50Z to 06:37:53Z. Docker reports no OOM kill.

This cross-service pattern supports a transient shared latency/resource-pressure explanation more strongly than an API-specific readiness or database-schema defect. Other projects were consuming material Docker VM memory at the observation (including one web container around 1.06 GiB and database containers around 396 MiB and 543 MiB). These are contextual samples only. No incident-time VM available-memory or CPU-pressure sample identifies a single cause, so **the exact cause remains unproven**. The 40-second stats timeout occurred in an earlier sample and cannot be causally tied to the API health failures.

No API source-level healthcheck defect is confirmed. Do not deploy a healthcheck change based only on this evidence. API/PostgreSQL/web startup and any shared-runtime intervention remain outside this authorization.
