"""Консольный интерфейс сервиса формирования списка подарков."""

from collections.abc import Iterable
from pathlib import Path

from models import Gift, GiftList
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


def show_gifts(gifts: Iterable[Gift]) -> None:
    """Вывести коллекцию объектов Gift в консоль."""
    items = list(gifts)
    if not items:
        print("Список подарков пуст.")
        return
    for gift in items:
        print(gift)


def save_changes(gift_list: GiftList) -> bool:
    """Сохранить объектную модель и сообщить об ошибке записи."""
    try:
        save_gifts(DATA_FILE, gift_list)
    except ValueError as error:
        print(f"Ошибка сохранения: {error}")
        return False
    return True


def main() -> None:
    """Загрузить список подарков и выполнять команды до выхода."""
    try:
        gift_list = load_gifts(DATA_FILE)
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
            show_gifts(gift_list)
        elif choice == "2":
            recipient = input("Кому подарок: ").strip()
            occasion = input("Повод: ").strip()
            gift_name = input("Название подарка: ").strip()
            event_date = input_date("Дата праздника (ГГГГ-ММ-ДД): ")
            price = input_int("Цена подарка (целые рубли): ", minimum=1)
            try:
                gift = gift_list.add_gift(
                    recipient,
                    occasion,
                    gift_name,
                    event_date,
                    price,
                )
            except ValueError as error:
                print(f"Подарок не добавлен: {error}")
                continue
            if save_changes(gift_list):
                print(f"Подарок «{gift.name}» добавлен.")
        elif choice == "3":
            query = input("Имя, получатель или повод для поиска: ")
            show_gifts(gift_list.find(query))
        elif choice == "4":
            max_price = input_int("Максимальная цена: ", minimum=1)
            show_gifts(gift_list.iter_affordable(max_price))
        elif choice == "5":
            sort_key = input("Сортировать по цене или дате: ").strip().lower()
            try:
                show_gifts(gift_list.sorted_by(sort_key))
            except ValueError as error:
                print(f"Ошибка: {error}")
        elif choice == "6":
            gift_id = input_int("Идентификатор подарка: ", minimum=1)
            if gift_list.mark_purchased(gift_id):
                save_changes(gift_list)
                print("Подарок отмечен купленным.")
            else:
                print("Подарок с таким идентификатором не найден.")
        elif choice == "7":
            gift_id = input_int("Идентификатор подарка: ", minimum=1)
            if gift_list.delete(gift_id):
                save_changes(gift_list)
                print("Подарок удалён.")
            else:
                print("Подарок с таким идентификатором не найден.")
        elif choice == "8":
            budget = input_int("Общий бюджет: ", minimum=1)
            total, purchased, total_price = gift_list.statistics()
            balance = gift_list.budget_balance(budget)
            print(f"Всего подарков: {total}")
            print(f"Куплено: {purchased}")
            print(f"Общая стоимость: {total_price} руб.")
            print(f"Остаток бюджета: {balance} руб.")
        else:
            print("Неизвестная команда. Выберите пункт от 0 до 8.")


if __name__ == "__main__":
    main()
