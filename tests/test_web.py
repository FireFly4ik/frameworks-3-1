"""Проверки Django-шаблонов, маршрутов и страниц ПР6."""

from pathlib import Path

import pytest
from django.conf import settings
from django.template.loader import render_to_string
from django.test import Client, override_settings
from django.urls import reverse


@pytest.fixture
def client() -> Client:
    """Создать тестовый HTTP-клиент Django."""
    return Client()


@pytest.mark.parametrize(
    ("route_name", "template_name", "expected_text"),
    [
        ("homepage:index", "homepage/index.html", "Подарки для семьи и друзей"),
        ("gifts:list", "gifts/gift_list.html", "Книга «Мастер и Маргарита»"),
        ("recipients:list", "recipients/recipient_list.html", "Анна Петрова"),
        ("occasions:list", "occasions/occasion_list.html", "Новоселье"),
    ],
)
def test_main_pages_use_templates(
    client: Client,
    route_name: str,
    template_name: str,
    expected_text: str,
) -> None:
    """Основные страницы отвечают 200 и используют шаблоны с данными JSON."""
    response = client.get(reverse(route_name))
    content = response.content.decode()
    template_names = [template.name for template in response.templates]

    assert response.status_code == 200
    assert template_name in template_names
    assert "base.html" in template_names
    assert expected_text in content
    assert "bootstrap@5.3.3" in content


@pytest.mark.parametrize(
    ("route_name", "template_name", "route_id", "expected_text"),
    [
        ("gifts:detail", "gifts/gift_detail.html", 1, "Книга «Мастер и Маргарита»"),
        ("recipients:detail", "recipients/recipient_detail.html", 1, "Анна Петрова"),
        ("occasions:detail", "occasions/occasion_detail.html", 1, "День рождения"),
    ],
)
def test_detail_pages_use_templates(
    client: Client,
    route_name: str,
    template_name: str,
    route_id: int,
    expected_text: str,
) -> None:
    """Динамические URL передают объект в соответствующий шаблон."""
    response = client.get(reverse(route_name, args=[route_id]))

    assert response.status_code == 200
    assert template_name in [template.name for template in response.templates]
    assert expected_text in response.content.decode()


@pytest.mark.parametrize(
    ("route_name", "expected_text"),
    [
        ("gifts:detail", "Подарок не найден"),
        ("recipients:detail", "Получатель не найден"),
        ("occasions:detail", "Событие не найдено"),
    ],
)
def test_missing_entities_render_404(
    client: Client,
    route_name: str,
    expected_text: str,
) -> None:
    """Несуществующий ID обрабатывается условием шаблона и HTTP 404."""
    response = client.get(reverse(route_name, args=[999]))

    assert response.status_code == 404
    assert expected_text in response.content.decode()
    assert "GiftList" in response.content.decode()


@override_settings(DEBUG=False)
def test_custom_404_page_uses_template(client: Client) -> None:
    """Неизвестный маршрут обрабатывается общим шаблоном 404."""
    response = client.get("/nonexistent/")

    assert response.status_code == 404
    assert "404.html" in [template.name for template in response.templates]
    assert "Страница не найдена" in response.content.decode()
    assert "На главную" in response.content.decode()


def test_navigation_and_static_files(client: Client) -> None:
    """Базовый шаблон содержит именованные ссылки и статические ресурсы."""
    content = client.get(reverse("homepage:index")).content.decode()

    for route_name in (
        "gifts:list",
        "recipients:list",
        "occasions:list",
    ):
        assert f'href="{reverse(route_name)}"' in content
    assert "/static/homepage/css/style.css" in content
    assert "/static/homepage/img/logo.png" in content
    assert "/static/homepage/js/main.js" in content


@pytest.mark.parametrize(
    ("template_name", "context", "expected_text"),
    [
        (
            "gifts/gift_list.html",
            {"gift_list": None, "gifts": []},
            "Подарки не найдены",
        ),
        (
            "recipients/recipient_list.html",
            {"recipient_cards": []},
            "Получатели не найдены",
        ),
        (
            "occasions/occasion_list.html",
            {"occasions": []},
            "События не найдены",
        ),
    ],
)
def test_empty_collections_have_messages(
    template_name: str,
    context: dict[str, object],
    expected_text: str,
) -> None:
    """Теги for-empty показывают понятное состояние пустых коллекций."""
    content = render_to_string(template_name, context)

    assert expected_text in content


def test_static_files_exist() -> None:
    """CSS, JavaScript и изображение находятся в static приложения."""
    static_root = Path(settings.BASE_DIR) / "homepage" / "static" / "homepage"

    assert (static_root / "css" / "style.css").is_file()
    assert (static_root / "js" / "main.js").is_file()
    assert (static_root / "img" / "logo.png").is_file()
