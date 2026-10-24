"""Представления списка и карточки получателя."""

from django.http import HttpRequest, HttpResponse
from django.utils.html import escape

from giftservice.data import load_project_data
from homepage.views import page


def recipient_list(request: HttpRequest) -> HttpResponse:
    """Показать получателей и их запланированные подарки."""
    gift_list_data = load_project_data()
    cards = ""
    for recipient in gift_list_data.recipients:
        gifts = [
            gift
            for gift in gift_list_data
            if gift.occasion.recipient.id == recipient.id
        ]
        total_price = sum(gift.price for gift in gifts)
        cards += f"""
        <div class="col-md-6">
            <a class="card h-100 text-decoration-none text-body shadow-sm"
               href="/recipients/{recipient.id}/">
                <div class="card-body">
                    <h2 class="h5">{escape(recipient.name)}</h2>
                    <p class="mb-1">Подарков: {len(gifts)}</p>
                    <p class="mb-0 text-secondary">Бюджет: {total_price:,} ₽</p>
                </div>
            </a>
        </div>
        """.replace(",", " ")
    content = f"""
    <h1>Получатели</h1>
    <p class="text-secondary">Люди, для которых запланированы подарки.</p>
    <div class="row g-3">{cards}</div>
    """
    return HttpResponse(page("GiftList — получатели", content))


def recipient_detail(
    request: HttpRequest,
    recipient_id: int,
) -> HttpResponse:
    """Показать получателя и связанные с ним подарки."""
    gift_list_data = load_project_data()
    recipient = gift_list_data.find_recipient_by_id(recipient_id)
    if recipient is None:
        content = """
        <h1 class="text-danger">Получатель не найден</h1>
        <a href="/recipients/" class="btn btn-outline-secondary">
        ← К получателям</a>
        """
        return HttpResponse(page("Получатель не найден", content), status=404)

    gifts = [
        gift
        for gift in gift_list_data
        if gift.occasion.recipient.id == recipient.id
    ]
    rows = "".join(
        f"""
        <tr>
            <td><a href="/gifts/{gift.id}/">{escape(gift.name)}</a></td>
            <td><a href="/occasions/{gift.occasion.id}/">
            {escape(gift.occasion.name)}</a></td>
            <td>{gift.price:,} ₽</td>
            <td>{escape(gift.status)}</td>
        </tr>
        """.replace(",", " ")
        for gift in gifts
    )
    content = f"""
    <h1>{escape(recipient.name)}</h1>
    <p class="text-secondary">Получатель #{recipient.id}</p>
    <div class="table-responsive"><table class="table table-hover align-middle">
        <thead><tr><th>Подарок</th><th>Событие</th>
        <th>Цена</th><th>Статус</th></tr></thead>
        <tbody>{rows}</tbody>
    </table></div>
    <a href="/recipients/" class="btn btn-outline-secondary">← К получателям</a>
    """
    return HttpResponse(page(recipient.name, content))
