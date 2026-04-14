###########################################################################################################
import os
from typing import Any

from src.generators import filter_by_currency
from src.processing import filter_by_state, sort_by_date, filter_by_description
from src.utils import get_json_data, get_xlsx_data, get_csv_data

menu_options = {
    1: get_json_data,
    2: get_csv_data,
    3: get_xlsx_data
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

######################################################################################################

def main():
    filtered_by_state = []
    user_list = []
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")

    # Выбираем из какого файла считывать данные транзакций.
    while True:
        print("""Выберите необходимый пункт меню:
        1. Получить информацию о транзакциях из JSON-файла
        2. Получить информацию о транзакциях из CSV-файла
        3. Получить информацию о транзакциях из XLSX-файла""")
        try:
            user_choice_source = int(input())
            if user_choice_source in choice_out:
                print(f'\nДля обработки выбран {choice_out[int(user_choice_source)]}')
                break
            else:
                print(f"Введенный пункт {user_choice_source} отсутствует в меню. Попробуйте снова.")
        except ValueError:
            print("Пожалуйста, введите число от 1 до 3.")

######################################################################################################

    # Выбираем по какому статусу фильтровать полученный список транзакций.
    while True:
        print("""\nВведите статус, по которому необходимо выполнить фильтрацию. \nДоступные для фильтровки статусы:
        \nEXECUTED, CANCELED, PENDING\n""")
        user_choice_state = input().upper()
        if user_choice_state in statuses:
            try:
                print(f'\nДля обработки выбран {user_choice_state}')
                break
            except ValueError:
                print("Пожалуйста, введите один из трёх предложенных статусов.")
        else:
            print(f'Статус операции {user_choice_state} недоступен.')

    path_to_file: str = os.path.join(os.path.dirname(__file__), "data", files_to_filter.get(user_choice_source))

######################################################################################################

    # Получаем данные из выбранного файла и фильтруем по выбранному статусу.
    try:
        selected_function = menu_options[user_choice_source]
        operations_data: list | None = selected_function(path_to_file)
        filtered_by_state: list[Any] = filter_by_state(operations_data, user_choice_state)
        user_list = filtered_by_state
    except Exception as ex:
        print(f'Возникла ошибка: {ex}')

######################################################################################################

    if user_list:
        print(f'Операции отфильтрованы по статусу "{user_choice_state}"\n')

        while True:
            # Выбираем фильтровать по дате или нет.
            print('Отсортировать операции по дате? Да/Нет')
            user_choice_for_sort = (input()).lower()
            if user_choice_for_sort == 'да' or user_choice_for_sort == 'нет':
                if user_choice_for_sort == 'да':
                    try:
                        while True:
                            # Сортируем по убыванию или возрастанию.
                            print('Отсортировать по возрастанию или по убыванию?')
                            user_choice_sort_up_or_down = (input()).lower()
                            if (user_choice_sort_up_or_down == 'по возрастанию'
                                or user_choice_sort_up_or_down == 'по убыванию'):
                                try:
                                    if user_choice_sort_up_or_down == 'по возрастанию':
                                        sorted_by_date: list[dict[str, Any]] = (
                                            sort_by_date(filtered_by_state, False))
                                        user_list = sorted_by_date
                                        break
                                    else:
                                        sorted_by_date: list[dict[str, Any]] = sort_by_date(filtered_by_state)
                                        user_list = sorted_by_date
                                        break
                                except Exception as ex:
                                    print(f'Возникла ошибка: {ex}')
                                    break
                            else:
                                print('Можно выбрать только: по возрастанию / по убыванию')
                    except UnicodeDecodeError:
                        print('Переключите раскладку и попробуйте снова')
                    break
                else:
                    break
            else:
                print('Можно выбрать только: Да/Нет')

        ###################################################################################################

        if user_list:
            while True:
                # Выбираем в какой валюте выводить транзакции.
                print('Выводить только рублевые транзакции? Да/Нет')
                user_choice_currency_code = (input()).lower()

                if user_choice_currency_code == 'да' or user_choice_currency_code == 'нет':
                    try:
                        if user_choice_currency_code == 'да':
                            filtered_by_currency = filter_by_currency(user_list, 'RUB')
                            user_list = filtered_by_currency
                            break
                    except Exception as ex:
                        print(f'Возникла ошибка: {ex}')
                        break
                    break
                else:
                    print('Можно выбрать только: Да/Нет')

        ###################################################################################################

        if user_list:
            while True:
                # Выбираем фильтровать ли список по описанию.
                print('Отфильтровать список транзакций по определенному слову в описании? Да/Нет')
                user_choice_filter_by_descriptions = (input()).lower()

                if user_choice_filter_by_descriptions == 'да' or user_choice_filter_by_descriptions == 'нет':
                    if user_choice_filter_by_descriptions == 'да':
                        user_string = input('Введите слово для поиска транзакций: ').lower()
                        filtered_by_description = filter_by_description(user_list, search_string=user_string)
                        user_list = filtered_by_description
                        break
                    else:
                        break
                else:
                    print('Можно выбрать только: Да/Нет')

        ###################################################################################################

        # Распечатываем итоговый список.
        print('Распечатываю итоговый список транзакций...')
        print(list(user_list))
    else:
        print(f'С выбранным статусом ({user_choice_state}) ничего не найдено.')
        print(list(user_list))

###########################################################################################################

if __name__ == "__main__":
    main()

############################################################################################################
