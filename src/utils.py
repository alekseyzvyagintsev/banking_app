###########################################################################################
import json
import os
from src.logging_utils import logger


def converting_data_into_a_dict_list(data_file: int | str | bytes) -> list | None:
    """
    Функцию принимает на вход путь до JSON-файла
    и возвращает список словарей с данными о финансовых транзакциях.
    Если файл пустой, содержит не список или не найден, функция возвращает пустой список.
    """

    # Регистрация входных данных
    logger.info(f"Входные данные: data_file={data_file}")

    if data_file:
        try:
            # Проверка существует ли указанный путь
            if os.path.exists(data_file):
                with open(data_file, encoding="utf-8") as json_file:
                    operations_data = json.load(json_file)
                if isinstance(operations_data, list):
                    logger.info(f"Исходящие данные: operations_data={operations_data}")
                    return operations_data
                else:
                    logger.error(f"Тип аргумента не является списком.")
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
    operations_list = converting_data_into_a_dict_list(file_with_operations)
    print(operations_list)

############################################################################################
