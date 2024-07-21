from collections import defaultdict
import logging
from random import choice
from timeit import default_timer
from typing import Sequence

from app.models.game import Piece
from app.schemas.piece import PiecePlacement
from engine.board import Board, invert
from engine.solver import solutions

logger = logging.getLogger(__name__)


def get_used_points(
        pieces: Sequence[Piece], used_pieces: Sequence[tuple[int, int, int]]
):
    used_piece_dict = defaultdict(set[tuple[int, int]])
    for piece_id, rotation_id, position in used_pieces:
        used_piece_dict[piece_id].add((rotation_id, position))
    on_board: list[tuple[int, tuple[tuple[int, int], ...]]] = []
    for piece_id in used_piece_dict:
        piece = next(filter(lambda piece: piece.id == piece_id, pieces), None)
        if not piece:
            continue
        for rotation_id, position in used_piece_dict[piece_id]:
            rotation = next(filter(
                lambda rotation: rotation.id == rotation_id, piece.rotations
            ))
            if rotation:
                on_board.append((position, rotation.points))
    return on_board


def get_available_pieces(
        pieces: Sequence[Piece], used_pieces: Sequence[tuple[int, int, int]]
):
    used_piece_count = defaultdict(int)
    for piece_id, _, _ in used_pieces:
        used_piece_count[piece_id] += 1
    return tuple(filter(lambda piece: used_piece_count[piece.id] == 0, pieces))


def merge_pieces(
    height: int, width: int,
    piece_positions: Sequence[tuple[int, tuple[tuple[int, int], ...]]]
) -> Board:
    board = Board(height, width)
    for position, points in piece_positions:
        board.merge_piece(points, position)
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
