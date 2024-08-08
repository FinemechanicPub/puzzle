from engine.disjointset import DisjointSet
from engine.types import Mask, PositionMasks, Points


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

    def __init__(self, board: 'Board', points: Points) -> None:
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

    def at_position(self, position: int) -> Mask:
        """Маска фигуры в заданной позиции на доске"""
        return self.mask << self.board_size - position - self.mask.bit_length()

    def at_cell(self, row: int, col: int) -> Mask:
        """Маска фигуры в заданной ячейке на доске"""
        return self.at_position(row * self.board_width + col)


class Board:
    height: int = 0
    width: int = 0
    size: int = 0

    def __init__(self, height: int, width: int) -> None:
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

    def has_even_space(self, board_mask: int, piece_size: int) -> bool:
        """Проверка кратности размера свободного пространства на доске."""
        position = 0
        while board_mask & self.probes[position]:
            position += 1
        return (
            self.count_area(board_mask, position) % piece_size == 0
        )

    def areas(self, board_mask: int | None = None):
        if board_mask is None:
            board_mask = self.board_mask
        _areas = DisjointSet(self.size)
        for position in range(self.size):
            if board_mask & self.probes[position]:
                continue
            left_neighbour = position % self.width and not board_mask & self.probes[position - 1]
            top_neighbour = position >= self.width and not board_mask & self.probes[position - self.width]
            if left_neighbour:
                _areas.union(position - 1, position)
            if top_neighbour:
                _areas.union(position - self.width, position)
        return tuple(size for size in _areas.sets() if size > 1)

    def is_full(self) -> bool:
        return self.board_mask == self.full

    def piece_masks(self, points: Points) -> PositionMasks:
        """Битовые маски фигуры в каждой позиции"""
        n = len(points)
        piece = Projection(self, points)
        piece_mask = piece.mask
        masks = [0] * self.size
        for row in reversed(piece.row_range):
            for col in reversed(piece.column_range):
                masks[row*self.width + col] = (
                    piece_mask
                    if not piece.on_edge(row, col)
                    # or max(area_size % n for area_size in self.areas(piece_mask)) == 0
                    or self.has_even_space(piece_mask, n)
                    else 0
                )
                piece_mask <<= 1
            piece_mask <<= piece.piece_width
        return tuple(masks)

    def merge_piece(self, points: Points, position: int):
        """Дополнить маску доски маской фигуры."""
        projection = Projection(self, points)
        self.board_mask |= projection.at_position(position)
        return
