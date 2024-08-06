from collections import Counter
from dataclasses import dataclass
import logging
from random import choice
from timeit import default_timer
from typing import Sequence, TypeAlias

from app.models.game import Game, Piece, PieceRotation
from engine.board import Board
from engine.solver import optimize, solutions
from engine.types import PieceSet, PieceRotations, PositionMasks

# Идентификаторы базы данных фигуры и ориентации и её позиция
PiecePositionDb: TypeAlias = tuple[int, int, int]
# Индексы фигуры и ориентации и её позиция
PiecePositionEngine: TypeAlias = tuple[int, int, int]

logger = logging.getLogger(__name__)


@dataclass
class PositionedPiece:
    position: int
    rotation: PieceRotation


def get_rotation(
        game: Game, piece_id: int, rotation_id: int
        ) -> PieceRotation | None:
    """Возвращает ориентацию фигуры или None, если в игре её нет."""

    piece = next(filter(lambda item: item.id == piece_id, game.pieces), None)
    if not piece:
        return None
    rotation = next(filter(
        lambda item: item.id == rotation_id, piece.rotations
    ), None)
    return rotation


def get_available_pieces(
        game: Game, installed_pieces: Sequence[PositionedPiece]
) -> Sequence[Piece]:
    counts = Counter(piece.rotation.piece_id for piece in installed_pieces)    
    # TODO: Возвращать количества оставшихся фигур
    return tuple(
        game_piece.piece
        for game_piece in game.game_pieces
        if game_piece.count > counts[game_piece.piece_id]
    )


def from_db_model(piece: Piece) -> PieceRotations:
    """Последовательность точек каждой ориентации фигуры."""
    return tuple(rotation.points for rotation in piece.rotations)


def get_mask(
        board: Board, rotations: PieceRotations
) -> Sequence[PositionMasks]:
    """Двоичные маски для каждой ориентации фигуры."""
    return tuple(board.piece_masks(rotation) for rotation in rotations)


def make_piece_set(pieces: Sequence[Piece], height: int, width: int):
    """Создает набор фигур в формате решателя."""

    board = Board(height, width)
    return tuple(
        optimize(get_mask(board, from_db_model(piece))) for piece in pieces
    )


def solve(board: Board, piece_set: PieceSet) -> PiecePositionEngine | None:
    """Вызывает решатель для поиска хода для заданной позиции на доске"""

    start_time = default_timer()
    moves = next(solutions(board, piece_set), None)
    elapsed_time = int((default_timer() - start_time) * 1_000_000)
    if moves:
        logger.info(f"Hint found in {elapsed_time} microseconds")
        return choice(moves)
    logger.info(f"Hint not found in {elapsed_time} microseconds")
    return None


def hint_move(
        game: Game, pieces: Sequence[PositionedPiece]
        ) -> tuple[bool, PiecePositionDb | None]:
    """Возвращает параметры следующего возможного хода.

    Первый элемент кортежа показывает заполнена ли доска полностью.
    Второй элемент кортежа содержит идентификатор фигуры и её ориентации
    и позицию для установки, если решение возможно, иначе None.
    """

    start_time = default_timer()
    board = Board(game.height, game.width)
    for piece in pieces:
        board.merge_piece(piece.rotation.points, piece.position)
    if board.is_full():
        return True, None
    available_pieces = get_available_pieces(game, pieces)
    hint = solve(
        board, make_piece_set(available_pieces, game.height, game.width)
    )
    elapsed_time = int((default_timer() - start_time) * 1_000_000)
    logger.info(f"Move calculation took {elapsed_time} microseconds total")
    if not hint:
        return False, None
    piece_index, rotation_index, position = hint
    return False, (
        available_pieces[piece_index].id,
        available_pieces[piece_index].rotations[rotation_index].id,
        position
    )
