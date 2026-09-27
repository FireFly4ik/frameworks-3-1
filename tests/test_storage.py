from datetime import date
import json

import pytest

from models import Gift, GiftList, Occasion, Recipient
from storage import load_gifts, save_gifts


def make_gift_list():
    recipient = Recipient(1, "Анна")
    occasion = Occasion(1, "День рождения", date(2027, 2, 3), recipient)
    return GiftList(
        [
            Gift(1, "Книга", 1500, occasion),
            Gift(2, "Наушники", 5000, occasion, purchased=True),
        ]
    )


def test_save_and_load_restores_object_graph(tmp_path):
    filename = tmp_path / "nested" / "gifts.json"

    save_gifts(filename, make_gift_list())
    restored = load_gifts(filename)
    first, second = restored.items

    assert restored.id == 1
    assert restored.name == "Основной список"
    assert first.occasion is second.occasion
    assert first.occasion.recipient is second.occasion.recipient
    assert second.purchased
    assert restored.statistics() == (2, 1, 6500)


def test_load_missing_file_returns_empty_gift_list(tmp_path):
    restored = load_gifts(tmp_path / "missing.json")

    assert len(restored) == 0


def test_load_invalid_json_reports_error(tmp_path):
    filename = tmp_path / "gifts.json"
    filename.write_text("not json", encoding="utf-8")

    with pytest.raises(ValueError, match="не удалось прочитать"):
        load_gifts(filename)


def test_load_rejects_broken_object_reference(tmp_path):
    filename = tmp_path / "gifts.json"
    filename.write_text(
        json.dumps(
            {
                "recipients": [],
                "occasions": [
                    {
                        "id": 1,
                        "name": "Праздник",
                        "event_date": "2027-01-01",
                        "recipient_id": 99,
                    }
                ],
                "gifts": [],
            }
        ),
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="не найден получатель"):
        load_gifts(filename)


def test_load_migrates_pr2_list_format(tmp_path):
    filename = tmp_path / "gifts.json"
    filename.write_text(
        json.dumps(
            [
                {
                    "id": 1,
                    "recipient": "Анна",
                    "occasion": "День рождения",
                    "name": "Книга",
                    "occasion_date": "2027-02-03",
                    "price": 1500,
                    "purchased": False,
                }
            ],
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    restored = load_gifts(filename)

    assert restored.items[0].occasion.recipient.name == "Анна"
    assert restored.items[0].name == "Книга"
