"""Представления списка и карточки события."""

from django.http import HttpRequest, HttpResponse
from django.utils.html import escape

from giftservice.data import load_project_data
from homepage.views import page


def occasion_list(request: HttpRequest) -> HttpResponse:
    """Показать события в хронологическом порядке."""
    occasions = sorted(
        load_project_data().occasions,
        key=lambda occasion: occasion.event_date,
    )
    items = "".join(
        f"""
        <a class="list-group-item list-group-item-action
           d-flex justify-content-between gap-3"
           href="/occasions/{occasion.id}/">
            <div><h2 class="h5 mb-1">{escape(occasion.name)}</h2>
            <span>{escape(occasion.recipient.name)}</span></div>
            <time datetime="{occasion.event_date.isoformat()}">
            {occasion.event_date:%d.%m.%Y}</time>
        </a>
        """
        for occasion in occasions
    )
    content = f"""
    <h1>События</h1>
    <p class="text-secondary">Поводы для подготовки подарков.</p>
    <div class="list-group">{items}</div>
    """
    return HttpResponse(page("GiftList — события", content))


def occasion_detail(
    request: HttpRequest,
    occasion_id: int,
) -> HttpResponse:
    """Показать событие и связанные подарки."""
    gift_list_data = load_project_data()
    occasion = gift_list_data.find_occasion_by_id(occasion_id)
    if occasion is None:
        content = """
        <h1 class="text-danger">Событие не найдено</h1>
        <a href="/occasions/" class="btn btn-outline-secondary">
        ← К событиям</a>
        """
        return HttpResponse(page("Событие не найдено", content), status=404)

    gifts = [gift for gift in gift_list_data if gift.occasion.id == occasion.id]
    gift_items = "".join(
        f"""
        <a href="/gifts/{gift.id}/" class="list-group-item
           list-group-item-action d-flex justify-content-between">
            <span>{escape(gift.name)}</span><strong>{gift.price:,} ₽</strong>
        </a>
        """.replace(",", " ")
        for gift in gifts
    )
    content = f"""
    <div class="card border-0 shadow-sm">
        <div class="card-body p-4">
            <h1>{escape(occasion.name)}</h1>
            <p><strong>Дата:</strong> {occasion.event_date:%d.%m.%Y}</p>
            <p><strong>Получатель:</strong>
                <a href="/recipients/{occasion.recipient.id}/">
                {escape(occasion.recipient.name)}</a></p>
            <h2 class="h5 mt-4">Подарки к событию</h2>
            <div class="list-group mb-4">{gift_items}</div>
            <a href="/occasions/" class="btn btn-outline-secondary">
            ← К событиям</a>
        </div>
    </div>
    """
    return HttpResponse(page(occasion.name, content))
