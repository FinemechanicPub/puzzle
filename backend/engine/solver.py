from typing import Sequence

from engine.board import Board
from engine.types import PieceData, PieceSet, PositionMasks


def optimize(rotation_masks: Sequence[PositionMasks]) -> PieceData:
    """Оптимизировать структуру данных по возможным установкам фигур.

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

    if board.is_full():
        return

    piece_count = len(piece_set)
    empty_probes = board.probes
    board_mask = board.board_mask
    full_board = board.full

    history = dict[int, tuple[int, int, int, int]]()

    next_piece: int = 0
    next_rotation: int = 0
    position = advance_position(board_mask, 0)
    while True:
        placed = False
        for piece_index in range(next_piece, piece_count):
            if piece_index in history:
                continue
            rotations = piece_set[piece_index][position]
            for rotation_index in range(next_rotation, len(rotations)):
                original_index, mask = rotations[rotation_index]
                if board_mask & mask:
                    continue
                new_board = board_mask | mask
                if new_board == full_board:
                    yield [
                        (piece_index, original_index, position)
                        for piece_index, (_, position, _, original_index)
                        in history.items()
                    ] + [(piece_index, original_index, position)]
                else:
                    history[piece_index] = (
                        rotation_index, position, board_mask, original_index
                    )
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
        if not history:
            break

        next_piece, (next_rotation, position, board_mask, _) = history.popitem()
        next_rotation += 1
