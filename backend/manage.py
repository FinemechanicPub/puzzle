import asyncio
import contextlib
from itertools import combinations
from typing import Iterable

import click
from sqlalchemy import delete, select
from sqlalchemy.sql.expression import func

from app.services.play import make_piece_set
from engine.board import Board
from engine.solver import solutions
from app.core.db import get_async_session
from app.models.game import Game, GamePieces, Piece
from app.repositories.piece_repository import piece_repository
from app.schemas.piece import PieceBase
from app.services.piece import create_piece_with_rotations


SIGNATURE = "manage"

NO_ENOUGH_PIECES = (
    "Фигур заданного размера {size} найдено всего {count}, "
    "что недостаточно для замощения поля {height}x{width}"
)
BAD_SIZE = (
    "Поле {height}x{width} невозможно без промежутков замостить "
    "фигурами размера {size}"
)
GAMES_DELETED = (
    "Удалено {count} ранее созданных с помощью этой команды игр"
)
GAMES_CREATED = "Создано {count} игр"

PIECES_CREATED = "Создано {count} фигур"

PIECES = {
    5: {
        "F": [(0, 0), (0, 1), (1, -1), (1, 0), (2, 0)],
        "I": [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0)],
        "L": [(0, 0), (1, 0), (2, 0), (3, 0), (3, 1)],
        "N": [(0, 0), (1, 0), (2, -1), (2, 0), (3, -1)],
        "P": [(0, 0), (0, 1), (1, 0), (1, 1), (2, 0)],
        "T": [(0, 0), (0, 1), (0, 2), (1, 1), (2, 1)],
        "U": [(0, 0), (0, 2), (1, 0), (1, 1), (1, 2)],
        "V": [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)],
        "W": [(0, 0), (1, 0), (1, 1), (2, 1), (2, 2)],
        "X": [(0, 0), (1, -1), (1, 0), (1, 1), (2, 0)],
        "Y": [(0, 0), (1, -1), (1, 0), (2, 0), (3, 0)],
        "Z": [(0, 0), (0, 1), (1, 1), (2, 1), (2, 2)],
    }
}

DEFAULT_COLORS = {
    "F": 14531481,
    "I": 15641258,
    "L": 13421704,
    "N": 11202218,
    "P": 12311961,
    "T": 10083771,
    "U": 8965324,
    "V": 10075101,
    "W": 11184878,
    "X": 12294621,
    "Y": 13404364,
    "Z": 14522811,
}


async def get_pieces(piece_size: int):
    session_context = contextlib.asynccontextmanager(get_async_session)
    async with session_context() as session:
        pieces = await piece_repository.list(
            session, clause=(Piece.size == piece_size)
        )
    return pieces


async def clean(height: int, width: int, piece_count: int):
    session_context = contextlib.asynccontextmanager(get_async_session)
    async with session_context() as session:
        select_statement = (
            select(Game.id).join(GamePieces)
            .where(Game.height == height)
            .where(Game.width == width)
            .where(Game.note == SIGNATURE)
            .group_by(Game.id)
            .having(func.count(GamePieces.game_id) == piece_count)
        )
        game_ids = await session.scalars(select_statement)
        delete_statement = delete(Game).where(Game.id.in_(game_ids))
        result = await session.execute(delete_statement)
        await session.commit()
        return result.rowcount


async def save_games(games: Iterable[Game]):
    session_context = contextlib.asynccontextmanager(get_async_session)
    async with session_context() as session:
        session.begin()
        session.add_all(games)
        await session.commit()
    return


async def save_pieces(pieces: Iterable[PieceBase]):
    session_context = contextlib.asynccontextmanager(get_async_session)
    async with session_context() as session:
        for piece in pieces:
            await create_piece_with_rotations(session, piece)
    return


@click.group()
def create():
    pass


@create.command()
@click.argument("height", type=click.INT)
@click.argument("width", type=click.INT)
@click.argument("piece_size", type=click.INT)
@click.argument("limit", type=click.INT, default=100)
def create_games(
    height: int,
    width: int,
    piece_size: int,
    limit: int,
):
    """Создание набора игр

    Размер поля HEIGHTxWIDTH. В игре используются фигуры размера PIECE_SIZE.
    """
    loop = asyncio.new_event_loop()

    board = Board(height, width)
    piece_count, excess = divmod(board.size, piece_size)
    if excess:
        raise click.ClickException(BAD_SIZE.format(
            size=piece_size, height=height, width=width
        ))
    pieces = loop.run_until_complete(get_pieces(piece_size))
    if piece_count > len(pieces):
        raise click.ClickException(NO_ENOUGH_PIECES.format(
            count=len(pieces), size=piece_size, height=height, width=width
        ))

    games: list[Game] = []
    for combination in combinations(pieces, piece_count):
        piece_set = make_piece_set(combination, height, width)
        if next(solutions(board, piece_set), None):
            game = Game(height=height, width=width, note=SIGNATURE)
            game.pieces.extend(combination)
            games.append(game)
            if len(games) >= limit:
                break
    deleted_count = loop.run_until_complete(clean(height, width, piece_count))
    click.echo(GAMES_DELETED.format(count=deleted_count))
    loop.run_until_complete(save_games(games))
    click.echo(GAMES_CREATED.format(count=len(games)))


@create.command()
@click.argument("size", type=click.Choice(list(map(str, PIECES))))
def create_pieces(size: str):
    """Создание набора фигур размера SIZE"""

    pieces = [
        PieceBase(name=name, points=points, color=DEFAULT_COLORS[name])
        for name, points in PIECES[int(size)].items()
    ]
    asyncio.run(save_pieces(pieces))
    click.echo(PIECES_CREATED.format(count=len(pieces)))


if __name__ == '__main__':
    create()
