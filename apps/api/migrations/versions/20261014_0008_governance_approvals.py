"""Add reviewable, scoped approval payloads and one-time decision receipts."""
from __future__ import annotations

import re

from alembic import op

from agent_corporation_api.settings import get_settings

revision = "20261014_0008"
down_revision = "20261009_0007"
branch_labels = None
depends_on = None


def upgrade() -> None:
    role = get_settings().app_database_user
    if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]{0,62}", role):
        raise RuntimeError("Invalid application role")
    quoted = op.get_bind().dialect.identifier_preparer.quote(role)
    op.execute("""
        ALTER TABLE approvals
          ADD COLUMN task_revision integer,
          ADD COLUMN action_payload jsonb NOT NULL DEFAULT '{}'::jsonb,
          ADD COLUMN budget_snapshot jsonb NOT NULL DEFAULT '{"cost_basis":"unknown"}'::jsonb,
          ADD COLUMN policy_snapshot_version integer,
          ADD COLUMN decided_at timestamptz,
          ADD COLUMN decision_reason text,
          ADD COLUMN decision_key uuid,
          ADD COLUMN decision_hash char(64);
        ALTER TABLE approvals ADD CONSTRAINT ck_approvals_payload_object
          CHECK (jsonb_typeof(action_payload) = 'object');
        ALTER TABLE approvals ADD CONSTRAINT ck_approvals_budget_object
          CHECK (jsonb_typeof(budget_snapshot) = 'object');
        ALTER TABLE approvals ADD CONSTRAINT ck_approvals_decision_hash
          CHECK (decision_hash IS NULL OR decision_hash ~ '^[0-9a-f]{64}$');
        ALTER TABLE approvals ADD CONSTRAINT fk_approvals_task_revision
          FOREIGN KEY (environment_id, company_id, task_id, task_revision)
          REFERENCES task_revisions(environment_id, company_id, task_id, revision) ON DELETE RESTRICT;
        CREATE INDEX ix_approvals_task_revision
          ON approvals(environment_id, company_id, task_id, task_revision);
        CREATE TABLE approval_decision_receipts (
          environment_id uuid NOT NULL,
          company_id uuid NOT NULL,
          idempotency_key uuid NOT NULL,
          approval_id uuid NOT NULL,
          request_hash char(64) NOT NULL CHECK (request_hash ~ '^[0-9a-f]{64}$'),
          response jsonb NOT NULL CHECK (jsonb_typeof(response) = 'object'),
          created_at timestamptz NOT NULL DEFAULT CURRENT_TIMESTAMP,
          PRIMARY KEY (environment_id, company_id, idempotency_key),
          FOREIGN KEY (environment_id, company_id, approval_id)
            REFERENCES approvals(environment_id, company_id, id) ON DELETE RESTRICT
        );
        CREATE TABLE approval_request_receipts (
          environment_id uuid NOT NULL,
          company_id uuid NOT NULL,
          idempotency_key uuid NOT NULL,
          approval_id uuid NOT NULL,
          request_hash char(64) NOT NULL CHECK (request_hash ~ '^[0-9a-f]{64}$'),
          created_at timestamptz NOT NULL DEFAULT CURRENT_TIMESTAMP,
          PRIMARY KEY (environment_id, company_id, idempotency_key),
          FOREIGN KEY (environment_id, company_id, approval_id)
            REFERENCES approvals(environment_id, company_id, id) ON DELETE RESTRICT
        );
    """)
    op.execute("ALTER TABLE approval_decision_receipts ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE approval_decision_receipts FORCE ROW LEVEL SECURITY")
    op.execute(f"""CREATE POLICY app_scope ON approval_decision_receipts TO {quoted}
        USING (environment_id = NULLIF(current_setting('app.environment_id', true), '')::uuid
           AND company_id = NULLIF(current_setting('app.company_id', true), '')::uuid)
        WITH CHECK (environment_id = NULLIF(current_setting('app.environment_id', true), '')::uuid
           AND company_id = NULLIF(current_setting('app.company_id', true), '')::uuid)""")
    op.execute("GRANT SELECT, INSERT ON approval_decision_receipts TO " + quoted)
    op.execute("ALTER TABLE approval_request_receipts ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE approval_request_receipts FORCE ROW LEVEL SECURITY")
    op.execute(f"""CREATE POLICY app_scope ON approval_request_receipts TO {quoted}
        USING (environment_id = NULLIF(current_setting('app.environment_id', true), '')::uuid
           AND company_id = NULLIF(current_setting('app.company_id', true), '')::uuid)
        WITH CHECK (environment_id = NULLIF(current_setting('app.environment_id', true), '')::uuid
           AND company_id = NULLIF(current_setting('app.company_id', true), '')::uuid)""")
    op.execute("GRANT SELECT, INSERT ON approval_request_receipts TO " + quoted)
    op.execute("GRANT UPDATE ON approvals TO " + quoted)


def downgrade() -> None:
    op.execute("DROP TABLE IF EXISTS approval_request_receipts, approval_decision_receipts")
    op.execute("DROP INDEX IF EXISTS ix_approvals_task_revision")
    op.execute("ALTER TABLE approvals DROP CONSTRAINT IF EXISTS fk_approvals_task_revision, DROP CONSTRAINT IF EXISTS ck_approvals_payload_object, DROP CONSTRAINT IF EXISTS ck_approvals_budget_object, DROP CONSTRAINT IF EXISTS ck_approvals_decision_hash")
    op.execute("ALTER TABLE approvals DROP COLUMN IF EXISTS decision_hash, DROP COLUMN IF EXISTS decision_key, DROP COLUMN IF EXISTS decision_reason, DROP COLUMN IF EXISTS decided_at, DROP COLUMN IF EXISTS policy_snapshot_version, DROP COLUMN IF EXISTS budget_snapshot, DROP COLUMN IF EXISTS action_payload, DROP COLUMN IF EXISTS task_revision")
