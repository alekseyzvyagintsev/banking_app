# from typing import Any
#
#
import os

from src.processing import filter_by_state
from src.utils import get_json_transactions, get_xlsx_transactions, get_csv_transactions

# def filter_by_state(arg1, arg2):
#     print(f"Фильтруется выбранный источник с аргументами: {arg1} и {arg2}")
#     # Здесь код для получения информации о транзакциях из JSON-файла
#
# def get_json_transactions(arg):
#     print(f"Обработка JSON-файла с аргументом {arg}...")
#     # Здесь код для получения информации о транзакциях из JSON-файла
#
#
# def get_csv_transactions(arg):
#     print(f"Обработка CSV-файла с аргументом {arg}...")
#     # Здесь код для получения информации о транзакциях из CSV-файла
#
#
# def get_xlsx_transactions(arg):
#     print(f"Обработка XLSX-файла с аргументом {arg}...")
#     # Здесь код для получения информации о транзакциях из XLSX-файла


menu_options = {
    1: get_json_transactions,
    2: get_csv_transactions,
    3: get_xlsx_transactions
}

choice_out = {
    1: "JSON-файл",
    2: "CSV-файл",
    3: "XLSX-файл"
}

files_to_filter = {
    1: "operations.json",
    2: "transactions.csv",
    3: "transactions_excel.xlsx"
}

statuses = ['EXECUTED', 'CANCELED', 'PENDING']

def main():
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    while True:
        print("""Выберите необходимый пункт меню:
        1. Получить информацию о транзакциях из JSON-файла
        2. Получить информацию о транзакциях из CSV-файла
        3. Получить информацию о транзакциях из XLSX-файла""")
        try:
            user_choice_source = int(input())
            if user_choice_source in choice_out :
                print(f'\nДля обработки выбран {choice_out[int(user_choice_source)]}')
                break
            else:
                print(f"Введенный пункт {user_choice_source} отсутствует в меню. Попробуйте снова.")
        except ValueError:
            print("Пожалуйста, введите число от 1 до 3.")

    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    while True:
        print("""\nВведите статус, по которому необходимо выполнить фильтрацию. \nДоступные для фильтровки статусы:
        \nEXECUTED, CANCELED, PENDING\n\n""")
        try:
            user_choice_status = input().upper()
            if user_choice_status in statuses :
                print(f'\nДля обработки выбран {user_choice_status}')
                break
            else:
                print(f"Введенный пункт {user_choice_status} отсутствует в меню. Попробуйте снова.")
        except ValueError:
            print("Пожалуйста, введите один из трёх предложенных статусов.")

    path_to_file = os.path.join(os.path.dirname(__file__), "data", files_to_filter.get(user_choice_source))
    selected_function = menu_options[user_choice_source]
    filter_by_state(selected_function(path_to_file), user_choice_status)


    print(f'\nОперации отфильтрованы по статусу "{user_choice_status}"\n')

if __name__ == "__main__":
    main()