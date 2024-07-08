
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.exceptions import GameNotFoundException
from app.core.db import get_async_session
from app.crud.game import game_crud
from app.crud.piece import piece_crud
from app.schemas.hint import GameStatus, HintRequest, HintResponse
from app.services.play import make_hint, merge_pieces


play_router = APIRouter()


@play_router.put('/hint/', response_model=HintResponse)
async def hint(
    request: HintRequest,
    session: AsyncSession = Depends(get_async_session)
):
    game = await game_crud.get(request.game_id, session, False)
    if not game:
        raise GameNotFoundException

    request_map = {
        piece.rotation_id: piece.position for piece in request.pieces
    }
    rotations = await game_crud.valid_game_pieces(
        session, game.id, list(request_map)
    )
    available_piece_ids = list(
        set(game_piece.piece_id for game_piece in game.game_pieces)
        - set(rotation.piece_id for rotation in rotations)
    )
    available_pieces = await piece_crud.get_many(session, available_piece_ids)
    board = merge_pieces(
        game, [(rotation, request_map[rotation.id]) for rotation in rotations]
    )
    if board.is_full():
        return HintResponse(status=GameStatus.complete, hint=None)
    piece_hint = make_hint(board, available_pieces)
    return HintResponse(
        status=GameStatus.progress if piece_hint else GameStatus.deadlock,
        hint=piece_hint
    )
