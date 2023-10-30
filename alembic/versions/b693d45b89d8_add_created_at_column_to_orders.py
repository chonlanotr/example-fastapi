"""add created at column to orders

Revision ID: b693d45b89d8
Revises: 1481fde65dd0
Create Date: 2023-10-28 06:25:15.497428

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b693d45b89d8'
down_revision: Union[str, None] = '1481fde65dd0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    
    op.add_column('orders', sa.Column('opened', sa.Boolean, nullable=False, server_default='TRUE'))
    op.add_column('orders', sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')))
    pass


def downgrade() -> None:
    op.drop_column('orders', 'opened')
    op.drop_column('orders', 'created_at')
    pass
