#############################################################################################################
import pandas as pd
import pytest

from src.reports import spending_by_category


@pytest.fixture(scope="module")
def sample_transactions():
    data = {
        "Дата операции": ["2025-04-10", "2025-03-15", "2025-02-20", "2025-01-01"],
        "Категория": ["Еда", "Транспорт", "Развлечения", "Еда"],
        "Сумма операции": [1000, 500, 1500, 800],
    }
    df = pd.DataFrame(data)
    return df


def test_no_date_provided(sample_transactions):
    result = spending_by_category(sample_transactions, "Еда")
    expected_result = pd.DataFrame({"Сумма операции": [1000]}, index=["Еда"])

    assert result.equals(expected_result), f"Результат {result} не соответствует ожидаемому {expected_result}"


def test_with_date(sample_transactions):
    result = spending_by_category(sample_transactions, "Еда", "2025-02-15")
    expected_result = pd.DataFrame({"Сумма операции": [800]}, index=["Еда"])

    assert result.equals(expected_result), f"Результат {result} не соответствует ожидаемому {expected_result}"


def test_empty_category(sample_transactions):
    result = spending_by_category(sample_transactions, "Одежда")

    assert result.empty, f"Ожидается пустой DataFrame, результат: {result}"


#############################################################################################################
