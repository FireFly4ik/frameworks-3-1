"""Представления списка и карточки подарка."""

from django.http import HttpRequest, HttpResponse
from django.utils.html import escape

from giftservice.data import load_project_data
from homepage.views import page


def gift_list(request: HttpRequest) -> HttpResponse:
    """Показать подарки из JSON-хранилища ПР3."""
    gift_list_data = load_project_data()
    items = "".join(
        f"""
        <a class="list-group-item list-group-item-action"
           href="/gifts/{gift.id}/">
            <div class="d-flex justify-content-between align-items-start gap-3">
                <div>
                    <h2 class="h5 mb-1">{escape(gift.name)}</h2>
                    <div>{escape(gift.occasion.recipient.name)} ·
                    {escape(gift.occasion.name)} ·
                    {gift.occasion.event_date:%d.%m.%Y}</div>
                </div>
                <div class="text-end">
                    <div class="fw-bold">{gift.price:,} ₽</div>
                    <span class="badge
                    {'bg-success' if gift.purchased else 'bg-warning text-dark'}">
                    {escape(gift.status)}</span>
                </div>
            </div>
        </a>
        """.replace(",", " ")
        for gift in gift_list_data.sorted_by("дата")
    )
    content = f"""
    <div class="d-flex justify-content-between align-items-center mb-3">
        <div><h1>Подарки</h1>
        <p class="text-secondary mb-0">Данные загружены из data/gifts.json.</p></div>
        <span class="badge bg-primary fs-6">{len(gift_list_data)}</span>
    </div>
    <div class="list-group">{items}</div>
    """
    return HttpResponse(page("GiftList — подарки", content))


def gift_detail(request: HttpRequest, gift_id: int) -> HttpResponse:
    """Показать подарок по идентификатору или вернуть HTTP 404."""
    gift = load_project_data().find_gift_by_id(gift_id)
    if gift is None:
        content = """
        <h1 class="text-danger">Подарок не найден</h1>
        <p>Подарка с таким идентификатором нет в списке.</p>
        <a href="/gifts/" class="btn btn-outline-secondary">← К подаркам</a>
        """
        return HttpResponse(page("Подарок не найден", content), status=404)

    badge = "bg-success" if gift.purchased else "bg-warning text-dark"
    content = f"""
    <div class="card border-0 shadow-sm">
        <div class="card-body p-4">
            <div class="d-flex justify-content-between gap-3">
                <h1 class="h2">{escape(gift.name)}</h1>
                <span class="badge {badge} align-self-start">
                {escape(gift.status)}</span>
            </div>
            <dl class="row mb-4">
                <dt class="col-sm-4">Идентификатор</dt>
                <dd class="col-sm-8">#{gift.id}</dd>
                <dt class="col-sm-4">Цена</dt><dd class="col-sm-8">{gift.price:,} ₽</dd>
                <dt class="col-sm-4">Получатель</dt><dd class="col-sm-8">
                    <a href="/recipients/{gift.occasion.recipient.id}/">
                    {escape(gift.occasion.recipient.name)}</a></dd>
                <dt class="col-sm-4">Событие</dt><dd class="col-sm-8">
                    <a href="/occasions/{gift.occasion.id}/">
                    {escape(gift.occasion.name)}</a></dd>
                <dt class="col-sm-4">Дата</dt><dd class="col-sm-8">
                    {gift.occasion.event_date:%d.%m.%Y}</dd>
            </dl>
            <a href="/gifts/" class="btn btn-outline-secondary">← К подаркам</a>
        </div>
    </div>
    """.replace(",", " ")
    return HttpResponse(page(gift.name, content))
