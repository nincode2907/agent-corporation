from functools import lru_cache

from sqlalchemy import Engine, create_engine, text
from sqlalchemy.orm import Session, sessionmaker

from .settings import get_settings


class DatabaseSchemaError(RuntimeError):
    """The database is reachable but does not provide the API's required schema."""


# These relations and columns are the API's minimum compatible schema contract.
# Keep the 0010 reconciliation table here so a pre-0010 database fails closed
# before the API or a worker can operate against it.
REQUIRED_SCHEMA_COLUMNS = {
    "employees": {"environment_id", "company_id", "id", "lifecycle"},
    "employee_versions": {"environment_id", "company_id", "id", "employee_id", "version"},
    "runs": {"environment_id", "company_id", "id", "employee_version_id"},
    "runtime_runs": {"environment_id", "company_id", "id"},
    "model_calls": {"environment_id", "company_id", "id", "run_id", "grant_id", "status"},
    "inference_grants": {"environment_id", "company_id", "id", "expires_at", "used_requests", "max_requests"},
    "runtime_dispatch_guard": {"id", "request_span_id"},
    "runtime_reconciliation_decisions": {
        "environment_id", "company_id", "id", "run_id", "request_span_id",
        "owner_id", "decision", "reason", "idempotency_key", "request_hash", "created_at",
    },
    "playground_sessions": {"environment_id", "company_id", "id", "used_requests", "max_requests"},
    "playground_turns": {"environment_id", "company_id", "id", "session_id", "status"},
}


def missing_schema_elements(actual: dict[str, set[str]]) -> list[str]:
    missing: list[str] = []
    for table, required_columns in REQUIRED_SCHEMA_COLUMNS.items():
        if table not in actual:
            missing.append(f"table:{table}")
            continue
        missing.extend(f"column:{table}.{column}" for column in sorted(required_columns - actual[table]))
    return missing


@lru_cache(maxsize=1)
def get_engine() -> Engine:
    return create_engine(get_settings().database_url, pool_pre_ping=True)


@lru_cache(maxsize=1)
def get_session_factory() -> sessionmaker[Session]:
    return sessionmaker(bind=get_engine(), expire_on_commit=False)


def database_is_ready() -> bool:
    with get_engine().connect() as connection:
        connection.execute(text("SELECT 1")).scalar_one()
        rows = connection.execute(text("""
            SELECT relation.relname, attribute.attname
            FROM pg_catalog.pg_class AS relation
            JOIN pg_catalog.pg_namespace AS schema ON schema.oid = relation.relnamespace
            JOIN pg_catalog.pg_attribute AS attribute ON attribute.attrelid = relation.oid
            WHERE schema.nspname = 'public'
              AND relation.relkind IN ('r', 'p')
              AND attribute.attnum > 0
              AND NOT attribute.attisdropped
              AND relation.relname = ANY(:tables)
        """), {"tables": list(REQUIRED_SCHEMA_COLUMNS)}).all()
    actual: dict[str, set[str]] = {}
    for table, column in rows:
        actual.setdefault(table, set()).add(column)
    missing = missing_schema_elements(actual)
    if missing:
        raise DatabaseSchemaError("database_schema_incompatible")
    return True
