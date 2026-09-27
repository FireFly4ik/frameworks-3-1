from datetime import date

from models import Gift, Occasion, Recipient


def make_gift():
    recipient = Recipient(1, "Анна")
    occasion = Occasion(1, "День рождения", date(2027, 2, 3), recipient)
    return Gift(1, "Книга", 1500, occasion)


def test_gift_methods_and_string():
    gift = make_gift()

    assert gift.matches("анна")
    assert gift.matches("РОЖДЕНИЯ")
    assert gift.is_affordable(2000)
    assert gift.status == "запланирован"
    assert "Книга" in str(gift)

    gift.mark_purchased()

    assert gift.purchased
    assert gift.status == "куплен"


def test_gift_from_data_restores_occasion_reference():
    gift = make_gift()
    restored = Gift.from_data(
        {
            "id": 2,
            "name": "Наушники",
            "price": 5000,
            "occasion_id": gift.occasion.id,
            "purchased": True,
        },
        {gift.occasion.id: gift.occasion},
    )

    assert restored.occasion is gift.occasion
    assert restored.purchased
    assert restored.to_data()["occasion_id"] == gift.occasion.id
