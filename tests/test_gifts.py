from datetime import date, timedelta

import pytest

from gifts import (
    add_gift,
    calculate_budget_balance,
    calculate_statistics,
    delete_gift,
    find_gifts,
    iter_affordable_gifts,
    mark_gift_purchased,
    sort_gifts,
)


def make_gifts():
    gifts = []
    future = date.today() + timedelta(days=30)
    add_gift(gifts, "Анна", "День рождения", "Книга", future, 1500)
    add_gift(gifts, "Иван", "Новый год", "Наушники", future, 5000)
    return gifts


def test_add_gift_assigns_sequential_ids():
    gifts = make_gifts()

    assert [gift["id"] for gift in gifts] == [1, 2]


def test_add_gift_rejects_past_date():
    gifts = []
    past = date.today() - timedelta(days=1)

    with pytest.raises(ValueError, match="в прошлом"):
        add_gift(gifts, "Анна", "Праздник", "Книга", past, 1000)


def test_find_gifts_searches_different_fields_case_insensitively():
    gifts = make_gifts()

    assert find_gifts(gifts, "анна") == [gifts[0]]
    assert find_gifts(gifts, "НОВЫЙ") == [gifts[1]]


def test_filter_and_sort_gifts():
    gifts = make_gifts()

    assert list(iter_affordable_gifts(gifts, 2000)) == [gifts[0]]
    assert sort_gifts(gifts, "цена") == [gifts[0], gifts[1]]


def test_mark_delete_and_statistics():
    gifts = make_gifts()

    assert mark_gift_purchased(gifts, 1)
    assert calculate_statistics(gifts) == (2, 1, 6500)
    assert delete_gift(gifts, 2)
    assert calculate_statistics(gifts) == (1, 1, 1500)


def test_budget_balance_uses_all_gifts():
    gifts = make_gifts()

    assert calculate_budget_balance(gifts, 7000) == 500
