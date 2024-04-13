from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.crud.base import CRUDBase
from app.core.base import GamePieces, Game
from app.schemas.game import CreateGameRequest


class CRUDGame(CRUDBase):

    async def get(self, instance_id: int, session: AsyncSession):
        game = await session.get_one(
                Game,
                instance_id,
                options=[
                    joinedload(Game.game_pieces)
                    .selectinload(GamePieces.piece)
                ]
            )
        return game

    async def get_many(self, session: AsyncSession, ids: list[int] | None = None):
        games = await session.execute(
            select(Game)
            .options(
                joinedload(Game.game_pieces)
                .joinedload(GamePieces.piece)
            )
        )
        return games.unique().scalars()

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
            game_id = game.id
            game = await session.get_one(
                Game,
                game_id,
                options=[
                    joinedload(Game.game_pieces)
                    .selectinload(GamePieces.piece)
                ],
                populate_existing=True
            )
        return game


game_crud = CRUDGame(Game)
