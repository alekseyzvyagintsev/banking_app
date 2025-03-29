###########################################################################################
import csv
import json
import os
import re
from typing import Any

import pandas as pd

from src.logging_utils import logger


def get_json_transactions(data_file: int | str | bytes) -> list | None:
    """
    Функцию принимает на вход путь до JSON-файла
    и возвращает список словарей с данными о финансовых транзакциях.
    Если файл пустой, содержит не список или не найден, функция возвращает пустой список.
    """

    # Регистрация входных данных
    logger.info(f"Предложен путь: data_file={data_file}")

    if data_file:
        try:
            # Проверка существует ли указанный путь
            logger.info("Пытаемся открыть файл и получить данные.")
            if os.path.exists(data_file):
                with open(data_file, encoding="utf-8") as json_file:
                    operations_data = json.load(json_file)
                if isinstance(operations_data, list):
                    logger.info("Полученные данные являются списком.")
                    return operations_data
                else:
                    logger.error("Тип данных не является списком.")
                    return []
            else:
                logger.warning("Путь не правильный")
                return []
        except (json.JSONDecodeError, FileNotFoundError) as e:
            logger.error(f"Возникла ошибка: {e}")
            return []
    logger.error("Обрабатывать нечего")
    return []


if __name__ == "__main__":
    file_with_operations = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "operations.json")
    operations_list = get_json_transactions(file_with_operations)
    print(operations_list[0])


############################################################################################
def get_csv_transactions(data_file: int | str | bytes) -> list | None:
    """
    Функцию принимает на вход путь до csv-файла
    и возвращает список словарей с данными о финансовых транзакциях.
    Если файл пустой, содержит не список или не найден, функция возвращает пустой список.
    """
    # Регистрация входных данных
    logger.info(f"Предложен путь: data_file={data_file}")

    if data_file:
        try:
            # Проверка существует ли указанный путь
            logger.info("Пытаемся открыть файл и получить данные.")
            if os.path.exists(data_file):
                with open(data_file, encoding="utf-8") as csv_file:
                    operations_data = list(csv.DictReader(csv_file, delimiter=";"))
                if isinstance(operations_data, list):
                    logger.info("Полученные данные являются списком.")
                    return operations_data
                else:
                    logger.error("Тип данных не является списком.")
                    return []
            else:
                logger.warning("Путь не правильный.")
                return []
        except Exception as e:
            logger.error(f"Возникла ошибка: {e}")
            return []
    logger.error("Обрабатывать нечего.")
    return []


# if __name__ == "__main__":
#     file_with_operations = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data/transactions.csv")
#     operations_list = converting_data_from_csv_to_dict_list(file_with_operations)
#     print(operations_list[0])


############################################################################################
def get_xlsx_transactions(data_file: int | str | bytes) -> list | None:
    """
    Функцию принимает на вход путь до excel-файла
    и возвращает DataFrame с финансовыми транзакциями.
    Если файл пустой или путь не верный, возвращает пустой список.
    """
    # Регистрация входных данных
    logger.info(f"Предложен путь: data_file={data_file}")
    if data_file:
        try:
            # Проверка существует ли указанный путь
            logger.info("Пытаемся открыть файл и получить данные.")
            if os.path.exists(data_file):
                df = pd.read_excel(data_file)
                operations_data = df.to_dict(orient="records")
                if isinstance(operations_data, list):
                    logger.info("Полученные данные являются списком.")
                    return operations_data
                else:
                    logger.error("Тип данных не является списком.")
                    return []
            else:
                logger.warning("Путь не правильный.")
                return []
        except Exception as e:
            logger.error(f"Возникла ошибка: {e}")
            return []
    logger.error("Обрабатывать нечего.")
    return []


# if __name__ == "__main__":
#     file_with_operations = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data/transactions_excel.xlsx")
#     operations_list = get_xlsx_transactions(file_with_operations)
#     print(operations_list[0])


############################################################################################
def search_operations(operations_list_for_cearch: list, search_string: str) -> list:
    """
    Функция принимает на вход список словарей с данными о банковских операциях
    и строку поиска, а возвращать список словарей, у которых в описании есть данная строка.
    """
    logger.info("Проверяем, является ли список пустым")
    if operations_list_for_cearch:
        try:
            logger.info("Преобразуем строку поиска в регулярное выражение (можно добавить флаг re.IGNORECASE)")
            pattern = re.compile(search_string, flags=re.IGNORECASE)

            logger.info("Фильтруем операции, где описание соответствует строке поиска")
            filtered_list = [
                operation
                for operation in operations_list_for_cearch
                if pattern.search(operation.get("description", ""))
            ]

            return filtered_list
        except Exception as ex:
            logger.error(f"Произошла ошибка: {ex}")

    return []


if __name__ == "__main__":
    data = [
        {"id": 1, "amount": 1000, "description": "Оплата услуг связи"},
        {"id": 2, "amount": 500, "description": "Покупка продуктов"},
        {"id": 3, "amount": 2000, "description": "Оплата коммунальных услуг"},
    ]

    search_result = search_operations(data, "услуг")
    print(search_result)


############################################################################################
def count_operations_by_category(operations_list_for_count: list, categories_list: list) -> dict[Any] | dict[Any, int]:
    """
    Функция принимает список словарей с данными о банковских операциях и список категорий операций,
    а возвращать словарь, в котором ключи — это названия категорий, а значения — это количество операций
    в каждой категории. Категории операций хранятся в поле description.
    """
    logger.info("Проверяем, является ли список пустым")
    if operations_list_for_count:
        try:
            logger.info("Создаем словарь для подсчета количества операций по категориям")
            category_count = {category: 0 for category in categories_list}

            logger.info("Проверяем, содержится ли категория в описании операции")
            for operation in operations_list_for_count:
                description = operation.get("description", "")

                for category in categories_list:
                    if category.lower() in description.lower():
                        category_count[category] += 1
                        break

            return category_count
        except Exception as ex:
            logger.error(f"Произошла ошибка: {ex}")
    return {}


# # Пример использования функции
# if __name__ == "__main__":
#     operations = [
#         {"id": 1, "amount": 1000, "description": "Оплата услуг связи"},
#         {"id": 2, "amount": 500, "description": "Покупка продуктов"},
#         {"id": 3, "amount": 2000, "description": "Оплата коммунальных услуг"},
#         {"id": 4, "amount": 1500, "description": "Покупка одежды"},
#         {"id": 5, "amount": 2500, "description": "Оплата образовательных услуг"},
#     ]
#
#     categories = ["связь", "продукты", "коммунальные услуги", "одежда", "образование"]
#
#     result = count_operations_by_category(operations, categories)
#     print(result)

############################################################################################
