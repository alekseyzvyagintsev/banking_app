###############################################################################################################
# import os
from datetime import datetime, timedelta
from typing import Optional

import pandas as pd

from src.decorators import report_decorator
from src.logging_reports import logger


@report_decorator()
def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> pd.DataFrame:
    """Возвращает траты по заданной категории за последние три месяца (от переданной даты)."""
    global filtered_transactions
    if date:
        try:
            date_obj = datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            logger.error(f"Неверный формат даты: {date}. Используйте формат YYYY-MM-DD.")
            return pd.DataFrame()
    else:
        date_obj = datetime.now()

    start_date = date_obj - timedelta(days=90)

    print(start_date)
    print(date_obj)

    logger.info("Фильтруем транзакции по дате и категории")
    try:
        filtered_transactions = transactions[
            (pd.to_datetime(transactions["Дата операции"], format="mixed", errors="coerce") >= start_date)
            & (pd.to_datetime(transactions["Дата операции"], format="mixed", errors="coerce") <= date_obj)
            & (transactions["Категория"] == category)
        ]
    except Exception as ex:
        logger.error(f"Возникла ошибка: {ex}")

    logger.info("Суммируем траты по категории")
    total_spending = filtered_transactions.groupby(["Категория"]).agg({"Сумма операции": "sum"})
    return total_spending


###############################################################################################################
