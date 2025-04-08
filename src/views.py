import datetime
import json
import os
from typing import Tuple

import pandas as pd

from src.external_api import fetch_exchange_rates, fetch_stock_prices
from src.processing import (calculate_total_expense,
                            calculate_total_income,
                            get_transfers_and_cash,
                            group_expenses_by_category,
                            group_income_by_category,
                            sort_by_descending)
from src.utils import get_xlsx_data, read_user_settings


def generate_report(date_str: str, period: str = "M") -> str:
    """
    Функция формирующая json - ответ для страницы событий на портале банка.
    Ответ содержит в себе:
    Раздел расходов за период
    1. Все расходы
    2. В категории Основные - Топ-7 расходов
    3. В категории Остальное - Переводы и наличные
    Раздел поступлений за период
    1. Все поступления
    2. В категории Основные - Топ-7 поступлений отсортированные по убыванию
    """

    # преобразует строку даты date_str в объект типа datetime
    date_obj = datetime.datetime.strptime(date_str, "%d.%m.%Y")
    # вычисляем начальную и конечную даты периода
    start_date, end_date = determine_period(date_obj, period)
    # Получаем полный список банковских операций
    transactions_list = get_xlsx_data(os.path.join(os.path.dirname(os.path.dirname(__file__)), "data/operations.xlsx"))
    # Преобразуем для удобства список в DataFrame
    df = pd.DataFrame(transactions_list)
    # Получаем данные только те которые входят в выбранный период
    df_filtered = filter_data(df, start_date, end_date)
    # Читаем из файла данные о валютах и ценных бумагах которые клиент отслеживает
    user_settings = read_user_settings(
        os.path.join(os.path.dirname(os.path.dirname(__file__)), "data/user_settings.json")
    )
    # Список валют
    currencies = user_settings.get("user_currencies")
    # Список ценных бумаг
    stocks = user_settings.get("user_stocks")
    # Получение курсов валют
    exchange_rates = fetch_exchange_rates(currencies)
    # Получение курса ценных бумаг
    stock_prices = fetch_stock_prices(stocks)
    # Все расходы
    total_expense = calculate_total_expense(df_filtered)
    # Основные категории расходов
    main_section = group_expenses_by_category(df_filtered)
    # Переводы и наличные
    transfers_and_cash_section = get_transfers_and_cash(df_filtered)
    # Все поступления
    total_income = calculate_total_income(df_filtered)
    # Основные категории поступлений
    main_income = group_income_by_category(df_filtered)
    # Основные категории поступлений отсортированные по убыванию
    sorted_income_categories = sort_by_descending(main_income)

    # Формирование json ответа
    report = {
        "expenses": {
            "total_amount": round(total_expense),
            "main": main_section,
            "others": transfers_and_cash_section,
        },
        "income": {"total_amount": round(total_income), "main": sorted_income_categories},
        "currency_rates": exchange_rates,
        "stock_prices": stock_prices,
    }

    return json.dumps(report, indent=4, ensure_ascii=False)


def determine_period(date_obj: datetime.datetime, period: str) -> Tuple[datetime.date, datetime.date]:
    """
    Формирование периодов для фильтрации DataFrame.
    Можно выбрать:
    W - неделя, на которую приходится дата.
    M - месяц, на который приходится дата.
    Y - год, на который приходится дата.
    ALL - все данные до указанной даты.
    """
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
    """
    Фильтрация данных по выбранному периоду W, M, Y или ALL
    """
    df["Дата операции"] = pd.to_datetime(df["Дата операции"], format="%d.%m.%Y %H:%M:%S")
    start_datetime = datetime.datetime.combine(start_date, datetime.datetime.min.time())
    end_datetime = datetime.datetime.combine(end_date, datetime.datetime.max.time())
    mask = (df["Дата операции"] >= start_datetime) & (df["Дата операции"] <= end_datetime)
    return df.loc[mask]


if __name__ == "__main__":

    report = generate_report("04.04.2021", "M")
    print(report)
