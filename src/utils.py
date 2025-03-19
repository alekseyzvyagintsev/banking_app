###########################################################################################
import json
import os


def converting_data_into_a_dict_list(data_file: int | str | bytes) -> list | None:
    """
    Функцию принимает на вход путь до JSON-файла
    и возвращает список словарей с данными о финансовых транзакциях.
    Если файл пустой, содержит не список или не найден, функция возвращает пустой список.
    """
    if data_file:
        try:
            if os.path.exists(data_file):
                with open(data_file, encoding="utf-8") as json_file:
                    operations_data = json.load(json_file)
                if isinstance(operations_data, list):
                    return operations_data
                else:
                    return []
            else:
                print("Путь не правильный")
                return []
        except (json.JSONDecodeError, FileNotFoundError) as e:
            print(f"Возникла вот такая ошибка: {e}")
            return []
    return []


if __name__ == "__main__":
    file_with_operations = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "operations.json")
    operations_list = converting_data_into_a_dict_list(file_with_operations)
    print(operations_list)

############################################################################################
