from collections import defaultdict
import logging
from random import choice
from timeit import default_timer
from typing import Sequence

from app.models.game import Game, Piece
from engine.board import Board
from engine.solver import optimize, solutions
from engine.types import PieceSet, PieceRotations, PositionMasks

logger = logging.getLogger(__name__)


def get_occupied_cells(
        pieces: Sequence[Piece], used_pieces: Sequence[tuple[int, int, int]]
):
    """Ячейки, занятые установленными на доске фигурами"""

    used_piece_dict: dict[int, set[tuple[int, int]]] = defaultdict(set)
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
    """Оставшиеся неиспользованными фигуры"""

    used_piece_count: dict[int, int] = defaultdict(int)
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


def from_db_model(piece: Piece) -> PieceRotations:
    """Получение последовательности точек каждой ориентации фигуры."""
    return tuple(rotation.points for rotation in piece.rotations)


def get_mask(
        board: Board, rotations: PieceRotations
) -> Sequence[PositionMasks]:
    """Получение двоичных масок для каждой ориентации фигуры."""
    return tuple(board.piece_masks(rotation) for rotation in rotations)


def make_piece_set(pieces: Sequence[Piece], height: int, width: int):
    """Создает набор фигур в формате решателя."""

    board = Board(height, width)
    return tuple(
        optimize(get_mask(board, from_db_model(piece))) for piece in pieces
    )


def solve(
        board: Board,
        piece_set: PieceSet
) -> tuple[int, int, int] | None:

    start_time = default_timer()
    moves = next(solutions(board, piece_set, board.board_mask), None)
    elapsed_time = int((default_timer() - start_time) * 1_000_000)
    if moves:
        logger.info(f"Hint found in {elapsed_time} microseconds")
        return choice(moves)
    logger.info(f"Hint not found in {elapsed_time} microseconds")
    return None


def hint_move(game: Game, pieces: Sequence[tuple[int, int, int]]):
    occupied_cells = get_occupied_cells(game.pieces, pieces)
    board = merge_pieces(game.height, game.width, occupied_cells)
    if board.is_full():
        return True, None
    available_pieces = get_available_pieces(game.pieces, pieces)
    hint = solve(
        board, make_piece_set(available_pieces, game.height, game.width)
    )
    if not hint:
        return False, None
    piece_index, rotation_index, position = hint
    return False, (
        available_pieces[piece_index].id,
        available_pieces[piece_index].rotations[rotation_index].id,
        position
    )
