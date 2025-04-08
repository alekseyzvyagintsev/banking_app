############################################################################
import os
import re
from typing import Any, Dict, Iterable, List, Optional

import pandas as pd

from src.utils import get_xlsx_data

INCOME: list = []
EXPENSES: list = []


def filter_by_state(list_of_actions: list[dict[str, Any]], state: Optional[str] = "EXECUTED") -> list[Any]:
    """
    принимает список словарей и опционально значение для ключа state (по умолчанию 'EXECUTED').
    Функция возвращает новый список словарей, содержащий только те словари, у которых ключ state
    соответствует указанному значению.
    """
    if not state:
        state = "EXECUTED"
    if any(state in dict_from_list.values() for dict_from_list in list_of_actions):
        result = [d for d in list_of_actions if d.get("state", "") == state]
        return result
    else:
        return []


def sort_by_date(list_of_actions: Iterable[dict[str, Any]], descending: Optional[bool] = True) -> list[dict[str, Any]]:
    """
    принимает список словарей и необязательный параметр,
    задающий порядок сортировки (по умолчанию — убывание).
    Функция возвращает новый список, отсортированный по дате (date).
    """
    if descending is not False:
        descending = True
    sorted_list = sorted(list_of_actions, key=lambda x: x["date"], reverse=descending)
    return sorted_list


def filter_by_description(
    list_of_actions: Iterable[dict[str, Any]], search_string: str
) -> list[dict[str, Any]] | None:
    """
    Функция принимает список словарей и слово для фильтрации списка транзакций,
    Функция возвращает новый список, отсортированный по предложенному слову.
    """
    if search_string:
        # Разделяем строку поиска на отдельные слова
        words = [word.lower() for word in search_string.split()]

        # Создаем регулярное выражение для каждого слова
        patterns = [re.compile(rf"\b{word}\b", flags=re.IGNORECASE) for word in words]

        filtered_list = []
        try:
            for transaction in list_of_actions:
                if all(
                    any(pattern.search(transaction.get("description", "")) for pattern in patterns)
                    for _ in range(len(patterns))
                ):
                    filtered_list.append(transaction)

            return filtered_list
        except Exception:
            print(f"Не найдено ни одной транзакции со словом(ами) {search_string}")
            return filtered_list
    else:
        return []


######################################################################################################
def calculate_total_expense(df: pd.DataFrame) -> float:
    """Отбираем строки, где "Сумма операции" меньше нуля (отрицательная)"""
    negative_values = df["Сумма операции"][df["Сумма операции"] < 0]
    return negative_values.sum()


def group_expenses_by_category(df: pd.DataFrame, top_n=7) -> list:
    """Функция для группировки расходов по основным категориям"""
    global EXPENSES
    # Отфильтровываем строки с расходами (суммы меньше нуля)
    df_expenses = df[df["Сумма операции"] < 0]

    # Группируем данные по категориям и считаем сумму операций
    grouped = df_expenses.groupby("Категория")["Сумма операции"].sum().abs()  # берем модуль от суммы

    # Сортируем категории по сумме операций в порядке убывания
    sorted_categories = grouped.sort_values(ascending=False)

    # Берём первые N категорий с наибольшими расходами
    top_categories = sorted_categories.head(top_n)

    # Формируем список категорий с суммами
    EXPENSES = [{"category": cat, "amount": round(sum_)} for cat, sum_ in top_categories.items()]

    # Суммируем остальные категории в "Остальное"
    other_sum = sorted_categories.tail(len(sorted_categories) - top_n).sum()
    EXPENSES.append({"category": "Остальное", "amount": round(other_sum)})

    return EXPENSES


# Функция для получения переводов и наличных
def get_transfers_and_cash(df: pd.DataFrame) -> list:
    # Фильтруем строки по категориям 'Наличные' и 'Переводы'
    filtered_df = df[(df["Категория"] == "Наличные") | (df["Категория"] == "Переводы")]

    # Сортируем по сумме операций в порядке убывания
    sorted_df = filtered_df.sort_values(by="Сумма операции", ascending=True)

    # Преобразуем результат в список объектов ExpenseCategory
    transfers_and_cash = [
        {"category": row["Категория"], "amount": row["Сумма операции"]} for _, row in sorted_df.iterrows()
    ]

    return transfers_and_cash


################################################################################################
def calculate_total_income(df: pd.DataFrame) -> float:
    # Отбираем строки, где "Сумма операции" меньше нуля (отрицательная)
    positive_values = df["Сумма операции"][df["Сумма операции"] > 0]
    return positive_values.sum()


def group_income_by_category(df: pd.DataFrame, top_n=7) -> List[dict]:
    # Отфильтровываем строки с доходами (суммы больше нуля)
    global INCOME
    df_income = df[df["Сумма операции"] > 0]

    # Группируем данные по категориям и считаем сумму операций
    grouped = df_income.groupby("Категория")["Сумма операции"].sum().abs()  # берем модуль от суммы

    # Сортируем категории по сумме операций в порядке убывания
    sorted_categories = grouped.sort_values(ascending=False)

    # Берём первые N категорий с наибольшими поступлениями
    top_categories = sorted_categories.head(top_n)

    # Формируем список категорий с суммами
    INCOME = [{"category": cat, "amount": round(sum_)} for cat, sum_ in top_categories.items()]

    # Суммируем остальные категории в "Остальное"
    other_sum = sorted_categories.tail(len(sorted_categories) - top_n).sum()
    INCOME.append({"category": "Остальное", "amount": round(other_sum)})

    return INCOME


def sort_by_descending(data: List[Dict]) -> List[Dict]:
    return sorted(data, key=lambda x: x["amount"], reverse=True)


############################################################################
if __name__ == "__main__":

    transactions_list = get_xlsx_data(os.path.join(os.path.dirname(os.path.dirname(__file__)), "data/operations.xlsx"))
    df = pd.DataFrame(transactions_list)

    expenses_categories = group_expenses_by_category(df)
    print(expenses_categories)

    income_categories = group_income_by_category(df)
    print(income_categories)

    print(f"глобальный {EXPENSES}")
    print(f"глобальный {INCOME}")
    sorted_list = sort_by_descending(income_categories)
    print(sorted_list)
