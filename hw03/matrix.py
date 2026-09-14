from __future__ import annotations

import contextlib
from collections.abc import Callable, Iterator
from typing import Self


class Matrix:
    """Класс матрицы с поддержкой арифметики, хеширования и форматирования."""

    def __init__(self, data: list[list[float]]) -> None:
        """Создаёт матрицу из прямоугольного вложенного списка."""
        if data and any(len(row) != len(data[0]) for row in data):
            raise ValueError("Строки матрицы должны иметь одинаковую длину")
        self._data = tuple(tuple(row) for row in data)

    @property
    def rows(self) -> int:
        """Возвращает количество строк матрицы."""
        return len(self._data)

    @property
    def cols(self) -> int:
        """Возвращает количество столбцов матрицы."""
        return len(self._data[0]) if self._data else 0

    def __add__(self, other: Self) -> Self:
        """Складывает две матрицы одинакового размера."""
        self._check_same_shape(other)
        result = self._operation_with_other_matrix(other, lambda x, y: x + y)
        return result

    def __sub__(self, other: Self) -> Self:
        """Вычитает матрицу того же размера."""
        self._check_same_shape(other)
        result = self._operation_with_other_matrix(other, lambda x, y: x - y)
        return result

    def _operation_with_other_matrix(
        self, other: Self, op: Callable[[float, float], float]
    ) -> Self:
        """Вычисляет операции над элементами матриц"""
        result = [
            [op(self._data[row][col], other._data[row][col]) for col in range(self.cols)]
            for row in range(self.rows)
        ]
        return type(self)(result)

    def _check_same_shape(self, other: Matrix) -> None:
        """Проверяет равенство размеров двух матриц"""
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Матрицы должны иметь одинаковый размер")

    def __mul__(self, scalar: int | float) -> Self:
        """Умножает каждый элемент матрицы на скаляр."""
        result = [[value * scalar for value in row] for row in self._data]
        return type(self)(result)

    def __rmul__(self, scalar: int | float) -> Self:
        """Поддерживает умножение скаляра на матрицу."""
        return self.__mul__(scalar)

    def __matmul__(self, other: Self) -> Self:
        """Выполняет матричное умножение."""
        if self.cols != other.rows:
            raise ValueError(
                "Количество столбцов первой матрицы должно совпадать с количеством строк второй"
            )
        result = [
            [
                sum(self._data[row][index] * other._data[index][col] for index in range(self.cols))
                for col in range(other.cols)
            ]
            for row in range(self.rows)
        ]
        return type(self)(result)

    def __eq__(self, other: object) -> bool:
        """Сравнивает матрицы по значениям элементов."""
        return isinstance(other, Matrix) and self._data == other._data

    def __hash__(self) -> int:
        """Возвращает хеш матрицы."""
        return hash(self._data)

    def __repr__(self) -> str:
        """Возвращает однозначное представление матрицы."""
        data = [list(row) for row in self._data]
        return f"{type(self).__name__}({data!r})"

    def __str__(self) -> str:
        """Возвращает матрицу в читаемом табличном виде."""
        return "\n".join(" ".join(str(value) for value in row) for row in self._data)

    def __format__(self, format_spec: str) -> str:
        """Форматирует каждый элемент матрицы по заданной спецификации."""
        return "\n".join(
            " ".join(format(value, format_spec) for value in row) for row in self._data
        )

    @classmethod
    def from_file(cls, path: str) -> contextlib.AbstractContextManager[Matrix]:
        """Создаёт контекстный менеджер для чтения матрицы из файла."""

        @contextlib.contextmanager
        def manager() -> Iterator[Matrix]:
            with open(path, encoding="utf-8") as file:
                data = [[float(value) for value in line.split()] for line in file if line.strip()]
                yield cls(data)

        return manager()
