from typing import Dict, List

import pytest

from src.processing import filter_by_description


@pytest.fixture
def operations_list() -> List[Dict]:
    return [
        {"id": 1, "description": "Оплата коммунальных услуг"},
        {"id": 2, "description": "Пополнение счета"},
        {"id": 3, "description": "Перевод средств на карту"},
        {"id": 4, "description": "Оплата услуг связи"},
        {"id": 5, "description": "Оплата интернета"},
        {"id": 6, "description": "Снятие наличных"},
        {"id": 7, "description": "Оплата мобильного телефона"},
    ]


def test_filter_by_description_exact_match(operations_list):
    """Тестируем точное совпадение строки поиска"""
    search_string = "Оплата"
    expected_output = [
        {"id": 1, "description": "Оплата коммунальных услуг"},
        {"id": 4, "description": "Оплата услуг связи"},
        {"id": 5, "description": "Оплата интернета"},
        {"id": 7, "description": "Оплата мобильного телефона"},
    ]
    actual_output = filter_by_description(operations_list, search_string)
    assert actual_output == expected_output


def test_filter_by_description_partial_match(operations_list):
    """Тестируем частичное совпадение строки поиска"""
    search_string = "услуг"
    expected_output = [
        {"id": 1, "description": "Оплата коммунальных услуг"},
        {"id": 4, "description": "Оплата услуг связи"},
    ]
    actual_output = filter_by_description(operations_list, search_string)
    assert actual_output == expected_output


def test_filter_by_description_case_insensitive(operations_list):
    """Тестируем нечувствительность к регистру"""
    search_string = "ОПЛАТА"
    expected_output = [
        {"id": 1, "description": "Оплата коммунальных услуг"},
        {"id": 4, "description": "Оплата услуг связи"},
        {"id": 5, "description": "Оплата интернета"},
        {"id": 7, "description": "Оплата мобильного телефона"},
    ]
    actual_output = filter_by_description(operations_list, search_string)
    assert actual_output == expected_output


def test_filter_by_description_empty_search_string(operations_list):
    """Тестируем пустой поисковый запрос"""
    search_string = ""
    expected_output = []
    actual_output = filter_by_description(operations_list, search_string)
    assert actual_output == expected_output


def test_filter_by_description_empty_operations_list():
    """Тестируем пустой список операций"""
    operations_list = []
    search_string = "Оплата"
    expected_output = []
    actual_output = filter_by_description(operations_list, search_string)
    assert actual_output == expected_output


def test_filter_by_description_no_match(operations_list):
    """Тестируем отсутствие совпадений"""
    search_string = "Не существует"
    expected_output = []
    actual_output = filter_by_description(operations_list, search_string)
    assert actual_output == expected_output


def test_filter_by_description_special_characters(operations_list):
    """Тестируем использование специальных символов в поиске"""
    search_string = "счет."
    expected_output = [
        {"id": 2, "description": "Пополнение счета"},
    ]
    actual_output = filter_by_description(operations_list, search_string)
    assert actual_output == expected_output
