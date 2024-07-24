from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends

from app.core.db import get_async_session
from app.repositories.game_repository import game_count_repository
from app.schemas.game import GameResponseBase

cover_router = APIRouter()


@cover_router.get('/suggestion/', response_model=list[GameResponseBase])
async def suggestion(
    session: AsyncSession = Depends(get_async_session), difficulty: str = ""
):
    piece_count = 8 if difficulty == "hard" else 5
    games = await game_count_repository.list(
        session, offset=10, limit=10, random=True, piece_count=piece_count
    )
    return games
