#######################################################################
import json
import os
import time
# from datetime import datetime
from functools import wraps
from typing import Any, Optional

import pandas as pd

from src.logging_decorators import logger


def log(filename: Any) -> Any:
    """Декоратор для применения в журналировании любых функций"""

    def decorator(function: Any) -> Any:
        @wraps(function)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            logging_string = ""
            try:
                result: Any = function(*args, **kwargs)
                logging_string: str = f"{time.asctime()} {function.__name__} Ok"
            except Exception as e:
                result = None
                logging_string: str = (
                    f"{time.asctime()} {function.__name__} error: {type(e).__name__}. Explanation {e}"
                )
            if filename:
                path_to_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs", filename)
                with open(path_to_file, "a", encoding="utf-8") as file:
                    file.write(f"{logging_string}\n")
            else:
                print(logging_string)
            return result

        return wrapper

    return decorator


# if __name__ == "__main__":
#
#     @log(filename="mylog.txt")
#     def my_func(value: Any) -> Any:
#         """Возведение числа в квадрат"""
#         return value
#
#     print(my_func())


######################################################################################################################
def report_decorator(filename: Optional[str] = None):
    """Декоратор для записи результатов функции в файл.
    Если filename не указан, используется имя файла по умолчанию."""

    def decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            global default_filename, custom_filename
            result = function(*args, **kwargs)

            if filename is None:
                logger.info("Имя файла генерируется автоматически")
                default_filename = f"{function.__name__}_{time.asctime()}.txt"
                file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", default_filename)
            else:
                logger.info("Добавляем дату и время к указанному файлу")
                custom_filename = f"{os.path.splitext(filename)[0]}_{time.asctime()}{os.path.splitext(filename)[1]}"
                file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", custom_filename)

            output_filename = default_filename or custom_filename

            logger.info("Записываем данные в файл")
            with open(file_path, "a") as file:
                if isinstance(result, pd.DataFrame):
                    # Сохранение DataFrame в JSON
                    data = result.to_dict(orient="records")
                    json.dump(data, file, ensure_ascii=False, indent=4)

                logger.info(f"Результаты сохранены в файл: {output_filename}")

            return result

        return wrapper

    return decorator


######################################################################################################################
# if __name__ == "__main__":
#     # Пример использования декоратора без параметра
#     @report_decorator()
#     def generate_report():
#         return "Это тестовый отчет!"
#
#
#     print(generate_report())
#
#     # Пример использования декоратора с параметром
#     @report_decorator("my_report.txt")
#     def generate_custom_report():
#         return "Это кастомный отчет!"
#
#
#     print(generate_custom_report())

######################################################################################################################
