##################################################################################################
from typing import Any

from src.generators import transaction_descriptions


def test_transaction_descriptions(transactions_data: list[dict[str, Any]]) -> None:
    """Тест волучения описания транзакций"""
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
    """Тест получения описания транзакции из пустого списка"""

    descriptions = transaction_descriptions()
    assert list(descriptions) == []


##################################################################################################
