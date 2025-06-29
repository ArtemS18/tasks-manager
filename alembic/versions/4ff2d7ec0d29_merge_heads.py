"""merge heads

Revision ID: 4ff2d7ec0d29
Revises: d59d55d415ef, 15159f2f976a
Create Date: 2025-06-28 17:57:57.789156

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4ff2d7ec0d29'
down_revision: Union[str, None] = ('d59d55d415ef', '15159f2f976a')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
