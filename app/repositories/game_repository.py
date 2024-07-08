from sqlalchemy.orm import joinedload

from app.models.game import Game, GamePieces, Piece
from .repository import RepositoryBase


class GameExtendedRepository(RepositoryBase):

    force_unique = True

    def selector(self):
        return super().selector().options(
            joinedload(Game.game_pieces).joinedload(GamePieces.piece).joinedload(Piece.rotations)
        )


game_repository = RepositoryBase(Game)
game_extended_repository = GameExtendedRepository(Game)
