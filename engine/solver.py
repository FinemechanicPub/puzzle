from typing import TypeAlias

from engine.board import Board


Mask: TypeAlias = int
Rotations: TypeAlias = tuple[tuple[Mask, int], ...]
Placements: TypeAlias = tuple[Rotations, ...]


def solutions(board: Board, piece_set: tuple[Placements, ...], board_mask=0):

    def advance_position(board: int, position: int) -> int:
        while board & empty_probes[position]:
            position += 1
        return position

    if board_mask == board.full:
        return

    piece_count = len(piece_set)
    empty_probes = board.probes
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
                mask, original_index = rotations[rotation_index]
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
