from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends

from app.core.db import get_async_session
from app.repositories.game_repository import game_repository
from app.schemas.game import GameResponseBase

cover_router = APIRouter()


@cover_router.get('/suggestion/', response_model=list[GameResponseBase])
async def suggestion(session: AsyncSession = Depends(get_async_session)):
    games = await game_repository.list(session, offset=0, limit=3)
    return games
