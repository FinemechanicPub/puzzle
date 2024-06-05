from typing import TypeAlias

from engine.piece import Point

Mask: TypeAlias = int
Orientations: TypeAlias = tuple[Mask, ...]
Placements: TypeAlias = tuple[Orientations, ...]


class Projection:
    """Проекция фигуры на доску"""
    board_width: int = 0
    board_height: int = 0
    board_size: int = 0
    piece_width: int = 0
    max_x: int = 0
    min_y: int = 0
    max_y: int = 0
    column_range: range = range(0)  # допустимые колонки установки
    row_range: range = range(0)  # допустимые строки установки
    mask: int = 0

    def __init__(self, board: 'Board', points: tuple[Point, ...]) -> None:
        self.board_width = board.width
        self.board_height = board.height
        self.board_size = board.size
        self.max_y = max(y for y, _ in points)
        self.max_x = max(x for _, x in points)
        self.min_x = min(x for _, x in points)
        self.piece_width = self.max_x - self.min_x

        self.column_range = range(-self.min_x, self.board_width - self.max_x)
        self.row_range = range(self.board_height - self.max_y)

        # Битовая маска фигуры при установке в крайнее положение снизу справа
        for y, x in points:
            self.mask |= 1 << (
                (self.max_y - y) * self.board_width + self.max_x - x
            )

    def on_edge(self, row: int, col: int) -> bool:
        """Прижата ли фигура к краю если верхняя точка в данной ячейке."""
        if row == 0 or row == self.board_height - self.max_y - 1:
            return True
        if col == -self.min_x or col == self.board_width - self.max_x - 1:
            return True
        return False

    def at_position(self, position: int) -> int:
        """Маска фигуры в заданной позиции на доске"""
        return self.mask << self.board_size - position - self.mask.bit_length()

    def at_cell(self, row: int, col: int) -> int:
        """Маска фигуры в заданной ячейке на доске"""
        return self.at_position(row * self.board_width + col)


class Board:
    height: int = 0
    width: int = 0
    size: int = 0

    def __init__(self, height, width) -> None:
        self.height = height
        self.width = width
        self.size = height * width
        self.full = 2**self.size - 1
        self.probes = tuple(1 << k for k in reversed(range(self.size)))
        self.board_mask = 0

    def count_area(self, board_mask: int, initial_point: int) -> int:
        """Подсчет количества достижимых ячеек"""
        if initial_point >= self.size:
            return 0

        count = 0
        shifts = ((0, 1), (0, -1), (1, 0), (-1, 0))
        edge = [initial_point]
        while edge:
            point = edge.pop()
            if board_mask & self.probes[point]:
                continue
            count += 1
            board_mask |= self.probes[point]
            row, col = divmod(point, self.width)
            for delta_row, delta_col in shifts:
                new_row = row + delta_row
                new_col = col + delta_col
                if new_row < 0 or new_row >= self.height:
                    continue
                if new_col < 0 or new_col >= self.width:
                    continue
                new_point = new_row * self.width + new_col
                if not board_mask & self.probes[new_point]:
                    edge.append(new_point)
        return count

    def is_connected(self, board_mask: int) -> bool:
        """Проверка связности пустого пространства на доске"""
        position = 0
        while board_mask & self.probes[position]:
            position += 1
        return (
            self.count_area(board_mask, position) % board_mask.bit_count() == 0
        )

    def piece_masks(self, points: tuple[Point, ...]) -> tuple[int, ...]:
        """Массив битовых масок для фигуры, установленной на доске."""
        piece = Projection(self, points)
        piece_mask = piece.mask
        masks = [0] * self.size
        for row in reversed(piece.row_range):
            for col in reversed(piece.column_range):
                masks[row*self.width + col] = (
                    piece_mask
                    if not piece.on_edge(row, col)
                    or self.is_connected(piece_mask)
                    else 0
                )
                piece_mask <<= 1
            piece_mask <<= piece.piece_width
        return tuple(masks)

    def merge_piece(self, points: tuple[Point, ...], position: int):
        projection = Projection(self, points)
        self.board_mask |= projection.at_position(position)
        return


def invert(
    masks: tuple[tuple[int, ...], ...]
) -> tuple[tuple[tuple[int, int], ...], ...]:
    """Создание массива масок фигуры:
    - внешний массив по всем позициями доски
    - внутренний массив по тем ориентациям фигуры,
    которые могут быть установлены в заданную позицию"""
    return tuple(
        tuple(
            (masks[rotation_index][position_index], rotation_index)
            for rotation_index in range(len(masks))
            if masks[rotation_index][position_index]
        )
        for position_index in range(len(masks[0]))
    )


def rotation_indices(masks: tuple[tuple[int, ...], ...]):
    return tuple(
        tuple(
            rotation_index
            for rotation_index in range(len(masks[0]))
            if masks[rotation_index][position_index]
        )
        for position_index in range(len(masks))
    )
