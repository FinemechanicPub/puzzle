"""add count column

Revision ID: 14be3affd958
Revises: 8ff83205898f
Create Date: 2024-07-29 22:29:35.591535

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '14be3affd958'
down_revision: Union[str, None] = '8ff83205898f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('gamepieces', sa.Column('count', sa.SmallInteger(), server_default='1', nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('gamepieces', 'count')
    # ### end Alembic commands ###
