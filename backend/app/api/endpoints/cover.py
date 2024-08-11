from enum import Enum
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends

from app.core.db import get_async_session
from app.repositories.game_repository import game_count_repository
from app.schemas.game import GameResponseBase

cover_router = APIRouter()


class Difficulty(int, Enum):
    easy = 5
    medium = 8
    hard = 12


@cover_router.get("/suggestion/", response_model=list[GameResponseBase])
async def suggestion(
    session: AsyncSession = Depends(get_async_session),
    difficulty: Difficulty = Difficulty.easy,
):
    games = await game_count_repository.list(
        session, offset=10, limit=10, random=True, piece_count=difficulty.value
    )
    return games
