"""Загрузка и сохранение данных сервиса в JSON-файле."""

import json
from pathlib import Path

from gifts import Gift


def load_gifts(filename: Path) -> list[Gift]:
    """Загрузить подарки; вернуть пустой список, если файла ещё нет."""
    try:
        with filename.open(encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError:
        return []
    except (json.JSONDecodeError, OSError) as error:
        message = f"не удалось прочитать {filename}: {error}"
        raise ValueError(message) from error

    if not isinstance(data, list):
        raise ValueError(f"в файле {filename} должен находиться список")
    if not all(isinstance(gift, dict) for gift in data):
        raise ValueError(f"в файле {filename} найдена некорректная запись")
    return data


def save_gifts(filename: Path, gifts: list[Gift]) -> None:
    """Сохранить подарки в JSON с использованием контекстного менеджера."""
    try:
        filename.parent.mkdir(parents=True, exist_ok=True)
        with filename.open("w", encoding="utf-8") as file:
            json.dump(gifts, file, ensure_ascii=False, indent=2)
    except OSError as error:
        raise ValueError(f"не удалось записать {filename}: {error}") from error
