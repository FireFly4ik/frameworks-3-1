"""Представления подарков на данных прямых SQL-запросов."""

from contextlib import closing
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from db.database import get_connection

GIFT_COLUMNS = """
    gifts.id,
    gifts.name,
    gifts.price,
    gifts.purchased,
    occasions.id AS occasion_id,
    occasions.name AS occasion_name,
    occasions.event_date,
    recipients.id AS recipient_id,
    recipients.name AS recipient_name
"""
GIFT_JOINS = """
    FROM gifts
    JOIN occasions ON occasions.id = gifts.occasion_id
    JOIN recipients ON recipients.id = occasions.recipient_id
"""


def gift_list(request: HttpRequest) -> HttpResponse:
    """Показать подарки из SQLite с данными связанных таблиц."""
    with closing(get_connection()) as connection:
        gift_list = connection.execute(
            "SELECT id, name FROM gift_lists ORDER BY id LIMIT 1"
        ).fetchone()
        gifts = connection.execute(
            f"SELECT {GIFT_COLUMNS} {GIFT_JOINS} "
            "ORDER BY occasions.event_date, gifts.name"
        ).fetchall()
    return render(
        request,
        "gifts/gift_list.html",
        {"gift_list": gift_list, "gifts": gifts},
    )


def affordable_gifts(request: HttpRequest) -> HttpResponse:
    """Найти подарки не дороже переданной параметром суммы."""
    raw_max_price = request.GET.get("max_price", "3000")
    error = ""
    gifts = []
    try:
        max_price = int(raw_max_price)
        if max_price <= 0:
            raise ValueError
    except ValueError:
        max_price = 3000
        error = "Максимальная цена должна быть положительным целым числом."
    else:
        with closing(get_connection()) as connection:
            gifts = connection.execute(
                f"SELECT {GIFT_COLUMNS} {GIFT_JOINS} "
                "WHERE gifts.price <= ? "
                "ORDER BY gifts.price, gifts.name",
                (max_price,),
            ).fetchall()
    return render(
        request,
        "gifts/affordable.html",
        {
            "gifts": gifts,
            "max_price": max_price,
            "raw_max_price": raw_max_price,
            "error": error,
        },
    )


def gift_detail(request: HttpRequest, gift_id: int) -> HttpResponse:
    """Показать подарок из SQLite или вернуть HTTP 404."""
    with closing(get_connection()) as connection:
        gift = connection.execute(
            f"SELECT {GIFT_COLUMNS} {GIFT_JOINS} WHERE gifts.id = ?",
            (gift_id,),
        ).fetchone()
    return render(
        request,
        "gifts/gift_detail.html",
        {"gift": gift},
        status=404 if gift is None else 200,
    )
