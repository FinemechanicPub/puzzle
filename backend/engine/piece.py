from engine.types import Point, Points


def _transpose(points: Points) -> tuple[Point, ...]:
    """Транспонирование точек фигуры."""
    return tuple((x, y) for y, x in points)


def _flip_vertically(points: Points) -> tuple[Point, ...]:
    """Отражение фигуры относительно горизонтальной оси."""
    return tuple((-y, x) for y, x in points)


def _rotate_left(points: Points, times=1) -> tuple[Point, ...]:
    """Поворот фигуры против часовой стрелки."""
    for _ in range(times):
        points = flip_vertically(transpose(points))
    return tuple(points)


def normalize(points: Points) -> tuple[Point, ...]:
    """Такой сдвиг фигуры, что самая левая точка в верхнем ряду
    получает координаты (0, 0)."""
    base_y, base_x = min(points)
    return tuple(sorted((y - base_y, x - base_x) for y, x in points))


def transpose(points: Points) -> tuple[Point, ...]:
    """Транспонирование точек фигуры с нормализацией."""
    return normalize(_transpose(points))


def flip_vertically(points: Points) -> tuple[Point, ...]:
    """Отражение фигуры относительно горизонтальной оси с нормализацией."""
    return normalize(_flip_vertically(points))


def rotate_left(points: Points, times=1) -> tuple[Point, ...]:
    """Поворот фигуры против часовой стрелки с нормализацией."""
    return normalize(_rotate_left(points))


def produce_rotations(
    points: Points, rotate=True, flip=True
) -> tuple[Points, ...]:
    """Создание версий фигуры на основе вращения и отражения."""
    rotations = list[tuple[Point, ...]]()  # список для стабильности порядка
    for side in range(2 if flip else 1):
        for quarter in range(4 if rotate else 1):
            upright = _rotate_left(points, quarter)
            rotation = normalize(_flip_vertically(upright) if side else upright)
            if rotation not in rotations:
                rotations.append(rotation)
    return tuple(rotations)
