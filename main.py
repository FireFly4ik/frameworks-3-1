"""Начальный сценарий сервиса формирования списка подарков."""

from datetime import date


def validate_gift(
    recipient: str,
    occasion: str,
    gift_name: str,
    occasion_date: date,
    price: int,
    budget: int,
) -> str:
    """Вернуть причину отказа или пустую строку, если данные корректны."""
    if not recipient.strip() or not occasion.strip() or not gift_name.strip():
        return "Получатель, повод и название подарка не должны быть пустыми."
    if occasion_date < date.today():
        return "Дата праздника не может быть в прошлом."
    if price <= 0 or budget <= 0:
        return "Цена подарка и бюджет должны быть положительными целыми числами."
    return ""


def calculate_budget_balance(price: int, budget: int) -> int:
    """Посчитать остаток бюджета после покупки подарка."""
    return budget - price


def format_gift_entry(
    recipient: str,
    occasion: str,
    gift_name: str,
    occasion_date: date,
    price: int,
    balance: int,
) -> str:
    """Сформировать первую запись будущего списка подарков."""
    return (
        "Список подарков\n"
        f"Получатель: {recipient.strip()}\n"
        f"Повод: {occasion.strip()} ({occasion_date:%d.%m.%Y})\n"
        f"Подарок: {gift_name.strip()}\n"
        f"Стоимость: {price} руб.\n"
        f"Остаток бюджета: {balance} руб."
    )


def main() -> None:
    print("Добавление подарка в список")
    recipient = input("Кому подарок: ")
    occasion = input("Повод: ")
    gift_name = input("Название подарка: ")

    try:
        occasion_date = date.fromisoformat(input("Дата праздника (ГГГГ-ММ-ДД): ").strip())
        price = int(input("Цена подарка (целые рубли): ").strip())
        budget = int(input("Бюджет (целые рубли): ").strip())
    except ValueError:
        print("Ошибка: проверьте дату (ГГГГ-ММ-ДД) и суммы в целых рублях.")
        return

    error = validate_gift(recipient, occasion, gift_name, occasion_date, price, budget)
    if error:
        print(f"Ошибка: {error}")
        return

    balance = calculate_budget_balance(price, budget)
    if balance < 0:
        print(f"Подарок не добавлен: бюджет превышен на {-balance} руб.")
        return

    print("\n" + format_gift_entry(
        recipient, occasion, gift_name, occasion_date, price, balance
    ))


if __name__ == "__main__":
    main()
