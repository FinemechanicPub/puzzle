import logging
from random import choice
from timeit import default_timer
from typing import Sequence

from app.models.game import Game, Piece, PieceRotation
from app.schemas.piece import PiecePlacement
from engine.board import Board, invert
from engine.solver import solutions

logger = logging.getLogger(__name__)


def merge_pieces(
    game: Game,
    piece_positions: Sequence[tuple[PieceRotation, int]]
) -> Board:
    board = Board(game.height, game.width)
    for rotation, position in piece_positions:
        board.merge_piece(rotation.points, position)
    return board


def make_hint(
        board: Board,
        pieces: Sequence[Piece]
) -> PiecePlacement | None:

    piece_set = tuple(
        invert(tuple(
            board.piece_masks(rotation.points)
            for rotation in piece.rotations
        ))
        for piece in pieces
    )
    start_time = default_timer()
    moves = next(solutions(board, piece_set, board.board_mask), None)
    elapsed_time = int((default_timer() - start_time) * 1_000_000)
    if moves:
        logger.info(f"Hint found in {elapsed_time} microseconds")
        piece_index, rotation_index, position = choice(moves)
        return PiecePlacement(
            piece_id=pieces[piece_index].id,
            rotation_id=pieces[piece_index].rotations[rotation_index].id,
            position=position
        )
    logger.info(f"Hint not found in {elapsed_time} microseconds")
    return None
