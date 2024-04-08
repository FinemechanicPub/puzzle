from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.crud.piece import piece_crud
from app.schemas.piece import Piece, PieceEntity


piece_router = APIRouter()


@piece_router.get(
    '/',
    response_model=list[PieceEntity],
    response_model_exclude_none=True,
)
async def list_pieces(session: AsyncSession = Depends(get_async_session)):
    pieces = await piece_crud.get_many(session)
    return pieces


@piece_router.post(
    '/',
    response_model=PieceEntity,
    response_model_exclude_none=True
)
async def create_piece(
    piece_data: Piece,
    session: AsyncSession = Depends(get_async_session)
):
    piece = await piece_crud.create_piece(piece_data, session, commit=True)
    return piece
