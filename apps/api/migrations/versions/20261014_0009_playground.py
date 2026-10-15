"""Development Playground; isolated from Work Orders. Merge existing migration heads."""
from alembic import op
from agent_corporation_api.settings import get_settings

revision = "20261014_0009"
down_revision = ("20261011_0008", "20261014_0008")
branch_labels = None
depends_on = None


def upgrade():
    op.execute("""CREATE TABLE playground_sessions (
      environment_id uuid NOT NULL, company_id uuid NOT NULL, id uuid NOT NULL,
      owner_id text NOT NULL, owner_session_id uuid NOT NULL REFERENCES owner_sessions(id),
      creation_key uuid NOT NULL, request_hash text NOT NULL,
      employee_snapshot jsonb NOT NULL, profile_snapshot jsonb NOT NULL,
      policy_snapshot jsonb NOT NULL, accepted_at timestamptz NOT NULL DEFAULT CURRENT_TIMESTAMP,
      max_requests integer NOT NULL CHECK(max_requests BETWEEN 1 AND 100),
      used_requests integer NOT NULL DEFAULT 0 CHECK(used_requests BETWEEN 0 AND max_requests),
      max_concurrency integer NOT NULL DEFAULT 1 CHECK(max_concurrency=1),
      timeout_seconds integer NOT NULL CHECK(timeout_seconds BETWEEN 1 AND 120),
      expires_at timestamptz NOT NULL, revoked boolean NOT NULL DEFAULT false,
      created_at timestamptz NOT NULL DEFAULT CURRENT_TIMESTAMP,
      PRIMARY KEY(environment_id,company_id,id), UNIQUE(environment_id,company_id,creation_key),
      FOREIGN KEY(company_id,environment_id) REFERENCES companies(id,environment_id)
    );
    CREATE TABLE playground_turns (
      environment_id uuid NOT NULL, company_id uuid NOT NULL, id uuid NOT NULL, session_id uuid NOT NULL,
      idempotency_key uuid NOT NULL, request_hash text NOT NULL, input_text text NOT NULL,
      history jsonb NOT NULL, profile_snapshot jsonb NOT NULL, policy_snapshot jsonb NOT NULL,
      status text NOT NULL CHECK(status IN ('queued','dispatched','completed','failed','cancelled','unknown')),
      stop_requested boolean NOT NULL DEFAULT false, output text, outcome text, gateway_call_id text,
      usage jsonb, usage_provenance text NOT NULL DEFAULT 'unknown', cost_basis text NOT NULL DEFAULT 'unknown' CHECK(cost_basis='unknown'),
      created_at timestamptz NOT NULL DEFAULT CURRENT_TIMESTAMP, dispatched_at timestamptz,
      heartbeat_at timestamptz, lease_until timestamptz, finished_at timestamptz,
      resolved_at timestamptz,
      PRIMARY KEY(environment_id,company_id,id), UNIQUE(environment_id,company_id,session_id,idempotency_key),
      FOREIGN KEY(environment_id,company_id,session_id) REFERENCES playground_sessions(environment_id,company_id,id)
    );
    CREATE INDEX ix_playground_pending ON playground_turns(environment_id,company_id,status,created_at);
    CREATE UNIQUE INDEX ux_playground_one_pending ON playground_turns(environment_id,company_id,session_id) WHERE status IN ('queued','dispatched');
    """)
    role = op.get_bind().dialect.identifier_preparer.quote(get_settings().app_database_user)
    for table in ('playground_sessions', 'playground_turns'):
        op.execute(f"ALTER TABLE {table} ENABLE ROW LEVEL SECURITY")
        op.execute(f"ALTER TABLE {table} FORCE ROW LEVEL SECURITY")
        op.execute(f"""CREATE POLICY scoped_access ON {table}
          USING (environment_id=nullif(current_setting('app.environment_id',true),'')::uuid AND company_id=nullif(current_setting('app.company_id',true),'')::uuid)
          WITH CHECK (environment_id=nullif(current_setting('app.environment_id',true),'')::uuid AND company_id=nullif(current_setting('app.company_id',true),'')::uuid)""")
        op.execute(f"GRANT SELECT, INSERT, UPDATE ON {table} TO {role}")


def downgrade():
    op.execute('DROP TABLE playground_turns, playground_sessions')
