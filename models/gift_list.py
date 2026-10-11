"""Сущность списка подарков и операции над его содержимым."""

from __future__ import annotations

from collections.abc import Iterable, Iterator
from datetime import date

from .gift import Gift
from .occasion import Occasion
from .recipient import Recipient


class GiftList:
    """Управляемая коллекция подарков, получателей и событий."""

    def __init__(
        self,
        gifts: Iterable[Gift] = (),
        list_id: int = 1,
        name: str = "Основной список",
    ) -> None:
        """Создать именованный список из существующих объектов Gift."""
        if list_id <= 0:
            raise ValueError("идентификатор списка должен быть положительным")
        normalized_name = name.strip()
        if not normalized_name:
            raise ValueError("название списка не должно быть пустым")
        self.id = list_id
        self.name = normalized_name
        self._gifts = list(gifts)
        gift_ids = [gift.id for gift in self._gifts]
        if len(gift_ids) != len(set(gift_ids)):
            raise ValueError("идентификаторы подарков должны быть уникальными")

    @property
    def items(self) -> tuple[Gift, ...]:
        """Вернуть неизменяемое представление списка подарков."""
        return tuple(self._gifts)

    @property
    def recipients(self) -> tuple[Recipient, ...]:
        """Вернуть уникальных получателей в порядке добавления."""
        recipients: dict[int, Recipient] = {}
        for gift in self._gifts:
            recipient = gift.occasion.recipient
            recipients.setdefault(recipient.id, recipient)
        return tuple(recipients.values())

    @property
    def occasions(self) -> tuple[Occasion, ...]:
        """Вернуть уникальные события в порядке добавления."""
        occasions: dict[int, Occasion] = {}
        for gift in self._gifts:
            occasion = gift.occasion
            occasions.setdefault(occasion.id, occasion)
        return tuple(occasions.values())

    def add_gift(
        self,
        recipient_name: str,
        occasion_name: str,
        gift_name: str,
        event_date: date,
        price: int,
    ) -> Gift:
        """Создать связанные объекты и добавить новый подарок."""
        Occasion.validate_event_date(event_date)
        normalized_recipient = recipient_name.strip()
        normalized_occasion = occasion_name.strip()
        if not normalized_recipient:
            raise ValueError("имя получателя не должно быть пустым")
        if not normalized_occasion:
            raise ValueError("название события не должно быть пустым")

        recipient = next(
            (
                item
                for item in self.recipients
                if item.name.lower() == normalized_recipient.lower()
            ),
            None,
        )
        if recipient is None:
            recipient_id = max(
                (item.id for item in self.recipients),
                default=0,
            ) + 1
            recipient = Recipient(recipient_id, normalized_recipient)

        occasion = next(
            (
                item
                for item in self.occasions
                if item.recipient.id == recipient.id
                and item.name.lower() == normalized_occasion.lower()
                and item.event_date == event_date
            ),
            None,
        )
        if occasion is None:
            occasion_id = max(
                (item.id for item in self.occasions),
                default=0,
            ) + 1
            occasion = Occasion(
                occasion_id,
                normalized_occasion,
                event_date,
                recipient,
            )

        gift_id = max((gift.id for gift in self._gifts), default=0) + 1
        gift = Gift(gift_id, gift_name, price, occasion)
        self._gifts.append(gift)
        return gift

    def find(self, query: str) -> list[Gift]:
        """Найти подарки по данным связанных объектов."""
        return [gift for gift in self._gifts if gift.matches(query)]

    def iter_affordable(self, max_price: int) -> Iterator[Gift]:
        """Последовательно вернуть подарки не дороже указанной суммы."""
        for gift in self._gifts:
            if gift.is_affordable(max_price):
                yield gift

    def sorted_by(self, sort_key: str) -> list[Gift]:
        """Вернуть подарки, отсортированные по цене или дате."""
        if sort_key == "цена":
            return sorted(self._gifts, key=lambda gift: gift.price)
        if sort_key == "дата":
            return sorted(
                self._gifts,
                key=lambda gift: gift.occasion.event_date,
            )
        raise ValueError("доступна сортировка только по цене или дате")

    def mark_purchased(self, gift_id: int) -> bool:
        """Найти подарок и изменить его состояние методом объекта."""
        for gift in self._gifts:
            if gift.id == gift_id:
                gift.mark_purchased()
                return True
        return False

    def delete(self, gift_id: int) -> bool:
        """Удалить подарок по идентификатору."""
        for gift in self._gifts:
            if gift.id == gift_id:
                self._gifts.remove(gift)
                return True
        return False

    def find_gift_by_id(self, gift_id: int) -> Gift | None:
        """Найти подарок по идентификатору."""
        return next((gift for gift in self._gifts if gift.id == gift_id), None)

    def find_recipient_by_id(self, recipient_id: int) -> Recipient | None:
        """Найти получателя по идентификатору."""
        return next(
            (item for item in self.recipients if item.id == recipient_id),
            None,
        )

    def find_occasion_by_id(self, occasion_id: int) -> Occasion | None:
        """Найти событие по идентификатору."""
        return next(
            (item for item in self.occasions if item.id == occasion_id),
            None,
        )

    def statistics(self) -> tuple[int, int, int]:
        """Вернуть количество, число покупок и общую стоимость."""
        purchased = sum(gift.purchased for gift in self._gifts)
        total_price = sum(gift.price for gift in self._gifts)
        return len(self._gifts), purchased, total_price

    def budget_balance(self, budget: int) -> int:
        """Посчитать остаток бюджета после покупки всех подарков."""
        return budget - sum(gift.price for gift in self._gifts)

    def to_data(self) -> dict[str, object]:
        """Преобразовать граф объектов в нормализованные данные JSON."""
        return {
            "gift_list": {"id": self.id, "name": self.name},
            "recipients": [item.to_data() for item in self.recipients],
            "occasions": [item.to_data() for item in self.occasions],
            "gifts": [gift.to_data() for gift in self._gifts],
        }

    def __iter__(self) -> Iterator[Gift]:
        """Перебирать подарки без доступа к внутреннему списку."""
        return iter(self._gifts)

    def __len__(self) -> int:
        """Вернуть количество подарков."""
        return len(self._gifts)

    def __str__(self) -> str:
        """Вернуть краткое описание списка."""
        return f"{self.name}: {len(self._gifts)} подарков"
