from sqlalchemy import ForeignKey
from sqlalchemy.ext.associationproxy import AssociationProxy, association_proxy
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import JSON, SmallInteger, String

from app.models.base import Base, EmptyBase


class PieceRotation(Base):
    piece_id: Mapped[int] = mapped_column(
        ForeignKey('piece.id', ondelete='CASCADE')
    )
    points: Mapped[tuple[tuple[int, int], ...]] = mapped_column(JSON)
    order: Mapped[int] = mapped_column(SmallInteger)
    piece: Mapped['Piece'] = relationship('Piece', back_populates='rotations')


class Piece(Base):
    name: Mapped[str] = mapped_column(String(1))
    size: Mapped[int] = mapped_column(SmallInteger)
    points: Mapped[tuple[tuple[int, int], ...]] = mapped_column(JSON)
    rotations: Mapped[list[PieceRotation]] = relationship(
        lazy='subquery', order_by='PieceRotation.order'
    )

    def __repr__(self) -> str:
        return (
            f'Piece(id={self.id}, name="{self.name}", '
            f'size={self.size}, points={repr(self.points)})'
        )


class Game(Base):

    title: Mapped[str] = mapped_column(default="", server_default="")
    width: Mapped[int] = mapped_column(SmallInteger)
    height: Mapped[int] = mapped_column(SmallInteger)
    game_pieces: Mapped[list['GamePieces']] = relationship(
        back_populates='game', cascade='all, delete-orphan'
    )
    pieces: AssociationProxy[list[Piece]] = association_proxy(
        target_collection='game_pieces', attr='piece',
        creator=lambda d: GamePieces(**d)
    )

    def __repr__(self) -> str:
        return (
            f'Game(id={self.id}, width={self.width}, '
            f'height={self.height}, pieces={repr(self.pieces)})'
        )


class GamePieces(EmptyBase):
    game_id: Mapped[int] = mapped_column(
        ForeignKey("game.id"), primary_key=True
    )
    piece_id: Mapped[int] = mapped_column(
        ForeignKey("piece.id"), primary_key=True
    )
    color: Mapped[int] = mapped_column()
    game: Mapped[Game] = relationship('Game', back_populates='game_pieces')
    piece: Mapped[Piece] = relationship('Piece')
    piece_name: AssociationProxy[str] = association_proxy(
        target_collection='piece', attr='name'
    )
    points: AssociationProxy[list] = association_proxy(
        target_collection='piece', attr='points'
    )
    rotations: AssociationProxy[list] = association_proxy(
        target_collection='piece', attr='rotations'
    )

    def __repr__(self) -> str:
        return (
            f'GamePieces(game_id={self.game_id}, piece_id={self.piece_id}, '
            f'color={self.color})'
        )
