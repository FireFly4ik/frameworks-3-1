"""Подключение к отдельной SQLite-базе предметной области."""

from pathlib import Path
import sqlite3

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "giftlist.sqlite"


def get_connection(database_path: Path | None = None) -> sqlite3.Connection:
    """Открыть SQLite, включить внешние ключи и именованные строки."""
    connection = sqlite3.connect(database_path or DB_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection
