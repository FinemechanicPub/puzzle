from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends

from app.crud.game import game_crud
from app.core.db import get_async_session
from app.schemas.game import GameResponse

cover_router = APIRouter()


@cover_router.get('/suggestion', response_model=list[GameResponse])
async def suggestion(session: AsyncSession = Depends(get_async_session)):
    games = await game_crud.get_many(session)
    return games
