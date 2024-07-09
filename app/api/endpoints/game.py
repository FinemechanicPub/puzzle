from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.exceptions import GameNotFoundException
from app.api.utility import OffsetLimit
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.repositories.game_repository import game_extended_repository, game_repository
from app.schemas.game import (
    CreateGameRequest, GameResponseBase, GameLongResponse
)


game_router = APIRouter()


@game_router.get(
        '/{game_id}/',
        response_model=GameLongResponse,
)
async def get_game(
    game_id: int, session: AsyncSession = Depends(get_async_session)
):
    game = await game_extended_repository.get(session, game_id)
    if not game:
        raise GameNotFoundException
    return game


@game_router.get(
    '/',
    response_model=list[GameResponseBase],
    response_model_exclude_none=True,
)
async def list_games(session: AsyncSession = Depends(get_async_session), pagination: OffsetLimit = Depends()):
    games = await game_repository.list(session, pagination.offset, pagination.limit)
    return games


@game_router.post(
    '/',
    response_model=GameResponseBase,
    response_model_exclude_none=True,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(current_superuser)],
)
async def create_game(
    data: CreateGameRequest,
    session: AsyncSession = Depends(get_async_session)
):
    return await game_repository.create(session, data)


@game_router.delete(
    '/{game_id}/',
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(current_superuser)],
)
async def remove_game(
    game_id: int, session: AsyncSession = Depends(get_async_session)
):
    game = await game_extended_repository.get(session, game_id)
    if not game:
        raise GameNotFoundException
    await game_extended_repository.remove(session, game)
    return
