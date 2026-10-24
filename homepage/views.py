"""Представления главной страницы и общей ошибки 404."""

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from giftservice.data import load_project_data


def index(request: HttpRequest) -> HttpResponse:
    """Показать главную страницу со статистикой списка подарков."""
    gift_list = load_project_data()
    total, purchased, total_price = gift_list.statistics()
    context = {
        "gift_list": gift_list,
        "total": total,
        "purchased": purchased,
        "planned": total - purchased,
        "total_price": total_price,
        "upcoming_occasions": sorted(
            gift_list.occasions,
            key=lambda occasion: occasion.event_date,
        )[:3],
    }
    return render(request, "homepage/index.html", context)


def page_not_found(
    request: HttpRequest,
    exception: Exception,
) -> HttpResponse:
    """Показать оформленную страницу для неизвестного URL."""
    return render(request, "404.html", status=404)
