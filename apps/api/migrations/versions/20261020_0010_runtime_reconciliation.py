"""Append-only Owner reconciliation notes for uncertain Runtime calls."""
from alembic import op
from agent_corporation_api.settings import get_settings

revision = "20261020_0010"
down_revision = "20261014_0009"
branch_labels = None
depends_on = None


def upgrade():
    op.execute("""CREATE TABLE runtime_reconciliation_decisions (
      environment_id uuid NOT NULL, company_id uuid NOT NULL, id uuid NOT NULL,
      run_id uuid NOT NULL, request_span_id uuid NOT NULL, owner_id text NOT NULL,
      decision text NOT NULL CHECK(decision='unresolved_retained'),
      reason text NOT NULL CHECK(length(reason) BETWEEN 1 AND 500),
      idempotency_key uuid NOT NULL, request_hash char(64) NOT NULL,
      created_at timestamptz NOT NULL DEFAULT CURRENT_TIMESTAMP,
      PRIMARY KEY(environment_id,company_id,id),
      UNIQUE(environment_id,company_id,idempotency_key),
      FOREIGN KEY(environment_id,company_id,run_id) REFERENCES runtime_runs(environment_id,company_id,id),
      FOREIGN KEY(environment_id,company_id,request_span_id) REFERENCES model_calls(environment_id,company_id,id)
    )""")
    role = op.get_bind().dialect.identifier_preparer.quote(get_settings().app_database_user)
    op.execute("ALTER TABLE runtime_reconciliation_decisions ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE runtime_reconciliation_decisions FORCE ROW LEVEL SECURITY")
    op.execute("""CREATE POLICY scoped_access ON runtime_reconciliation_decisions
      USING (environment_id=nullif(current_setting('app.environment_id',true),'')::uuid AND company_id=nullif(current_setting('app.company_id',true),'')::uuid)
      WITH CHECK (environment_id=nullif(current_setting('app.environment_id',true),'')::uuid AND company_id=nullif(current_setting('app.company_id',true),'')::uuid)""")
    # The application role can append and read decisions, but cannot rewrite history.
    op.execute(f"GRANT SELECT, INSERT ON runtime_reconciliation_decisions TO {role}")


def downgrade():
    op.execute("DROP TABLE runtime_reconciliation_decisions")
