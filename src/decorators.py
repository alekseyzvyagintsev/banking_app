#######################################################################
import os
import time
from functools import wraps
from typing import Any
from logging_config import logger


def log(filename: Any) -> Any:
    def decorator(function: Any) -> Any:
        @wraps(function)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                result: Any = function(*args, **kwargs)
                logging_string: str = f"{time.asctime()} {function.__name__} Ok"
            except Exception as e:
                result = None
                logging_string: str = (
                    f"{time.asctime()} {function.__name__} error: {type(e).__name__}. Explanation {e}"
                )
            if filename:
                path_to_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), "tests", filename)
                with open(path_to_file, "a", encoding="utf-8") as file:
                    file.write(f"{logging_string}\n")
            else:
                print(logging_string)
            return result

        return wrapper

    return decorator


def log_function_decorator(function: Any) -> Any:
    @wraps(function)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        try:
            result_local: Any = function(*args, **kwargs)
            logger.debug(f"{time.asctime()} {function.__name__} Ok")
        except Exception as e:
            result_local: Any = None
            logger.debug(
                f"{time.asctime()} {function.__name__} error: {type(e).__name__}. Explanation {e}"
            )
        return result_local
    return wrapper


if __name__ == "__main__":

    @log(filename="mylog.txt")
    def my_func(value: Any) -> Any:
        """Возведение числа в квадрат"""
        return value

    print(my_func())

###################################################################################
