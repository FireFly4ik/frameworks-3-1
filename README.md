# Сервис формирования списка подарков

Локальный учебный проект для планирования подарков к событиям и контроля расходов. В ПР6 веб-интерфейс переведён с HTML-строк во view-функциях на Django Template Language. Консольная версия, объектная модель ПР3 и данные `data/gifts.json` сохранены.

## Возможности

- просмотр подарков, получателей и событий в браузере;
- открытие карточек объектов по динамическим URL;
- отображение связей `Gift → Occasion → Recipient`;
- вывод статуса покупки, даты события, цены и сводной статистики;
- обработка пустых коллекций, неизвестных адресов и идентификаторов;
- работа прежнего консольного меню;
- хранение данных между запусками в JSON.

Изменение данных через веб-интерфейс, Django ORM, формы и авторизация будут добавлены в следующих практических работах.

## Технологии

- Python 3.10+;
- Django 5.2 LTS и Django Template Language;
- HTML, CSS, JavaScript и Bootstrap 5.3;
- pytest и pytest-django;
- flake8 и mypy в строгом режиме.

## Объектная модель

Каждая сущность находится в отдельном файле пакета `models`:

- `Recipient` — получатель подарка;
- `Occasion` — событие с датой и ссылкой на `Recipient`;
- `Gift` — подарок с ценой, статусом и ссылкой на `Occasion`;
- `GiftList` — агрегат, который управляет коллекцией подарков.

```text
GiftList
└── Gift
    └── Occasion
        └── Recipient
```

Веб-слой использует ту же модель через `load_gifts()`. Django ORM для предметных данных на этапе ПР6 не используется.

## Шаблонная архитектура

Общий каркас находится в `templates/base.html`. Он подключает Bootstrap, собственный CSS, логотип, навигацию, подвал и JavaScript. Все страницы наследуют его через `{% extends %}` и переопределяют блоки `title` и `content`.

Повторяющиеся части вынесены в подключаемые шаблоны:

- `templates/includes/navigation.html`;
- `gifts/templates/gifts/includes/gift_card.html`;
- `gifts/templates/gifts/includes/gift_status.html`;
- `recipients/templates/recipients/includes/recipient_card.html`;
- `occasions/templates/occasions/includes/occasion_card.html`.

View-функции загружают объекты, формируют контекст и вызывают `render()`. Циклы, условия, обработка пустых коллекций и форматирование данных выполняются средствами шаблонов. Для ссылок используются `{% url %}`, пространства имён и имена маршрутов. Применяются фильтры `length`, `default`, `date`, `first` и `upper`.

## Статические файлы

Каталог `homepage/static/homepage/` содержит:

- `css/style.css` — адаптивное оформление карточек, навигации и страниц;
- `img/logo.png` — логотип сервиса подарков;
- `js/main.js` — автоматический вывод текущего года в подвале.

Ресурсы подключаются в `base.html` через `{% load static %}` и `{% static %}`.

## URL веб-интерфейса

| URL | View-функция | Назначение |
| --- | --- | --- |
| `/` | `homepage.views.index` | главная страница и статистика |
| `/gifts/` | `gifts.views.gift_list` | список подарков из JSON |
| `/gifts/<id>/` | `gifts.views.gift_detail` | карточка подарка |
| `/recipients/` | `recipients.views.recipient_list` | список получателей |
| `/recipients/<id>/` | `recipients.views.recipient_detail` | подарки получателя |
| `/occasions/` | `occasions.views.occasion_list` | список событий |
| `/occasions/<id>/` | `occasions.views.occasion_detail` | карточка события |

Несуществующие ID и адреса возвращают код 404 и страницу, наследующую общий шаблон.

## Структура проекта

```text
.
├── templates/          # base.html, общий 404 и навигация
├── giftservice/        # настройки и корневые URL
├── homepage/           # главная страница и static-файлы
├── gifts/              # шаблоны подарков
├── recipients/         # шаблоны получателей
├── occasions/          # шаблоны событий
├── models/             # объектная модель ПР3
├── data/gifts.json     # JSON-хранилище
├── tests/              # тесты модели, консоли и Django
├── manage.py
├── main.py
└── storage.py
```

## Установка и запуск

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py check
python manage.py runserver
```

Веб-интерфейс доступен по адресу `http://127.0.0.1:8000/`. Консольная версия запускается командой `python main.py`.

## Проверка

```bash
./scripts/check.sh
python manage.py findstatic homepage/img/logo.png
```

Скрипт запускает системную проверку Django, flake8, строгий mypy и pytest. Тесты проверяют использование шаблонов, контекст, динамические URL, ответы 404, пустые коллекции, навигацию и static-файлы.

## Текущее состояние

ПР6 завершает перенос веб-интерфейса на шаблоны Django. HTML удалён из view-функций; все основные страницы используют `render()`, наследование, включаемые шаблоны, именованные URL, фильтры и собственные статические ресурсы. Источником данных остаются JSON и объектная модель ПР3.
