from app.core.base import Piece, PieceRotation
from engine.piece import produce_rotations


def add_rotations(piece: Piece) -> Piece:
    rotations = produce_rotations(piece.points)
    for order, rotation in enumerate(rotations, 1):
        piece.rotations.append(
            PieceRotation(piece=piece, order=order, points=rotation)
        )
    return piece
