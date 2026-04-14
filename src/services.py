################################################################################################
import re
from datetime import datetime

from src.logging_services import logger


def investment_bank(month: str, transactions: list, limit: int) -> float:
    """
    Функция позволяет копить через округление трат.
    Можно задать комфортный порог округления: 10, 50 или 100 ₽.
    Траты округляются, и разница между фактической суммой трат по карте
    и суммой округления попадает насчет «Инвесткопилки».
    """
    logger.info("Преобразуем месяц в объект datetime")
    split_date = re.findall(r"\d+", month)
    joined_date = ""
    if len(split_date) >= 2:
        joined_date = f"{split_date[0]}.{split_date[1]}"
    target_date = datetime.strptime(joined_date, "%Y.%m")

    total_saved = 0.0

    logger.info("Фильтруем транзакции по указанному месяцу")
    for transaction in transactions:
        operation_date_str = transaction.get("Дата операции")
        if not operation_date_str:
            continue  # Пропускаем операции без даты

        split_operation_date_str = re.findall(r"\d+", operation_date_str)
        joined_operation_date_str = ""
        if len(split_operation_date_str) >= 3:
            joined_operation_date_str = (
                f"{split_operation_date_str[0]}.{split_operation_date_str[1]}.{split_operation_date_str[2]}"
            )
        try:
            logger.info("Преобразуем дату операции в объект datetime")
            operation_date = datetime.strptime(joined_operation_date_str[:10], "%Y.%m.%d")
        except ValueError:
            try:
                operation_date = datetime.strptime(joined_operation_date_str[:10], "%d.%m.%Y")
            except ValueError:
                continue

        logger.info("Сравниваем месяцы и годы двух дат")
        if operation_date.year == target_date.year and operation_date.month == target_date.month:
            amount = abs(transaction.get("Сумма операции"))
            if amount is not None and amount != 0:
                remainder = amount % limit
                difference = limit - remainder
                total_saved += difference

    return round(total_saved, 2)


################################################################################################
