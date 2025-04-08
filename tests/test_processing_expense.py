#################################################################################
import pandas as pd

from src.processing import calculate_total_expense, get_transfers_and_cash, group_expenses_by_category


def test_calculate_total_expense():
    # Создание тестового DataFrame
    data = {
        "Дата": ["01-01-2023", "02-01-2023"],
        "Сумма операции": [-1000, -500],
        "Категория": ["Продукты", "Транспорт"],
    }
    df = pd.DataFrame(data)

    # Проверка результата
    total_expense = calculate_total_expense(df)
    assert total_expense == -1500


def test_calculate_total_expense_no_expenses():
    # Создание DataFrame без расходов
    data = {"Дата": ["01-01-2023", "02-01-2023"], "Сумма операции": [1000, 500], "Категория": ["Зарплата", "Прочее"]}
    df = pd.DataFrame(data)

    # Проверка результата
    total_expense = calculate_total_expense(df)
    assert total_expense == 0


#################################################################################
def test_group_expenses_by_category():
    # Создание тестового DataFrame
    data = {
        "Дата": ["01-01-2023", "02-01-2023", "03-01-2023"],
        "Сумма операции": [-1000, -2000, -3000],
        "Категория": ["Продукты", "Транспорт", "Развлечения"],
    }
    df = pd.DataFrame(data)

    # Проверка результата
    expense_categories = group_expenses_by_category(df)
    assert len(expense_categories) >= 3
    assert isinstance(expense_categories[0], dict)
    assert expense_categories[0]["category"] == "Развлечения"
    assert expense_categories[0]["amount"] == 3000
    assert expense_categories[1]["category"] == "Транспорт"
    assert expense_categories[1]["amount"] == 2000
    assert expense_categories[2]["category"] == "Продукты"
    assert expense_categories[2]["amount"] == 1000


def test_group_expenses_by_category_with_top_n():
    # Создание тестового DataFrame
    data = {
        "Дата": ["01-01-2023", "02-01-2023", "03-01-2023", "04-01-2023"],
        "Сумма операции": [-1000, -2000, -3000, -4000],
        "Категория": ["Продукты", "Транспорт", "Развлечения", "Прочее"],
    }
    df = pd.DataFrame(data)

    # Проверка результата
    expense_categories = group_expenses_by_category(df, top_n=3)
    assert len(expense_categories) == 4
    assert expense_categories[-1]["category"] == "Остальное"
    assert expense_categories[-1]["amount"] == 1000


#################################################################################
def test_get_transfers_and_cash():
    # Создание тестового DataFrame
    data = {
        "Дата": ["01-01-2023", "02-01-2023", "03-01-2023"],
        "Сумма операции": [-1000, -2000, -3000],
        "Категория": ["Наличные", "Переводы", "Прочее"],
    }
    df = pd.DataFrame(data)

    # Проверка результата
    transfers_and_cash = get_transfers_and_cash(df)
    assert len(transfers_and_cash) == 2
    assert isinstance(transfers_and_cash[0], dict)
    assert transfers_and_cash[0]["category"] == "Переводы"
    assert transfers_and_cash[0]["amount"] == -2000
    assert transfers_and_cash[1]["category"] == "Наличные"
    assert transfers_and_cash[1]["amount"] == -1000


#################################################################################
