"""add content column to orders table

Revision ID: 9468daeb953f
Revises: c88aa94e98df
Create Date: 2023-10-28 05:34:37.588971

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9468daeb953f'
down_revision: Union[str, None] = 'c88aa94e98df'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('orders', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('orders', 'content')
    pass
