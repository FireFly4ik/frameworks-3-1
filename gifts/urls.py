"""URL-маршруты подарков."""

from django.urls import path

from . import views

app_name = "gifts"

urlpatterns = [
    path("", views.gift_list, name="list"),
    path("affordable/", views.affordable_gifts, name="affordable"),
    path("<int:gift_id>/", views.gift_detail, name="detail"),
]
