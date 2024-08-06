"""Типы данных решателя головоломок"""

from typing import Sequence, TypeAlias


# Точка с координатами [строка, столбец]
Point: TypeAlias = tuple[int, int]
# Определенная ориентация фигуры - последовательность точек
Points: TypeAlias = Sequence[Point]
# Набор ориентаций для фигуры
PieceRotations: TypeAlias = Sequence[Points]

# Двоичная маска фигуры
Mask: TypeAlias = int
# Двоичные маски фигуры при установке в каждой позиции на доске
PositionMasks: TypeAlias = Sequence[Mask]
# Кортеж идекса ориентации фигуры и её маски в определенной позиции
Placement: TypeAlias = tuple[int, Mask]
# Последовательность кортежей ориентаций для определенной позиции
PositionRotations: TypeAlias = Sequence[Placement]
# Кортежи ориентаций для всех позиций
PieceData: TypeAlias = Sequence[PositionRotations]
# Набор фигур для решателя головоломок
PieceSet: TypeAlias = Sequence[PieceData]
