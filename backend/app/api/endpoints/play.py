
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.exceptions import GameNotFoundException
from app.core.db import get_async_session
from app.schemas.hint import GameStatus, HintRequest, HintResponse
from app.services.play import (
    get_used_points, get_available_pieces, make_hint, merge_pieces
)
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
    used_pieces = tuple(
        (piece.piece_id, piece.rotation_id, piece.position)
        for piece in request.pieces
    )
    on_board = get_used_points(game.pieces, used_pieces)
    available_pieces = get_available_pieces(game.pieces, used_pieces)
    board = merge_pieces(game.height, game.width, on_board)
    if board.is_full():
        return HintResponse(status=GameStatus.complete, hint=None)
    piece_hint = make_hint(board, available_pieces)
    return HintResponse(
        status=GameStatus.progress if piece_hint else GameStatus.deadlock,
        hint=piece_hint
    )
