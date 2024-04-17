from random import choice
from app.models.game import Game, Piece, PieceRotation
from app.schemas.piece import PiecePlacement

from engine.board import Board, Projection, invert
from engine.solver import solutions


def make_hint(
        game: Game,
        placed_pieces: list[tuple[PieceRotation, int]],
        available_pieces: list[Piece]
) -> PiecePlacement | None:
    board = Board(game.height, game.width)
    board_mask = 0
    for placed_piece, position in placed_pieces:
        projection = Projection(board, placed_piece.points)
        board_mask |= projection.at_position(position)
    piece_set = tuple(
        invert(tuple(
            board.piece_masks(rotation.points)
            for rotation in piece.rotations
        ))
        for piece in available_pieces
    )
    moves = next(solutions(board, piece_set, board_mask), None)
    if moves:
        piece_index, rotation_index, position = choice(moves)
        return PiecePlacement(
            piece_id=available_pieces[piece_index].id,
            rotation_id=rotation_index,
            position=position
        )
    return None
