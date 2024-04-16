from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.crud.base import CRUDBase
from app.core.base import GamePieces, Game, Piece
from app.schemas.game import CreateGameRequest


class CRUDGame(CRUDBase):

    selector = (select(Game).options(
            joinedload(Game.game_pieces).joinedload(GamePieces.piece)
        ))

    async def get(
            self, instance_id: int, session: AsyncSession, load_rotations=False
    ):
        if load_rotations:
            stmt = select(Game).options(
                joinedload(Game.game_pieces)
                .joinedload(GamePieces.piece)
                .joinedload(Piece.rotations)
            )
        else:
            stmt = self.selector
        game = await session.scalar(
            stmt.where(Game.id == instance_id)
        )
        return game

    async def get_many(
            self, session: AsyncSession, ids: list[int] | None = None
    ):
        games = await session.scalars(self.selector)
        return games.unique()

    async def create_game(
        self,
        data: CreateGameRequest,
        session: AsyncSession,
        commit: bool | None = True
    ):
        model_dict = data.model_dump()
        model_dict.pop('pieces')
        game = Game(**model_dict)
        for piece in data.pieces:
            game.game_pieces.append(
                GamePieces(game=game, piece_id=piece.id, color=piece.color)
            )
        session.add(game)
        if commit:
            await session.commit()
            await session.refresh(game)
        return game


game_crud = CRUDGame(Game)
