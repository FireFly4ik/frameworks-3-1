from datetime import date, timedelta

import pytest

from models import GiftList


def make_gift_list():
    gift_list = GiftList()
    event_date = date.today() + timedelta(days=30)
    first = gift_list.add_gift(
        "Анна",
        "День рождения",
        "Книга",
        event_date,
        1500,
    )
    second = gift_list.add_gift(
        "Анна",
        "День рождения",
        "Наушники",
        event_date,
        5000,
    )
    return gift_list, first, second


def test_add_gifts_reuses_related_objects_and_assigns_ids():
    gift_list, first, second = make_gift_list()

    assert gift_list.id == 1
    assert gift_list.name == "Основной список"
    assert str(gift_list) == "Основной список: 2 подарков"
    assert [gift.id for gift in gift_list] == [1, 2]
    assert first.occasion is second.occasion
    assert first.occasion.recipient is second.occasion.recipient
    assert len(gift_list.recipients) == 1
    assert len(gift_list.occasions) == 1


def test_search_filter_and_sort_preserve_pr2_features():
    gift_list, first, second = make_gift_list()

    assert gift_list.find("анна") == [first, second]
    assert list(gift_list.iter_affordable(2000)) == [first]
    assert gift_list.sorted_by("цена") == [first, second]
    assert gift_list.sorted_by("дата") == [first, second]


def test_invalid_sort_key_is_reported():
    gift_list, _, _ = make_gift_list()

    with pytest.raises(ValueError, match="только по цене или дате"):
        gift_list.sorted_by("название")


def test_mark_delete_statistics_and_budget():
    gift_list, first, second = make_gift_list()

    assert gift_list.mark_purchased(first.id)
    assert gift_list.statistics() == (2, 1, 6500)
    assert gift_list.budget_balance(7000) == 500
    assert gift_list.delete(second.id)
    assert gift_list.statistics() == (1, 1, 1500)


def test_add_gift_rejects_past_date():
    gift_list = GiftList()

    with pytest.raises(ValueError, match="в прошлом"):
        gift_list.add_gift(
            "Анна",
            "Праздник",
            "Книга",
            date.today() - timedelta(days=1),
            1000,
        )
