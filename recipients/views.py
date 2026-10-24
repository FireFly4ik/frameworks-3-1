"""Представления списка и карточки получателя."""

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from giftservice.data import load_project_data


def recipient_list(request: HttpRequest) -> HttpResponse:
    """Показать получателей и сводные данные об их подарках."""
    gift_list = load_project_data()
    recipient_cards: list[dict[str, object]] = []
    for recipient in gift_list.recipients:
        gifts = [
            gift
            for gift in gift_list
            if gift.occasion.recipient.id == recipient.id
        ]
        recipient_cards.append(
            {
                "recipient": recipient,
                "gift_count": len(gifts),
                "total_price": sum(gift.price for gift in gifts),
            }
        )
    return render(
        request,
        "recipients/recipient_list.html",
        {"recipient_cards": recipient_cards},
    )


def recipient_detail(
    request: HttpRequest,
    recipient_id: int,
) -> HttpResponse:
    """Показать получателя и связанные с ним подарки."""
    gift_list = load_project_data()
    recipient = gift_list.find_recipient_by_id(recipient_id)
    gifts = (
        [
            gift
            for gift in gift_list
            if gift.occasion.recipient.id == recipient_id
        ]
        if recipient is not None
        else []
    )
    return render(
        request,
        "recipients/recipient_detail.html",
        {"recipient": recipient, "gifts": gifts},
        status=404 if recipient is None else 200,
    )
