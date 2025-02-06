from typing import Optional

from masks import get_mask_account, get_mask_card_number


def mask_account_card(account_card: Optional[str] = None) -> str:
    """
    Принимать один аргумент — строку, содержащую тип и номер карты или счета.
    Возвращать строку с замаскированным номером.
    """
    if account_card is None:
        return "Принимать один аргумент — строку, содержащую тип и номер карты или счета."
    elif "Счет" in account_card:
        result = get_mask_account(int(account_card[-20:]))
        return f"{account_card[0:-20]}{result}"
    else:
        result = get_mask_card_number(int(account_card[-16:]))
        return f"{account_card[0:-16]}{result}"


def get_date(date_and_time: Optional[str] = None) -> str:
    """
    принимает на вход строку с датой в формате
    "2024-03-11T02:26:18.671407"
    и возвращает строку с датой в формате
    "ДД.ММ.ГГГГ"
    """
    if date_and_time is None:
        return "принимает на вход строку с датой в формате '2024-03-11T02:26:18.671407'"
    else:
        split_date_and_time = date_and_time.split("T")
        split_date = split_date_and_time[0].split("-")
        return f"{split_date[2]}.{split_date[1]}.{split_date[0]}"
