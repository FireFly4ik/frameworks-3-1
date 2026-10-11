"""Конфигурация приложения получателей."""

from django.apps import AppConfig


class RecipientsConfig(AppConfig):
    """Настроить приложение получателей."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "recipients"
