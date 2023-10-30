"""add foreign-key to orders table

Revision ID: 1481fde65dd0
Revises: 49ad38114680
Create Date: 2023-10-28 06:14:00.561246

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1481fde65dd0'
down_revision: Union[str, None] = '49ad38114680'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('orders', sa.Column('customer_id', sa.Integer(), nullable=False))
    op.create_foreign_key('orders_customer_fk', source_table="orders", referent_table="customers",
                          local_cols=['customer_id'], remote_cols=['id'], ondelete="CASCADE")
    pass


def downgrade() -> None:
    op.drop_constraint('orders_customer_fk', table_name="orders")
    op.drop_column('orders', 'customer_id')
    pass
