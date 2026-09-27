"""Загрузка и сохранение объектной модели в JSON-файле."""

from collections.abc import Mapping
from datetime import date
import json
from pathlib import Path
from typing import cast

from models import Gift, GiftList, Occasion, Recipient


def _as_mapping(value: object, label: str) -> Mapping[str, object]:
    """Проверить, что элемент JSON является объектом."""
    if not isinstance(value, dict):
        raise ValueError(f"некорректные данные: {label}")
    return cast(Mapping[str, object], value)


def load_gifts(filename: Path) -> GiftList:
    """Загрузить JSON, создать объекты и восстановить связи между ними."""
    try:
        with filename.open(encoding="utf-8") as file:
            raw_data: object = json.load(file)
    except FileNotFoundError:
        return GiftList()
    except (json.JSONDecodeError, OSError) as error:
        message = f"не удалось прочитать {filename}: {error}"
        raise ValueError(message) from error

    if isinstance(raw_data, list):
        legacy_gifts: list[Gift] = []
        for raw_gift in raw_data:
            data = _as_mapping(raw_gift, "подарок ПР2")
            gift_id = data.get("id")
            recipient_name = data.get("recipient")
            occasion_name = data.get("occasion")
            gift_name = data.get("name")
            raw_date = data.get("occasion_date")
            price = data.get("price")
            purchased = data.get("purchased", False)
            if (
                not isinstance(gift_id, int)
                or isinstance(gift_id, bool)
                or not isinstance(recipient_name, str)
                or not isinstance(occasion_name, str)
                or not isinstance(gift_name, str)
                or not isinstance(raw_date, str)
                or not isinstance(price, int)
                or isinstance(price, bool)
                or not isinstance(purchased, bool)
            ):
                raise ValueError("некорректная запись формата ПР2")
            try:
                event_date = date.fromisoformat(raw_date)
            except ValueError as error:
                raise ValueError("некорректная дата в формате ПР2") from error
            recipient = Recipient(gift_id, recipient_name)
            occasion = Occasion(
                gift_id,
                occasion_name,
                event_date,
                recipient,
            )
            legacy_gifts.append(
                Gift(gift_id, gift_name, price, occasion, purchased)
            )
        return GiftList(legacy_gifts)

    if not isinstance(raw_data, dict):
        raise ValueError(f"в файле {filename} должен находиться объект JSON")

    gift_list_data = _as_mapping(
        raw_data.get(
            "gift_list",
            {"id": 1, "name": "Основной список"},
        ),
        "список подарков",
    )
    gift_list_id = gift_list_data.get("id")
    gift_list_name = gift_list_data.get("name")
    if (
        not isinstance(gift_list_id, int)
        or isinstance(gift_list_id, bool)
        or not isinstance(gift_list_name, str)
    ):
        raise ValueError("некорректные данные списка подарков")

    recipients_data = raw_data.get("recipients")
    occasions_data = raw_data.get("occasions")
    gifts_data = raw_data.get("gifts")
    if (
        not isinstance(recipients_data, list)
        or not isinstance(occasions_data, list)
        or not isinstance(gifts_data, list)
    ):
        raise ValueError("JSON должен содержать списки recipients, occasions и gifts")

    recipients: dict[int, Recipient] = {}
    for raw_recipient in recipients_data:
        recipient = Recipient.from_data(
            _as_mapping(raw_recipient, "получатель")
        )
        if recipient.id in recipients:
            raise ValueError("идентификаторы получателей должны быть уникальными")
        recipients[recipient.id] = recipient

    occasions: dict[int, Occasion] = {}
    for raw_occasion in occasions_data:
        occasion = Occasion.from_data(
            _as_mapping(raw_occasion, "событие"),
            recipients,
        )
        if occasion.id in occasions:
            raise ValueError("идентификаторы событий должны быть уникальными")
        occasions[occasion.id] = occasion

    gifts: list[Gift] = []
    for raw_gift in gifts_data:
        gifts.append(
            Gift.from_data(
                _as_mapping(raw_gift, "подарок"),
                occasions,
            )
        )
    return GiftList(gifts, gift_list_id, gift_list_name)


def save_gifts(filename: Path, gift_list: GiftList) -> None:
    """Сохранить связанные объекты в нормализованный JSON."""
    try:
        filename.parent.mkdir(parents=True, exist_ok=True)
        with filename.open("w", encoding="utf-8") as file:
            json.dump(
                gift_list.to_data(),
                file,
                ensure_ascii=False,
                indent=2,
            )
    except OSError as error:
        raise ValueError(f"не удалось записать {filename}: {error}") from error
