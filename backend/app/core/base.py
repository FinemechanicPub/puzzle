"""Импорты класса Base и всех моделей для Alembic."""

from app.models.base import Base  # noqa
from app.models.game import Game, GamePieces, Piece, PieceRotation  # noqa
from app.models.menu import Menu  # noqa
from app.models.user import User  # noqa
