"""Конфигурация приложения подарков."""

from django.apps import AppConfig


class GiftsConfig(AppConfig):
    """Настроить приложение подарков."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "gifts"
