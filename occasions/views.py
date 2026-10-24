"""Представления событий на данных SQLite."""

from contextlib import closing
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from db.database import get_connection


def occasion_list(request: HttpRequest) -> HttpResponse:
    """Показать события и получателей посредством JOIN."""
    with closing(get_connection()) as connection:
        occasions = connection.execute(
            """
            SELECT
                occasions.id,
                occasions.name,
                occasions.event_date,
                recipients.id AS recipient_id,
                recipients.name AS recipient_name
            FROM occasions
            JOIN recipients ON recipients.id = occasions.recipient_id
            ORDER BY occasions.event_date
            """
        ).fetchall()
    return render(
        request,
        "occasions/occasion_list.html",
        {"occasions": occasions},
    )


def occasion_detail(
    request: HttpRequest,
    occasion_id: int,
) -> HttpResponse:
    """Показать событие и его подарки из SQLite."""
    with closing(get_connection()) as connection:
        occasion = connection.execute(
            """
            SELECT
                occasions.id,
                occasions.name,
                occasions.event_date,
                recipients.id AS recipient_id,
                recipients.name AS recipient_name
            FROM occasions
            JOIN recipients ON recipients.id = occasions.recipient_id
            WHERE occasions.id = ?
            """,
            (occasion_id,),
        ).fetchone()
        gifts = connection.execute(
            """
            SELECT id, name, price, purchased
            FROM gifts
            WHERE occasion_id = ?
            ORDER BY price, name
            """,
            (occasion_id,),
        ).fetchall()
    return render(
        request,
        "occasions/occasion_detail.html",
        {"occasion": occasion, "gifts": gifts},
        status=404 if occasion is None else 200,
    )
