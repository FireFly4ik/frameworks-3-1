import json

import pytest

from storage import load_gifts, save_gifts


def test_save_and_load_gifts(tmp_path):
    filename = tmp_path / "nested" / "gifts.json"
    gifts = [{"id": 1, "name": "Книга"}]

    save_gifts(filename, gifts)

    assert load_gifts(filename) == gifts


def test_load_missing_file_returns_empty_list(tmp_path):
    assert load_gifts(tmp_path / "missing.json") == []


def test_load_invalid_json_reports_error(tmp_path):
    filename = tmp_path / "gifts.json"
    filename.write_text("not json", encoding="utf-8")

    with pytest.raises(ValueError, match="не удалось прочитать"):
        load_gifts(filename)


def test_load_rejects_non_list_json(tmp_path):
    filename = tmp_path / "gifts.json"
    filename.write_text(json.dumps({"id": 1}), encoding="utf-8")

    with pytest.raises(ValueError, match="должен находиться список"):
        load_gifts(filename)
