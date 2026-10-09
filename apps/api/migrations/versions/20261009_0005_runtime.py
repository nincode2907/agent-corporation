"""Durable bounded runtime, scoped grants and model call ledger."""
from alembic import op
from agent_corporation_api.settings import get_settings
revision = "20261009_0005"
down_revision = "20261009_0004"
branch_labels = None
depends_on = None
TABLES = ("inference_grants", "runtime_runs", "model_calls")

def upgrade():
    op.execute("""CREATE TABLE runtime_dispatch_guard (
        id integer PRIMARY KEY CHECK(id=1), request_span_id uuid, environment_id uuid, company_id uuid,
        CHECK((request_span_id IS NULL) = (environment_id IS NULL)),
        CHECK((request_span_id IS NULL) = (company_id IS NULL))
    ); INSERT INTO runtime_dispatch_guard(id) VALUES(1)""")
    op.execute("""CREATE TABLE inference_grants (
        environment_id uuid NOT NULL, company_id uuid NOT NULL, id uuid NOT NULL,
        phase text NOT NULL CHECK (phase IN ('06','07')), batch_id text NOT NULL,
        purpose text NOT NULL, model text NOT NULL, effort text NOT NULL,
        max_requests integer NOT NULL CHECK (max_requests BETWEEN 1 AND 10),
        used_requests integer NOT NULL DEFAULT 0 CHECK (used_requests >= 0 AND used_requests <= max_requests),
        max_concurrency integer NOT NULL CHECK (max_concurrency = 1),
        timeout_seconds integer NOT NULL CHECK (timeout_seconds BETWEEN 1 AND 120),
        max_requeues integer NOT NULL DEFAULT 0 CHECK (max_requeues BETWEEN 0 AND 2),
        expires_at timestamptz NOT NULL, revoked boolean NOT NULL DEFAULT false,
        owner_id text NOT NULL, created_at timestamptz NOT NULL DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY(environment_id,company_id,id),
        FOREIGN KEY(company_id,environment_id) REFERENCES companies(id,environment_id)
    )""")
    op.execute("""CREATE TABLE runtime_runs (
        environment_id uuid NOT NULL, company_id uuid NOT NULL, id uuid NOT NULL,
        task_id uuid NOT NULL, grant_id uuid NOT NULL, phase text NOT NULL, batch_id text NOT NULL,
        purpose text NOT NULL, model text NOT NULL, effort text NOT NULL, input_text text NOT NULL,
        idempotency_key uuid NOT NULL, request_hash char(64) NOT NULL,
        policy_snapshot jsonb NOT NULL, history jsonb NOT NULL,
        stop_requested boolean NOT NULL DEFAULT false, stop_epoch integer NOT NULL DEFAULT 0,
        available_at timestamptz NOT NULL DEFAULT CURRENT_TIMESTAMP,
        output text, artifact_id uuid, outcome text, usage jsonb,
        created_at timestamptz NOT NULL DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY(environment_id,company_id,id), UNIQUE(environment_id,company_id,idempotency_key),
        FOREIGN KEY(environment_id,company_id,id) REFERENCES runs(environment_id,company_id,id),
        FOREIGN KEY(environment_id,company_id,grant_id) REFERENCES inference_grants(environment_id,company_id,id),
        FOREIGN KEY(environment_id,company_id,artifact_id) REFERENCES artifacts(environment_id,company_id,id)
    )""")
    op.execute("""CREATE TABLE model_calls (
        environment_id uuid NOT NULL, company_id uuid NOT NULL, id uuid NOT NULL,
        run_id uuid NOT NULL, grant_id uuid NOT NULL, attempt integer NOT NULL CHECK(attempt BETWEEN 1 AND 3),
        status text NOT NULL CHECK(status IN ('dispatched','completed','failed','unknown','rate_limited')),
        gateway_call_id text, usage jsonb, usage_provenance text NOT NULL DEFAULT 'unknown',
        cost_basis text NOT NULL DEFAULT 'unknown' CHECK(cost_basis='unknown'),
        dispatched_at timestamptz NOT NULL DEFAULT CURRENT_TIMESTAMP, heartbeat_at timestamptz NOT NULL DEFAULT CURRENT_TIMESTAMP, lease_until timestamptz NOT NULL,
        finished_at timestamptz, reason text,
        PRIMARY KEY(environment_id,company_id,id), UNIQUE(environment_id,company_id,run_id,attempt),
        FOREIGN KEY(environment_id,company_id,run_id) REFERENCES runtime_runs(environment_id,company_id,id),
        FOREIGN KEY(environment_id,company_id,grant_id) REFERENCES inference_grants(environment_id,company_id,id)
    )""")
    op.execute("CREATE INDEX ix_runtime_dispatch ON runtime_runs(environment_id,company_id,available_at)")
    op.execute("CREATE INDEX ix_runtime_calls_active ON model_calls(environment_id,company_id,grant_id,lease_until) WHERE status='dispatched'")
    role = op.get_bind().dialect.identifier_preparer.quote(get_settings().app_database_user)
    op.execute("GRANT SELECT, UPDATE ON runtime_dispatch_guard TO " + role)
    for table in TABLES:
        op.execute(f"ALTER TABLE {table} ENABLE ROW LEVEL SECURITY")
        op.execute(f"ALTER TABLE {table} FORCE ROW LEVEL SECURITY")
        op.execute(f"CREATE POLICY scoped_access ON {table} USING (environment_id = nullif(current_setting('app.environment_id',true),'')::uuid AND company_id = nullif(current_setting('app.company_id',true),'')::uuid) WITH CHECK (environment_id = nullif(current_setting('app.environment_id',true),'')::uuid AND company_id = nullif(current_setting('app.company_id',true),'')::uuid)")
        op.execute(f"GRANT SELECT, INSERT, UPDATE ON {table} TO {role}")

def downgrade():
    op.execute("DROP TABLE runtime_dispatch_guard")
    for table in reversed(TABLES):
        op.execute(f"DROP TABLE {table}")
