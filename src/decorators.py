#######################################################################
import os
import time
from typing import Any, Callable

from functools import wraps


def log(filename: Any=None) -> Callable:
    def decorator(function: Any) -> Any:
        @wraps(function)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                result: Any = function(*args, **kwargs)
                log_message: str = f"{time.asctime()} {function.__name__} Ok\n"
            except Exception as e:
                result = None
                log_message: str = f"{time.asctime()} {function.__name__} error: {type(e).__name__}. Explanation {e}\n"
            if filename:
                path_to_file = os.path.join(os.path.dirname(os.path.dirname(__file__)),"tests", filename)
                with open(path_to_file, "a", encoding="utf-8") as file:
                    file.write(f"{log_message}\n")
            else:
                print(log_message)
            return result
        return wrapper
    return decorator


if __name__ == '__main__':
    @log(filename="mylog.txt")
    def square():
        """ Возведение числа в квадрат"""
        return value ** 2



    print(square(0))
