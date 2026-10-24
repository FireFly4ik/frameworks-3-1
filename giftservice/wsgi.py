"""WSGI-конфигурация Django-проекта."""

import os

from django.core.handlers.wsgi import WSGIHandler
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "giftservice.settings")

application: WSGIHandler = get_wsgi_application()
