"""Сущность получателя подарка."""

from __future__ import annotations

from collections.abc import Mapping


class Recipient:
    """Человек, для которого планируются подарки."""

    def __init__(self, recipient_id: int, name: str) -> None:
        """Создать получателя с уникальным идентификатором и именем."""
        if recipient_id <= 0:
            raise ValueError("идентификатор получателя должен быть положительным")
        normalized_name = name.strip()
        if not normalized_name:
            raise ValueError("имя получателя не должно быть пустым")
        self.id = recipient_id
        self.name = normalized_name

    @classmethod
    def from_data(cls, data: Mapping[str, object]) -> Recipient:
        """Создать получателя из данных JSON."""
        recipient_id = data.get("id")
        name = data.get("name")
        if (
            not isinstance(recipient_id, int)
            or isinstance(recipient_id, bool)
            or not isinstance(name, str)
        ):
            raise ValueError("некорректные данные получателя")
        return cls(recipient_id, name)

    def to_data(self) -> dict[str, object]:
        """Преобразовать получателя в данные для JSON."""
        return {"id": self.id, "name": self.name}

    def __str__(self) -> str:
        """Вернуть строковое представление получателя."""
        return f"Получатель #{self.id}: {self.name}"
