"""Представления главной страницы и общая разметка сайта."""

from django.http import HttpRequest, HttpResponse
from django.utils.html import escape

from giftservice.data import load_project_data


def page(title: str, content: str) -> str:
    """Собрать общий HTML-каркас страницы с Bootstrap и навигацией."""
    bootstrap = (
        "https://cdn.jsdelivr.net/npm/bootstrap@5.3.3"
        "/dist/css/bootstrap.min.css"
    )
    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{escape(title)}</title>
    <link rel="stylesheet" href="{bootstrap}">
    <style>
        body {{ background: #fffaf5; }}
        .navbar-brand {{ font-weight: 700; }}
        .hero {{ background: linear-gradient(135deg, #6f42c1, #d63384); }}
        .stat-card {{ border: 0; box-shadow: 0 0.5rem 1.5rem #30205014; }}
        .page-footer {{ color: #6c757d; border-top: 1px solid #e8dfd7; }}
    </style>
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <div class="container">
            <a class="navbar-brand" href="/">GiftList</a>
            <div class="navbar-nav flex-row gap-2">
                <a class="nav-link" href="/gifts/">Подарки</a>
                <a class="nav-link" href="/recipients/">Получатели</a>
                <a class="nav-link" href="/occasions/">События</a>
            </div>
        </div>
    </nav>
    <main class="container py-4">{content}</main>
    <footer class="page-footer container py-3 mt-4">
        Сервис формирования списка подарков · ПР5
    </footer>
</body>
</html>"""


def index(request: HttpRequest) -> HttpResponse:
    """Показать главную страницу со статистикой списка подарков."""
    gift_list = load_project_data()
    total, purchased, total_price = gift_list.statistics()
    planned = total - purchased
    upcoming = sorted(
        gift_list.occasions,
        key=lambda occasion: occasion.event_date,
    )[:3]
    event_items = "".join(
        f"""
        <li class="list-group-item d-flex justify-content-between gap-3">
            <a href="/occasions/{occasion.id}/">{escape(occasion.name)}</a>
            <span>{escape(occasion.recipient.name)} ·
            {occasion.event_date:%d.%m.%Y}</span>
        </li>
        """
        for occasion in upcoming
    )
    content = f"""
    <section class="hero text-white rounded-4 p-4 p-md-5 mb-4">
        <h1 class="display-5 fw-bold">{escape(gift_list.name)}</h1>
        <p class="lead mb-3">Планируйте подарки, события и бюджет в одном месте.</p>
        <a href="/gifts/" class="btn btn-light me-2">Открыть подарки</a>
        <a href="/recipients/" class="btn btn-outline-light">Получатели</a>
    </section>
    <section class="row g-3 mb-4" aria-label="Статистика">
        <div class="col-6 col-lg-3"><div class="card stat-card h-100">
            <div class="card-body"><div class="fs-3 fw-bold">{total}</div>
            <div>всего подарков</div></div></div></div>
        <div class="col-6 col-lg-3"><div class="card stat-card h-100">
            <div class="card-body"><div class="fs-3 fw-bold">{purchased}</div>
            <div>уже куплено</div></div></div></div>
        <div class="col-6 col-lg-3"><div class="card stat-card h-100">
            <div class="card-body"><div class="fs-3 fw-bold">{planned}</div>
            <div>запланировано</div></div></div></div>
        <div class="col-6 col-lg-3"><div class="card stat-card h-100">
            <div class="card-body"><div class="fs-3 fw-bold">
            {total_price:,} ₽</div><div>общая стоимость</div></div></div></div>
    </section>
    <section>
        <h2 class="h4">Ближайшие события</h2>
        <ul class="list-group">{event_items}</ul>
    </section>
    """.replace(",", " ")
    return HttpResponse(page("GiftList — главная", content))


def page_not_found(
    request: HttpRequest,
    exception: Exception,
) -> HttpResponse:
    """Показать оформленную страницу для неизвестного URL."""
    content = """
    <div class="text-center py-5">
        <div class="display-1 fw-bold text-danger">404</div>
        <h1 class="h2">Страница не найдена</h1>
        <p class="text-secondary">Проверьте адрес или вернитесь на главную.</p>
        <a href="/" class="btn btn-primary">На главную</a>
    </div>
    """
    return HttpResponse(page("404 — страница не найдена", content), status=404)
