"""Add access token table

Revision ID: f7544c3ee252
Revises: 43a53c5959b0
Create Date: 2024-07-09 16:59:37.882847

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from fastapi_users_db_sqlalchemy.generics import TIMESTAMPAware


# revision identifiers, used by Alembic.
revision: str = 'f7544c3ee252'
down_revision: Union[str, None] = '43a53c5959b0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('accesstoken',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('token', sa.String(length=43), nullable=False),
    sa.Column('created_at', TIMESTAMPAware(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='cascade'),
    sa.PrimaryKeyConstraint('token')
    )
    op.create_index(op.f('ix_accesstoken_created_at'), 'accesstoken', ['created_at'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_accesstoken_created_at'), table_name='accesstoken')
    op.drop_table('accesstoken')
    # ### end Alembic commands ###
