"""Write aggregate and metadata-fingerprint snapshots in a read-only transaction."""
from __future__ import annotations

from datetime import UTC, datetime
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "apps/api/src"))

from sqlalchemy import create_engine, text
from agent_corporation_api.settings import get_settings


SAFE_COLUMNS = {
    "events": ("event_id", "stream_seq", "event_type", "recorded_at", "run_id", "task_id"),
    "event_stream_counters": ("environment_id", "company_id", "last_seq"),
    "outbox_events": ("id", "event_id", "status", "attempts", "available_at"),
    "runtime_runs": ("id", "task_id", "grant_id", "stop_requested", "artifact_id", "created_at"),
    "run_execution_state": ("run_id", "status", "current_step"),
    "model_calls": ("id", "run_id", "status", "attempt", "lease_until"),
    "checkpoints": ("id", "run_id", "sequence", "boundary", "created_at"),
    "artifacts": ("id", "run_id", "mime_type", "size_bytes", "created_at"),
    "work_orders": ("id", "created_at"),
    "task_execution_state": ("task_id", "status", "transition_version"),
    "approvals": ("id", "status", "created_at", "consumed_at"),
    "playground_sessions": ("id", "used_requests", "revoked", "expires_at"),
    "playground_turns": ("id", "status", "outcome", "resolved_at"),
}


def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit("Usage: read_only_db_snapshot.py <output.json>")
    output = Path(sys.argv[1]).resolve()
    engine = create_engine(get_settings().migration_database_url or get_settings().database_url)
    snapshot = {"captured_at": datetime.now(UTC).isoformat(), "transaction": "READ ONLY", "tables": {}}
    try:
        with engine.connect() as connection:
            with connection.begin():
                connection.exec_driver_sql("SET TRANSACTION READ ONLY")
                for table, columns in SAFE_COLUMNS.items():
                    names = ", ".join(f'"{name}"' for name in columns)
                    rows = connection.execute(text(f'SELECT {names} FROM "{table}" ORDER BY 1')).all()
                    canonical = json.dumps([[None if value is None else str(value) for value in row] for row in rows],
                                           ensure_ascii=False, separators=(",", ":"))
                    snapshot["tables"][table] = {"row_count": len(rows), "metadata_sha256": hashlib.sha256(canonical.encode("utf-8")).hexdigest()}
    finally:
        engine.dispose()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(snapshot, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output), "table_count": len(snapshot["tables"]), "transaction": "READ ONLY"}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
