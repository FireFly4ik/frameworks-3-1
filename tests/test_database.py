"""Проверки схемы, импорта и SQL-запросов ПР7."""

from pathlib import Path
import sqlite3

import pytest

from db.database import get_connection
from db.import_json import import_data


@pytest.fixture
def database_path(tmp_path: Path) -> Path:
    """Создать отдельную тестовую базу из исходного JSON."""
    path = tmp_path / "giftlist.sqlite"
    import_data(path)
    return path


def test_json_import_creates_all_entities(database_path: Path) -> None:
    """Импорт сохраняет все четыре сущности в отдельных таблицах."""
    with get_connection(database_path) as connection:
        counts = {
            table: connection.execute(
                f"SELECT COUNT(*) FROM {table}"
            ).fetchone()[0]
            for table in ("gift_lists", "recipients", "occasions", "gifts")
        }

    assert counts == {
        "gift_lists": 1,
        "recipients": 4,
        "occasions": 5,
        "gifts": 8,
    }


def test_foreign_keys_are_valid_and_enforced(database_path: Path) -> None:
    """Связи не нарушены, а подарок без события добавить нельзя."""
    with get_connection(database_path) as connection:
        assert connection.execute("PRAGMA foreign_key_check").fetchall() == []
        with pytest.raises(sqlite3.IntegrityError):
            connection.execute(
                """
                INSERT INTO gifts (
                    id, name, price, purchased, gift_list_id, occasion_id
                )
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (999, "Подарок без события", 100, 0, 1, 999),
            )


def test_join_and_aggregate_queries(database_path: Path) -> None:
    """JOIN и агрегаты возвращают проверяемые результаты предметной области."""
    with get_connection(database_path) as connection:
        summary = connection.execute(
            """
            SELECT COUNT(*) AS gifts_count, SUM(price) AS total_price,
                   SUM(purchased) AS purchased_count
            FROM gifts
            """
        ).fetchone()
        joined_gift = connection.execute(
            """
            SELECT gifts.name, occasions.name AS occasion_name,
                   recipients.name AS recipient_name, gift_lists.name AS list_name
            FROM gifts
            JOIN gift_lists ON gift_lists.id = gifts.gift_list_id
            JOIN occasions ON occasions.id = gifts.occasion_id
            JOIN recipients ON recipients.id = occasions.recipient_id
            WHERE gifts.id = ?
            """,
            (1,),
        ).fetchone()

    assert dict(summary) == {
        "gifts_count": 8,
        "total_price": 31000,
        "purchased_count": 3,
    }
    assert dict(joined_gift) == {
        "name": "Книга «Мастер и Маргарита»",
        "occasion_name": "День рождения",
        "recipient_name": "Анна Петрова",
        "list_name": "Подарки для семьи и друзей",
    }


def test_import_is_repeatable(database_path: Path) -> None:
    """Повторный импорт не дублирует строки и восстанавливает JSON-данные."""
    with get_connection(database_path) as connection:
        connection.execute("UPDATE gifts SET name = ? WHERE id = ?", ("Изменено", 1))

    import_data(database_path)

    with get_connection(database_path) as connection:
        gift = connection.execute(
            "SELECT name FROM gifts WHERE id = ?", (1,)
        ).fetchone()
        count = connection.execute("SELECT COUNT(*) FROM gifts").fetchone()[0]

    assert gift["name"] == "Книга «Мастер и Маргарита»"
    assert count == 8
