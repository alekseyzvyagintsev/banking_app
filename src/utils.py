###########################################################################################
import csv
import json
import os

import pandas as pd
from pandas import DataFrame

from src.logging_utils import logger


def converting_data_from_json_to_a_dict_list(data_file: int | str | bytes) -> list | None:
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


# if __name__ == "__main__":
#     file_with_operations = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "operations.json")
#     operations_list = converting_data_from_json_to_a_dict_list(file_with_operations)
#     print(operations_list[0])


def converting_data_from_csv_to_dict_list(data_file: int | str | bytes) -> list | None:
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


def converting_data_from_xlsx_to_dataframe(data_file: int | str | bytes) -> DataFrame | None:
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
                operations_data = df.to_dict(orient='records')
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


if __name__ == "__main__":
    file_with_operations = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data/transactions_excel.xlsx")
    operations_list = converting_data_from_xlsx_to_dataframe(file_with_operations)
    print(operations_list[0])

    # print(operations_list.shape)
    # print(operations_list.head())

############################################################################################
