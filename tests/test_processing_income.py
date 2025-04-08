###############################################################################
import pandas as pd

from src.processing import calculate_total_income, group_income_by_category, sort_by_descending


def test_calculate_total_income():
    # Создание тестового DataFrame
    data = {"Дата": ["01-01-2023", "02-01-2023"], "Сумма операции": [1000, 500], "Категория": ["Зарплата", "Прочее"]}
    df = pd.DataFrame(data)

    # Проверка результата
    total_income = calculate_total_income(df)
    assert total_income == 1500


def test_calculate_total_income_no_income():
    # Создание DataFrame без доходов
    data = {
        "Дата": ["01-01-2023", "02-01-2023"],
        "Сумма операции": [-1000, -500],
        "Категория": ["Продукты", "Транспорт"],
    }
    df = pd.DataFrame(data)

    # Проверка результата
    total_income = calculate_total_income(df)
    assert total_income == 0


###############################################################################
def test_group_income_by_category():
    # Создание тестового DataFrame
    data = {
        "Дата": ["01-01-2023", "02-01-2023", "03-01-2023"],
        "Сумма операции": [1000, 2000, 3000],
        "Категория": ["Зарплата", "Прочее", "Инвестиции"],
    }
    df = pd.DataFrame(data)

    # Проверка результата
    income_categories = group_income_by_category(df)
    assert len(income_categories) >= 3
    assert isinstance(income_categories[0], dict)
    assert income_categories[0]["category"] == "Инвестиции"
    assert income_categories[0]["amount"] == 3000
    assert income_categories[1]["category"] == "Прочее"
    assert income_categories[1]["amount"] == 2000
    assert income_categories[2]["category"] == "Зарплата"
    assert income_categories[2]["amount"] == 1000


def test_group_income_by_category_with_top_n():
    # Создание тестового DataFrame
    data = {
        "Дата": ["01-01-2023", "02-01-2023", "03-01-2023", "04-01-2023"],
        "Сумма операции": [1000, 2000, 3000, 4000],
        "Категория": ["Зарплата", "Прочее", "Инвестиции", "Дивиденды"],
    }
    df = pd.DataFrame(data)

    # Проверка результата
    income_categories = group_income_by_category(df, top_n=3)
    assert len(income_categories) == 4
    assert income_categories[-1]["category"] == "Остальное"
    assert income_categories[-1]["amount"] == 1000


###############################################################################
def test_sort_by_descending():
    # Создание тестового списка
    categories = [
        {"category": "Продукты", "amount": 1000},
        {"category": "Транспорт", "amount": 2000},
        {"category": "Развлечения", "amount": 3000},
    ]

    # Проверка результата
    sorted_categories = sort_by_descending(categories)
    assert sorted_categories[0]["category"] == "Развлечения"
    assert sorted_categories[0]["amount"] == 3000
    assert sorted_categories[1]["category"] == "Транспорт"
    assert sorted_categories[1]["amount"] == 2000
    assert sorted_categories[2]["category"] == "Продукты"
    assert sorted_categories[2]["amount"] == 1000


###############################################################################
