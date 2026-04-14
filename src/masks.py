###########################################################################
from typing import Optional

from src.logging_masks import logger


def get_mask_card_number(card_number: Optional[int] = None) -> str:
    """
    Функция get_mask_card_number принимает на вход номер карты в виде 16-ти значное числа
    и выводит замаскированный вариант в формате XXXX XX** **** XXXX
    """
    # Регистрация входных данных
    logger.info(f"Входные данные: card_number={card_number}")

    # Проверка типа аргумента
    if type(card_number) is not int:
        logger.warning("Тип аргумента не является целым числом.")
        return "Введите 16-ти значное число"

    # Преобразование аргумента в строку
    card_number_str = str(card_number)

    # Проверка длины строки
    if len(card_number_str) != 16:
        logger.warning("Длина строки не равна 16 символам.")
        return "Введите 16-ти значное число"

    # Форматирование номера карты
    masked_card_number = f"{card_number_str[0:4]} {card_number_str[4:6]}** **** {card_number_str[-4:]}"

    # Регистрация результата
    logger.info(f"Маскированный номер карты: {masked_card_number}")

    return masked_card_number


def get_mask_account(account_number: Optional[int] = None) -> str:
    """
    Функция принимает на вход 20-ти значное число (номер счета)
    и возвращает маску номера по правилу **XXXX
    """
    # Регистрация входных данных
    logger.info(f"Входные данные: card_number={get_mask_account}")

    # Проверка типа аргумента
    if type(account_number) is not int:
        logger.warning("Тип аргумента не является целым числом.")
        return "Введите 20-ти значное число"

    # Преобразование аргумента в строку
    account_number_str = str(account_number)

    # Проверка длины строки
    if len(account_number_str) != 20:
        logger.warning("Длина строки не равна 16 символам.")
        return "Введите 20-ти значное число"

    # Регистрация результата
    logger.info(f"Маскированный номер карты: {get_mask_account}")

    # Форматирование номера карты
    return f"**{account_number_str[-4:]}"


#####################################################################
