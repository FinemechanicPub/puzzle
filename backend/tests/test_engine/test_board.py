import pytest

from engine.board import Board
from engine.types import Points

HORIZONTAL_BAR = [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4)]
VERTICAL_BAR = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0)]
T_SHAPE = [(0, 0), (0, 1), (0, 2), (1, 1), (2, 1)]

CASES: list[tuple[Points, int, list[int]]] = [
    (HORIZONTAL_BAR, 0, [20]),
    (HORIZONTAL_BAR, 5, [5, 15]),
    (HORIZONTAL_BAR, 10, [10, 10]),
    (HORIZONTAL_BAR, 15, [15, 5]),
    (HORIZONTAL_BAR, 20, [20]),
    (VERTICAL_BAR, 0, [20]),
    (VERTICAL_BAR, 1, [5, 15]),
    (VERTICAL_BAR, 2, [10, 10]),
    (VERTICAL_BAR, 3, [15, 5]),
    (VERTICAL_BAR, 4, [20]),
    (T_SHAPE, 1, [20]),
    (T_SHAPE, 2, [20]),
    (T_SHAPE, 3, [20]),
    (T_SHAPE, 5, [20]),
    (T_SHAPE, 10, [18, 2]),
    (T_SHAPE, 11, [20]),
    (T_SHAPE, 12, [18, 2]),
]


@pytest.mark.parametrize(["piece", "position", "areas"], CASES)
def test_areas(piece: Points, position: int, areas: list[int]):
    board = Board(5, 5)
    board.merge_piece(piece, position)
    assert list(board.areas()) == areas
    expect_even_space = all(area % 5 == 0 for area in areas)
    assert board.has_even_space(board.board_mask, 5) == expect_even_space
