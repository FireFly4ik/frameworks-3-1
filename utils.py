"""Функции безопасного консольного ввода."""

from datetime import date


def input_int(prompt: str, minimum: int | None = None) -> int:
    """Запрашивать целое число, пока пользователь не введёт допустимое."""
    while True:
        try:
            value = int(input(prompt).strip())
        except ValueError:
            print("Введите целое число.")
            continue
        if minimum is not None and value < minimum:
            print(f"Значение должно быть не меньше {minimum}.")
            continue
        return value


def input_date(prompt: str) -> date:
    """Запрашивать дату ISO, пока пользователь не введёт допустимую."""
    while True:
        try:
            return date.fromisoformat(input(prompt).strip())
        except ValueError:
            print("Введите дату в формате ГГГГ-ММ-ДД.")
