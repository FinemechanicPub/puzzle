
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.exceptions import GameNotFoundException
from app.core.db import get_async_session
from app.schemas.hint import GameStatus, HintRequest, HintResponse
from app.schemas.piece import PiecePlacement
from app.services.play import hint_move
from app.repositories.game_repository import game_extended_repository

play_router = APIRouter()


@play_router.put('/hint/', response_model=HintResponse)
async def hint(
    request: HintRequest,
    session: AsyncSession = Depends(get_async_session)
):
    game = await game_extended_repository.get(session, id=request.game_id)
    if not game:
        raise GameNotFoundException
    board_is_full, move = hint_move(
        game,
        tuple(
            (piece.piece_id, piece.rotation_id, piece.position)
            for piece in request.pieces
        )
    )
    if move:
        piece_id, rotation_id, position = move
        return HintResponse(
            status=GameStatus.progress,
            hint=PiecePlacement(
                piece_id=piece_id,
                rotation_id=rotation_id,
                position=position
            )
        )
    if board_is_full:
        return HintResponse(status=GameStatus.complete, hint=None)
    return HintResponse(status=GameStatus.deadlock, hint=None)
