"""Перенос проверенных данных проекта из JSON в SQLite."""

from pathlib import Path
import sqlite3

from db.database import BASE_DIR, DB_PATH, get_connection
from storage import load_gifts

DATA_FILE = BASE_DIR / "data" / "gifts.json"
SCHEMA_FILE = BASE_DIR / "sql" / "schema.sql"


def import_data(database_path: Path | None = None) -> None:
    """Пересоздать содержимое таблиц из текущего JSON-файла."""
    gift_list = load_gifts(DATA_FILE)
    connection = get_connection(database_path or DB_PATH)
    try:
        connection.executescript(SCHEMA_FILE.read_text(encoding="utf-8"))
        connection.execute("DELETE FROM gifts")
        connection.execute("DELETE FROM occasions")
        connection.execute("DELETE FROM recipients")
        connection.execute("DELETE FROM gift_lists")
        connection.execute(
            "INSERT INTO gift_lists (id, name) VALUES (?, ?)",
            (gift_list.id, gift_list.name),
        )
        connection.executemany(
            "INSERT INTO recipients (id, name) VALUES (?, ?)",
            [(item.id, item.name) for item in gift_list.recipients],
        )
        connection.executemany(
            """
            INSERT INTO occasions (id, name, event_date, recipient_id)
            VALUES (?, ?, ?, ?)
            """,
            [
                (
                    item.id,
                    item.name,
                    item.event_date.isoformat(),
                    item.recipient.id,
                )
                for item in gift_list.occasions
            ],
        )
        connection.executemany(
            """
            INSERT INTO gifts (
                id, name, price, purchased, gift_list_id, occasion_id
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            [
                (
                    gift.id,
                    gift.name,
                    gift.price,
                    int(gift.purchased),
                    gift_list.id,
                    gift.occasion.id,
                )
                for gift in gift_list
            ],
        )
        connection.commit()
    except (sqlite3.Error, ValueError):
        connection.rollback()
        raise
    finally:
        connection.close()


if __name__ == "__main__":
    import_data()
