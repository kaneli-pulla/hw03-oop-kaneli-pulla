from __future__ import annotations

import logging
from typing import Any

logger = logging.getLogger(__name__)


class Logged:
    """Дескриптор с логированием операций чтения и записи."""

    def __init__(self, default: Any = None) -> None:
        """Создаёт дескриптор со значением по умолчанию."""
        self.default = default
        self.name = ""

    def __set_name__(self, owner: type, name: str) -> None:
        """Сохраняет имя управляемого атрибута."""
        self.name = name

    def __get__(self, obj: Any, objtype: type | None = None) -> Any:
        """Возвращает значение и логирует обращение к атрибуту."""
        if obj is None:
            return self
        value = obj.__dict__.get(self.name, self.default)
        logger.info("Getting %s: %r", self.name, value)
        return value

    def __set__(self, obj: Any, value: Any) -> None:
        """Сохраняет значение и логирует его изменение."""
        logger.info("Setting %s: %r", self.name, value)
        obj.__dict__[self.name] = value


class Cached:
    """Дескриптор с ленивым вычислением и кешированием."""

    def __init__(self, factory: Any) -> None:
        """Создаёт дескриптор с функцией вычисления значения."""
        self.factory = factory
        self.name = ""

    def __set_name__(self, owner: type, name: str) -> None:
        """Сохраняет имя управляемого атрибута."""
        self.name = name

    def __get__(self, obj: Any, objtype: type | None = None) -> Any:
        """Вычисляет значение при первом обращении и кеширует его."""
        if obj is None:
            return self
        if self.name not in obj.__dict__:
            obj.__dict__[self.name] = self.factory()
        return obj.__dict__[self.name]

    def __set__(self, obj: Any, value: Any) -> None:
        """Сохраняет переданное значение в кеше."""
        obj.__dict__[self.name] = value


class ReadOnly:
    """Дескриптор, допускающий однократную запись."""

    def __init__(self, default: Any = None) -> None:
        """Создаёт дескриптор со значением по умолчанию."""
        self.default = default
        self.name = ""

    def __set_name__(self, owner: type, name: str) -> None:
        """Сохраняет имя управляемого атрибута."""
        self.name = name

    def __get__(self, obj: Any, objtype: type | None = None) -> Any:
        """Возвращает записанное значение или значение по умолчанию."""
        if obj is None:
            return self
        return obj.__dict__.get(self.name, self.default)

    def __set__(self, obj: Any, value: Any) -> None:
        """Разрешает установить значение только один раз."""
        if self.name in obj.__dict__:
            raise AttributeError(f"Атрибут {self.name} доступен только для чтения")
        obj.__dict__[self.name] = value


class Observable:
    """Дескриптор с поддержкой подписки на изменения."""
    def __init__(self, default: Any = None) -> None:
        raise NotImplementedError

    def __set_name__(self, owner: type, name: str) -> None:
        raise NotImplementedError

    def __get__(self, obj: Any, objtype: type | None = None) -> Any:
        raise NotImplementedError

    def __set__(self, obj: Any, value: Any) -> None:
        raise NotImplementedError

    def add_observer(self, obj: Any, callback: Any) -> None:
        """Регистрирует callback для отслеживания изменений."""
        raise NotImplementedError


class Typed:
    """Дескриптор со строгой проверкой типа."""
    def __init__(self, expected_type: type) -> None:
        raise NotImplementedError

    def __set_name__(self, owner: type, name: str) -> None:
        raise NotImplementedError

    def __get__(self, obj: Any, objtype: type | None = None) -> Any:
        raise NotImplementedError

    def __set__(self, obj: Any, value: Any) -> None:
        raise NotImplementedError


class Validated:
    """Дескриптор с проверкой типа и диапазона значений."""
    def __init__(
        self,
        expected_type: type,
        min_value: Any = None,
        max_value: Any = None,
    ) -> None:
        raise NotImplementedError

    def __set_name__(self, owner: type, name: str) -> None:
        raise NotImplementedError

    def __get__(self, obj: Any, objtype: type | None = None) -> Any:
        raise NotImplementedError

    def __set__(self, obj: Any, value: Any) -> None:
        raise NotImplementedError
