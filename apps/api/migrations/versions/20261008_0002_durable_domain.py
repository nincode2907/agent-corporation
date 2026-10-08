"""Create scoped business, execution-state, event and outbox schema.

Revision ID: 20261008_0002
Revises: 20261008_0001
"""

from __future__ import annotations

import re
from typing import Sequence

from alembic import op
from psycopg import sql
from sqlalchemy import text

from agent_corporation_api.settings import get_settings


revision: str = "20261008_0002"
down_revision: str | None = "20261008_0001"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


COMPANY_TABLES = (
    "companies",
    "departments",
    "employees",
    "employee_versions",
    "policies",
    "work_orders",
    "task_revisions",
    "task_execution_state",
    "runs",
    "run_execution_state",
    "checkpoints",
    "approvals",
    "artifacts",
    "event_stream_counters",
    "events",
    "outbox_events",
)


def _ensure_app_role() -> None:
    settings = get_settings()
    username = settings.app_database_user
    if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]{0,62}", username):
        raise RuntimeError("APP_DATABASE_USER không hợp lệ")
    if not settings.app_database_password:
        raise RuntimeError("APP_DATABASE_PASSWORD chưa được cấu hình")
    connection = op.get_bind()
    exists = connection.execute(
        text("SELECT 1 FROM pg_roles WHERE rolname=:role"), {"role": username}
    ).scalar_one_or_none()
    raw = connection.connection.driver_connection
    role = sql.Identifier(username)
    password = sql.Literal(settings.app_database_password)
    statement = sql.SQL(
        "ALTER ROLE {} WITH LOGIN NOSUPERUSER NOCREATEDB NOCREATEROLE NOINHERIT "
        "NOREPLICATION NOBYPASSRLS PASSWORD {}" if exists else
        "CREATE ROLE {} WITH LOGIN NOSUPERUSER NOCREATEDB NOCREATEROLE NOINHERIT "
        "NOREPLICATION NOBYPASSRLS PASSWORD {}"
    ).format(role, password)
    raw.execute(statement)


def upgrade() -> None:
    _ensure_app_role()
    op.execute("""
        CREATE TABLE environments (
            id uuid PRIMARY KEY,
            name text NOT NULL CHECK (length(btrim(name)) BETWEEN 1 AND 120),
            kind text NOT NULL CHECK (kind IN ('demo', 'benchmark', 'real')),
            release_locked boolean NOT NULL DEFAULT true,
            created_at timestamptz NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
    """)
    op.execute("""
        CREATE TABLE companies (
            id uuid PRIMARY KEY,
            environment_id uuid NOT NULL REFERENCES environments(id) ON DELETE RESTRICT,
            name text NOT NULL CHECK (length(btrim(name)) BETWEEN 1 AND 160),
            mission text,
            created_at timestamptz NOT NULL DEFAULT CURRENT_TIMESTAMP,
            UNIQUE (id, environment_id),
            UNIQUE (environment_id, name)
        )
    """)
    op.execute("""
        CREATE TABLE departments (
            id uuid NOT NULL,
            environment_id uuid NOT NULL,
            company_id uuid NOT NULL,
            parent_department_id uuid,
            name text NOT NULL CHECK (length(btrim(name)) BETWEEN 1 AND 120),
            created_at timestamptz NOT NULL DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (environment_id, company_id, id),
            FOREIGN KEY (company_id, environment_id) REFERENCES companies(id, environment_id) ON DELETE RESTRICT,
            FOREIGN KEY (environment_id, company_id, parent_department_id)
                REFERENCES departments(environment_id, company_id, id) ON DELETE RESTRICT,
            CHECK (parent_department_id IS NULL OR parent_department_id <> id)
        )
    """)
    op.execute("""
        CREATE TABLE employees (
            id uuid NOT NULL,
            environment_id uuid NOT NULL,
            company_id uuid NOT NULL,
            department_id uuid,
            lifecycle text NOT NULL CHECK (lifecycle IN ('active', 'probation', 'draining', 'offboarded')),
            created_at timestamptz NOT NULL DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (environment_id, company_id, id),
            FOREIGN KEY (company_id, environment_id) REFERENCES companies(id, environment_id) ON DELETE RESTRICT,
            FOREIGN KEY (environment_id, company_id, department_id)
                REFERENCES departments(environment_id, company_id, id) ON DELETE RESTRICT
        )
    """)
    op.execute("""
        CREATE TABLE employee_versions (
            id uuid NOT NULL,
            environment_id uuid NOT NULL,
            company_id uuid NOT NULL,
            employee_id uuid NOT NULL,
            version integer NOT NULL CHECK (version > 0),
            profile jsonb NOT NULL CHECK (jsonb_typeof(profile) = 'object'),
            created_at timestamptz NOT NULL DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (environment_id, company_id, id),
            UNIQUE (environment_id, company_id, employee_id, version),
            FOREIGN KEY (environment_id, company_id, employee_id)
                REFERENCES employees(environment_id, company_id, id) ON DELETE RESTRICT
        )
    """)
    op.execute("""
        CREATE TABLE policies (
            id uuid NOT NULL,
            environment_id uuid NOT NULL,
            company_id uuid NOT NULL,
            version integer NOT NULL CHECK (version > 0),
            policy jsonb NOT NULL CHECK (jsonb_typeof(policy) = 'object'),
            created_by jsonb NOT NULL CHECK (jsonb_typeof(created_by) = 'object'),
            created_at timestamptz NOT NULL DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (environment_id, company_id, id),
            UNIQUE (environment_id, company_id, id, version),
            UNIQUE (environment_id, company_id, version),
            FOREIGN KEY (company_id, environment_id) REFERENCES companies(id, environment_id) ON DELETE RESTRICT
        )
    """)
    op.execute("""
        CREATE TABLE work_orders (
            id uuid NOT NULL,
            environment_id uuid NOT NULL,
            company_id uuid NOT NULL,
            created_by jsonb NOT NULL CHECK (jsonb_typeof(created_by) = 'object'),
            created_at timestamptz NOT NULL DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (environment_id, company_id, id),
            FOREIGN KEY (company_id, environment_id) REFERENCES companies(id, environment_id) ON DELETE RESTRICT
        )
    """)
    op.execute("""
        CREATE TABLE task_revisions (
            task_id uuid NOT NULL,
            environment_id uuid NOT NULL,
            company_id uuid NOT NULL,
            revision integer NOT NULL CHECK (revision > 0),
            goal text NOT NULL CHECK (length(btrim(goal)) > 0),
            expected_outputs jsonb NOT NULL CHECK (jsonb_typeof(expected_outputs) = 'array' AND jsonb_array_length(expected_outputs) > 0),
            acceptance_criteria jsonb NOT NULL CHECK (jsonb_typeof(acceptance_criteria) = 'array' AND jsonb_array_length(acceptance_criteria) > 0),
            scope jsonb NOT NULL DEFAULT '{}'::jsonb CHECK (jsonb_typeof(scope) = 'object'),
            deadline_at timestamptz,
            execution_grant_id uuid,
            budget_limits jsonb NOT NULL DEFAULT '{}'::jsonb CHECK (jsonb_typeof(budget_limits) = 'object'),
            stop_conditions jsonb NOT NULL DEFAULT '{}'::jsonb CHECK (jsonb_typeof(stop_conditions) = 'object'),
            assignee_id uuid,
            reviewer_id uuid,
            autonomy text NOT NULL CHECK (autonomy IN ('strict', 'supervised', 'delegated')),
            policy_id uuid,
            policy_version integer,
            created_by jsonb NOT NULL CHECK (jsonb_typeof(created_by) = 'object'),
            created_at timestamptz NOT NULL DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (environment_id, company_id, task_id, revision),
            FOREIGN KEY (environment_id, company_id, task_id)
                REFERENCES work_orders(environment_id, company_id, id) ON DELETE RESTRICT,
            FOREIGN KEY (environment_id, company_id, assignee_id)
                REFERENCES employees(environment_id, company_id, id) ON DELETE RESTRICT,
            FOREIGN KEY (environment_id, company_id, reviewer_id)
                REFERENCES employees(environment_id, company_id, id) ON DELETE RESTRICT,
            FOREIGN KEY (environment_id, company_id, policy_id, policy_version)
                REFERENCES policies(environment_id, company_id, id, version) ON DELETE RESTRICT,
            CHECK ((policy_id IS NULL) = (policy_version IS NULL))
        )
    """)
    op.execute("""
        CREATE TABLE task_execution_state (
            task_id uuid NOT NULL,
            environment_id uuid NOT NULL,
            company_id uuid NOT NULL,
            revision integer NOT NULL,
            status text NOT NULL CHECK (status IN ('draft','queued','planning','awaiting_approval','executing','reviewing','rework','awaiting_acceptance','accepted','blocked','paused','failed','cancelled')),
            resume_target text,
            transition_version integer NOT NULL DEFAULT 1 CHECK (transition_version > 0),
            updated_at timestamptz NOT NULL DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (environment_id, company_id, task_id),
            FOREIGN KEY (environment_id, company_id, task_id, revision)
                REFERENCES task_revisions(environment_id, company_id, task_id, revision) ON DELETE RESTRICT,
            CHECK ((status = 'paused') OR resume_target IS NULL)
        )
    """)
    op.execute("""
        CREATE TABLE runs (
            id uuid NOT NULL,
            environment_id uuid NOT NULL,
            company_id uuid NOT NULL,
            task_id uuid NOT NULL,
            task_revision integer NOT NULL,
            attempt integer NOT NULL CHECK (attempt > 0),
            employee_version_id uuid,
            profile_snapshot jsonb NOT NULL DEFAULT '{}'::jsonb CHECK (jsonb_typeof(profile_snapshot) = 'object'),
            created_at timestamptz NOT NULL DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (environment_id, company_id, id),
            UNIQUE (environment_id, company_id, task_id, attempt),
            FOREIGN KEY (environment_id, company_id, task_id, task_revision)
                REFERENCES task_revisions(environment_id, company_id, task_id, revision) ON DELETE RESTRICT,
            FOREIGN KEY (environment_id, company_id, employee_version_id)
                REFERENCES employee_versions(environment_id, company_id, id) ON DELETE RESTRICT
        )
    """)
    op.execute("""
        CREATE TABLE run_execution_state (
            run_id uuid NOT NULL,
            environment_id uuid NOT NULL,
            company_id uuid NOT NULL,
            status text NOT NULL CHECK (status IN ('queued','running','waiting_model','waiting_tool','waiting_approval','paused','interrupted','reconciling','completed','failed','cancelled')),
            transition_version integer NOT NULL DEFAULT 1 CHECK (transition_version > 0),
            current_step integer CHECK (current_step IS NULL OR current_step >= 0),
            updated_at timestamptz NOT NULL DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (environment_id, company_id, run_id),
            FOREIGN KEY (environment_id, company_id, run_id)
                REFERENCES runs(environment_id, company_id, id) ON DELETE RESTRICT
        )
    """)
    op.execute("""
        CREATE TABLE checkpoints (
            id uuid NOT NULL,
            environment_id uuid NOT NULL,
            company_id uuid NOT NULL,
            run_id uuid NOT NULL,
            sequence integer NOT NULL CHECK (sequence > 0),
            boundary text NOT NULL CHECK (length(btrim(boundary)) > 0),
            checkpoint jsonb NOT NULL CHECK (jsonb_typeof(checkpoint) = 'object'),
            created_at timestamptz NOT NULL DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (environment_id, company_id, id),
            UNIQUE (environment_id, company_id, run_id, sequence),
            FOREIGN KEY (environment_id, company_id, run_id)
                REFERENCES runs(environment_id, company_id, id) ON DELETE RESTRICT
        )
    """)
    op.execute("""
        CREATE TABLE approvals (
            id uuid NOT NULL,
            environment_id uuid NOT NULL,
            company_id uuid NOT NULL,
            task_id uuid NOT NULL,
            run_id uuid,
            policy_id uuid,
            policy_version integer,
            action_type text NOT NULL,
            payload_hash char(64) NOT NULL CHECK (payload_hash ~ '^[0-9a-f]{64}$'),
            summary text NOT NULL CHECK (length(btrim(summary)) > 0),
            status text NOT NULL CHECK (status IN ('pending','approved','rejected','expired','stale','consumed')),
            expires_at timestamptz,
            decided_by jsonb,
            created_at timestamptz NOT NULL DEFAULT CURRENT_TIMESTAMP,
            consumed_at timestamptz,
            PRIMARY KEY (environment_id, company_id, id),
            FOREIGN KEY (environment_id, company_id, task_id)
                REFERENCES work_orders(environment_id, company_id, id) ON DELETE RESTRICT,
            FOREIGN KEY (environment_id, company_id, run_id)
                REFERENCES runs(environment_id, company_id, id) ON DELETE RESTRICT,
            FOREIGN KEY (environment_id, company_id, policy_id, policy_version)
                REFERENCES policies(environment_id, company_id, id, version) ON DELETE RESTRICT,
            CHECK ((policy_id IS NULL) = (policy_version IS NULL)),
            CHECK ((status = 'consumed') = (consumed_at IS NOT NULL))
        )
    """)
    op.execute("""
        CREATE TABLE artifacts (
            id uuid NOT NULL,
            environment_id uuid NOT NULL,
            company_id uuid NOT NULL,
            task_id uuid,
            run_id uuid,
            storage_key text NOT NULL CHECK (storage_key !~ '(^/|(^|/)\\.\\.(/|$)|\\\\)'),
            sha256 char(64) NOT NULL CHECK (sha256 ~ '^[0-9a-f]{64}$'),
            mime_type text NOT NULL,
            size_bytes bigint NOT NULL CHECK (size_bytes >= 0),
            sensitivity text NOT NULL CHECK (sensitivity IN ('public','internal','confidential')),
            created_at timestamptz NOT NULL DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (environment_id, company_id, id),
            FOREIGN KEY (environment_id, company_id, task_id)
                REFERENCES work_orders(environment_id, company_id, id) ON DELETE RESTRICT,
            FOREIGN KEY (environment_id, company_id, run_id)
                REFERENCES runs(environment_id, company_id, id) ON DELETE RESTRICT,
            CHECK (task_id IS NOT NULL OR run_id IS NOT NULL)
        )
    """)
    op.execute("""
        CREATE TABLE event_stream_counters (
            environment_id uuid NOT NULL,
            company_id uuid NOT NULL,
            last_seq bigint NOT NULL DEFAULT 0 CHECK (last_seq >= 0),
            PRIMARY KEY (environment_id, company_id),
            FOREIGN KEY (company_id, environment_id) REFERENCES companies(id, environment_id) ON DELETE RESTRICT
        )
    """)
    op.execute("""
        CREATE TABLE events (
            event_id uuid PRIMARY KEY,
            environment_id uuid NOT NULL,
            company_id uuid NOT NULL,
            schema_version integer NOT NULL CHECK (schema_version = 1),
            event_type text NOT NULL CHECK (length(btrim(event_type)) > 0),
            stream_seq bigint NOT NULL CHECK (stream_seq > 0),
            occurred_at timestamptz NOT NULL,
            recorded_at timestamptz NOT NULL DEFAULT CURRENT_TIMESTAMP,
            task_id uuid,
            run_id uuid,
            agent_id uuid,
            employee_version_id uuid,
            correlation_id uuid NOT NULL,
            parent_event_id uuid,
            source text NOT NULL CHECK (source IN ('app','gateway_adapter','executor')),
            actor jsonb NOT NULL CHECK (jsonb_typeof(actor) = 'object'),
            sensitivity text NOT NULL CHECK (sensitivity IN ('public','internal','confidential')),
            payload jsonb NOT NULL CHECK (jsonb_typeof(payload) = 'object'),
            evidence_refs jsonb NOT NULL DEFAULT '[]'::jsonb CHECK (jsonb_typeof(evidence_refs) = 'array'),
            dedup_key text NOT NULL CHECK (length(btrim(dedup_key)) BETWEEN 1 AND 240),
            UNIQUE (environment_id, company_id, stream_seq),
            UNIQUE (environment_id, company_id, dedup_key),
            UNIQUE (event_id, environment_id, company_id),
            FOREIGN KEY (company_id, environment_id) REFERENCES companies(id, environment_id) ON DELETE RESTRICT,
            FOREIGN KEY (environment_id, company_id, task_id) REFERENCES work_orders(environment_id, company_id, id) ON DELETE RESTRICT,
            FOREIGN KEY (environment_id, company_id, run_id) REFERENCES runs(environment_id, company_id, id) ON DELETE RESTRICT,
            FOREIGN KEY (environment_id, company_id, employee_version_id) REFERENCES employee_versions(environment_id, company_id, id) ON DELETE RESTRICT,
            FOREIGN KEY (parent_event_id, environment_id, company_id) REFERENCES events(event_id, environment_id, company_id) ON DELETE RESTRICT,
            CHECK (run_id IS NULL OR task_id IS NOT NULL)
        )
    """)
    op.execute("""
        CREATE TABLE outbox_events (
            id uuid PRIMARY KEY,
            event_id uuid NOT NULL UNIQUE,
            environment_id uuid NOT NULL,
            company_id uuid NOT NULL,
            topic text NOT NULL,
            status text NOT NULL CHECK (status IN ('pending','published','dead')),
            available_at timestamptz NOT NULL,
            published_at timestamptz,
            attempts integer NOT NULL DEFAULT 0 CHECK (attempts >= 0),
            last_error text,
            created_at timestamptz NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (event_id, environment_id, company_id)
                REFERENCES events(event_id, environment_id, company_id) ON DELETE RESTRICT,
            CHECK ((status = 'published') = (published_at IS NOT NULL))
        )
    """)

    op.execute("CREATE INDEX ix_companies_environment ON companies(environment_id, created_at)")
    op.execute("CREATE INDEX ix_departments_parent ON departments(environment_id, company_id, parent_department_id)")
    op.execute("CREATE INDEX ix_employees_lifecycle ON employees(environment_id, company_id, lifecycle, created_at)")
    op.execute("CREATE INDEX ix_work_orders_recent ON work_orders(environment_id, company_id, created_at DESC)")
    op.execute("CREATE INDEX ix_task_state_status ON task_execution_state(environment_id, company_id, status, updated_at DESC)")
    op.execute("CREATE INDEX ix_runs_task ON runs(environment_id, company_id, task_id, attempt DESC)")
    op.execute("CREATE INDEX ix_run_state_status ON run_execution_state(environment_id, company_id, status, updated_at DESC)")
    op.execute("CREATE INDEX ix_approvals_pending ON approvals(environment_id, company_id, expires_at) WHERE status = 'pending'")
    op.execute("CREATE INDEX ix_artifacts_task_run ON artifacts(environment_id, company_id, task_id, run_id)")
    op.execute("CREATE INDEX ix_events_task_seq ON events(environment_id, company_id, task_id, stream_seq)")
    op.execute("CREATE INDEX ix_events_run_seq ON events(environment_id, company_id, run_id, stream_seq)")
    op.execute("CREATE INDEX ix_outbox_ready ON outbox_events(status, available_at, id) WHERE status = 'pending'")

    app_role = get_settings().app_database_user
    quoted_role = op.get_bind().dialect.identifier_preparer.quote(app_role)
    op.execute("GRANT USAGE ON SCHEMA public TO " + quoted_role)
    op.execute("GRANT SELECT ON environments TO " + quoted_role)
    op.execute("GRANT SELECT ON companies TO " + quoted_role)
    for table in (
        "departments", "employees", "employee_versions", "policies", "work_orders",
        "task_revisions", "task_execution_state", "runs", "run_execution_state",
        "checkpoints", "approvals", "artifacts", "event_stream_counters", "events", "outbox_events",
    ):
        op.execute("GRANT SELECT ON " + table + " TO " + quoted_role)
    for table in ("departments", "employees", "employee_versions", "policies", "work_orders", "task_revisions", "task_execution_state", "runs", "run_execution_state", "checkpoints", "approvals", "artifacts", "event_stream_counters", "events", "outbox_events"):
        op.execute("GRANT INSERT ON " + table + " TO " + quoted_role)
    for table in ("employees", "task_execution_state", "run_execution_state", "approvals", "event_stream_counters", "outbox_events"):
        op.execute("GRANT UPDATE ON " + table + " TO " + quoted_role)

    env_setting = "NULLIF(current_setting('app.environment_id', true), '')::uuid"
    company_setting = "NULLIF(current_setting('app.company_id', true), '')::uuid"
    op.execute(f"ALTER TABLE environments ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE environments FORCE ROW LEVEL SECURITY")
    op.execute(
        f"CREATE POLICY app_scope ON environments TO {quoted_role} "
        f"USING (id = {env_setting}) WITH CHECK (id = {env_setting})"
    )
    for table in COMPANY_TABLES:
        op.execute(f"ALTER TABLE {table} ENABLE ROW LEVEL SECURITY")
        op.execute(f"ALTER TABLE {table} FORCE ROW LEVEL SECURITY")
        row_scope = f"environment_id = {env_setting} AND id = {company_setting}" if table == "companies" else f"environment_id = {env_setting} AND company_id = {company_setting}"
        op.execute(
            f"CREATE POLICY app_scope ON {table} TO {quoted_role} "
            f"USING ({row_scope}) WITH CHECK ({row_scope})"
        )


def downgrade() -> None:
    for table in reversed(("environments", *COMPANY_TABLES)):
        op.execute(f"DROP TABLE IF EXISTS {table} CASCADE")
    app_role = get_settings().app_database_user
    quoted_role = op.get_bind().dialect.identifier_preparer.quote(app_role)
    op.execute("REVOKE ALL PRIVILEGES ON SCHEMA public FROM " + quoted_role)
    op.execute("DROP ROLE IF EXISTS " + quoted_role)
