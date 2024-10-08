from sqlalchemy.ext.asyncio import AsyncSession

from app.core.base import Piece, PieceRotation
from app.repositories.piece_repository import piece_repository
from app.schemas.piece import PieceBase
from engine.piece import flipped_rotated


async def create_piece_with_rotations(
    session: AsyncSession, piece_data: PieceBase
):
    piece = await piece_repository.create(session, piece_data, commit=False)
    add_rotations(piece)
    await session.commit()
    await session.refresh(piece)
    return piece


def add_rotations(piece: Piece) -> Piece:
    rotations, reflections = flipped_rotated(piece.points)
    for order, rotation in enumerate(rotations, 1):
        piece.rotations.append(
            PieceRotation(piece=piece, order=order, points=rotation, flipped=0)
        )
    for order, reflection in enumerate(reflections, len(rotations) + 1):
        piece.rotations.append(
            PieceRotation(
                piece=piece, order=order, points=reflection, flipped=1
            )
        )
    return piece
