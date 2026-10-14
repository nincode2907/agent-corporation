"""Add fenced leases to the durable Work Order queue.

Revision ID: 20261011_0008
Revises: 20261009_0007
"""
from __future__ import annotations

from typing import Sequence

from alembic import op

revision: str = "20261011_0008"
down_revision: str | None = "20261009_0007"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.execute("ALTER TABLE task_queue_entries DROP CONSTRAINT task_queue_entries_queue_status_check")
    op.execute("""ALTER TABLE task_queue_entries
        ADD CONSTRAINT task_queue_entries_queue_status_check
        CHECK (queue_status IN ('pending','leased','paused','completed','cancelled'))""")
    op.execute("""ALTER TABLE task_queue_entries
        ADD COLUMN lease_owner text,
        ADD COLUMN lease_token uuid,
        ADD COLUMN lease_until timestamptz,
        ADD COLUMN claim_count integer NOT NULL DEFAULT 0 CHECK (claim_count >= 0),
        ADD CONSTRAINT task_queue_lease_fields_consistent CHECK (
            (queue_status = 'leased' AND lease_owner IS NOT NULL AND lease_token IS NOT NULL AND lease_until IS NOT NULL)
            OR
            (queue_status <> 'leased' AND lease_owner IS NULL AND lease_token IS NULL AND lease_until IS NULL)
        ),
        ADD CONSTRAINT task_queue_lease_owner_valid CHECK (
            lease_owner IS NULL OR length(btrim(lease_owner)) BETWEEN 1 AND 120
        )""")
    op.execute("""CREATE INDEX ix_task_queue_active_leases ON task_queue_entries
        (environment_id, company_id, lease_until) WHERE queue_status='leased'""")
    # The existing app-scoped RLS policy and UPDATE grant cover the lease fields.


def downgrade() -> None:
    op.execute("""UPDATE task_queue_entries SET queue_status='pending',lease_owner=NULL,
        lease_token=NULL,lease_until=NULL WHERE queue_status='leased'""")
    op.execute("DROP INDEX IF EXISTS ix_task_queue_active_leases")
    op.execute("ALTER TABLE task_queue_entries DROP CONSTRAINT IF EXISTS task_queue_lease_owner_valid")
    op.execute("ALTER TABLE task_queue_entries DROP CONSTRAINT IF EXISTS task_queue_lease_fields_consistent")
    op.execute("ALTER TABLE task_queue_entries DROP COLUMN IF EXISTS claim_count")
    op.execute("ALTER TABLE task_queue_entries DROP COLUMN IF EXISTS lease_until")
    op.execute("ALTER TABLE task_queue_entries DROP COLUMN IF EXISTS lease_token")
    op.execute("ALTER TABLE task_queue_entries DROP COLUMN IF EXISTS lease_owner")
    op.execute("ALTER TABLE task_queue_entries DROP CONSTRAINT IF EXISTS task_queue_entries_queue_status_check")
    op.execute("""ALTER TABLE task_queue_entries
        ADD CONSTRAINT task_queue_entries_queue_status_check
        CHECK (queue_status IN ('pending','paused','completed','cancelled'))""")
