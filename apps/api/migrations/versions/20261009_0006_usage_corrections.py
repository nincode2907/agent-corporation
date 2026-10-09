"""Immutable adapter-sourced late usage; does not reactivate grants or unknown calls."""
from alembic import op
from agent_corporation_api.settings import get_settings
revision="20261009_0006"
down_revision="20261009_0005"
branch_labels=None
depends_on=None

def upgrade():
    op.execute("""CREATE TABLE runtime_usage_corrections (
        environment_id uuid NOT NULL, company_id uuid NOT NULL, request_span_id uuid NOT NULL,
        gateway_call_id uuid NOT NULL, usage jsonb NOT NULL CHECK(jsonb_typeof(usage)='object'),
        usage_hash char(64) NOT NULL, source text NOT NULL CHECK(source='gateway_final_response'),
        correction_reference text NOT NULL,
        recorded_at timestamptz NOT NULL DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY(environment_id,company_id,request_span_id),
        FOREIGN KEY(environment_id,company_id,request_span_id) REFERENCES model_calls(environment_id,company_id,id)
    ); ALTER TABLE runtime_usage_corrections ENABLE ROW LEVEL SECURITY;
    ALTER TABLE runtime_usage_corrections FORCE ROW LEVEL SECURITY;
    CREATE POLICY scoped_access ON runtime_usage_corrections USING (
        environment_id=nullif(current_setting('app.environment_id',true),'')::uuid AND
        company_id=nullif(current_setting('app.company_id',true),'')::uuid) WITH CHECK (
        environment_id=nullif(current_setting('app.environment_id',true),'')::uuid AND
        company_id=nullif(current_setting('app.company_id',true),'')::uuid)
    """)
    role=op.get_bind().dialect.identifier_preparer.quote(get_settings().app_database_user)
    op.execute("GRANT SELECT, INSERT ON runtime_usage_corrections TO "+role)

def downgrade():
    op.execute("DROP TABLE runtime_usage_corrections")
