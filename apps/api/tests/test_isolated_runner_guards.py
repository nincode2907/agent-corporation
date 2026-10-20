"""Fail-closed target checks for the disposable PostgreSQL regression runner."""
import importlib.util
from pathlib import Path
import sys
from datetime import UTC, datetime
from unittest.mock import patch

import pytest


def load_runner():
    path = Path(__file__).resolve().parents[3] / "scripts/test_playground_isolated.py"
    spec = importlib.util.spec_from_file_location("isolated_pg_runner", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_shared_runtime_database_url_is_rejected_before_connector_invocation():
    runner = load_runner()
    expected = runner.DatabaseTarget("127.0.0.1", 49152, "ac_pgtest_fixture", "ac_pgtest_fixture", "synthetic")
    called = False

    def connector(_url):
        nonlocal called
        called = True
        raise AssertionError("connector must never be called for a shared target")

    with pytest.raises(ValueError, match="shared database hostname"):
        runner.guarded_connect(
            "postgresql+psycopg://agent_corporation:synthetic@agent-corporation-postgres:5432/agent_corporation",
            expected,
            connector,
        )
    assert called is False


@pytest.mark.parametrize("url", [
    "postgresql+psycopg://fixture:synthetic@127.0.0.1:49152/agent_corporation",
    "postgresql+psycopg://wrong:synthetic@127.0.0.1:49152/ac_pgtest_fixture",
    "postgresql+psycopg://ac_pgtest_fixture:wrong@127.0.0.1:49152/ac_pgtest_fixture",
    "postgresql+psycopg://ac_pgtest_fixture:synthetic@127.0.0.1:15510/ac_pgtest_fixture",
])
def test_database_target_mismatch_is_rejected(url):
    runner = load_runner()
    expected = runner.DatabaseTarget("127.0.0.1", 49152, "ac_pgtest_fixture", "ac_pgtest_fixture", "synthetic")
    with pytest.raises(ValueError):
        runner.validate_target(url, expected)


def test_exact_generated_isolated_target_is_accepted():
    runner = load_runner()
    target = runner.DatabaseTarget("127.0.0.1", 49152, "ac_pgtest_fixture", "ac_pgtest_fixture", "synthetic")
    runner.validate_target("postgresql+psycopg://ac_pgtest_fixture:synthetic@127.0.0.1:49152/ac_pgtest_fixture", target)


def test_pytest_summary_counts_results_independently():
    result = load_runner().parse_pytest_summary("4 passed, 1 failed, 2 skipped, 1 warning in 3.5s")
    assert result["passed"] == 4
    assert result["failed"] == 1
    assert result["skipped"] == 2
    assert result["warnings"] == 1


def test_capacity_confirmed_requires_fresh_provenance_bearing_vm_measurement():
    runner = load_runner()
    now = datetime.now(UTC)
    result = runner.assess_capacity(
        5 * 1024**3, 4, 80 * 1024**3,
        [{"available_bytes": 3 * 1024**3, "source": "Docker VM memory.available", "scope": "docker-desktop-vm", "verified": True,
          "observed_at_utc": now.isoformat()}], now=now,
    )
    assert result["classification"] == "CAPACITY_CONFIRMED"
    assert result["budget_passed"] is True


def test_measured_insufficient_memory_is_denied():
    runner = load_runner()
    now = datetime.now(UTC)
    result = runner.assess_capacity(
        5 * 1024**3, 4, 80 * 1024**3,
        [{"available_bytes": 2 * 1024**3, "source": "Docker VM memory.available", "scope": "docker-desktop-vm", "verified": True,
          "observed_at_utc": now.isoformat()}], now=now,
    )
    assert result["classification"] == "INSUFFICIENT_CAPACITY"
    assert result["budget_passed"] is False


def test_vm_probe_timeout_is_telemetry_unavailable():
    runner = load_runner()
    with patch.object(runner, "checked_capture", return_value="5368709120|4"), \
         patch.object(runner, "sample_docker_vm_memory", return_value={
             "classification": "TELEMETRY_UNAVAILABLE", "budget_passed": False,
             "budget_blockers": ["probe timeout"], "probe_evidence": {"probe_error_type": "TimeoutError"},
         }), patch.object(runner.shutil, "disk_usage", return_value=type("Disk", (), {"free": 80 * 1024**3})()):
        result = runner.resource_preflight()
    assert result["classification"] == "TELEMETRY_UNAVAILABLE"
    assert result["budget_passed"] is False


def test_docker_engine_unavailable_is_distinct_from_stats_failure():
    runner = load_runner()
    with patch.object(runner, "checked_capture", side_effect=RuntimeError("daemon unavailable")), \
         patch.object(runner.shutil, "disk_usage", return_value=type("Disk", (), {"free": 80 * 1024**3})()):
        result = runner.resource_preflight()
    assert result["classification"] == "DOCKER_ENGINE_UNHEALTHY"


def test_malformed_or_partial_docker_stats_are_not_capacity_evidence():
    runner = load_runner()
    now = datetime.now(UTC)
    for sample in ([], [{"available_bytes": 1, "source": "", "scope": "container-cgroup", "verified": True,
                         "observed_at_utc": now.isoformat()}]):
        result = runner.assess_capacity(5 * 1024**3, 4, 80 * 1024**3, sample, now=now)
        assert result["classification"] == "TELEMETRY_UNAVAILABLE"
        assert result["budget_passed"] is False


def test_vm_probe_validates_vm_scope_and_confirms_cleanup():
    runner = load_runner()
    total = 8 * 1024**3
    probe_output = (
        "VM_MEMINFO_BEGIN\nMemTotal: 8388608 kB\nMemAvailable: 6682664 kB\n"
        "MemFree: 4703776 kB\nSwapTotal: 1048572 kB\nSwapFree: 1048572 kB\n"
        "VM_PRESSURE_BEGIN\n"
        "some avg10=0.00 avg60=0.00 avg300=0.00 total=0\n"
        "CGROUP_MEMORY_MAX_BEGIN\n67108864"
    )
    host_config = '{"Memory":67108864,"MemorySwap":67108864,"NanoCpus":250000000,"PidsLimit":16,"ReadonlyRootfs":true,"NetworkMode":"none","Binds":null}'
    with patch.object(runner, "checked_capture", side_effect=[
        runner.VM_PROBE_IMAGE, "probe-container-id", host_config, probe_output, "probe-container-id", "",
    ]) as command:
        sample = runner.sample_docker_vm_memory(total)
    assert sample["classification"] == "CAPACITY_MEASURED"
    assert sample["memory_measurement"]["available_bytes"] == 6682664 * 1024
    assert sample["memory_measurement"]["scope"] == "docker-desktop-vm"
    assert sample["probe_evidence"]["cleanup_verified"] is True
    assert command.call_count == 6


def test_resource_preflight_accepts_fresh_vm_available_measurement():
    runner = load_runner()
    now = datetime.now(UTC).isoformat()
    sample = {"classification": "CAPACITY_MEASURED", "budget_passed": False,
              "memory_measurement": {"available_bytes": 6 * 1024**3,
                                     "source": "Docker Desktop Linux VM /proc/meminfo MemAvailable",
                                     "scope": "docker-desktop-vm", "verified": True,
                                     "observed_at_utc": now},
              "probe_evidence": {"cleanup_verified": True}}
    with patch.object(runner, "checked_capture", return_value="8589934592|4"), \
         patch.object(runner, "sample_docker_vm_memory", return_value=sample), \
         patch.object(runner.shutil, "disk_usage", return_value=type("Disk", (), {"free": 80 * 1024**3})()):
        result = runner.resource_preflight()
    assert result["classification"] == "CAPACITY_CONFIRMED"
    assert result["budget_passed"] is True


def test_postgres18_test_volume_mount_matches_versioned_pgdata_parent():
    compose = (Path(__file__).resolve().parents[3] / "compose.test.yml").read_text()
    assert "test_pgdata:/var/lib/postgresql" in compose
    assert "test_pgdata:/var/lib/postgresql/data" not in compose
    assert "published:" not in compose


def test_isolated_database_provision_and_probe_scripts_compile_with_synthetic_targets():
    runner = load_runner()
    compile(runner.database_provision_code("ac_pgtest_fixture", "ac_pgtest_fixture", "synthetic-password"),
            "isolated-db-provision", "exec")
    compile(runner.database_probe_code("ac_pgtest_fixture", "ac_pgtest_fixture"),
            "isolated-db-probe", "exec")


def test_conflicting_fresh_memory_sources_block_capacity_confirmation():
    runner = load_runner()
    now = datetime.now(UTC)
    result = runner.assess_capacity(
        5 * 1024**3, 4, 80 * 1024**3,
        [{"available_bytes": 4 * 1024**3, "source": "Docker VM source A", "scope": "docker-desktop-vm", "verified": True, "observed_at_utc": now.isoformat()},
         {"available_bytes": 3 * 1024**3, "source": "Docker VM source B", "scope": "docker-desktop-vm", "verified": True, "observed_at_utc": now.isoformat()}],
        now=now,
    )
    assert result["classification"] == "TELEMETRY_UNAVAILABLE"
    assert result["budget_passed"] is False


def test_denied_preflight_never_invokes_resource_creation_action():
    runner = load_runner()
    resource_creation_attempts = []
    denied = {"classification": "TELEMETRY_UNAVAILABLE", "budget_passed": False}
    with pytest.raises(RuntimeError, match="capacity is not confirmed"):
        runner.capacity_guarded(denied, lambda: resource_creation_attempts.append("compose up"))
    assert resource_creation_attempts == []
