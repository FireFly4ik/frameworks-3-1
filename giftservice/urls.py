"""Корневые URL-маршруты проекта."""

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("homepage.urls")),
    path("gifts/", include("gifts.urls")),
    path("recipients/", include("recipients.urls")),
    path("occasions/", include("occasions.urls")),
]

handler404 = "homepage.views.page_not_found"
