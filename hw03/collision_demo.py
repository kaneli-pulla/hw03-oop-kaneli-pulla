from hw03.matrix import Matrix


class CollidingMatrix(Matrix):
    """Матрица с намеренно одинаковым хешем для демонстрации коллизии."""

    def __hash__(self) -> int:
        """Возвращает фиксированный хеш для любой матрицы."""
        return 239

    def __eq__(self, other: object) -> bool:
        """Сравнивает коллидирующие матрицы по значениям элементов."""
        return isinstance(other, CollidingMatrix) and self._data == other._data
        # чтобы сравнение Matrix и CollidingMatrix всегда было False и
        # соблюдался инвариант a == b -> hash(a) == hash(b).



def demonstrate_set_dict() -> dict[str, object]:
    """Демонстрирует использование Matrix в set и dict."""
    first = Matrix([[1, 2], [3, 4]])
    second = Matrix([[5, 6], [7, 8]])
    first_copy = Matrix([[1, 2], [3, 4]])
    matrices_in_set = {first, second, first_copy}
    matrix_dict = {
        first: "first",
        second: "second",
        first_copy: "first copy",
    }
    assert first == first_copy
    assert hash(first) == hash(first_copy)
    return {"matrices_in_set": matrices_in_set, "matrix_dict": matrix_dict}


def demonstrate_collision() -> tuple[Matrix, Matrix]:
    """Демонстрирует корректную обработку коллизии хешей."""
    first = CollidingMatrix([[1, 2], [3, 4]])
    second = CollidingMatrix([[5, 6], [7, 8]])
    assert first != second
    assert hash(first) == hash(second)
    matrices = {first, second}
    assert len(matrices) == 2
    # Для hashable-объектов должен выполняться инвариант:
    # a == b -> hash(a) == hash(b).
    # Если равные объекты имеют разные хеши, set и dict могут искать их
    # в разных ячейках хеш-таблицы и воспринимать как разные ключи.
    # Обратное неправда: одинаковый hash не означает равенство объектов.
    # При коллизии Python дополнительно сравнивает объекты через __eq__,
    # поэтому разные объекты с одинаковым хешем могут храниться вместе.
    # В среднем поиск в set и dict выполняется за O(1).
    # При большом количестве коллизий производительность ухудшается,
    # а в худшем случае поиск может приблизиться к O(n).
    return first, second


if __name__ == "__main__":
    print("=== Демонстрация Matrix в set/dict ===")
    result = demonstrate_set_dict()
    print(f"Матрицы в set: {result['matrices_in_set']}")
    print(f"Matrix dict: {result['matrix_dict']}")

    print("\n=== Демонстрация коллизии хешей ===")
    m1, m2 = demonstrate_collision()
    print(f"m1 = {m1!r}")
    print(f"m2 = {m2!r}")
    print(f"m1 == m2: {m1 == m2}")
    print(f"hash(m1) == hash(m2): {hash(m1) == hash(m2)}")
    print(f"Обе в set: { {m1, m2} }")
