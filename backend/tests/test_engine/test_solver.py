from engine.board import Board
from engine.piece import make_versions
from engine.solver import make_piece_set, solutions


PIECES = [
    [(0, 0), (0, 1), (1, -1), (1, 0), (2, 0)],  # F
    [(0, 0), (1, 0), (2, -1), (2, 0), (3, -1)],  # N
    [(0, 0), (0, 1), (0, 2), (1, 1), (2, 1)],  # T
    [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)],  # V
    [(0, 0), (1, -1), (1, 0), (2, 0), (3, 0)],  # Y
]

SOLUTIONS = set(
    (
        ((4, 6, 0), (2, 0, 1), (1, 2, 4), (0, 2, 11), (3, 1, 14)),
        ((0, 1, 0), (4, 7, 1), (2, 3, 9), (3, 0, 10), (1, 1, 16)),
        ((0, 6, 0), (3, 2, 2), (4, 2, 5), (1, 6, 8), (2, 2, 12)),
        ((1, 3, 0), (3, 2, 2), (2, 1, 5), (0, 3, 13), (4, 5, 16)),
        ((1, 4, 0), (2, 0, 1), (4, 0, 4), (3, 0, 10), (0, 4, 13)),
        ((3, 3, 0), (0, 0, 3), (1, 0, 6), (4, 4, 9), (2, 2, 12)),
        ((3, 3, 0), (1, 5, 3), (2, 3, 9), (0, 5, 11), (4, 3, 18)),
        ((4, 1, 0), (0, 7, 4), (2, 1, 5), (3, 1, 14), (1, 7, 16)),
    )
)


def test_solutions():
    board = Board(5, 5)
    rotations = [make_versions(piece) for piece in PIECES]
    piece_set = make_piece_set(board, rotations)
    solution_list = list(solutions(board, piece_set))
    assert len(solution_list) == 8
    assert all(tuple(solution) in SOLUTIONS for solution in solution_list)
