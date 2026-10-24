"""Представления списка и карточки события."""

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from giftservice.data import load_project_data


def occasion_list(request: HttpRequest) -> HttpResponse:
    """Показать события в хронологическом порядке."""
    occasions = sorted(
        load_project_data().occasions,
        key=lambda occasion: occasion.event_date,
    )
    return render(
        request,
        "occasions/occasion_list.html",
        {"occasions": occasions},
    )


def occasion_detail(
    request: HttpRequest,
    occasion_id: int,
) -> HttpResponse:
    """Показать событие и связанные подарки."""
    gift_list = load_project_data()
    occasion = gift_list.find_occasion_by_id(occasion_id)
    gifts = (
        [gift for gift in gift_list if gift.occasion.id == occasion_id]
        if occasion is not None
        else []
    )
    return render(
        request,
        "occasions/occasion_detail.html",
        {"occasion": occasion, "gifts": gifts},
        status=404 if occasion is None else 200,
    )
