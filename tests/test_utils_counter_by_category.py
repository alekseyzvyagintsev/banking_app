import pytest

from src.utils import count_operations_by_category


@pytest.fixture
def operations_list() -> list[dict]:
    return [
        {"description": "Оплата коммунальных услуг"},
        {"description": "Пополнение счета"},
        {"description": "Перевод средств на карту"},
        {"description": "Оплата услуг связи"},
        {"description": "Оплата интернета"},
        {"description": "Снятие наличных"},
        {"description": "Оплата мобильного телефона"},
    ]


@pytest.fixture
def categories() -> list:
    return ["оплата", "перевод", "пополнение", "снятие"]


def test_count_operations_by_category_empty_operations_list(categories) -> None:
    """
    Проверяет работу функции при пустом списке операций — результат должен быть пустым словарем.
    """
    assert count_operations_by_category([], categories) == {}


def test_count_operations_by_category_empty_categories(operations_list) -> None:
    """
    Тестирует поведение функции, когда категории отсутствуют (передан пустой список).
    Ожидается, что функция вернет пустой словарь.
    """
    assert count_operations_by_category(operations_list, []) == {}


def test_count_operations_by_category_no_match(operations_list) -> None:
    """
    Проверяется случай, когда ни одно описание операции не соответствует
    переданным категориям — ожидается пустой словарь результатов.
    """
    categories = ["несуществующая категория"]
    assert count_operations_by_category(operations_list, categories) == {}


def test_count_operations_by_category_simple_case(operations_list, categories) -> None:
    """
    Простейший сценарий, где каждая операция относится ровно к одной категории,
    и результаты соответствуют ожидаемым значениям.
    """
    expected_result = {
        "оплата": 4,
        "перевод": 1,
        "пополнение": 1,
        "снятие": 1,
    }
    assert count_operations_by_category(operations_list, categories) == expected_result


def test_count_operations_by_category_case_insensitive(operations_list, categories) -> None:
    """
    Убедитесь, что регистры букв в описаниях операций не влияют на результат
    (например, слова "Оплата" и "ОПЛАТА" считаются одинаковыми).
    """
    operations_list_with_mixed_case = [
        {"description": "Оплата коммунальных услуг"},
        {"description": "ПОПОЛНЕНИЕ счета"},
        {"description": "Перевод средств НА КАРТУ"},
        {"description": "Оплата услуг СВЯЗИ"},
        {"description": "Оплата ИНТЕРНЕТА"},
        {"description": "Снятие НАЛИЧНЫХ"},
        {"description": "Оплата МОБИЛЬНОГО ТЕЛЕФОНА"},
    ]
    expected_result = {
        "оплата": 4,
        "перевод": 1,
        "пополнение": 1,
        "снятие": 1,
    }
    assert count_operations_by_category(operations_list_with_mixed_case, categories) == expected_result


def test_count_operations_by_category_multiple_matches_per_operation(operations_list, categories) -> None:
    """
    Случай, когда несколько категорий подходят к одному описанию операции.
    Функция должна корректно учитывать такие ситуации.
    """
    operations_list_with_multiple_matches = [
        {"description": "Оплата коммунальных услуг и пополнение счета"},
        {"description": "Перевод средств на карту и оплата интернета"},
        {"description": "Снятие наличных и оплата мобильного телефона"},
    ]
    expected_result = {
        "оплата": 3,
        "перевод": 1,
        "пополнение": 1,
        "снятие": 1,
    }
    assert count_operations_by_category(operations_list_with_multiple_matches, categories) == expected_result
