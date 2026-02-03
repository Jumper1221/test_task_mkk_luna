"""add extension postgis

Revision ID: 1e9b2b7d8d79
Revises: 8da74957ed16
Create Date: 2026-02-02 15:44:03.869192

"""

from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "1e9b2b7d8d79"
down_revision: Union[str, Sequence[str], None] = "8da74957ed16"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("CREATE EXTENSION IF NOT EXISTS postgis")


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("DROP EXTENSION IF EXISTS postgis")
