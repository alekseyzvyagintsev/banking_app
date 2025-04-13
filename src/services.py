################################################################################################
# import os
import re
from datetime import datetime

from src.logging_services import logger

# from src.utils import get_json_data, get_csv_data, get_xlsx_data


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
# operations_list = [
#         {"Дата операции": "2021-03-15", "Сумма операции": 1712},  # Округление до 1750
#         {"Дата операции": "2021-04-20", "Сумма операции": 1020},  # Округление до 1050
#         {"Дата операции": "2021-03-25", "Сумма операции": 510},   # Округление до 550
#         {"Дата операции": "2021-03-28", "Сумма операции": 200},   # Округление до 250
#         {"Дата операции": "2021-04-10", "Сумма операции": 800},   # Округление до 850
#         {"Дата операции": "2021-03-11", "Сумма операции": 1250},  # Округление до 1300
#         {"Дата операции": "2021-03-17", "Сумма операции": 900},   # Округление до 950
#     ]
#
# if __name__ == "__main__":
#     # file_with_operations = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data/operations.xlsx")
#     # operations_list = get_xlsx_data(file_with_operations)
#     # print(operations_list[0])
#     saved_sum = investment_bank('2021.03', operations_list, 100)
#     print(f'Сумма сбережений: {saved_sum}')
