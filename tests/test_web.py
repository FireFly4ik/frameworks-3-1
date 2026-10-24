"""Проверки Django-шаблонов, SQL-данных и страниц ПР7."""

from pathlib import Path

import pytest
import db.database
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
    """Основные страницы отвечают 200 и используют шаблоны с данными SQLite."""
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
        "gifts:affordable",
        "recipients:list",
        "occasions:list",
        "homepage:statistics",
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
            {"recipients": []},
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


def test_affordable_gifts_are_filtered_by_parameter(client: Client) -> None:
    """SQL-параметр цены ограничивает выдачу без подстановки в строку запроса."""
    response = client.get(reverse("gifts:affordable"), {"max_price": "2000"})
    content = response.content.decode()

    assert response.status_code == 200
    assert "Книга «Мастер и Маргарита»" in content
    assert "Комнатное растение" in content
    assert "Термокружка" not in content


def test_affordable_gifts_reject_invalid_parameter(client: Client) -> None:
    """Некорректный бюджет не выполняет SQL-запрос и даёт понятную ошибку."""
    response = client.get(reverse("gifts:affordable"), {"max_price": "-10"})

    assert response.status_code == 200
    assert "Максимальная цена должна быть положительным" in response.content.decode()


def test_statistics_page_contains_sql_aggregates(client: Client) -> None:
    """Страница статистики показывает результаты агрегатных SQL-запросов."""
    response = client.get(reverse("homepage:statistics"))
    content = response.content.decode()

    assert response.status_code == 200
    assert "Статистика подарков" in content
    assert "31 000" in content or "31000" in content
    assert "Анна Петрова" in content


def test_web_pages_read_from_sqlite(
    client: Client,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Изменение SQLite отражается в Django без чтения исходного JSON."""
    database_path = tmp_path / "giftlist.sqlite"
    database_path.write_bytes(db.database.DB_PATH.read_bytes())
    monkeypatch.setattr(db.database, "DB_PATH", database_path)

    with db.database.get_connection() as connection:
        connection.execute(
            "UPDATE gifts SET name = ? WHERE id = ?",
            ("SQL-подарок", 1),
        )

    content = client.get(reverse("gifts:list")).content.decode()
    assert "SQL-подарок" in content
    assert "Книга «Мастер и Маргарита»" not in content
