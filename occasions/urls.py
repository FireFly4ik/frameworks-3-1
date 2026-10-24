"""URL-маршруты событий."""

from django.urls import path

from . import views

app_name = "occasions"

urlpatterns = [
    path("", views.occasion_list, name="list"),
    path("<int:occasion_id>/", views.occasion_detail, name="detail"),
]
