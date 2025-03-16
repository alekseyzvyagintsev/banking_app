import time
from typing import Any

from _pytest.capture import CaptureFixture

from src.decorators import log


@log(filename="mylog.txt")
def my_func(value: Any) -> Any:
    """Тестовая функция вызываемая в тестах декоратора
    Возвращает входящий аргумент без изменений"""
    return value


def test_transiting_decor_log_without_errors() -> None:
    """
    Тест на то, что декоратор отрабатывает
    декорируемую функцию без изменений
    """
    assert my_func(3) == 3


def test_decor_log_without_err_in_logfile() -> None:
    """
    Тест декоратора на правильность логирования в файл
    при штатном выполнении декоратора. Если декоратору
    аргументом передано имя логвайла
    """
    # Вызываем функцию
    my_func(3)

    # Проверяем содержимое log - файла
    path_to_file = "/home/alex0236889/PycharmProjects/src/tests/mylog.txt"
    with open(path_to_file, "r", encoding="utf-8") as file:
        logline = None
        for line in file:
            logline = line
        assert f"{time.asctime()} my_func Ok\n" in logline


def test_decor_log_without_err_in_konsole(capsys: CaptureFixture[str]) -> None:
    """
    Тест декоратора на правильность вывода в консоль
    при штатном выполнении декоратора. Если декоратору
    аргументом не передано имя логвайла.
    """

    @log(filename="")
    def test_function(value: Any) -> Any:
        """Тестовая функция вызываемая в тестах декоратора
        Возвращает входящий аргумент без изменений"""
        return value

    # Вызываем функцию
    test_function(3)

    # Проверяем вывод в консоль
    captured = capsys.readouterr()
    assert captured.out == f"{time.asctime()} test_function Ok\n"


##########################################################################################
