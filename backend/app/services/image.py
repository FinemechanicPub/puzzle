from typing import Iterable, Sequence

from PIL import Image, ImageColor, ImageDraw

from engine.board import Board
from engine.piece import Piece, Point

WHITE = ImageColor.colormap["white"]
BLACK = ImageColor.colormap["black"]

BACKGROUND = WHITE
GRID_COLOR = BLACK


def rgb(color: int) -> tuple[int, int, int]:
    return (color & 0xFF, (color & 0xFF00) >> 8, (color & 0xFF0000) >> 16)


def stack_horizontally(
    images: Sequence[Image.Image],
    padding=5
) -> Image.Image:
    height = max(image.height for image in images)
    width = sum(image.width for image in images)
    width += padding * (len(images) + 1)
    im = Image.new("RGB", (width, height), BACKGROUND)
    left = padding
    for image in images:
        im.paste(image, (left, (height - image.height) // 2))
        left += image.width + padding
    return im


def stack_vertically(
    images: Sequence[Image.Image],
    padding=5
) -> Image.Image:
    width = max(image.width for image in images)
    height = sum(image.height for image in images)
    height += padding * (len(images) + 1)
    im = Image.new("RGB", (width, height), BACKGROUND)
    top = padding
    for image in images:
        im.paste(image, (((width - image.width) // 2), top))
        top += image.height + padding
    return im


def wrap(images: Sequence[Image.Image]) -> Image.Image:
    line_width = sum(image.width for image in images) // 2
    lines = [[]]
    current_width = 0
    for image in images:
        if current_width > line_width:
            lines.append([])
            current_width = 0
        lines[-1].append(image)
        current_width += image.width
    return stack_vertically(tuple(map(stack_horizontally, lines)))


def draw_board(board: Board, cell_width=10):
    width = cell_width * board.width + 1
    height = cell_width * board.height + 1
    im = Image.new("RGB", (width, height), BACKGROUND)
    canvas = ImageDraw.Draw(im)
    for row in range(board.height):
        for col in range(board.width):
            canvas.rectangle(
                [
                    col * cell_width, row * cell_width,
                    (col + 1) * cell_width, (row + 1) * cell_width
                ],
                outline=GRID_COLOR
            )
    return im


def draw_piece(points: tuple[Point, ...], color: int, cell_width=10):
    max_y = max(y for y, _ in points)
    max_x = max(x for _, x in points)
    min_x = min(x for _, x in points)
    width = (max_x - min_x + 1) * cell_width + 1
    height = (max_y + 1) * cell_width + 1
    im = Image.new("RGB", (width, height), BACKGROUND)
    canvas = ImageDraw.Draw(im)
    for row, col in points:
        col += -min_x
        canvas.rectangle(
            [
                col * cell_width, row * cell_width,
                (col + 1) * cell_width, (row + 1) * cell_width
            ],
            fill=rgb(color),
            outline=BACKGROUND
        )
    return im


def thumbnail(board: Board, pieces: Iterable[Piece]) -> Image.Image:
    return stack_vertically([
        draw_board(board),
        wrap(tuple(draw_piece(piece.points, piece.color) for piece in pieces)),
    ])
