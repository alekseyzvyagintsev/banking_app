import json
import os

import pytest

from src.utils import read_user_settings

# Тестовые данные
TEST_FILE_PATH = "test.json"


@pytest.fixture(scope="module")
def create_test_file():
    # Создаем временный файл для теста
    with open(TEST_FILE_PATH, "w") as f:
        data = {"setting1": "value1", "setting2": 42, "setting3": True}
        json.dump(data, f)

    yield TEST_FILE_PATH

    # Удаляем файл после завершения всех тестов
    os.remove(TEST_FILE_PATH)


def test_read_user_settings(create_test_file):
    # Проверка успешной загрузки настроек
    expected_data = {"setting1": "value1", "setting2": 42, "setting3": True}
    result = read_user_settings(create_test_file)
    assert result == expected_data


def test_missing_file():
    # Проверка исключения при отсутствии файла
    non_existent_file = "nonexistent.json"
    with pytest.raises(FileNotFoundError):
        read_user_settings(non_existent_file)


def test_empty_file(create_test_file):
    # Проверка исключения при пустом файле
    empty_file = "empty.json"
    with open(empty_file, "w"):
        pass
    with pytest.raises(json.JSONDecodeError):
        read_user_settings(empty_file)
    os.remove(empty_file)


def test_invalid_json_format(create_test_file):
    # Проверка исключения при неправильном формате JSON
    invalid_json_file = "invalid.json"
    with open(invalid_json_file, "w") as f:
        f.write("This is not valid JSON!")
    with pytest.raises(json.JSONDecodeError):
        read_user_settings(invalid_json_file)
    os.remove(invalid_json_file)
