"""Функции обработки списка подарков."""

from collections.abc import Iterator
from datetime import date
from typing import TypeAlias, cast


GiftValue: TypeAlias = str | int | bool
Gift: TypeAlias = dict[str, GiftValue]


def validate_gift(
    recipient: str,
    occasion: str,
    gift_name: str,
    occasion_date: date,
    price: int,
) -> None:
    """Проверить данные подарка и вызвать ValueError при ошибке."""
    if not recipient.strip() or not occasion.strip() or not gift_name.strip():
        raise ValueError(
            "получатель, повод и название подарка не должны быть пустыми"
        )
    if occasion_date < date.today():
        raise ValueError("дата праздника не может быть в прошлом")
    if price <= 0:
        raise ValueError("цена подарка должна быть положительным целым числом")


def add_gift(
    gifts: list[Gift],
    recipient: str,
    occasion: str,
    gift_name: str,
    occasion_date: date,
    price: int,
) -> Gift:
    """Проверить данные, добавить подарок и вернуть созданную запись."""
    validate_gift(recipient, occasion, gift_name, occasion_date, price)
    gift_ids = [cast(int, gift["id"]) for gift in gifts]
    gift: Gift = {
        "id": max(gift_ids, default=0) + 1,
        "recipient": recipient.strip(),
        "occasion": occasion.strip(),
        "name": gift_name.strip(),
        "occasion_date": occasion_date.isoformat(),
        "price": price,
        "purchased": False,
    }
    gifts.append(gift)
    return gift


def find_gifts(gifts: list[Gift], query: str) -> list[Gift]:
    """Найти подарки по названию, получателю или поводу без учёта регистра."""
    normalized_query = query.strip().lower()
    if not normalized_query:
        return []

    result = []
    for gift in gifts:
        searchable_fields = (
            cast(str, gift["name"]),
            cast(str, gift["recipient"]),
            cast(str, gift["occasion"]),
        )
        matches = (
            normalized_query in field.lower() for field in searchable_fields
        )
        if any(matches):
            result.append(gift)
    return result


def iter_affordable_gifts(
    gifts: list[Gift], max_price: int
) -> Iterator[Gift]:
    """Последовательно вернуть подарки не дороже указанной суммы."""
    for gift in gifts:
        if cast(int, gift["price"]) <= max_price:
            yield gift


def sort_gifts(gifts: list[Gift], sort_key: str) -> list[Gift]:
    """Вернуть новый список подарков, отсортированный по цене или дате."""
    if sort_key == "цена":
        return sorted(gifts, key=lambda gift: cast(int, gift["price"]))
    if sort_key == "дата":
        return sorted(gifts, key=lambda gift: cast(str, gift["occasion_date"]))
    raise ValueError("доступна сортировка только по цене или дате")


def mark_gift_purchased(gifts: list[Gift], gift_id: int) -> bool:
    """Отметить подарок купленным и вернуть признак успешного поиска."""
    for gift in gifts:
        if gift["id"] == gift_id:
            gift["purchased"] = True
            return True
    return False


def delete_gift(gifts: list[Gift], gift_id: int) -> bool:
    """Удалить подарок по идентификатору."""
    for gift in gifts:
        if gift["id"] == gift_id:
            gifts.remove(gift)
            return True
    return False


def calculate_statistics(gifts: list[Gift]) -> tuple[int, int, int]:
    """Вернуть количество подарков, купленных подарков и общую стоимость."""
    purchased = 0
    total_price = 0
    for gift in gifts:
        total_price += cast(int, gift["price"])
        if cast(bool, gift["purchased"]):
            purchased += 1
    return len(gifts), purchased, total_price


def calculate_budget_balance(gifts: list[Gift], budget: int) -> int:
    """Посчитать остаток общего бюджета после покупки всех подарков."""
    return budget - sum(cast(int, gift["price"]) for gift in gifts)


def format_gift_entry(gift: Gift) -> str:
    """Сформировать строку для вывода одной записи списка подарков."""
    purchased = "куплен" if cast(bool, gift["purchased"]) else "запланирован"
    gift_date = date.fromisoformat(cast(str, gift["occasion_date"]))
    return (
        f"#{gift['id']} | {gift['recipient']} | {gift['name']} | "
        f"{gift['occasion']} ({gift_date:%d.%m.%Y}) | "
        f"{gift['price']} руб. | {purchased}"
    )
