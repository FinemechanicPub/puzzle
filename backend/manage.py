import asyncio
import contextlib
from itertools import combinations
from typing import Iterable

import click
from sqlalchemy import delete, select
from sqlalchemy.sql.expression import func

# from engine.board import Board
from engine.board import Board, invert
from engine.solver import solutions
from app.core.db import get_async_session
from app.models.game import Game, GamePieces, Piece
from app.repositories.piece_repository import piece_repository


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

    board = Board(height, width)
    piece_count, excess = divmod(board.size, piece_size)
    if excess:
        raise click.ClickException(BAD_SIZE.format(
            size=piece_size, height=height, width=width
        ))
    pieces = asyncio.run(get_pieces(piece_size))
    if piece_count > len(pieces):
        raise click.ClickException(NO_ENOUGH_PIECES.format(
            count=len(pieces), size=piece_size, height=height, width=width
        ))

    games: list[Game] = []
    for combination in combinations(pieces, piece_count):
        piece_set = tuple(
            invert(tuple(
                board.piece_masks(rotation.points)
                for rotation in piece.rotations
            ))
            for piece in combination
        )
        if next(solutions(board, piece_set), None):
            game = Game(height=height, width=width, note=SIGNATURE)
            game.pieces.extend(combination)
            games.append(game)
            if len(games) >= limit:
                break
    deleted_count = asyncio.run(clean(height, width, piece_count))
    click.echo(GAMES_DELETED.format(count=deleted_count))
    asyncio.run(save_games(games))
    click.echo(GAMES_CREATED.format(count=len(games)))


if __name__ == '__main__':
    create()
