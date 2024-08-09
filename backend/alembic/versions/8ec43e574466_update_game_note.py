"""Update game note

Revision ID: 8ec43e574466
Revises: 14be3affd958
Create Date: 2024-08-10 01:00:21.784686

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8ec43e574466'
down_revision: Union[str, None] = '14be3affd958'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute("UPDATE game SET note='manage' || height || '.' || width || '.5' WHERE note='manage';")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute("UPDATE game SET note='manage' WHERE note LIKE 'manage%';")
    # ### end Alembic commands ###
