from dataclasses import dataclass
from uuid import UUID

from sqlalchemy import text
from sqlalchemy.orm import Session


@dataclass(frozen=True)
class CompanyScope:
    environment_id: UUID
    company_id: UUID


def set_company_scope(session: Session, scope: CompanyScope) -> None:
    session.execute(
        text("SELECT set_config('app.environment_id', :value, true)"),
        {"value": str(scope.environment_id)},
    )
    session.execute(
        text("SELECT set_config('app.company_id', :value, true)"),
        {"value": str(scope.company_id)},
    )
