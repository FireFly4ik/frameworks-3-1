"""Представления получателей на данных SQLite."""

from contextlib import closing
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from db.database import get_connection


def recipient_list(request: HttpRequest) -> HttpResponse:
    """Показать получателей с агрегатами SQL."""
    with closing(get_connection()) as connection:
        recipients = connection.execute(
            """
            SELECT
                recipients.id,
                recipients.name,
                COUNT(gifts.id) AS gift_count,
                COALESCE(SUM(gifts.price), 0) AS total_price
            FROM recipients
            LEFT JOIN occasions ON occasions.recipient_id = recipients.id
            LEFT JOIN gifts ON gifts.occasion_id = occasions.id
            GROUP BY recipients.id, recipients.name
            ORDER BY recipients.name
            """
        ).fetchall()
    return render(
        request,
        "recipients/recipient_list.html",
        {"recipients": recipients},
    )


def recipient_detail(
    request: HttpRequest,
    recipient_id: int,
) -> HttpResponse:
    """Показать получателя и его подарки из связанных таблиц."""
    with closing(get_connection()) as connection:
        recipient = connection.execute(
            "SELECT id, name FROM recipients WHERE id = ?",
            (recipient_id,),
        ).fetchone()
        gifts = connection.execute(
            """
            SELECT
                gifts.id,
                gifts.name,
                gifts.price,
                gifts.purchased,
                occasions.id AS occasion_id,
                occasions.name AS occasion_name,
                occasions.event_date
            FROM gifts
            JOIN occasions ON occasions.id = gifts.occasion_id
            WHERE occasions.recipient_id = ?
            ORDER BY occasions.event_date, gifts.name
            """,
            (recipient_id,),
        ).fetchall()
    return render(
        request,
        "recipients/recipient_detail.html",
        {"recipient": recipient, "gifts": gifts},
        status=404 if recipient is None else 200,
    )
