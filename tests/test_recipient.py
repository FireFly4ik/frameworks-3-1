import pytest

from models import Recipient


def test_recipient_creation_and_string():
    recipient = Recipient(1, "  Анна  ")

    assert recipient.id == 1
    assert recipient.name == "Анна"
    assert str(recipient) == "Получатель #1: Анна"


def test_recipient_from_data():
    recipient = Recipient.from_data({"id": 2, "name": "Иван"})

    assert recipient.to_data() == {"id": 2, "name": "Иван"}


def test_recipient_rejects_empty_name():
    with pytest.raises(ValueError, match="не должно быть пустым"):
        Recipient(1, "  ")
