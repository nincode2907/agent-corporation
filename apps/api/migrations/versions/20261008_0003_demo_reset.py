"""Allow app role to reset only the fixed, release-locked demo scope.

Revision ID: 20261008_0003
Revises: 20261008_0002
"""

from __future__ import annotations

import re
from typing import Sequence

from alembic import op

from agent_corporation_api.settings import get_settings


revision: str = "20261008_0003"
down_revision: str | None = "20261008_0002"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

DEMO_ENVIRONMENT_ID = "b93f752e-7b69-5e8b-8f74-1498a15a5609"
DEMO_COMPANY_ID = "b4375333-b12b-5fca-b984-87864032d3a8"


def upgrade() -> None:
    app_role = get_settings().app_database_user
    if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]{0,62}", app_role):
        raise RuntimeError("APP_DATABASE_USER không hợp lệ")
    quoted_role = op.get_bind().dialect.identifier_preparer.quote(app_role)
    op.execute(f"""
        CREATE FUNCTION public.reset_agent_corporation_demo()
        RETURNS void
        LANGUAGE plpgsql
        SECURITY DEFINER
        SET search_path = pg_catalog, public
        AS $function$
        BEGIN
            IF session_user <> '{app_role}' THEN
                RAISE EXCEPTION 'demo reset is available only to the application role';
            END IF;
            IF NOT EXISTS (
                SELECT 1 FROM public.environments
                WHERE id = '{DEMO_ENVIRONMENT_ID}'::uuid
                  AND kind = 'demo' AND release_locked = true
            ) OR NOT EXISTS (
                SELECT 1 FROM public.companies
                WHERE id = '{DEMO_COMPANY_ID}'::uuid
                  AND environment_id = '{DEMO_ENVIRONMENT_ID}'::uuid
            ) THEN
                RAISE EXCEPTION 'fixed demo scope is not provisioned';
            END IF;

            DELETE FROM public.outbox_events WHERE environment_id = '{DEMO_ENVIRONMENT_ID}'::uuid AND company_id = '{DEMO_COMPANY_ID}'::uuid;
            DELETE FROM public.events WHERE environment_id = '{DEMO_ENVIRONMENT_ID}'::uuid AND company_id = '{DEMO_COMPANY_ID}'::uuid;
            DELETE FROM public.artifacts WHERE environment_id = '{DEMO_ENVIRONMENT_ID}'::uuid AND company_id = '{DEMO_COMPANY_ID}'::uuid;
            DELETE FROM public.approvals WHERE environment_id = '{DEMO_ENVIRONMENT_ID}'::uuid AND company_id = '{DEMO_COMPANY_ID}'::uuid;
            DELETE FROM public.checkpoints WHERE environment_id = '{DEMO_ENVIRONMENT_ID}'::uuid AND company_id = '{DEMO_COMPANY_ID}'::uuid;
            DELETE FROM public.run_execution_state WHERE environment_id = '{DEMO_ENVIRONMENT_ID}'::uuid AND company_id = '{DEMO_COMPANY_ID}'::uuid;
            DELETE FROM public.runs WHERE environment_id = '{DEMO_ENVIRONMENT_ID}'::uuid AND company_id = '{DEMO_COMPANY_ID}'::uuid;
            DELETE FROM public.task_execution_state WHERE environment_id = '{DEMO_ENVIRONMENT_ID}'::uuid AND company_id = '{DEMO_COMPANY_ID}'::uuid;
            DELETE FROM public.task_revisions WHERE environment_id = '{DEMO_ENVIRONMENT_ID}'::uuid AND company_id = '{DEMO_COMPANY_ID}'::uuid;
            DELETE FROM public.work_orders WHERE environment_id = '{DEMO_ENVIRONMENT_ID}'::uuid AND company_id = '{DEMO_COMPANY_ID}'::uuid;
            DELETE FROM public.event_stream_counters WHERE environment_id = '{DEMO_ENVIRONMENT_ID}'::uuid AND company_id = '{DEMO_COMPANY_ID}'::uuid;
            DELETE FROM public.policies WHERE environment_id = '{DEMO_ENVIRONMENT_ID}'::uuid AND company_id = '{DEMO_COMPANY_ID}'::uuid;
            DELETE FROM public.employee_versions WHERE environment_id = '{DEMO_ENVIRONMENT_ID}'::uuid AND company_id = '{DEMO_COMPANY_ID}'::uuid;
            DELETE FROM public.employees WHERE environment_id = '{DEMO_ENVIRONMENT_ID}'::uuid AND company_id = '{DEMO_COMPANY_ID}'::uuid;
            DELETE FROM public.departments WHERE environment_id = '{DEMO_ENVIRONMENT_ID}'::uuid AND company_id = '{DEMO_COMPANY_ID}'::uuid;
        END
        $function$
    """)
    op.execute("REVOKE ALL ON FUNCTION public.reset_agent_corporation_demo() FROM PUBLIC")
    op.execute("GRANT EXECUTE ON FUNCTION public.reset_agent_corporation_demo() TO " + quoted_role)


def downgrade() -> None:
    op.execute("REVOKE ALL ON FUNCTION public.reset_agent_corporation_demo() FROM PUBLIC")
    op.execute("DROP FUNCTION IF EXISTS public.reset_agent_corporation_demo()")
