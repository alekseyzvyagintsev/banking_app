###########################################################################
from typing import Optional


def get_mask_card_number(card_number: Optional[int] = None) -> str:
    """
    Функция get_mask_card_number принимает на вход номер карты в виде 16-ти значное числа
    и выводит замаскированный вариант в формате XXXX XX** **** XXXX
    """
    card_number_str = str(card_number)
    if type(card_number) is not int:
        return "Введите 16-ти значное число"
    elif len(card_number_str) != 16:
        return "Введите 16-ти значное число"
    else:
        return f"{card_number_str[0:4]} {card_number_str[4:6]}** **** {card_number_str[-4:]}"


def get_mask_account(account_number: Optional[int] = None) -> str:
    """
    Функция принимает на вход 20-ти значное число (номер счета)
    и возвращает маску номера по правилу **XXXX
    """
    account_number_str = str(account_number)
    if type(account_number) is not int:
        return "Введите 20-ти значное число"
    elif len(account_number_str) != 20:
        return "Введите 20-ти значное число"
    else:
        return f"**{account_number_str[-4:]}"

#####################################################################
