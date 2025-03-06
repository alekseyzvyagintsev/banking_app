from src.generators import transaction_descriptions

from conftest import transactions_data

def test_transaction_descriptions(transactions_data) -> None:
    """Тест волучения описания транзакции"""
    answers = [
        "Перевод организации",
        "Перевод со счета на счет",
        "Перевод со счета на счет",
        "Перевод с карты на карту",
        "Перевод организации",
    ]
    descriptions = transaction_descriptions(transactions_data)
    for answer in answers:
        description = next(descriptions)
        assert description == answer


def test_by_empty_list_transaction_descriptions() -> None:
    """Тест получения описания транзакции из пустого"""

    descriptions = transaction_descriptions()
    description = next(descriptions)
    assert description == 'Список пуст'

