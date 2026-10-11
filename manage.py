#!/usr/bin/env python
"""Командная утилита Django-проекта."""

import os
import sys


def main() -> None:
    """Запустить команду управления Django."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "giftservice.settings")
    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
