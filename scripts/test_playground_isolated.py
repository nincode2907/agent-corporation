"""Run the API regression suite on a private, disposable PostgreSQL Compose project.

The runner never loads application settings or connects to the shared database.
All Docker resources are scoped by one generated Compose project label.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import UTC, datetime
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import threading
import time
from collections import deque
from collections.abc import Callable
from uuid import uuid4

from sqlalchemy import create_engine, text
from sqlalchemy.engine import make_url


ROOT = Path(__file__).resolve().parents[1]
COMPOSE_FILE = ROOT / "compose.test.yml"
EVIDENCE_ROOT = ROOT / "docs/reviews/infrastructure-fix-08/evidence"
LOCK_PATH = ROOT / ".local/infrastructure-fix-08-test.lock"
DOCKER = ("rtk", "proxy", "docker")
MIN_HOST_DISK_BYTES = 2 * 1024**3
MIN_ENGINE_FREE_BYTES = 2560 * 1024**2
MIN_DATABASE_DISK_BYTES = 1024**3
MIN_ENGINE_TOTAL_BYTES = 4 * 1024**3
MIN_ENGINE_CPUS = 2
VM_PROBE_IMAGE = "sha256:d7a8005067f55a2f8ea369e767545fd467b1943a4f0f1a48b7dc44f06c366109"
VM_PROBE_MEMORY_BYTES = 64 * 1024**2

@dataclass(frozen=True)
class DatabaseTarget:
    host: str
    port: int
    database: str
    username: str
    password: str


def validate_target(url: str, expected: DatabaseTarget) -> None:
    """Fail closed unless every URL field names this run's private PostgreSQL."""
    try:
        parsed = make_url(url)
    except Exception:
        raise ValueError("test database URL is invalid") from None
    if parsed.drivername not in {"postgresql", "postgresql+psycopg"}:
        raise ValueError("test database must use PostgreSQL")
    if parsed.host in {"postgres", "agent-corporation-postgres", "host.docker.internal"}:
        raise ValueError("shared database hostname is forbidden")
    if parsed.database == "agent_corporation":
        raise ValueError("shared runtime database name is forbidden")
    if parsed.port == 15510:
        raise ValueError("shared runtime database port is forbidden")
    if (parsed.host, parsed.port, parsed.database, parsed.username, parsed.password) != (
        expected.host, expected.port, expected.database, expected.username, expected.password
    ):
        raise ValueError("database target does not exactly match this isolated test run")


def guarded_connect(url: str, expected: DatabaseTarget, connector):
    """Validate the whole target before invoking any database connector."""
    validate_target(url, expected)
    return connector(url)


def safe_text(value: str, secrets_to_redact: tuple[str, ...]) -> str:
    for secret in secrets_to_redact:
        if secret:
            value = value.replace(secret, "[REDACTED]")
    value = re.sub(
        r"(postgres(?:ql)?(?:\+\w+)?://[^:/\s]+:)[^@/\s]+@",
        r"\1[REDACTED]@",
        value,
        flags=re.IGNORECASE,
    )
    return value


def docker_command(*args: str) -> list[str]:
    return [*DOCKER, *args]


def checked_capture(*args: str, timeout: int = 30, env: dict[str, str] | None = None) -> str:
    try:
        result = subprocess.run(
            docker_command(*args), cwd=ROOT, text=True, capture_output=True,
            encoding="utf-8", errors="replace", timeout=timeout, env=env,
        )
    except subprocess.TimeoutExpired:
        raise TimeoutError(f"Docker command timed out after {timeout}s ({args[0]})") from None
    if result.returncode:
        raise RuntimeError(f"Docker command failed ({args[0]}): {result.stderr.strip()[:500]}")
    return result.stdout.strip()


def parse_size(value: str) -> int:
    match = re.fullmatch(r"\s*([0-9]+(?:\.[0-9]+)?)\s*(B|KiB|MiB|GiB|KB|MB|GB)?\s*", value)
    if not match:
        return 0
    amount = float(match.group(1))
    unit = (match.group(2) or "B").lower()
    multiplier = {"b": 1, "kib": 1024, "mib": 1024**2, "gib": 1024**3,
                  "kb": 1000, "mb": 1000**2, "gb": 1000**3}[unit]
    return int(amount * multiplier)


def assess_capacity(engine_total: int, cpus: int, host_free: int,
                    memory_measurements: list[dict[str, object]], *,
                    now: datetime | None = None) -> dict[str, object]:
    """Evaluate only fresh, provenance-bearing VM-available-memory readings."""
    hard_blockers = []
    if cpus < MIN_ENGINE_CPUS:
        hard_blockers.append("Docker VM has fewer than two CPUs")
    if engine_total < MIN_ENGINE_TOTAL_BYTES:
        hard_blockers.append("Docker VM has less than 4 GiB total memory")
    if host_free < MIN_HOST_DISK_BYTES:
        hard_blockers.append("Host filesystem has less than 2 GiB free")
    if hard_blockers:
        return {"classification": "INSUFFICIENT_CAPACITY", "budget_passed": False,
                "budget_blockers": hard_blockers}

    now = now or datetime.now(UTC)
    valid: list[tuple[int, str, str, datetime]] = []
    for measurement in memory_measurements:
        try:
            amount = int(measurement["available_bytes"])
            source = str(measurement["source"]).strip()
            scope = str(measurement["scope"]).strip()
            verified = measurement["verified"] is True
            observed = datetime.fromisoformat(str(measurement["observed_at_utc"]).replace("Z", "+00:00"))
            age = (now - observed.astimezone(UTC)).total_seconds()
            if (not source or scope != "docker-desktop-vm" or not verified or amount < 0
                    or amount > engine_total or age < 0 or age > 60):
                continue
            valid.append((amount, source, scope, observed.astimezone(UTC)))
        except (KeyError, TypeError, ValueError):
            continue
    if not valid:
        return {"classification": "TELEMETRY_UNAVAILABLE", "budget_passed": False,
                "budget_blockers": ["No fresh, reliable Docker VM available-memory measurement is available"]}

    values = [item[0] for item in valid]
    spread = max(values) - min(values)
    conflict_limit = max(256 * 1024**2, max(values) * 0.15)
    if len(values) > 1 and spread > conflict_limit:
        return {"classification": "TELEMETRY_UNAVAILABLE", "budget_passed": False,
                "budget_blockers": ["Fresh memory sources conflict beyond the 15%/256 MiB tolerance"],
                "memory_measurements": [{"available_bytes": amount, "source": source,
                                         "scope": scope, "verified": True,
                                         "observed_at_utc": observed.isoformat()}
                                        for amount, source, scope, observed in valid]}

    # The most conservative valid value governs the resource decision.
    available = min(values)
    provenance = [{"available_bytes": amount, "source": source, "scope": scope,
                   "verified": True, "observed_at_utc": observed.isoformat()}
                  for amount, source, scope, observed in valid]
    if available < MIN_ENGINE_FREE_BYTES:
        return {"classification": "INSUFFICIENT_CAPACITY", "budget_passed": False,
                "budget_blockers": ["Measured Docker VM available memory is below the 2.5 GiB isolated-test budget"],
                "memory_available_bytes": available, "memory_measurements": provenance}
    return {"classification": "CAPACITY_CONFIRMED", "budget_passed": True,
            "budget_blockers": [], "memory_available_bytes": available,
            "memory_measurements": provenance}


def require_capacity(preflight: dict[str, object]) -> None:
    if preflight.get("classification") != "CAPACITY_CONFIRMED" or preflight.get("budget_passed") is not True:
        raise RuntimeError("Isolated test resources denied: Docker capacity is not confirmed")


def capacity_guarded(preflight: dict[str, object], action: Callable[[], object]) -> object:
    """Invoke a resource-creating action only after capacity is confirmed."""
    require_capacity(preflight)
    return action()


def database_provision_code(database: str, role: str, password: str) -> str:
    role_sql = f'CREATE ROLE "{role}" LOGIN PASSWORD \'{password}\''
    database_sql = f'CREATE DATABASE "{database}" OWNER "{role}"'
    return (
        "import os; from sqlalchemy import create_engine; from sqlalchemy.engine import make_url; "
        "u=make_url(os.environ['DATABASE_URL']); "
        "assert u.host=='isolated-postgres' and u.database=='postgres'; "
        "e=create_engine(u,isolation_level='AUTOCOMMIT'); c=e.connect(); "
        f"c.exec_driver_sql({role_sql!r}); c.exec_driver_sql({database_sql!r}); "
        "c.close(); e.dispose(); print('Disposable role/database created inside isolated network')"
    )


def database_probe_code(database: str, role: str) -> str:
    query = ("SELECT current_database(), current_user, "
             "has_table_privilege(current_user,'public.employee_versions','SELECT')")
    return (
        "import os; from sqlalchemy import create_engine, text; "
        "e=create_engine(os.environ['DATABASE_URL']); c=e.connect(); "
        f"row=c.execute(text({query!r})).one(); "
        f"assert row[0]=={database!r} and row[1]=={role!r} and row[2]; "
        "print('database='+row[0]+' role='+row[1]+' employee_versions_select='+str(row[2])); "
        "c.close(); e.dispose()"
    )


def sample_docker_vm_memory(engine_total: int) -> dict[str, object]:
    """Read VM /proc memory through a tiny isolated container and verify scope."""
    probe_id = uuid4().hex[:12]
    name = "ac-vm-mem-probe-" + probe_id
    label = "agent-corporation.fix081.probe=" + probe_id
    evidence: dict[str, object] = {
        "probe_id": probe_id, "container_name": name, "image_id": VM_PROBE_IMAGE,
        "image_preexisting": False,
        "constraints": {"network": "none", "mounts": [], "read_only_rootfs": True,
                        "memory_limit_bytes": VM_PROBE_MEMORY_BYTES,
                        "memory_swap_limit_bytes": VM_PROBE_MEMORY_BYTES,
                        "cpus": 0.25, "pids_limit": 16, "user": "65534:65534",
                        "capabilities_dropped": "ALL", "timeout_seconds": 8},
        "started_at_utc": datetime.now(UTC).isoformat(),
    }
    container_created = False
    cleanup_ok = False
    try:
        image_id = checked_capture("image", "inspect", "--format", "{{.Id}}", VM_PROBE_IMAGE, timeout=10)
        if image_id != VM_PROBE_IMAGE:
            raise RuntimeError("trusted local probe image ID did not match the pinned image")
        evidence["image_preexisting"] = True
        script = (
            "printf 'VM_MEMINFO_BEGIN\\n'; cat /proc/meminfo; "
            "printf 'VM_PRESSURE_BEGIN\\n'; "
            "if [ -r /proc/pressure/memory ]; then cat /proc/pressure/memory; "
            "else printf 'UNSUPPORTED\\n'; fi; "
            "printf 'CGROUP_MEMORY_MAX_BEGIN\\n'; "
            "if [ -r /sys/fs/cgroup/memory.max ]; then cat /sys/fs/cgroup/memory.max; "
            "else printf 'UNAVAILABLE\\n'; fi"
        )
        container_id = checked_capture(
            "create", "--name", name, "--label", label, "--network", "none", "--read-only",
            "--memory", str(VM_PROBE_MEMORY_BYTES), "--memory-swap", str(VM_PROBE_MEMORY_BYTES),
            "--cpus", "0.25", "--pids-limit", "16", "--cap-drop", "ALL",
            "--security-opt", "no-new-privileges", "--user", "65534:65534",
            "--entrypoint", "/bin/sh", VM_PROBE_IMAGE, "-c", script, timeout=10,
        )
        container_created = True
        evidence["container_id"] = container_id
        host_config = json.loads(checked_capture("inspect", "--format", "{{json .HostConfig}}", container_id, timeout=10))
        limits = {"Memory": host_config.get("Memory"), "MemorySwap": host_config.get("MemorySwap"),
                  "NanoCpus": host_config.get("NanoCpus"), "PidsLimit": host_config.get("PidsLimit"),
                  "ReadonlyRootfs": host_config.get("ReadonlyRootfs"),
                  "NetworkMode": host_config.get("NetworkMode"), "Binds": host_config.get("Binds")}
        evidence["observed_host_config"] = limits
        if (limits["Memory"] != VM_PROBE_MEMORY_BYTES or limits["MemorySwap"] != VM_PROBE_MEMORY_BYTES
                or limits["NanoCpus"] != 250_000_000 or limits["PidsLimit"] != 16
                or limits["ReadonlyRootfs"] is not True or limits["NetworkMode"] != "none"
                or limits["Binds"]):
            raise RuntimeError("probe container did not receive the required isolation limits")

        started = time.monotonic()
        output = checked_capture("start", "--attach", container_id, timeout=8)
        evidence["probe_elapsed_seconds"] = round(time.monotonic() - started, 3)
        if len(output) > 16_384:
            raise RuntimeError("probe output exceeded the expected bound")
        evidence["raw_probe_output"] = output
        section = output.split("VM_MEMINFO_BEGIN\n", 1)[-1].split("VM_PRESSURE_BEGIN\n", 1)[0]
        values: dict[str, int] = {}
        for key in ("MemTotal", "MemAvailable", "MemFree", "SwapTotal", "SwapFree"):
            match = re.search(r"(?m)^" + key + r":\s+(\d+)\s+kB$", section)
            if match:
                values[key + "_bytes"] = int(match.group(1)) * 1024
        if "MemTotal_bytes" not in values or "MemAvailable_bytes" not in values:
            raise RuntimeError("probe did not report both MemTotal and MemAvailable")
        cgroup_section = output.split("CGROUP_MEMORY_MAX_BEGIN\n", 1)[-1].strip().splitlines()
        cgroup_limit = cgroup_section[0].strip() if cgroup_section else "UNAVAILABLE"
        if cgroup_limit != str(VM_PROBE_MEMORY_BYTES):
            raise RuntimeError("probe cgroup limit was not visible at the configured 64 MiB value")
        consistent = abs(values["MemTotal_bytes"] - engine_total) <= engine_total * 0.05
        scope_proven = consistent and values["MemTotal_bytes"] > VM_PROBE_MEMORY_BYTES * 4
        evidence["meminfo_values"] = values
        evidence["cgroup_memory_max_bytes"] = int(cgroup_limit)
        evidence["vm_total_consistency"] = {
            "proc_memtotal_matches_engine_within_5_percent": consistent,
            "delta_bytes": values["MemTotal_bytes"] - engine_total,
            "meminfo_scope_proven_outside_probe_cgroup": scope_proven,
        }
        pressure = output.split("VM_PRESSURE_BEGIN\n", 1)[-1].split("CGROUP_MEMORY_MAX_BEGIN\n", 1)[0].strip()
        evidence["memory_pressure"] = pressure or "not exposed by this Docker VM kernel"
        evidence["observed_at_utc"] = datetime.now(UTC).isoformat()
        if not scope_proven or values["MemAvailable_bytes"] > values["MemTotal_bytes"]:
            raise RuntimeError("/proc memory values do not prove Docker VM scope or have invalid bounds")
    except Exception as error:
        evidence["probe_error_type"] = type(error).__name__
        evidence["probe_error"] = str(error)[:500]
    finally:
        if container_created:
            try:
                checked_capture("rm", "-f", name, timeout=10)
                remaining = checked_capture("ps", "-aq", "--filter", "label=" + label, timeout=10)
                evidence["cleanup_remaining_by_label"] = remaining
                cleanup_ok = not remaining
            except Exception as error:
                evidence["cleanup_error_type"] = type(error).__name__
        evidence["cleanup_verified"] = cleanup_ok if container_created else not evidence.get("container_id")
        evidence["completed_at_utc"] = datetime.now(UTC).isoformat()

    if not evidence.get("cleanup_verified") or evidence.get("probe_error_type"):
        return {"classification": "TELEMETRY_UNAVAILABLE", "budget_passed": False,
                "budget_blockers": ["Docker VM memory probe or its scoped cleanup could not be verified"],
                "probe_evidence": evidence}
    return {"classification": "CAPACITY_MEASURED", "budget_passed": False,
            "memory_measurement": {"available_bytes": values["MemAvailable_bytes"],
                                   "source": "Docker Desktop Linux VM /proc/meminfo MemAvailable",
                                   "scope": "docker-desktop-vm", "verified": True,
                                   "observed_at_utc": evidence["observed_at_utc"]},
            "probe_evidence": evidence}


def resource_preflight() -> dict[str, object]:
    observed_at = datetime.now(UTC).isoformat()
    host_free = shutil.disk_usage(ROOT).free
    try:
        info = checked_capture("info", "--format", "{{.MemTotal}}|{{.NCPU}}", timeout=12)
    except (TimeoutError, RuntimeError) as error:
        return {"classification": "DOCKER_ENGINE_UNHEALTHY", "budget_passed": False,
                "budget_blockers": [f"Docker Engine info is unavailable: {type(error).__name__}; check Docker Desktop/Engine health"],
                "diagnostics": {"docker_info": "unavailable", "error_type": type(error).__name__},
                "measurements": {"host_filesystem_free_bytes": host_free,
                                  "host_filesystem_observed_at_utc": observed_at}}
    try:
        engine_total_text, cpu_text = info.split("|")
        engine_total, cpus = int(engine_total_text), int(cpu_text)
        if engine_total <= 0 or cpus <= 0:
            raise ValueError("Docker info reported non-positive capacity")
    except (ValueError, TypeError):
        return {"classification": "PREFLIGHT_IMPLEMENTATION_ERROR", "budget_passed": False,
                "budget_blockers": ["Docker Engine info output was malformed; no isolated resources were created"],
                "diagnostics": {"docker_info": "malformed", "raw_value": info[:160]},
                "measurements": {"host_filesystem_free_bytes": host_free,
                                  "host_filesystem_observed_at_utc": observed_at}}

    measurements: dict[str, object] = {
        "docker_engine_memory_total_bytes": engine_total,
        "docker_engine_cpus": cpus,
        "docker_engine_observed_at_utc": observed_at,
        "docker_engine_source": "Docker Engine info (VM capacity, not available memory)",
        "host_filesystem_free_bytes": host_free,
        "host_filesystem_observed_at_utc": observed_at,
        "host_filesystem_source": "shutil.disk_usage on test runner filesystem",
    }
    hard_blockers = []
    if cpus < MIN_ENGINE_CPUS:
        hard_blockers.append("Docker VM has fewer than two CPUs")
    if engine_total < MIN_ENGINE_TOTAL_BYTES:
        hard_blockers.append("Docker VM has less than 4 GiB total memory")
    if host_free < MIN_HOST_DISK_BYTES:
        hard_blockers.append("Host filesystem has less than 2 GiB free")
    if hard_blockers:
        return {"classification": "INSUFFICIENT_CAPACITY", "budget_passed": False,
                "budget_blockers": hard_blockers, "measurements": measurements}

    sample = sample_docker_vm_memory(engine_total)
    measurements["docker_vm_memory_available"] = sample.get("memory_measurement")
    diagnostics = {"docker_vm_probe": sample.get("probe_evidence")}
    if sample.get("classification") != "CAPACITY_MEASURED":
        return {**sample, "measurements": measurements, "diagnostics": diagnostics}
    capacity = assess_capacity(engine_total, cpus, host_free,
                               [sample["memory_measurement"]])
    capacity["measurements"] = measurements
    capacity["diagnostics"] = diagnostics
    return capacity

def write_json(path: Path, payload: dict[str, object]) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary.chmod(0o600)
    temporary.replace(path)


def compose_command(project: str) -> list[str]:
    return [*DOCKER, "compose", "--project-name", project, "--file", str(COMPOSE_FILE)]


def sanitized_run(command: list[str], log_path: Path, secrets_to_redact: tuple[str, ...],
                  *, env: dict[str, str], timeout: int | None = None,
                  abort_event: threading.Event | None = None) -> tuple[int, str]:
    tail: deque[str] = deque(maxlen=80)
    timed_out = threading.Event()
    with log_path.open("w", encoding="utf-8") as log:
        process = subprocess.Popen(
            command, cwd=ROOT, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            text=True, encoding="utf-8", errors="replace", bufsize=1,
        )
        timer = None
        if timeout is not None:
            def stop_timed_out_process() -> None:
                if process.poll() is None:
                    timed_out.set()
                    process.kill()
            timer = threading.Timer(timeout, stop_timed_out_process)
            timer.daemon = True
            timer.start()
        abort_stop = threading.Event()
        abort_triggered = threading.Event()
        abort_watcher = None
        if abort_event is not None:
            def stop_on_resource_violation() -> None:
                while not abort_stop.wait(0.2):
                    if abort_event.is_set() and process.poll() is None:
                        abort_triggered.set()
                        process.kill()
                        return
            abort_watcher = threading.Thread(target=stop_on_resource_violation, daemon=True)
            abort_watcher.start()
        assert process.stdout is not None
        for line in process.stdout:
            safe = safe_text(line, secrets_to_redact)
            log.write(safe)
            log.flush()
            tail.append(safe)
        code = process.wait()
        abort_stop.set()
        if abort_watcher:
            abort_watcher.join(timeout=1)
        if timer:
            timer.cancel()
        if abort_triggered.is_set():
            raise RuntimeError("subprocess stopped because Docker VM available memory telemetry fell below the safe budget")
        if timed_out.is_set():
            raise TimeoutError("subprocess exceeded its time limit; full output is retained")
    return code, "".join(tail)


def resource_inventory(project: str) -> dict[str, list[str]]:
    result: dict[str, list[str]] = {}
    for kind, args in {
        "containers": ("ps", "-aq", "--filter", f"label=com.docker.compose.project={project}"),
        "volumes": ("volume", "ls", "-q", "--filter", f"label=com.docker.compose.project={project}"),
        "networks": ("network", "ls", "-q", "--filter", f"label=com.docker.compose.project={project}"),
        "images": ("image", "ls", "-q", "--filter", f"reference={project}-api-tests:isolated"),
    }.items():
        output = checked_capture(*args, timeout=40)
        result[kind] = [line for line in output.splitlines() if line]
    return result


def parse_pytest_summary(output: str) -> dict[str, int | None]:
    summary_lines = [line for line in output.splitlines() if re.search(
        r"\b(?:passed|failed|skipped|warnings?|errors?|xfailed|xpassed)\b", line, re.IGNORECASE
    )]
    summary: dict[str, int | None] = {key: 0 for key in ("passed", "failed", "skipped", "warnings", "errors")}
    for line in reversed(summary_lines):
        for count, label in re.findall(
            r"\b(\d+)\s+(passed|failed|skipped|warnings?|errors?)\b", line, re.IGNORECASE
        ):
            lowered = label.lower()
            key = "warnings" if lowered.startswith("warning") else "errors" if lowered.startswith("error") else lowered
            if key in summary:
                summary[key] = int(count)
        if any(value for key, value in summary.items() if key != "warnings") or "warning" in line.lower():
            summary["summary_line"] = line.strip()  # type: ignore[assignment]
            break
    if "summary_line" not in summary:
        summary["summary_line"] = None  # type: ignore[assignment]
    return summary


class ResourceMonitor:
    def __init__(self, project: str, postgres_container_id: str, output: Path):
        self.project = project
        self.postgres_container_id = postgres_container_id
        self.output = output
        self.stop_event = threading.Event()
        self.capacity_violation = threading.Event()
        self.first_sample_complete = threading.Event()
        self.thread = threading.Thread(target=self._run, name="isolated-pg-resource-monitor", daemon=True)

    def start(self) -> None:
        self.thread.start()

    def stop(self) -> None:
        self.stop_event.set()
        self.thread.join(timeout=15)

    def _observe(self) -> dict[str, object]:
        row: dict[str, object] = {"time_utc": datetime.now(UTC).isoformat(),
                                  "host_free_bytes": shutil.disk_usage(ROOT).free}
        containers = resource_inventory(self.project)["containers"]
        row["container_cpu_percent_and_memory"] = {}
        for container_id in containers:
            stats = checked_capture("stats", "--no-stream", "--format",
                                    "{{.CPUPerc}}|{{.MemUsage}}", container_id, timeout=15)
            row["container_cpu_percent_and_memory"][container_id] = stats  # type: ignore[index]
        row["postgres_data_disk"] = checked_capture(
            "exec", self.postgres_container_id, "sh", "-c",
            "df -Pk /var/lib/postgresql | tail -1; du -sk /var/lib/postgresql", timeout=15,
        )
        engine_total = int(checked_capture("info", "--format", "{{.MemTotal}}", timeout=12))
        sample = sample_docker_vm_memory(engine_total)
        row["docker_vm_memory_probe"] = sample.get("probe_evidence")
        if sample.get("classification") != "CAPACITY_MEASURED":
            row["safety_status"] = "telemetry_unavailable"
            self.capacity_violation.set()
        else:
            available = sample["memory_measurement"]["available_bytes"]  # type: ignore[index]
            row["docker_vm_memory_available_bytes"] = available
            row["safety_status"] = "within_budget" if available >= MIN_ENGINE_FREE_BYTES else "below_budget"
            if available < MIN_ENGINE_FREE_BYTES:
                self.capacity_violation.set()
        if int(row["host_free_bytes"]) < MIN_HOST_DISK_BYTES:
            row["safety_status"] = "host_disk_below_budget"
            self.capacity_violation.set()
        return row

    def _run(self) -> None:
        with self.output.open("a", encoding="utf-8") as log:
            while not self.stop_event.is_set():
                try:
                    row = self._observe()
                except Exception as error:
                    row = {"time_utc": datetime.now(UTC).isoformat(),
                           "observation_error": type(error).__name__,
                           "safety_status": "telemetry_unavailable"}
                    self.capacity_violation.set()
                log.write(json.dumps(row, sort_keys=True) + "\n")
                log.flush()
                self.first_sample_complete.set()
                self.stop_event.wait(30)


def main() -> int:
    run_id = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ") + "-" + uuid4().hex[:8]
    project = "ac-pgtest-" + uuid4().hex[:12]
    run_dir = EVIDENCE_ROOT / run_id
    run_dir.mkdir(parents=True, exist_ok=False)
    run_dir.chmod(0o700)
    manifest_path = run_dir / "run-manifest.json"
    manifest: dict[str, object] = {
        "run_id": run_id, "compose_project": project, "status": "incomplete",
        "started_at_utc": datetime.now(UTC).isoformat(), "commands": {},
        "test": {"executed": False, "exit_code": None, "warnings": []},
        "resources": {}, "cleanup": {"status": "not_started"},
        "network_isolation_note": "Separate PostgreSQL container/project limits database coupling, not Docker VM-level failure risk.",
    }
    write_json(manifest_path, manifest)
    owner = None
    monitor = None
    compose_env: dict[str, str] = {}
    secret_values: tuple[str, ...] = ()
    test_code: int | None = None
    setup_ok = False
    lock_stream = None
    lock_acquired = False
    compose_attempted = False
    return_code = 2
    try:
        LOCK_PATH.parent.mkdir(mode=0o700, exist_ok=True)
        lock_stream = LOCK_PATH.open("a")
        os.chmod(LOCK_PATH, 0o600)
        try:
            fcntl.flock(lock_stream, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            manifest["status"] = "blocked"
            manifest["blocker"] = "another isolated PostgreSQL regression run holds the lock"
            raise RuntimeError("another isolated PostgreSQL regression run holds the lock")
        lock_acquired = True

        try:
            preflight = resource_preflight()
            manifest["resources"]["preflight"] = preflight  # type: ignore[index]
        except Exception as error:
            manifest["status"] = "blocked"
            manifest["resource_classification"] = "PREFLIGHT_IMPLEMENTATION_ERROR"
            manifest["resources"]["preflight"] = {  # type: ignore[index]
                "classification": "PREFLIGHT_IMPLEMENTATION_ERROR",
                "budget_passed": False,
                "budget_blockers": ["Resource preflight raised unexpectedly; no isolated resources were created"],
                "error_type": type(error).__name__,
            }
            manifest["blocker"] = "Resource diagnostics unavailable due to a preflight implementation error"
            raise RuntimeError("Docker resource preflight could not be completed") from None
        if not preflight["budget_passed"]:
            manifest["status"] = "blocked"
            manifest["blocker"] = "; ".join(preflight["budget_blockers"])
            manifest["resource_classification"] = preflight.get("classification")
            raise RuntimeError("Docker capacity preflight blocked the isolated test run")
        require_capacity(preflight)

        admin_user = "ac_admin_" + uuid4().hex[:8]
        admin_password = uuid4().hex + uuid4().hex
        compose_env = {key: os.environ[key] for key in ("PATH", "HOME", "TMPDIR", "TEMP", "LANG", "LC_ALL",
                                                        "DOCKER_HOST", "DOCKER_CONTEXT", "DOCKER_CERT_PATH",
                                                        "DOCKER_TLS_VERIFY") if key in os.environ}
        isolated_image_tag = project + "-api-tests:isolated"
        compose_env["ISOLATED_TEST_IMAGE"] = isolated_image_tag
        compose_env.update(ISOLATED_PG_ADMIN_USER=admin_user, ISOLATED_PG_ADMIN_PASSWORD=admin_password)
        secret_values = (admin_password,)
        compose_base = compose_command(project)

        compose_attempted = True
        code, tail = capacity_guarded(preflight, lambda: sanitized_run(
            [*compose_base, "up", "-d", "--wait", "isolated-postgres"],
            run_dir / "postgres-start.log", secret_values, env=compose_env, timeout=90,
        ))
        manifest["commands"]["postgres_start"] = {"exit_code": code, "tail": tail}  # type: ignore[index]
        if code:
            try:
                failed_container = checked_capture(
                    "ps", "-aq", "--filter", f"label=com.docker.compose.project={project}",
                    "--filter", "label=com.docker.compose.service=isolated-postgres", timeout=10,
                )
                if failed_container:
                    failed_state = checked_capture("inspect", "--format", "{{json .State}}", failed_container, timeout=10)
                    (run_dir / "postgres-container-state.json").write_text(failed_state + "\n", encoding="utf-8")
                    manifest["commands"]["postgres_state"] = {"sanitized_state": "postgres-container-state.json"}  # type: ignore[index]
                    failed_config = checked_capture(
                        "inspect", "--format",
                        "{{json .Config.Entrypoint}}|{{json .Config.Cmd}}|{{json .Config.User}}|{{.Path}}|{{json .Args}}",
                        failed_container, timeout=10,
                    )
                    (run_dir / "postgres-container-command.json").write_text(failed_config + "\n", encoding="utf-8")
                    manifest["commands"]["postgres_command"] = {"sanitized_command": "postgres-container-command.json"}  # type: ignore[index]
                    env_output = checked_capture("inspect", "--format", "{{json .Config.Env}}", failed_container, timeout=10)
                    env_values = dict(item.split("=", 1) for item in json.loads(env_output) if "=" in item)
                    (run_dir / "postgres-container-env-summary.json").write_text(json.dumps({
                        "postgres_user_present": bool(env_values.get("POSTGRES_USER")),
                        "postgres_user_length": len(env_values.get("POSTGRES_USER", "")),
                        "postgres_password_present": bool(env_values.get("POSTGRES_PASSWORD")),
                        "postgres_password_length": len(env_values.get("POSTGRES_PASSWORD", "")),
                        "postgres_db": env_values.get("POSTGRES_DB"),
                        "environment_keys": sorted(env_values),
                    }, indent=2) + "\n", encoding="utf-8")
                    manifest["commands"]["postgres_env_summary"] = {"sanitized_summary": "postgres-container-env-summary.json"}  # type: ignore[index]
                    postgres_logs = checked_capture("logs", "--timestamps", failed_container, timeout=15)
                    postgres_logs = safe_text(postgres_logs, secret_values)
                    (run_dir / "postgres-container.log").write_text(postgres_logs + "\n", encoding="utf-8")
                    manifest["commands"]["postgres_logs"] = {"sanitized_log": "postgres-container.log"}  # type: ignore[index]
                else:
                    manifest["commands"]["postgres_logs"] = {"capture_error_type": "ContainerNotFound"}  # type: ignore[index]
            except Exception as error:
                manifest["commands"]["postgres_logs"] = {"capture_error_type": type(error).__name__}  # type: ignore[index]
            raise RuntimeError("isolated PostgreSQL failed to start")

        container_id = checked_capture(*compose_base[3:], "ps", "-q", "isolated-postgres", timeout=30,
                                       env=compose_env)
        if not container_id:
            raise RuntimeError("isolated Compose project did not report its PostgreSQL container")
        details = checked_capture("inspect", "--format",
                                  "{{index .Config.Labels \"com.docker.compose.project\"}} {{index .Config.Labels \"com.docker.compose.service\"}}",
                                  container_id)
        if details != f"{project} isolated-postgres":
            raise RuntimeError("isolated PostgreSQL container labels did not match the unique project")

        pg_disk = checked_capture("exec", container_id, "sh", "-c", "df -Pk /var/lib/postgresql | tail -1")
        disk_values = pg_disk.split()
        available_bytes = int(disk_values[3]) * 1024 if len(disk_values) >= 4 else 0
        manifest["resources"]["postgres_volume_before_tests"] = {
            "df_line": pg_disk, "available_bytes": available_bytes,
            "limits": {"memory": "512m", "memory_plus_swap": "768m", "cpus": 0.75, "pids": 96},
        }  # type: ignore[index]
        if available_bytes < MIN_DATABASE_DISK_BYTES:
            raise RuntimeError("Docker PostgreSQL volume has less than 1 GiB free")

        monitor = ResourceMonitor(project, container_id, run_dir / "resource-observations.jsonl")
        monitor.start()
        if not monitor.first_sample_complete.wait(20):
            raise RuntimeError("Docker resource monitor did not complete its initial safety sample")
        if monitor.capacity_violation.is_set():
            raise RuntimeError("Docker VM capacity fell below budget or became unmeasurable before build")

        database = "ac_pgtest_" + uuid4().hex[:16]
        role = database
        app_password = uuid4().hex + uuid4().hex
        admin_server_target = DatabaseTarget("isolated-postgres", 5432, "postgres", admin_user, admin_password)
        admin_target = DatabaseTarget("isolated-postgres", 5432, database, admin_user, admin_password)
        app_target = DatabaseTarget("isolated-postgres", 5432, database, role, app_password)
        admin_url = f"postgresql+psycopg://{admin_user}:{admin_password}@isolated-postgres:5432/postgres"
        migration_url = f"postgresql+psycopg://{admin_user}:{admin_password}@isolated-postgres:5432/{database}"
        app_url = f"postgresql+psycopg://{role}:{app_password}@isolated-postgres:5432/{database}"
        validate_target(admin_url, admin_server_target)
        validate_target(migration_url, admin_target)
        validate_target(app_url, app_target)
        secret_values = (admin_password, app_password)
        compose_env.update({
            "ISOLATED_TEST_DATABASE_URL": admin_url,
            "ISOLATED_TEST_MIGRATION_DATABASE_URL": admin_url,
            "ISOLATED_TEST_DATABASE_USER": admin_user,
            "ISOLATED_TEST_DATABASE_PASSWORD": admin_password,
        })
        create_target_code = database_provision_code(database, role, app_password)
        create_code, create_tail = sanitized_run(
            [*compose_base, "run", "--build", "--rm", "--no-deps", "-T", "api-tests",
             "/app/apps/api/.venv/bin/python", "-c", create_target_code],
            run_dir / "database-provision.log", secret_values, env=compose_env, timeout=300,
            abort_event=monitor.capacity_violation,
        )
        manifest["commands"]["database_provision"] = {"exit_code": create_code, "tail": create_tail}  # type: ignore[index]
        if create_code:
            raise RuntimeError("disposable database role/database provisioning failed")
        compose_env.update({
            "ISOLATED_TEST_DATABASE_URL": app_url,
            "ISOLATED_TEST_MIGRATION_DATABASE_URL": migration_url,
            "ISOLATED_TEST_DATABASE_USER": role,
            "ISOLATED_TEST_DATABASE_PASSWORD": app_password,
        })
        manifest["test_target"] = {"host": "isolated-postgres", "port": 5432,
                                   "database": database, "role": role,
                                   "admin_user": admin_user, "passwords_recorded": False,
                                   "host_port_published": False}
        manifest["resources"]["project_inventory_before_tests"] = resource_inventory(project)  # type: ignore[index]

        # The test container receives only generated DB credentials, dummy gateway
        # settings and an internal-only network. No host config/secrets are mounted.
        migration_code, migration_tail = sanitized_run(
            [*compose_base, "run", "--build", "--rm", "--no-deps", "-T", "api-tests",
             "/app/apps/api/.venv/bin/alembic", "-c", "apps/api/alembic.ini", "upgrade", "head"],
            run_dir / "migration.log", secret_values, env=compose_env, timeout=240,
            abort_event=monitor.capacity_violation,
        )
        manifest["commands"]["migration"] = {"exit_code": migration_code, "tail": migration_tail}  # type: ignore[index]
        if migration_code:
            test_code = migration_code
            raise RuntimeError("isolated Alembic migration failed")

        database_probe_script = database_probe_code(database, role)
        probe_code, probe_tail = sanitized_run(
            [*compose_base, "run", "--rm", "--no-deps", "-T", "api-tests",
             "/app/apps/api/.venv/bin/python", "-c", database_probe_script],
            run_dir / "database-probe.log", secret_values, env=compose_env, timeout=60,
            abort_event=monitor.capacity_violation,
        )
        manifest["commands"]["database_probe"] = {"exit_code": probe_code, "tail": probe_tail}  # type: ignore[index]
        if probe_code:
            raise RuntimeError("isolated database identity/privilege probe failed")
        manifest["database_probe"] = {"database": database, "role": role,
                                       "employee_versions_select": True,
                                       "connection_scope": "isolated Compose network only"}

        manifest["test"]["executed"] = True  # type: ignore[index]
        test_code, test_tail = sanitized_run(
            [*compose_base, "run", "--rm", "--no-deps", "-T", "api-tests",
             "/app/apps/api/.venv/bin/pytest", "apps/api/tests", "-q", "-rs", "-p", "no:cacheprovider"],
            run_dir / "api-tests.log", secret_values, env=compose_env, timeout=1800,
            abort_event=monitor.capacity_violation,
        )
        warning_lines = [line.strip() for line in (run_dir / "api-tests.log").read_text(encoding="utf-8").splitlines()
                         if re.search(r"\bwarning(?:s)?\b|PytestWarning|DeprecationWarning", line, re.IGNORECASE)]
        pytest_summary = parse_pytest_summary((run_dir / "api-tests.log").read_text(encoding="utf-8"))
        manifest["test"].update({"exit_code": test_code, "tail": test_tail,
                                 "summary": pytest_summary, "warning_lines": warning_lines,
                                 "warnings": pytest_summary.get("warnings", 0)})  # type: ignore[index,union-attr]
        setup_ok = True
        manifest["status"] = "passed" if test_code == 0 else "failed"
        return_code = test_code
    except Exception as error:
        manifest["failure"] = {"type": type(error).__name__, "message": str(error)}
        if manifest.get("status") != "blocked":
            manifest["status"] = "incomplete"
        return_code = test_code or 1
    finally:
        if monitor:
            monitor.stop()
        if compose_attempted:
            try:
                existing = resource_inventory(project)
                manifest["cleanup"]["resources_before"] = existing  # type: ignore[index]
                down_cmd = [*compose_command(project), "down", "--volumes", "--remove-orphans", "--timeout", "10"]
                down_code, down_tail = sanitized_run(
                    down_cmd, run_dir / "cleanup.log", secret_values, env=compose_env, timeout=90,
                )
                after_down = resource_inventory(project)
                image_remove_code = 0
                image_remove_tail = "not present"
                if not after_down["containers"] and after_down["images"]:
                    image_remove_code, image_remove_tail = sanitized_run(
                        docker_command("image", "rm", isolated_image_tag),
                        run_dir / "cleanup-image.log", secret_values, env=compose_env, timeout=60,
                    )
                remaining = resource_inventory(project)
                manifest["cleanup"].update({"command_exit_code": down_code, "tail": down_tail,
                                            "isolated_image_remove_exit_code": image_remove_code,
                                            "isolated_image_remove_tail": image_remove_tail,
                                            "resources_after": remaining,
                                            "status": "complete" if down_code == 0 and image_remove_code == 0 and not any(remaining.values()) else "incomplete"})  # type: ignore[index,union-attr]
                if down_code != 0 or image_remove_code != 0 or any(remaining.values()):
                    manifest["status"] = "incomplete"
                    return_code = 2
            except Exception as error:
                manifest["cleanup"].update({"status": "incomplete", "error_type": type(error).__name__,
                                            "message": str(error)})  # type: ignore[index,union-attr]
                manifest["status"] = "incomplete"
                return_code = 2
        else:
            manifest["cleanup"]["status"] = "not_needed"  # type: ignore[index]
        manifest["completed_at_utc"] = datetime.now(UTC).isoformat()
        manifest["infrastructure_and_tests_complete"] = bool(setup_ok and manifest["cleanup"].get("status") == "complete")  # type: ignore[index,union-attr]
        write_json(manifest_path, manifest)
        if lock_stream and lock_acquired:
            fcntl.flock(lock_stream, fcntl.LOCK_UN)
            lock_stream.close()

    print(f"Infrastructure Fix 08 test run {run_id}: {manifest['status']}")
    print(f"Sanitized evidence: {run_dir.relative_to(ROOT)}")
    return return_code


if __name__ == "__main__":
    raise SystemExit(main())
