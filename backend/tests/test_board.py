from engine.board import Board
from engine.piece import normalize, rotate_left
from engine.samples import PENTAMINO_PIECES


def test_areas():
    board = Board(12, 5)

    board.merge_piece(normalize(rotate_left(PENTAMINO_PIECES["I"])), 5)
    print(board.areas(board.board_mask))


if __name__ == "__main__":
    test_areas()
