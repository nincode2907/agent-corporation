"""Establish the empty Phase 01 schema baseline.

Revision ID: 20261008_0001
Revises:
Create Date: 2026-10-08
"""

from typing import Sequence

from alembic import op


revision: str = "20261008_0001"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Create no domain tables; Phase 03 owns the initial business schema."""


def downgrade() -> None:
    """The baseline contains no schema objects to remove."""
