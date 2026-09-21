"""Консольный интерфейс сервиса формирования списка подарков."""

from pathlib import Path

from gifts import (
    Gift,
    add_gift,
    calculate_budget_balance,
    calculate_statistics,
    delete_gift,
    find_gifts,
    format_gift_entry,
    iter_affordable_gifts,
    mark_gift_purchased,
    sort_gifts,
)
from storage import load_gifts, save_gifts
from utils import input_date, input_int


DATA_FILE = Path(__file__).parent / "data" / "gifts.json"
MENU = """
=== Сервис формирования списка подарков ===
1. Показать все подарки
2. Добавить подарок
3. Найти подарки
4. Показать подарки в пределах цены
5. Отсортировать подарки
6. Отметить подарок купленным
7. Удалить подарок
8. Показать статистику
0. Выход
"""


def show_gifts(gifts: list[Gift]) -> None:
    """Вывести список подарков в консоль."""
    if not gifts:
        print("Список подарков пуст.")
        return

    for gift in gifts:
        print(format_gift_entry(gift))


def save_changes(gifts: list[Gift]) -> bool:
    """Сохранить подарки и сообщить об ошибке записи."""
    try:
        save_gifts(DATA_FILE, gifts)
    except ValueError as error:
        print(f"Ошибка сохранения: {error}")
        return False
    return True


def main() -> None:
    """Загрузить данные и выполнять команды меню до выхода пользователя."""
    try:
        gifts = load_gifts(DATA_FILE)
    except ValueError as error:
        print(f"Ошибка загрузки: {error}")
        return

    while True:
        print(MENU)
        choice = input("Выберите действие: ").strip()

        if choice == "0":
            print("До свидания!")
            break

        if choice == "1":
            show_gifts(gifts)
        elif choice == "2":
            recipient = input("Кому подарок: ").strip()
            occasion = input("Повод: ").strip()
            gift_name = input("Название подарка: ").strip()
            occasion_date = input_date("Дата праздника (ГГГГ-ММ-ДД): ")
            price = input_int("Цена подарка (целые рубли): ", minimum=1)
            try:
                gift = add_gift(
                    gifts,
                    recipient,
                    occasion,
                    gift_name,
                    occasion_date,
                    price,
                )
            except ValueError as error:
                print(f"Подарок не добавлен: {error}")
                continue
            if save_changes(gifts):
                print(f"Подарок «{gift['name']}» добавлен.")
        elif choice == "3":
            query = input("Имя, получатель или повод для поиска: ")
            show_gifts(find_gifts(gifts, query))
        elif choice == "4":
            max_price = input_int("Максимальная цена: ", minimum=1)
            show_gifts(list(iter_affordable_gifts(gifts, max_price)))
        elif choice == "5":
            sort_key = input("Сортировать по цене или дате: ").strip().lower()
            try:
                show_gifts(sort_gifts(gifts, sort_key))
            except ValueError as error:
                print(f"Ошибка: {error}")
        elif choice == "6":
            gift_id = input_int("Идентификатор подарка: ", minimum=1)
            if mark_gift_purchased(gifts, gift_id):
                save_changes(gifts)
                print("Подарок отмечен купленным.")
            else:
                print("Подарок с таким идентификатором не найден.")
        elif choice == "7":
            gift_id = input_int("Идентификатор подарка: ", minimum=1)
            if delete_gift(gifts, gift_id):
                save_changes(gifts)
                print("Подарок удалён.")
            else:
                print("Подарок с таким идентификатором не найден.")
        elif choice == "8":
            budget = input_int("Общий бюджет: ", minimum=1)
            total, purchased, total_price = calculate_statistics(gifts)
            balance = calculate_budget_balance(gifts, budget)
            print(f"Всего подарков: {total}")
            print(f"Куплено: {purchased}")
            print(f"Общая стоимость: {total_price} руб.")
            print(f"Остаток бюджета: {balance} руб.")
        else:
            print("Неизвестная команда. Выберите пункт от 0 до 8.")


if __name__ == "__main__":
    main()
