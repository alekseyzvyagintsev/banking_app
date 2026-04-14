###########################################################################################
import csv
import json
import os
import re
from collections import Counter
from typing import Any

import pandas as pd

from src.logging_utils import logger


def get_json_data(data_file: int | str | bytes) -> list | None:
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


############################################################################################
def get_csv_data(data_file: int | str | bytes) -> list | None:
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


############################################################################################
def get_xlsx_data(data_file: int | str | bytes) -> list | None:
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


############################################################################################
def search_operations(operations_list: list, search_string: str) -> list:
    """
    Функция принимает на вход список словарей с данными о банковских операциях
    и строку поиска, а возвращать список словарей, у которых в описании есть данная строка.
    """
    logger.info("Проверяем, является ли список пустым")
    if operations_list:
        try:
            logger.info("Преобразуем строку поиска в регулярное выражение (можно добавить флаг re.IGNORECASE)")
            pattern = re.compile(search_string, flags=re.IGNORECASE)

            logger.info("Фильтруем операции, где описание соответствует строке поиска")
            filtered_list = [
                operation for operation in operations_list if pattern.search(operation.get("description", ""))
            ]

            return filtered_list
        except Exception as ex:
            logger.error(f"Произошла ошибка: {ex}")

    return []


############################################################################################
def count_operations_by_category(operations_list_for_count: list, categories_list: list) -> dict[Any] | dict[Any, int]:
    """
    Функция принимает список словарей с данными о банковских операциях и список категорий операций,
    а возвращать словарь, в котором ключи — это названия категорий, а значения — это количество операций
    в каждой категории. Категории операций хранятся в поле description.
    """
    logger.info("Проверяем, является ли список пустым")
    if not operations_list_for_count:
        return {}

    logger.info("Инициализируем счетчик для категорий")
    category_counter = Counter()

    try:
        logger.info("Проходим по каждому описанию операции и ищем соответствие с категориями")
        for operation in operations_list_for_count:
            description = operation.get("description", "").lower()

            matched_categories = [category for category in categories_list if category.lower() in description]

            logger.info("Увеличиваем счетчики для найденных категорий")
            for category in matched_categories:
                category_counter.update({category: 1})

        return dict(category_counter)
    except Exception as ex:
        logger.error(f"Произошла ошибка: {ex}")


############################################################################################
def read_user_settings(file_path: str) -> dict:
    """Функция для получения курса акций из входящего списка акций."""
    with open(file_path, "r") as f:
        settings = json.load(f)
    return settings


############################################################################################
