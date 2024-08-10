from typing import Sequence

import pytest

from engine.piece import Points, produce_rotations

CASES: list[tuple[Points, Sequence[Points]]] = [
    (
        [(0, 0), (0, 1), (1, -1), (1, 0), (2, 0)],
        (
            ((0, 0), (0, 1), (1, -1), (1, 0), (2, 0)),
            ((0, 0), (1, 0), (1, 1), (1, 2), (2, 1)),
            ((0, 0), (1, 0), (1, 1), (2, -1), (2, 0)),
            ((0, 0), (1, -1), (1, 0), (1, 1), (2, 1)),
            ((0, 0), (1, -1), (1, 0), (2, 0), (2, 1)),
            ((0, 0), (1, -1), (1, 0), (1, 1), (2, -1)),
            ((0, 0), (0, 1), (1, 1), (1, 2), (2, 1)),
            ((0, 0), (1, -2), (1, -1), (1, 0), (2, -1))
        )
    ),
    (
        [(0, 0), (0, 1), (1, 1), (2, 1), (2, 2)],
        (
            ((0, 0), (0, 1), (1, 1), (2, 1), (2, 2)),
            ((0, 0), (1, -2), (1, -1), (1, 0), (2, -2)),
            ((0, 0), (0, 1), (1, 0), (2, -1), (2, 0)),
            ((0, 0), (1, 0), (1, 1), (1, 2), (2, 2))
        )
    )
]


@pytest.mark.parametrize(["points", "rotations"], CASES)
def test_rotations(points: Points, rotations: Sequence[Points]):
    assert produce_rotations(points) == rotations
