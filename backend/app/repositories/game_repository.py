from sqlalchemy.orm import joinedload
from sqlalchemy.sql.expression import func

from app.models.game import Game, GamePieces, Piece
from .repository import RepositoryBase

piece_count = func.count(GamePieces.game_id).label("piece_count")


class GameCountRepository(RepositoryBase[Game]):

    def selector(self, piece_count):
        return (
            super()
            .selector()
            .join(GamePieces)
            .group_by(self.model.id)
            .having(func.count(GamePieces.game_id) == piece_count)
        )


class GameExtendedRepository(RepositoryBase[Game]):

    force_unique = True

    def selector(self):
        return (
            super()
            .selector()
            .options(
                joinedload(Game.game_pieces)
                .joinedload(GamePieces.piece)
                .joinedload(Piece.rotations)
            )
        )


game_repository = RepositoryBase(Game)
game_count_repository = GameCountRepository(Game)
game_extended_repository = GameExtendedRepository(Game)
