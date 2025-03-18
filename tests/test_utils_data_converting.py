##################################################################################################
import os
from typing import Any

from src.utils import converting_data_into_a_dict_list

expected = {
    "id": 41428829,
    "state": "EXECUTED",
    "date": "2019-07-03T18:35:29.512364",
    "operationAmount": {"amount": "8221.37", "currency": {"name": "USD", "code": "USD"}},
    "description": "Перевод организации",
    "from": "MasterCard 7158300734726758",
    "to": "Счет 35383033474447895560",
}


def test_data_converting() -> Any | None:
    """
    Тест конвертации json - файла в pyton - обьект
    и на выходе должен быдь правильный словарь
    из списка словарей.
    """

    file_with_operations = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "operations.json")

    operations_list = converting_data_into_a_dict_list(file_with_operations)
    assert operations_list[1] == expected


def test_data_converting_without_file() -> None:
    """
    Тест реакции на отсутствие файла в указанном пути
    """

    file_with_operations = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")

    try:
        converting_data_into_a_dict_list(file_with_operations)
    except (IsADirectoryError, TypeError) as e:
        print(f"Произошла ошибка {e}")


def test_data_converting_not_list() -> None:
    """
    Тест Тест конвертации json - файла в pyton - обьект
    На вход подается файл правильного типа но с содержимым которое
    не преобразуется в список словарей.
    На выходе должен быть пустой список.
    """

    file_with_operations = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "api_response.json")

    operations_list = converting_data_into_a_dict_list(file_with_operations)
    assert operations_list == []
