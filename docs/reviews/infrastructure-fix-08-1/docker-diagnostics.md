# Docker resource diagnostics

**Observed:** 2026-10-20 07:38 UTC. All commands were bounded and read-only.

## Classification

**`TELEMETRY_UNAVAILABLE` for available-memory capacity.** The Docker Engine responds, and Docker stats now completes. Its output contains per-container usage and limits, not the Docker Desktop VM's available memory. Docker reports 5,173,080,064 bytes total memory, 4 CPUs, and the runner filesystem has 91,754,942,464 bytes free. Total memory cannot substitute for available memory, and the host filesystem metric has a different scope.

| Required condition | Finding |
|---|---|
| `INSUFFICIENT_CAPACITY` | Not established: no trustworthy current VM available-memory reading. |
| `TELEMETRY_UNAVAILABLE` | **Current preflight result.** No verified VM available-memory source; capacity cannot be confirmed. |
| `DOCKER_ENGINE_UNHEALTHY` | Not current: `docker info`, container listing and bounded stats all succeeded. |
| `PREFLIGHT_IMPLEMENTATION_ERROR` | The former estimate was invalid; no remaining parser defect was found in focused tests. |
| `CAPACITY_CONFIRMED` | Not established. |

The prior 40-second stats timeout is not reproducible now. A bounded comparison completed in 2.705 seconds through `rtk proxy docker stats` and 2.13 seconds through `/usr/local/bin/docker stats`. The difference does not support an `rtk` wrapper bug. The prior timeout remains a historical transient with no retained Engine trace sufficient to identify whether it came from Engine/API latency, Docker Desktop scheduling, or host contention. See [current evidence](evidence/docker-current.json) and the prior sample `../infrastructure-fix-08/evidence/resource-preflight-current.json`.

## Source fix

The runner no longer computes “free” memory by subtracting summed per-container usage from Docker VM total. That calculation omits VM/daemon/kernel/cache usage and can falsely confirm capacity. Docker stats is now treated only as a bounded telemetry-health and format check. Capacity confirmation requires a fresh, provenance-bearing Docker-VM available-memory measurement; macOS host memory/swap is not substituted. Missing, malformed, partial, stale, or conflicting measurements fail closed. The 4 GiB total VM, 2 CPU, 2.5 GiB available-memory and 2 GiB host-disk thresholds were not lowered.

The current Docker Desktop setup does not expose a verified VM-available-memory source to the runner. Therefore no isolated PostgreSQL or test resource was created.

## Final measured probe (supersedes the earlier blocked classification)

On 2026-10-20 09:10:33 UTC the bounded probe read Docker Desktop Linux VM `/proc/meminfo`: `MemTotal=8,337,670,144` bytes and `MemAvailable=5,269,766,144` bytes. `MemTotal` exactly matched Docker Engine total, and the observed cgroup limit remained 67,108,864 bytes. Docker Engine reported 4 CPUs; workspace free disk was 93,423,759,360 bytes. Capacity was confirmed. `/proc/pressure/memory` was unsupported. A second fresh probe before startup smoke also passed. Both probe containers were removed and their labels returned no matches. Full evidence is [docker-vm-memory-probe-final.json](evidence/docker-vm-memory-probe-final.json).
