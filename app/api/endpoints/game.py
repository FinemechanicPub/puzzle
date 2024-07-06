from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.crud.game import game_crud
from app.schemas.game import (
    CreateGameRequest, GameResponseBase, GameResponse, GameResponseLong
)


game_router = APIRouter()


@game_router.get(
        '/{game_id}/full/',
        response_model=GameResponseLong,
)
async def game_full(
    game_id: int, session: AsyncSession = Depends(get_async_session)
):
    game = await game_crud.get(game_id, session, load_rotations=True)
    if game is None:
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='404 - Not Found'
            )
    return game


@game_router.get(
    '/{game_id}/',
    response_model=GameResponse,
    response_model_exclude_none=True,
)
async def game(
    game_id: int, session: AsyncSession = Depends(get_async_session)
):
    game = await game_crud.get(game_id, session)
    return game


@game_router.get(
    '/',
    response_model=list[GameResponse],
    response_model_exclude_none=True,
)
async def list_games(session: AsyncSession = Depends(get_async_session)):
    games = await game_crud.get_many(session)
    return games


@game_router.post(
    '/',
    response_model=GameResponseBase,
    response_model_exclude_none=True,
)
async def create_game(
    game_data: CreateGameRequest,
    session: AsyncSession = Depends(get_async_session)
):
    game = await game_crud.create_game(
        game_data, session, commit=True
    )
    return game
