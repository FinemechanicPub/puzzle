from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.crud.game_crud import game_crud
from app.schemas.board import Board, BoardEntity


game_router = APIRouter()


@game_router.get(
    '/',
    response_model=list[BoardEntity],
    response_model_exclude_none=True,
)
async def list_games(session: AsyncSession = Depends(get_async_session)):
    games = await game_crud.get_many(session)
    return games


@game_router.post(
    '/',
    response_model=BoardEntity,
    response_model_exclude_none=True
)
async def create_game(
    game_data: Board,
    session: AsyncSession = Depends(get_async_session)
):
    game = await game_crud.create(game_data, session, commit=True)
    return game
