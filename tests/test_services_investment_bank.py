import pytest
from src.services import investment_bank

@pytest.fixture
def transactions():
    """Фикстура для создания тестовых транзакций."""
    return [
        {"Дата операции": "2021-03-15", "Сумма операции": 1712},  # Округление до 1750
        {"Дата операции": "2021-04-20", "Сумма операции": 1020},  # Округление до 1050
        {"Дата операции": "2021-03-25", "Сумма операции": 510},   # Округление до 550
        {"Дата операции": "2021-03-28", "Сумма операции": 200},   # Округление до 250
        {"Дата операции": "2021-04-10", "Сумма операции": 800},   # Округление до 850
        {"Дата операции": "2021-03-11", "Сумма операции": 1250},  # Округление до 1300
        {"Дата операции": "2021-03-17", "Сумма операции": 900},   # Округление до 950
    ]

def test_investment_bank_with_50_limit(transactions):
    expected_result = 228.0
    result = investment_bank("2021-03", transactions, 50)
    assert result == expected_result, f"Ожидалось: {expected_result}, Получено: {result}"

def test_investment_bank_with_100_limit(transactions):
    expected_result = 428.0
    result = investment_bank("2021-03", transactions, 100)
    assert result == expected_result, f"Ожидалось: {expected_result}, Получено: {result}"

def test_investment_bank_empty_transactions():
    empty_transactions = []
    result = investment_bank("2021-03", empty_transactions, 50)
    assert result == 0.0, f"Ожидалось: 0.0, Получено: {result}"

def test_investment_bank_no_matching_month(transactions):
    result = investment_bank("2021-06", transactions, 50)
    assert result == 0.0, f"Ожидалось: 0.0, Получено: {result}"

def test_investment_bank_zero_amounts(transactions):
    zero_amount_transaction = [
        {"Дата операции": "2021-03-15", "Сумма операции": 0},
        {"Дата операции": "2021-03-20", "Сумма операции": 0},
    ]
    result = investment_bank("2021-03", zero_amount_transaction, 50)
    assert result == 0.0, f"Ожидалось: 0.0, Получено: {result}"