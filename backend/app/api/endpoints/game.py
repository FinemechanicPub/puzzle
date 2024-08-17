from io import BytesIO

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.exceptions import GameNotFoundException
from app.api.utility import GameParameters, OffsetLimit
from app.core.db import get_async_session
from app.core.user import superuser
from app.repositories.game_repository import (
    game_extended_repository,
    game_repository,
)
from app.schemas.game import (
    CreateGameRequest,
    GameResponseBase,
    GameLongResponse,
)
from app.services.image import Piece, thumbnail
from app.models.game import Game
from engine.board import Board


router = APIRouter(prefix="/games", tags=["Games"])


@router.get(
    "/{game_id}/",
    response_model=GameLongResponse,
)
async def get_game(
    game_id: int, session: AsyncSession = Depends(get_async_session)
):
    game = await game_extended_repository.get(session, game_id)
    if not game:
        raise GameNotFoundException
    return game


@router.get(
    "/",
    response_model=list[GameResponseBase],
    response_model_exclude_none=True,
)
async def list_games(
    session: AsyncSession = Depends(get_async_session),
    pagination: OffsetLimit = Depends(),
    game_parameters: GameParameters = Depends(),
    shuffle: bool = False,
):
    games = await game_repository.list(
        session,
        pagination.offset,
        pagination.limit,
        clause=(
            Game.height == game_parameters.height,
            Game.width == game_parameters.width,
        ),
        random=shuffle,
    )
    return games


@router.post(
    "/",
    response_model=GameResponseBase,
    response_model_exclude_none=True,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(superuser)],
)
async def create_game(
    data: CreateGameRequest, session: AsyncSession = Depends(get_async_session)
):
    return await game_repository.create(session, data)


@router.delete(
    "/{game_id}/",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(superuser)],
)
async def remove_game(
    game_id: int, session: AsyncSession = Depends(get_async_session)
):
    game = await game_extended_repository.get(session, game_id)
    if not game:
        raise GameNotFoundException
    await game_extended_repository.remove(session, game)
    return


@router.get(
    "/{game_id}/thumbnail/",
    responses={
        200: {"content": {"image/png": {}}},
        404: {"description": "Game not found"},
    },
    response_class=Response,
)
async def game_thumbnail(
    game_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    game = await game_extended_repository.get(session, game_id)
    if not game:
        raise GameNotFoundException
    image = thumbnail(
        Board(game.height, game.width),
        (
            Piece(
                game_piece.points, game_piece.color or game_piece.default_color
            )
            for game_piece in game.game_pieces
        ),
    )
    with BytesIO() as data:
        image.save(data, "png")
        return Response(
            content=data.getvalue(),
            media_type="image/png",
            headers={"Cache-Control": "max-age=604800"},
        )
