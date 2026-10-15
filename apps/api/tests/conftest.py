"""Tests never start a worker against the configured local gateway."""
import pytest


@pytest.fixture(autouse=True)
def disable_live_playground_worker(monkeypatch):
    monkeypatch.setenv('PLAYGROUND_WORKER_ENABLED', 'false')
