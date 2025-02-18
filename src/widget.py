import datetime

from typing import Optional

from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(account_card: Optional[str] = None) -> str:
    """
    Принимает один аргумент — строку, содержащую тип и номер карты или счета.
    Возвращать строку с замаскированным номером.
    """
    if account_card is None:
        return "Ожидается не пустая строка"
    elif type(account_card) != str:
        return f"Ожидается строка, это ({account_card}) не строка"
    else:
        split_account_card = list(account_card.split(" "))
        if (split_account_card[-1]) != "":
            if len(split_account_card[-1]) == 20 and len(split_account_card[-1]) == 16:
                return "Функция принимает один аргумент — строку, содержащую тип и номер карты или счета."
            elif len(split_account_card[-1]) == 20:
                result = get_mask_account(int(split_account_card[-1]))
                return f"{account_card[0:-20]}{result}"
            elif len(split_account_card[-1]) == 16:
                result = get_mask_card_number(int(split_account_card[-1]))
                return f"{account_card[0:-16]}{result}"
            else:
                return f"Номер карты = 16-ти символам, а счета 20-ти. Здесь ({account_card}) не правильно"
        else:
            return "Номер карты или счета должен быть без пробелов и других симболов после номера."


def get_date(date_and_time: Optional[str] = None) -> str:
    """
    принимает на вход строку с датой в формате
    "2024-03-11T02:26:18.671407" (ISO8601)
    и возвращает строку с датой в формате
    "ДД.ММ.ГГГГ"
    """

    try:
        datetime.datetime.strptime(date_and_time, "%Y-%m-%dT%H:%M:%S.%f")
    except ValueError:
        return "Ожидается строка в формате '2024-03-11T02:26:18.671407'. Это {date_and_time} не правильный формат"
    except TypeError:
        return "Ожидается строка в формате '2024-03-11T02:26:18.671407'. Это {date_and_time} не строка"
    else:
        split_date_and_time = date_and_time.split("T")
        split_date = split_date_and_time[0].split("-")
        return f"{split_date[2]}.{split_date[1]}.{split_date[0]}"
