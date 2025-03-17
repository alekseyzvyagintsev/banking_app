###########################################################################################
import os
import json
from typing import Any


def converting_data_into_a_dict_list(data_file: Any):
    """
    Функцию принимает на вход путь до JSON-файла
    и возвращает список словарей с данными о финансовых транзакциях.
    Если файл пустой, содержит не список или не найден, функция возвращает пустой список.
    """
    with open(data_file, encoding="utf-8") as json_file:
        operations_data = json.load(json_file)

    return operations_data


if __name__ == "__main__":
    file_with_operations = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "operations.json")
    operations_list = converting_data_into_a_dict_list(file_with_operations)
    print(operations_list[-1])

############################################################################################
