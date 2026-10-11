"""URL-маршруты получателей."""

from django.urls import path

from . import views

app_name = "recipients"

urlpatterns = [
    path("", views.recipient_list, name="list"),
    path("<int:recipient_id>/", views.recipient_detail, name="detail"),
]
