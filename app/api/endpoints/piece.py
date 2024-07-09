from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.exceptions import PieceNotFoundException
from app.api.utility import OffsetLimit
from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.repositories.piece_repository import piece_repository
from app.schemas.piece import PieceBase, PieceGetResponse
from app.services.piece import create_piece_with_rotations


piece_router = APIRouter()


@piece_router.get('/piece_id/', response_model=PieceGetResponse, dependencies=[Depends(current_user)])
async def get_piece(piece_id: int, session: AsyncSession = Depends(get_async_session)):
    piece = await piece_repository.get(session, piece_id)
    if not piece:
        raise PieceNotFoundException
    return piece


@piece_router.get(
    '/',
    response_model=list[PieceGetResponse],
    response_model_exclude_none=True,
    dependencies=[Depends(current_user)],
)
async def list_pieces(session: AsyncSession = Depends(get_async_session), pagination: OffsetLimit = Depends()):
    pieces = await piece_repository.list(session, offset=pagination.offset, limit=pagination.limit)
    return pieces


@piece_router.post(
    '/',
    response_model=PieceGetResponse,
    response_model_exclude_none=True,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(current_superuser)],
)
async def create_piece(
    piece_data: PieceBase,
    session: AsyncSession = Depends(get_async_session),
):
    return await create_piece_with_rotations(session, piece_data)


@piece_router.delete('/piece_id/', status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(current_superuser)])
async def remove_piece(piece_id: int, session: AsyncSession = Depends(get_async_session)):
    piece = await piece_repository.get(session, piece_id)
    if not piece:
        raise PieceNotFoundException
    await piece_repository.remove(session, piece)
