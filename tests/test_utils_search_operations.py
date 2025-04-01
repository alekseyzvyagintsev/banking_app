import pytest

from src.utils import search_operations


@pytest.fixture
def operations_list() -> list[dict]:
    return [
        {"id": 1, "description": "Оплата коммунальных услуг"},
        {"id": 2, "description": "Пополнение счета"},
        {"id": 3, "description": "Перевод средств на карту"},
        {"id": 4, "description": "Оплата услуг связи"},
        {"id": 5, "description": "Оплата интернета"},
        {"id": 6, "description": "Снятие наличных"},
        {"id": 7, "description": "Оплата мобильного телефона"},
    ]


def test_search_operations_exact_match(operations_list) -> None:
    """Тестируем точное совпадение строки поиска"""
    search_string = "Оплата"
    expected_output = [
        {"id": 1, "description": "Оплата коммунальных услуг"},
        {"id": 4, "description": "Оплата услуг связи"},
        {"id": 5, "description": "Оплата интернета"},
        {"id": 7, "description": "Оплата мобильного телефона"},
    ]
    actual_output = search_operations(operations_list, search_string)
    assert actual_output == expected_output


def test_search_operations_partial_match(operations_list) -> None:
    """Тестируем частичное совпадение строки поиска"""
    search_string = "услуг"
    expected_output = [
        {"id": 1, "description": "Оплата коммунальных услуг"},
        {"id": 4, "description": "Оплата услуг связи"},
    ]
    actual_output = search_operations(operations_list, search_string)
    assert actual_output == expected_output


def test_search_operations_case_insensitive(operations_list) -> None:
    """Тестируем нечувствительность к регистру"""
    search_string = "ОПЛАТА"
    expected_output = [
        {"id": 1, "description": "Оплата коммунальных услуг"},
        {"id": 4, "description": "Оплата услуг связи"},
        {"id": 5, "description": "Оплата интернета"},
        {"id": 7, "description": "Оплата мобильного телефона"},
    ]
    actual_output = search_operations(operations_list, search_string)
    assert actual_output == expected_output


def test_search_operations_empty_search_string(operations_list) -> None:
    """Тестируем пустой поисковый запрос"""
    search_string = ""
    expected_output = [
        {"description": "Оплата коммунальных услуг", "id": 1},
        {"description": "Пополнение счета", "id": 2},
        {"description": "Перевод средств на карту", "id": 3},
        {"description": "Оплата услуг связи", "id": 4},
        {"description": "Оплата интернета", "id": 5},
        {"description": "Снятие наличных", "id": 6},
        {"description": "Оплата мобильного телефона", "id": 7},
    ]
    actual_output = search_operations(operations_list, search_string)
    assert actual_output == expected_output


def test_search_operations_empty_operations_list() -> None:
    """Тестируем пустой список операций"""
    operations_list = []
    search_string = "Оплата"
    expected_output = []
    actual_output = search_operations(operations_list, search_string)
    assert actual_output == expected_output


def test_search_operations_no_match(operations_list) -> None:
    """Тестируем отсутствие совпадений"""
    search_string = "Не существует"
    expected_output = []
    actual_output = search_operations(operations_list, search_string)
    assert actual_output == expected_output


def test_search_operations_special_characters(operations_list) -> None:
    """Тестируем использование специальных символов в поиске"""
    search_string = "счет."
    expected_output = [
        {"id": 2, "description": "Пополнение счета"},
    ]
    actual_output = search_operations(operations_list, search_string)
    assert actual_output == expected_output
