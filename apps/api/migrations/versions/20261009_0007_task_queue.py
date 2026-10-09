"""Add scoped persistent task queue and immutable command receipts.

Revision ID: 20261009_0007
Revises: 20261009_0006
"""
from __future__ import annotations
from typing import Sequence
from alembic import op
from sqlalchemy import text
from agent_corporation_api.settings import get_settings

revision: str = "20261009_0007"
down_revision: str | None = "20261009_0006"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    app_role = get_settings().app_database_user
    quoted_role = op.get_bind().dialect.identifier_preparer.quote(app_role)
    op.execute("""
        CREATE TABLE task_queue_entries (
            environment_id uuid NOT NULL,
            company_id uuid NOT NULL,
            task_id uuid NOT NULL,
            priority integer NOT NULL DEFAULT 0 CHECK (priority BETWEEN -100 AND 100),
            queue_status text NOT NULL CHECK (queue_status IN ('pending','paused','completed','cancelled')),
            ready_at timestamptz NOT NULL DEFAULT CURRENT_TIMESTAMP,
            created_at timestamptz NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at timestamptz NOT NULL DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (environment_id, company_id, task_id),
            FOREIGN KEY (environment_id, company_id, task_id)
                REFERENCES work_orders(environment_id, company_id, id) ON DELETE RESTRICT
        )
    """)
    op.execute("""CREATE INDEX ix_task_queue_ready ON task_queue_entries
        (environment_id, company_id, queue_status, priority DESC, ready_at, created_at)""")
    op.execute("""
        CREATE TABLE task_command_receipts (
            environment_id uuid NOT NULL,
            company_id uuid NOT NULL,
            idempotency_key uuid NOT NULL,
            task_id uuid NOT NULL,
            payload_hash char(64) NOT NULL CHECK (payload_hash ~ '^[0-9a-f]{64}$'),
            response jsonb NOT NULL CHECK (jsonb_typeof(response) = 'object'),
            created_at timestamptz NOT NULL DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (environment_id, company_id, idempotency_key),
            FOREIGN KEY (environment_id, company_id, task_id)
                REFERENCES work_orders(environment_id, company_id, id) ON DELETE RESTRICT
        )
    """)
    for table in ("task_queue_entries", "task_command_receipts"):
        op.execute(f"ALTER TABLE {table} ENABLE ROW LEVEL SECURITY")
        op.execute(f"ALTER TABLE {table} FORCE ROW LEVEL SECURITY")
        op.execute(f"""CREATE POLICY app_scope ON {table} TO {quoted_role}
            USING (environment_id = NULLIF(current_setting('app.environment_id', true), '')::uuid
               AND company_id = NULLIF(current_setting('app.company_id', true), '')::uuid)
            WITH CHECK (environment_id = NULLIF(current_setting('app.environment_id', true), '')::uuid
               AND company_id = NULLIF(current_setting('app.company_id', true), '')::uuid)""")
    op.execute("GRANT SELECT, INSERT, UPDATE ON task_queue_entries TO " + quoted_role)
    op.execute("GRANT SELECT, INSERT ON task_command_receipts TO " + quoted_role)


def downgrade() -> None:
    for table in ("task_command_receipts", "task_queue_entries"):
        op.execute(f"DROP TABLE IF EXISTS {table} CASCADE")
