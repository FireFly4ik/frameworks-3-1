"""Представления списка и карточки подарка."""

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from giftservice.data import load_project_data


def gift_list(request: HttpRequest) -> HttpResponse:
    """Показать подарки из JSON-хранилища ПР3."""
    gift_list_data = load_project_data()
    context = {
        "gift_list": gift_list_data,
        "gifts": gift_list_data.sorted_by("дата"),
    }
    return render(request, "gifts/gift_list.html", context)


def gift_detail(request: HttpRequest, gift_id: int) -> HttpResponse:
    """Показать подарок по идентификатору или вернуть HTTP 404."""
    gift = load_project_data().find_gift_by_id(gift_id)
    return render(
        request,
        "gifts/gift_detail.html",
        {"gift": gift},
        status=404 if gift is None else 200,
    )
