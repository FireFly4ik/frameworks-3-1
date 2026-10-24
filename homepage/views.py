"""Главная страница и статистика на данных SQLite."""

from contextlib import closing
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from db.database import get_connection


def index(request: HttpRequest) -> HttpResponse:
    """Показать сводку списка и ближайшие события из SQLite."""
    with closing(get_connection()) as connection:
        gift_list = connection.execute(
            "SELECT id, name FROM gift_lists ORDER BY id LIMIT 1"
        ).fetchone()
        statistics = connection.execute(
            """
            SELECT
                COUNT(*) AS total,
                COALESCE(SUM(purchased), 0) AS purchased,
                COALESCE(SUM(price), 0) AS total_price
            FROM gifts
            """
        ).fetchone()
        upcoming_occasions = connection.execute(
            """
            SELECT
                occasions.id,
                occasions.name,
                occasions.event_date,
                recipients.name AS recipient_name
            FROM occasions
            JOIN recipients ON recipients.id = occasions.recipient_id
            ORDER BY occasions.event_date
            LIMIT 3
            """
        ).fetchall()
    context = {
        "gift_list": gift_list,
        "total": statistics["total"],
        "purchased": statistics["purchased"],
        "planned": statistics["total"] - statistics["purchased"],
        "total_price": statistics["total_price"],
        "upcoming_occasions": upcoming_occasions,
    }
    return render(request, "homepage/index.html", context)


def statistics(request: HttpRequest) -> HttpResponse:
    """Показать агрегированную SQL-статистику по получателям."""
    with closing(get_connection()) as connection:
        summary = connection.execute(
            """
            SELECT
                COUNT(*) AS gifts_count,
                COALESCE(SUM(price), 0) AS total_price,
                COALESCE(SUM(purchased), 0) AS purchased_count,
                COALESCE(SUM(CASE WHEN purchased = 1 THEN price END), 0)
                    AS purchased_total
            FROM gifts
            """
        ).fetchone()
        recipients = connection.execute(
            """
            SELECT
                recipients.id,
                recipients.name,
                COUNT(gifts.id) AS gifts_count,
                COALESCE(SUM(gifts.price), 0) AS total_price,
                COALESCE(SUM(gifts.purchased), 0) AS purchased_count
            FROM recipients
            LEFT JOIN occasions ON occasions.recipient_id = recipients.id
            LEFT JOIN gifts ON gifts.occasion_id = occasions.id
            GROUP BY recipients.id, recipients.name
            ORDER BY total_price DESC, recipients.name
            """
        ).fetchall()
    return render(
        request,
        "homepage/statistics.html",
        {"summary": summary, "recipient_statistics": recipients},
    )


def page_not_found(
    request: HttpRequest,
    exception: Exception,
) -> HttpResponse:
    """Показать оформленную страницу для неизвестного URL."""
    return render(request, "404.html", status=404)
