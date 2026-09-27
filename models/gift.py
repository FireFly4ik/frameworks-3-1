"""Сущность подарка."""

from __future__ import annotations

from collections.abc import Mapping

from .occasion import Occasion


class Gift:
    """Подарок, запланированный к определённому событию."""

    def __init__(
        self,
        gift_id: int,
        name: str,
        price: int,
        occasion: Occasion,
        purchased: bool = False,
    ) -> None:
        """Создать подарок и связать его с событием."""
        if gift_id <= 0:
            raise ValueError("идентификатор подарка должен быть положительным")
        normalized_name = name.strip()
        if not normalized_name:
            raise ValueError("название подарка не должно быть пустым")
        if price <= 0:
            raise ValueError("цена подарка должна быть положительным целым числом")
        self.id = gift_id
        self.name = normalized_name
        self.price = price
        self.occasion = occasion
        self.purchased = purchased

    @property
    def status(self) -> str:
        """Вернуть читаемый статус покупки."""
        return "куплен" if self.purchased else "запланирован"

    def mark_purchased(self) -> None:
        """Отметить подарок купленным."""
        self.purchased = True

    def matches(self, query: str) -> bool:
        """Проверить совпадение с названием, получателем или событием."""
        normalized_query = query.strip().lower()
        if not normalized_query:
            return False
        return any(
            normalized_query in value.lower()
            for value in (
                self.name,
                self.occasion.name,
                self.occasion.recipient.name,
            )
        )

    def is_affordable(self, max_price: int) -> bool:
        """Проверить, укладывается ли подарок в указанную цену."""
        return self.price <= max_price

    @classmethod
    def from_data(
        cls,
        data: Mapping[str, object],
        occasions: Mapping[int, Occasion],
    ) -> Gift:
        """Создать подарок из JSON и восстановить связь с событием."""
        gift_id = data.get("id")
        name = data.get("name")
        price = data.get("price")
        occasion_id = data.get("occasion_id")
        purchased = data.get("purchased", False)
        if (
            not isinstance(gift_id, int)
            or isinstance(gift_id, bool)
            or not isinstance(name, str)
            or not isinstance(price, int)
            or isinstance(price, bool)
            or not isinstance(occasion_id, int)
            or isinstance(occasion_id, bool)
            or not isinstance(purchased, bool)
        ):
            raise ValueError("некорректные данные подарка")
        occasion = occasions.get(occasion_id)
        if occasion is None:
            raise ValueError(
                f"для подарка #{gift_id} не найдено событие #{occasion_id}"
            )
        return cls(gift_id, name, price, occasion, purchased)

    def to_data(self) -> dict[str, object]:
        """Преобразовать подарок в данные для JSON."""
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "occasion_id": self.occasion.id,
            "purchased": self.purchased,
        }

    def __str__(self) -> str:
        """Вернуть строковое представление подарка."""
        return (
            f"#{self.id} | {self.occasion.recipient.name} | {self.name} | "
            f"{self.occasion.name} "
            f"({self.occasion.event_date:%d.%m.%Y}) | "
            f"{self.price} руб. | {self.status}"
        )
