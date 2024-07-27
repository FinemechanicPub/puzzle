"""Added cascade to gamepieces

Revision ID: 8ff83205898f
Revises: 6b4a0e0c1564
Create Date: 2024-07-23 04:38:59.015212

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8ff83205898f'
down_revision: Union[str, None] = '6b4a0e0c1564'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    naming_convention = {
        "fk":
        "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    }
    engine_name = op.get_bind().engine.name
    with op.batch_alter_table('gamepieces', schema=None, naming_convention=naming_convention) as batch_op:
        if engine_name == "postgresql":
            batch_op.drop_constraint('gamepieces_game_id_fkey', type_='foreignkey')
            batch_op.drop_constraint('gamepieces_piece_id_fkey', type_='foreignkey')
        else:
            batch_op.drop_constraint('fk_gamepieces_piece_id_piece', type_='foreignkey')
            batch_op.drop_constraint('fk_gamepieces_game_id_game', type_='foreignkey')
        batch_op.create_foreign_key(batch_op.f('fk_gamepieces_piece_id_piece'), 'piece', ['piece_id'], ['id'], ondelete='CASCADE')
        batch_op.create_foreign_key(batch_op.f('fk_gamepieces_game_id_game'), 'game', ['game_id'], ['id'], ondelete='CASCADE')

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    engine_name = op.get_bind().engine.name
    with op.batch_alter_table('gamepieces', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('fk_gamepieces_game_id_game'), type_='foreignkey')
        batch_op.drop_constraint(batch_op.f('fk_gamepieces_piece_id_piece'), type_='foreignkey')
        if engine_name == "postgresql":
            batch_op.create_foreign_key('gamepieces_game_id_fkey', 'piece', ['piece_id'], ['id'])
            batch_op.create_foreign_key('gamepieces_game_id_fkey', 'game', ['game_id'], ['id'])
        else:
            batch_op.create_foreign_key(None, 'piece', ['piece_id'], ['id'])
            batch_op.create_foreign_key(None, 'game', ['game_id'], ['id'])

    # ### end Alembic commands ###
