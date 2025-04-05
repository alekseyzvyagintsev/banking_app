import json
import datetime
import os
import pandas as pd
from typing import Union, Optional, List, Tuple
from dataclasses import dataclass

from src.utils import get_xlsx_data, read_user_settings
from src.external_api import fetch_exchange_rates, fetch_stock_prices
# from src.processing import (
#     group_expenses_by_category,
#     calculate_total_expense,
#     calculate_total_income,
#     sort_by_descending,
# )


@dataclass
class ExpenseCategory:
    category: str
    amount: int


@dataclass
class IncomeCategory:
    category: str
    amount: int


def generate_report(date_str: str, period: str = "M") -> str:
    date_obj = datetime.datetime.strptime(date_str, "%d.%m.%Y")
    start_date, end_date = determine_period(date_obj, period)

    transactions_list = get_xlsx_data(
        os.path.join(os.path.dirname(os.path.dirname(__file__)),
        "data/operations.xlsx")
    )
    df = pd.DataFrame(transactions_list)
    df_filtered = filter_data(df, start_date, end_date)

    user_settings = read_user_settings(
        os.path.join(os.path.dirname(os.path.dirname(__file__)),
        "data/user_settings.json")
        )
    currencies = user_settings.get("user_currencies")
    stocks = user_settings.get("user_stocks")
    print(currencies, stocks)

    exchange_rates = fetch_exchange_rates(currencies)
    stock_prices = fetch_stock_prices(stocks)

    total_expense = calculate_total_expense(df_filtered)
    expense_categories = group_expenses_by_category(df_filtered)
    sorted_expense_categories = sort_by_descending(expense_categories)

    total_income = calculate_total_income(df_filtered)
    income_categories = group_income_by_category(df_filtered)
    sorted_income_categories = sort_by_descending(income_categories)

    report = {
        "expenses": {
            "total_amount": round(total_expense),
            "main": sorted_expense_categories[:7],
            "others": sum([cat.amount for cat in sorted_expense_categories[7:]])
        },
        "income": {
            "total_amount": round(total_income),
            "main": sorted_income_categories
        },
        "currency_rates": exchange_rates,
        "stock_prices": stock_prices
    }

    return json.dumps(report, indent=4)


def determine_period(date_obj: datetime.datetime, period: str) -> Tuple[datetime.date, datetime.date]:
    today = date_obj.date()
    if period == "W":
        start_date = today - datetime.timedelta(days=today.weekday())
        end_date = start_date + datetime.timedelta(days=6)
    elif period == "M":
        start_date = datetime.date(today.year, today.month, 1)
        end_date = today
    elif period == "Y":
        start_date = datetime.date(today.year, 1, 1)
        end_date = today
    elif period == "ALL":
        start_date = datetime.date(1900, 1, 1)
        end_date = today
    else:
        raise ValueError(f"Invalid period: {period}")
    return start_date, end_date


def filter_data(df: pd.DataFrame, start_date: datetime.date, end_date: datetime.date) -> pd.DataFrame:
    df["Дата операции"] = pd.to_datetime(df["Дата операции"], format='%d.%m.%Y %H:%M:%S')
    start_datetime = datetime.datetime.combine(start_date, datetime.datetime.min.time())
    end_datetime = datetime.datetime.combine(end_date, datetime.datetime.max.time())
    mask = (df["Дата операции"] >= start_datetime) & (df["Дата операции"] <= end_datetime)
    return df.loc[mask]

if __name__ == '__main__':
    report = generate_report("04.04.2025", "M")
    print(report)
