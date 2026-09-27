from datetime import date, timedelta

import main
from models import GiftList
from storage import load_gifts


def test_main_adds_and_persists_object_model(monkeypatch, tmp_path, capsys):
    data_file = tmp_path / "gifts.json"
    future = (date.today() + timedelta(days=30)).isoformat()
    answers = iter(
        [
            "2",
            "Анна",
            "День рождения",
            "Книга",
            future,
            "1500",
            "1",
            "0",
        ]
    )
    monkeypatch.setattr(main, "DATA_FILE", data_file)
    monkeypatch.setattr("builtins.input", lambda _: next(answers))

    main.main()

    restored = load_gifts(data_file)
    output = capsys.readouterr().out
    assert isinstance(restored, GiftList)
    assert restored.items[0].name == "Книга"
    assert "Подарок «Книга» добавлен." in output
    assert "Анна" in output
