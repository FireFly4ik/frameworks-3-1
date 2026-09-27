from datetime import date, timedelta

import pytest

from models import Occasion, Recipient


def test_occasion_links_recipient_and_formats_string():
    recipient = Recipient(1, "Анна")
    event_date = date(2027, 1, 2)
    occasion = Occasion(1, "День рождения", event_date, recipient)

    assert occasion.recipient is recipient
    assert str(occasion) == "День рождения для Анна (02.01.2027)"


def test_occasion_from_data_restores_recipient_reference():
    recipient = Recipient(3, "Иван")
    occasion = Occasion.from_data(
        {
            "id": 4,
            "name": "Новый год",
            "event_date": "2027-01-01",
            "recipient_id": 3,
        },
        {recipient.id: recipient},
    )

    assert occasion.recipient is recipient
    assert occasion.event_date == date(2027, 1, 1)


def test_occasion_rejects_past_date_for_new_event():
    yesterday = date.today() - timedelta(days=1)

    with pytest.raises(ValueError, match="в прошлом"):
        Occasion.validate_event_date(yesterday)
