"""Сущность события, к которому готовится подарок."""

from __future__ import annotations

from collections.abc import Mapping
from datetime import date

from .recipient import Recipient


class Occasion:
    """Событие конкретного получателя."""

    def __init__(
        self,
        occasion_id: int,
        name: str,
        event_date: date,
        recipient: Recipient,
    ) -> None:
        """Создать событие и связать его с получателем."""
        if occasion_id <= 0:
            raise ValueError("идентификатор события должен быть положительным")
        normalized_name = name.strip()
        if not normalized_name:
            raise ValueError("название события не должно быть пустым")
        self.id = occasion_id
        self.name = normalized_name
        self.event_date = event_date
        self.recipient = recipient

    @staticmethod
    def validate_event_date(
        event_date: date,
        today: date | None = None,
    ) -> None:
        """Проверить, что новое событие не находится в прошлом."""
        current_date = today or date.today()
        if event_date < current_date:
            raise ValueError("дата праздника не может быть в прошлом")

    @classmethod
    def from_data(
        cls,
        data: Mapping[str, object],
        recipients: Mapping[int, Recipient],
    ) -> Occasion:
        """Создать событие из JSON и восстановить связь с получателем."""
        occasion_id = data.get("id")
        name = data.get("name")
        raw_date = data.get("event_date")
        recipient_id = data.get("recipient_id")
        if (
            not isinstance(occasion_id, int)
            or isinstance(occasion_id, bool)
            or not isinstance(name, str)
            or not isinstance(raw_date, str)
            or not isinstance(recipient_id, int)
            or isinstance(recipient_id, bool)
        ):
            raise ValueError("некорректные данные события")
        recipient = recipients.get(recipient_id)
        if recipient is None:
            raise ValueError(
                f"для события #{occasion_id} не найден получатель #{recipient_id}"
            )
        try:
            event_date = date.fromisoformat(raw_date)
        except ValueError as error:
            raise ValueError("некорректная дата события") from error
        return cls(occasion_id, name, event_date, recipient)

    def to_data(self) -> dict[str, object]:
        """Преобразовать событие в данные для JSON."""
        return {
            "id": self.id,
            "name": self.name,
            "event_date": self.event_date.isoformat(),
            "recipient_id": self.recipient.id,
        }

    def __str__(self) -> str:
        """Вернуть строковое представление события."""
        return (
            f"{self.name} для {self.recipient.name} "
            f"({self.event_date:%d.%m.%Y})"
        )
