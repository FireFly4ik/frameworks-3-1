"""Конфигурация приложения событий."""

from django.apps import AppConfig


class OccasionsConfig(AppConfig):
    """Настроить приложение событий."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "occasions"
