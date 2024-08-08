from timeit import default_timer
from typing import Iterable

from engine.types import Points
from engine.piece import produce_rotations
from engine.board import Board
from engine.samples import PENTAMINO_PIECES
from engine.solver import solutions, optimize


def make_piece_set(board: Board, pieces: Iterable[Iterable[Points]]):
    return tuple(
        optimize([
            board.piece_masks(rotation)
            for rotation in rotations
        ])
        for rotations in pieces
    )


def find_all_solutions():
    board = Board(10, 6)
    start = default_timer()
    piece_set = make_piece_set(
        board,
        (
            produce_rotations(piece)
            for piece in PENTAMINO_PIECES.values()
        )
    )
    print(f"Piece generation time: {(default_timer() - start)*1000:.0f} ms")
    start = default_timer()
    sols = list(solutions(board, piece_set))
    print(f"Solution generation time: {(default_timer() - start):.2f} s")
    print(f"Solutions: {len(sols)}")


if __name__ == "__main__":
    find_all_solutions()
