from threading import Lock
from typing import Iterable, Sequence

from cachetools import LRUCache, cached, keys

from engine.board import Board
from engine.types import PieceData, PieceSet, Points, PositionMasks


def cache_key(board: Board, points: Points):
    """Возвращает ключ кэша для функции rotation_masks"""
    return keys.hashkey(
        board.height,
        board.width,
        tuple(number for point in points for number in point),
    )


@cached(cache=LRUCache(maxsize=512 * 1024), lock=Lock(), key=cache_key)
def rotation_masks(board: Board, points: Points):
    """Возвращает маски для фигуры в определенной ориентации."""
    return board.piece_masks(points)


def make_piece_set(board: Board, pieces: Iterable[Iterable[Points]]):
    """Создает набор фигур в формате решателя."""
    return tuple(
        optimize([rotation_masks(board, rotation) for rotation in rotations])
        for rotations in pieces
    )


def optimize(rotation_masks: Sequence[PositionMasks]) -> PieceData:
    """Оптимизирует структуру данных по возможным установкам фигур.

    Если маска равна нулю, значит фигура не может стоять в данной позиции.
    Возвращается последовательность длиной в количество позиций на доске,
    каждый элемент которой представляет собой последовательность кортежей
    из индекса и маски ориентации фигуры для тех ориентаций, которые могут
    быть установлены в данную позицию.
    """
    position_count = len(rotation_masks[0])
    return tuple(
        tuple(
            (rotation_index, masks[position])
            for rotation_index, masks in enumerate(rotation_masks)
            if masks[position]
        )
        for position in range(position_count)
    )


def solutions(board: Board, piece_set: PieceSet):
    """Генератор решений головоломки"""

    def advance_position(board_mask: int, position: int) -> int:
        while board_mask & empty_probes[position]:
            position += 1
        return position

    def build_result(last_piece: tuple[int, int, int]):
        result = [
            (piece_index, original_index, position)
            for piece_index, _, position, _, original_index in context
        ]
        result.append(last_piece)
        return result

    if board.is_full():
        return

    piece_count = len(piece_set)
    empty_probes = board.probes
    board_mask = board.board_mask
    full_board = board.full

    context: list[tuple[int, int, int, int, int]] = []

    free_pieces = [1] * piece_count
    next_piece: int = 0
    next_rotation: int = 0
    position = advance_position(board_mask, 0)
    while True:
        placed = False
        for piece_index in range(next_piece, piece_count):
            if not free_pieces[piece_index]:
                continue
            rotations = piece_set[piece_index][position]
            for rotation_index in range(next_rotation, len(rotations)):
                original_index, mask = rotations[rotation_index]
                if board_mask & mask:
                    continue
                new_board = board_mask | mask
                if new_board == full_board:
                    yield build_result((piece_index, original_index, position))
                else:
                    context.append(
                        (
                            piece_index,
                            rotation_index,
                            position,
                            board_mask,
                            original_index,
                        )
                    )
                    free_pieces[piece_index] -= 1
                    board_mask = new_board
                    position = advance_position(board_mask, position + 1)
                    placed = True
                    next_piece = 0
                break
            next_rotation = 0
            if placed:
                break

        if placed:
            continue
        if not context:
            break

        next_piece, next_rotation, position, board_mask, *_ = context.pop()
        free_pieces[next_piece] += 1
        next_rotation += 1
