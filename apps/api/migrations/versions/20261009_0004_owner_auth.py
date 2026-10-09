"""Durable local Owner session and immutable audit-backed model profile baseline."""
import re
from alembic import op
from agent_corporation_api.settings import get_settings

revision = "20261009_0004"
down_revision = "20261008_0003"
branch_labels = None
depends_on = None


def upgrade():
    role = get_settings().app_database_user
    if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]{0,62}",role):
        raise RuntimeError("Invalid application role")
    quoted = op.get_bind().dialect.identifier_preparer.quote(role)
    op.execute("""CREATE TABLE owner_scopes (
        owner_id text NOT NULL CHECK(owner_id='owner-local'),environment_id uuid NOT NULL,company_id uuid NOT NULL,
        PRIMARY KEY(owner_id,environment_id,company_id));
        INSERT INTO owner_scopes VALUES ('owner-local','b93f752e-7b69-5e8b-8f74-1498a15a5609','b4375333-b12b-5fca-b984-87864032d3a8');
        CREATE TABLE owner_sessions (
        id uuid PRIMARY KEY,owner_id text NOT NULL,environment_id uuid NOT NULL,company_id uuid NOT NULL,
        token_hash text NOT NULL UNIQUE,csrf_hash text NOT NULL,
        created_at timestamptz NOT NULL DEFAULT CURRENT_TIMESTAMP,expires_at timestamptz NOT NULL,revoked_at timestamptz,
        FOREIGN KEY(owner_id,environment_id,company_id) REFERENCES owner_scopes);
        CREATE TABLE owner_model_profiles (
        environment_id uuid NOT NULL,company_id uuid NOT NULL,version integer NOT NULL CHECK(version>0),
        model text NOT NULL,reasoning_effort text NOT NULL,fallback_models jsonb NOT NULL DEFAULT '[]',
        updated_at timestamptz NOT NULL DEFAULT CURRENT_TIMESTAMP,PRIMARY KEY(environment_id,company_id),
        FOREIGN KEY(environment_id,company_id) REFERENCES companies(environment_id,id));
        ALTER TABLE owner_model_profiles ENABLE ROW LEVEL SECURITY;
        ALTER TABLE owner_model_profiles FORCE ROW LEVEL SECURITY;
        CREATE POLICY owner_profile_scope ON owner_model_profiles USING (
            environment_id=nullif(current_setting('app.environment_id',true),'')::uuid AND
            company_id=nullif(current_setting('app.company_id',true),'')::uuid) WITH CHECK (
            environment_id=nullif(current_setting('app.environment_id',true),'')::uuid AND
            company_id=nullif(current_setting('app.company_id',true),'')::uuid);
    """)
    op.execute("GRANT SELECT ON owner_scopes TO " + quoted)
    op.execute("GRANT SELECT,INSERT,UPDATE ON owner_sessions,owner_model_profiles TO " + quoted)


def downgrade():
    op.execute("DROP TABLE owner_model_profiles; DROP TABLE owner_sessions; DROP TABLE owner_scopes")
