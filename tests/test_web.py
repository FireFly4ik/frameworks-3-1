"""Проверки Django-маршрутов и веб-страниц ПР5."""

import pytest
from django.test import Client, override_settings
from django.urls import reverse


@pytest.fixture
def client() -> Client:
    """Создать тестовый HTTP-клиент Django."""
    return Client()


@pytest.mark.parametrize(
    ("route_name", "expected_text"),
    [
        ("homepage:index", "Подарки для семьи и друзей"),
        ("gifts:list", "Книга «Мастер и Маргарита»"),
        ("recipients:list", "Анна Петрова"),
        ("occasions:list", "Новоселье"),
    ],
)
def test_main_pages(
    client: Client,
    route_name: str,
    expected_text: str,
) -> None:
    """Основные страницы отвечают 200 и выводят данные JSON."""
    response = client.get(reverse(route_name))

    assert response.status_code == 200
    assert expected_text in response.content.decode()
    assert "bootstrap@5.3.3" in response.content.decode()


@pytest.mark.parametrize(
    ("route_name", "route_id", "expected_text"),
    [
        ("gifts:detail", 1, "Книга «Мастер и Маргарита»"),
        ("recipients:detail", 1, "Анна Петрова"),
        ("occasions:detail", 1, "День рождения"),
    ],
)
def test_detail_pages(
    client: Client,
    route_name: str,
    route_id: int,
    expected_text: str,
) -> None:
    """Динамические URL находят связанные объекты по ID."""
    response = client.get(reverse(route_name, args=[route_id]))

    assert response.status_code == 200
    assert expected_text in response.content.decode()


@pytest.mark.parametrize(
    "route_name",
    ["gifts:detail", "recipients:detail", "occasions:detail"],
)
def test_missing_entities_return_404(
    client: Client,
    route_name: str,
) -> None:
    """Несуществующий ID возвращает оформленный ответ HTTP 404."""
    response = client.get(reverse(route_name, args=[999]))

    assert response.status_code == 404
    assert "не найден" in response.content.decode().lower()
    assert "GiftList" in response.content.decode()


@override_settings(DEBUG=False)
def test_custom_404_page(client: Client) -> None:
    """Неизвестный маршрут обрабатывается пользовательской страницей."""
    response = client.get("/nonexistent/")

    assert response.status_code == 404
    assert "Страница не найдена" in response.content.decode()
    assert "На главную" in response.content.decode()


def test_navigation_links(client: Client) -> None:
    """Общий каркас содержит ссылки на основные разделы."""
    content = client.get(reverse("homepage:index")).content.decode()

    assert 'href="/gifts/"' in content
    assert 'href="/recipients/"' in content
    assert 'href="/occasions/"' in content
