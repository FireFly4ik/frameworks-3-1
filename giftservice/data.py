"""Доступ веб-слоя к данным объектной модели ПР3."""

from pathlib import Path

from django.conf import settings

from models import GiftList
from storage import load_gifts


def load_project_data() -> GiftList:
    """Загрузить объектную модель из общего JSON-файла проекта."""
    data_file = Path(settings.BASE_DIR) / "data" / "gifts.json"
    return load_gifts(data_file)
